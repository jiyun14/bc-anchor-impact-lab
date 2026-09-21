from __future__ import annotations

import streamlit as st

from utils.formatting import number, text, truthy


def _cards(anchors: list[dict]) -> None:
    for start in range(0, len(anchors), 3):
        cols = st.columns(3)
        for col, anchor in zip(cols, anchors[start:start + 3]):
            identity = anchor.get("identity", {})
            ranking = anchor.get("ranking", {})
            decision = anchor.get("decision", {})
            priority = truthy(decision.get("priority_field_review"))
            warnings = anchor.get("warnings", []) or []
            warning_label = f"주의사항 {len(warnings)}건" if warnings else "주의사항 없음"
            key = f"{identity.get('region_code')}_{identity.get('analysis_code')}"
            with col:
                with st.container(key=f"anchor_item_{key}"):
                    st.markdown(
                        f'<div class="anchor-card">'
                        f'<span class="pill {"priority" if priority else ""}">{"우선 현장검토" if priority else "핵심 강건후보"}</span>'
                        f'<h3>{identity.get("sido", "")} {identity.get("sigungu", "")}</h3>'
                        f'<div class="anchor-industry">{text(identity.get("anchor_industry"))}</div>'
                        f'<div class="anchor-peer">{text(anchor.get("peer", {}).get("name"))}</div>'
                        f'<div class="anchor-score"><div><strong>{number(ranking.get("official_m4_score"), 2)}</strong><br><span>M4 공식 점수</span></div>'
                        f'<span>Peer 내 {number(ranking.get("peer_rank"), 0)}위</span></div>'
                        f'<div class="anchor-meta"><span>{text(anchor.get("action", {}).get("type"))}</span><span>{warning_label}</span></div>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )


def render(core: dict, data: dict, mapping: list[dict]) -> None:
    del data, mapping
    st.markdown(
        '<div class="page-head"><div class="eyebrow">CORE ANCHORS</div>'
        '<div class="page-title">핵심 Anchor 9</div>'
        '<p class="page-subtitle">다양한 조건에서도 결과가 유지된 9개 후보를 한눈에 비교할 수 있습니다.</p></div>',
        unsafe_allow_html=True,
    )
    anchors = core.get("core_anchors", [])
    if not anchors:
        st.info("표시할 핵심 후보가 없습니다.")
        return
    _cards(anchors)
