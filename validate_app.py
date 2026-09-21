from __future__ import annotations

import ast
import csv
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any


APP_DIR = Path(__file__).resolve().parent
FINAL_DIR = APP_DIR.parent
FRONTEND_DIR = APP_DIR / "data"
RESULT_PATH = APP_DIR / "app_validation.csv"
BASELINE_PATH = APP_DIR / "protected_analysis_hashes.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def count_unique_cases(cases: list[dict[str, Any]]) -> int:
    return len({str(row.get("case_id", "")) for row in cases if row.get("case_id")})


def python_imports() -> set[str]:
    names: set[str] = set()
    for path in APP_DIR.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                names.add(node.module.split(".")[0])
    return names


def render_interfaces() -> dict[str, tuple[list[str], int]]:
    """Return each component render parameter list and its app.py positional call count."""
    app_tree = ast.parse((APP_DIR / "app.py").read_text(encoding="utf-8"), filename="app.py")
    call_counts: dict[str, int] = {}
    for node in ast.walk(app_tree):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
            continue
        owner = node.func.value
        if node.func.attr == "render" and isinstance(owner, ast.Name):
            call_counts[owner.id] = len(node.args)

    interfaces: dict[str, tuple[list[str], int]] = {}
    for component in ["home", "explorer", "candidates", "core9", "portfolio", "validation", "methodology"]:
        path = APP_DIR / "components" / f"{component}.py"
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        definition = next(
            node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == "render"
        )
        parameters = [argument.arg for argument in definition.args.args]
        interfaces[component] = (parameters, call_counts.get(component, -1))
    return interfaces


