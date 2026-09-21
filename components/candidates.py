from __future__ import annotations

import pandas as pd
import streamlit as st

from utils.formatting import number, text, truthy


def _warning(row: dict) -> str:
    fields = ["m5_warning_mapping", "m5_warning_market_size", "m5_warning_low_store", "m5_warning_low_demand", "m5_warning_tourism_context"]
    return "주의 있음" if any(truthy(row.get(field)) for field in fields) else "주의 없음"


def render(data: dict) -> None:
    st.markdown('<div class="page-head"><div class="eyebrow">CANDIDATE REVIEW</div><div class="page-title">공식 후보를 조건별로 살펴보세요</div><p class="page-subtitle">지역·업종·Peer 조건을 좁혀 후보의 공식 점수와 검토수준을 비교할 수 있습니다.</p></div>', unsafe_allow_html=True)
    rows = data.get("candidates", [])
    if not rows:
        st.info("표시할 후보 데이터가 없습니다.")
        return
    df = pd.DataFrame(rows)
    df["경고 여부"] = [_warning(row) for row in rows]
    filters = {}
    with st.container(key="candidate_filter_toolbar"):
        f1, f2, f3, f4, f5, f6 = st.columns(6)
        for col, field, label in zip([f1,f2,f3,f4,f5,f6], ["sido","sigungu","analysis_name","peer_group_name","m5_review_level","경고 여부"], ["시도","지역","업종","Peer Group","검토수준","경고"]):
            options = ["전체"] + sorted(df[field].dropna().astype(str).unique())
            filters[field] = col.selectbox(label, options, key=f"candidate_{field}")
    view = df.copy()
    for field, value in filters.items():
        if value != "전체":
            view = view[view[field].astype(str) == value]

    st.markdown(f'<div class="kpi-row" style="grid-template-columns:repeat(3,minmax(0,1fr))"><div class="kpi-card"><div class="kpi-value">{len(view):,}</div><div class="kpi-label">검색된 후보</div></div><div class="kpi-card"><div class="kpi-value">{view["sigungu"].nunique():,}</div><div class="kpi-label">포함 지역</div></div><div class="kpi-card"><div class="kpi-value">{view["analysis_name"].nunique():,}</div><div class="kpi-label">포함 업종</div></div></div>', unsafe_allow_html=True)
    st.markdown('<div class="compact-note">M4 공식 점수는 후보 비교를 위한 종합점수이며 확률값이 아닙니다. 서로 다른 Peer Group은 별도로 순위가 계산됩니다.</div>', unsafe_allow_html=True)
    display = view[["sido","sigungu","analysis_name","peer_group_name","박샘_기본점수","박샘_Peer순위","결과구분","m5_review_level","경고 여부"]].rename(columns={"sido":"시도","sigungu":"지역","analysis_name":"업종","peer_group_name":"Peer","박샘_기본점수":"M4 점수","박샘_Peer순위":"Peer 순위","결과구분":"결과구분","m5_review_level":"검토수준","경고 여부":"경고"})
    event = st.dataframe(display, hide_index=True, width="stretch", height=470, on_select="rerun", selection_mode="single-row", column_config={"M4 점수": st.column_config.NumberColumn(format="%.2f"), "Peer 순위": st.column_config.NumberColumn(format="%d")})
    indices = event.selection.rows if event and event.selection else []
    if indices:
        row = view.iloc[indices[0]].to_dict()
        st.markdown('<div class="section-title">선택 후보</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="detail-hero"><div class="detail-main"><span class="pill">{text(row.get("m5_review_level"))}</span><h2>{text(row.get("sido"))} {text(row.get("sigungu"))}</h2><p>{text(row.get("analysis_name"))} · {text(row.get("peer_group_name"))}</p></div><div class="detail-stat"><span>M4 공식 점수</span><strong>{number(row.get("박샘_기본점수"))}</strong></div><div class="detail-stat"><span>Peer 내 순위</span><strong>{number(row.get("박샘_Peer순위"),0)}위</strong></div><div class="detail-stat"><span>전략 방향</span><strong>{text(row.get("m5_strategy_type"))}</strong></div></div>', unsafe_allow_html=True)

