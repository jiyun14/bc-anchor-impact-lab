from __future__ import annotations

from typing import Any


MISSING = "데이터 없음"


def present(value: Any) -> bool:
    return value is not None and str(value).strip() not in {"", "nan", "None", "null"}


def text(value: Any, fallback: str = MISSING) -> str:
    return str(value).strip() if present(value) else fallback


def number(value: Any, digits: int = 2, fallback: str = MISSING) -> str:
    if not present(value):
        return fallback
    try:
        return f"{float(value):,.{digits}f}"
    except (TypeError, ValueError):
        return text(value, fallback)


def integer(value: Any, fallback: str = MISSING) -> str:
    if not present(value):
        return fallback
    try:
        return f"{int(float(value)):,}"
    except (TypeError, ValueError):
        return text(value, fallback)


def percent(value: Any, digits: int = 1, fallback: str = MISSING) -> str:
    if not present(value):
        return fallback
    try:
        return f"{float(value):,.{digits}f}%"
    except (TypeError, ValueError):
        return text(value, fallback)


def truthy(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "y", "예", "o"}


def safe_get(data: Any, *path: str, default: Any = None) -> Any:
    current = data
    for key in path:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return current


def join_region(record: dict[str, Any]) -> str:
    parts = [text(record.get("sido"), ""), text(record.get("sigungu"), "")]
    return " ".join(part for part in parts if part) or MISSING


def warning_text(value: Any) -> str:
    if not present(value) or str(value).strip() in {"0", "False", "false", "[]"}:
        return "주의사항 없음"
    return text(value)