def main() -> int:
    results: list[dict[str, str]] = []

    def check(item: str, expected: Any, actual: Any, ok: bool, detail: str = "") -> None:
        results.append({"검증항목": item, "기대값": str(expected), "실제값": str(actual), "상태": "PASS" if ok else "FAIL", "설명": detail})

    core_path = FRONTEND_DIR / "frontend_core.json"
    data_path = FRONTEND_DIR / "frontend_data.json"
    mapping_path = FRONTEND_DIR / "M2_AXIS_MAPPING.csv"
    check("app.py 존재", True, (APP_DIR / "app.py").exists(), (APP_DIR / "app.py").exists())
    check("requirements.txt 존재", True, (APP_DIR / "requirements.txt").exists(), (APP_DIR / "requirements.txt").exists())

    asset_manifest = read_json(FRONTEND_DIR / "asset_hashes.json")
    missing_assets = [name for name in asset_manifest if not (FRONTEND_DIR / name).exists()]
    changed_assets = [name for name, expected in asset_manifest.items() if (FRONTEND_DIR / name).exists() and sha256(FRONTEND_DIR / name) != expected]
    check("배포 필수 asset", "누락 0", f"누락 {len(missing_assets)}", not missing_assets, ", ".join(missing_assets))
    check("배포 asset SHA256", "불일치 0", f"불일치 {len(changed_assets)}", not changed_assets, ", ".join(changed_assets))

    expected_render_parameters = {
        "home": ["core", "full_data", "navigate"],
        "explorer": ["data", "mapping"],
        "candidates": ["data"],
        "core9": ["core", "data", "mapping"],
        "portfolio": ["core"],
        "validation": ["core"],
        "methodology": ["core", "mapping"],
    }
    for component, (parameters, call_count) in render_interfaces().items():
        expected = expected_render_parameters[component]
        actual = f"definition={parameters}, app_call_args={call_count}"
        check(
            f"{component.upper()}_RENDER_SIGNATURE_MATCH",
            f"definition={expected}, app_call_args={len(expected)}",
            actual,
            parameters == expected and call_count == len(expected),
            "app.py 호출부와 component render 정의의 positional interface 대조",
        )

    core, data, mapping = read_json(core_path), read_json(data_path), read_csv(mapping_path)
    check("frontend_core JSON 로드", "성공", "성공", isinstance(core, dict))
    check("frontend_data JSON 로드", "성공", "성공", isinstance(data, dict))
    anchors = core.get("core_anchors", [])
    candidates = data.get("candidates", [])
    regions = data.get("regions", [])
    linkage_count = sum(len(anchor.get("portfolio", {}).get("linkages", [])) for anchor in anchors)
    protection_count = sum(1 for anchor in anchors if anchor.get("portfolio", {}).get("protection"))
    priority_count = sum(str(anchor.get("decision", {}).get("priority_field_review", "")).lower() == "true" for anchor in anchors)
    external = core.get("real_world_validation", {})
    cases = external.get("cases", [])
    check("핵심 후보 수", 9, len(anchors), len(anchors) == 9)
    check("공식 후보 수", 460, len(candidates), len(candidates) == 460)
    check("분석 지역 수", 255, len(regions), len(regions) == 255)
    check("Linkage 수", 27, linkage_count, linkage_count == 27)
    check("Protection 수", 9, protection_count, protection_count == 9)
    check("우선 현장검토 수", 6, priority_count, priority_count == 6)
    check("외부 사례 수", 3, count_unique_cases(cases), count_unique_cases(cases) == 3, f"저장 결과 행 {len(cases)}개")
    direct = external.get("direct_validation_of_core9")
    check("외부 사례의 core9 직접 검증 여부", False, direct, direct is False)
    check("M2 표시 매핑 수", 6, len(mapping), len(mapping) == 6)

    required_saved = {row.get("final_saved_variable") for row in mapping}
    candidate_keys = set().union(*(row.keys() for row in candidates)) if candidates else set()
    missing_axes = sorted(name for name in required_saved if f"m2_source__{name}" not in candidate_keys)
    check("M2 6축 저장값 연결", "누락 0", f"누락 {len(missing_axes)}", not missing_axes, ", ".join(missing_axes))

    py_files = list(APP_DIR.rglob("*.py"))
    absolute_pattern = re.compile(r"[A-Za-z]:[\\/]Users[\\/]")
    absolute_hits = [str(path.relative_to(APP_DIR)) for path in py_files if absolute_pattern.search(path.read_text(encoding="utf-8"))]
    check("절대 Windows 사용자 경로", "0건", f"{len(absolute_hits)}건", not absolute_hits, ", ".join(absolute_hits))

    deployment_text_files = [
        *APP_DIR.rglob("*.py"), *APP_DIR.rglob("*.md"), *APP_DIR.rglob("*.toml"),
        *APP_DIR.rglob("*.txt"), *APP_DIR.rglob("*.json"), *APP_DIR.rglob("*.csv"),
    ]
    deployment_text_files = [path for path in deployment_text_files if "__pycache__" not in path.parts and path.name not in {"app_validation.csv", "ui_validation.csv"}]
    windows_dependency_hits: list[str] = []
    onedrive_hits: list[str] = []
    secret_hits: list[str] = []
    secret_pattern = re.compile(r"(?:sk-[A-Za-z0-9_-]{20,}|ghp_[A-Za-z0-9]{20,}|AIza[A-Za-z0-9_-]{20,}|AKIA[A-Z0-9]{16}|(?:api[_-]?key|token|secret)\s*[:=]\s*['\"][^'\"]{8,})", re.I)
    for path in deployment_text_files:
        source = path.read_text(encoding="utf-8-sig", errors="ignore")
        relative = str(path.relative_to(APP_DIR))
        if absolute_pattern.search(source):
            windows_dependency_hits.append(relative)
        if re.search(r"[A-Za-z]:[\\/][^\r\n\"]*OneDrive", source, re.I):
            onedrive_hits.append(relative)
        if secret_pattern.search(source):
            secret_hits.append(relative)
    check("배포 절대경로 의존성", "0건", f"{len(windows_dependency_hits)}건", not windows_dependency_hits, ", ".join(windows_dependency_hits))
    check("배포 OneDrive 의존성", "0건", f"{len(onedrive_hits)}건", not onedrive_hits, ", ".join(onedrive_hits))
    check("배포 민감정보 패턴", "0건", f"{len(secret_hits)}건", not secret_hits, ", ".join(secret_hits))

    # Positive claims only. Negated interpretive cautions in official JSON are not violations.
    banned = ["성공" + " 보장", "반드시" + " 출점", "최적" + " 입지", "예상" + " 매출", "매출 증가" + " 보장", "인과효과" + " 입증", "Anchor가 주변 매출을" + " 증가", "TOP" + "6", "전국" + " 1위"]
    user_files = [path for path in py_files if path.name != Path(__file__).name] + [APP_DIR / "README.md"]
    claim_hits: list[str] = []
    for path in user_files:
        source = path.read_text(encoding="utf-8")
        for phrase in banned:
            if phrase in source:
                claim_hits.append(f"{path.relative_to(APP_DIR)}:{phrase}")
    check("사용자-facing 과장 표현", "0건", f"{len(claim_hits)}건", not claim_hits, "; ".join(claim_hits))

    required_packages = {"streamlit", "pandas", "plotly"}
    missing_packages = sorted(name for name in required_packages if importlib.util.find_spec(name) is None)
    check("필수 외부 패키지 import", "누락 0", f"누락 {len(missing_packages)}", not missing_packages, ", ".join(missing_packages))
    local_imports_ok = all((APP_DIR / name).exists() or (APP_DIR / f"{name}.py").exists() or name not in {"components", "utils", "styles"} for name in python_imports())
    check("로컬 모듈 경로", "정상", "정상" if local_imports_ok else "누락", local_imports_ok)

    baseline = read_json(BASELINE_PATH)
    changed: list[str] = []
    missing: list[str] = []
    for relative, expected_hash in baseline.items():
        path = FINAL_DIR / Path(relative)
        if not path.exists():
            missing.append(relative)
        elif sha256(path) != expected_hash:
            changed.append(relative)
    check("보호된 FINAL 분석파일 hash", "변경 0 / 누락 0", f"변경 {len(changed)} / 누락 {len(missing)}", not changed and not missing, "; ".join(changed + missing))

    with RESULT_PATH.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["검증항목", "기대값", "실제값", "상태", "설명"])
        writer.writeheader()
        writer.writerows(results)
    counts = {status: sum(row["상태"] == status for row in results) for status in ["PASS", "WARN", "FAIL"]}
    print(json.dumps(counts, ensure_ascii=False))
    for row in results:
        print(f"{row['상태']}: {row['검증항목']} — {row['실제값']}")
    return 1 if counts["FAIL"] else 0


if __name__ == "__main__":
    sys.exit(main())
