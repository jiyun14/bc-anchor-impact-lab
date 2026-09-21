from __future__ import annotations

import re

import pandas as pd
import plotly.express as px
import streamlit as st

from utils.formatting import number, percent, text


OUTCOME_LABELS = {"nonanchor_sales":"비앵커 이용금액", "nonanchor_stores":"비앵커 점포수"}


def _display_percent_text(value: object) -> str:
    source = text(value)
    return re.sub(r"(?<![\w.])([-+]?\d+\.\d+)%", lambda match: f"{float(match.group(1)):.2f}%", source)


def _display_range(value: object) -> str:
    source = text(value)
    return re.sub(r"(?<![\w.])([-+]?\d+\.\d+)", lambda match: f"{float(match.group(1)):.2f}", source)


def render(core: dict) -> None:
    st.markdown('<div class="page-head"><div class="eyebrow">REAL-WORLD EVIDENCE</div><div class="page-title">실제 상권에서도 비슷한 변화가 관찰됐을까?</div><p class="page-subtitle">외부 앵커 사례 전후의 저장된 변화 패턴과 민감도 결과를 함께 살펴봅니다.</p></div>', unsafe_allow_html=True)
    real = core.get("real_world_validation", {})
    st.markdown('<div class="info-banner">외부 실제 사례를 활용한 탐색적 검증이며, 핵심 9개 후보의 직접 효과 검증은 아닙니다.</div>', unsafe_allow_html=True)
    cases = real.get("cases", [])
    if not cases:
        st.info("표시할 외부 사례가 없습니다.")
        return
    names = list(dict.fromkeys(row.get("case", "데이터 없음") for row in cases))
    tabs = st.tabs(names)
    for tab, name in zip(tabs, names):
        with tab:
            rows = [row for row in cases if row.get("case") == name]
            first = rows[0]
            c1,c2,c3 = st.columns(3)
            c1.metric("처리상권", text(first.get("treatment_area")))
            c2.metric("개점일", text(first.get("opening_date")))
            c3.metric("근거 상태", text(first.get("evidence_status")))
            plot_rows=[]
            for row in rows:
                try: value=float(row.get("main_percent_change"))
                except (TypeError,ValueError): continue
                plot_rows.append({"지표":OUTCOME_LABELS.get(row.get("outcome"),row.get("outcome")),"저장된 변화율":value})
            if plot_rows:
                fig=px.bar(pd.DataFrame(plot_rows),x="지표",y="저장된 변화율",color="저장된 변화율",color_continuous_scale=[[0,"#7991ad"],[.5,"#d9e7f8"],[1,"#246bfd"]])
                fig.add_hline(y=0,line_width=2,line_color="#102a43")
                fig.update_layout(height=280,yaxis_title="변화율(%)",xaxis_title=None,coloraxis_showscale=False,margin=dict(l=10,r=10,t=10,b=10),paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="#fff",font=dict(color="#334e68"))
                fig.update_yaxes(gridcolor="#e8eef5")
                st.plotly_chart(fig,width="stretch",config={"displayModeBar":False})
            for outcome_index, row in enumerate(rows):
                label=OUTCOME_LABELS.get(row.get("outcome"),text(row.get("outcome")))
                unit_key = f"validation_outcome_{name}_{row.get('outcome')}_{outcome_index}"
                with st.container(key=unit_key):
                    st.markdown(f'<div class="validation-outcome"><span class="pill">{label}</span><strong>{percent(row.get("main_percent_change"),2)}</strong><b>{text(row.get("source_interpretation_label"))}</b><p>{_display_percent_text(row.get("safe_interpretation"))}</p></div>',unsafe_allow_html=True)
                    with st.expander(f"{label} 통계 상세 보기"):
                        st.markdown(
                            '<div class="stat-summary">'
                            f'<div><span>사전추세</span><b>{text(row.get("linear_pretrend_status"))}</b><small>p = {number(row.get("main_p_value"),4)}</small></div>'
                            f'<div><span>사전기간 검정</span><b>{text(row.get("preblock_placebo_status"))}</b></div>'
                            f'<div><span>비교상권 민감도</span><b>{text(row.get("loco_status"))}</b><small>{_display_range(row.get("loco_range_percent"))}</small></div>'
                            f'<div class="stat-limitation"><span>해석 범위</span><p>{text(row.get("limitation"))}</p></div>'
                            '</div>',
                            unsafe_allow_html=True,
                        )

