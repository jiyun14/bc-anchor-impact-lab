from __future__ import annotations

import streamlit as st

from components import candidates, core9, explorer, home, methodology, portfolio, validation
from styles import APP_CSS
from utils.data_loader import load_core_data, load_full_data, load_m2_mapping

st.set_page_config(page_title="BC Anchor Impact Lab", page_icon="◈", layout="wide", initial_sidebar_state="collapsed")
st.markdown(APP_CSS, unsafe_allow_html=True)

PAGES = ["홈", "상권 탐색", "후보 분석", "Anchor 9", "지역 전략", "실제 사례", "방법론"]


def navigate(page: str) -> None:
    st.session_state["active_page"] = page


def top_navigation() -> str:
    if st.session_state.get("active_page") not in PAGES:
        st.session_state["active_page"] = "홈"
    with st.container(key="top_nav"):
        brand, menu = st.columns([1.45, 4.55], vertical_alignment="center")
        brand.button("BC Anchor Impact Lab", key="nav_brand", type="tertiary", on_click=navigate, args=("홈",))
        menu_pages = PAGES[1:]
        menu_columns = menu.columns(len(menu_pages), gap="small")
        for column, page in zip(menu_columns, menu_pages):
            state = "active" if st.session_state["active_page"] == page else "inactive"
            column.button(page, key=f"nav_{state}_{page}", type="tertiary", on_click=navigate, args=(page,), width="stretch")
    return st.session_state["active_page"]


def main() -> None:
    core = load_core_data("frontend_core.json")
    mapping = load_m2_mapping()
    page = top_navigation()
    if page == "홈":
        home.render(core, load_full_data("frontend_data.json"), navigate)
    elif page == "상권 탐색":
        explorer.render(load_full_data("frontend_data.json"), mapping)
    elif page == "후보 분석":
        candidates.render(load_full_data("frontend_data.json"))
    elif page == "Anchor 9":
        core9.render(core, load_full_data("frontend_data.json"), mapping)
    elif page == "지역 전략":
        portfolio.render(core)
    elif page == "실제 사례":
        validation.render(core)
    else:
        methodology.render(core, mapping)


if __name__ == "__main__":
    main()
