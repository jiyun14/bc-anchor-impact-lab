APP_CSS = r"""
<style>
:root {
  --navy: #17233b;
  --blue: #246bfd;
  --blue-hover: #1d5be0;
  --soft: #eef4ff;
  --ink: #24324a;
  --body: #44516a;
  --muted: #74819a;
  --line: #dce4f0;
  --surface: #ffffff;
  --canvas: #f7f9fc;
  --warn: #a85800;
  --warn-bg: #fff8eb;
}
html { scroll-behavior: smooth; }
body,p,li,[data-testid="stMarkdownContainer"] { line-height: 1.68; }
.stCaptionContainer,[data-testid="stCaptionContainer"] { line-height: 1.55; }
.stApp {
  background:
    radial-gradient(circle at 8% 0%, rgba(74, 134, 246, .15) 0, rgba(220, 234, 255, .08) 22rem, transparent 40rem),
    radial-gradient(circle at 92% 3%, rgba(110, 165, 255, .11) 0, transparent 34rem),
    linear-gradient(180deg, #f5f9ff 0, #ffffff 34rem, #f8fafd 68rem, #ffffff 100%);
  color: var(--ink);
}
.block-container { max-width: 1240px; padding: 4.75rem 2rem 4rem; overflow-x: clip; }
header[data-testid="stHeader"] { background: transparent; }
[data-testid="stToolbar"] { visibility: hidden; }
[data-testid="stSidebar"] { display: none; }
footer { visibility: hidden; }

/* SaaS navigation: normal document flow, text actions, active underline. */
.st-key-top_nav {
  position: relative;
  top: auto;
  z-index: 10;
  min-height: 76px;
  background: transparent;
  border: 0;
  border-bottom: 1px solid rgba(120,145,180,.16);
  border-radius: 0;
  padding: 0.35rem 0;
  margin: 0 0 1.25rem;
  box-shadow: none;
  overflow: visible;
}
.st-key-top_nav [data-testid="stHorizontalBlock"] { align-items: center; gap: .7rem; }
.st-key-nav_brand button {
  background: transparent !important;
  color: #102a43 !important;
  border: 0 !important;
  opacity: 1 !important;
  white-space: nowrap;
  min-height: 48px;
  padding: .35rem 0;
  font-size: 1.18rem;
  font-weight: 800;
}
.st-key-nav_brand button:hover,
.st-key-nav_brand button:focus,
.st-key-nav_brand button:active { background: transparent !important; color: #246bfd !important; }
[class*="st-key-nav_inactive_"] button,
[class*="st-key-nav_active_"] button {
  background: transparent !important;
  border: 0 !important;
  border-radius: 0;
  min-height: 48px;
  padding: .45rem .35rem;
  font-size: .96rem;
  font-weight: 580;
  white-space: nowrap;
  opacity: 1 !important;
}
[class*="st-key-nav_inactive_"] button { color: #475569 !important; }
[class*="st-key-nav_inactive_"] button:hover,
[class*="st-key-nav_inactive_"] button:focus-visible {
  background: #edf4ff !important;
  color: #174ea6 !important;
  outline: 2px solid #9bc3ff;
  outline-offset: 1px;
}
[class*="st-key-nav_active_"] button { color: #246bfd !important; box-shadow: inset 0 -2px 0 #246bfd; }
[class*="st-key-nav_active_"] button:hover,
[class*="st-key-nav_active_"] button:focus-visible,
[class*="st-key-nav_active_"] button:active { background: transparent !important; color: #174ea6 !important; box-shadow: inset 0 -2px 0 #174ea6; }
.st-key-nav_brand button p,
[class*="st-key-nav_inactive_"] button p,
[class*="st-key-nav_active_"] button p { color: inherit !important; opacity: 1 !important; }
.st-key-nav_brand button p { font-size: 0; }
.st-key-nav_brand button p::before { content: 'BC'; color: var(--blue); font-size: 1.18rem; }
.st-key-nav_brand button p::after { content: ' Anchor Impact Lab'; color: var(--navy); font-size: 1.18rem; }

/* Streamlit widgets share one explicit light interaction system. */
div[data-baseweb="select"] > div {
  min-height: 46px;
  background: #ffffff !important;
  color: var(--navy) !important;
  border-color: #dce4f0 !important;
  border-radius: 11px !important;
}
div[data-baseweb="select"] > div:hover { background: #ffffff !important; border-color: #c9d5e6 !important; }
div[data-baseweb="select"] > div:focus-within { background: #ffffff !important; border-color: var(--blue) !important; box-shadow: 0 0 0 3px rgba(36,107,253,.11) !important; }
div[data-baseweb="select"] input,div[data-baseweb="select"] svg,div[data-baseweb="select"] span { color: var(--navy) !important; fill: var(--navy) !important; }
div[data-baseweb="select"][aria-disabled="true"] > div { background: #f4f6f9 !important; color: var(--muted) !important; }
ul[role="listbox"] { background: #ffffff !important; border: 1px solid #dce4f0 !important; }
li[role="option"] { background: #ffffff !important; color: var(--navy) !important; }
li[role="option"]:hover { background: #f4f7fc !important; }
li[role="option"][aria-selected="true"] { background: #eef4ff !important; color: var(--blue) !important; }
[data-testid="stWidgetLabel"] p { color: #44516a !important; font-size: .84rem !important; font-weight: 600 !important; }

div[data-testid="stExpander"] details { background: #ffffff; border: 1px solid #dce4f0; border-radius: 11px; overflow: clip; }
div[data-testid="stExpander"] { margin: 1rem 0 2rem; }
div[data-testid="stExpander"] summary { background: #ffffff !important; color: var(--navy) !important; }
div[data-testid="stExpander"] summary:hover { background: #f4f7fc !important; color: var(--blue) !important; }
div[data-testid="stExpander"] details[open] > summary { background: #eef4ff !important; color: var(--navy) !important; border-bottom: 1px solid #dce4f0; }
div[data-testid="stExpander"] summary svg { fill: var(--blue) !important; color: var(--blue) !important; }

div[data-testid="stDataFrame"] { background: #ffffff !important; border: 1px solid #dce4f0; border-radius: 12px; overflow: hidden; color: #24324a !important; }
div[data-testid="stDataFrame"] [role="columnheader"] { background: #f5f7fb !important; color: var(--navy) !important; }
div[data-testid="stDataFrame"] [role="gridcell"] { background: #ffffff !important; color: #24324a !important; border-color: #e6ebf2 !important; }
div[data-testid="stDataFrame"] [role="gridcell"]:hover { background: #f8fafd !important; }
div[data-testid="stDataFrame"] [aria-selected="true"] { background: #eef4ff !important; color: var(--navy) !important; }
[data-baseweb="tab"] { background: transparent !important; color: var(--body) !important; }
[data-baseweb="tab"]:hover { background: #f4f7fc !important; color: var(--blue) !important; }
[aria-selected="true"][data-baseweb="tab"] { background: #eef4ff !important; color: var(--blue) !important; }
div[data-testid="stCheckbox"] label,div[data-testid="stRadio"] label { color: var(--navy) !important; }

/* Home primary CTA states. */
.st-key-cta_primary button {
  background: #246bfd !important;
  color: #ffffff !important;
  border: 1px solid #246bfd !important;
  border-radius: 10px;
  font-weight: 700;
  opacity: 1 !important;
}
.st-key-cta_primary button:hover { background: #174ea6 !important; color: #ffffff !important; border-color: #174ea6 !important; }
.st-key-cta_primary button:focus,
.st-key-cta_primary button:focus-visible { background: #246bfd !important; color: #ffffff !important; border-color: #174ea6 !important; outline: 2px solid #9bc3ff; }
.st-key-cta_primary button:active { background: #123f8c !important; color: #ffffff !important; border-color: #123f8c !important; }
.st-key-cta_primary button p,
.st-key-cta_primary button span,
.st-key-cta_primary button div { color: inherit !important; opacity: 1 !important; }

/* Home secondary CTA states. */
.st-key-cta_secondary button {
  background: #ffffff !important;
  color: #102a43 !important;
  border: 1px solid #9fb3c8 !important;
  border-radius: 10px;
  font-weight: 700;
  opacity: 1 !important;
}
.st-key-cta_secondary button:hover { background: #edf4ff !important; color: #174ea6 !important; border-color: #246bfd !important; }
.st-key-cta_secondary button:focus,
.st-key-cta_secondary button:focus-visible { background: #ffffff !important; color: #174ea6 !important; border-color: #246bfd !important; outline: 2px solid #9bc3ff; }
.st-key-cta_secondary button:active { background: #dbeafe !important; color: #174ea6 !important; border-color: #246bfd !important; }
.st-key-cta_secondary button p,
.st-key-cta_secondary button span,
.st-key-cta_secondary button div { color: inherit !important; opacity: 1 !important; }

.page-head { margin: .7rem 0 1.75rem; }
.page-title { font-size: 2rem; line-height: 1.25; letter-spacing: -.04em; font-weight: 800; color: var(--navy); margin: 0 0 .35rem; }
.page-subtitle { color: var(--muted); font-size: 1rem; line-height: 1.72; margin: .75rem 0 0; max-width: 780px; }
.eyebrow { color: var(--blue); font-size: .73rem; font-weight: 800; letter-spacing: .12em; text-transform: uppercase; margin-bottom: .35rem; }
.section-title { font-size: 1.4rem; line-height: 1.35; font-weight: 780; color: var(--navy); letter-spacing: -.025em; margin: 1.6rem 0 .25rem; }
.section-copy { color: var(--muted); line-height: 1.6; margin: 0 0 .9rem; }
.small-muted,.compact-note { color: var(--muted); font-size: .8rem; line-height: 1.5; }
.service-hero { max-width: 700px; padding: 2rem 0 .8rem; margin-bottom: .25rem; }
.service-hero h1 { color: #0f2742; font-size: clamp(2.75rem,3.8vw,3.25rem); font-weight: 800; line-height: 1.18; letter-spacing: -.05em; margin: 0 0 1rem; }
.service-hero p { color: #64748b; font-size: 1.05rem; line-height: 1.65; margin: 0; }
.search-title { color: #0f2742; font-size: .95rem; font-weight: 750; margin: 1rem 0 .35rem; }
.search-title span { color: var(--blue); }
.st-key-home_sido [data-baseweb="select"] > div,.st-key-home_sigungu [data-baseweb="select"] > div { background: #fff !important; color: var(--navy) !important; border-color: #cbd8e8 !important; border-radius: 12px !important; min-height: 54px; box-shadow: 0 4px 16px rgba(36,107,253,.05); }
.st-key-home_sido [data-baseweb="select"] *,.st-key-home_sigungu [data-baseweb="select"] * { color: var(--navy) !important; }
.st-key-home_region_start button { min-height: 54px; background: #246bfd !important; color: #fff !important; border: 1px solid #246bfd !important; border-radius: 12px; box-shadow: 0 7px 18px rgba(36,107,253,.18); }
.st-key-home_region_start button:hover,.st-key-home_region_start button:focus-visible { background: #174ea6 !important; color: #fff !important; }
.st-key-home_region_start button p { color: inherit !important; }
.location-visual { position: relative; height: 340px; max-width: 450px; margin: 0 auto; border-radius: 50%; background: radial-gradient(circle, rgba(255,255,255,.9) 0 4%, rgba(226,238,255,.55) 5%, rgba(238,246,255,.18) 42%, transparent 68%); overflow: hidden; }
.orbit { position: absolute; inset: 50%; border: 1px solid rgba(36,107,253,.17); border-radius: 50%; }
.orbit-one { width: 108px; height: 108px; margin: -54px; }
.orbit-two { width: 206px; height: 206px; margin: -103px; }
.orbit-three { width: 310px; height: 310px; margin: -155px; }
.location-pin { position: absolute; left: 50%; top: 50%; width: 46px; height: 46px; margin: -23px; border-radius: 50% 50% 50% 12px; background: var(--blue); rotate: -45deg; box-shadow: 0 14px 28px rgba(36,107,253,.24); }
.location-pin span { position: absolute; width: 14px; height: 14px; border-radius: 50%; background: #fff; left: 16px; top: 16px; }
.data-point { position: absolute; width: 10px; height: 10px; border-radius: 50%; background: #79a9ff; box-shadow: 0 0 0 7px rgba(121,169,255,.13); }
.point-one { left: 22%; top: 29%; }.point-two { right: 18%; top: 38%; }.point-three { left: 30%; bottom: 18%; }
.insight-chip { position: absolute; right: 4%; bottom: 10%; width: 178px; max-width: calc(100% - 2rem); overflow: visible; white-space: normal; background: rgba(255,255,255,.92); border: 1px solid #dce4f0; border-radius: 12px; padding: .72rem .85rem; box-shadow: 0 8px 22px rgba(23,78,166,.08); }
.insight-chip b,.insight-chip small { display: block; white-space: normal; overflow: visible; text-overflow: clip; overflow-wrap: break-word; }.insight-chip b { color: var(--navy); font-size: .82rem; }.insight-chip small { color: var(--muted); font-size: .7rem; margin-top: .15rem; }
.stats-strip { display: grid; grid-template-columns: repeat(5,minmax(0,1fr)); background: rgba(255,255,255,.62); border-top: 1px solid #dce6f2; border-bottom: 1px solid #dce6f2; margin: 2.25rem 0 3.25rem; }
.stat-item { display: flex; align-items: center; justify-content: center; gap: .7rem; padding: 1rem 1.2rem; border-right: 1px solid #dce6f2; }
.stat-item:last-child { border-right: 0; }
.stat-item i { width: 9px; height: 9px; flex: 0 0 9px; border-radius: 50%; background: #8cb5ff; box-shadow: 0 0 0 5px #edf4ff; }
.stat-item strong { display: block; color: #0f2742; font-size: 1.55rem; line-height: 1; }
.stat-item span { color: #64748b; font-size: .8rem; }
.section-heading { display: flex; align-items: end; justify-content: space-between; margin: 2.5rem 0 1rem; }
.section-heading.secondary { margin-top: 4rem; }
.section-heading h2 { color: #0f2742; font-size: 1.35rem; margin: 0 0 .2rem; }
.section-heading p { color: #64748b; margin: 0; font-size: .9rem; }
.st-key-candidate_filter_toolbar { background: rgba(255,255,255,.92); border: 1px solid #dce4f0; border-radius: 14px; padding: .9rem 1rem .35rem; margin-bottom: 1rem; }
.preview-row { background: #fff; border: 1px solid #dce6f2; border-radius: 13px; padding: 1rem 1.1rem .8rem; min-height: 156px; box-shadow: 0 8px 24px rgba(15,39,66,.045); }
.status-badge { display: inline-flex; background: #edf4ff; color: #174ea6; border-radius: 999px; padding: .22rem .55rem; font-size: .7rem; font-weight: 750; }
.preview-row h3 { color: #64748b; font-size: .82rem; margin: .65rem 0 .12rem; }
.preview-row strong { color: #0f2742; font-size: 1.12rem; }
.preview-row p { display: flex; justify-content: space-between; gap: .5rem; color: #64748b; font-size: .76rem; line-height: 1.5; margin: .75rem 0 0; border-top: 1px solid #edf2f7; padding-top: .65rem; }
.preview-row p b { color: #334e68; }
.st-key-home_all_anchors button { background: transparent !important; color: #246bfd !important; border: 0 !important; box-shadow: none !important; padding: .25rem 0; min-height: 34px; font-weight: 700; }
.st-key-home_all_anchors button:hover { color: #174ea6 !important; background: transparent !important; }
.st-key-home_all_anchors button p { color: inherit !important; }
.method-line { display: grid; grid-template-columns: repeat(5,minmax(0,1fr)); gap: .35rem; border-top: 1px solid #dce6f2; border-bottom: 1px solid #dce6f2; }
.method-line > div { padding: 1.35rem 1.15rem 1.35rem 3rem; position: relative; }
.method-line > div > i { position: absolute; left: .8rem; top: 1.2rem; display: grid; place-items: center; width: 26px; height: 26px; border-radius: 50%; background: #edf4ff; color: var(--blue); font-size: .72rem; font-style: normal; font-weight: 800; }
.method-line > div:not(:last-child)::after { content: '→'; color: #8aa5c2; position: absolute; right: -.2rem; top: 1.65rem; }
.method-line small { display: block; color: #94a3b8; }
.method-line b { display: block; color: #0f2742; margin: .2rem 0 .45rem; }
.method-line span { display: block; color: #64748b; font-size: .75rem; line-height: 1.55; }
.hero { display: grid; grid-template-columns: minmax(0,1.6fr) minmax(260px,.7fr); gap: 2rem; align-items: center; padding: 3rem; border: 1px solid var(--line); border-radius: 24px; background: #f5f8ff; color: var(--navy); box-shadow: 0 12px 32px rgba(36,107,253,.07); margin: .4rem 0 1rem; overflow: visible; }
.hero h1 { font-size: clamp(2.3rem,4vw,3.25rem); line-height: 1.12; letter-spacing: -.05em; margin: .4rem 0 .8rem; }
.hero p { color: var(--body); font-size: 1.03rem; line-height: 1.75; margin: 0; max-width: 710px; overflow-wrap: anywhere; }
.hero-question { font-size: 1.02rem; color: #93c5fd; font-weight: 700; }
.hero-side { background: #ffffff; border: 1px solid var(--line); border-radius: 18px; padding: 1.25rem; }
.hero-side strong { font-size: 1.1rem; display: block; margin-bottom: .5rem; }
.hero-side span { color: var(--body); font-size: .9rem; line-height: 1.6; }
.kpi-row { display: grid; grid-template-columns: repeat(5,minmax(0,1fr)); gap: .7rem; margin: 1rem 0 .5rem; }
.kpi-card { background: #fff; border: 1px solid var(--line); border-radius: 14px; padding: .9rem 1rem; min-width: 0; }
.kpi-value { color: var(--navy); font-size: 1.8rem; line-height: 1; font-weight: 820; }
.kpi-label { color: var(--body); font-size: .84rem; margin-top: .42rem; overflow-wrap: anywhere; }
.process { display: grid; grid-template-columns: repeat(5,minmax(0,1fr)); gap: .55rem; margin: .8rem 0; }
.process-step { position: relative; background: #fff; border: 1px solid var(--line); border-radius: 13px; padding: .85rem; min-width: 0; }
  .process-step:not(:last-child)::after { content: '›'; position: absolute; right: -.48rem; top: calc(50% - .65rem); color: #9fb3c8; font-size: 1.3rem; z-index: 2; }
.process-step b { display: block; color: var(--blue); font-size: .76rem; }
.process-step strong { display: block; color: var(--navy); margin: .14rem 0; }
.process-step span { color: var(--muted); font-size: .78rem; line-height: 1.4; }
.peer-grid { display: grid; grid-template-columns: repeat(3,minmax(0,1fr)); gap: .75rem; }
.peer-card,.info-card { background: #fff; border: 1px solid var(--line); border-radius: 15px; padding: 1rem 1.1rem; min-width: 0; overflow-wrap: anywhere; }
.peer-card strong { color: var(--navy); display: block; }
.peer-card span { color: var(--muted); font-size: .86rem; }
.pill { display: inline-flex; align-items: center; padding: .25rem .58rem; border-radius: 999px; background: var(--soft); color: #174ea6; font-size: .75rem; font-weight: 700; margin: .08rem .18rem .08rem 0; }
.pill.priority { background: #e9f8f1; color: #146c4c; }
.pill.warn { background: var(--warn-bg); color: var(--warn); }
.info-banner { background: var(--soft); border: 1px solid #cfe0ff; border-radius: 11px; padding: .72rem .9rem; color: #294e77; font-size: .87rem; line-height: 1.55; margin: .65rem 0 1rem; }
.warning-banner { background: var(--warn-bg); border: 1px solid #f5d8a8; border-radius: 11px; padding: .72rem .9rem; color: #7a4500; font-size: .87rem; line-height: 1.55; margin: .65rem 0; }
.anchor-card { background: transparent; border: 0; border-radius: 0; padding: 0; box-shadow: none; overflow-wrap: anywhere; }
.anchor-card h3 { color: var(--navy); margin: 1.35rem 0 .75rem; font-size: 1.08rem; }
.anchor-industry { color: var(--blue); font-size: 1.18rem; font-weight: 780; margin-bottom: .45rem; }
.anchor-peer { color: var(--muted); font-size: .8rem; margin: 0 0 1.2rem; }
.anchor-score { display: flex; justify-content: space-between; align-items: end; border-top: 1px solid #edf1f5; padding-top: 1.1rem; }
.anchor-score strong { color: var(--navy); font-size: 1.5rem; }
.anchor-score span { color: var(--muted); font-size: .76rem; }
.anchor-meta { display: flex; justify-content: space-between; align-items: baseline; color: var(--body); font-size: .82rem; line-height: 1.55; margin-top: 1rem; gap: .75rem; }
[class*="st-key-anchor_item_"] { height: auto; min-height: 280px; box-sizing: border-box; overflow: visible; background: #fff; border: 1px solid var(--line); border-radius: 12px; padding: 1.5rem 1.6rem 1.65rem; margin-bottom: 1.65rem; box-shadow: 0 6px 20px rgba(23,35,59,.04); }
.detail-hero { display: grid; grid-template-columns: minmax(0,1.3fr) repeat(3,minmax(130px,.45fr)); gap: .65rem; margin: .8rem 0 1rem; }
.detail-main { background: #f5f8ff; color: var(--navy); border: 1px solid #dce4f0; border-radius: 17px; padding: 1.2rem; min-width: 0; }
.detail-main h2 { margin: .25rem 0; font-size: 1.55rem; }
.detail-main p { color: var(--body); margin: .25rem 0 0; }
.detail-stat { background: #fff; border: 1px solid var(--line); border-radius: 14px; padding: 1rem; min-width: 0; }
.detail-stat span { color: var(--muted); font-size: .76rem; }
.detail-stat strong { display: block; color: var(--navy); font-size: 1.22rem; margin-top: .25rem; overflow-wrap: anywhere; }
.strategy-map { background: #fff; border: 1px solid var(--line); border-radius: 17px; padding: 1.05rem; margin: .7rem 0; text-align: center; }
.strategy-anchor { display: inline-block; background: var(--navy); color: #fff; border-radius: 12px; padding: .65rem 1.3rem; min-width: 150px; }
.strategy-line { width: 1px; height: 18px; background: #9fb3c8; margin: 0 auto; }
.strategy-links { display: grid; grid-template-columns: repeat(3,minmax(0,1fr)); gap: .55rem; max-width: 740px; margin: 0 auto; }
.strategy-link { background: var(--soft); color: #174ea6; border-radius: 11px; padding: .6rem; overflow-wrap: anywhere; }
.strategy-protection { display: inline-block; background: var(--warn-bg); color: #8a4b00; border-radius: 11px; padding: .55rem 1rem; min-width: 145px; }
.action-summary { background: #fff; border: 1px solid var(--line); border-radius: 15px; padding: 1.5rem 1.65rem; line-height: 1.72; overflow-wrap: anywhere; }
.benefit-summary { margin-bottom: 1.75rem; }
.benefit-summary > strong { display: block; color: var(--navy); font-size: 1.15rem; margin-top: .9rem; }
.benefit-summary > p { color: var(--body); max-width: 850px; margin: .6rem 0 0; line-height: 1.75; }
.workspace-title { color: #0f2742; font-size: 1.15rem; font-weight: 780; margin: 1.25rem 0 .65rem; }
.evidence-line { display: grid; grid-template-columns: auto 1fr auto 1fr; gap: .65rem; align-items: center; border-top: 1px solid #e2e8f0; margin: 1.5rem 0 2.75rem; padding: 1.1rem .25rem; color: #475569; font-size: .82rem; }
.evidence-line b { color: #0f2742; }
.action-block { border-top: 1px solid #e2e8f0; padding: 1rem 0; }
.action-block b,.action-block span { display: block; }
.action-block b { color: #0f2742; margin-bottom: .35rem; }
.action-block span { color: #475569; line-height: 1.6; font-size: .88rem; }
.kpi-section-title { margin-top: 3rem; margin-bottom: 1.1rem; }
.kpi-plain { height: 100%; border: 1px solid #e2e8f0; border-radius: 13px; padding: 1.4rem 1.5rem; min-height: 230px; background: #fff; }
.kpi-plain b { display: block; color: #0f2742; margin-bottom: .85rem; font-size: .98rem; }
.kpi-list { height: 100%; background: #fff; border: 1px solid var(--line); border-radius: 13px; padding: 1.4rem 1.5rem; min-height: 220px; overflow-wrap: anywhere; }
.kpi-list strong { display: block; color: var(--navy); margin-bottom: .85rem; font-size: .98rem; }
.kpi-items { list-style: none; padding: 0; margin: 0; }
.kpi-items li { position: relative; color: var(--body); font-size: .86rem; line-height: 1.7; padding-left: 1rem; margin: .45rem 0; }
.kpi-items li::before { content: '•'; position: absolute; left: 0; color: var(--blue); font-weight: 800; }

[class*="st-key-validation_outcome_"] { margin: .75rem 0 2.35rem; }
[class*="st-key-validation_outcome_"] .validation-outcome { background: #fff; border: 1px solid var(--line); border-radius: 15px; padding: 1.45rem 1.6rem; margin-bottom: 1.1rem; }
.validation-outcome > strong { display: block; color: var(--navy); font-size: 2rem; line-height: 1.1; margin: .9rem 0 .35rem; }
.validation-outcome > b { display: block; color: #9a5b08; font-size: .85rem; margin-bottom: .65rem; }
.validation-outcome > p { color: var(--body); max-width: 850px; line-height: 1.75; margin: 0; }
.stat-summary { display: grid; grid-template-columns: repeat(3,minmax(0,1fr)); gap: .75rem; padding: .4rem 0; }
.stat-summary > div { background: #f8fafd; border: 1px solid #e2e8f0; border-radius: 11px; padding: 1rem; min-width: 0; }
.stat-summary span,.stat-summary b,.stat-summary small { display: block; }
.stat-summary span { color: var(--muted); font-size: .76rem; font-weight: 650; }
.stat-summary b { color: var(--navy); font-size: .88rem; line-height: 1.55; margin-top: .4rem; overflow-wrap: anywhere; }
.stat-summary small { color: var(--body); font-size: .78rem; margin-top: .45rem; }
.stat-summary .stat-limitation { grid-column: 1 / -1; background: #fffaf0; border-color: #f3dfb9; }
.stat-limitation p { color: #6f4a12; line-height: 1.7; margin: .45rem 0 0; }

.methodology-head { margin-bottom: 2rem; }
.methodology-head + div[data-testid="stTabs"] { margin-top: .25rem; }
[data-baseweb="tab-list"] { gap: .65rem; }
[data-baseweb="tab"] { padding: .8rem 1rem; }
[data-testid="stTabs"] [data-baseweb="tab-panel"] { padding-top: 1.75rem; }
div[data-testid="stMetric"] { background: #fff; border: 1px solid var(--line); padding: .78rem .9rem; border-radius: 13px; box-shadow: none; }
div[data-testid="stMetric"] label { color: var(--muted) !important; }
div[data-testid="stMetric"] [data-testid="stMetricValue"] { color: var(--navy) !important; }
[data-baseweb="tab-list"] { gap: .65rem; border-bottom: 1px solid var(--line); }
[data-baseweb="tab"] { color: var(--body); padding: .8rem 1rem; }
[aria-selected="true"][data-baseweb="tab"] { color: var(--blue); }
.js-plotly-plot .plotly text { fill: #334e68 !important; }

@media (max-width: 1100px) {
  .st-key-top_nav > div [data-testid="stHorizontalBlock"] { gap: .25rem; }
  [class*="st-key-nav_inactive_"] button,[class*="st-key-nav_active_"] button { padding-left: .15rem; padding-right: .15rem; font-size: .78rem; }
  .block-container { padding-left: 1.2rem; padding-right: 1.2rem; }
  .hero { grid-template-columns: 1fr; padding: 2rem; }
  .kpi-row,.process { grid-template-columns: repeat(3,minmax(0,1fr)); }
  .process-step::after { display: none; }
  .detail-hero { grid-template-columns: repeat(3,minmax(0,1fr)); }
  .detail-main { grid-column: 1/-1; }
  .location-visual { height: 300px; }
}
@media (max-width: 760px) {
  .block-container { padding: 4.75rem .8rem 3rem; }
  .st-key-top_nav { min-height: 56px; padding: .4rem .5rem; }
  .brand { display: none; }
  .hero { padding: 1.5rem; border-radius: 18px; }
  .hero h1 { font-size: 2.15rem; }
  .kpi-row { grid-template-columns: repeat(2,minmax(0,1fr)); }
  .stats-strip { grid-template-columns: repeat(2,minmax(0,1fr)); }
  .stat-item { border-bottom: 1px solid #e2e8f0; }
  .method-line { grid-template-columns: 1fr; }
  .method-line > div::after { display: none; }
  .process,.peer-grid,.strategy-links { grid-template-columns: 1fr; }
  .detail-hero { grid-template-columns: 1fr; }
  .detail-main { grid-column: auto; }
  .page-title { font-size: 1.72rem; }
  .service-hero { padding-top: 1rem; }
  .service-hero h1 { font-size: 2.35rem; }
  .location-visual { height: 230px; }
  .preview-row { min-height: 0; }
  .kpi-plain,.kpi-list { min-height: 0; }
  .stat-summary { grid-template-columns: 1fr; }
  .stat-summary .stat-limitation { grid-column: auto; }
}
</style>
"""
