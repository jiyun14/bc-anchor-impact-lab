from __future__ import annotations

from collections.abc import Callable

import pandas as pd
import streamlit as st

from utils.formatting import number, text, truthy


def render(core: dict, full_data: dict, navigate: Callable[[str], None]) -> None:
    counts = core.get("meta", {}).get("key_counts", {})
    regions = pd.DataFrame(full_data.get("regions", []))
    hero_copy, hero_visual = st.columns([1.35, 1], gap="large", vertical_alignment="center")
    with hero_copy:
        st.markdown(
            """<div class="service-hero"><h1>우리 지역에 필요한<br>다음 Anchor를 찾아보세요</h1>
            <p>유사 상권과 비교해 수요 공급 불균형을 진단하고,<br>검토할 중심 업종과 실행 전략을 확인합니다.</p></div>""",
            unsafe_allow_html=True,
        )
        st.markdown('<div class="search-title"><span>⌖</span> 지역 탐색 시작</div>', unsafe_allow_html=True)
        search1, search2 = st.columns(2, vertical_alignment="bottom")
        sido_options = sorted(regions["sido"].dropna().astype(str).unique()) if not regions.empty else []
        sido = search1.selectbox("시도", sido_options, index=None, placeholder="시도 선택", key="home_sido")
        scoped = regions[regions["sido"].astype(str) == sido] if sido else regions.iloc[0:0]
        sigungu_options = sorted(scoped["sigungu"].dropna().astype(str).unique()) if sido else []
        sigungu = search2.selectbox("시군구", sigungu_options, index=None, placeholder="시군구 선택", key="home_sigungu", disabled=not sido)
        if st.button("상권 분석하기 →", type="primary", key="home_region_start", disabled=not sigungu, width="stretch"):
            st.session_state["explorer_sido"] = sido
            st.session_state["explorer_sigungu"] = sigungu
            navigate("상권 탐색")
            st.rerun()
    with hero_visual:
        st.markdown(
            """<div class="location-visual" aria-hidden="true">
            <div class="orbit orbit-one"></div><div class="orbit orbit-two"></div><div class="orbit orbit-three"></div>
            <i class="data-point point-one"></i><i class="data-point point-two"></i><i class="data-point point-three"></i>
            <div class="location-pin"><span></span></div>
            <div class="insight-chip"><b>지역의 새로운 기회</b><small>데이터로 발견하는 Anchor</small></div>
            </div>""",
            unsafe_allow_html=True,
        )

    stats = [
        (counts.get("regions"), "분석 지역"),
        (counts.get("official_candidates"), "공식 후보"),
        (counts.get("peer_top10_combined"), "Peer 상위 후보"),
        (counts.get("core_robust"), "핵심 Anchor"),
        (counts.get("priority_field_review"), "우선 현장검토"),
    ]
    st.markdown('<div class="stats-strip">' + "".join(
        f'<div class="stat-item"><i></i><div><strong>{value if value is not None else "–"}</strong><span>{label}</span></div></div>' for value, label in stats
    ) + '</div>', unsafe_allow_html=True)

    heading, all_action = st.columns([4, 1], vertical_alignment="bottom")
    heading.markdown('<div class="section-heading"><div><h2>지금 확인할 핵심 Anchor</h2><p>실제 분석 결과 중 대표적인 후보를 먼저 확인해보세요.</p></div></div>', unsafe_allow_html=True)
    if all_action.button("전체 Anchor 9 보기 →", key="home_all_anchors", type="tertiary", width="stretch"):
        navigate("Anchor 9")
        st.rerun()
    anchors = core.get("core_anchors", [])[:3]
    cols = st.columns(3, gap="medium")
    for col, anchor in zip(cols, anchors):
        identity, ranking, decision = anchor.get("identity", {}), anchor.get("ranking", {}), anchor.get("decision", {})
        with col:
            status = "우선 현장검토" if truthy(decision.get("priority_field_review")) else "핵심 강건후보"
            st.markdown(f'<div class="preview-row"><span class="status-badge">{status}</span><h3>{text(identity.get("sido"))} {text(identity.get("sigungu"))}</h3><strong>{text(identity.get("anchor_industry"))}</strong><p><span>{text(anchor.get("peer",{}).get("name"))}</span><b>Peer 내 {number(ranking.get("peer_rank"),0)}위</b></p></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading secondary"><div><h2>어떻게 찾았나요?</h2><p>결과를 만들기까지의 분석 흐름입니다.</p></div></div>', unsafe_allow_html=True)
    steps = [("M1","진단","수요·공급 구조"),("M2","지표화","비교 가능한 6개 축"),("M3","유사 상권 비교","같은 구조끼리 비교"),("M4","후보 선별","우선순위와 강건성"),("M5","실행 전략","지역별 실행 방향")]
    st.markdown('<div class="method-line">' + ''.join(f'<div><i>{index}</i><small>{code}</small><b>{title}</b><span>{copy}</span></div>' for index,(code,title,copy) in enumerate(steps,1)) + '</div>', unsafe_allow_html=True)
    st.caption("M4 공식 점수는 확률값이 아니며, 실제 실행 전에는 임대료·입지·현장 경쟁 상황을 함께 확인해야 합니다.")
