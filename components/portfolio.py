from __future__ import annotations

import streamlit as st

from utils.formatting import number, text, truthy


def _kpi_items(value: object) -> str:
    items = [item.strip() for item in text(value, "").split("|") if item.strip()]
    return '<ul class="kpi-items">' + "".join(f"<li>{item}</li>" for item in items) + "</ul>"


def render(core: dict) -> None:
    st.markdown('<div class="page-head"><div class="eyebrow">LOCAL STRATEGY</div><div class="page-title">지역에 맞는 실행 전략</div><p class="page-subtitle">지역과 Anchor를 선택해 연계 지원 검토 업종, 보호 모니터링 대상과 BC 공동혜택을 확인하세요.</p></div>', unsafe_allow_html=True)
    anchors = core.get("core_anchors", [])
    labels = [f"{a.get('identity',{}).get('sido','')} {a.get('identity',{}).get('sigungu','')} · {a.get('identity',{}).get('anchor_industry','')}" for a in anchors]
    if not labels:
        st.info("표시할 지역 전략이 없습니다.")
        return
    selected = st.selectbox("지역·Anchor 선택", labels, key="portfolio_select")
    anchor = anchors[labels.index(selected)]
    identity, ranking, decision = anchor.get("identity", {}), anchor.get("ranking", {}), anchor.get("decision", {})
    priority = truthy(decision.get("priority_field_review"))
    st.markdown(f'<div class="detail-hero"><div class="detail-main"><span class="pill {"priority" if priority else ""}">{"우선 현장검토" if priority else "핵심 강건후보"}</span><h2>{identity.get("sido","")} {identity.get("sigungu","")} · {text(identity.get("anchor_industry"))}</h2><p>{text(anchor.get("peer",{}).get("name"))}</p></div><div class="detail-stat"><span>M4 공식 점수</span><strong>{number(ranking.get("official_m4_score"))}</strong></div><div class="detail-stat"><span>Peer 내 순위</span><strong>{number(ranking.get("peer_rank"),0)}위</strong></div><div class="detail-stat"><span>실행유형</span><strong>{text(anchor.get("action",{}).get("type"))}</strong></div></div>', unsafe_allow_html=True)
    portfolio, action = anchor.get("portfolio", {}), anchor.get("action", {})
    links = portfolio.get("linkages", [])
    protection = portfolio.get("protection", {})
    html = f'<div class="strategy-map"><div class="strategy-anchor"><b>ANCHOR</b><br>{text(portfolio.get("anchor"))}</div><div class="strategy-line"></div><div class="strategy-links">'
    html += "".join(f'<div class="strategy-link"><b>{text(x.get("industry"))}</b><br><span class="small-muted">연계 지원 검토 · {text(x.get("robustness"))}</span></div>' for x in links)
    html += f'</div><div class="strategy-line"></div><div class="strategy-protection"><b>{text(protection.get("industry"))}</b><br><span class="small-muted">보호 모니터링</span></div></div>'
    st.markdown(html, unsafe_allow_html=True)
    st.caption("업종 관계를 구조화해 보여주며, 업종 사이의 인과관계를 의미하지 않습니다.")
    st.markdown('<div class="section-title">BC 공동혜택</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="action-summary benefit-summary"><span class="pill">{text(action.get("type"))}</span><strong>BC 공동혜택 제안</strong><p>{text(action.get("bc_benefit"))}</p></div>', unsafe_allow_html=True)
    cols = st.columns(3, gap="large")
    for col, title, key in zip(cols, ["주 KPI","보조 KPI","보호 KPI"], ["primary_kpi","secondary_kpi","protection_kpi"]):
        col.markdown(f'<div class="kpi-list"><strong>{title}</strong>{_kpi_items(action.get(key))}</div>', unsafe_allow_html=True)
    with st.expander("평가 방법 자세히 보기"):
        st.write(text(action.get("evaluation_design")))
