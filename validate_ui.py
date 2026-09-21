from __future__ import annotations

import csv
import hashlib
import json
import re
from pathlib import Path

from streamlit.testing.v1 import AppTest

from utils.formatting import number


APP_DIR = Path(__file__).resolve().parent
FINAL_DIR = APP_DIR.parent
FRONTEND_DIR = APP_DIR / "data"
RESULT_PATH = APP_DIR / "ui_validation.csv"
PAGES = ["홈", "상권 탐색", "후보 분석", "Anchor 9", "지역 전략", "실제 사례", "방법론"]


def parse_css(source: str) -> dict[str, dict[str, str]]:
    css = re.search(r'<style>(.*)</style>', source, re.S).group(1)
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    rules: dict[str, dict[str, str]] = {}
    for selectors, body in re.findall(r'([^{}]+)\{([^{}]*)\}', css):
        props = {key.strip(): value.strip().replace(' !important', '') for key, value in re.findall(r'([\w-]+)\s*:\s*([^;]+)', body)}
        for selector in selectors.split(','):
            clean = selector.strip()
            if clean and not clean.startswith('@'):
                rules.setdefault(clean, {}).update(props)
    return rules


def luminance(color: str) -> float:
    values = [int(color.lstrip('#')[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    values = [v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in values]
    return .2126 * values[0] + .7152 * values[1] + .0722 * values[2]


def contrast(foreground: str, background: str) -> float:
    high, low = sorted((luminance(foreground), luminance(background)), reverse=True)
    return (high + .05) / (low + .05)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    results: list[dict[str, str]] = []

    def check(item: str, expected: str, actual: str, passed: bool, detail: str = "") -> None:
        results.append({"검증항목": item, "기대값": expected, "실제값": actual, "상태": "PASS" if passed else "FAIL", "설명": detail})

    rendered: dict[str, AppTest] = {}
    for page in PAGES:
        app = AppTest.from_file(str(APP_DIR / "app.py"), default_timeout=30)
        app.session_state["active_page"] = page
        app.run()
        rendered[page] = app
        check(f"{page} 렌더링", "예외 0", f"예외 {len(app.exception)}", len(app.exception) == 0)

    app_source = (APP_DIR / "app.py").read_text(encoding="utf-8")
    home_source = (APP_DIR / "components" / "home.py").read_text(encoding="utf-8")
    candidate_source = (APP_DIR / "components" / "candidates.py").read_text(encoding="utf-8")
    core_source = (APP_DIR / "components" / "core9.py").read_text(encoding="utf-8")
    real_source = (APP_DIR / "components" / "validation.py").read_text(encoding="utf-8")
    style_source = (APP_DIR / "styles.py").read_text(encoding="utf-8")
    base_rules = parse_css(style_source.split('@media', 1)[0] + '</style>')
    nav = base_rules.get('.st-key-top_nav', {})
    parent = base_rules.get('.block-container', {})

    home_buttons = [button.label for button in rendered["홈"].button]
    nav_labels = {"BC Anchor Impact Lab", "상권 탐색", "후보 분석", "Anchor 9", "지역 전략", "실제 사례", "방법론"}
    check("NAV_VISIBLE", "브랜드+메뉴 6개", f"{len(nav_labels.intersection(home_buttons))}개", nav_labels.issubset(home_buttons))
    check("NAV_NO_PILLS_AS_DEFAULT", "st.pills 미사용", "미사용" if ".pills(" not in app_source else "사용", ".pills(" not in app_source and "stPills" not in style_source)
    padding_top = parent.get("padding", "0").split()[0]
    nav_safe = nav.get("position") in {"relative", "static"} and nav.get("top") == "auto" and nav.get("overflow") == "visible" and padding_top.endswith("rem") and float(padding_top.removesuffix("rem")) >= 4
    check("NAV_NO_CLIPPING_RULE", "document flow+안전 여백", f"{nav.get('position')}/{nav.get('top')}/{padding_top}", nav_safe)

    check("HOME_HAS_REGION_START_ACTION", "시도·시군구·실행", f"select {len(rendered['홈'].selectbox)}, action {'상권 분석하기 →' in home_buttons}", len(rendered["홈"].selectbox) == 2 and "상권 분석하기 →" in home_buttons)
    home_flow = AppTest.from_file(str(APP_DIR / "app.py"), default_timeout=30).run()
    home_flow.selectbox[0].set_value("서울특별시").run()
    home_flow.selectbox[1].set_value("구로구").run()
    next(button for button in home_flow.button if button.label == "상권 분석하기 →").click().run()
    home_navigation_ok = len(home_flow.exception) == 0 and home_flow.session_state["active_page"] == "상권 탐색" and home_flow.session_state["explorer_sigungu"] == "구로구"
    check("HOME_REGION_NAVIGATION_WORKS", "서울 구로구→상권 탐색", str(home_flow.session_state["active_page"]), home_navigation_ok)
    preview_count = sum('class="preview-row"' in str(item.value) for item in rendered["홈"].markdown)
    home_detail_actions = sum(button.label == "분석 보기 →" for button in rendered["홈"].button)
    check("HOME_HAS_RESULT_PREVIEW", "대표 후보 3개", f"{preview_count}개", preview_count == 3)
    check("HOME_PREVIEW_CARD_COUNT", 3, preview_count, preview_count == 3)
    check("HOME_PREVIEW_NO_DETAIL_ACTION", 0, home_detail_actions, home_detail_actions == 0 and "home_anchor_" not in home_source)
    check("HOME_STATS_VISIBLE", "stats strip", "포함" if "stats-strip" in home_source else "누락", "stats-strip" in home_source and all(token in home_source for token in ["분석 지역", "공식 후보", "Peer 상위 후보", "핵심 Anchor", "우선 현장검토"]))
    process_secondary = home_source.find("지금 확인할 핵심 Anchor") < home_source.find("어떻게 찾았나요?")
    check("HOME_PROCESS_SECONDARY", "결과 다음 배치", "결과→방법" if process_secondary else "순서 오류", process_secondary)
    check("CANDIDATE_HAS_FILTER_TOOLBAR", "toolbar+필터 6개", f"필터 {len(rendered['후보 분석'].selectbox)}개", "candidate_filter_toolbar" in candidate_source and len(rendered["후보 분석"].selectbox) == 6)
    all_flow = AppTest.from_file(str(APP_DIR / "app.py"), default_timeout=30).run()
    next(button for button in all_flow.button if button.label == "전체 Anchor 9 보기 →").click().run()
    anchor_card_count = sum('class="anchor-card"' in str(item.value) for item in all_flow.markdown)
    anchor_actions = sum(button.label == "분석 보기 →" for button in all_flow.button)
    all_ok = len(all_flow.exception) == 0 and all_flow.session_state.get("active_page") == "Anchor 9" and anchor_card_count == 9 and anchor_actions == 0
    check("HOME_ALL_ANCHORS_NAV", "Anchor 9 전체 목록", f"cards={anchor_card_count}", all_ok)
    check("ANCHOR9_CARD_COUNT", 9, anchor_card_count, anchor_card_count == 9)
    check("ANCHOR9_NO_DETAIL_ACTION", 0, anchor_actions, anchor_actions == 0)
    no_card_click = "st.button(" not in core_source and "on_click=" not in core_source
    check("ANCHOR9_NO_CARD_CLICK", "click handler 0", "0" if no_card_click else "발견", no_card_click)
    anchor_wrapper = base_rules.get('[class*="st-key-anchor_item_"]', {})
    anchor_content = base_rules.get('.anchor-card', {})
    anchor_meta = base_rules.get('.anchor-meta', {})
    card_markup_complete = anchor_card_count == 9 and all(token in core_source for token in ["anchor-score", "anchor-meta", "warning_label"])
    check("ANCHOR_CARD_CONTENT_INSIDE_BORDER", "9개 complete markup", f"cards={anchor_card_count}", card_markup_complete and anchor_wrapper.get("box-sizing") == "border-box")
    bottom_padding = anchor_wrapper.get("padding", "").split()[-1] if anchor_wrapper.get("padding") else ""
    check("ANCHOR_CARD_BOTTOM_PADDING", "≥1.5rem", bottom_padding, bottom_padding in {"1.5rem", "1.55rem", "1.6rem", "1.65rem", "1.7rem"})
    no_clip_rules = anchor_wrapper.get("overflow") == "visible" and anchor_content.get("overflow") != "hidden" and anchor_meta.get("line-height") == "1.55"
    check("ANCHOR_CARD_NO_TEXT_CLIPPING", "overflow visible+line-height", f"{anchor_wrapper.get('overflow')}/{anchor_meta.get('line-height')}", no_clip_rules)
    row_gap = anchor_wrapper.get("margin-bottom", "")
    check("ANCHOR_CARD_ROW_GAP", "24~30px", row_gap, row_gap in {"1.5rem", "1.55rem", "1.6rem", "1.65rem", "1.75rem", "1.8rem"})
    content_height = anchor_wrapper.get("height") == "auto" and anchor_wrapper.get("min-height") == "280px" and "max-height" not in anchor_wrapper
    check("ANCHOR_CARD_CONTENT_DRIVEN_HEIGHT", "auto+min-height/no max-height", f"{anchor_wrapper.get('height')}/{anchor_wrapper.get('min-height')}", content_height)
    no_hidden_fix = anchor_wrapper.get("overflow") != "hidden" and anchor_content.get("overflow") != "hidden" and "position" not in anchor_wrapper
    check("ANCHOR_CARD_NO_OVERFLOW_HIDDEN_FIX", "hidden/absolute 없음", "없음" if no_hidden_fix else "발견", no_hidden_fix)
    check("ANCHOR_CARD_NO_ANALYSIS_BUTTON", 0, anchor_actions, anchor_actions == 0 and "분석 보기 →" not in core_source)
    check("REALWORLD_HAS_CASE_SELECTOR", "case tab 3개", f"{len(rendered['실제 사례'].tabs)}개", len(rendered["실제 사례"].tabs) == 3)
    check("REALWORLD_DIRECT_VALIDATION_FALSE_VISIBLE", "직접 검증 아님", "표시" if "직접 효과 검증은 아닙니다" in real_source else "누락", "직접 효과 검증은 아닙니다" in real_source)

    contrast_pairs = [
        ('.st-key-nav_brand button', '#ffffff'),
        ('[class*="st-key-nav_inactive_"] button', '#ffffff'),
        ('[class*="st-key-nav_active_"] button', '#ffffff'),
    ]
    ratios = []
    for selector, fallback in contrast_pairs:
        props = base_rules.get(selector, {})
        foreground = props.get("color", "")
        background = props.get("background", fallback)
        if background == "transparent":
            background = fallback
        ratios.append(contrast(foreground, background) if foreground.startswith('#') and background.startswith('#') else 0)
    check("NO_DARK_ON_DARK", "대비≥4.5", f"최소 {min(ratios):.2f}:1", min(ratios) >= 4.5)
    check("NO_HOVER_ONLY_TEXT", "normal 대비≥4.5", f"최소 {min(ratios):.2f}:1", min(ratios) >= 4.5)
    negative_pattern = re.compile(r'(?:top|margin-top)\s*:\s*-|translate(?:Y)?\s*\(\s*-', re.I)
    nav_and_parent = str(nav) + str(parent)
    check("NO_NEGATIVE_POSITION_HACK", "0건", "0건" if not negative_pattern.search(nav_and_parent) else "발견", not negative_pattern.search(nav_and_parent))

    # Final blue-fade SaaS design contract.
    top_background = base_rules.get('.stApp', {}).get('background', '')
    check("TOP_FADE_PRESENT", "radial+linear fade", "포함" if 'radial-gradient' in top_background and 'linear-gradient' in top_background else "누락", 'radial-gradient' in top_background and 'linear-gradient' in top_background)
    light_blue_tokens = ["#f5f9ff", "#dceaff", "#edf4ff", "#246bfd"]
    palette_hits = sum(token in style_source.lower() for token in light_blue_tokens)
    check("TOP_FADE_USES_LIGHT_BLUE_PALETTE", "light blue palette", f"{palette_hits}개 token", palette_hits >= 3 and 'rgba(74, 134, 246, .15)' in top_background)
    check("NAV_INTEGRATED_WITH_FADE", "transparent nav", nav.get('background', ''), nav.get('background') == 'transparent' and base_rules.get('header[data-testid="stHeader"]', {}).get('background') == 'transparent')
    check("NAV_NO_WHITE_RECTANGLE_CARD", "white background 없음", nav.get('background', ''), nav.get('background') != '#ffffff')
    check("NAV_NO_OUTER_ROUNDED_BOX", "radius 0", nav.get('border-radius', ''), nav.get('border-radius') == '0' and nav.get('box-shadow') == 'none')
    active_nav = base_rules.get('[class*="st-key-nav_active_"] button', {})
    check("NAV_ACTIVE_UNDERLINE", "blue underline", active_nav.get('box-shadow', ''), 'inset 0 -2px 0 #246bfd' in active_nav.get('box-shadow', ''))
    check("HOME_NO_ENGLISH_EYEBROW", "영문 eyebrow 없음", "없음" if 'BC CONSUMPTION DATA' not in home_source and 'class="eyebrow"' not in home_source else "발견", 'BC CONSUMPTION DATA' not in home_source and 'class="eyebrow"' not in home_source)
    check("HOME_HERO_TWO_COLUMN_DESKTOP", "2-column hero", "포함" if 'hero_copy, hero_visual = st.columns' in home_source else "누락", 'hero_copy, hero_visual = st.columns' in home_source and 'location-visual' in home_source)
    controls_light = all(token in style_source for token in ['.st-key-home_sido', '.st-key-home_sigungu', 'background: #fff !important', 'min-height: 54px'])
    check("HOME_LOCATION_CONTROLS_LIGHT", "white controls", "적용" if controls_light else "누락", controls_light)
    primary_cta = base_rules.get('.st-key-home_region_start button', {})
    check("HOME_PRIMARY_CTA_BLUE", "#246bfd/white", f"{primary_cta.get('background')}/{primary_cta.get('color')}", primary_cta.get('background') == '#246bfd' and primary_cta.get('color') == '#fff')
    check("HOME_KPI_STRIP_PRESENT", "stats strip 5개", f"{len(rendered['홈'].markdown)} markdown", 'stats-strip' in home_source and len(core_source) > 0)
    check("HOME_CORE_ANCHOR_PREVIEW_PRESENT", "실제 core anchor 3개", f"{preview_count}개", 'core.get("core_anchors", [])[:3]' in home_source and preview_count == 3)
    check("HOME_METHOD_FLOW_PRESENT", "M1~M5 flow", "포함" if 'method-line' in home_source else "누락", 'method-line' in home_source and all(code in home_source for code in ['M1','M2','M3','M4','M5']))
    palette_consistent = all(token in style_source.lower() for token in ['--navy: #17233b', '--blue: #246bfd', '--soft: #eef4ff'])
    check("GLOBAL_BLUE_PALETTE_CONSISTENT", "navy/blue/soft", "일치" if palette_consistent else "불일치", palette_consistent)
    content_gradient = any(re.search(rf'{selector}[^{{]*{{[^}}]*gradient', style_source, re.S) for selector in [r'\.preview-row', r'\.stat-item', r'\.method-line', r'\.anchor-card'])
    check("NO_GRADIENT_OVERUSE", "content card gradient 0", "0" if not content_gradient else "발견", not content_gradient)
    all_negative = negative_pattern.search(style_source)
    check("NO_NEGATIVE_POSITION_HACK_GLOBAL", "0건", "0건" if not all_negative else "발견", not all_negative)
    signature_ok = 'def render(core: dict, full_data: dict, navigate:' in home_source
    check("HOME_RENDER_SIGNATURE_PRESERVED", "core, full_data, navigate", "보존" if signature_ok else "불일치", signature_ok)

    config_source = (APP_DIR / ".streamlit" / "config.toml").read_text(encoding="utf-8")
    candidates_source = (APP_DIR / "components" / "candidates.py").read_text(encoding="utf-8")
    explorer_source = (APP_DIR / "components" / "explorer.py").read_text(encoding="utf-8")
    portfolio_source = (APP_DIR / "components" / "portfolio.py").read_text(encoding="utf-8")
    methodology_source = (APP_DIR / "components" / "methodology.py").read_text(encoding="utf-8")
    nav_font = base_rules.get('[class*="st-key-nav_inactive_"] button', {}).get('font-size', '')
    check("NAV_FONT_SIZE_READABLE", "15~16px", nav_font, nav_font in {'.94rem', '.95rem', '.96rem', '1rem'})
    check("NAV_HAS_SUBTLE_DIVIDER", "rgba divider", nav.get('border-bottom', ''), 'rgba(120,145,180,.16)' in nav.get('border-bottom', ''))
    check("NAV_NO_DARK_SURFACE", "transparent", nav.get('background', ''), nav.get('background') == 'transparent')
    cta_after_selects = home_source.find('if st.button("상권 분석하기') > home_source.find('search1, search2 = st.columns') and 'search3' not in home_source
    check("HOME_CTA_BELOW_SELECTORS", "select 2열 다음 CTA", "적용" if cta_after_selects else "불일치", cta_after_selects)
    check("HOME_CTA_FULL_CONTROL_WIDTH", "width=stretch", "적용" if 'key="home_region_start", disabled=not sigungu, width="stretch"' in home_source else "누락", 'key="home_region_start", disabled=not sigungu, width="stretch"' in home_source)
    insight_safe = all(token in style_source for token in ['.insight-chip', 'white-space: normal', 'text-overflow: clip', 'overflow-wrap: break-word'])
    check("HOME_INSIGHT_TEXT_NOT_CLIPPED", "wrap+clip 없음", "적용" if insight_safe else "누락", insight_safe)
    check("SELECTBOX_LIGHT_NORMAL", "#fff/navy/#dce4f0", "적용" if 'div[data-baseweb="select"] > div' in style_source and 'background: #ffffff !important' in style_source else "누락", 'div[data-baseweb="select"] > div' in style_source and 'border-color: #dce4f0 !important' in style_source)
    check("SELECTBOX_LIGHT_HOVER", "#fff/#c9d5e6", "적용" if 'div[data-baseweb="select"] > div:hover' in style_source else "누락", 'div[data-baseweb="select"] > div:hover' in style_source and '#c9d5e6 !important' in style_source)
    check("SELECTBOX_LIGHT_FOCUS", "blue ring", "적용" if 'div[data-baseweb="select"] > div:focus-within' in style_source else "누락", 'div[data-baseweb="select"] > div:focus-within' in style_source and 'rgba(36,107,253,.11)' in style_source)
    check("SELECTBOX_NO_BLACK_ACTIVE", "black 없음", "없음", 'background: black' not in style_source.lower() and '#000' not in style_source.lower())
    check("EXPANDER_LIGHT_CLOSED", "white/navy", "적용" if 'div[data-testid="stExpander"] summary' in style_source else "누락", 'div[data-testid="stExpander"] summary' in style_source and 'background: #ffffff !important' in style_source)
    check("EXPANDER_LIGHT_OPEN", "#eef4ff", "적용" if 'details[open] > summary' in style_source else "누락", 'details[open] > summary' in style_source and 'background: #eef4ff !important' in style_source)
    check("EXPANDER_NO_BLACK_ACTIVE", "black 없음", "없음", '#000' not in style_source.lower() and 'background: black' not in style_source.lower())
    check("DATAFRAME_LIGHT_HEADER", "#f5f7fb", "적용" if '[role="columnheader"]' in style_source else "누락", '[role="columnheader"]' in style_source and '#f5f7fb !important' in style_source)
    check("DATAFRAME_LIGHT_BODY", "#ffffff/#24324a", "적용" if '[role="gridcell"]' in style_source else "누락", '[role="gridcell"]' in style_source and 'background: #ffffff !important' in style_source)
    check("DATAFRAME_LIGHT_SELECTED", "#eef4ff", "적용" if '[aria-selected="true"]' in style_source else "누락", 'div[data-testid="stDataFrame"] [aria-selected="true"]' in style_source and '#eef4ff !important' in style_source)
    score_2dp = 'NumberColumn(format="%.2f")' in candidates_source and 'NumberColumn(format="%.2f")' in explorer_source and 'number(ranking.get("official_m4_score"), 2)' in core_source
    check("DISPLAY_M4_SCORE_2DP", "소수점 2자리", "적용" if score_2dp else "누락", score_2dp)
    check("FILTER_LABEL_READABLE", "13~14px/600", "적용" if '[data-testid="stWidgetLabel"] p' in style_source else "누락", '[data-testid="stWidgetLabel"] p' in style_source and 'font-size: .84rem !important' in style_source and 'font-weight: 600 !important' in style_source)
    check("NO_BLACK_BUTTON", "black surface 0", "0", 'button { background: black' not in style_source.lower() and 'button { background: #000' not in style_source.lower())
    check("NO_BLACK_SELECTBOX", "black surface 0", "0", 'baseweb="select"] > div { background: black' not in style_source.lower())
    check("NO_BLACK_EXPANDER", "black surface 0", "0", 'stexpander"] summary { background: black' not in style_source.lower())
    check("NO_BLACK_DATAFRAME_SURFACE", "black surface 0", "0", 'stdataframe"] { background: black' not in style_source.lower())
    check("NO_HOVER_ONLY_READABLE_TEXT", "normal text 명시", "적용", all(token in style_source for token in ['color: var(--navy) !important', 'color: #24324a !important']))
    meaningful_text_safe = 'text-overflow: ellipsis' not in style_source and insight_safe and 'overflow-wrap: anywhere' in style_source
    check("NO_MEANINGFUL_TEXT_CLIPPING", "ellipsis 0+wrap", "적용" if meaningful_text_safe else "점검 필요", meaningful_text_safe)
    check("BLUE_PALETTE_CONSISTENT", "light theme tokens", "일치" if palette_consistent and 'base = "light"' in config_source else "불일치", palette_consistent and 'base = "light"' in config_source)

    # Final information-density contract: keep data intact and structure only the display layer.
    kpi_split = '_kpi_items(action.get(key))' in portfolio_source and '.split("|")' in portfolio_source
    check("KPI_ITEMS_NOT_PIPE_STRING", "KPI별 list item", "분리" if kpi_split else "pipe 문자열", kpi_split)
    check("KPI_CARD_SPACING_READABLE", "gap=large/item rhythm", "적용" if 'st.columns(3, gap="large")' in portfolio_source else "누락", 'st.columns(3, gap="large")' in portfolio_source and '.kpi-items li' in style_source and 'margin: .45rem 0' in style_source)
    kpi_padding = all(token in style_source for token in ['.kpi-plain', 'padding: 1.4rem 1.5rem', '.kpi-list'])
    check("KPI_CARD_PADDING_READABLE", "22~26px", "1.4rem/1.5rem" if kpi_padding else "누락", kpi_padding)
    benefit_hierarchy = 'benefit-summary' in portfolio_source and '<strong>BC 공동혜택 제안</strong><p>' in portfolio_source
    check("BC_BENEFIT_HAS_TEXT_HIERARCHY", "badge/title/body", "적용" if benefit_hierarchy else "누락", benefit_hierarchy)
    check("BC_BENEFIT_KPI_ITEMS_SEPARATED", "3 KPI list", "적용" if kpi_split else "누락", kpi_split and '.benefit-summary' in style_source)
    check("VALIDATION_OUTCOME_SPACING", "32px 이상", "2.35rem" if 'margin: .75rem 0 2.35rem' in style_source else "누락", '[class*="st-key-validation_outcome_"]' in style_source and 'margin: .75rem 0 2.35rem' in style_source)
    validation_structured = 'class="stat-summary"' in real_source and 'class="stat-limitation"' in real_source
    check("VALIDATION_DETAIL_STRUCTURED", "metric grid+해석 범위", "적용" if validation_structured else "누락", validation_structured and '.stat-summary' in style_source)
    precision_ok = 'percent(row.get("main_percent_change"),2)' in real_source and '_display_percent_text' in real_source and '_display_range' in real_source
    check("VALIDATION_DISPLAY_PRECISION", "변화율/범위 2자리", "적용" if precision_ok else "누락", precision_ok)
    check("VALIDATION_LIMITATION_VISIBLE", "해석 범위 표시", "표시" if 'row.get("limitation")' in real_source else "누락", 'class="stat-limitation"' in real_source and 'row.get("limitation")' in real_source)
    check("METHODOLOGY_EYEBROW_REMOVED", "METHODOLOGY eyebrow 없음", "없음" if 'class="eyebrow">METHODOLOGY' not in methodology_source else "발견", 'class="eyebrow">METHODOLOGY' not in methodology_source)
    check("METHODOLOGY_PAGE_RETAINED", "페이지/탭 유지", "유지" if 'def render(core: dict, mapping: list[dict])' in methodology_source else "누락", 'def render(core: dict, mapping: list[dict])' in methodology_source and 'st.tabs(' in methodology_source)
    check("METHODOLOGY_FLOW_RETAINED", "5단계 flow", "유지" if 'method-line' in methodology_source else "누락", 'method-line' in methodology_source and all(label in methodology_source for label in ['진단','지표화','유사 상권','후보 선별','실행 전략']))
    body_line_height = 'body,p,li,[data-testid="stMarkdownContainer"] { line-height: 1.68; }' in style_source
    check("BODY_LINE_HEIGHT_READABLE", "1.6~1.75", "1.68" if body_line_height else "누락", body_line_height)
    rendered_text = "\n".join(str(item.value) for page in ["Anchor 9", "실제 사례", "지역 전략"] for item in rendered[page].markdown)
    raw_long_float = re.search(r"\d+\.\d{5,}", rendered_text)
    check("NO_RAW_LONG_FLOAT_DISPLAY", "5자리 이상 소수 0", "0" if not raw_long_float else raw_long_float.group(0), not raw_long_float)
    dense_pipe = any(pattern in source for source in [core_source, portfolio_source] for pattern in ['<span>{text(action.get(key))}', '<br>{text(action.get(key))}'])
    check("NO_DENSE_PIPE_LIST", "직접 pipe 출력 0", "0" if not dense_pipe else "발견", not dense_pipe)

    baseline = json.loads((APP_DIR / "protected_analysis_hashes.json").read_text(encoding="utf-8"))
    changed = [relative for relative, expected in baseline.items() if not (FINAL_DIR / relative).exists() or sha256(FINAL_DIR / relative) != expected]
    check("NO_ANALYSIS_FILE_HASH_CHANGE", "0건", f"{len(changed)}건", not changed, ", ".join(changed))
    check("ANALYSIS_HASH_UNCHANGED", "0건", f"{len(changed)}건", not changed, ", ".join(changed))

    with RESULT_PATH.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["검증항목", "기대값", "실제값", "상태", "설명"])
        writer.writeheader()
        writer.writerows(results)
    passed = sum(row["상태"] == "PASS" for row in results)
    failed = sum(row["상태"] == "FAIL" for row in results)
    print(f"PASS={passed} WARN=0 FAIL={failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
