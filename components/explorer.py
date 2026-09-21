from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from utils.formatting import number, text


def render(data: dict, mapping: list[dict]) -> None:
    st.markdown('<div class="page-head"><div class="eyebrow">REGION EXPLORER</div><div class="page-title">우리 지역은 어떤 상권일까?</div><p class="page-subtitle">지역을 선택하면 유사 상권 유형과 핵심 소비·공급 지표, 공식 후보 업종을 바로 확인할 수 있습니다.</p></div>', unsafe_allow_html=True)
    regions = data.get("regions", [])
    if not regions:
        st.info("표시할 지역 데이터가 없습니다.")
        return
    df = pd.DataFrame(regions)
    top1, top2, top3 = st.columns(3)
    peer_options = ["전체"] + sorted(df["peer_group_name"].dropna().astype(str).unique())
    peer = top3.selectbox("Peer Group", peer_options, key="explorer_peer")
    filtered = df if peer == "전체" else df[df["peer_group_name"].astype(str) == peer]
    sido_options = sorted(filtered["sido"].dropna().astype(str).unique())
    preset_sido = st.session_state.get("explorer_sido")
    sido_index = sido_options.index(preset_sido) if preset_sido in sido_options else None
    sido = top1.selectbox("시도", sido_options, index=sido_index, placeholder="시도를 선택하세요", key="explorer_sido_select")
    scoped = filtered[filtered["sido"].astype(str) == sido] if sido else filtered.iloc[0:0]
    sigungu_options = sorted(scoped["sigungu"].dropna().astype(str).unique()) if sido else []
    preset_sigungu = st.session_state.get("explorer_sigungu")
    sigungu_index = sigungu_options.index(preset_sigungu) if preset_sigungu in sigungu_options else None
    sigungu = top2.selectbox("시군구", sigungu_options, index=sigungu_index, placeholder="시군구를 선택하세요", disabled=not sido, key="explorer_sigungu_select")
    if not sigungu:
        counts = filtered.groupby("peer_group_name", dropna=False).size().reset_index(name="지역 수")
        fig = px.bar(counts, x="지역 수", y="peer_group_name", orientation="h", color="peer_group_name", color_discrete_sequence=["#246bfd", "#65a3ff", "#9bc3ff"])
        fig.update_layout(showlegend=False, yaxis_title=None, xaxis_title="지역 수", height=260, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#334e68"))
        fig.update_xaxes(gridcolor="#e8eef5")
        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
        st.markdown('<div class="info-banner">공식 데이터에 지역 좌표가 없어 임의 지도 대신 Peer Group 분포와 지역 선택 방식을 제공합니다.</div>', unsafe_allow_html=True)
        return

    selected = scoped[scoped["sigungu"].astype(str) == sigungu].iloc[0].to_dict()
    st.markdown(f'<div class="detail-hero"><div class="detail-main"><span class="pill">선택 지역</span><h2>{sido} {sigungu}</h2><p>{text(selected.get("peer_group_name"))}</p></div>'
                f'<div class="detail-stat"><span>안정후보</span><strong>{number(selected.get("stable_candidate_count"),0)}개</strong></div>'
                f'<div class="detail-stat"><span>핵심 8업종 점포</span><strong>{number(selected.get("core8_store_count"),0)}</strong></div>'
                f'<div class="detail-stat"><span>평균 인구</span><strong>{number(selected.get("population_avg"),0)}</strong></div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">지역 핵심 지표</div>', unsafe_allow_html=True)
    cols = st.columns(4)
    metrics = [
        ("소비 규모", selected.get("core8_amt_total"), "BC 핵심 8개 업종 이용금액 합계"),
        ("공급 규모", selected.get("core8_store_count"), "핵심 8개 업종 점포 수"),
        ("소비 다양성", selected.get("spend_entropy_11"), "11개 소비업종 구성 다양성"),
        ("공급 다양성", selected.get("supply_entropy_247"), "247개 세부업종 구성 다양성"),
    ]
    for col, (label, value, help_text) in zip(cols, metrics):
        col.metric(label, number(value), help=help_text)

    candidates = [row for row in data.get("candidates", []) if str(row.get("region_code")) == str(selected.get("region_code"))]
    st.markdown('<div class="section-title">이 지역의 공식 후보 업종</div>', unsafe_allow_html=True)
    if candidates:
        cand = pd.DataFrame(candidates).sort_values("박샘_기본점수", ascending=False)
        show = cand[["analysis_name", "박샘_기본점수", "박샘_Peer순위", "결과구분", "m5_review_level"]].rename(columns={"analysis_name":"업종", "박샘_기본점수":"M4 공식 점수", "박샘_Peer순위":"Peer 내 순위", "결과구분":"결과구분", "m5_review_level":"검토수준"})
        st.dataframe(show, hide_index=True, width="stretch", height=min(310, 38 * (len(show) + 1)), column_config={"M4 공식 점수": st.column_config.NumberColumn(format="%.2f"), "Peer 내 순위": st.column_config.NumberColumn(format="%d")})
    else:
        st.info("이 지역에는 공식 후보가 없습니다.")
    with st.expander("지표 해석 기준 보기"):
        st.write("지역 지표는 저장된 집계값입니다. M2 표시명과 통계적 정의는 방법론 화면에서 확인할 수 있습니다.")

