from __future__ import annotations

import pandas as pd
import streamlit as st

from utils.formatting import text


def render(core: dict, mapping: list[dict]) -> None:
    st.markdown('<div class="page-head methodology-head"><div class="page-title">분석 방법과 해석 범위</div><p class="page-subtitle">추천 결과가 만들어지는 과정과 해석 시 주의사항을 확인할 수 있습니다.</p></div>', unsafe_allow_html=True)
    method = core.get("methodology", {})
    flow, m12, m3, m4, m5, limits = st.tabs(["전체 흐름", "M1~M2", "M3", "M4", "M5 및 검증", "한계"])
    with flow:
        steps = [("진단","지역×업종 수요·공급 구조"),("지표화","비교 가능한 정규화 축"),("유사 상권","구조가 비슷한 지역 그룹"),("후보 선별","Peer 내부 우선순위와 강건성"),("실행 전략","Anchor·Linkage·Protection")]
        st.markdown('<div class="method-line">' + ''.join(f'<div><b>{title}</b><span>{copy}</span></div>' for title,copy in steps) + '</div>', unsafe_allow_html=True)
    with m12:
        st.markdown("### 상권 진단과 지표화")
        st.write(text(method.get("M1", {}).get("role")))
        st.write(text(method.get("M2", {}).get("role")))
        with st.expander("M2 6축 변환과 해석 보기"):
            st.dataframe(pd.DataFrame(mapping)[["korean_display_name","transformation","interpretation","caution"]].rename(columns={"korean_display_name":"표시명","transformation":"변환","interpretation":"해석","caution":"주의"}), hide_index=True, width="stretch")
    with m3:
        detail = method.get("M3", {})
        st.markdown("### 유사 상권 Peer Group")
        st.write(text(detail.get("note")))
        cols = st.columns(3)
        cols[0].metric("PCA 구성요소", detail.get("pca_components", "–"))
        cols[1].metric("군집 수", detail.get("k", "–"))
        cols[2].metric("평균 ARI", detail.get("k3_mean_ari_approx", "–"))
    with m4:
        st.markdown("### 후보 우선순위와 강건성")
        st.write(text(method.get("M4", {}).get("role")))
        st.info("M4 공식 점수는 후보 비교를 위한 종합점수이며 확률값이 아닙니다. Peer 순위는 동일 Peer 내부 비교입니다.")
    with m5:
        st.markdown("### 지역 전략과 외부 사례")
        st.write(text(method.get("M5", {}).get("role")))
        st.info("Linkage는 인과적 보완관계가 아니며 Protection은 보호효과의 입증이 아닙니다. 외부 사례도 핵심 9개 후보의 직접 검증이 아닙니다.")
    with limits:
        for limitation in core.get("limitations", []):
            st.markdown(f"- {text(limitation)}")
        st.caption("분석기간 2026년 1~6월 · 시군구 단위 집계")
