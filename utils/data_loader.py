from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

try:
    import streamlit as st
except ImportError:  # validation can still inspect data without optional UI packages
    st = None


APP_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = APP_DIR / "data"


def _read_json(name: str) -> dict[str, Any]:
    with (DATA_DIR / name).open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def _read_mapping() -> list[dict[str, str]]:
    with (DATA_DIR / "M2_AXIS_MAPPING.csv").open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


if st is not None:
    load_core_data = st.cache_data(show_spinner=False)(_read_json)
    load_full_data = st.cache_data(show_spinner="전체 후보 데이터를 불러오는 중입니다…")(_read_json)
    load_m2_mapping = st.cache_data(show_spinner=False)(_read_mapping)
else:
    def load_core_data(name: str = "frontend_core.json") -> dict[str, Any]:
        return _read_json(name)

    def load_full_data(name: str = "frontend_data.json") -> dict[str, Any]:
        return _read_json(name)

    def load_m2_mapping() -> list[dict[str, str]]:
        return _read_mapping()


def candidate_index(data: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    return {
        (str(row.get("region_code", "")), str(row.get("analysis_code", ""))): row
        for row in data.get("candidates", [])
    }


def matching_candidate(anchor: dict[str, Any], data: dict[str, Any]) -> dict[str, Any]:
    identity = anchor.get("identity", {})
    key = (str(identity.get("region_code", "")), str(identity.get("analysis_code", "")))
    return candidate_index(data).get(key, {})


def m2_axis_values(anchor: dict[str, Any], data: dict[str, Any], mapping: list[dict[str, str]]) -> list[dict[str, Any]]:
    candidate = matching_candidate(anchor, data)
    diagnosis = anchor.get("diagnosis", {}).get("M2", {})
    rows: list[dict[str, Any]] = []
    for axis in sorted(mapping, key=lambda row: int(row.get("axis_order", 99))):
        saved = axis.get("final_saved_variable", "")
        value = candidate.get(f"m2_source__{saved}", diagnosis.get(saved))
        try:
            numeric = float(value) if value not in (None, "") else None
        except (TypeError, ValueError):
            numeric = None
        rows.append({"축": axis.get("korean_display_name", saved), "값": numeric, "설명": axis.get("interpretation", "")})
    return rows
