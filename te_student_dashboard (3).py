import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Critical Materials for Solar: The Tellurium Case",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Always use the light theme ────────────────────────────────────────────────
# The dashboard is designed on light green backgrounds. Without this, a viewer whose
# computer is in dark mode gets Streamlit's dark theme: light text on those light
# backgrounds, which cannot be read. If this call is ever unavailable, the fixed text
# and chart colours further down still keep every page readable.
try:
    if st.get_option("theme.base") != "light":
        st._config.set_option("theme.base", "light")
        st.rerun()
except Exception:
    pass

# ── Light green theme (same as original dashboard) ────────────────────────────
st.markdown("""
<style>
.stApp { background-color: #e8f5e9 !important; }
[data-testid="stSidebar"] { background-color: #c8e6c9 !important; }
[data-testid="stSidebar"] * { color: #1b5e20 !important; }
h1, h2, h3, h4, h5, h6 { color: #2e7d32 !important; }
.stButton > button {
    background-color: #4caf50 !important;
    color: white !important;
    border: none !important;
    border-radius: 6px !important;
}
.stButton > button:hover { background-color: #388e3c !important; }
.stSelectbox > div > div,
.stNumberInput > div > div > input,
.stTextInput > div > div > input,
.stSlider > div { background-color: #f1f8e9 !important; border-color: #a5d6a7 !important; }
/* Text and number inputs share one look: same fill, border and corners, and the
   +/- strip of a number input is part of the same box (current and older Streamlit markup) */
[data-baseweb="input"],
[data-baseweb="base-input"],
[data-testid="stTextInputRootElement"],
[data-testid="stNumberInputContainer"] { background-color: #f1f8e9 !important; }
[data-baseweb="input"],
[data-testid="stTextInputRootElement"],
[data-testid="stNumberInputContainer"] {
    border: 1px solid #a5d6a7 !important;
    border-radius: 8px !important;
}
[data-baseweb="input"]:focus-within,
[data-testid="stTextInputRootElement"]:focus-within,
[data-testid="stNumberInputContainer"]:focus-within { border-color: #2e7d32 !important; }
[data-testid="stNumberInputStepDown"],
[data-testid="stNumberInputStepUp"] {
    background-color: transparent !important;
    color: #2e7d32 !important;
}
[data-testid="stNumberInputStepDown"]:hover,
[data-testid="stNumberInputStepUp"]:hover { background-color: #dcedc8 !important; }
hr { border-color: #a5d6a7 !important; }
[data-testid="stDataFrame"] { background-color: #f1f8e9 !important; }
.stDownloadButton > button {
    background-color: #66bb6a !important;
    color: white !important;
    border: none !important;
    border-radius: 6px !important;
}

/* ── Fixed text colours ──────────────────────────────────────────────────────
   The backgrounds above are always light, so the text on them must always be dark,
   whatever theme the viewer picks in Streamlit's settings menu. Colours written
   inline in the page content still win over these. */
[data-testid="stMain"], section.main { color: #2f2d2b; }
.stApp [data-testid="stMarkdownContainer"]:not(
    .stButton *, .stDownloadButton *, [role="tab"] *, [data-testid="stMetricDelta"] *,
    [data-testid="stSliderThumbValue"] *, [data-testid="stSliderTickBar"] *, [data-testid="stAlertContainer"] *),
.stApp [data-testid="stCaptionContainer"],
.stApp [data-testid="stWidgetLabel"],
.stApp [data-testid="stMetricValue"],
.stApp [data-testid="stExpander"] summary,
.stApp [data-testid="stIconMaterial"],
.stApp [data-baseweb="select"] div,
.stApp [role="tab"][aria-selected="false"],
.stApp [role="tab"][aria-selected="false"] [data-testid="stMarkdownContainer"] { color: #2f2d2b; }
/* (the :not list above leaves accent text alone: white on buttons, the selected tab,
   slider values, metric deltas and messages keep their own colours) */
.stApp [data-testid="stSliderTickBar"],
.stApp [data-testid="stSliderTickBar"] [data-testid="stMarkdownContainer"] { color: rgba(47, 45, 43, 0.7); }
.stApp [data-testid="stTooltipIcon"] svg { color: #2f2d2b !important; stroke: rgba(47, 45, 43, 0.6) !important; }
/* typed text, placeholders and the answer boxes */
.stApp input:not([type="range"]):not([type="radio"]):not([type="checkbox"]), .stApp textarea {
    color: #2f2d2b !important;
    -webkit-text-fill-color: #2f2d2b !important;
    caret-color: #2f2d2b !important;
}
.stApp input::placeholder, .stApp textarea::placeholder {
    color: #9d968e !important;
    -webkit-text-fill-color: #9d968e !important;
    opacity: 1 !important;
}
.stApp [data-testid="stSidebar"] input:not([type="range"]):not([type="radio"]):not([type="checkbox"]) {
    color: #1b5e20 !important;
    -webkit-text-fill-color: #1b5e20 !important;
}
[data-testid="stTextAreaRootElement"], [data-baseweb="textarea"] {
    background-color: #f8f8f7 !important;
    border: 1px solid #dcd8d4 !important;
}
.stApp textarea { background-color: transparent !important; }
.stApp [data-testid="stExpander"] details { border-color: #dcd8d4 !important; }
.stApp code { color: #2f2d2b; background-color: #f7f7f6; }
/* messages from st.error / st.success */
.stApp [data-testid="stAlertContainer"] { background-color: #fff1f2 !important; }
.stApp [data-testid="stAlertContainer"],
.stApp [data-testid="stAlertContainer"] * { color: #9e303b !important; }
.stApp [data-testid="stAlertContainer"]:has([data-testid="stAlertContentSuccess"]) { background-color: #e9f7ee !important; }
.stApp [data-testid="stAlertContainer"]:has([data-testid="stAlertContentSuccess"]),
.stApp [data-testid="stAlertContainer"]:has([data-testid="stAlertContentSuccess"]) * { color: #0c5a44 !important; }
</style>
""", unsafe_allow_html=True)

# ── Helpers ───────────────────────────────────────────────────────────────────
def info_box(text: str):
    st.markdown(
        f"<div style='background:#e8f5e9;border-left:4px solid #2e7d32;"
        f"padding:10px 14px;border-radius:6px;margin:8px 0;font-size:14px;'>{text}</div>",
        unsafe_allow_html=True,
    )

def show_chart(fig, **kwargs):
    """Draw a Plotly chart with fixed colours.

    Streamlit recolours chart text and grid lines to match the viewer's theme. Every chart
    here sits on a light background, so those colours are set explicitly (only where the
    figure has not chosen one) and the chart reads the same in light and dark mode.
    """
    lay = fig.layout
    if lay.font.color is None:
        lay.font.color = "#808495"          # tick labels, axis titles, default annotations
    if lay.legend.font.color is None:
        lay.legend.font.color = "#262730"
    if lay.paper_bgcolor is None:
        lay.paper_bgcolor = "#e8f5e9"
    if lay.plot_bgcolor is None:
        lay.plot_bgcolor = "#f9fbe7"
    for ax in (lay.xaxis, lay.yaxis):
        for prop in ("gridcolor", "zerolinecolor"):
            if ax[prop] is None:
                ax[prop] = "#e6eaf1"
        if ax.ticks and ax.tickcolor is None:      # only where tick marks are switched on
            ax.tickcolor = "#e6eaf1"
        if ax.tickfont.color is None:
            ax.tickfont.color = "#808495"
        if ax.title.font.color is None:
            ax.title.font.color = "#808495"
    st.plotly_chart(fig, **kwargs)

def go_to_page(name: str):
    """Ask for a page change and rerun.

    The sidebar dropdown is already drawn when a page button is clicked, and Streamlit does
    not allow changing a widget after it is drawn. So the target waits in "_goto" and is
    applied at the top of the next run, before the dropdown is created.
    """
    st.session_state["_goto"] = name
    st.rerun()

def formula_box(title: str, formula: str, example: str = ""):
    content = (
        f"<div style='background:#f1f8e9;border:1px solid #a5d6a7;"
        f"border-radius:8px;padding:12px 16px;margin:8px 0;'>"
        f"<b style='color:#2e7d32;'>{title}</b><br>"
        f"<code style='font-size:13px;'>{formula}</code>"
    )
    if example:
        content += f"<br><span style='font-size:12px;color:#555;'>Example: {example}</span>"
    content += "</div>"
    st.markdown(content, unsafe_allow_html=True)

# ── Session state defaults ────────────────────────────────────────────────────
DEFAULTS = {
    # Project
    "student_name": "",
    "student_id": "",
    "start_year": 2025,
    "end_year": 2030,
    # Supply – Direct Mining
    "mine_base_production": 100.0,
    "mine_growth_rate": 5.0,
    # Supply – Byproduct (fixed defaults, not student-editable)
    "bp_copper_anode": 29.0,       # million tonnes
    "bp_te_content": 110.0,        # ppm
    "bp_yield": 50.0,              # %
    # Recycling (CE page)
    "rec_retired_pv": 10.0,        # GWp
    "rec_te_intensity": 67.0,      # kg/MWp
    "rec_efficiency": 90.0,        # %
    "rec_collection": 85.0,        # %
    "rec_rate": 100.0,             # %
    # Demand – PV
    "pv_production_start": 626.71,
    "pv_market_share_start": 7.27,
    "pv_te_intensity": 24800.0,
    "pv_production_growth": 10.0,
    "pv_share_growth": 0.38,
    # Demand – Non-PV
    "nonpv_base": 455.0,
    "nonpv_growth": 4.0,
    # Calculated flag
    "calculated": False,
    # Circularity Reality Check
    "crc_panel_lifetime": 25,
    "crc_te_intensity_scenario": "Constant (67 kg/MWp)",
    "crc_collection_stress": 10.0,
    # Policy Brief responses
    "pb_sourcing": "",
    "pb_method": "",
    "pb_ce": "",
    "pb_risk": "",
    "pb_submitted": False,
    # Navigation
    "_current_page": "🏠 Welcome",
}

for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Sidebar navigation ────────────────────────────────────────────────────────
st.sidebar.title("Critical Materials for Solar")
st.sidebar.markdown(
    "<div style='color:#2e7d32;font-size:15px;font-weight:600;margin-top:-10px;'>The Tellurium Case</div>",
    unsafe_allow_html=True,
)
st.sidebar.divider()

PAGES = [
    "🏠 Welcome",
    "👤 Student Info",
    "🔗 Hitchhiker Concept",
    "⛏️ Material Supply",
    "☀️ Material Demand",
    "📊 Results & Gap",
    "♻️ Circular Economy",
    "⚠️ Circularity Reality Check",
    "🌍 LCA of CdTe Solar",
    "🔍 Scenario Analysis",
]

# The dropdown's own value ("_nav_select") is the single source of truth for the page.
# A page button's request (see go_to_page) is applied here, before the dropdown is drawn.
if "_goto" in st.session_state:
    st.session_state["_nav_select"] = st.session_state.pop("_goto")
elif "_nav_select" not in st.session_state:
    st.session_state["_nav_select"] = st.session_state["_current_page"]
if st.session_state["_nav_select"] not in PAGES:
    st.session_state["_nav_select"] = PAGES[0]
page = st.sidebar.selectbox("Navigate to", PAGES, key="_nav_select")
st.session_state["_current_page"] = page

st.sidebar.divider()
st.sidebar.markdown(
    "<small style='color:#2e7d32;font-weight:600;'>How to use</small><br>"
    "<small>1. Enter your name on <b>Student Info</b><br>"
    "2. Learn the <b>Hitchhiker Concept</b><br>"
    "3. Set supply parameters<br>"
    "4. Set demand parameters<br>"
    "5. View <b>Results & Gap</b><br>"
    "6. Explore <b>Circular Economy</b><br>"
    "7. Challenge assumptions — <b>Circularity Reality Check</b><br>"
    "8. Study <b>LCA of CdTe Solar</b><br>"
    "9. Complete <b>Scenario Analysis</b></small>",
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: Welcome
# ─────────────────────────────────────────────────────────────────────────────
if page == "🏠 Welcome":
    # Banner photo: CdTe thin-film modules (image embedded so the app stays a single file)
    _FS_PHOTO = "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAYEBAUEBAYFBQUGBgYHCQ4JCQgICRINDQoOFRIWFhUSFBQXGiEcFxgfGRQUHScdHyIjJSUlFhwpLCgkKyEkJST/2wBDAQYGBgkICREJCREkGBQYJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCT/wgARCAKKA7YDASIAAhEBAxEB/8QAGwAAAgMBAQEAAAAAAAAAAAAAAAECAwQFBgf/xAAZAQEBAQEBAQAAAAAAAAAAAAAAAQIDBAX/2gAMAwEAAhADEAAAAfcNnfgiQIYIbIkgQwQwRIIkgiSCLYIYqGCJAhghghghghghtItghghghioZCGUhuItghghghsi2CGKhuEMESCJIEMlQwQwQwQ2RJBFsEMEMEMIkgi2CUkJjEMEMEME2CGCGCGyJIEMMgPeQGIYAMQwQwAAAAYIYIYIZCGABQBABQMEMhDABiGCGCGCJKEwtBkIYiGKAxDBDBDAAgGKhgAAAAAAAAAwQwQwQwQwQwQwQwQwQwQwAzZaTFqzZg+kTAAAAAYJgABkA1lgAwAAAYhghgAAAAADAAAAAIAAAAABlAEACjQAxEMUAAAAIGhWIGIGIGJgADQMTAAAAAAAAAaBiBiBiBiBiBiUSIumUqLxOgAITpyokjjrFunMtaPRliBgAAAANAxBlaeoNMAYAAAAEAAAxMAAAAAKAIAABiGAAAMAAAgAABQAAAAAAAQwAAAGAEAAAAAAAADEDEUxMAAAAAAACqLTFrylh3YZZyx5OGrOtx+hEr/NbOOu9CjP7MdLlriee9+vHfz1p28Pf1z0o4qus6M67O+QAYgYmAFABladgwAAYAASgAADEDEwAAAAAAQBqAAAApAAAMQwAATQAAAAIYgYgYgYgYiGIGIpiBiCREJEQkRYxEMAAAaBiKYgrzrn+fVldHD+b09xn89s0XJ6OHyah3eUtzdy283u5eZWbbuJfwelzc3f9HOumNfSV9vz/AKvrJT5/Q9eGI3GIGIGIpiDO0waYADEDAAAAAABgAAAAADTAAAACITw6c20CwaBiBoAAARTQAAAIYgYgaAAQxMAAAAAAAAGIGAMRDEDE1YhHnvrXmcHqcv4vacFv42FmKepjjloO5LPoxc+bp5esuz41xtezbR6cc67Zh8Ouno832+z0+vlV/W59PVy+n2y2jtGIGIGIGIM7GDTAAGmAAAAADTAAAAAAAYAAAmiGC453hdfhni36avn0d8+hsrn6YxAArGIGIAEMQNAAAAAAAAAAADQMQMQMTAAGhWIGIGIRgGfl7eJ49LJZy/Dtyr1eXrz+vyb7noUwz7dmGLR688nq+fqw6m3hLbp4uTPOO/dyLPB0t7OXVu21zpss25efqeyu83o63obvPb/TjsqK+lzmIGIKwajTAAGmAAAAADQMAAEAFGgYgYgpjZzOTTyJT8942eK8XSz0WLV7OfV083R6JtA7QEDQAAAAAACGIGIAAAAAGIGIGIGIGIGIGIGIGKKzKqYvlxV5rr5ebtnk7KM/y+s9uCnjrbVRj3Ojt5ezjTRWdc83H6LB3vIz9rd1x57P6nLiczqZNmU1qz5t+lbGsuWN3mvX8vt63SZenn7nqxT0ZP6mADpAArFGWb41uHUaOhgA0DEDEDEwEwaBiBiBgACM/nPU+P8ALa6M2Twbt73l9mp7nmcTX6M6fReZ9R0XqifplojUaAAAAAQD59+LpEbjEDSYCBiBiBiBiBiBiBiBiYBSQrx8/wA109ng87hqqEK/Drrc+fB00WUaajZz7eGrjVVbc1m4NuNaJY7eJu3Nee67LPNcDpO31fLehzquPUr75i44umeF3sGjrNFXqYdpzfWee6htdFnvzMiWSIhny8DD49WauTv4PZ2YNn0ZIwbCwT1AAABiAdc5WJ2DQMQMQOIpcvD6OXy3yWPr5PFvk6r9BRGZHo/R+V6Xtxf2ON0us0vJq7GIsYgBA8tPL43Lr4Xd819Ec7b7c2CNGIGIGIGIGAAAAAAMQMQPmQ874tWKqfh3q4yjx1ZPBZ5lsMmnrOdXee3PM9Bkz411zlzXXHJculaFwtMNGzU43XjyOU6tOfQlPq+D6z7vKOHnWeHpz5aeb47M69nrzyPU8H0Poz18mKXaQ38nV5ddOfnux3agPZj5jLIfI3p04ux2z6S7l8Hu9D0eF6PbQ4vvGADQNKK1XczocrcROskAjEDEhVYThdfnO/5zha+Vt5/k3u5d1mby91M9zrRwaz0G+le7nr14tPaXCOhoAMWuPN8Hr+S8OjpcjRi971XhPTdZ29PD6PpzrXO1aaBGjEBju8dyvbr81p8uvdy4568dg523Syvm+f5PYvy99bLvJP5vTucSmjhq6vmadTo28iPn10stWrMhK6fSxlm1clXE7WXtOfTo2+yZ8WnF0vpb/M93ybV9GHzZjCPY9Ux9rlauDpX8uXSZ6ttPm1Tv5t1WXZM1nYeJc7tzvlbve28v0/vxp20X/V5MRt8vwdTN8rWffVt9Es0ZtZ0e9h0+ma3F9DEDEBxuvyedx7/Oy899AcLeehs893O8trlw8ujX52z5+9HMVXG6KMtGLoreeL1j06SmWGfp+d63Sdurj6ek7Pd8x6H1Z3oq9uS3jdfLlTxczy3X5fVxuGtUdJy1qv5d0m/byd3HWvp8c7Z9Nn4VXR6mnlr14jy3T5umX03mtvfHbosy1ls5c/Bq+OXZrOzXkxemc3olHj6X5cvOjRfC+LY8/divo8e/LXfjli8/XsqsI5Onq8q+6zZee9H53oPR8DsSQq5/b4Odtu0LyupnSXXc+/jdPC79UnL2Wc30utXfDnqq+MuK4y27dbbzD28/U3cjr/Y5AG3zCiVvy+nC3Gn0533ZepZb6rh9HtOhXy9GnQA0cJZ5q3E8XHXNwVaPPK49F8NPv+U0SdXz9+LzW4Dzb1wx17Za7qe8uipxkvyZus3zo6GbVTBV2MlDs63sPH+192LeR0OJ6c4PSeDs8mvUeY2eZ5ulnUOG7q6oakr82kutx7vPdFuR8dbFyXJ2rMD6NHO3ZeyOkXSWc+6i5qFl1OjGgLt3P2Zt1Kw+Lccvb5/VddzdES5d2zrOb2OFp6OhLBb570LadPk1Rnvz9pcRjtqzZbsTB0oy72uF74zZRVZyToqhpn6fHh6JvXM69t7y7/Ot15rcb5dltG86781vNsptp7zqej8/6H7XKYj05+XS0YvldLNeTfvNK058r9PM1dXS9N5zs+vPQA6CqvNjWDzXoeR498qHX0JyOzzd3Nktdvnq4fQv5q5yhw3RVpy9ZB44dU9GXHqdjlbYkLufbp2qsF/ntph09Z0vZeK7XbPZ4F/L565OXUjI7att0Zc3C5Sp3NKy6I0buXu5W9TXluOvpZOrHuzSk3X5as6uein0ZpSh1xfztPP0lDZn6rNlenhcWio5tMqNfl6HPJdGfO5d882WzP6JZ08Nnlt0s+eOnZjvuulXg2eJGqOXrmPThPVowdyvDmR6nJ6SzTj01md+yIdDFbz1HOY2dkuL09tFlVMu6zk7bNurCHrY+c6n0cemOee7HzyzHt+Z1tlzevnNefVlzdfb8pu9+ffT43S9M0xyZJel5Ttcfz7I4auU0WU8uzuLmwxexyVbyufdyNnnXTgsbu5+/BqUcfs8r1Z04tOy3n9XHdhFbuTHWwzzD0romnXw+hysyiEc7Vwep6MwKbLd1Fqw5cJ4fVO3by9PC6HknJtNFPnttvP3VBXrz3JdU+iZV1+rnq7N2wRm0npz1+fpGjqPcwXZ5lsuVPJGWrpNGrHZvVWPr8zrDTk31qrxR87qTx3c1K05NNRVttsxqvhNmrHmxYyyv056uSuWLojguS2eHp04XUVKu+PSbCm1KK9y75vloqtx9Plnr5984Bt57rYur4OuLrxXK856eT0G1+q7553peNdnpG/NZw3HlXYNZ1YJ69c7OfTsrFusyS3VwOeqtG5+e4atcPOWPdTurldKW5waOlxvZnpXbN/mrorfG569mbrLIG2XjdpW5Rrq59dTnTWzt5fR1L6K4U8+3Hu6arKszmXC9Gd19FHDXQ1YulxGOvnyb3J4p08tvC05uyeqcSvdL0Z4u2rYSpp6nm3WrMy8uyOvrjlX6cqa4ZNm9059dHpZt1e1z51PW1bnPr7F3N5nf0r+uclmx83Oy9p95gw959c8S/q9Pbg9LXyNXLfJ9ecWzcQwQwDRfjVF2SiW2oNZAAAMWrlbPhenq0YFOnQ5N/V79Iel8F6XNovrh5fVqzzq6+ONMaunHNi2c3a6zT0E03c3byt0snMy60Muflq2nTdxue2a5uXqqXRry1zlnJ1xBSu1JyplixKuT1m+/my3NGboYNSyvXNbK6b8Xn3zl0k+fpSy5HRxdc5tGi+3OZenJdpVfntNfQy6zRX0Kek00aLox5PQVerPJs6q6ZyVdMOXp1vbKa3ZybOiuswS1nXNFsn0yiRSbsyrmqV0ZwoB2AMGb5cHSnysXp8qBQw1kAoGCb3ZuPbVgl1ZGWAAJgmAAGJ10fB9e23Lbnd9sJT01bOTub0XuyayZenk6eTn5e9T04czpXcnN6HlteTrOrZyOjm74Ty8701g3+S5o2VJpzdLhRpz6qZYQybOiq7LsrB1KoxpxaFDxaTczaYWd856d3Q9GeZPtx5vPYvYX+jPhdns7ek89q9DlxeLT0X358+3XLcx3X1aFuZ6iJGom2JqBKCagOxNsjJRiUEKDLE2CbnELCmW2lFAOxMYmaFo16sGLv52UoYayNFMAGa5cm14M3bgRYAWAEoAAAPWs6sOWHM0c674fp6le7Lz6WaOdpdOjXCGPRYoZ+nPnnR4Xq8Xd5Fzy6m/y7PV8nD0pPOz9Fl3uNNVklktkueefLsTOPh9NZ6M+T3eikcCPoFrPEj332nHv6ENzPO+W1M5m8oqrqyDmlc5zWFmrNjWjJgesxcjeUyEThAVNliYxMiShEAZQDBqMs4IhMNQBiZIjNwzbKoFAFgDAJrG3o0c7ox850AbyxAxOhq6WrTdlzdOOoBhrIClAAGqC+/FqnkpWcA1kAKLNWz4nq5K7U93h2d+23zWru2bcOj0RpwK/RnfhzZbVqc2fSn0zlu1VLKOd6iJQuZRTIuUaaiQKTqMiESgTWEwJKqBODaKakpLXVizq561EM3kCMShEVMLAYARicIiiZqAMTFK4oACgBAGDnDNshSDEajEwBg+m8bIcqMNBvA0DEUwYrNcM6tz5AYFgAAAAAPfLj1VYpdOZGoAIAAIPUzgcuk0nAwAkCIqxKx1GVsIshnLAI6koppGTQ4xATdJkInAYmFMrhE4NiY6ctccanXzoWSiG8g4w4xFTCwAAagikoBqAADIElKAUAWAMTsWa1SCA1AABgPbpxqm7mZpbqQ3kaaAAAUPVbjSMMFYGsgAAAMANZk3S5+dbuciwBWAAAAAAw9NKEuPRsKkQIZKQi2snXQayNRsnEYmRJxiUhtEyBKKYmFgQjLKI6QyxPZLGkc+snAN5TCCJFUBYAAOURarWUGrAHSJOIshLKAUAWAwTseaiqJKIWCZSGxF/RxrDtx8+XbiDeQBAABgFuqapvy55bqQ1kAAAYmDJkNGjLnWrFQWAFgAAAAAABttzpHNF9Q6p86SbG7VLKNIJOGoRC5TcbJKMiLbIsiSinUWOxEYjhIENWBsljUZYKiypmsptARisooQApNuFKEFsrRYAxEgTUJZwRQDRDYnJyjqgTgFACAMTfUmub1KOTm9PmBrIBYAADEzZNZddWONeUKAdiGCbBNgpazOrKMQAGsgMQwQwQwRZ0M6x68uKW/OzWUMT1UpnLpN53ElFVIGIcRwS1ESLlNIkhkSSpEYRJRVTK0lqunK58+iNNMFuWFciarjm2QgWWFTqbhKJFMFujUJaVFWusLSNEuiEETKiy11MsdNsspV5Y111KrnQrNKzsuKOjLl6dfMzrrciiVligtSZBkhSESujPthll1ZEwAsTQrQI2hWtGnNqtxUEos3lDZFTCBMIOQRU+hLzd2nkZvW4klZFWFQUwgTI9O5rnpKcqrlOIokiBcygupoqm7mp2uyknBYxuklZYrImqyWmzLmLKZG8pSBBCWdY0iSKiSBKBKKRZFtkSQIcZZwgCG7EME3OWuyNUX52UmFgAAapcuzTz866HLzlgM1EMRDACxa7b82dX5qnYmFgAAMTAB9LNwdCrnS7cQ9RMLAAGmAABMhp6GPGtfMylAGsgAgAAEMj1E0cekoxlScgbjAsrJlU7FZEjVU6nO5jNihbfFF2TJZpys1lDKTcZXBAhliGAEJUmIm1QMEWLNIQQAagDEOUsLHVFlKdIasAYhylhd0KM6vx88Ew3kAAAAAetZ06cwAGsgAAAAAa5cnRs52b0OWjUBlgAAAAAAD6OrGq48upRM3hMQAAmoAABDIh6iQ+XRtRJxJEZgMhWWVN2QJPWYO7TLl1ZcKbcQ95AKBKWSiIAUAAKMsopiGrAACZmhXEcQ1AABuWMpQidcCgCwAAADpmNuHKgNBvIAgAAChoszYyyVrKIayAAAAABZFd+7PnWjHlKANZAAaBoBgAWdnOub0sfMl2Yg1kAsAUAAAgAAWlc3T6HKxrqnmBfWEZ4Eoum4wJwUhSbpFmmMurJzrnoYYvphidDjGWSBBhQABGMsogA1YAASlLFwhDi1qAAmwTnDNnXApMLBMEMBbdGN1Wc3MW1BvIAgAoABPTm0X56FupC5AKAAAAaGbp40R56oA1kAAAAABiZ0s3ndiXFmutxkayAWA0AKAAAAQBLrX428/GrGg3kAPWOuHHpdCM7BtgzRLTqy83WelzU+mBhYMjElFg06AYCjLKKYmFgAA5yxcK4nANQAEMAnHNlGoADUAATALt+dZNeLny7MiNZYigAAAZqlzaoY83VlDUALAAAAAGtGvOs9+PPFtYbgAgCGAAABfLRt6GHGt3KyrUYGsgAAQJoAAABX9zOuZ0+dyZrZjDeEAAIAD0tqly22tMtGqjmXPT5ifTCcp1W51xKEXQwsYMAjLJRAYWDATLIhZCmW2oLBMpDBORmiqQAagAAAEupnXN6efky9PlhrIBQAgDVNaYz6pYs614kagBYAAAJgA+jm4d1fPl2Yw1AAALACAChgD6tuNqvkwADWAAAAAAAAADqy8vu2efzrs8BLUaCwBDQAChiD1einFy3vwQl0wiU6jMqlvqpaDT1lg6GoS2RhIGFgwBihyhGW2oLBBQME2ZoVwJRDQAQGCHvzrn9N8iXrceJYAagAAAmWRXdpzZ1fkpLACwAoABMAWyXH0J8/N6HMRYAWAFAAAAANaOvjWDfz+bLqyhvA0DEDQDAAABWFezs4sb3cbnKmg1kBDQAAAgaCAAhfv5fz/AFbnHtY3yte2mTBZZyu3Pqy85l9HP1r5GjM6Feanbc8M952PPZZY65aklFwhlJhYmMQyUIQiUGUhlACAaZrNsvwZvQ5ecsANQAAABgpa441ZTiKANZAIAAAoCyWvRrzZunFmdAFgAACAAAKD7EvJ7ceHm9TkBrIBYAAAAAAwBA+j1MbyW8bITgLeQABAAAIAAAIASh0COnX4fT8n6HVrlm68/V6fDdjz77PD34M6y8Dt8T6Hl9z1eL0Pm+uy/mWYvSWS66lCWqubb0XrPl6/VZbjz0PQ7dzyEfZYN5871tk954ir53fn2X5z0Gpa80DYsT1nZOPR1Hi4llaCuXTEglqRGIhgjRbNQeOEomayhggAAAYKWuWdTr54iYayAKAAAAABqMvS2czGunxs5YAayAABaASAAAwU+/nXG72bz2ddbkBvIIsAAEAAAiGgVoAT9Lm8D2e7x3LfrD5uV52UFw63xhGXV0OTbc9bmbObZ3eJ2eLXc6vlI8e3rNPip4172fg9/Pfs6/Paue+3CGjGqahGmWSRprsqkqfQnJm53o4r4XP7zz3s8/Uu8N386699lvl758O7DqeOnW/o+Hme18J9V49uDV6lcO3lq/Vw3nyfW2Lpjhw6lPTGV3Gs1uVG8WGeHTOsxx1naY/RWY7MEFtgn0wKRZEkhDBDBDZGzqmNWZOWhDN5TABAAwAoAgDbGPsbeJjfZ87Q9RDWsgAACAAAE1AAoFpT0/S38el3F87iqcA6cwQecIHi9UnXAunQGzPW7O5y41pqhSTV7oDRPKzWYnGq7BI7K5DzrtrjSOnLmOz0N/l3nXr6vMLN+g9P5hq5dPa+R3Q3in3Hzavpj6Ly+R57nb6Z0ejlm+nfLvp/DvuhVHx+jW8tsXGGCabsNidI5410a81aaKJV2mqpU8+uOs4Y77q4tPq1Z46n2NOs+Qq9tV0z46Xp5bz5iXcw7zo1V+a3joV8/L259tUMuVC1NBRK5sISpgag1KyN/YsxqWHkwIkjeYkkIYRGCTBDBAAmgOl7TnrzvpeL5DG+xwg68wCwQCAPNK5+H1UF0aqJbYwilSCYEQHBlkNmaIO/Mr2Yt0UQhsrLKedLSFxAgqtUQmMlsSrS2dW2yNOjJrOvMUSrucHTNd7X5Gzlv12/wc5r3ej53PN99p+d6s36NLwFmNe4y+XvzfQU8yUdavLONVbnNXlNaqVdmcXzyu3TZz7bZ112zOayaIZehbvXkeX7vk+jh5T2/lOd35/S83E73j9OXN2as3l19V6z57mek8h25dC3n8v0cvqnleL9B5dPNQ9dn568y/Rx3OA+tVvHON8d5wy0Q1KRR3mRCOs2lPSrL7Hu+X567Hickd5rJrplKaSKkqSlGEBUod+Hw/Z5uz0l+Z4Tp+izWeIO3b6rwJdK9ONn9P5yyM+hk0m9U8MFHSnbxdktSZSDbyV3Q6Yjp34MM1gtmQckko2ycay1wFuhWVoVMkVlLLpUhcqwsnQy4pReUs0xohGx4w2mYNtvMlL6jX4uONes1eLnHv6/E1y/Q7vnazr6Jl8PE+gbPnvQ569pR5rZNdCXntzOzy/rujXzPb1eD7PP9AXzn0/l79WXOjx3f5D0nmfRxv53R53r46fp3zL6f5O9ClT5ewrXUM2+S4au1KuBb1IW82++qMFmu6zl1TvvPu+R61fSch9wTjV+igz5yHpc3S8M9FmuOK9tHWUFhc7m6/k6p3QsmbLqLNbsxyrW2vVnzcVPeW5zOH62vUwYfRwy8rq7+Xd4+rcufPyeztXdunnKfXcnWeFPv8jox5Nq6TmS3PTBZPRbz4312QnOkmragQoashQDqLFDE7RW1yKUZDrlFRwnUlO2TMpwphGJThMtqQlhGFt9ZFJypktpVYFqz5uozGp0MtMo3Z67t57EuJKyu6qzNMt+Jd/0b5pp5b+h3fOquHT6LR4+zOvXw8wW+rh5rRznps3Lsb2S4vUrokM/NfTkK0WYEz0K3kL92Yt0Zt1DWbLoy6xupIy2mQ1ZpX8fNYrapNeLbkmnVuhrVdOvLz5yC+oRset5r4nORstjLTVrzXNlvK3zezPVoucGlX61ydGpXPIo68tzx+rq9fr181zfacycvLS9Pj654uHtQ3eOt9fRkUzSA5yVxl0l5a14663LdstLjCy6MbC+rS86zdHHREIynvNcp1DlUVbPORqqrmEXGrVAklbQLN1onCRUnW0biyzS8Os3vNbm6cVlNaJVSlnAROKZIgyc6JkyDHOkl3dHz9mb6aflnnXr5eQJfYPxpL7uzwuvN9Zm86S9jVxNB0LudTLrKCTs21V8Jsw7ceMTruqrTCqcl1GnE3Y8+npl2023cNOeGdb3Vjk6GerNOUrKLGpyvgaaoTz0lGzOkoWuYuhoz53OsqYvwbFc8irt5u1x83sdDO/E4PSafTjzR6nl73m3z1855Ovuy6uDDtw1nzc+vh3MZqhZn3VdPFzc7fksqbNZgpxtITZTY1UCbIpzCNkUrkCsixuDJkETlUxShIU62XxgEnWiwrCYJJADcCJpMJ1ytkQcjcSnOsJlYWuoS5VBZKlraq1VgiPeZ83P8fbuZq54WdDHp5s08m/WbbuX071hLNfMyvxV5aLcHRc+bv0QzKuTC3pprVZduWrlc5vnXbOlvNunM5NmTfRCGtrNOqvPN7ce/nMVdOnVjKvo9OnPsnkxLKds+lzl8Znn0djB11glbm0o0yVZVr6eZ53T1sWrxuN2+P6ONenP3NY41Hb5C0WN6jrJ5zAk6rdkLVFCyZAAsIJulC2JFtxAlCrFBlkYslCTEoyJKuZNUXkU2JwmRlGYRcRyIjdUkmkE0gnAAagWRJIxFf/EADAQAAICAgECBgEDBAIDAQAAAAECAAMEERITIQUQICIwMRQjMkEVM0BQJGA0QkOA/9oACAEBAAEFAv8A9mW2cAl/Mcxr/uTHiCzbsXcUFHrq1/2knUB35dQSslvVZKu86nF+Kkq2z/2i4kzH7LdcKwt3VYNxUWgu1nHy5eV2SFau8NLAbGR9yv6nKK3If9hsYqOttgd+T6nU4vd+qyXV0Gz9WrHtK2fkc2NoUWX8CcocLUNrYi+xnZDXdyeu3iWyQIgZio0P+wM/ErZza08XGT0YlyutpUksGazIat+ZLluIYcSpZLLLFahnFoVRyWz302KIW2yIpLIarb34tjBgOQ/7DkIXFTGmZD8zaGD1M6RmUxQqtbVzNTBGazT3XM5pXqWWoVephZGdq2ot5RmCTATmMi56WaxrV4PaVHFOXK3/AFX8/wC0scrLLOKdZiXtcoE6gr0xuoBrcgrQ04gheEtrdEp3W9zlnU1kBebpj8Vs5TCusqHM2LSCWSpeWxK17/6rnplbl/tH1qz3A18J1NGhVaOem/UdVvdtY5YhanLLX7Bb1VJAl9ug53MGpKwbfezpcqjjDe9cwbnlNjC18kCUWK3+p5iZNxpH5J3XkLpbeUe/jEOx/r7Syjqs0uv0z3dq2InM1nqGyVFdWqLTWPxZRZ+QbnNTV3Fb73r4+zkcc7ycsqK7nMN9dkR62lqWdTBbTHIfr2FTKyUWvKdRXaXll3BTnLK7eY/0diQ8bUsq4Ov31eEHKy8dh/r8jZCpZGoHG8pWce5LJYhefjlRQeNbW8VV+Sq/Sll6OOpyjuwAtUFsggtYWPWmKis6LxyEPEr9lR00pUzMYQW6leRqrrLan4XIYXPW5vf+gZuMZ9Q28haWoltzcha+xYbJiq6qhLNv/Ws4WBuQsK2szWUotrkfpkL4eaWru07HuNtFPCxaAYEIdRLMfUPLQHubu1SgRqyJigIznqTq7VLXAx7edjo6t2nBTavGuu6x6jh5Niyi1t/qPFGh/nv9G6C4K1/Gyt+4FTtKMEx36bi9QKTz/wBUTqK/KdaXMGXruV96vxRq7gUKdoL7ENj99lozFWqBMoYlrufJbFJ5S1CwFPvGKm2pVZdjNayYzidLp2XKi04++TJ03N4sRrRqt4tnVaqitl4jqVUcJr/Q3LtXIBsPBmv3Op78XMWs9ZZd+7kGNH7PkJ1/mdUc2PODJKkFbE8RuNVuHbYjWWnV17LPybHhs5QHZvpCk2ALWiWxwNVK1RazlEHFjZ7k2rWjkFpvM/cpcKldhNjVKrmrkE2xUBpm1LUnCzlVWHGPh27LvVKGPV9bNxX8vS0XGz/JPcZq8WI2HJ0hgs0TkMTZl7TEs2av22NqJvXxW3hTVb1P8o2ANlhFGPkrwuVQv5hU209coXSM+5aT1KxLVqVRboU1m9hQiDmHfpyxzK1LMRNi67nxauzlXtuNmxL32cPfUtDAV0vLqgH5aa3La8oeL4zPRbj29ZMjGSyNiNWMfkF5jfoVwwuuXiOVjq71un7ZvUB38J+MwPps77LEl2cBmJmnIrHYtyPhtfTL28YMjm6ntv4XsAOXb7vDrGsP+TmHjGTqvwWPk8qQvvB0/Hcfs1iaYvs5D7HLYqdOiLRw5gt1OBqJ3Zdxnv4Koua0ERXcRSIQdW6arG5u1m1C2qLMhjcd9+BY2UFkqRrGo59XC5XeVtvGG0mD2lbFach5DL4m24lxZ0zj39RqLS0J0GbqQe0fAx18Rn3L6n52kWK+LwjMCK69xNqCRsNyNFxYG5dVOFgf21d/gsv4WZb++5tPiW101/kBgp2P8bIteqW5TXEfpmx+M7gvt16bRnNYbZXmwRaNxkY2W4Z3y0a9pOJ5N2ZLByrFfVcgxNaX9jWooe79at2tc1trFY1LYRZOpq3nsmteJyGN3UGkCBat9fHuQS3IZbDbVYtL6e+4EI/KVgMs+msO5x6korKnD58bMhVK5gBR+t8NjTfwsNhO0vBKs7VPdZC/aq9AmRayE82K0ylhXLrg74tZUX3aWmzYB36/Em4nIyea2M0oJAF3GJZqmpuXw2ZSJB4iGleazOp2PQzhYtitGcILM3RXLHG25bow073cm6jFhaoL9jYCAqF4E4jpc4yaVG4qQWJ7WWNELQ91RtNjOqC7GUoK9qrdNOubD0WLUtp8ZeJcV9RrWaW1kOnLqi7gylTGb3o4LEFXDmXE8uqQevzdEstFNIRfKywbRtzqqr4+aGssyWqj2uz4TI8DoB69gy3s6fW5v1bluSa2TKUm6wcbH0XPKN7os0rSz3GlzNgGrHDRLBTWmrZsKtf16Hu42fYzVJe4EMh3DcZR2KOXSrI4w3iNlASpgw9DuFmZaOoXGsQsSmVwWq8u/wCUOfIS7LFbX5ZvbCJD5buY9vtqPtNmjlBlFRMrs1GSG4hUs6oYdKI3vcLDlDipqZXcCZVMNYUpWthyK+KpoCnJ4Mu1NisVLMQuniOOnb7WrZieaMVdq4X2bOKIEW8VcUl+wwDUtZdsJtnZTwsYmylGstB6AqJK+VlQM1yNVXdP04LerOhyWjw/iRUo9ZltvSezIQxcsMi2GG1ufLQ8mcLDkqDZfMl+oAxWNlMY8sGwbQF7FR2gr4xhxAKSuvsePHZ3W+5V9eSuG8sk6dMrZzrQ0uea3FUltdvyGrAY2nTiEEzEOjZeElmVxnWDy/J6QstN8uRdJ75g9IDIPJ250IlrA/lvCxecJR7bPELxpSbZRtF4hxZcFnfqcTo3oY9leqlBljBQG5Rvcjo6SpWdLvaHH6NlfJcNVDdIZFuUnTsq7TfJDkcQg91dBD65Fx7kr6a7XkzKVb2hievWxSVMnLhp3082rLUNkHsMdTMbs7e8o415HbSrGPPYrJUO1mEyFV/FmLk9Vet7vVy3MoAy5kVjbxgyuUOQIt7MyHY3qZVvcWd77wK0csvE7uENzmB9ixfbUO/cRWBlp9oVwVsITQ2j8ILkSY1hsWctlX4ZH2MzalsjYuuLRuZdew5aht2a22EcKWc6WzmobpEt1IdqatS0ajOwJfnKxwam3puH4zIyeqOod8+29SqDpmWIplFew9p5Xt0lS7uEJazbSmsvZfidMV3bJLM1XdVflCRuw6DbMr09TVbiVCVqaxd++gdVtcKqzt6QsB1KiAXXlYHAR7V4UoLZXUIEW5rMcqO4dEawLWvGpURNKsr5bDmp1bScmlFZbzuyOI67MrFi1L2JK8i2+PduYKOWVAPIN382OoAJkLuWqDDkbnThDLKbOErvHC7L9vUZgm9KvOLpRbohy4flxaz6Dbn9s8uoos0S5YAxgwcaaEg2KmzjjVcs2llmWvUpyEsXMq5Sxgkc7HPvyjoWPHge5FSiWk6pbigfb3EAVnt9wMeDJ7OI2B3CLuxvaXjMBK3DRtMEbgA3KIy6r4glBMis2tdjhRjheBx+cPANfe17Yziu13BCHYe0CJX1Z0eKW1q6BiJ9yqwVnr9RnoAb8dqrFR2PTFbLsz+5W+wEtAW5RpB1XDBUaws/J+djsIo5FXap3TlLLfcG2G/Y/wC3tGt749zBkPITpKxFapWtY5LYAMPIFTLfj2vh3DlfkioLmclxxy9FvcLZxmRZtRYwZU5HkN8lM0VYWx15RYo1NnlZYUZnFgLbHZiv2bFl79uXAVLzCqJYPdvuLW1/7YjAvX+134y3IDG/92Pk9JsvLZ1Ls5QkRrRXORj2MR9zfILtZw5ryFc2DOuCersq05Gdb2KnKIBu0zfY610uYCEHZAS0PBxScVKu2oHLEHpBuRa1bN1G3i2yX4BeSB3yBtX5t+8Yzog5gGyzYRduSeV1ZCJ7Z+V3Y9SIttTs5YY5gbRJ7/ZZnCqXSW5DSrqM4qZZva4+mXuILNjirlDtx7BsRO9XbnRV1COwjr1TDVyFONxRsTUFQBW7pm5maV1M0qTgnm31aSsyrbNqRaptsrFNj2RF4rZvmimMey8xdy4znHblNcYTCAZ/7t+mOQdUKJbZevGlmntgxl5WERXOsc+6m32NdsWMZdbzbZEsLccVGJZe44g2A7F2gOLhvpNiI+oUUk18Z0+Lv7Ga0mUnkqJzLaWHcXvOWpyWcgJcxUgmVjRHvhGkbmq1tORM6XIMDXLXnJBMi6MhEMqPuT2nfEhy448VpXbGwI7iGisTook0Q+KXL3IUKM0KGLb0rGyOcTlbXchBopDF0VGWnqIau37F6+g1u4LCkYAmpwWZPfzVZUEdaMitVTJNlsA9rNsVPNxHOmfQp9xtcrKXsMqd2PlYSIuQHN7qpu4MKSFlnDhzCxbOS/jkkgIBZybUUiMQS47P2UKZvvZZoteWZfdP6esRAHa4sS09y1V2AhHlXaVWlhYdD+chB1JZ3Wu4xz7bn4RbCRdWLR3plZ2eqIrAhX4j8mEB41HGAcYG7q+lXYaoq7WsOZ00URu8ZWZ2q7aYNx4SxtAvuc+Mp5OSzKos5R7E0RuHH9pIAqbT/tNd3vtO4HYRbGafUa3tVYGGUSBU7tGTZ4lFLcwxQHfEZFfda9RX4xqmcrxUa9v5AA6r7Z9n3E49mlsOgp3ORVhZxnDmtY4iYzBSt3IbMFM6SxBqHuXbRxeJmPjJyCroDXkTHPtd93WcdVVqDkNtqSgFrqILagXt3OZ5ddQ3MmEzqATnMhiQDZCztaKmhTk1fItxYjpkmq5FYViNaQ9yCY6aCv7a7uK25PM70Mll59uHMSiwc31LVFitY1cpJaEjgjLriA795z0Fgcgu3I65Q/pkWCbG+em1ygjAxNrCvdVCvtUm+cq5lqF3bYqsUPAt3ljibUTmeXcrx7kGJuBdwVaVUESkx6isc6It3PyC0rV62dgAl0R5ra2rZERp+1DT364Ea7cF/uOio5MrDUQaC6rianSBjU7h2poY1rvm3LkRoDrq0qHTnJgK7OTrQWHuWMvKcuEXPMpzhYqE6svAHX3GyNAgc3G2st6ErfkL7hUa2L1FfbW0ZOUauU7Eb2ik8pYAI53LyeCJYpF5YpxpCP0rKnLMR3fHIYO0scGxKtkpwVLdxT1FWnjHY8Srq629RXx5w0oVgrftyHHFNqKOTw/t6nFalLwhVXmAPdv6C74k7jBYE2EADCoFbCFnPsp2GIRca1bgELtWg3xWusFuJb2tYREYu1/FT3Ykab3Ip/ttYCFaG0dIW2KA7Su7jGv72WVsDSQUXpRLOUPtKshP1GymC9VjBayR7dzrgT7JJmu9dIccHE1cZ0mhxyx6JJWviOI0EAKUNwtsr4eav7uRefine3FbZL1Hri2EMDVWd4yGljbpFbkV9sYy3ntbKxFPVt6qiW4VVi1YjqqtXBUhjOUnLkQO32o2kXuP2v8AvBV0jUlSzbjoz14q8Y/dQfbb7FR63UPxmRb7aQQao9ugGBjKGjU8WW1QSytA+hyANlS2pVX2GhLa2IO4l/Gcy8ZRoRK59Q26a7ZVeRRdK3LvZ5KSpuqdxW/RGNeULW7ilnK0WJLQoFn7j3mjyUHk/eXA2JVZqXpplXQUhk+24skx+NiXaivuKTqlNhwvLp7FeO6PxsIfCtaDAbX4Ii4SvP6PiUBMaqptD168q6HtnVpolljWt6Px+RVOIBhLCW184Kj1KQWdMZQiuFfJyeQRtr1OU26tkWWSvF5qEXGS/naarV11AVA7uLFiVtYVxBPx+mKyBCQxVexQbZ+JsHIOvt6bcqdlAq6ezpkPuXDmq1CtUbRCK4UIIRoHUst4sthjXBpxZnXH4hj3crXAfbW5Z7VOlvmRYDKuJVSESsc4DNgC2wrACxFntQ6LqGnPURkeOaUGxOoDLq+TpSqLxDWIvRllxjjkqJyss41ghHXeoLZjtyDV+++q1ymNfExbAPwXLHC5BMJVH9PpEGJQkFaiDtPv1Lh8FbOFYJ2fgrpsuJ6FEtue71ox2u2Nx4BCLBw7V2cLMe5LTQyiq/8Au75j+LLDXPygFNvWU1dILks0fNslCWXmqnU6A5cNkMlIe551eQOxF3EfcMsI5LYJ01llHONsKAdEAhF3FAjpzJ472Z1dP1eYsLpG087hav3ACW9Sb0VAMU8pb+lYL1slh0dd0Xu5BRR00xjufbZClpWOMbfINt1YacmLuMxZhubAh4slTEt0G5cGNSV+01llGDDhK0/CqWDFpWCmsQAD0a8uM6uvhrwmKnLqojO1jfAlbWE1048tyXtHwUMxJdlHW5RmYCq/kBRV0aya2q/aV0T3mhGfiRjo9lyrXHr6y3L0ilRML9KVZDOenY8sLUr1+vKidO3Eh9rXucV5tLEBYDQ5ERbOcD6JsBmwYEUT3RToPxhv1Y6hzUdHqBYbFZ6yBOwJbiRb7Twae0KmgbU7VKqy0BmSomMmgykGhOS8dTi00QDRYzHGcgYLwYkrx+M4CfjVmdNBOC+nXkTqb+Dj25gT7+CnDstH5GPiy26y9vgA3Px1pj5bFfiV+MDKzBFEX3L+OgVDpQ1YsLcYGNk6O4qNyvx7GOmxkFzsKWsB/H2TcQL7ibMVRxN1inhZaK8cVRXXdqBgyNrm80YSC2yxewgL3QngqWcgDuP1BZy9tdnEWsSauy2YvJ+l04zJYlduxpWcKVjtqI4lhe0mqxZRTZZFxXWV4tthu8PalvwlMXEUT8dDPxqYKlE0BNp0/UTqb9e9QnfwBSZzVYSSfXTi25E54uJL8m3JPwrjaByeE+/iALHoV1wHqgVMsVWneAlYE5KMZi4SIIW4xrFWNnoBtL1XHq3YoqVsy5o4yLWysZqzQ541kibcTJtdYl5IV9yy4VxD1IV6de9MLtC1vYl7Bue5Wn6n0d8p/Ke6duWQ3CEvZX+Nc1dOHkKG8LyLTT4YK5+Ok/GrMGNUIKxBXAmya66o+WxHnqdhC+/XvU3v4N/AFLTkqRmLfBTRZexXGxJfl25HxV4zMPyK6YzM7fEMfiGyeIh/SldyAkkxWldnUn8/QC7iNxexS6P1VNdQsLdOmfqI65ab51EoqiZNFtxah6YMgMFuTjc6kKNJ1e5UO2ikN/ayzvzMrG4+Lyn4brDh2GLgPv8AABgwaxBj1LOkk4icZqfULz7mpqagHdq1pj5Z16S3wb+DfwBS09iRnLfBXU9rdGjFl2bZavw10PbOpTRLLHtb4koZ166UxmLHy91q1U6gUBCqEKs0UGzpNtLVnUsSPYhlnvtNTCcLNUv7mydv+TbZKrbdNiG0f08A2eFZCuPDL5XhWADw/uuIqzoKZ+NVOhXAizsJvy15b1O59G4Xn3NTjNQCGoVB8wgffp5fBv4N/AATPasLlvgVS5/Frx5bnsV+Gup7T+jRLb3u+Oul7Typollr2n0dKBIW0Bwh+wvKM/Fq9w8jHquMbEZlp8MIYYp2MQaXApQjAx9rRWs6YnALDbqfc1Pqb9G9Te/RvU2TNTXluFp9zXoanpA5nAfZ9Bb4N/Bv4PuaCw2E/B9xcLpq2f0xvZ+BEZz0qqJZku4+JK2sbjTRLch7fWmDcAmGRDgIYvh9QgxahOkk6aTU3Pua8uU1NTU4cYbdT7mp9Tfo3qbJ9G9TZM1NefOffo1OhwDZgSHbH0cp9+vfwb+HiFhf4a8E8Tm148Z2sb4Nbn461R8o6+IAsegtMsymYfAPLfwcpqa8uAEN2p9+X1N+jep3Po2BNkzXo5T789eQx+IOWtcJLH0cp9+vf+Dx1DZ8NOFZav5WPiy22y5vhXG0pyhXPv41xdKcoIPi3O816fqb3OPnwAht8/qbmvPep3Po2BNkzXo5epcYhTlpVGZnPo3Pv1/U3v4N/AE7cwJ9/BRiW5E6uLiS/JtyW+GvGZx16qI7tY3xVYzWDr1UR3axvjHnrz3ua8+PGG3Xn9T7mvPc7n0fU2T6eU+/SuK3E5VdMZ2sb0b+D6hbfr1N/AEJnJVhJb4Kce3IP/FxJkZduT8VVD2znRRLLXuPxVUPceVGPLbnuPx/cXDOhNee9zXnx4w268/qbPo36fqb9PKffpTGZl/Iqoj2Pa3p369anL16m9T79aoWm1WMxb4KqbL26WNiS/NtvHw11Paf0aJbe93xojWHhTjy3Je0fJVitYDk1Y8exnYeXczj5fc4cZ1PP6myfRudz6Pqb9PKffprxndevTRLLXub079etTl8G9T79YUtNosZy3wIjWN+NTiy7Pd1+FVLHhVRLMh3HxAEzoJTHymI+Sqiy48sfFl19l58hszXl9zgFnU157mz6Nz7+LlPv014zuvWooltr3N6d/By+Dl8ABM9qxnLfAAWIw1pD55C/D9zorVGyDr41x9KcoVz7+RUaw9KnGl2W9o9I7zgFnU89zuZrzJAnc+j69XL1V4z2Dq0US26y4+nfwb+Dfq159lhYt56mvSmHxRs9KYW5HYnJZyWc1nNJzWclnNBOos6BVDlKg5Azks5LOazks5rOos5ichOQnPcx6WyDZemKzXM7cpynOcpznMzm05NOTTbzbz9QwYz1G/MrWs7nunununumjAgUGzz36S07ma89gTuZr0cxNic0nUSdRJ1UlVTXD8jFoluUbj1EnUSdVJ1ViuGLPwbqAzqCdQTqCdQTnEbkzOQ3KczOZnNpzacmm7DAfbtpszbTbzbz3z3zTmGsqLH5ziZxnCcJ0xOmJ01nTSVeGc1/Ix8SW2vfOCziJxE4rOImhNeWzFqdh1ggLsZszZmzNn11Y9l5PQxpbc97fJThPaGyacYMzO3r28982wm2M989898Jae4jTTi84NCNTvspybpzpLOks4pAgBK8jxE0JqVUPbC2PTLLXtPp7CE79ROpv4OwhffwcZ1dfDRiW3zrY2JLr7MhvhSprJyqpj2NYfiStrG6VONLsuy4fJTjWZB/wCNhy/JtyT8O53mvMtqdzAs15EgTkT5a8y2p3M16K6XthOPRLsiy/179X1Ds/Ae05fBxnMCffwUY1uQT+LiTIy7cn4kRrDqqmWXNZ8Y7wYq0izMPH5Eraxvx6cSX51lw+Mee9TuZrz3qciZqcfMsBO5gE1510vaT+PRLsmy71HtN+sn4OOpy+AISOQWEkn11U2Xt0sbEl+bbePhALTpJTHvZh8deGSpy0phJY/GO8rweC2Z/Bfvz1r4hN6nczXnvU2TOM15lwISWmvRXW9pPQoluVZcPT9Tl6/qb36+PbmFn36wpabVYzFvgVGsb8WrGl2e7L8Qx+IbJ4j46cWy6dWjFltr3N8mPg2XA5VGJLLHtb5u5g7ee5sma9BcCHk0+vQlb2krRRLcqy0erl8G/WF3OSrCST6gpae1Yzlvg+yMMVB8/gvxJjkr11qhJY/FVRZe2sfFl2TZf8tGLbkt/wATBmRlW5J+bG8PtyZ+RhYXn9Te5r0FgJ3afXnqLWXJSmiW5buPTv4N/ABuclWElvWBue1YXLfCmEeJzkojMWPwpQzjqVUx3aw/EiNYehTjS3Lexfkrre1vxaMOZGfZcvzUY1uQ3SxPD5lZ92V5b7b9JYCdzB56ioWJSuiWZjsPTuffr38AUmbVYST6/udlhbfw1Yb2L+XTiyyx7W+FKmsO6aZZa9vxjvBjCoPmED5ANxMAVrZ4hwXe/mVWcp4fXjLf4oxXzHoJAncz69AXZNddMszWI+Xc+/WAWntWFi3wa4wv8NGJbfOtjYkuyLchvhVGc8aqZZc1nyJikqcpaYSWPyUYD2g5lOLHsa1vl+5j+HNYr+IVYod2sb0DyLBZsmAa9AENa0x8069O9Tfr3Pv1gEz2rC5b4NanP4aca3IJ/ExJkZduT8QBadJKo97EfHVjPbOrTjyyx7W+THxLck8sXCl+Vbkt82NhW5JL4fh8yMu7Kb1bAGyYBr08AkbN4z79W/X9TfrA3NBYXJ+DU56+Gqmy5jXjYkvzbbx8Qp4g5GvkqosuP6GNLb7Lvlqpe5uhj4UyM628fNVS9zfi4+CMnxG28fAB6ejxDZgSElj6Pqb+Dfr+zxCw2H4AvbmBPv4ERrG/GpxZdn2OvxLjkqb1rhOz8SI1h6VWPLcp7R8gBaJgrStviJ4/MAWNXhwrS3xMIpJJ+EfXkKfactaozM58tTjDpZy+DfwcdTqa+AKTOSrCSx9YBYjDWkWeIFV+KuhrB1aqY7tY3xAFoMVaQ+YdfLT4ezK2dVjB3axvmxfDrL42ZjYIuvsvf4xFrJU5NdcZ2sbz1NhYbN+v6m/g1OevgAJm1WFi3wphEK2clIZix+Gul7jumiW3PcfjrxDxOWtQJLH5MfCtyZ1cTBl+Rbkt82PiW5LccTw6ZWfdl/N1q6w7va2pqamp9Q2ev6nLfwbnL4Nbm1EZi3w04T2L+XTiyyx7W+FK2tbjTRLch7R8dOLZdOtTjyyx7W+Smiy9uniYQyc63J+dK2sK4FOIuR4o7r8/OxVpuutnUyln5Vgn5yiNcBT10ac1Po15cpr1k6nf4dgQsT8NOLZfOtjYsuyLchvhALHopTLMlmHx1UWXn/j40uyLLz8iqXK4NeML/EGYfN9yjw0lW8Srxld2sb/AbD2bKir4+b3VYe8spWxWwsfWVRXTXUpdHympar8mxEOTyyreOR+VqfmJBlVwX1mdRZzWb7fc18H1CfhpxrbzvFxJflW5PxigIGyuI+NK3tbpU40uyrLR8n3KfDiUbxCvHDMXb5sXAuyibcPw6ZGVblP/AIOPgX5MGQksNd0vxyooybMQjJosQMhUsvLP3xx/7WV/d8PVTjKiCNZVWVIZRUsOFQ0/pmOYfCaJ/SV3kU2/hf0u8D8LLE6Gas/5gnVyFn5hE/OExgMin8pILUM5pOany16K63tfp4+JL8y28fEtBKnIWuEkn4gCZ+MtMszG4/Lj4NuRDkYuFLr7Mh/mpx7L2/GxfDxleJ25I/waqXubE8FrpF3jFGMRkOsXNMXxXQtyKiV7SjMWycgZn5NTUY5/Tyf7mD/4y8o4IgsKwZnt/Jn5MFwM5CbEJ2Taoi2c4IY4mkVUeusXYPEFFsFViq/4AYHBeHEyFnQypxyxMNWbJ8Wvsw3/AChBkIYLUM5rNr6q6GsnVqpju1jfGmP7TlCsHufkoxrchuOJgzJzbsn51UuavDVqW7xXipJY/wCAO8wvBbLo2Ri+GV5filuQZubm5yiuUIsS+V5RRsnvdR/ZyP7lOd0FTxRRP6jW8TKptn6OlRTD+mAy8gPcUO2cgfug2JyZpxczg6x1YmoMSQVl+D1zfXqV23+HNj51eUh2T9kMBDPEkN9ON3tzPYK7mZ6vDUspbwxt/wBPuEOHlrOllrC9wmM1X4lmb1ILkM5rOSz7+CvHawdWqmO7WN8iVtYRiU4gv8QssX58bw2y4PnY+ELbrL2/wcTw+7LanDxfDlzvGy8d2sb0jyReTOHrFvtNH9m/97zlNzc6jSrNsqn9U3KfEK2KZtGxkhw7CCxTCC0r4pPygs/KDMr7iNuK1bQ8TGprtS/w98cdHRwfFlsPtMPGNoHMf/iYx1bnHaU/3MbXQ2JxXRbiDZ27gsnJVw0CnDpn9PqJPhuo3hd2j4fkrGx8qqayZ1bBPyGEGQDLEpxKHyjdOQnNZ2+LW5XgcVfxAVAksfmx8S3Jb/h+HTKzrss/4NdL3NieCpSMvxarGXIy7ck+vc3Oep+RYYx3K7B0bjt3Pnvz3qcpy4lb3WHObic2xoM6zh+Y5HXYkXtyHiHE2eKFko8S9v8AUNPVcjgWLvJ8PruORRybE8RtwGqyKchMmZCccWs97mbp1b62PV+n0gZ0prsK4uzYQIOw4qSVSAJo3IA7JZDpo1fs6QiBShxqnl+JzqHheNwPg9M/o7GN4TkLG8NyxPxcpYUyFnN1nXnXE6wnVBmFhWZpbJowTZc1zTXlr46qXuZcGjDXJ8Uexf8ABALTC8FtvhtxPDK8zxWy8/D/AD6OZ0e82Zub8uU5Tl35TlNzflvUBmzORnOc5znPUW4rFzXU1eMhBf4pTkp1lg54rV5aZKZX9ykamRsClt20FuiNzqlStpMNmwMhhHs1FbcJ1OZm9wsixUWcTD977chrqDQM7iI5insRCSkJYuWivyYkA8KSTTjmNiVcsOsYpyT0GJPEZSbCWkauWF3E60606onUE5ibE5LOSwe40eGHjZ4ilCszWN/g4mBdltRgY3h4zvGtyyx7W+TXp3Nzc3OOx6Mek32OvBpubnKbhM3CZuDyA7dp2ldpqPBClrFhimW2cjSR1vz7EK+JnS+I1cfz6yT4jjFUzMeLfU8LKXLLraaYVmcUaOemy3WCWVlonsXms6yKEbqHpMIeoR1+EW7kOqIl86lc6iNOPGWvpiyb5CPYBBoy7Bsxo1dWWtOTdgNi5VGSnHsU1DRLMZA34atPwQRfQKa+tGt4jF8T/Hu8YzPyKQrtCLBOc6k5znOXlubHnry15pW1jYngi1jK8TpxEyc23JPwshU1VGxgvJgvldXqvy+5rXkfOgbFaczaor88YB2irpba+kZ9xE2NGd/L7iAcv2znOU37cUhbLq0Vr35GluKv3lPax+53qfwH1C4nMGJboG2DNPFfEjybxVzK/FWAPiu4PGEAq8Xqaf1HHdzdjsnSoCqtQCsxlico9KaZUE6Yj9SLsGwNDsRPbB3iUvtaNwViscFMyvDRbG/c1duI+B4ml0FgJ3qssxLb3qZ//ifzbvRlF9hiNqN3Vq1YdCmfjUQ4lMfBqBPhwn9PbX4d8/GyIarRONgnIznOcwqUyb6KKcNfEs6wuQSeM15a9d+HsVYrVxMR/wAgYbvL8U0s9J/p/TJhr4np7nBkjUkAwDcOuOK2ruHFb6WFjIVrEx/71uzaALFY7MrDO1zicjA8Jm5uHv6NzlqF5WfaYv2Sdzc36O0JEMGpyAHOc9zmJzG+SwXss/JeVeKCpG8ZraDxReFXjFfH+p4xH51evzEEXKEfKKoMtMhRYa26w3rqM9dixTWYOyZddWRW624ktxg0wvFGoao0WLdx5HIUStxYPELB+J/NhJDTH/eq+wrtddv3BV7kcW4935bZrFnUs4LZ7dGcjrnqbEbp66dYP9UrWm6tnvarUNVgJpyFHC6HYmxNpPZNCcJwg2T0wICsB/UZOYFYNL08cdMWPiuqWUOIakswip3XR7unqrHqFsNJtVTwyMlOjBV2uxyld/a5hqk9/IY5ox+Feu0dNfD9wifU32m/Lc3Nzc3Nzc3ucvLc3NwHflygfU5nXLvz3OZ3uEwPqfkMpbLssUXMrV5j8vz+Uo8QVIvitazKz1vlGemOn5dW7MnHK5nh/SBWvJFV12C1NteWDiBlB92by/EH73b2NMf96MQOXsLtDaoi3DbWIx9hPQ3OmNBK7g1NaToLx9oRak4hBL8hC1PG6PjBAVUimjkrUcGIHTVG0Vs30yIuOrhsZQbKqxaaljUaVX01rlYauTa7HfHWl0oNndukrTjq16CEXAGjSFT8R7LVpFdLUS1esb8YvbVjESxAarq9gVA4FWMrY/RWhR1Mm+usW2ZaKk46qn8wIWHlr4Pvz35fz5fxD6N9t9tzfo/mFtzcbUJm5ubnKbncnkBOc6p1+Xdp2ZmS8WhqrMdsXxEWC46lhYsiaa24CE7GOf1K7UKLbW612gR7a+XUDnXIt0+THpjeo22jUu0VGnTOjsJ0QS9Fa1qiIV7xXVhx0XdltdOU3ufy2nhISomzem4e6fuh0bLD3VGaJsoykx2Erb3xO4G1Q8RGXivbl01eIsCcq+mIKmYVJ+o6NzGIvU/EPTsw01lVi0U46oiUmvKvQ1HJTjVj4+2GMYwBmIP1uBLcY68YZb+kfL+R+37n89/Twbie0/iffoQKz9EtY6lHmp9nuIDNmaJ89QzvuCce7N2Jm/IfcGjEvNcuqVpXkkS32tVbs2jlG5CY594VjOJSNb3PiLsF8TOv6oIPEKxD4mrU1eKVrXRlqim/YXMrS0Z1TQW16sHfkwBDFixrSq1zG/UUsVm3rCXe7rqJ+TWouylAqyOVnULwkiNYKjWOAZNsWIP/AKAdOBf1f2msLy/+bcYFfpnfMjvW3GWKyMDzCXclvJ41+5ynEo/al9iwCw9McChrCp1GtxK7ci7Gqtuox5kUHJj0myV4zVNXjtRkdMG00TGo5XunJeM4zU0NfXmxg7wjXkmQ+QmvPevLH6YttHF62Cs5/Dabgn8zj2+4TqKPbDDB5fcWwibhYHz5Re535AvQx45EPaV66jOI/wB1fYbhC0+/L7m+259Tc5eQi9p+Q8XPIVvEFIGdWR+XSS2RjPCyAca3au2sOOBsdyrbAir1hVVuoI0NepbRYTw2qudllVuSl2I5b5MwnYq3T4FdNXtow2eXusHKZHJwP0wqK5sr51VhqoVBi97OopRXUtYfc6iUtNjnWNGxOqDxWVU3C3og15NHsfE6eLj41VN2iKL6pmVlXvoNDBTXVOPKDtP41uX66pXmDPov3h8lgG5Wa3g7mlRLG52T2xiDNzc32Ris3OU357m9+gTXlud4BDGsrKEKIW2au7t38l7HfbW5sQTYB/n6m++5uE7nKbm53mzN9gYWhbsrMItxSV57LPz7RBmsy15aKUya+K5taz8wQ5J5D3AdnKQqEstTc6h5G1dVuXUd43ulZCg++c10INbVlCKeLG9WZ2G330lr91AnIkVAtVYo5mvi91fMPZxmtF6tjhxN2uRVmQhWRjWxuAluLqvpVoldIvwfxuQvuak1++6yn9SrVcx7VSOdV8O91ARqumH6PFTGTUVPNP1DlXe7XfRhh8x6wO2vMT+RN78gdTffyHknZyZub0dzlPvz3578tz689+e5ubm/Lt5GGfxuEwHc6Qnd2PIRW1FtVzrnWtarNsrMAq2niKjyDcVdk41r3bpqICK3Dr0z7pra22dIow5oum4gU8V0Ttv5Yspdhqtg0B038fcrsBbfNlrHIVKV41KB0rptounXJxaiasbHx7bqeyKSlWOtkNbMDjbl9FbrTXjI7U80fHFN3SZmKETplQlZsbB0sagm0jR7mBC/q1NbmteQ8vqCHcHl9QfflvzHl9H6gPcjyIPn/GjDDNzfo3B83KbnU2Oena8lC9jEsFh/aLRyNnUgsBC9zxrntsjajMAOovJuq0Jax68fjL8mquDhcqfvWwl0LlqZsNSzc1PZHcsqEwKACVUsvM1a2F21dupWRsqC3UVYNGzhxsZuCciTXSLiK+V9NaoHPSVEFsrVK5k0cqqU6lVyayGx9J0TYbcELMfG4v0+hTkOz0QQdqlr2utET7mtQxY2poejc36u/mfQfM+jc3seR8t+W/P+Zub8/ryP1vy36LPs96/4sln3X/Zy/a9E/wDu320/9WlZPRP7KSedIH5dn7/EVHTxf7l37KAN0/tT/wAofss/uXk7r7mn+9VF7pZ/bH3kdq3/AGH9tJ2gA4H7/wDmoGrf/Fq/tCVfd/3/APOwS0npliHt73WHtj/up7q4AmR+3NA6n8rKADj56gP/ACfsQT+BB9w+X8eRg+vL+P5n8fzD9H7/AIEP0YI30v1P5WCN5N5f+sP3/JjQT+PL+TP4n8iDy//EACgRAAIBAgYCAgMBAQEAAAAAAAABEQIgEBITITFRAzBAQQQUUGFxYP/aAAgBAwEBPwH/ANhH9pYT/UgQqRrcykCRA0Kn+kkcoVBDRBwLY2ONxSMf9GlEQhkkiRInuNYRI18aNvlITggX+jIwYjNhwL/TSGl8V/IjBHHBOEbkDMpBTjUN/CWDRA/jc4zamQcFNSglSfZMGbsq7sj3r1P2pEW8E2cY00j2HuQRg6cXe7kQRg7lg1akRblRGE2PGZwjBU948Y1PF4TfGC3HSRdA8UhYwOkyEEDtXFk4RhG5ULBYIdkla9NK3IxaFt6asIFdJA8H6ZxeCsWCEN4VDsixD9rQlg/S7EsEPBixnBDWMYNk4SO54KkVNq+LGKMuE4IagWE2TjODaM6NSkfkpH5DUNTBIcrnBUOYZXCew6pVlK79bdrsnFrBYPFD4MyM9JnRqmsarH5WKqpmcbdkE9W0cnlarhUni8VNSFRB5aYe9yQ/RN8YyjMjUQ/IjUNU1matRnqHU/QlJshubEpNkc3UOGJ7yimprlFdWxX5J5sggRHozIzI1UapnZqNGozPUSyfgwlyOqyDZDdsdk4ZDxsqqmrY8tI7FXBV5ZNRGpSapqmqzUqMzJdkHA6vVF02R2ZrYX2N2wT1jmRqop8qW4vyI3H+Sx1szMln/SfZxyZuro9ME2ZezN1bHZNsSbL2T7Ijkzde+CbMvZMcW5eyerYk2Q3Prn2R2Zuro9ME2JEpcWpExxdEck3R2SvgQT174tSk2Q3NiRsro7J6uSJS49sYQZT/AIQQQbkEEYQQRhBBBthsbCUmyG5NsNhI2JNjY2NiDMlwTjJItzZGYzGYzXzbBPVk3x2T6IkhLkbtiBu1KTZDc3RHI6vXFs9WTfBNs2RHJmtjsm2DZDc3ZezN174JvgnGCerZsy9mbq3L2T1dEck3KmSUuPRCXJnugzdE3zjBNkE2ZeyerYJji6OyerkpNkNzfl7M3V+Ybm6LItjsmxUkpcDsSk2RNsExxfEcjqvVJKXF7qG2yCCcYJxi2CerEpNkNzZEmyG5tSNkTdl7M3V6UmyG5ulIbbIwnGPTFqUmyG5tiORu1KTZEzcqSUuPRljkdXodMci8dDH4UPwfZpmkzIzIzKyLYOLEiEuRubcvZPV0RyTclJshub1T2Zo49OVmoNJb0lPknkqaPsooUGXchGVD8dI/HSaFI/x0fror8Uci8Obgf47NCo0uxqoysjHL2T1dHZPVy3IS5HVN6pk2Q3PoSkhUmfFoQinyNGqzVRnVuRTJkT5K/E6d6Sjy/VWFS2HyeJJ8mlSaCH4F9H6w/wAZn67NFmkzTZDXBDuy9mbq+CEuR1T6VR2Ovq+LZMzMzJM7NRi8pWqat0U+R07GrLw8POEkmYkknB0pmSk06TRpP10frof44/FlNNGkzTZpsyMyshmXsnr0qmSVTwNz7aVuRN7xWxqVGqzVF5TVpNSkmlk9E4S5JJKnBmf1hX4uimp0lNSqIRkRWo4wopzGiaBoGgaLNI0zTYqYHJFraNiqkgajFFXJPxJM7M7NQ1TVF5EZ6TOiqhVDpdLKfInyb/Z5MPCNk2cYZqZgyLgyKDIjSNNGkaZOGfYlwNyQKmdylFZGEC3xj2xi/ROEY+OvKahqIz0jrkkVSKXIxvc2EoGQilQbEEbEIT+hiOB7MdI1BTxgoKikpoUFS3teMzZwr4+AqmajNVmqLyr7NRCqRmRKMuwxiX2OkppIwb6KqhPYaYqYZVSfWwlGxUiCDLsZNyqgRlFSOnClSyqbZ+W2NSU0kYyMSFTvBEGaBFe4qRclY3Dxe25IsI3PsgiEV84NQ4+d/8QAMBEAAgIABAYBAwMFAAMAAAAAAAECEQMSITEEEBMgQVEiFDAyBUBhFSNCUHFSYGL/2gAIAQIBAT8B/wDb26VkcWMtv9vfOWwtrZHCSd/7NuiM09jE2MTHUY0tzCn8NHbI8VVp7k8WMVbZjY2ZVhseM8n9wwsaPlkuIW0Rba/7HExMr12JYjw5vKPj9KkiUoS1ZHGUFZ85uzGxcSb+JGc8PYw5vF/tyRjdNrJ5MDC+VkZX+2Uv3TOKmpEZSxJmFJXlaMTDk9CGBJPVGLiLaI8KWa0Y2BkwtCOMyGdtZh8RCEbMLEU1cf2rt6GeUXoLF8eRfuMeUo6oxcPNG2jaRiOo3FmBjNLMyWOpQ0KS2W4llVMxbkS4etiEpJ3Q1ndSMTNGWXDH+pOKqjh8bFlJZtmX+xm6HLPH+TWyEMnyZGXj9s5I+oV6n5ak/kTTl+ZDCVaGKq2I8S1FZUYePdIlLUjxCk6JYuuVeTGhk1JQi1ZFSexgtN5J7mBhZvxexDDUdezqJ6fd4hV8kSlrSIYmR2fUJ7mBrqXrXcpq6+63RKfyyMWL0vyMSai8xh4jmyWmw1JK5bHU+OhlctiqeVEsFqNksSXkwsHPoY3CzzXDYXCSyXIUoRhRHDhjK1oT4bLG4anB5sP+20KSfOXE6EXb0E9BO+3z3TbfxZO0y9T82dSMVSMPTci77MTEpGFbnchO/ucTxGVVRPFtfEd+zLruRg0yMorQk44qVDwIslClRDLmqicqGsz0RBTujCj7OM4p/jEhhrEb1IzjhtQMHGhsTx4u4pkJLV3/AMMHiJTdNctTBh5MTGy6Iw8zVy7Yyt129WOY4hxv+TqbixKY8yI29CO2VMi/HOzEfy5YU9yE00KSe3PFnlWhHEm3qdRCkmTxkjq/Gx8Xi5iWJNyJfEcM2xWXQv2NyMFrydT0YUVujGwnGWdEVmZi/BWQxKamT42WZqA8WTfyKyfJbmXqO2NLcWHZwuGmrexBJLTlhuzpuRHDrdEcqWnZibCctxYlbmHiKRxGN0o2R41zTOs5n8lcszLyme1ocPV1fKMrJ4jjJkpZ3ZmaG2th4jicPxOX8kS45vYWNmWg8VtkKWpiySV2fIjaY5JxyimlKkdLN8iTtnTimNO9SZ1syqtRaaksTSjhpfI4hPNuTWRGJiyZGaapkklqzBxFB2xyw8VWhySSoaLlscLjfDK0Qba5KKWqFI6d62QioozW6XKT0JTVFkvZh47wziJvF1ZF3aRGLXNRzIbSI+xytnCInJeSGNUjGam9CvAkxmKjUyMhjNbGFLS2KTk8q5JLYSaLp2S1k2jDxGThTzJmG8piQbexKKT1JZlLQw7q2S+WjFBxfwFiuX5k3uzVMUddB4Tm6ROKwtB/FF6jaew34MKUbtnDW1fJajko6Dl6Yl8SCrk51oXqWTHF0SdIUVuRMpGDZFxjoyUdKRla2ZlowsXKY+M2RarQ/wAaRGNi9MempNDziloVa0G5NbmBLwMw46mbwSkZdNiSplEcsXY52rJxc9jpihS1Jwy6ojGTjmseJpRHE0qjDlm0kSUa+I8Wo0iUnLRbkYy8k8NRVijew8FogqdkcaTaiZ0S/g6cmRVOjDkktRSTHiIxpp6CWhQ0SiSqtBPQh7MKqstxMTXUjUtJEI6kpaZT8D8icKSoeWhaCjcRw8DXkTslGtS3dEonWjEXy1PJO71Ooqodt2Sh5I4aaMiehGyX8HRl7PmnRh/LdEko6CgqFBv8TpyqjpyWx0khxrYjgYknoiPC4z/xF+nY5H9PxvLMP9OknuLgfbPo/wD6HOC3JY0iK6mvkjh3qxYiSYpMXLY3JSRNaaEFLyJkZZTDd7ksTTKUJqtS0nZiSzMhC9iKaJRiJCboV7o3jqjKS9HSW7MzSok71MPG8UW1qYjVDSibtWSepmciKa3Iw8olhT9CwcX0fRYme2S4CT8n9KbduRD9OjFVmIcBhR2OhhR8CwV6oUIrZdjkVe/ZKCQ/kzChl+TJ48ojlZHkhsZQ3exOTS5PVCzLU15xw3I6arQgn6LKLI7kErJYnglUUfk7OnOfxojw02thfp87ujD4OaPo2/J/Tl5Z/T4eWL9PwRcPh+hYMPRXJs1YlzbS3LkxRrsbo1e/c9d+Tkxpco2WasiqJIsm2mRfsyMS1HHKSobsWjIKe6OjN60PAnWiI8FivcjwTTux8Mq1YuDgR4TDR9Ph+jJD0Zedlc7K987NWJc26Mzewo12N0asSrtv0U/Y0q1FLShlEWLU2MhVC+R9K3qPgsRkeBxRcDLyx/pye7F+nQ8sXB4S8H0+Gv8AEWHFeOyy29hQ991le+dldl+iuzM3+Io++x6Ft7CXbm9FXvz+mxBcJM+jl7Pov5I8DFeRcPFHQh6MsUf8K9/arld7GT33WVzvtv0V2Zr/ABMvvtzXsV77W6Kb3+3ZX3LvYy++6yudmpXPN6K99mb0Zb/LtzejL77W6NWJV9q/RX2q5ZvRl99lcr5LlZqVzsr32ORTe4lXZmKvfutvYS7s3op++d+vu5vRlvfsrlZqVyvlXNsq9+xySKb3EktuxujVldub0Zffc5FN78/+fas0LM3oq9+VlmhZZZZZZfKyzMa8tTUcqPkxRrY1NTUuj5MSaNSmUymWZW9ymUymUUPTdlNmRGUyoyrvrnXLN6Mt787K779Fc7NWJc263Lb2FFLsstvYS7W6KbK7szewo19u+yzK3uJVzrsrnfor3zs1K7Mzewo+e2/RXvtbo1YlXdm9GX392uWYyt7iVcrK7K52V77P+Fdma/xMvvtv0V77rb2FHucqMre/fZbexkXZXLMKLe4lW3Kyuyudle+y/RXZn9GW/wAu1sq9+7N6MvvubSNWJJd+b0ZffdYot7iSW3K+yyudlX2X6K99jkZW9+1ujVlV2uRV791lt7Cil3uVGVv8u6xRbEkiyyudle+dmpXO/RXvsckim9xJLbsbo1YlXa3RTe4l3Z//ABMvvvbS3NWJJd1NiSXKyud9lmpXOyvfY2kasSS7bb2Eu1ujViVdzkZW/wAvsZm/xFGtfsQxc2xLiJw3FxvsjxiOt/B9TA6sWdSJmRa5VzsrsbrctvYUUu272K991t7CXc5JGshJLbvcvCMt/l9nMjo1sRt6TRiYDX4kYNPbliL5MynyRmn7FjTR9RM+qmLjJC417Mhj3sS4jLufVxFxMTrp7ClHczovnm9Fe+7N6K99zdFt7Cil3uSRTluJVt9hyS3LlPY6S52PlLDTY8FHRY8ORryoy8lKmQx1LSRiYFaxGRbIbGPJxWh1pC4iR9S/IuLFxiFxcRcTE60TqxMye7LXdmv8TL5fe3RblsKKX2XiXpEWH5fffbRkRkRlR04nSQ8D0YbnHR7E8GM9T6WtbFoqOI2XNckac4zkjqT9nWmLiJC4qR9WxcWLHznVfo66OsjqxOpEzozIz3+Io+X9mWIkZXLcSrsvk5V23ylsN13rm0mdKJ0UPAHgM6EjpSR05ejK1zXNuhS0MxDH8SJQU0Sg4HUZ1JezDm2UYk3AXEs+qPqj6pH1KOujrI6qHiZiOVF9rx/A+IlujrOSVnUHiIw8TMZhyVin4HNbHjlmT1/Y5UdKJ0YnQifTn048Bo6ckODIYjgJxxEYnD1qjKYKGcT4LLZZm9mYszHUaOszrs+oYuIFxSFxB9R/I9WNULbk5a0Rm0QxWjqnW9DxG5DxtkRxbIzTE9jOhvS/2K70u3Fw859P/J0WdKRLCl6KkU0IpjQtdCuSiRVcktRrSyPovwRFd6lDMmo0VyvQzP2LE1snjeCGMPF8EZ+BSW/OxG3Ozd/t8iOlE6KOiPBfg6THFmVlMkrGJiqtCitRlXyoktBrQjFmUVifJS1M51JRFipLRCxNCUk2LEMwpFk3oRqv9BlMo4lJD5y0G9SMdLP5MxZ4GUPl/HJRMxfyFIvQb2J4jizNbIbDIu1fLyef3f8A/8QAQRAAAQMCAgYHBgQEBwADAQAAAQACESExAxIQEyIwQVEEIDJSYYGRI0BCYnGhU7HB4TNQotEUJGBjcoKSQ4Dwsv/aAAgBAQAGPwL/AO5s/wCtfDRkPFVP+rDuDKylSiP9U0KidFltUWUdXKpGjL/qaepPFAgrNNuCg8VKceC8EPHReSs1ZV66OUKOegu/1FCIUQjKBnRAKIN02khNaCjNNDa6Lq6IMLM3zCJIV5aoNP8AUdEZKB+6zAyFHBTmUytY0yiOHBA8FmQqiEQaFRKhXRdKyjslclDvhQVP9QWV0WytWW+aCvPBSxRYohTxWYHyRUj6rMp4o8QFevBVNCtkqHIaIWaf9QVThwWZRNE6CoRNwpLVQLaojzC2vhRA8kC1B0RKdN3c1lAlQWwjlRpVNnioIRQj+VSgTb+aSFQqAVlVRIRNQFMoCaKBZbO0HIcIRa2xW1ZbKDTxWUOoKhcJsjF7oRfio4rmFOIF4K9UHSqmQpmilNjj/JZUFRw0ZQV4fzGjoRJWc2WZu0EUQbKWozdbJqpnRmiEUHLarKJDlUpsU4SnbVYRmig+ujOF7SxWViyclHmjDlmaZhGf5JAU81KJVLqToj+XnDKe0VUE0RZzWcGQqoqp2VeVLSociHBFyqpKMBEuCIUppw+F9FllgwVBsg1SPooMQnNZaUaXCzd5W/kRGiZqvFbIQcg2VRZj/LDKuobwWtcj4o00VUqtlknQYQJsFSyIhAwrUQPNDN6ohossr7phHmqXlWoUIUOoUcQLMVHC6fnrVNDKBT/IrrtIVUBRKDS3RmIUNCt/KYlFQpWQLaqqrZfC2h5oKCu1o2zEKhR8VAXimiURNCpss00Chy7VUMx0TFkTaFtBSLlQOKBF4T3RAUTe6Zy3Eon3swFLlQKSpQrRQFZV0V/k2VEihR7yDohasFGX7S2lGiCVsmqqpJU3Cy5YRQUrNyXJZSi1ygOQe36QosVDxMrmRVZpugSMpUgpzXBSDtcijnKuFHFS1bSjrESssoBD3iFIV0aIKiqVQ0UuOi27upCM+9ByJc+ipwWUVWaylSHIVUwpVNAijleq+qvo2FmchlojxhChhGqupjaQhqY5wqaIjwlfRPqqdpDENCFrGmY5o6vZdyWfE7WjKoUuNVfTRSs0qVUaKe7ZgVlhZuCoFMaKqGhDZqFD7qlVJU7gAqZogAaFeKke8GFlKDVshZwqGqqsqzTVVsVMpoDTl5rPwHBUUlTKlBVFEY7IWZhqjFzcIAtUtWVEKtwVheKNVeqd6hMyNhHDI4rZoVm4o8FfZXzKSvFAjTMqiqtkLaChWU8PdIV1aVJVllhbIQMKQVIKBWcDRbcCqDQrqqDZQKnc30R1qlUKqoUqZWYWUt0QV9VdZSVF1EoclEhEKqhXVVldbmiDVThOvwXIhF11XRZTdbFCEwts1ZxSdBzKQFmOiVCEGRGiGiCoQHUqUCoaxVKzEraVNzG6rbTfRCrwUqiqrqcyhSSonrRoOaykLaUBbS8FCuoU9WqoqaNpTNFlGmAYUZllVbhEyhCkFfMjnClVOgGECRdZ1ZVCAHBB7eKGZZWq6MlRcLPNCs4RrVSKFBpFUCCpBR4FDLYqyInauCq+qLCbcVAqOazPQN0DMDRCwwR5rLfkpOmSoCMqQqqhqgd0HytlSUIVerOiignRdUGiFMqqqpBoozK/XBUHQICtpiVdXVVE6ArqlVy6mVoUrMrqSVRAkqiIKMomVC2VJQCtVS2iAmuiNGZUQqgZRdNkVlWZAxRFoNESnGVbRIMomKIQdB5aDm4oVorqnBZTZQp4qVPUKNVBKb4rZN0C506I3FUGwthhhXQI6lOpVSFZVCorqqqrKyyqpUIQFOiFB0TmVlHVqqKZUK6qVeVUqbrwUKNGs0U6lUTKlZQuS2kHsULKplQ0LaTpKGjMLKV46IbxTgUVklFsqykrLCjgjAoqXUK90WudULL8XNSFBClHOuZWyiJVVLe1NkFJOmFsq9VKlZTUqeGmOv8ARZYVAsuiUYKOiqjTXRlhTo+mi6BaZQJCohVDRIVboQVM6baL6OSqqGioqqQp0zply2T14cis0ockIVDCzNqszaEKCVF0aaAYWYWXNAjZIUC6krMVLeKIhSjWUZVE3mFQoNN1maq2UC6zKWqM2ys68Cg5tlFkCgW9oITVB3FEcUJKnQcx0FxRpKqFwlEcNErP1jBRzFZp0GApWXQROmqkHRtabKhlZlGihUFT1KhF6C2SoVVZSrIdSFKg6KlGCoWadEdaNAeswChZSF4Kgp4LZMKE06v6qWaNlZdE8FfQRCDgs0qt1eqklWR8VEqqkogC+gRwVCpJRkIMUngUWtUxKLFGiVmKz6aINRAVVm4KVRCUBwUdW6kFWMq2m6roMLaUqvUopK7KOcr2ak6M8rK1QtlV0GVEaLrMdOdS5SFsnrSFRS5U0SFXqU0FQoXgrLaQUTKpfQNWUFZUUqVCPNVKtdbSylFeCy4nGyOiVVUUKq2lmYjVZdHhyTYEIZeKzDQAD4o7SJmYUBRw0ToglXRDtMXKbIVtNNErMuzCstlquplXnTVQBpqolQLrKVdF7nTooFRTK2jozBU0XV1ZWWWNAVRRCCoFlMKgVdEOClq2tHgqLaM6KKuiihUVkEAoUBVXgrqBfRKi+iQoctlU0XWUohy2VzUBZpQBVlPAqboOiihCeCqj6ot8Fmcp4Ki26oFo0UQceKmEW2UIuKzKAZU6JJVFCixUmqt1TCqVzUAQqIQ1VWzojRRW0UCkhSFmKlqgK6osrlmWU2WypKoFZRoFVOioUqy8FKE6MyzBUVVTRaitoCop0UVVIVUaIoytqyMaCZVFOkmNMrNcIngplTKlSFAEqBYq9VBUKoUA0ULIgqaDK8eCyq2ib1W0iUaoMuiVmOgGVQqJ0VKngipUzVABQ1S5UVNBcoVCsxErZN1dWlRKovFQ5Eqqpo2ZWZZV4lExdTOjMAhNlAGmijQQsxFFClpQ0UUEQUYUuspVVfTReKjqZVCgabozdGKqCIKcB2tHirqpUBAaK9QNKyg0RE0VSpCaYVCi9SaIm40VCgqFdCURdUQVdBIXYUiiuF2kRmNVCssz3DDw+ZWTCZ/3N+pJUKUAtoKAoKtolwU6IGiOKtQKtEXN7SkuoolS1RokqFGiVYKqzyplSpcpaqhSQqhQ0KOpRQVSyy9TxVQohUVdAV1Cur6JCmUJUBQRohSCoddSFmJUBVssoUXWzRbWgFU4KDolV0SttU01KgcUWwpymFGX7q7VXEHoqvPosoDnSp6XT5AdpHICRwzKw3M2Au42XsxrH951vRZnuLj1aITpqoaVDgp0UCnQVEKc8KQZQ2aKCiAqCNFdBJVerKyqFDho8NEKqhWWVUUlbKzKmiqyrms0KFIVVAVdBk0Q00UHSFtaJ6kSpUys2iFdX0eCgAqjHHyX8Mqw9VOYKrvsokle0zfSao5WeplUaNxn6S7Us5HtHyWTojNUO+e0VJM7mGhfjP8A6Qto04AWHXgKqEKEaou4IwFCpouoaFJuosj7SVAsoXLRKiV4qWqCdFlB0VKhSpsg0DRtKmgRbRQqqhUqrKysqLwUuUlQLLMo0wsuio61dEq+nxUZTH0RICjioeoov4keS2nuK+L1XYVMNvordaXGAtgR48dzrMVwwsPvOUdFZX8V9/JZnOLjzO5ysBJXtXZ39xv6lZaNZ3W23NAvFVVAtookcVDdEqiFdEkyqBezTWtFUJYqUVCpzqlVyKr1KjRMaJ4dTKqFUVSpnRIuocrSraJjRtK6utnRJ0BUVVVUUrslTljRUhdpVM6KhUC7I9wkmAtkeZ3OcwzD77qBf5dutf8AiPFPILNiPLj47minpDsvyDtLJhDVM5C5+p3cgaSFRZVGmmiizSi4rZCzuRFldZgYUAq6k3VlQKiAnRdRCywoVAiqBVHUiFmss0q1VlcFAUwpRJVLLiVXDdH0VGqMvosrnM+gNlddpy4rsSqNXBcc/vE2HNbInxKkmdxsinFxsFs/5nE5/CP7qcR8+HAbrPjO1bfuVGA3J83xftu4Ale3xMp7oElURM30QqhE8VKqVRVV9Eq6liyhtUGmgVlEqoUtQMq1dF9HNGisswElVCmETClqrpgrZVGuUZHLsfdSXMatp6iSqtlfwwqNGiAJK9u6D3G3WXCGqZ4XPn1qe802j9lU7jLhsLltu1+L3W9keahxhnBjaDdZ3EMZ3iowGye+4fkFmcSTzO7z4ztW37nyWXAGrHP4jp5qQpN9FNElRKMGqqtswsrTVZyZCbRUCkqWgLMUAr6AgApKooJUwpXZPouwqBXAX8T7LtlXcV2V2QrdSnVgCSvbvy/IO0suC3VN8Lnz61PeKBd4/ZVPluMrGlx8F/mH53/hsP5latsYWF3GbqggcSbBbA1r+Zssz3Sd3mMNZ3nWXsBJ/EcPyCzOMnmdMnqTKmVXRRRCqhlMLnoNLKyoKLKQocVDWEqjYH1Vwoc4KS5VcdHZXYCsN5Tq0CnHfk+UdpZcBuqHP4j59anvFAqmTyCjhy3ENElZulvy/wC22rlq8Buow+Tbnz3UNEqvtX8hb1W0acGiw3eyPPktn2z/AOkf3UvdPVpohUVlBWVWXZVGq1VmeVdGXKRJU5FRoVlLjC2BHiq+5U604x1fhxWXAbq/m+JSerT3naPkFAoOQ3OfpT9S3l8R8lk6IzVDvfEVJ3MNEr2zszu41ZRDGd1u7hoJK9odY/utP5lQaM7rbderwquVSVxVl2QuyFbq0VdMuMLYEePudOtmx3apvLifJR0dmT5z2lJMnrV942j5LZpudZjuGDh83KOiMg/ivuszyXE8TuaKekOy/L8Sy4Q1TfC5893AU9IdB7g7X7LIwatnIcfqfc6KumXmFsCPFV9yp1s+M7VN8bnyUdHZl+d3aUuMnx9+lxhbIjc5zGHh991Ao6MzWP8AxHj8gs2I8uPjus+K7Vs8eKjo7cvzntfspO7z4ztWzxufosvR25PmPa/b3Oirp2zChgj3Oir1c+K4YTObv7KOjsr33XWZxJPM+/STAWwPM7mWiG8XGgC9mP8AEYnePZCnFeT4cBusxhjO85RgtzO77x+QWZ7i48zu8xhjBdzrKMBud3fcPyCzPcXO5n3KnU2jC2BHudOtnxCMJnNyjo7K9991me4uPjva7mm4mw5lbInxKkmTuIw2z+i2j/iMXkOyFtu2eDRQDdUFOJNlsjXP5ns/upe6f03eyPNU9u/+kf3UvdPIcBvZxXtwgbZuPVp1NowtgR7nRV6ud5GGzvOXsGZnd9/9lme4uPjvaqlNxTcfqqbR+yqdxlw2lxXt3a3E/DYaeZWSmHh9xlBuoaJW17V/IW9VtGnBotu4aCSvanO/uNP5lZeyzuNtvcxhjO86yjo7czvxHD8gsznEuPHTTqbZjwWyI9zoq9XO6MNnecvYs1ju+/8Ass2I4uO9qqU9wou8fsqncZWAuPIKelP2vwmXWrwgMHC7rf77qAJXtTmd3GrL2Wd1u7op6Q6PkHaWTDGqZyFz9TvYYJXDHxP6R/dS908hwHX2zHgoYMvudFXq5zDGd5y9k3Wu777eizYji476nuFF3j4Lw5biAJKzdLfq/kHaKydGZqGcx2j57ucZ0fKLrLhjVt8Lnz3mfFdq2ePH6BR0duT5z2v23uVoJKnHdmf+G39VkEMw+423Wots+QUNGX3Oir1c1Gs7zqBezbrn951vRTiOJ9/rXwCiw5bnWdJxBgs8e0fJZeiNGH85q4qS6T9VcK49V2m+q7Q9V22+q7Q9V2h6rtBdoLWYuxh8yF7LY+birq6urq6v9lx9Fx9FY+is70XZf6IxsgXL6BFmEzO4f/JFPJZnB5PMrsldly7Ll2CuwV2D6rsfddn7rsj1Vm+q+FfCmu6UQzDPK/otX0TNh953Eq6urq67RXaK2z5BQ0ZRua9Xl1quC7QXaCurqW0b3jRbHtn83DZ9FOJiSrq/2V/suPogADXwRa645Lj6KzvRWd6KzvRWd6Lsu9FljL4uRET9F2Sv4ZX8Mr+GfVfw/uux91Rg9U7OcruAFVwXwr4V8Ku30XaHou19l2/stvFM92EA0ZPobrtuXad6rtP9V2n/APpXd/6XH1VvuuytZiBmFhd56/ymEM/4rgvaOL/quy30Vh6Kw9FYeisPRWGm5WYmG8yVGHX5nf2VXOPmrlXKuVc9eGNlcMfE/pH91mxHTvc5hmHxc6yy9GGZ/wCK79AsziSeZ3FgrNXDRwXwq4V1Uq/2Xa+y7ZXbKuVMkfRXd6r4vVW+6o2VMKTdW0y0bPeNlT27+fwhS4z1ufuFfRchuJcYC2Bl8eO5zCjBd7qAL2Tdfid93ZHks2K8uO6oFT2rufw/upeZ3eVgJPgvbuzv/DZ+pWWjMPuNtvYY2Vw6Ri8vhH91OI76DgPdeXVpVV6uwKc+C/Hf/Sts05C2+5bitFTcSTAWyPM7mMNs8zwCr/mcXkOwP7r2jqcGiw3UNEraOsdyBp6qD2e6LbuizdKfk+QdorJgt1TPC5+p3uVoJKnpTpf+G2/msjYw8LuN91pu9hsraOufyHZUEw3ui3Wr7htUVNxNhzK2a+JUmu4y4bC4+C9u7W4n4bDTzKyUZh9xlBuoAXtjXuC/7LK0ZGchvNZiuGFh83cfosvRWZf9x3a/ZSTJ3lFrelP1TPufJavojNU3vfEfcOXVpu4Y2VtnWv7rbeqy9lndbbrVVKb+TQLYHmdzTaP2VTuA1oJJ4BT0t9fwmdpavCAwMLut4+e7zYzsg5cT5LLgjVjn8R3k9lgu42C9iNdid9wp5BZsRxcfHe5zDMPi91lHRW53/iOH5BZ8RxceZ96rTq5WNLivau1ju4z+6yjYZ3W9em/mw5rZE+JUk9egXeP2VdxAWfpb9UO78RRw+is1LefxHz3ed5DGcyvYNr33X/ZSTJ3cMbK2jr8TkOyPNbZoLNFhvYw2yqx0jG5fCF7R1OAFhv5jKzi42WTDw/8AEu4uNt1y6uVoLivbOzO7jP7rI2MNndb7vSqqevRVqeQXhy3Os6Q4YGH81z5LL0PDyf7jquWZxJPM7qbNFybL2Y1ju863oszySd3DRJX+Ydmf+G39VkbGHh91u9ysaSVPSny/8Jt1q2RhYXcbv8uG0le2Ouxe42w+qgnKzgxttzy6sASV7d9e4y6yYYGEzk33fvHc1PkFFhudY4jCwu+9R0Vmd/4uIPyCzYji53jutkL8V39K2j9BwG8zdJdk+X4ismA3VN/qPnvaLWdKfqmcviPktX0Rmqb3viO/holazpr8nyfEVqujN1GH4XO55dWAJK9u+D3G3WTCGqZ4XPn7tRd47na9FAoNzmAhnF7qBeyH+IxO87sjyWbFeXHdQ0Sts53d1v8AdRZvdFt5nxCMNnMqOjNj/cdf9lJMne53EYeH3nLL0RmZ34rx+QWZ7i48zv8AWYpGHhd5yydCZtfiuv5LM9xceZ3HLrT0h+T5R2llwG6pvP4j5+7UCrU+C8OW42jC2abmMNs+PAKv+ZxeXwD+69o6nBosN1QL2xr3Bf8AZZWjIzkP13k9lou42XshrH99wp6LM9xcfHe7DfNUjpGL/SP7qcR0+HAb/ZbTmoaB0jG/pCnFfPhwG45dacZ2rHLisvR26sd74lJ91otr0Ciw5biTRbNPHc5cNhcfBe2drsT8Nhp5lZaMw+4yg3ebGOQcuJ8lGCNWOfxbyGBfjYnh2Qts0Fmiw3uVjSSp6S7Pifhs/VZKYeH3G23+VjSVm6U7M/8ADbdatsYWF3G77NjO1TfG58lHR2Zfnd2lJMn3WgW2fJQNkbiTQc1sjzO5ysaXHwU9KftfhMv5rV4YGDhd1m7zvIYzmVGA2Pndf9lJMndw0SV7Z2Z/cb+qy0Zh9xu9oFrOlv1Y7vxFavozdSz+o+e/oFrelP1TPG5Rw+hs1Te/8RUmp3ufEIw2c3L/AC7K9911mcSTzPVqVT3Daoobs/nuJ4c1s18SpJncQBKz9LxNWO4KuK1fRmalnP4j57uey0XcbL2Q1ju84U9Fme4uPju4AWbpLsny/EVkwW6pnhc+e+1mKRhYfecsvQ2V/FdfyWZ7i48zv8x2GC7jZZeit1uJ+I63ks+I8uO9zGGM7zl7FuZ3ff8AoFmc4uPj1aqnuFStmnjue8fsqnc6zpDxgYfzXPksvRMPJ/uO7RWZxJPM7rZCp7Z/9P7rbP0HAbzWYrhhYfM8Vl6M3L/uHtfspJk73ZEN4k2UYYHSMXvHshZsV5dv4Y0le0Ovxu6LBbZhnBgtvvZjO7vOt6LM9xcfHrbPr16qlPcu8q7nWPIwsLvuUdFZmf8Aiv8A0CzYji48zusrASV7Q6x/daaeZWXss7rbbzN2WC7nWUYLdY/vut5BZnuLj473KxpKnGdrsTuNt5rKTkw+DG238NErWdNfHJguVqujt1OFyFz7hmY7MtlzT4SqsW1gn0VWFDFlsOMXqu0u0OtT3Ln4bqQIYLvdQBeybr8Tvu7I8lmxXlx3UASvbur3G3/ZZGDVs5N/XeQxq/HxP6R/dbZ+gFhvYaJWfpj8vyDtFavBGpwuQud/Ra3HcMLD8Vk6FhwfxHXWZ7i53M+4zhnKV+Hij7rV4+y5SrLJYeC/hrMzMD9VmzkKMzlna4R9UMzZbxhFuG0xwBqVtMI8lbRdXXaCnhuqrluYw2yqx0nE5DsD+69o6gs0WG7zY7sg5cT5LLgN1Y5/F67zKwEle2dnf+G39SslGYfcbbfa3pDhg4fM8Vk6Fh5f9x11mcSTzO/2RDeZUYY/xGNz+ELNiOnw9yJYwkKih4C2xmZ3lXbwkMplXV14aRJV1QKVVoPkv4bFXD+6pmHmqYuIEOjtc5+V0jgp1rJ5QqOYfNdmfo5Vwnrawn/+VVn2VgsTG1jGtw6mslcvNXV12h69bJhtLncgvbO1uJ+Gw08yslGYfcbQbvO8hjOZUYDY+d1/2Ukyd3RT0l2X5B2lkwhqmeFz577N2WcXGyjo7ddid91gs2K8uO/ysaSs3SnZ8T8NqyD2eF3W+5ZWNJKD+lGvcC1YoBYMV1JUFsqcNscwtZgH6tUEZX8lYrLIzTbSFZVC5KNHFXXaUzoMrZVVfRtNanZWRnGUws2DL+bXcUcmw8fCVq+kZmHvCyBZjuVMX+lXauH/AKX8MnzTWdJw8YNNKL/D4TdVhRNPi81Zfuv2V12h69abN7xsvZDO7vOFPRZnuLj47zPiHVs5n9Fl6O3L857X7KTvcrGkrbOvxe6LBbRhvBotv4aJWt6Y/Vt5cStV0NmqZ3uJUkyfcaLPi+zw+ZUYUDx4lENOVvWkFV2X81lxP/XUDY0baiVdUdp5q5V1dU0URlc1tAtVFnnKea1fSG3s/gpHtMLks2HE8lVU0TKdiP2i0UlVqpbRAGEHjEeCv43qFsvYVYH6OX8N/qqsf6LExnh7sRh7OWnmtvhYctF1dX3E9lvEleyGsd3nCnosz3Fx8d7DRJWbpb9r8Nt1q8MDBwu633DO/Yw+8Vk6IzO/8RyzYji4+5QxtOazPjExBzsFlwq+KzOMncAc1keJYeKgWQ0D6dS5XNCWLaEKjl4KqtCnNAU5jojRJCtoyuywUXYPtcPu8Qtd0V0O5LV4+w9SFYaMSOWiiCZXgqq6ppe2aFEZAfEqrfRRtBbOK5TrJ+oUyxVb91Orcq4bvRW+yrCw8UvZivfUNBpC2ifAcAuPou0Ffd6zpL9UzxuVk6GzVjvntFSTJ38Matr2+NyFgtt2z3Rb3LKxpJWs6Wf+gWrwgB8rVtGnLdSF2ypKjQNz2iouvoolXUygdGVohQbqqug3mi/COrxOfA/VavGbkxQtXjjPh81nwyIVHALFnEb2eadVQSCgsODwUSolQVUK1NFVOiQoQi2i8LNyVQFVrfRNwWPDWtMjwQnOXc5WziPC2cc+YX8Vh+q7OGfoV/BPkVXBxVUP9Ff7LguHqv3RyUaLkoswBnxBTWPH5LM/EzO+u/hglZ+mPr3BdavBGpwuQ9yos+JsM5lezgfMbohpgc9/Hu1Cr2W0Csr8P9lkeczeazYJzN7qoYdy0GFeapqZXgrqlVMaOyYRJN1UKRoiUAYkrMEIChQolWRV1bSOPNbInREqMrStrAb6IzgMCo37o4jJc0iC2aFVBa22ZSDmWWYPiFIbP0VWPVQ8L9lcei4L99HH0V/srhQCtb0g6rD8Vq+hMy/ObrM4knx9yhjVmfGJifYLLh1/JZnmfdiRw6uUFRmDvpvL6abTeS1mG4h4W2If+aMo5kFAdaigoiHBDbMDgozGSu1KEBcPVAgCNEBo+qEhUaV2VeFlLlUyqK6EXUH89HFSFMQrXRyrMIWU8eS4oUzKhy/Ki10ODuBss/R9vD44fEKW0csrqsUg+StK7MrsNI+i7I5q2VSCUXVohdTmKbiA27wWC5r5YRMQpa2VXDcrOV/srhcPVW+6sVx9FfcZWgklazpZj5Vq8IBvgFUw3luoKjzVtLMTgdziCLsOgYfxXJ05TQ1I0RxKjjx0lx7LepEKq8VOna4hB+FiAH6q4TjoCOiysqBclcqjnINzUWYtlUEeajKqn7L9kRibPim5XjzU5gs2eq7UIw7wWUuQJdQFXvokWQGrWy0KgRB48xZQUbKpaiHFqJaawtbgkMxefAo4PSGZX/ms+EaLLiUdo/RWauCrVPMVKb9UOWgYZecoFkNmKKlkaraj0XYEcF2YUSVTEUtxFR4PmrAquGF/DK7Ll8Sv9kGOxWtHivYMrxxCi3DfPMhVzbsn4kz61UCgBunForFlluVHcKHionN9FsgrbaYRJtw8dPimg/RYWJ5LEPimv5mNDeEVJ8E+B2UXcQOekNbcoYbOy3jzO6roKPUrvKjRbRQlVMqNVPmqscKKHgkoB2HXwXEc0RntaCv4rYRtH1WdwAamk35KXitl2o8YVEZAUGjvqhwCyYgnkeSjEBdh95Z8IrJjiRzQeCJXahcCUHBw+ic1rpTfqoi2jyWyVx5IwJW0IKykwOaAminmqKyOyoymbraEcVMwrqrWlScMeiGymwMzreCc4DtVQ27qA+VPBfw58lXCVWH1XxLtfZdoK7V++jaEKvFZ/ss4yMPOJKe2KEIYuXaNE0PpmVqyonhZVmWmKaM0Ug/kge8td3LhYjQey/N6oSKOofomYRgtaKhbPZzLYESM7vpyUj6oloo4onRncQx2Lz4NV3O+y7P3VLfyiiylxgcFINVmcZN58UJCuQiCMyLw7K8UFE1mI8Yp58lIIOWqqZa5vFf4jolGmuq/suTlzYpa+vJNcLoBgTs9yeSajIjR5KimRtVQDQ7yVAS5QWqCI8UAChWyjMI5rtz5KQZPNfxbIuzDKi7MQpBELZNjCB48UHSD5oVvVDaAgoSWkrhlsoBIqpexp4SrBB+xBQBjaPJER4rkpEngtrhwHFWFSqnxuiYWVosEIiTwRjkmZhx4LL9050CGhFvB6w+YqU8RVDKJDRQBbLJ4OAstmZeyiacpFYlB8tIcZqngGgMp7Zvw5LDjjRFnGZT3PcG5Yj6oY+LDu63vH+y9ptOdRHBB40TcsWg/VBxs49R0fCJ/kMabqnX/AF0XKjWeCzztc1kxRBWfDKyODc3zL+ygk+qBUX0eSq9ub6ogKOH1UkUtdbNJoFtEAoRiRFxKkYhQfn2PsVsdnmiJWVtS02UZb1RDifoo5otoYqmEcvspzSzkiHNhQ1zgpBjLeiDjPiq5gjVy2SgzZDZiEMh8UTG0toBCiwy3hyVa5a1QzTPIIzPaqqeapyosqdtVV/hUjsi6zGjVAKjnco5fJeUINc/6HxRcJ2kA8djinTSOCr2aQrHLMpvDPX6JoeNiZp8RTJGY1pZOeJlDID7MzmhPwjWHLAbHwytY6jGbSzvoOapRqb3TsHzWUVNtGX10BnFor1DuJyGOcbgBxyg8U5mHWEWngrdSdBO58D1IGjaWV20z8kHYfFavG9UDw5qE6BoryUgyVtuLfNSHuQnaj81/DbPNfwvOVGpIWXIQ7imtymfGqO1fhKcGOk3R+Fds1qm5pLlmBV7qi+ZcAVmBiBaVlz8OKoRHiocI+ujsBSADHE8E4zs2bIuu14QhtNVTJ8EBICGzLVylP+ynii9x4p/OIlS6YKzeCpYCPqokXnyVSgG1kKTSUXjgtkbN/NROU2WYOhv6puzekhEuIvxVDVEuJEcxwQk1ARpU1CzB1U15aSHtqCjjFpBHCe0UwGpaz0WI7GZHCPAInOI4u7qBbs4TaeKAgnbusTGB7BnyTsg2ZzAfojt5sTjCDXig2nJ3SMSmc7I57zUTBy08epTQDiAuaOCPLh9EC4SOKfDttwj6DrTogLMdM9Ty0DRdSNJVLHgpt4LLw5aDF9NFVW3VCqmZQlrc3NWKil1XEiPBUx/UKj5lSTspxzdlS0urxNQqbQ8Vm8kTOyeC8TVQA2h5qWyVFGm6iIQ9ENmeagTBNFld9ioInKqC6tHBcmgSUDJIV1NFSyk15qQ4BsqWFZvOERDXC67SaHT4p2TjyUONLQoBK9nwTZ7NQQmM52TmOtaqixNfqss8eXFHCA2Tdx5p4d2OACYHPAiqxco7bcqINHmniESMPMxrRVyxX02tlXz5dnL3fqmF3KFFwatPMJznCjqD66K9RpjKIjswnYnEEbOiQg4ceqBibMUkJ2EbE0HIrWOEsZ90XzMnTQZfcY030BvJS09SY6lfcbrtFbJIWW4lVfdFruN6KSPDyV48ZVw6t1T0WbDdFLI/KtqnJTMrj9Fm4XUclmEq3FbdlAbFVKvH0VaGyy2ITmuqPFRKM1CLZnivJSTX9ECIHMovdAjgsQ97khUtKAPJF4JuiT9aJjW1KidoVQk05wqpltkrI3bd+qLH14XUBjwQJumtyWrTiVrGw52JEjismJ2ZvdAOEllucItcKEjLHJZGYDMKKWk+qaDWSiwBB8WdDkcPHyljezSoKyOlxPEjisxs6hKEGedOKnFEthODjBu3qU0NI7VkcPCphg2HH3W24jqzbcxvTVXV9HjosUc1UCSPNeErbpyUfZZANq0gKOFlSmYyswPkhkHaRYdmi+yBAvVQaUR4m6LnSaIhxr8MpuUbUJvM8FkdHLwQqEW3RLZLhfxCGVybloYiqkyFniTFlMUhZrGImEyDfh4K/knNBiVNs3CVU22gjWS4WQAPaRzCpMQtue3Ujitn4aoNcBaIRy+AELBy4Li85dp6ceIThkHac3Kmu1YbzlcKV+qmwPBF8kkVP0THYwztdTLMZU/KWkUuU1kaz9UVEWUx4rKIlYpcyQ1s+KuXMPHSfCvu9+pdCaqh63h7tfTWQrtQhTTLxCoImspzmDxUwrWWT7qgCtUJoAtzUk2qswbeqMCT4ldmW8kABFaNXtiDl4ojDftCkJ8PPP6oAtlomqxM0r/9KL2mKxBWYR+6iIIV5gUVKVywmiKeK1jqx+SlVOysrfrKMmYU5e0YTnzRtoQ7oug5/wAZ4c06nHiszftdOIw5e42KByCgoYssrviC+XL90WjDgTCcankFnpnNYKkUM2TnuzbMZR+ibOBs2LuCbiETyHgjQBznAynbVMRs+ayZ+QTbia1RIJ2u0eYTC41ig0vd9Gpz5FOHVnRbdn3CPeSnHjReqPloH0Rilkz/AJIpiJ+iZ/yQ+qZVOTa8CpjgUwfVMoLofUL/AKlGnwheSKf9Qgr91Geaj5UfNBeaCxIptLD/AOacq1t+qdTinf8AFYX/AO4LDp8BTP8Akv8AuvMfkm/Up30TzxQ/5FCvxINBIGaywZrUr/oUP+v5lGa2ToERh0+6wB4uRHzacCRfEf8A/wAqgHZG8Gg6QjuTvBoG/On/xAArEAEAAgIBAwIGAwEBAQEAAAABABEhMUFRYXEQgSAwkaGx0cHh8PFQQGD/2gAIAQEAAT8hr/8AEVKlSpUqVKlSpXwV8mpX/wAVSpUqV/79fDUqV/8Apa+OpUqVK/8A0lf+5dMqRSTYh/8Ass7PLIAL2xRQGiRc2f8A9SBt1AFnoWBwksl18SxXWWYtRENp4h1JuXhx/wDqcRgh2jXDO4o75dIRFItKwKDBsuGVJmLiN3szDStNMuhojasnMHoQXnMK4/8A0VCFkpSYg6JGPVgcRRJTsiNKuGOzMZRNEzG9k9YXXDDC6wlWfRmHApiFGYZyKTednaO1v8kG53RapsqcQ6j/APHX/wDGIrmYLwSuwXLgyrUqazK1ZcxhM3TMRUvWzlMxBPknYDzMElOJlCUS0dDUWgCjrGO9DOQAahSSHTM5Sai0nCnrMz0kNXP/AJd5/wDHv0v5vZaNXEW7l8WEFF6EmUXzqBlmY3ZyQwJVyRcbF24jZtWqzUBqw1KoZsy+6wVaWI4duLhtXEUxtDve8kU0OhgE2v6RFW2hfaVA4JYORs/8t/8AVEbJEXW9LDNBOsM4OwRs6ggANAQV3HE33Myt/UzbBzUKuhx0RdXeTxK5uSKm6SzMOxlUvlSyRDyusJMgH0ik27InVtM5XNTLmwqJFKxBHU3/AOUtk5+pYxr1G/8A0VbsS7vLEJWuusxQLdYXRGHmhcqXNxG81HhzbhUbaZU9yDRS+EB8lTndzFCaNVLH4MkZFYa7QzeQb83pKhYWpkBnhFFK5dOb1FRpzBP/AB2IY5mALIXwWmZh9cB11mV/9Df/ALRzvIMqCZ3Du6RiHi2Y3QbjyeuILMKUyi+oBZmQeJnm9ZWA5UzCku+IXq5MLNUKJ5hGeBksE4WIRDpvrE4UenmWFFDE1GZxxRsteM5I+UVwswIwb7JMsjsgEkv/AMOlreIsMWDWL6JfEwMCQUY3KcxgEH/z7UGcHidofnN9oHtXb0jVWqdQjhJfUZJfOaFd1lRQsy/SEhsvqRfkVSTJpZAs4GCsOB5maBrMudjuLyXWEHCmZjZBMXCoQss44mSc8kbB5LHpABVWMws+xc55XIicGVz1kExFCnJEm4HT/wACxqVLIK7GNZwjO08S5nWZz6DdNzbMRPlD/wAzew7IvFMxsjUS2+iXhtH6TO3ZrmWxo4zFsughq99zATQcy/BngliEu6gaSyrItC2niDBcvrzD6AliJN7US0Z0y1vvBXE4ckbxXvHVWBmhGGUBS1Rw5I6IdoczIq4JmHtiysn3YEC1wqHNphgh/wCBTaoZZoiSo06hqByYjaiyoijF0mpmPMY/+UCOIFonAJXMBXzlzUoxByUvEEFliDZUGBSu3rHBan6RgYWypWCwsLXVxLKw94cWOIgDfQnIH4Q2KeeZfPQ1ia7DXpSpUgbgreH1gzcLIks5xruloR2JbRyKYXF8dYlSjriWIGmmE3mQgbOgh1girImIdFsZQb6/Iv8A+lmpEquTCYWHcHgcXE5LVMDZ5leTmYXyMLhVE0MJcv8A8cF9mFjdczt4w9hmIrgdVOs6WOwwgMA4g+riDx1jEHjIUWwlzBsiVU5saMETLqWSlRWUuzUJs0tkNTVGCmHIEfkevE3jZEQRseIqSpwN7JkVtqZYmTEVPEJiofCEma2sbJgBRK6y7UTe40mjTcqDuwYHrGCJj4yZaI/bsr1wfNv5bKwzKXtEyGOI62ibhpuEWGJj5WOVC942osToqMMTynyrlQ5II/8AqJLbG6OrNkXkdZaNbmDLkeYjsDUqaFmJWtzzCkbbhK1CGzvIFPDmaszhlwYOIVes5jlSqCHKZIAVgwh9qOUyOkDc2B9IWuPMzIhgi7Qi1g6KjR6RAZoUjgNqaliExXECmMcQoONQNdlcDDfK5DiDSOjUVBRJXOlSwt9Z9LgmC/gvwy7xcajhBmc1E5N+iNpQ+TpDXyhZMmheLFDIQRRS+8SqYldlo4YkIgW1gjEWu2JZdxNvkXKUgic0qWIwS/8A6RINJLVmQbQnWQtxOJeiX7x0TpjeoR+ktYksW4h1tEEEpNXmYeq6TVJTdM3lDoyzBe8MU7yGYvY6QaRw6lDbdYcqU6WPBNy+Nql6lUzXWZ7gdxcB4g54ydrwS1jRnDcqDdToQ5O8EhbD6HqRWN0Vio10aEjBWGYhQy6YeCC6gGBBC7PTBvEbK7itggC8pB6omai0LzAHfyaENfKXSU2ESzMtSurlqIsARL6okUW9J05fEKgUQ8K4MzhhxqjaJYal7t+QeoMCrp1QLE9B6gSZ6X/8yCdnSaxjEZBJlWRTbeSG8xbUpo5xadcMQHhm+iGIlnQuP9fQh2a5BF06VqWONnCG4nBR5JcNEQ29koi7cx6g4gzC9hPtD4Rxuk6Y7GbkW6xLCSpCbcFjUIUxDAw28zUrWB6lKuO6GVRPjZcQ6dmGbNwu0hhdA5iLnuouTTXeVAIy8ll5qGIj1yKhhku7M4sMdOojqGZkQa+NYNFwvVfKB2Zwik48PMbtvEK4UGKlnUWckCETkpe6hHvI2bx0gjEesoaMvEc9IPwr9AUZRqEsx6ylof1mGbNXAueI59V38K1LGxcsgmHrJTMs7fAPYHppeFDofWZ9VktODiLimDLYbgWOCYy2YgLSg6JqNZYquFzcKa0DiUzcHqnfcXzvrCOLmKC3EChauI0hEutl9kDLqGYN3NhcCbBOMHJySi3zFBONRsmWpxsXSSi6gkR573jnKcCQ7JTFkZi5bKOV1hTJSzItZmUM5uEa1pUT0bL1K2T8svY1dRRF8wA16WW7g0lfFoOpqacXNGdooyo2tcQ1jBsv4lqalxA2uc0rA3XPxNJWoBk2zCdZ1kdJUUrMSqVGVWsXw8QL8TpCYwCWiYMpRe8zOI0QYgRpguCr9fhpnz6H14JlhLHFM3KJZUoTZ7TFsGWxOJwYftzKAd+t+h7epdiu9zpZmC6mDxSMhBTGgxdzDkZciJZibjjmHDKqKSMhaDbmJmI9JXshAcjzEEbmXhccRrAzEA2haMJYpZXJEULNwZueYDY6IapHonHF3KCFhiViVdJFcVwSo2R5BwHScVx4hMeCIwacJAYsdxG4mbq+TiDZwYiezaQKNOe0qfHB1NouDtF47JpNMkBMBuKhg5l8YW5VfUZUPWYbBhEBri3BOy31J0BLXoHWYLU5gvpSHa1p1lBbHER53CTGvj0iOsSXSX2LVkEBt6wocoNl+m0lauYKQ+OZB6lIvPEfTbGDSpRMxzABnMs+BLLkuD3UaZwQLIpO2GviQGZuNc/RaIog5PTHRUxhQQSozQqltwzSSjiALO5UnCY2iDSpY/OJsSLhe4KpkYCKgdpenrlcsrcOJ0i4YrZ0lzUcbM35RDIuBW4Q8YgyvMHA2u4BIqkicQTmsLK2+IgOCLrupkwUiBkvEpKeYxcniEXW5rzECrQ5JQMHE64ZcjvpLWYxeg5vUvxolQUyNjFMQtEVxAxnJiXVbsgrFX1JytfiYxWLjUck3jSll4TMoxdCqmR64ScwHXCotc5hrvSAukAjXxm5ujEvRUVDmRd+NRJPUha6ZxgRHItytkrCpS6or2WHlxUq0jD4bgMCY8jEwqZhABzHRdAgTiw8GYw3E7TKFqbjazBHPp9HZTAsyJxFSliDyUbpd4jThFycJW0mqCdGmHC5jUEFgbbGG7UBLXpVINkw+gB2eJZ5CQgpGABqKg5mW3DHxwEZpXKVYwneJi4mFW8Q1yzSww2gwFSxEdQZVLAa3CpdzvRuYzRHB0iMGVxsiFub+DNoCCnE4jnjiW5TxHzFkrKhNDVnO4O5aimyJxC3Yl4HvAYcmo1DcpLrE0OdMe5Y8Ql6OGEt46Ro4KS4ETmIvy53DDFcXxiD3EFkyEw1UW71EIB5do2WSIthiZBsY5kE4t9PrFmIIJ1XcXED2jtN0fSbgqYXVmYMpZYhVLupVLUwcPbKM1LFyyj3m/U5elWOckcyvzaglVsmiMWWWUAMF+gvwQnM3DmGLlQtQrSely/kjgLWe/jLqgO4lsW7is6y3PDIu7lSMkv38Qhihk3nblNneJRA7EQrC2YqiAqZNzcMfadpTKD0bbKlahAx2yS6aiIYZWJWYaYoPeFOEUFNsvGgjmsJmkUTlfoXFC5fY5jjumLo59F2LzEr1nWDrFqYOkz1mZAm6h7iIku49IgAOJe5CZlvlU+qkgzYyZDA5JgDxodVRMGWZZlHiDm4l91CFkMi3b6gzWqScRDUtDaMuQ2cQxzoqLHJgcL3PfqH0yVmbUoTqXBDqYZDLY3cdUUNwcCGVw2wzik5jOdoOYHNDUIuSq4ncS95UhF3XRMtk7mWEusS1VHmXtxfEKMRxPIPRgDEOYqpCVzkxEhJJt9DB18OYe5uCkJm5+AuGJS45iuBQueZS1V2hXDRDCF9ZsG4tZYla+IyxEbnDEIedOsxAVxNlVkrtsRg5OIV1maW2phqKdCLFFquV4WweGbcpvDKdTXWCLzmKxGN7izBCXHEVmUhroS7HUAqOtFl3HxNjCQVK8kzqxUeXazBWDqOJnlJuBqWGvpCUg9AdJTFueMcRWLmNeUthmWLrKI3Kea6zIDkgasMtS0nzAOATFjnUbOF0yjUIDtwsCzzFd3d7loForCdNhxFd0dtIneEd5zpJhDlDWvZENUqZxJ1iTDXEqHHbrpENMxzK4ldCIQqkcWmuYG1EOuNGC80qwKDUxnNJaN4dwrvgEeSJOQRUAtBN3ChylEx1OY0RUnDhLJtbb2jU01RZLX6zx0gURfCaIQT0ak1HLwm30MDwPMuQw1KwyvpAeJlMbyq6fW5e0vqSEyWDpLQtCYFjrDKTLzGsq5b1ekaXjUdrcFQaXmLBTMpWFStjd6lDjmVJkqeKlJAGwWce8zShK7lE1huL75h0PUM9Ygo1AoxhcoaTOIqNqiaWa4hpcMe85FhMw01MUKriBUUMsNUsiWBpYmCS1cxxpqV1WMRiHtAr2jWCMHMlOiLpIm7vKpGFnW4Cal85RY3zPdUBg4iZzGBuMeMpkLzLu0RSlDGMXOSQqDuYRkdwJPPMvjaNTlHi5XcQ9crE/OGSzKcJFQYYRdYjEjk0xKHLwx+0npGXkJxyTVdku4Ks3VSoRe/ULjQmSUFSu4RZVTghsaIR7dEN/JFlnJzBUMjaTkzkQG2iKBycwKI1CAODVEwslrtMBKNSuIGVu1MDBtlKZkucpem4TnMrkMxY8RJVKQ5lLtR65cYIgFCOLDNEV6ExSPticCti7ROEscjERubpGSzHSaWFRThcsclVKxNzli3PxF0M00x5NQVAqRUsG43vjUO4AjY6ptn4jxoYYPJA1hiKdsuUqGxAhD4il1p1iKeEFQVQ+RELNS2WQ1VEsjJGQII2amGsBhYaYG9LrKVI11DcHYjGBG456zIJCseJaHGUPQ2hYl4ZgWzGgEvaF6dvMIAu5hnRGpKkjfvcZXp9YiVUx5cb9bi5ajx8IWaqZYomYGBiHVtH7tiCCmeYUtrZpV0zKnWrg0DRycSmES7g6EcwIy5gE7OYoK0cxJumAADRmEZDc5sFxcM81QUopTdl0iqYXBmDVRyRXytAflRmHSMoGlJlW0kOEG4e6TXidUXxLQtOpaYNRcdTZty0KK4rXVEHeZZ0pe6B6yKIzTbvKyhD09BJYsXEBcRzHUZojbB0hF+AiQyreZarx6Q/XcAJWpQrj1MwAdJkyjUrLrKppgySDUCMMDcBlbidMjzqyNFfE6WrbG1SxTag4JzuTDYTgZ2dF4RBoa6xOPnmUQswwOqqOVHEt66gvvUI9EBqrgRtjpLpsxGVE3nERRdcTAdGJ42QSHEW5gnCnKI5SqlSQvsWVuYQcytLCfL5croxtC1xNC54mCFCEiPdKc1UY9VA2cWHgye43aMMGzbXJK8JDNmCPTMOy31mcxXRvzLnAzkKpRm4mA2SqZwplXeSW4hkbEcwM8pfGE+gGVhZGVnu4RQ4NwY8iNRDMVLAqOl0XD2erlenCBpKYqaYaTYaOSCjTGZiEYcMuYBEN7EeDPFRVrZmXLhFTSB3gO1ljY8S/KiZk8oGhqdqZR0wQzdA2wpkZdQtyg8Q3GrnHK8Sr59ZbCxY7DDFwdqdQIu1hB2QdIAZO9QumygkM2SpmEQHVzF1RgiNnVsFRzC1sdI55GZexSYzKZUUtBLzKpLqZGwJoVmz0kzdJEEI3VlCHhUTpukXwmC+Y+G3pFTRPaRDkpC2itMUbp09WJlZ7gIlkO1QD4nhzbJUtrMoiodgsmMclLJS4N4jmX0oMsO+IrLDmX7yQA9UwUVKkgscuAcjEHM1bEWvc7nJ9SAEz1jDN9eJTC3IhAuqBVLOkKm2KlkxMfAuVdAhLeJA5dRbclYYiuzL5wi4uDiJ0XWJtBgib3magw4lMbKRQ6oxcKYbqgmNa9424Oy5dELbmRce0zVmM8BCyXe7c+lRF+OvtKZlDfK8HB6VKi9yyjimI4ZYEPBK/u5iHWzaCciGFUvPEa0EuKNMWTVEduhnd1BFI9ct6byROmKP02ziOMF1xKmypfVCyxxrtA4DMNsajnFSl0ROSIMvpLXsMRJLUysKwUbiDlL9LEUAxmpQGsbgTAwzYzE8kudWRuUKIlR6ax4QWyjpYQe1CpheOJcJEDisIiGFSdOY61xjHFysuJXXJEq5jLlWRbQdWIQTJhDym2HNZl+ojdVUwRLwCE9hKBMMdNBjXLfLEqquWIL/EoANiHbROsQwSeZITYYZ7xDZMXMQgYGSOc1G6OYW4YmXPEu+IzsivRW6hQGBHNFVxGN7TMawLjbm+ZXUa6WhWDKjP0wohZ60xef6iRbHJaE6Ae0r4rVeamtSwNbRoeWUK7dY+OXv9J3Yi/D1HEJ25KBxuVnEA6JCQtsgwbW3pAd1iIRimtRBqYldMQau8UPIjw1uYHBm99Zi7J1gYlqNbKZVJrtLVZ7TYrMd8kAZdVNrNTurAuzOnrh2K3DNGoQKAg6FZi0QefD6VpmSwHRmZpDbSmBlQQEejKFswTkscXeZQ41KiaqUDtNJtEajOQSsqVkdzSszKdRmsDUqpz1iHe4TzTzH7aVVoNGiGiYjQsXO4oyqri7WpRxKuzE1W/EouKH1AjaGE8JgOkyDCzgRIstaQQzEod41XObqU2Ywyg7spiEF7GYATxG71Go1fUe0YsJeMwmiftKahFdvSpUqBepWHTJ9hhxwVye9xEZCdrlfk3LIZ7H6iOvZMe5z7fWLGt0XgPjwxqVVYWuJlJJU4hDYGrFgL+kWWF6xtF+0pViyGhSpt33iop2XN+Exs97ptqswwAdo1RhAFF8xEJpIigGLCFGCpffmFk2QcYtXUnEFWsr6LmAhzMWtwQCkemkLNMRs6EoUwJazmpeNE4Z7zHeidMvU5ioNhWKm6JC+FhnA5S7dLnRbgCg3Ck8Q9CkQI1A0YxCUNkvRc3E0YZ1hmlbuCJLgrEpQcEB9GbvE8DNsiHDiAu1TM1UowWkE5iuFoiyUcVO0FFGse81iIhks7RX2X0gam0OWDw5JoDAlAPHpUr0VAgfkT4jp81n+k31+R95rvg2zxr037XEYOO0t+SXSuk2sXPr8E+1Cvd19/ktLPLK2/TBLmajd96XDQalADHUd6lio5yzfJyKo0rbpC2bmRxyEY5Iwtu5NirdS8wAaw2x3DMKXnNLlAhdGNTSSlsywByGZTgRA51PvQm6p7y/Zwl+jUOngl5Q0y1bBCbhlm8srYqoTMcLTAzQmhlW8EeaXMI5macukpE2wbZnaV7pU1XBhYaS69LFaPeJahnRG4TLdtKz85U8GL1lDbS9oRtEqpXvLlxIFMBLuKrEWZX3gGhZyZTOvSpUr0VA7ntLVwePir0NW6zHF/NfSKq1tevxV6Y2La/9I41P2T/HMY9d/kkdBWAh68i9uPeMAphX5QXHKEjkxkzO9dJRCXJyhFbJEiq3mNyKNTGxopYg6OSXywdpfOy9dypuB9LNRt3NWEfW6uptamuq4KLL0DKNZbs3iU/RGzAirmV62JaaCIhnCXtxWKpvGZpBcobKuIxOkTPmdODKXrTkMAobhLACkJqz3nbCOmYlGH8rpKjhFXVXYj6F7oH5+8wuV0ZMK2yW2HyiaylTkbtNZFXeXbKOsJwBNuhGnV0+AJX1lSpUqVB0yyzt9j4a9EQnYdvir0Nth5YI8m+19P3MiDq/IvGs9B5GOrB5YksKrrTwHyS3BayjGurz4DmCcLq+V/nT6xVK5Xl+UeUnpNW96I89JlcKhg2VMMcMoPXBK0QLilL4cnMy1Id6ko5TJP3zidanX/abn2XKqNmqgNmBp8EHZvoA+ODrMBsdIkaqEAycxMKjFME8XfWFnyZnlWxApXzCIQKajrL4LEe7gw4Bglco7ZI6uKI3OgiU3DoS62ulQTznrKqg8xRW/WE2a9iIFFI/lia/6MHp+0TtGBmoDLCb90vfwR6VOPvIqVKhGG2gn7llc5Xq/BXojqiuw+CpUqLUv4+RfUYNrgI8J1n/AC4nbNfb5FuRzWjy8Tgq5/qcoIELoH2+VQ094T+/aIPq3fwe8dLe0tfl1NgyDnwf4TLHQ7+5x7eiEdzUN1sTplMLqQN6HpBMNpRfzDOGWWiOCdEeBcQsAGIPDZgvRZKQ2uaxtg7XfFxpQd4O7SKCiURW5WDLARVPWIN1BIuIuukakAm5MOOHgi1yjCPCgKh92YCId6h0jeR8Tce4mHLPSdj/ADDiIQikU7J/YisEAg2XiwaDLAru+VfqWwE3t5vRUqVMHotttr8FeihHpx8h+QYqyX+CP5cyj0GhgPkE3HiHPq/9jUrwTWA9+vyrxAei8jNAvBHwcy1LUXo8dPl3yF2v7PYjhU/dfweXMTpfKlr6pzTUuBzMjSM6cxh0VDcCzdRbDz4iY5zHy3MRTvHkA4mV2YFSsRzjwppSpaL/AAnXzzLoqekW7BD1yF5jmm+fQp8/viZRDE1ZqHMXzAf0wWi9p9ToS0plOZUR5dJezB0gdJQS49XoMrNsGwgkbBFeDMwzeMy9uPeKBrh2gbVqq8yvWwj/AHTLvPxvT8VRa+SRpFif5o7wrh0NfICtbQFrA5ZbMh56RKFP7L5S/wDUrfD5cfPL2+sogK9B7HyrjzQZVg8niccdRx/h7S958HB4OPhLdkxtMa64isO5A1dHiIrKCGIFiHKmDnxI4+Zr2/WAgWaIZKfFQIOjHgo7VmQFe80Oh0MqUj94OHnNxV2rer6MbR6PSpUR5RXZAlSojyj2BCCMEQT+1MwdcKIdoGa2soa51u/bj3j4WcLyvfj2iqJa7Xfw+R+JS7z8WCPT8VSw6R6fr8gHAGPPn3v6hX8meevyAVQLAIq5HnwwS2fC8+9xFIirlXfyQ7U8EeCPn93RPpOEPnr7/LLPXSPFTtj/ABxAiotYh7fI4XXKvSbVdojcp22e8yXVAP1QBwlOJTtKRo3Uy195lnKEGfWUFI9OZpeQ3G1a2wjG0W6xKlSonuY9gSpUIjyj2BCO/wBLqP8AZM7WyvQGHuekxQppfagF6btX6iQpNrl+FHGY2ry+LUen5D0Tz8joLs3F0K6xv6/Jq/eyfBzDunaL9pxGG6SfJEqCwAdbDle3HvLcqlP5H6fLpAq8Sv8AU2v86/SMRvvf+R8kYL9EEte3rcq9yo9WNtfeZ5swgOkA4PpzNCv1ZY2rSvWVFIW6xKlSonuekXsEqVKj5EewIRXo94yp2zK9CKItKfX4Ue+rkX6j9rbVb8KNGWN7fG9P1+Qtd55z8jFSP3+koKq9efk3DLtf+kcAH2x/jmK3flfJLcEcDNzt4HMC+9q8f55iqUVcq5X5WWMB20/YuY6WdOZf50iq22r8oAEy7Qp6X0lSo1tL6fdnVZZRAvUo34PMIKJ6uWLbba+im0s6weipUR5RexKlSo+R0j2BD1YNx80q9r+AgT3QHxymoXl+w4jtb2lvwoIrtrp8QRTuYr4VenEt8hMN13nx1ji/kP6iqtyvL8iwou39RHCA+GvEczBI608B8pu4N4CIPo6f46xIg8lvy0vMSoR+zDv8dYuYNpb8vcBR6X0h1SiKG5fR7sDty+lXjmVFl28zQo9eY2ttrAim0t7CA9Undi7MEr0qKQ9gQA+BPdG9s/Cz6m58HM2K6a/YcRggcr4UEVfHxVEN+ehuJpg+KppbgiP7fIItXhCPMvs+x+4xaTr8i82m3R5MTWdbrzPMpgA/pr5Vu1HOEPLODB2B/MHVMwGjwOPlpC8Mq0eXidGH/XX8IewmNHgOPmAqi2V/ORp8DcSmIdXoobZbR7sObllQPMqL8TmUKo9eYqtt3KYptLOxAPVJ3ekte016VFNop7Er4HyRHqSvg9uBt+DmOP2q/EMFHn4j8SpTbXbmPE0+/wANSpbeiV6ndiuTb8eSMBtYCP3+cf2idsvyDLZ0jwW7JCsqOvvHX5VocBvBc+Pnl7fWUxQehHt8sa9cBc2Kbtj8HtCyoNYB+/f5r1w7xf2g1b/C/ZE29iZoRQl6FHVgNuX0BVArKZB2MsaYI9eY5eWVFIewJXqg7s6mDtKCVKikKe0r4HySnqfDaDwU9uscep4se0eaAfEjjP4irv4KlSgtB+Y9Py5+CpUqVK6FsV2+PWPeP/Df2nQ40aD5AhJ0EoZ/FL97oi7wUr55fKDKTiiczHkz7uiUvXij36+/y0aFsq33szr9e8cjXD/anzb3aZeA89I4RRkHqpox4Dj09pQKx3YE7suFqgV6E3PGZY1UB159UEU7SpUqJMbZnbB0IAa9VCKvaUHwPDKUwr4Po4ef3HFqeDDxHlxGj4Kih5jKr8FSpYbY9Ku/Mv4KlTROwirv4qjtC2LvfsPrMEtdDB8gwpMAZWB67Zn9riPjJvJ5Y5tyvPwv0+AFUE5i+Z+3HvL8iYfyP8JUr0qV8FTEq4oCbJy+4YT94F/nSNq3K8vyK+A6lYALZV8oc+7idjjw+7r7+leo4JZULZ0C+RiwpDtv6+qDzPYPRUqd0ehF2YO0CvSopFr2letRHd+Jl6vgZq9b/wBDHjRx0fEWOvfR4JXwqletSpUwdI9HrUqVK9EGsxtlSpUr0VA4Nzrbf4zDvoWv7lSpb0V5lPf0KWjL0gAx6/AgZIuFz9KXt8yrZZ/3vQ3Uk/46f8B6u87n15wwr7maNzwc/iUag1bL/XtN6ucyjjOx9f8AvvqlP9s/zc6X1cq5ffOlCTE3FVE5c4H2P5Y6U95H8w/3P3P9q/ct/wAv3L/2n7lv7Sf8ZOhDs5/z/wBR/un6n+dwFoy8MOjl4W/FoUpnYff/AFFxd+CD/snl+36nl+36if4fqH9rBzl8zEql2N/X1Ypd4gVr1AwZehHlUdCANEqVHyOkvsPvCkqYlnWNlG++Ir/Mn/Z9SqH9ZRKneET8lwHjlLWK6NB4J/qT/dTvPqn+aiNqqLpDvFlcj6keNXyn/UfBn5qyUaV+wEJCI1ejL/3k/wCyT/sk/wCQndfTOykZXk/8wnEnQn34nZ+tn+Vx4/zn+Yz/AKr9z/X+88P++ZpGXYy/B6Qt89IYo4U7vJZm/llvTDX+xP8App/u5331TtJ+ZqvBzDC98HsTqXXzD4gOdZ3/ACoDoQs6+kYEPdYP92isV3CX44e/2n3dEz/vT/vT/vT/AKEt6st6zPeZ9dRbK6Dy8ThIen+/wmeDwcHg4+a1UW1Q/cXL5h1+DzHS3tLZXxlf88v+5OZnEXAw6Kzzj/Ug+K9Amjl7Q4ax3Mdf6U5ceW86LLDM8KiUk7ijrqE8AoIos1XEBTFcs7KdolOhB0AN4B7wmvNY9jmWB9BwSpUqVA4I8mX2ifpKlelSoHl05int+ZUqVKlSvSu76NxhR4D4alegQ6q7vgjRVT6nvx7elfGCibw+qjhEfDXg5Tz2bR46fKstRlXAeXicCdVp/P2S7FGDoeDj5ZZKwAub9Dza/B7TUY1j/s+fm3X8l4P1F30eH3mDNgNOPAei30+RQCWu0ID0DDK9pfZOh6FD0Fyx1cOvMr/sIqVBwyTqvYhFelS/0tvA952W9j+5QaesQ9viUPMU40fEptEnR94AalfEH/Biuz8/IMaXWefHWPUx5P6iqtyvPx3EaQdjyM5YLse5CRo9B4j5Vv67Tgh9s8/p9ZRrQ1gHt8sLoWvEEVLkyexx7y2M+G1/NwstaAuVzmw9+5xKjC1hPfr8D8gYPQie56T2ISHojZj0g6w55WHVKCVMAZekXa0dD0SK9KtgbdB7x8JdseXmB0h1jHtK+DxKbM9CLcaJXxJxjvK+vxqFqr12+0a4Nd+fkak8IR1luhj6fuWIV3+QBdeIciu7Z/jiayev9D8pC0rwTcf3/u/zxHZPrfl5+Z9b53g5gNhc5F4hA5NrlfmBVC2CIGyD9uBax4Xn3+PaKq21evqqi8/K0Inuek6mHaAPVGzHUUd4ZXm4EmPTF7ehNlg6EAQr0uWvPtog4+58fMXggaxf2+KjZ7cxWsH3+NTuYrw6fGPI77/szvD3v6iqtyvx31GDa4CdG6z/AJcTtl+RqBsG5Txdxb9zoiv38fLl8rLqAVqybeL9pYcN5e5x7fMsyHQP3JpCHZfye8StfPzWF76AQeqfbEHaLyfO3xCg4IDT1QTgY7sOe3vA9cTlehFsU6EA0PUniIE4E+TB5jCbx579fixyx8H5+Ow7xT8ai1dRgjzB/jEyoLy/G1kxP1x/lyjtg0GA+QCQWuAOYfsuQ59rj3j2F4d/PCq25Xn5X3IV+OvtHGq6K/Ya/KOFJlXK/Lunf2Jxgef6nL2jZ7MPCfNul6ng8zsFw+88w+2DovAfPxcB0Y944b/49DRCWbS2mO7DnzMeuFyvQi7mnQ3ANPUbO32SfVfr+vCU98Nvy8/FTzFX46cZir8ai9By6nA36uvpHLs+GvRHQVnUfSPr+oRWuhg+SYtGn7DaEPQHO+OkXpe0tflNsdx0I4FZxfZy9/pO7yn5Y17YomzWc9vu0SvXg579ff5ohC4MwAc6MvueJTDgYfq8/PBpXpKNmfN9RNJvoB6AAss6wdWUXfPweQ6EXfh23BWpUr0A39MnNHne54jH3AnywqO8YPgR5mdpXxJ4z+Jl38eh0c8R0PJx/c2rrjj4wVQKvETmn3IopXQP9n5Pt1QPbrHSJ1Ffgitu5XymxZWV4P1OBX0x/LFBdDRjwHHywqi1hyrchz7PHvEInwpny/p81FQVhEzZF9mLSx4dvd4jYqqvX52VAwLVuQZ9jiMQ/wCUsW+vqMHL6k2m+kXsPvANJXpUYlJwZYTfvR7+kSjbf5nxFr9S1/Xxp4zG9vp8ekS/4zU3jg4MHyK7Eejf9RKwdrb7/JBRFsU+/wCoqoR4/pcp0nFejwcfKLtTwZnQXyYPP6Qe9HrGP37/AC96n3x3+DmBZvye0/6ihybXK/M3qVXPeM/uF/UI/gjVx2lvw18kFUZZXKt4D26xJ0BH7HEfsO0t+HQ9NhvpzHs/3gaegeliBleCDHaMy9uPeDVy2M+SNttr1+FG30l+MfGg89Ir4dPjVpGPO7Wn1hFa6GD5Fc/A5+ka4FevP1+SwojenkYtoLhiBI0ei8R8pCkVmzT5Pu/b6RWZvK+XPzCnHaND3jjH4h8cvf6RB1Z+aoqUbWjyxw6uS7emhjwHz6e1NrR5eIZQX1/5lynQMeA+OquOvj94Gm4Er1rg9mFvwfuOWzcsr349oqlFXa/DrcejHxqfpFPiV8SKhbHbWwPp4HyMS0DrvHi+Tf8AXyew5/8AMTgs7J/jiE7h0VP7+Vl1BKyZKX4/2qOelOa9+Pb5dyxl57Eeai4X1Hn2jp7IPAfNDLXSfXGteXEpKjrD7uvzwiB1UBuWDX7niVtDrCe/X5OL+YHwFcia/Aix6LsX8EQKTa5fWpUerE7cfG4l/j/QbnRj05f6jCnsG33+KvRMjuv9mPW3vfSKq1VeX5AxB0C47D62/c4n3G9eXn5f3g0+Dn2mVC/wDX5d4jITa5X5Y97YAzHP792+7RKr9gHv19/mvVcvSBrVk39nj3gVf8KZ8sL5X51euYcNsPwCXpjCs/piJFNrv5NzR6tT3KnwbZiKPL9hojtb2lvpUIHK2iL413dz89fiwTs+KvSmb8OYsU068vf5AGgOWCOov7H0/cvAXf5BhSdBAvKj7C4iG1YRnyw5bdvPyn2O0aHvHCHwZ45e/wBI8QeflkLCwJkshz7HHvLsTYdvN+nzS3BK/wD/AOA5nYEo37HEQIO0t+dl1awPH0REogHFGHhEyn1+ZoS2fiR7dZieyX/D3jBR5XpUCEILVEXTR1dzm216/FjaXdYPv8gG6CPF/JN/DXpa0a26COt+L+0atmtdvknWDT9lCnpjk/VE6XvIvyng6GV0HnpO2HsP5+yBG0NGPCcfL8RJ90HwOZ97OrxCBSZVyvzXrpOiHvHER/x8y0g4ODwf/ATifEH94xCqboR85K8N4eP2nfCMC9BBOBbQdYjge6Uraq9X4lBaAih+Tcr46TsCXfX4xYAse5dDX1lNbBoMB8n2Aont1j7Jzr8EVt/J8oolcGY66XbP8cSyKDJiH79/mAOG4qHvH2aPD/HMVvvOXzRyztCqnX8PKDUA6Afv55d6cYhK73lScA/7I/8AwOFE4NwK++MvvHkvimEZGgHviZbgBl9EFW3e8NL6sKdJKleigLcHWK4+7NrcvWV8Q4bektbx2Pkc1m2O226P3AK0dDXyT024Pqv1HHquGvBynmcGjwcfKPKTwTbXnu937fSLwP5ny2/Mz0croJ16Lgx738IGbw6LwHzR7U8EG9fM/wCiJx6Pyj88FUFZRUM3u+CPOLO546R8wbS3/wCC4oE5b0zHfwIv98cMBcrIQWir5l2W7dYXOCWdHM2gFUxlQfWZTPErXl1ymfZJlLqC8cLH4pb7wRP8GK6/acg+k/3Jx5fMrsvqMkt0wdtwp8hrdnob/qLVFB6c+esqV8aJNNug8seAP9hDx7EPEfKBdQVZizbxftFTgfJfw9vmEErpN6q5dfglLUOz7uvv80FUZZ9SEvgcxz0BzPx0j5b2lvz9ATeIJgQPLbGD1xwP/iNAHNRwZ3Cbx4eSVJuAbPMHGdzyR0UMCVG7pWYrG8mOdkY3O0CdoSoV55i5cxZYXeAhWXtLWA8InVvtLrd5uX9vCiu/WUFN74PeP2LMj+0H5lb37DP5jnlR5ZC/NHufxG0Gf4BHUeVC5pFOx94aUxTqmWlSvQUjf47TYqOyf44l5INYz9/LvBXv+OvtMql5vaa/LvESEyrlflo0FYCu8zIvbj3iEd8J9784Y0C6Me8FqHxfSOZ59Hx88OpekKw7jJ9ZiiWDF9f/AIbh9y0Bcsz7fslQDD4fmE2O4V2sfAHRl4pd+vaXWG8kGwjcXLzcsroiO6YPp3cdkOW0sK+1yrXCtEAHPpCjkxCzgpCjlAc1mMAY3YJcMAmVlAUYEprWDk3cMpnuXAAguhY+IuSDqPZ0gMOUOpU1WlygqkfeBcL5jQfigOre79wJ9laOpPKm+La1AQ2NPz7M6g+5Nh+E5R+78QfiecQbS+IrpKlSvQBxPa0PeOJ7Nnjl7/SJEHnL5joP9V8OZ2c7mXiEoirtd/NtTPxHRj5/rPMwJj0Y9vn5YDA5d5/El8DUxKEJtcv/AMIXQuFj8nI+CNSXrzBcDfVjnbLynmUJvAFZlWY+hG1jWOhlUTTKV4m+NmxVzL5l9ygRgrrAAUW6mRiAMjbL/NkPM2nBHMyaTLlHxqlXjEIwiQQpsXHdMdZnnd8Rjw5gbi4pMA2/UM2+6qfy0EznTDYsQ+pa6Qld/bhNXB3iKw8CXTh7R7nLo1KalTzdP4zVNd/pdYnL9i0Vx/r/AIgSjC9DbQ9RERfoBo8CqJ/sJ3H0Z2sE0D4ZXpUqV6tMR26D3jhj4M8cvf6RMg8xXx+3whXtiiBOuGZ+ek9tIK+Xn54K43LlBZcJFwtToPEdvPL/APFZj1LAS/WYuBJ/gDxFy25fWpXpk36d6W4ndxOUhpZpq4nVcduU+lC2J1wrzKg3Sm495baIyqeTBgGW47Bh72lZSPpy1aMdJklkyq/3AdhqBwxMqRa4j3gCMShHb+x1isJtzQ+nGdMvpDCaBJcYzMRAFVAqDarO0+7mSOOGVxqbBSdZSoHLKab7xVHVWOY+PdrKWMeiqVtruRijd6SjBtxAksfaIdTp/eBGSdd+ijme1pHKA+sPDv1YLz4xGC4GmvYDUH/smSqPOIK0H39KlelSvgGqMspzcf4BGvE3J+mMEJtfn3zvV4Ig6n/czTIaxD/4iiFoC2CAnJsfMqeTB/JNB+lr4RxKiytdKmemXZYJHYSO7LYQciFYS2naVPpC0JeNwPKEDwRbAEbynlggWBHKVSgyuOWJbPEbTQzKYdsDj03B5C5g58pXSJPaoL7CC/BiafDB9jx2QWnTUNh9XhOQW7mFZQxVzkGVQVU8bMlwGOW74ugOCOJxHrg7zfGuLjbEAM0SoJ2wP4TpAJ1YGNVo3Fg7Md/0iiDdiFCd7S65WKSX2FDvRCS7O5QepYvtP1OZcr/c7xSiNwJ7BHfT/PWaCff+Jxt5nDf1f3h1PuISDgfQREPbsIcHKYB4fzGd+5Y36a9FelelfBXpZKmECGxnUo30cr5fSvk18aFBWUPV/wBEVBTnMouJ/czK2/FeYsvv6KJd49St0SytikH6BSYS1ceotNbzDHUuiFUwbnflTn0ArMpPem8S4fc6VF46NFvR5Uv2HT37zGFMtsTXk29y/Jq4p5GBigw/RLFXDSgnK3/iKmFJTfQiZLxmLHvOIntBCVaJSpzM+RqoMOGXCHJHNjfbmLOQ6l+ReiwZ3OkAFBUrzodYFOnOoYPtiPDUe9OY1bK3ce4mKCsKDbG0QGXpLO80u4ZzSmehOSMAocsWQWXgRSurThB2o7Zjrj4ODBjqo6i92fgE/qW7+8U/4IUfuzsHtHYft6R4HlSiWABXgZRhDN7viOqLSeUYLe3JlSpT6V8NfIGorl4JiqM5hea314RUlvX5D6OoFRGXEjC5zLmkeEJ7oLvAwlSqIXKFTF5xcKjW50lrCBRfNS/oKjX2g+JZ8zN7hKXLpBplhhzUwSl9Ev8APDvA7Rc8Qw2XUQmVLKydZw50Tdqc1GoRxNfcjTcwdYK6ReFM6uIJQXzMBw7wox5woWAJuVSjGoEdTeZc0SyTFxETNVNPi9dwvcE3HGN8OZa6N4JSuOWGWtAdYWKVA56wOr74mWjBzc2Nh6TMIr7phOXMcwOomdEXWUuHbgI2h0ZrJDV8BqAT7KC5v5BvwdZ+wQTPXpQHl8w6ij7ysieyHdqFaigBFW6wry6oGukPbemGGYxvG4t6mAQKr4YWdSaIRht4mjNYvMsbGB6veKv6klJe54EG5U6Dz6NjhGVLSvRUqFsNAC1hGr3Xb5lIAYN8QXdB6VK+PpklAaC3iNUbcRMnJmVHEqmoy8YlW6Qb4plZlCUxEY7Cqp3rMdKrBdPMZHI9109o7qczUIEBlxqV5i0E5b4IQ54XAnozhN3d4I5WsQK6mwhapGJ1bMSwjjs4it6tm1tTmeupbKUu5yYmZRxbXqRbAXEzNOILfeaPazBXMts8JdzGHHMigxvWCMQGKnEo8BxeI2Jke6GWOqkZ/Xiufdhe0DVNzRAdFVEgG90zKb9EbtcjMwaxt1i0phuuZdCQBXQ263C6xZgyWxVZl4WvNyrQKx4jVVrpL7CuGBWCy64lkdrwQ6XucsyQR5qFKTuSrbuH3T+ZfBvrruHmWj+hzOcHeFlotcc4QCjF3uF7Y1A3Solmam0eDPvLvxJ07qnOWcXVwIA3KaMStVqOv5hwNR2kovkOYFbtXLmJvLslBFAKJjtLczKJB7S8T+DErZ+/HnL3nfSV6/eGzrkVK6SoSLHSsxYhLylxR19yeXpbvElfC9rdMSwNCivaWNWzR3Km23At8RddekZZuagGXQhX0jfD+4LaHfccMS7RMqNK9DiQMVpzE0dunmNAqhvxm5U1Q9/mKQMwfEs6l8CBdhymDYJ10JYVyG9qf7isu2JiB3komdr/AHpjyahV6AemY5YnUld7j1vE2xu6ZgK4GHWBmbDTBuuNRNHSTOWXCrMJTVEx8zMu3wTEuUYjxHo1mGMJ0jAD7k8+JtEZOnidCbe4V4ndx6+BxhB24uY6xpx7rRDux6RC/LrrqI2XgcS5eu7AqWU3OQMov4MYghS06YTEOgOY4YE8MJUrjjiYSg7w/CmKaMNuuQuUBZdNXZjlp6rk8wuoO8QYbRaKmPnmGwz78yrtRtqCsBvaY/Al+bhISwHVzDhgx8otBOPxLxWyYS7cDGOImFh0kVDGc9UFa+bjmDGjC306zh63SzTK+03jA+sSisVTrDJbW+yWCgpXiWthvklRkHA1uDWjTikFFRG4BugnSYt6suoJQ74QRZOIZdOHeciIW6MZ0zHjfeeT3i3UqXQnvF9oeSOTTC8qrx3h+lxuJRYQ06RU3T/LiCVnOcxDOJrNE5igeY0aU4bnVgDbJLLq3ov+IrqiYAIai3JJTwSkyv3Tw/uESswPSA348+jA0YE5Vv8AU2LNFP7iXSHcVaj6v4huWxovtLYkjfQ6fWoad0lQGLsO/YOr+IFh4hC36IBClen1OkptiUd4XzqUXuJ9Z0O4lQv3Rgj39Gdk90tlgjE6JvN4zfaWs7Ruu0w8+kjKtg9pbMRFVDGNdoLSWGVuGBf3lArPvDShzZMiqezKfIGXM8wtRwg2vmW6m5MwmpK+02yKqquPoE55YhmAeRXmDUAUNQU3FFWo+oQ4JMImWTx/mojrHscJKS30oaZqZUxCGllLByh0prEYwqj9Ud+SVJVHbzMhZp8pp9sK+kFR9M7wSyG14XKykbWVahXZxM2y4o9+IEWxw7zWkjuqcQMEBraq4Tice9Mc4NFdkWEe74l0t3O1jgGtTpEAJQ+ic+G+BAfHIH4/EBVjJeW4NhBnmiULy0Lqukffpa+sDdLp5ixVf5mcgtpkZfJ0VTBuCOgCjpKZVpxmZByWriZN3wgFzqavMXIw7gSo9CksN9Q6VB3WhYdEreb5Y1KBm233RYuIEqcoU9uZXCwKuWcENbvtUcFF7QhZxbySvbKFMA0rTj3xEtjrd/8AMd+JXIoI9g8A5hltiZdQtw83Yfpf7mYNiPNXMWMAtXwJiM1X5Xs+8Nh2cumPtUO4UFdjeY4xbRz/ALqC2GFeOfvDpicoatjpTh+8faYsluIBzK5z7TibJWOfMpj2+kOBmX5lkdIPWJ3VA9Vc3E1HiXmeLqfUg+qZZmN7g1jrOcQcwXhuA1fnUsPWFnmWc1IIHKowC6lvYlqzzzPKGtKJQK7gwq2ppEq3kEwcwVefXlEnC8MuaxKjTwmntGFGOmkEJi6YSixcAeNpOkPBDR1jTZ2bRsxqnpNsDnylAEx7jHnrE4PMWHXNFjMJugLZleuPbB5lHWaBnk4grxBkDDO4bmQ79cVF7uRXxGCoAdUKg1yBlem0doAPO6gIRyjlAR2+tS65MWyygAbQr0Q00b3Aun3DVwQ1OfeJKYe7zHmYIncAOG0Na7SjiBsqDSlcq4qCkCwadkwYcr4RQb+Bt6ErWjfJNwE0RzfwilE2UPtCq6V6yscS3ETR7zxNNcrlJcDPtdoAh653UbDiO7BAdXiA8VDCZTb/AObgDVYHY5mKo0p+JvSK4OGDxZKpBK0DN9Zr8kgI44nHTBIaygwA/gJb8Gc8Y/EfBmU2jv8ACe8RCtKndf6Jc4Qq+a/uCMj5X16Byy2TR7sdSrXbwEjU6LpFArnNQHTYHugfaB04Pc5jS410lldpelsRkjBixKVprmBGumosGZWLy6IynWNX9vQ6Ill2Y4hZluZuKPQCC6haC9y8ylu1WGyJwe6dTshpLuUmpU5RbJuVIA/aXbMLi0QILntF1lkUNVsjU4A95nrHtDGKp2lqDjqzOahYMhc3xEWzWPMXm7E1NoY1+8FwiroaYp8WC6VlZmhXEYT1Jc8MAhlUF6yi5xMC67yRaiX1ody1XUlFpc5zfvGwUq24Gam60i8tFeyusvzVN4fOBmza8QvC0w/glqXeGL8xs/eKpgshtr2J0EGisRcU9vFcQq9rAuEiWTaxhMusomkehHjJqOI1siagJHbqtQ5x3rcqp2tH1RKAY/UF94qMTGSA4z4xKyAYw+sEwSFl37RL4TmtfqBKWguoBVwJtzCKsjKE54JC+IAowbIQN394YSq7jHg5YDXdEF0AF6jCQ02v3iUAuLf3hh3IJzH5wD3IfMMOYHtgEwzfs26dJfPiHhd/aFS1HsnUlmwzLiBtPM14iABhnvGgzswdYmsIVWeJymjYptFii4NARjjCFSAUscbK+tfSFps9AmYAMRQ35PdhUKnExhT+YXwEvvqfyEvq16x7PNESraCNBeL6zF5bZoDMEqpO45fBL3jiL51NbLxLOXWYp19C1DNXCujUK6Iip3HpElqIA45V9o5HiLc7QFMrOYBdMefdI58yklZ2znhL3jgdoxuHOtF95Y4lvrGq8QvNxYbYthhgtJUweTmDnVY4lZGptnEpdOYrcxD6zZqqiCdUPSOBrEAwROmpZW/aW9RP0JyHFLLjqNj+EDOpfdMQVQzy/ucPL5amIFBEgG2YhobJS/YjW5RHZYX/ACRAwV0xiKeXaIKGxlsXntB7veAG6uWtukjeyzNJE9XvFe1Gceme0R1ZXokE3162E1ADBcYgtnZOwxelzaYSDq7MVuCeOrOyVVuiHE1wK959YYbnsFY5jpLMoYzzusFZ7S2cXKK41ZCeUiiwxll4aIGF/RzFrb3fxNU3p0iI0Ygw7znHiUiH1IC0WZ8eZnx0NToI4TfLBD+ZSrF3yTLvJqjpmWlqpjgJSm9AubYJdJgHtroe0sAW28RIilwWjrHZJNtv6YRaqxR+amyttqblRvKL6O0uPuZDrAWXx/UQpaqj1PHWMblp+AY2UV5Oabz0hfb9w+Yu4hR2dYdBF1Q92WuB4ADBbhcxYo2crfBy1MBr6HnP8R8Qgl0LMInGG7sVrntFh0WrZWX64geDkwGM4BVOtc/Soh1BIIWp8ttyjnpALgwd0NnkgAYZdo0wwJvEzXQj2Jv/AHWbDAdImu0rgK/LmGmKxHMOUHGIBvs/uOhg5/0eJYtruurgjtJM53EyHE2KPPMz50xRzHPUXVVeYt90Uassmg9Z367xsE+nvM3xL0zJBpq4NkrlxNjpHsqLeQeY0xVw0riIR0JuOZLBErt9o4LdwGDpCDK4gYbMx3NN1Uy33xGhpuodZ7RbmQl2NMu1dcVO9qYzn2zBGTmA1EUVcdKZdM2MuO0DYLZi4lGqi48MwxMDjczKhizmBYmRupeczsOYIYhyja12YhYKrnBcPppbNxFu5nSOLi5LNQ2lzhuo+PegOJhaA3ZyTdUhgYJWb4tPMCytaJlPaCxEsCS47VVm8ETbTONy4EsHJLZ9+4DZkHC47W9Df8xAHDTaUjRETmOvEM2RWnDQofaDFVVLOkNpWy0fRBosGAq4ld6THhSgQ/0wCc7gjLEP6/3aFYzj1OZrgiU26+0Va3viu8qKbgBhZeKr30IqywWD/Eu4Gx4aZlK6Os8oNi+XJImxAnBePErWKsildz7Q0KkFsacff2l3kGjI7eI6nlo5WBIzvsvTFPOr6i0vcGZnmFiiHTcqM0RJVrD28kPTtBWsRzq6pZKb0Nw0RVtSuRBvB46tY1HJcDvQc9NkPAba+k2PE4wiNFcxJQCi/cHHOfyGam9wpdXBWYvvCm4E6pVsx9IlneCk3C6gDeWYauVeftHtFM0y0xGS8xS6mDLWMfmIwNcXCneo+8wiXnneI3gTNUcKxCov1iKwQ7HoZrNXOJbpBGXHGusbrpGRdK4l59HLGJbqXWMSwUt9oGsahlxLd5dOrKzcXYc37ROrLXdP5lq2mMSNNkUgrmPoncl9sjmu8QiM+yJ7rBKkWyDKHYeHtfMxNgaC+fE9kKORqZAU2NJD4rvTBG4RyOu82EJ41KKrAKMrHoKrrqWARU11r8TszSepDY8LHib/ABdMY7DlL1G7avah8yeluGkiXVO7qUPQLz24lkWx4MMmhe3b/wBjNuxXUfuFmId8XzFIQ4Iw+Ze2iyOI5kBYOEMGI2bRYYDryuYSC+znc36UZWoqFBQMo/EwQoPWVrMUJTDGziUmtHQrv5itRYoHwO0zXknymfqCnDbyfWCfDDZN8cwmwMagvOA5mqU+H3z/ABEJsg22buXNWwVetd4wcSt74/5hMVNtp2yTPuIm3h/c50qF2l7RXGzgLx+MzLFac6FSj6Trg3LpItnEyhUlHip9bY0RZUGxpBVUDpxCU3WIcVjEuFMpVGa8RrXrVjKaZT2Ru4qsznme6FRRPSfbBl9YksYOJW3vF3doKqRcnaCi3i6me7iezxOO0yDM2YMoYTHuOk4nIrE5iG5yMyilbXSaGmKnmOOIc9jMO3Es4MQreZberlLzCusN4qu8/EF6sV5n5lugJ/EFqZ3UvGdTWsjLghQWMsiqDX7naFUWwb65XV8SjJE6Ky1NRZw3SLxLOwapuUbXWW9wvnYXTmaVAEzCxxclqxCxCyilg0Iav6jhPW5HX8Qz8lFUUQMYMZJdHBcAK0gZfchDYNMBKuHQNH1hpBWD1RZ4FCxmD6AaDBCKUFZdiXQQ2WC89ICFgNcPslEAam9n1hM1ml/MtwxsHX3j6KGx4f3DOks9n/YlTtz4gWoPY4lxxWU6EgbMcfeX702uQ/U4gC5rM7l0Cod1cxUXlOFP+yqmQyFJkVsBf/ER4A7WZfiH9ycS4Oyx5bxNEFKdEyIeZdjm6/dzXgGDNS41G9dS4xN6dKzU6swNW8PZwzAS40fZfeMg0TuKBiwCc6uGziW4wr9MT0WDjF2wV5qYO3XpcBmDyGov7sp5s4KK/iZ10mneE6w/yfxAcPHJy+J0GSW775lAOkpjlGHLAt7MQa4SjP2ll1LPEahlLRCsSkeILxxKbhqKV8cyqYVeZg/zKyTBVejA85g5YYfMGcYliU095VfqGoCp1ipahE246TohqaV1g1dzQy5hddiLD6I6uNY0g/aWXNPaXiKDZYvEfGWV3la1LsOY/owi4NMuYNY4xHFxwgOHP8RVRLROl4EI0SxzOsFotoqNKWrnurygGkg3lnKbSyvPdm3ze4KlHcmsL212i7ZunWFoCxeJndnF9iKlWP2MciLuv2nFxCs3JcxqxD7eVpar5+YCuHPczHAvUyo5Kw9psM4/UJlWafj0SvZKGJjTi6feY1YyH3jXJVbQgkVGSu6P3jhDbZcam3+8bu3V+k/M/Ezbdwu7s/1wZuf2h4agedwCgAVfiOzs9c4vJHGmeNHPiNycrCa5iGAK2mNFnA1iD2jcdcTExXH2JX3v5mjKzHIs3CWh0CfzmibRN7jG74mWUrfo6R3jvwnX0NHiE4hIH4Tn0sdYvQPqAYJoz8M3Tk9OjOU2hs8M0h58+iczRDbxNZw8eljknTx6NJxnWcZv5eh3P//aAAwDAQACAAMAAAAQ1xNZxN9xxxhM8wAAU885hBFM+86nFN5hM7HR1OOO+6yiCCCyjWrDPdhFP5xBaO2KS+MMIw1/+cOMQ2/LH/8Ad7Av3jDRPT8thjrnvuNPNPPPPOMPL+eIDPPPDV14z/8AP/333EEEc89/n/67Pwxz/wC++u48sIAQw88888888+8x88hblsMQx899ooc88/8A+4wwwR//APY/gA//AO+++yW888+yz/8A/wA8whDDDzvPXiYog9a4X388sEH+P/37744oIJb/AO+++e8888801/PNd/zhDxBNJfz3vNMRphpvc+awREyPPf8Afaqnvvvvvowz/wD/AP8A/XPtvvu7Xedby09+888//wC/lf8A6H0IQTK1QYsDZPXsMMNNzrX/AP8A/wDrDT//AP8A/XzzTirUkPc9/wD/AO9//wC000lHDzz3F9HyKIYX69aiIWbQ047Kpb77zywAFT3y2kVpVtE1nPn3133333kU0sMM8d7id8XCA7Nx66HeI+/8EMMKa7H233liQ1zCELaHep43HHH14ENv/wDv/wCwwh37dRPdesshxmqR0ZIU6RaDwmH4hb1/zy+4xz1snqFxH3Cw/wBanvfvLX3DDrg4YkMw5KnKzxLkTvBS14i0MrITfYi/P8zf788u3Hxowheu5KJ1HYV4IKFgf79AezXbeY/mrn6ruDXwPP0oAL6XSKKJT3SfSakYhys+MyHYKSk15P6/5eCuirmCDomabI31W6EI5Djmx6Zmlv8AKYk5V/ck32qPQ2Zjr4Q/+NFrGPp/md78ZyId6nOqtVSUzV9OmB7Uyih1Tvs/zpTynzY3IAtGkTI9Fyj5NP8AqqhaQmhqzuAVKheamCbOqXw5dfMtSLBx4H8bP2H7KtoabLRyCnDk1JrzbIjX5uIRvrneHno3Bqe8bSIm+2Wzbfh+k/5Jkb1+8X7uNCaXyxaFHLHrPww1YBLdgpOD4aLzSM+5jytJv/vI7UnMa0Qnu4dffvnzz+2egWBvDFZAiUZ7dFm7qlpWYLHBkMnNAvkv5rHojeVG3VGHAJTpzcZ9fX/7w6VwUcixXw++Jz355FPNIlRVeHQw6zD1rieC4KZF5swZC6/BRb7dccbffv8A/I6Pb7d8DpL9REMLIpMKbztyOwKqYv6K7l1Fwx63umsX/txcl132AG6EbbTv5/O5levl/wCxW4XC0zAjYOtvu7g8f2t2fGd640c/9Pvf/wDSPv7zQbVUtvruunOwzwD9s54hlQLY2TN0zT/vORXN4rep/vT013v66RffdQbnv/8A296PPffnI6/+88MZxdo9U9P+j6+9FqjC7AC9C37dxfnNJ63WM1/nlopz/wD3YEZ5/PlE8+/f7r0Au2GWuvHLrmMoB8104+jErGrIN+dw87zHN6/bs+jTLb69O51lltef6zzj+amD0rVt6EFLN0Xs/tbE4abMmEvMkYAdhoHGBPzE6EsMdVax8PC3PF5xxdMb1QMOfFB7vEOPcOXVy8Ue7S4qFKUZHbHivWvPb9dc93Ywpld5pzDKleuOVbaVB99/jZU9GHOXWtpz8omY0UvuA3PNL2jbX72pqsc8oIyNJhd2ndxBBF9r651pX/3PVlB18DjSjbE49M8EqG8Wzd9O7/NJNUnc958nUdhhNbzM99tdBM4ed/7n7sN8zthv2Wnp4slgEIOMMIH99l3Jt558V898878HZhFVTxd9995nE191/wCw33j2snDX3uHNNQTOGKvvKH+WPX53edTVbzPPJWgoUQXUHxJVcfej/dff9/2xSEehvJSB1cSULENJLJK760NL/wC333Al3z3i06EEEGX9Nz73/wBpQwjz/wC8+5UfGtmvjx+XHY30ZKBdJ/7/AAS7fz3Hb0MEEW9P88ElEzMNMEEX1ed2898MM3UR6Z7wzvOlbJ27/FSqGvbynRd/w0xl0g1zm833/MV41gJINNbJl/8A/wD/APseZXyo6b70sD0FEK5EbkPKxNYNFIbF9vIIA+uh7Lb77KYuMIIL522fvvz/AP7WS+KyK2+e4+DOladmBosv+A2oyRTGNDmCkwIg3KH0P7eBx3uf0tK62++4+/GY0kE8U3816g/P+uuJnGoVf1/pz1Xi9Q8/V1qGYErW1Rhy/ZgDZtRYL64phf8AtgunsvMN5vm+/wDZThpiiA36/wBP2BcKHrZL4rAyvhDOFJcaQViWIIc0cKMIJpuBxq0xM+N0TVX9AcTa2yCvc+GNeZ73nS4AlNF9pp3T+GL6FSo7ZdR9MAJcATa/E4YuUnJjcus/QkW8zN8HIpaFxPpUdBQeTAu4jPKc51P09UV81j9jRmxOTHPM+YsUTlLVkbSM2Jfws0lWTLGr1hyVCAS1oaI9psV0ruqMnuQfr2QB9R78a5R711u7Zl43/DZPGfpOgclfF8M4eVkY37dQqAScQoSjP/qbUIIlg8MJA5doY2xZDTAf8CuPLaY+JwT5igSbGdYA7zU4sGqFrI1hWWC+v3V4v107O3skeUVcU8JJRRws0r0cSmbx/8QAKREAAwACAgIBAgYDAQAAAAAAAAERITEQQSBRYTBxQIGRobHB0eHw8f/aAAgBAwEBPxB8XxhCE+jCEJ4whOZzCfUnE8KXml+nCecIQhOZxeEiEJ+DSuBuvoQhCEIT6sJxSEJ+GnOx3BtIvCeEIT68IQhPpwhCE80qNkbjG6dxYHc9Cd4RLLEreBnSGbZ9vJkIT6M+pCfVhCE4pomwy4Z0B28jiCpMmQ1qJOjxQSfWhCEJ4NeM/CwcskAtzRSxq1ga1XsSF4MpiNItoOW/ClJ+ASNCca/BUY+UTcZVvAkawJlJBFYKGV6vGUz2ZEzGhkgkeaLJpdE5ZCcTmczicpTLG8DXH4eFzAjZQqyDR5E02Kch44Eo2SommRhN2DaGbVRHfY3SE4gvpXj0EmiiL6PTza+hS8XiHVJ0EnMjSSSEE+hp9jXY68mTI16E0LCaNQbYtsipwS8BopRUPXn15L2Q0QeERt0fhRKkpRcUvFL52yJU8mH0X2Uab6FdhdC5F7ZExsNqDcFbY1JsR5DfYn2NP0KXfGKMJUvghFE/GYFYgsMmGyEfI/BMG+BqeFGNUicQ7goETAndnyN5EhNXAlI6JtMSpBuHuxq4YtiJMecPRSmOocsIbu+VHWvFbHIqZEEqCFGJEaKIg1cGBn1zRUSIch9yG8l3ULDJg8iRFvArobTHoSmRG8izAljIm2LDAnDDInWQEK2hOidDTowllNMnoS7IhlqY+HljGy0nCHDHDHGhfBQWpw/XNjFR+hKGwlR2i0dDYjoWiRoxK8ESyxjOy3YlcITSUY12dwecCcWRUJKDWaYaE29iK5FuDzktUGwb0bEWMo6IRtYEj4k5PZa+PgZkFg7EsjGyjaRKUqZaUEkyIqNn2H6EJoa9HyJTIlyMbxxmyXJkjIZkykXOBNQh4G49GLojoeBO7FlkUWWIWUZFmGJcIbEZEskHwxCFHkjlj3wmLORHRehjImIeMobPkWeE/fDdKVymyC+RSCoqGsiEUqHlSKC6j3kSucSIOCSHeBXs7FGzDHIUJ07TGvsZdIRMo+wv0V9FPuLgFJKBSMAMQkIboTzELhqjQl2UzSUSh6B5FeEklWN0LDwMWRt0QTE7GkV0JN5I6J2QZPYy2ZDsfuLjRaQ06Q+pDJpmNlp0adb8E7VeiF4ESkuSIsi1NoYzb4ZeJyvY6uBaFgwxtcXobnBidEQ6HkWBs0iXY/eP3nTGk0Jl0LoQyfYxrFG2+Em9GENt75Zgibs/wN28GC6MsbeT8ZBd2hKlyJrAlg8icUHsWdDKQ5yaGxYMtEuNja0QxRX2NOENOkJ2kPYG94GzsbctmHM9l9cpey+uUm8IiWxtvlJtxHzD9DHjrwTPRPkf7DHvhcyhPoVbwOY7nYtyLPZGS0xMwErwmMC8BJ7GU9IvpD6kNnZfbLdkLDLEMbDHhY4SKkN3ieyzXKYTS0PjeiJbH05SpKLaRYXgk3hEPkNeOuVwu7wSsclbLGDfAczgY0hofuLdjU2L6J7KS8bIJ+uGyiXoiBt8OEqYQ3eEKlofCTZhaG7zhsfReCjLT+TDCTxlZD6rHhROLoyNt5f0GuIls+PFN8N0nsvGiiIQP7HCVMIbvCVMLRffCTZhFb3z8j4eCaXBEi3fBdsDD0/nxTYInyP9hm3neMjxs+JCzjA3SF9ctkMc4GHBJswhtvhMypDdKJN6MIbvK7Mw14Narwj/ACA226/Bry9CQG74JN4RH9A3eOieK74I+HjHRPZfQxkMIbIWaHknsvHu8DnA3sSbMLY23wk2YQ23vhJvREtjd5TbZUtDd5bkXRljGr8GsujI23vic45w/kfXDya89H3D2VvL4nsvrwY6TiPhH0UJtss0KExjsaYoTsxIyhMxe7Gvk+4+4V5okg4+ye3DpEd7Oxwi4IeEjF+xq9l/5/4X0/cvp+5fQSNVqI6Aaeir0VeiPQk9CNokN/Ixu9lekUVxecjH6FZWV8JtvBKDdyxES2PglSJbG+cA+i5Sb0YXyNt75TNEfIMa8eCTeERsNePFoujLGNX4pN6Ev9IxqLQvo54PBfRETFY1QbbdfEmz4cJUiWy8qNnw5SbwjC+Rs+Um8IS7fyG0iwuHwlRTsPqseKZ6Jsz/AAN28lhcEOMY/VbGmxPtkrQ226+J7L65w2fDldmYckrhES2NvDDLwcYx8ILtgYY/28UrogG7UWF5My6PuXsbbdfkk3hH3r0V6XhfRD2Y0QbPfE9l9cybPhymeWQtFvMLY+i8FjcCVj/fxTvPRANt5fjjnD+RzjDya0R+e/2G7eanOI4Ux8L64g1WhmT4nss1z8izXKZ5Klobb3ziPh4MarwjqfzGby/BmhdGRs9+KdqvCJ/sHnxSbcRP9Yx4682PPR/mxtvL8EQQtZNgJmY7IWufkYa5TMqWhtvfK9zDwNyLoyxjV+CbBE2ZG7eLWXRljZuvyU5xHKmPm1oifOxu3jB6mTYGREtj9T78ZFS0b4Sb0YQ23vldmVLXg3QnyP8AYbt4JN4RH9A1468WaE2Z/gbbcXwY8vCP82Nt5fkldCTL9IxqLC+g3JMCWoQVTMOR8WfINekPtQ0dFahEhtvlM8lWg87JwxuI+QY3DxwyX1wJ4JXCI/oG7wteTdD15f7DWr82vOCGmHlXPwEvDQ4r+RdAwnkQYRw/QLqNDf0NKQS2hMJ6hp08lOHEIjR/4UhFEoho6Gy5TbwMfIp9P5H1wF4o2iPmn6GYdebtC68sY1f0G6Hayy+aG1NhFELsE7aE9xMUemVCUGlREMJoC2EohteB40g2DHa2HWXwmbX/AMxpPYPQD4JxOEiz/uPCYLzTNxHzT9DPJCEbwhCVOCeSIQXNEy0fOX7L9inKaRPaM8RmfZGlJ+48um4biyKhdTBaFasEtHIkJY0fFxP2Db3+w3a4YMfqUzTFUNXH8Z8R8QpVLxmCIQhCE5fk8GoGNWQhB45ngsuDUcKImKmBqOeCWLwmBZFsdthiR2JIn7QntHcfIPEbRM0KL3BJhvBLcRA3QcKgsoyUtMfoKKv0E2o7WhbBMTXwNWsMz9DeyDddD9TG6L98Ccx36K8XXWNRRiSZbcH7CyUfLMGQoahI2LOSqlJwi8peb4TLsWuiWJ9wv0On8EomTJR5Mi8MlmYzcWWhi58CN2KWhsoSxixlk9DayYo1SlF+w7h5TE7sd9jyZFeUj7R50c30U0o31BMtkJtMkYRsVWlbQ7/BXfE9lQqcISiMi8NCdJxRPZeCqILIxZGphFaGz2xqaH2XCGM8GPRbAlKJiGUYlaox2WPEQlwIeg0yyLCJjpOFBbPYPAiCUCvoStMT0XQjxaLr/vRgNdjYMa9iw0uyE78it3AwzXo3PYxaoleSWMDUY4UgkSpIWzvmcNk4JwvD42QQl4Si4Q0+P3IntDSwLnsDWt8DYJHOhE61oWoGSkMMaOxCmmiVUxCn0NaJIirFYBGWxOswxGFNKehS/sbQpQkJsCLwI+9GaGLYxEMI9DM6+IhC5LxnDVIJcbIQhCUnL8YIXkxTqZKcLFgbgmkHryZZSwNYg80Giv5foMFQlsPJwD6LimRtn/l/k3vzwkjIV+xLJDXA1x/9fGgn0N5ExEEuXy+VyxPiU7INctcf/8QAKREBAAICAQQABgMBAQEAAAAAAQARITFBECBRYXGBkaGxwTDR8OHxQP/aAAgBAgEBPxCUSiUSiUSiUSiUSiUSiUSiUSiUSiUSiUSiY63LmO3Esly/4WV/8ty+ly4PW+ty5cuXL6MuXLly+y+ly5cv+Q2UJtfwDLly5cuX33Lly+ldbly5fZcv/wCBa7TpVCFzfmX1nx/Adty5cuXLly5cuXLl91y5fbcuXLly5feAtiNKG6S3ZDGDEP8AgKnCJK/Y2+IEIaa1+Y/NlXmWTOv0lqcpcuX1GXLl/wAty/4K7KlSpUqVKldl9Xxfilpd6uGnkRpDP2r5yvi5dUVepRcMAnsgKqs5lHgef94gYjDmam6NfXUZN6JUqV1NfzsBUly5ffUr+OpUroVMNRQBcQ8OfF6qXB6eYBQ1KdcMtGsxEvIPiULkkNRkYl2OftB+pdRpo7jX8yyo2pimZRHBjSV1qV/8doK+ouFOzzKUDEBb9fmMsCS9i2UkC+UMdvqVUdQcreSDqsTNNDneLeZnmk8cywnfn3HDUsgLq+prpcuX/F5cNgcIWocxTRBuja9l/wAldq1BAsCYvhLojD+mHm5ItSu9MvRQb2ut/qAHxJYUPjK6VCVdcfuBl2wjqnD/AGSjvl4eaY76fWPgvO15P/JTLqWK1FMrffUQMwQD+UBRcHAomBxA6yqS/bviFbPSpUqV/AGTG8BzLdOx+0WnLEjcwWbuXIofeVEnDzAlZjAJz/mHhxs/qLa3lMTVa+EAGQY+soto5uK1dNVCt1GFX2qn38IUaV5viXFdSAG4YFrvcFsS16/iLxAHFnEFNLl6AQXRcNGxtlWyhfW4KVxGjEQdISpXbfS5cFm5/aIFd5atmVCA+fULQ6zCZ/8AsUpWYZmA/Abl6jXiUzRuAF8zF5UYhbm2GWKOGNlxV759TET9ZTAPvn4SymfB/UCdJSLZZSa9Qab4AJjxL6qRFizsvoNJFFHCCVQQxqILMSrTUwOQxoroFsOIt+Lg0Uk40x5iFKVKi+RBwpkDmXFOpjzLFF5BfFqD8zBGwdwfsjnlUCNjCPG5QByPMIKXccpGBvF/uNAG4wmCPYofUqStf3FARIazy5/mY63OLb8wxTHRhV5iChqW36zKB0ZXUDYYCw7gBFFaIVuXS1+YDtaSW3lbDW4lKTMDA5Ob9xxhUQ2GXKr5Jw5CjGUTOQGhi4RrJEHX4xr/AKp+4RJzjJ5cQRpY/QiS25TjUQ3h4lAGoUts12GlqCF/Emunxh5mj9Qbg2RlDL9QWPMIDiIOSbaAi0bP9mIXz49TkQbgWg4iGHMEGIS9JXQIgQ0tSvuzFJUOggkipuOWFbUYXZKJtcQVgM+ZwSskPFSkeYxUANI2iMCsKZVLRGxlh+eC0gnEtdzKKygKQHcsxxLpLQxyA5iDLMAs1A3NSzHECgOImgMBC5WCU4QRXETDU1CuDEIahl3F1GBQRaoiWJXdfGG9E4C2agyB8YDhUFsVUZMtahPAjsnHRc9EyWXh86P5QD76ErRtaPmRLomchsJLGEyKhfTF74lo+4P7MxeSXxSKsOIlVylpiCqCI8SlxBg1Fdwg8wdo6CGK04ijQzK8wmUFwVgaiLm0whuCEsuES3EwIVhF/P3EW5cXlTjhNibP8ymyzAdWIKuxqISZ9QUGxLtKUhligpmXgSmGXmOjBPZElkZAx7UrxzNJCamBRGhC2JxRzECt80pyMQA0iswl9vf6gVUxGSkyLzMYMu0S1jOUCaA7iEIzNVTCHOUlnUV4MQsEwaYYBkJQAwywrFdNxhHGBUEqIw2hluiNASrRA6jKwtVqABg4zA0mJcIXFbgWmrgIRl3F+SChLLQtfBijapliwr5kQUX1/wCSwIX5ww2vwgPKECMx7dVOMwiDRUVh+BBmGFW5YfGU5EVVsIUxdMItMQLalz0wDa1+JWlqDCzUR5pVIg/EmpDSQlK5gy5Bh9qWW/KgEswEvAhDWtQWDcOiy4sARd3bNftmUQQA3KFVTKWmCMoG4kaazCr8f7iiajxcpaBH7XT/ALFCSPwjN2ijy+c4oH3msIdQujLL/pgV1RzmBsqIlajiOoFSVTEAMEq73A0EKOYY3M8jACKXggAIMJuBTJLopiN2TUxyNoQz80a2JBDe42NR1XiEYahLGRvE4EMIqPUzx38IWj60/uMKgfOaaIU/pl+x+n9QTaL84NsuwjdPpAmjoBuX6IBrqbanBwfeFr2DhzK8AgAUdtLO0BcXKFLiMbuBbYQ7EMcmZ4IazKLYJxMcIiWMQRY+CRVrEYcTFEqpRmpjX5huinqNvkit1PnL0H0i6ZPpHat9rAdXAeMCwD6Q+T4Qxg6ek9urwJl1INy9GIBDoAtnD0eX9Q1e3z2DtL9B94Gnbd/fjpNozFbdQGiCOY63cxSyGzRLOCmRgqlxBogXj6xVVfeAfhIQyM8++cMYE0w+hDGsQLlBEdDAzlLiyl3ADXT0mXU8JZ3ArXRQLZZgI3z1UC2cV84N3ky+qBaz0H+8QTPPai6yZ/y8dXwRBmj5w0ohwftiV2h1ZYBqDUIBxgYvglS66al+JXmMOhfMvpuA3n0WpSwA10eBLO5VdEalLuAGuucHNz2OoX+IXbd/jswblv2wzvJ7Rw5noPX/AGABR3EDrZ1PfpXmKEywKlyr30+Erz0v5fxC+c/x0UNzLADojUs7gBrogmW8QBrq2xGecuxN1ky2S+XEAMHWo2xlMs5/jtAWz5Z94Onbcx1xBMV5lyrmplgBL8Sr303qe3Rs1lBO9+uIYihuZfUAdEEpdwBglxBuZeoA11rozLvYMaMs5/HggCjsQNGWX2/KGMHS+igWz+4gje3ubYz/AB01x9zKK8wYe5cyypcC9zUvxA89MsZMttgBgihuWuoA6IJS9QBro03MuoA6iNGWWgAYOuM58T0x45glDsHCVswQAUdrbGf4hleT3ANbZ/QkKMEuXFXvrcMwqXKvc10XyZTzE6yZ5PyggURJM9QRKRJMvUAQMSS7ohjNNxXiW8RpipnshYUEvw6Klsv1n3jcU+X7z5PvPk+8Vs/mYPE0lf75yvM/3zntns+09n2irobfhHcQ8k9k9kv5l/MobgZd0feAalfM+N9eyqBMdAcyiUcEpySiIuhbLbfkf7MMFEuWdQpnoobmWAEWXLMHJzGXEG58ggGulwRanpjzGL57EBbPQe4JnntHacnBABR0uX0UC2cHjzAVuXsWX0vpc+MPCDepXmKxq0ZYbH5EAUdLXU8npqWuoAz1z8pl0XEG5a1iAMwlxQLZwPzYI2y9t3H18QzvJ7QFsvRg+8HTubtG2F23f4j1vtuV0M6hAhEXRlh4H0f3AFB0y1Pbra6hyY9PEzLvUoZZawAzz2cQv8Qu27/Ha8cpntf47VDLP7mANuXuJVtnwPwQAKOj0eiAtnqzzPc9fhPaXGjXM2moAodPSZb62up7dU6Nyz1OJZgO3L2OVG2XyV+uO0Royy+z5QAwdrbGf4hyy7jbZ8s+8No63L6t2s/xC7eb1+ErzLiDE8IPvBK6PSVe+vpPaX0SY5ltoAYOuX+VDnl2CNGWcnjwQAKOwdpWzBACjtAaMsv+nj/s1rtQFs+F+WZDb57zVbZsrHiABR1uXEEyDj8zWxBM9Szvq+Ey6kGJS3iAMHXPGUz8vx2YjnxPTHiCUOwNpfoPvB07Rj0BACiX0vq2aF/iGdu3vMtT5Z94bR3HqE1kuNnEL7gV0eBKXcrog3MvUAa6pujLLPY3s+Wfea3sUC2f2EEztl9gC2XowfeHp3GNGWbK+UAMHcoZY4v1Q1bL/ABzpjFSzCqKhhmEmlhuMOFg+knulr6gDqkxzLO4AFHUBanpjz/yZzntv+3iGd5PSpXRQLZ/cMEzt7tiyt2D7wSh3jexg8svXH8L54tXKH6yP3kQJanEFZi1xDgfvKuUQu4BzA3P7g//AGIcn2jHMi6fzDmi/wD06Dfs2+4LpIB5ly48MpnnP8d2XnDO8u4Baz155mY589+5npD7wBQ/gJjQwJ7ZiVCk0jqXxnBjThgi0iDZNGpSW3UcRbjcK1sX8KKASmaYAVzAeYP/ADDXp8ZRgnK/EV4+sT/6QaNWIfhnH/YcT3XVC/fEDex7wFrPWnmanfW+l9VAtjKGbaw7bYw9KlRLuemU8T0RZupnWo7DdFxjGGGD8EIEXxeZniAwq1MhcCkMoURVmlZRmAOftOaE8D7wHz9on+Jc3cCxFTSfeD8QaDcwXmCcxurL8Qb2suXLly5fXAmWC7dEE0diAuXAQeel9TJg2XEiSUMwRLihvpcvNQjtjiOoJkinEXgumcBnglzUdzDhVFrcF1E3TMLRMXHFy20Aa3K37kzz6xrOoA4YQUFvMRBCeJ94IzmGeX7Q5kh5CDf+w8HTbAwQ5rzK8Ms63EC0UUS8jIkTVwnwhFfEAuJjPrEwozPmDgwTUEeBLh0uXMRcQcd2J6lRTZF81F+J4ojhhjlzMAS5QQJdSuxiecniXLrIKpiPj0Kj5papgupclKijxE7lashuXAnEKssCNEasn3jsCy43K/8AiDAzCj5FzJEVCCDCMQZcTZ/mYQzo/ZDweZb3h/2JaBgCYxf/AJuIKShQJNwbLmYPS4kvoGeimoTmLMN9B6NEM7lEAyQb3L4Y3GCC2qniRXxAuJhsJNVHeJnrEU+EsbqVFoOrgPiVi1OR0pTGfRCmW4QFLfMIgYUyxTzEUZvdQwuFhRGmG5h2xqJhieFf5gtZy0S2wwbDzf2igHMuOo0KI7MwLUQJdRo2xPg89BuZiQHnpWYlyuzRLjHrXWripqPFPEz1ZYtSueHPXDwxBVyzYRrpgwQJcQRRgEsldWI5J4yxHqICC3LaYyxFuU3jiCAeZoF4mS8L9Jk4r/uWXZSwwLK1CrTBSzopdb/uVUJbuDLly+vP8F32PVlyiV23K1EwKuJBIAr3FQuVimAFxqBC/wAcSisJdsIO5dhYaQJWDNEKuoLFWfKANuVf+fqKFg3KI3B7cRKp/swdWpYL8/i+k+kEhjoXfTfTnpffXV6muvHWp//EACoQAQACAgICAQQCAwEBAQEAAAEAESExQVFhcYEQkaGxIMEw0fDh8UBQ/9oACAEBAAE/ECKlSpUqVKlSpUqVKlSpUqVKlSpUqVKlSpUqVKlSpUqVKlSpUplSpUqVKlSpUqVKlSpUqVKlSpUqVKlSpUqVKlv8YAVKlfRUqVKlSpUr6lSpUqVKlSpUqVKlQJUqV/EKQJUqVKlSpUqVKlSpUqVKlSpUqVKlSpUqVKlSpUqVKlSpUqVKlSpUqVKlSpUqVKlSpUqVKlSpX0VKlSv4CpUqVKlSpUqVKlSpUr6V9KlSpUqVK+lfSpUqVKlSpUqVKlSpUqVKlSpUqVKlSpUqVKlSpUqVKlSpUqVKlSpUqVKlfSpUqVKlSpUqVKlSpUqVKlSpUqVK+ipRKlQJT/ECKlSvpUqVK/hUr6VKlSpUr6VK+lfSv8FSpUqV9K/jUr6VKlSv4VD+FfSvpX0r+dSpUr+FSpUqVKlSpX1qVKlSmVKlfRUxMTH8KlfSpX8a/jX/AOCpX8K/x1KlfwV7VWJmpimNxEXscJyRCWZHX+U+lf8A76/ifwuX9KlSpUqV/hv/ACX/APuvOseFKrpM09y0TRV8QiAuv6Y9aOM8Qxjj+F/4T6H8KlfWpX/6K/hUplSpUr/8J/8AuvDQ2ziR9PSt9xTnqJf8Lj+LlGEaJ1+YRPe3UDmqFPXiMapeHs/yX9AgfSv8tf8A4KlMqVKlf51+jf8A+G/8F/4b+i0XAtphDdRbyGjsmXNvRzKmLLRsrEvEAlni9poYnkK0+5RDmZ1QNMAtGGKK/uX+hpNkrC5PHiNUoNGj6iDVturl5qVSlC6nCL/GQ+p/+qmVMS/4VK/y1MzP+G5cuX/hv/KZrDk8RJRACvHqHlhriaMJeQ57TWgOCl+JUKCtYPNwUbQpbZXrSoXv7RU9kdhvM6fbXIxHNVuRlyOEsf0w2WEBz8wiHA1w8Ixi1EqLdPhuNj3JyOamUasXinkiFbGi9DKq3xLHXtAeITChzXV/xuXL+l/Q/wD4NSv/AMS/S5cuWSyL9blyyWS/ouXLly5cv+N/S/44deLN3sQ8XH6qW9Qw9nkcnLCLQYgoEx2zE2qJjD4gn2lhfsy5RUDYeo9R4i9ag1C4Qd+W4oLs6LXWcNRcavYcvwQwUeur6hde2F45uUCEG6a1iajVi1+Y7cnC8XlJfXR/pYYEHO6ArJHlwU5MsMOBojXEQqaDSS5cuXLl/wAT/wDfUaA7lf57iy5f+C5cuXLly5cuXLly0v6L+l5ly/43Llm3BDCt7Ea/U3JuPUwXOhgfmMpyIvJ5hKYGGTR4jNBNGazoI6/iuz8SvqGfjqBJZty3UK4llazzAK3if+Rb4TV3xEchug6HxEzVZLH2SqGBBf3U3Oja5ifgOVupRwFFmQ6qAVmG1cscDRb+CSwEUoZtzLhXQEdU7w2QcGK8fS5cuXL/AIEIf/tsuUr7/wA1/wA7ly5cuXLly5cv/Ff0tly/4XLl/RWWBsmW9a6kzBPLzLjkqvRMvbk3Tc2Amdlx4ae6f9mZy5XAkw/3gt26xC8jLLAzSELK8vBL1w6q34TDY2E18RPmKuNuIJ3J4z7lTWSVujpY5vD0HVQYqCnldLKQF0Rs+YOdk3lTpIcNqi5x3DHLeO7OmX7CMEvUHh7l/wA7l/Q1D/8AbcJW8m4oV3amMzgIobllXBeP5XLl/wAbly5cuXLly/pcv/Ff8bl/W5cuXL+g6GCIToZOvBULdK5dzPpVZ+ls53WhRbUFEDsTvuCzrVnnrEEUr4Q44iDFK0OPfEaYBrk13FU8zYrVvKEXAMDyTVysVR1KrqUQwaA843K64rYXrRMoztSn/UcyEWzalIjMmhdKQQNJT36YAmdhNMAkIo1rPFRFJKN8OypVTihsWOsHUeutgvMUYcH8rly5cLg//svWJkD6ROWplOpdoUE5iqWr0QtTAYXWXh44YxIqy5cuLLly5cuXLly5cv8AzX/+RgNAypjWBrYDxBexxcN9wyg+Ey34iDOaspll0Ya5QtF7staG4rq0RMvaQBrVawDAwwwmnxcdiyo1XLDkl4UwvvDOSBtAGzj09yzStm9PnMuMHQw7L8QegW7Al3iUwvSlxEOSg2MpyDQHCGii2Q4SkDPP9S+XsDwfEaQrILzWoKxlGW/vBMh51XjEQCEiL3yQZmCp2eIg75TTuoDeHfhjCstly4ECEP8A9NkURzAB/AXFzsETD+5v4VBwxruKBIqZevccYAB4IEMUYlhcuXLly5f+a5f+S5f1uXLly5cuXLlzQQYXuOrEbWNS29L3vI8x1gtFi6lJDClxO0hEzfOYVMXY0HiOI8D1fEV3jkc43iF1FhOV94NKFPI85qZWGy3fDBpRog5ur4nIAB1GcgLLRlFgVRWVwRlry/3ALSzpK4XzCpPU2KN3KUg4dD5GGM4VwTqDaUoqOogEX7L7omQE+T0lvQgQ864mWFsDs3liqgYjiLzmYEigzd9iwsJYBxcxcFaNtxqlXEdRZNy5f0HEH/8AVuOINHcUysr7TKzirphGwUiGplQAIVRDQclRmznoYAApYOK7JzoJaoxgS/8ALf8AkuXLly5cuXLly5cuXLly5cIFb15hQ4PMppJZmoYZbE8f7lzvbdPMx86zeVd41AeVuT7CMhskFMeiKVYuOD7xkAJ9nmPrYUbCclwUzkuQOcQSzzHAvARiCGWi4XbM1sePcAh4xhTiVK2WAz9pYgzWIWnuCmarWYYGmR1dxTnErLHdR8LUsug3CBVNX0dYnnisuzqM9DIHQ74mfigcMPJWp99Sm2AF44uID4AAntldDGS8NlRUVMpkKYlp7WGveIluhSPjr3EAM1t3/Ah/+vPsPcfRWy+YpG7aUzmV4tgTz6hPUdW/MODmlZhiByiZ/wDYn8uUb0IN39pUBzr19b+ty5f0v/Hf0uXLly5cuXLly5cuXLly5cuMlbHEIoauvMGnOAtTW0WEavN5riCFzBqyC1VWrq+IuUZVt8TEODDqOXQY8u5c6wAr6RxgS0Cs+IH+4huXkw8mnoHmCCocdoJJGXXqEgz7wetwRa1ydpe3msNKHcRoXySw1lgcsyXinpirOQH/AJ3PExDn3KAMaRpHDqA8gWmDaXL/ADXwncWKZHtfNxk1UOEYVUaWjK8Yl554QWQmM4CKw6shOXqhVo5iOxbY4zolAAbOeLG3qWssAoEHUVIXFKwjBAFO38Rly4Rcv+V/xuXL+l/yv6PTJzLruNJea8wlWWNPuXti0HJ3GHKKvhZZQDGKesRr4Q0Fm/UV2mVcf+wWFa0DZziXFgIg3N6ly/8ABcFA8y5f0uXLly5cuXLl/S5cuXLly5cuX9Li0MyQDiGDMcDUo/OJvde43rh8bj15l5EtKoQN9YhKdkA8R5yRBUVMgi+dscCpmSGGzdua8wvVASG0ZZbn/cq3kQ1juYfhzOuNS9Blp5mGxUrhqGjoafyTm9E7qLETeyPiFRiwDFvMJtZnDnXuZiEJ0mByweIEKyRV7L3fEJXHNopZScrXku9BEAVCZZvmZiRK2S8MDsKFOr8wVItejGcwXaYI4eRjk1gBM+yXRYm/Y3SlcSw6QCOCvHmElWcS63D63BjD0FsbZitPxG/kvP8AC5cuX9Lly5cQGYMuX9Lly5cuXHRdxLHNkodwV5Hh7l61xWa6njoaiYQA3/8AYshC21GHKghv5lBIq3t3GhzeOPUSMjgga+YkHcZly5cuXLly5cQSx3wfMsIVLly5cuXLly5cuXLly5cuXL/wdjUci0wzaQoTY9sviMka+8ydAA5r4mBVb1XdN71KEzLB84zCQLpeyngiEAfODUtjtNsrObvzTl8zCt0PCXgV4TZv4m3UxtTM44wiiuZUhWc4MyzOKgz/AMw+cm1q+CIrFZTV+bhgWgOA/M0qKI7dQhi0Do8QKuJRxS+pcFJabV7qDBAtlYqJeUjv8Kw3coG61LjDJqOI14YrNup9wwswYpMEayClAlcy1viWw5xRBiiIEt+INTzBguCKhVdN01FY1Xg2i1zvD3D02ax6ly5cMGYLChAld8t40dTNEBhpzGNmguXDLVQLCXLly/ofS49orEuXLly5cuXLhMMBGsdZ3DtsBV8RpHIm8R+yGbOYjcltJaXcrmCjf2DklrbPF3niDo0zk6yzMJdXCbcdYH7xgDTTuVaDLly5cuXLm0u/MmY5tYl8PxMNDgBKGLly5cuXLly5cuXLl/4bly5a0FKccQ0/FhbQcFSwIXFnGsQdSXPLzUfeFYm5QUEVP3MJjp0YKivAkZHdKZ/5mg62mn7S8Ym6ae4sFg/dgWQmcj71LxNWxn0RbqJQBd+epaCDsv5nUNDWJlKL2uO5tArA7PMa+4hHUUtOL0RUzhehP6iA5QuXJ8zIW6rQlOHQGGBeF3XTnCEtIAW1kMjPGEOFqmErkoVlOSNfiIuW85ihSoP0+JYoE07z+4+EsgyGyXurCUzuobPKsCjkzAVX4nJA4rFwfeYwabxqIXko1WSXqIAKFofMsh+K6vmMTZouEi9y5qPAZoeZlQGK6go81GhBvMYtgbz9L/hcuHax4epcv+Fy/ogLWiGIR1FS0jKwS758QVdhpyryRHsIGMQZMTiz9QjzCXdfeDuyzI1ccWLzj4lrYttL8JxEdI5gAz5QzT6Zk4Vg/wBwAhS4PpcuXLlxYpVUZ8zJE4LYusXXEw0wCunkZ5fB+fUMli0fa7jg9JiAdS5cuXLly/rcuXL+l/S5f0WtwYHyqxOYbuwU6OaYJqOUW6zz3GtqJkQvfBxBgoNHnj8zl0LQfcWpTlTh9sKPIvM16iXL6c4fmVOAzsaZn4sg0nuG+Lw+y5kHmB8rcUdNwlIFYX9wKgDs0kcpD0R5Sxz0+JicU4xfdEWeUs/8QI65FHHqE3/vMXluEwCzsj2RYyfJjmXFh5HHuYiRoa8spAKYMpcrnQK8a8xWp25tL5IGvBGAp1LzTHDh6itKrHA3SrzBmsSwpHLEZLYCt8jA4Kyg0+yKo1uHF6ZSUBQjuWssEWxjMgwdLeTMxC7d0HkjkQdHLDl0rPYwUDgKghbtbn3spYp0BVcsfjzZ1KLcQeyIymojIl5YFQWvMCA6/lcYLg7VNlkOjr/hvi6hsNt4uNOO6hvOrfK/MQuSxH/VRdnNXXyxON8LPzMtS8AZrxC9HA+qhgVls59QBZeF7ZxoAnaXDgF5TbaoYAF12uozY6ly5cuU+YswsLq/OIvGhb37lg4OAu2FchN2fmXrEscqhEs5P2idFD9vpcDq3/ECrgITgFzOXCh5YFFlprj3PIsuaG0uXLjCgdsNaFOo2Ae4R53HBOWISgLb/EaVBcpsOWWnHWFpPEJpRwIpVmPn5hkbGRVJf9wUQOEajWuKXrqL1KWNX6zLRwXZtDcvBIsd2PWYRKoAu2/c3vHFcPRKAxZFYe5XEWj14l7A6iyZ5vCj0u2MzvAEVloFLZ5Yp5Axh5oiJAqR57alnNJWazGcRMdFQrHxHBvJxqyECmmZz5I1kU1FoeSKHZadnTFF5BeDVViNRlWrpJnTexOpkqwByVeYQ19dYHsSK+SxYzMrhirj0XlB4YFq5rc1yRFoQtp3UoeAt2fa5e2QCOhWKjwi2J0/jcKhQsux3FLFfQWgVpfcU0NmYNS2ImAikIqXNBTA9S1MrszUeXoGYqBwBKztLly5cuUrmScpyyNTIeEQavMRn7V/G4R3mOg9ps+D5jrTSJn5Dg1LiZMnXqV5FKqFXGMA5DESFbjAhVTZhC0lSKxqgpqbmTkXV6hUhyJUFUt2ZrPxDaqxjuGHLL6X9avNMp/DFbTCmIpCgNeXuOlzoEgOWwilYuCzEIXRm2/MA0rhmxThxCzNab4lMSR5mvhymXqLlxBuXDoBW2YtiyHHiY1LXfuIN9gP7YaDSzQ0SlpXPuDUTt8THUxcrHIMzXPMxDTA8TNyV0SqIJSm/O9SwVvO42YqiuH2QJZ3Sqpbp5Xz1iA01AwDxGoKLGtx+wuhZ5oomhhhOaiXrFuGFotDx+YIo96TE4Hw46dxGw+NkfLKglixtOszCtC4fsjOrp5Rbldjl+2pZCu1aPLUHmWwruaBkDK71BSc8u11Kqm0vP2lptZU4ffcBOm9WZeYMWwnWIZYLGu44rrIbEW+kulu+2YWizGPdyxEvD3fhzK7EQWWukIxyoBII/EtYQBW/NgPaYLTjVy4lSlDQ3xPXJ2THiCzi2mlrmbRdtDPMAEmCpeHmVIlEW04uOxFW5rqEGMtMuXKZl1DliV1EKhPQAnfzHBNjnUZwJhyjZ2MHZ1HYQoiqhSeKFVRqXL+tyyiIg551ibgLN4fUAplCp3S3Lrg0+HcO01ySuHMuOUqZzn5gZODPiW/Y5g/MY8feI3zADwx8b4M4lEu7JfE6qJ/CBwL7/1Lle3udwWhzZ7jelUvUrlhev8AUUqaw7JtZW1sv3L9rPh35xBSyExd/MONg4GXLpl0BMkWjMS1A75PmamDn7Rnay6afHNzDAVb48QYN5yf3ClA2EbOobWqY9QvUdWH/kpQBwXcObQwU7PmEr4xteIot2FuiMUKqxmKGouuJWoNdwRiOoHa0HS7ILCuni4N0HmuJfGO7m7jjW7s1ULq5mDuWrsyxa9F+6I5ZzWwGjbuHie1/eF+qUo1x4jSjkt5xM0ZSZ5qDpzeWOqgRFSlc+OZTqjI6RvWnldEM6ht3EljEm1+8zpGgFHzCMB7mNrwTCNY103Ck8t//Yo3IbszcVCgcTUGAz/TzFHyNVdeqj2gbw/EwAjinHVeZlmrYDl/cTLUxRWPUGOAeRBh3BEgMgZ4VCYRcAoCCkDQQHlxKUiQAfm3uBfNtXtDasB9cw+oNmi/NwzoyHwzAxS8Xh3uDrNEtI8koQ4TXtekJe8LQbD8yz7shhTugh6JuhbmvmANbS3eNJKB9d9o+JiXLrdMeSkreGnZEAEtsXDwwrLqB1uXspKK8/UaqRD1Eo4tizg5GcxJZQh/qE6zOPejoysbLtoMq3l01iJQXcuXLlxAWxZTMaOyXLQ7tEUfUE4ScKPzATUlNSl1dmERnt+YtGmoQ2qpdknTmCh/yA8yg3Ex3XqK0LHvczEFze4Y3g+UYhci6YrKnof6iOM5e2Y8TSwQ1z5VAhW4rF59TnhoePtHA3ypNBRkvXRLly7auKX5Abuplgbm8wyKpFotjaJyTIsysxrE4TDEQgNnlApA/eIbFZlXJfLF7ML3CzOOefiU8gNTHFhXzCitcF4qG1Mrq8mYnAmX33BFt5gw3KqPscwm08XVQUaHHcNFFZrGYzaiXnCxxxTdcHiDlTznmItztLHuBZEMEpAKCyOZ4/i1zCU9tdy4DKZ8EUWAXzEScG3/AOQ2ODZd69yxUN9vqpUKrFWj3CbRoLqMRokNWdQguTz/AOy/MYU/OiFCzml7QE1dYXJQpFv3O8jxisYnP4VTGorbTfn7wFNNN3evM38MEZdIhpHfqBXYMcnxUtfIUp+CcSC8jN9RwhegvoqKEi0FGviFFSqlefvK3KFPfmXACb4fvESpFTjTMQmgDyRVbmBhXVxXiynaviL14WIc+IPJY1iQRmL48sRIGN6zXcFTMBag8VcOhfVTYdsI/QW+ZnJXB/SGAACjnCDtKyXyYlFyRs7Fo3MRgqKmGuIPk8exzHNsceuJagUFoQTDDLkcjzOAEB4hgrr6IAadkQgWYLhsoqRiBhya2/MKJ8BeIlDfeMk3icikSJhBcWWyfS5cturLPMLlbNJyyoycqcnxDVqyQn73MB7qN4jO2rxxCRea5IrUIcTG1Vq2mPlFOYxthu4ygwcLiWFKHxAoIDRu5yiMf+RI0FRRuHugejEYmOEasTxC9U5GvtOkJw67jC2RhOfcvJHHw6mdahHZKcBChKkBenmDRi2kuOiLI6Z73KgBWMVHTHws4wfmHpgk/e4bGxgEY7tclXHzZx4gg07P7lVVqC2GQ2xDZqs9Qi1Fl7mQ+BPvLOhkcxWICq7OYze6vjrmIIMYAuvtB5cImHc1+V0LHZ6JqIToXm8RVhxnjEoq80vQ9BhFiaFv9EHpjPh1HqqUU0Q1al5ubYWa/wDZgDhpJj/Bqnf3hJas5zCNbXBmiVmuHS+YNKiWOLaZ44KyPxBRdVbmj80zXkzEYQbvr4moSzgW9VDIXRS6gDIOrt4uGNXs4XxUQFaA0/8AsarNThpx1CFh6NV5qcZC+jiMW4hjxnuPOcCgr8xBnIzzBbjqDrxCIVNdu/MJmG9V4zEHV4mq+Z4XMSg7g0BTpLAZj7Z8Qsy5T6lo39p7PUyGClrcyGDKsF+WOi4vVx7F2IbIZQznOa6xHZilDrxL7caIUeYUsgpOC+pZjBJTj+oQm1RSweKjFrrTjZGygpfPiCp00rWSsjC4JBZ62alXUBQMfMHDIuLuO6Mp2+Io8cw+i7lLoZl6nIYLFi73cIrApjBMAN2xioJs/ZDDkUKrr3H4baVNQQMwFXLs/hWdyFBYDJDlkYbMfDKkFZbSiDvaL/cBi91hj5giQvlfGYqrJZIAYFHS1LMChbEIB5Ge4QBS6xM5T15dMMJUAdFrDnfLG6dbDVPi4MJwDj8xAFD8eIyw8qNWVL8yIP1KzVGHn7xGgGzzKIwuDgisHXB66YbNU2ZYRRzbb9o0ZcvP5gvCipWpSMKgBGrp9wWQWiZlFBOPtKgzbeI1yFmty9WrM9wwSy2F5+JfRRdLmEw3p8xq8hHmVYLYPFsEdg446hwrhRmRih94AMJaHUs7JgX+WUdIbp9ooUIa89ykDOiWW/IvxmUHBkvQ9wM0Ldv9Ql9msevMzA6czPC+DqAVpqK8Nk6VDDgNXiYwRqubmSHLn3CxQsRuWZKYDF4mo11bq46GWw9dykJfB34zF5i6tYO5idDfN+AZk0eVtwZ7MgaKq6vMKvq6Hr5glTCsZcQgGZaGI1ttLQ3/AOQTzD23iLS18DmpmWzSOM1DDkYfMoLTIMDqciSZa1FXGRwtcGLgVXca0pAaq+6g2Ai8d8TnHFm1la0xVPGOYfgkfEoQxLw1j1Ksm55l6ZbTq/DDGBpcwBIhlNVrMyrnIS8epWeOz11UXNxS8VGyjlEZvqVKKxgtqBWPJOfIeYRKYNbGMTVTV8kJhwRHPCGehkNLUREfNOVsxBB58ccwo+AXkhLwAAS41WzKauFuqHJq5est5N1KihOMJe2sOS9StaQcjL7ow508wV9bkwzN1039LqVqajNmpcrA/wDkJkhlNL8koke2lPOSU5ulGk4zLyDLl+JsQTnUY/g4RI2SyKOqyBDLg6MWkxqguDdSucRbaGx5gWGze3XMC0CzXD3E6CgbHiXorzRl1DR183zBPApZTNQMJWQeIYHWVAb+JcBdLvH3lfQpzbm/cWd3ZcugEr29ygAbpuvcZc3i6lpLAzA2yy9wHMdVv1ELQaH+osxpQXmOEQOvEvU2gFNTaOoGDwn8wDUPi7hEiAR4I+Mlv3lAq4fMFhemnjM0GH/rholqpiYIpX+5RrkM/EV0AVlM4y2i9xHSFgajNUOU/UKmL5BxHBkC6/3Ly2Cs9R1zuhZYiU/aGGC4vzF2W1QuWRw4gDXJlz9o4bcMS3KMXyEuuX/uDy8AKr8ymNTQ9XBAcl1oqGhhad0c1MolxgYqaQUu+RjYLiFYfmE1S8jVxNJoyhBUK0fMxpQaTcskCFEq2KY1JQ5hkEGQWGBRspp8RQJhUjivUxoqHQfMDe5vwSvh3LFvMyDpXDWtRHGi2jIvxL1boFxRvBC3bd6gsMMHdQQNJ8hFGVGrMLtFMhyxENsUJfPmVKECHTVN2Sha6Gc91UboowIWkIl6QTxwxayrhnNYWFWcPUfJCVhHZ7goxFUU5yRIrsJYQsCxuy9XFXCqy8Xk1MLMLstsy+gGukpPg4e5ovdROZNpEls2HvzGpq33jbrIYLv8RgwcWwSFrB4IQNwd3qYQkiC8S2EltKs6qLKGK+4XRe/p5WCwMCFUygIHEDyrHHIdcn3MascgC+llo5FgrPiCjAcQe2OTkmMIA7XCCgMJaQ9hEgA0j/uVimrUxAI4m8U0xtzxc1Edwb7X5hro3aXxECaFvRNrADXVxiCijNY8QsSFLX+pTIB4N0wZVVNddQeVutnxKvItosMqlmS/cr8s1Tn3mGWgxdGZTb3StgxaFsMviKaJzslJBdoa+/UDXdYaYqogyI1zFztqaKs+Y8rY+crWpZQKrsftBPYPtNBZsOmVVsw39iEggYH+oliDiuZYXB3+WJk/Z1LerwHEECp0cRNA4cQLi0Y54iRsWgx7uXpQ/Q8REUK4ccw4KDpxC4IVSwBnuAK1YauBmmTGOHuFkpRf9xVSpsCA3zdI74KcuO4DSgb8dsqDvg/8Y6ALF63GQ7qKx79SkA4d+l1KCtdKteBYIg5G7/8AsCgtbVahCNBvHHMZqjhykIZrsOYMlMMceJrJsmf6mZQH8dy0ttEl5DQ1xEDBpR19onaa9/mawz/pYuWQmSDUWpI4gLCrXw/MzGMTsZwyBPUdhHQJRBCC5Q9M3Rhe8RnRVjgMEFpVy/U3YherNlkVDSawiPqKoqELVIylY68nGIIb5qmuYw8Joyesyl15F6hCpSAGj1M9bDmr5lNIXJofvBeSKF5eo5ad+5C/ipAZb1F1RO43qpUNhdaPMqBJsgiCK09Q5oQjePMohq14lkdOr5j5ScBA0fnxOYOVxZSIZYLbd27xxMMgFFEBab3LmFNwegahJYAuqjsndvPxCEFl2ZWQvjI+ILFaUbZ+YltEoH7yoA44olwJGc0nqVFL3fUJGCty2XiKUyGU2JOMsrJx4jStiYUirWDXgjqwijt83D90KNQPETJHRPZltuY9dwIyRkvj1F4yazeeIB2rW6b4idUGT8JEuR8HXGYBcN7P1CuQcOcSpFnbxLsgNrxA9lHIhyrtejcFlzTm69xDQDPMcmLvDyzEImhfxMiE6oNSmQCxi6jvS49zOMW/uiAbTBUP4pv3Ld21omDM2DVwdroBxcbbZOLNSsQKwf8AYgU1A/HM5g9kx3GjbqrPvMDHWXWY2yB34hosJQ8S7SuTxcoWZMY6HliUVutalBrdGtwm+7twfBHxiNP/ALMRxylceiVW7R/1bKygtvQ4JUZZReOczCVA51M0iWncK451rmMBFjJUYlFlEDWAVsoqAMtVob7hAWxQMMdkinGZkAX7Z+ZXU0ZTWc5qEbk0jn+oCiy4JjdWVczOAOW8XFUQaQ69yldZDj1E/YCVXYQ1YRaOW+YGWCg4lC5L2D1EM2Dbz48wCroqM0e55Wy26eZSiI6FDEvYGtmRZb7TTq/mbyDbuoACtKuHU2LRzK3EVWbruowXAbOpURFR7JSwTFjtl94Bo65rEDVxRjWoZEIOrG46xERBKm4+gRau81D4i9sAqJW3N/aGmrpBSsObgVpwRXxPDCL09RNpXBL8h4MQyKbFr+5EahLlmcQspe7nTBsuWxLfiiT0gL5g06HNTMA+JbKPniAwXYC8Rlr7NKxVtoWfNai0AKrKEMEWF0SzDWB/FTWdjDyQl/At13KVmbSFRSWKtWKty4YBYNMDCc3i7c4lbgav+poMdn+ohWRVVuyBpMlKFlQgi4a3M1AoXjMZV3UN/EGqMyfzHLYYD9EzNWJTfplkwuV37hGKBVfMsYosRiOpVrL4OpbUA04iWbopZLM0GWC0g827moBgrv8A1KsVavnVwK4xPiZFm9oeJdJgDrMWlrR5nXEIEVDCJzHOpK1BgrIDzDBsHRrHMsQvr7Sk6c+3iAzD3xMlo9x1wZDxLgKMwDFN4PzDolozcZmr3i5iAPnaSxebtf7hHArjnNjGRLk4lkb+YC3t8sVmpwyloLpm/EF7JA2LuGxBcgK9sIA2IrXOY6nTVjdXMiPI83HUq/OWXC01V0TMgjsZuFJVdYwnfzLVYxCYfUYywL98zGCsWoYUHhUsALBSwlmjgWkFVhvk9R18Df7hOartiEGHN0gbKsNXHUo9LmATfYNfMSZQw/mOkvYC8/EB214xbBrBYxsYiLVMOcSy033RhGzsf7ls6eFbbhgKYf7jKGD8GCg0KstuFy3ZUh6IwsGI34zHRIabAVzzEk3Kt4fiJywIy/1EBgCqD1jmBTMstDXiNVDQrLl9yqJlF34XHhHXjOsgC34D8TCICwt0DXut8y3uZblOoI2Jg5xeICUCKez3DmkctTGE0B37iG6PTUbrcbIbsa4ZvlNDzK26rpmKsIoJbFg0TALHLxENgveCDky4B1DsMysJ7qE9iyHcGjFQlZ4pIrJhOSMLKPkt8JX4uCXZfhIyhBTf6i6C0XLEFFAYgtIwOIkQnRh1MmK2qtTAvGPfzMtecCNVrQcS9Qih1BhOVn3m9LD5hfUOqJXE1dPFzPQGMRQspgmjs0OfVRUEMin5lqrYTVe4EsWvGamYa+5vE6XNxgwGb7gFVtKb17hg7ewqvcvAG5DGPEQLG2+/EKgFjqITzXbFSzOXQG4xxauGU/P1X2lMYJqX51lRMCJfmVTQ2HmYYTVYlsDkIRocXzAWM7cXCak9t/EZt2p5+8Gp7o5lWAAs5iEA23lj00OP9HUqW0rRhVFmVgjOHdRKuTTDqVdObXipZCVcvxLGXgR10EfxT3X+YbSgUHXs7jEFc7OWzbM6AFDmYpWGQx+Cbd1u3qGjQZGUROuwfEqtdt1ANsoonOuZjiDUyJeO5zrMWgPtMTbBRCbNbXzDCgdmdREIUxWpsTHCLwyOGODbWX6qaegotz8TYTogw/cj0pEFCV9RdKMRHMsuaH2JVHe1+1RQnd0Az8soHcBMr0AQvd4/cMYuvdinBVK7wNAPuBcJqgf1AmQqVMypUqVBgTQ1hfcG97GmHmSxz/Ji/G3gjREjKBe2z7UITMGLbo6Dg8GJUr64NqURzU1UWEIjrDr3Hnz2xKWGbrUU6WvcPXKChZ5hNFV9iJpyaZSRO3UECB+0qDNGQoYqi8AOb+0v1heGZ5GKQvyLHhOwysAcGyQp8TCcGnIfxFxWFJY+BYqvzaYvgjtTClEuUQhSiNssN0DmaJVoOpdEoiKtZpd3AtTghdGTVFJcqdBHEaq1a3jogioUIOC4AgKF1Hlg1PMqRrtqBGL4sfeCI04a/G4IChjPPqZIJsxmI93dEyoP7jtqDdHESOd1jXxCVWbDHMXcSc+INDlFPcxHyoQLxIqtw2oW0gRNFP8AxEtUo47g2UGjuDWrPcp30UzJi3qWxQP1qKx5mGNls+yNWMHT8MtJbLxVy60MGGYwSd0saj2cce4bDY6hj2KcEt0APbC6pbrLq9wXN2SjT7hEaXKQOUpId0FQsbmCsOWYBKBNmsaIxVoUOGnncZq24MPMaraFUqjW4u5V5vazOvCTH2jFAC7wwywNpxuKx3fOo+xYrq2KAogua+alCEACKvuxwnLVH7Yoo2rD+ocF9Fr+oWumWz9sbkmzgl0wqy6j0qvbXzL2SkMDgUC/tPx4iHIR7oj1r4MH2IH0EBisBa4PfUIsikvwbflr1CcINAb/AJwR412tR2ruVK/iEuEA+pWh5VcDzqZgCu1VeRn1oeUyAaUG6HB+/wCNfRS0OU3DgC6wzBhCvX2jVUN219pVFoqPiGsOt4l340hYglBEVn7zKJm6a3M5AGZuwWKriZl3c4H6gYJyDl5Jdu1gtY8y7FAqZ451L1bOF5lkaNIMxe3NExUIuFlzCReRiosEGxqAynkOZisXGSj5jkzZfEMBTpiFUqHcsflAHKpE/qACwyXiotplAIWsuVYi5IDePmOwHbWoVqIvNiepni0dN7u5jsdW7OZiH5HqAwNq3KrA1rgwBgAYPEbisqiWLmNN89QEVO+6h65lZkYaTLEJbZ2lZhaA3pmwwFUbq4gRwvjxN7DYvTxEfSudQDb0a/MyINiCZk+8qKy1CMYF26q5Wji1+YwZAorcRFVaxx7jmKb04jtImalWdGYsHPwimXQdS9AGsMOZlnGZg+owHEaBL4GCvgEMqq2mbdFWLftHTgYRZ8Z1EXQNCwJUw5vty564IlgqYA210R+3iVePMpUvt3fdlIDYKr+kbl2i/wA1qWEbKsfZS7n4Mj/qUJfQA/EBloQdp4S5EFi6PDn9eYVq/wAS+n+mfMVSqlbVyr5lSpUCBAgW0bhTceYfHe/jzLWuRQOhdB/Mc0dpJ7f5hNRGM0BVv4mW4iSPrIehb6ml22G2cOVvyn6V/CpUqWXGq8kyHU5eBDAOJcTCBnwInLkHUuICW8j6mJRB6Li5wHPmZjg5i4xeYLdq23DB4FasiXmCBH4jVYGg1RuPVdfcRUQ3RUOtHFoZruD0KDdUxvqrF1TAXGbBNRXhbu3UeJxp3fuIu1xdfEdau7uKIKNsp1T8oItjh6ZX2dDUpTIybV7WWIaeEGFGC9lRm5lLw+ZYBZKr1KMxqatalNlM/wDkyjBsvBGlHJym78xqUOdWRIYOt34CUCiUjqpr1DBt9w0FC6vFnDBVqnHiFh0OGGcYsPEq9nCkUDeSjV92RKBdWiCRXmW86Vbih2nJ1FvIuzGHhJjE/D17jCV35bi0mDfrEJ6IGIhRFzLkG+GGleDJKEW3dA/1M5olZf3A5YN5DH3ihSvCJegrulf6iG4903NudBKJePJwYl+Tc1Y/UD1LAWp8rMorClDD4ldY+oZQTAnlmEp4D+zxLqbNn+30r6BKhBXGWNkDrl8Ab+JrGjdA/DQ/LHrspVa+1lfSpUCEeDcSvlahPC/pcubkdBdXy+4WsOS6OgMB6+gQlSvpUxArAgB3EgDIZ0LWvmnphBCtCP3H0UePpUr7/wCBmMucCzK5sPctM2uzG451VcT2KfMc/ARYIF3HlBcIVglaii/xGwgGPc0gMUyknZ2/EOJnUYThC0CLj5hp6fRCpUeBdfeUABKFxUK3XINP2itU2F4/MEKVRrFeMTL0TSzES+URzGVgYWsRRgM3GM6afaM1DC8S1O6LUghAcbhfkCr3MEwvn1Km5f8AVL8oFHxODAU/fzHYxs+ZY2Oy5PvUrsK7VmM6X7Tb8RHnTDmocVnGa+IbXF2RqoFp/UevBhDmsSgxXgZ6g0oLP/kYFb/gmp0JgvnxLAjZDhrklV8maxnuoTU7hn9TsjRg+LhFupVoP3Bnc6s9BFEqys3QMDEPYEC7+YgKI8A/UcBHakWjqha/i5jhvH+43l5VEtlkYrpnywqrlW1ywggkkMxg8R/bHhg+A/8AZ61KlSoJgBNw54DcCS7uFn5YAYCiVKgSoQURahuLR4vn0ZmKqXT+C/51Hyk2ltdSpUqVKlTHEa2bSG5Ux/fiDVwUq/Bv9IVNYFhGgMH0r+YUBHBNvG0ovHn2weZrErKeSOvyeUcJVaiq9q/4KlxwlUAVXoCVw2cG802Hot+JRvQJWre5t44GKiPQIlPD2m4DtcYEeCJexZdJSUY5vEYHwkydNtZxDTMq6IVNu1Ex+IWirHpcKUxepPmMEMyokf5tStn6i3FdO/vL/tlqDhlhcJirlpZuf0uIAB8MS6gOQZa1TIhpgTzzNpzo7mJQnFoqvSwucytpBo/UroANI0tvFb7iUSeH7l2shk4mEvMf/GZwAcP5jfBfe5aONnD/AFKDTWCMAnmxct994sPWIWeRgIYbDsoFftl8VWKt/EEc0Aq/BF6Fldj8zuJDglRodncsG+7ijwGqB/URnAiOph1PQbmMMLFG9v25mAJirR5sv6me4CGWJ24jcUHLGNYHR+iGVn2h+gQIQATEOXRuY74DfywDiVK+gtAG4Jzjo5imv9pUqBAlQJglyqyqAeV1E8RuhD6N/ge4Icig0DoDB8SvrX0qYisBLwAdpj5MHakcBOqr9Cauvqiaob+foH8gl5xljFeUnJ0crwFjbEKRNu0s9rPqKde2keVh/OvplaIR0ekR+LL7a8mKj2KUBps6eKfMabtct57hwKFnT3LlWzG6ZdlZMHUAz3BxiG2R4VjEPtDU0C2RJQODmKhl1H7A4dReoBlS7jezunEyv00pczkMazRcbg4W6lcUbeFmURyKEQBIl2weIJlJmYwSrYU1ysLcG+GqZUHXKeyD3GKLYvKTC8cUZftM8TVOeJo4rP8A9gW0tFjiEIyJLGIIGWFqU1DHTUOD1AGiflloKbFottHgH7hAe4p+pvgN5KrKKovAA/JhgC2gCJ8QLeYBeB2y1oX5RS1uWZYD3NSUdsRETQFHwG4JuBZT7hr5zXZ6SDyZ+CiUqrlcrCBQ7zBnB3EMG/Lr7RGx7Tx6lSoEIom1a/cbWLvn6VAgQJRzFx0dxePvMyvoEr6USzJBbXB2vEd1DdiD2M/D7ypdXD0A/wDv8qmJozgStG3151H+Uayj0WPQz5nGUCt8ra7uBiVK/iSyYpDVgO0wfMRodhNX3gfnR4ZXhjgB0DA8ED/BqW6OeOY4dyKZOQavwCz0VQo9pZ8j0iuJtCPKy5csDWgnNd7VjF1Mz3nS7uXpgV5hLO7OokEAx4mSbBzmEaMuYaqOl4loYQz6+8SkVrhcoNMDZG7turd+IFpdt6vlqeENuKPMATAZyS4G4DQF/DAKOd/2JVFlDVj8QBoUCEiASGlbLGjxVszui1pF+ltFS6R6Nu4pMN7QTH20AAw0Ai4yvAinjwQRmS1bDoUTHLfRln6iZflleBXfcM1npAC1ROE/LqOQk8zhYp4gvMsUagFL0BuFBMWAL6P3QK0qLU8rXoqWLgtTavasIAIDxENrg5YzgX5YI2W7SpUqVA7ihvBP/QxVbcsqVKgQpAOWjiLvBjzuKv8AElQy5aAtlniXeUe9PtfxL0Q8mP2e33cr+NTEeddLI6A3LSeFOPfKj7/EwhqUXyvlnPvcx9bly/pcBLmWjAcq9edR5Yl1H8H4SoDayesOfLnzK/hfX0uV9RJhbQF2jXyfUcAKZNV4HPyrwZVRCkoHoMDwR+vMNYGFtVMZmNMII7PEbkNh3Go8Zx8QsrMDxCNIZdy/K8lUxqsGjDDF09GJQ2vzbF+Z7UmA9Rm8SgaE9LKSvU61EkwSZ217Qij/AFGpVvGIAcFm16CWo+LSr11GrG2lv5gmIVr4juMTuVe8sIFMVvoTBadG5SYxCSMet9DLMIfFuEaMv3na14h6YTbg7Z0r8tRvttfxB5QaAiXA+YiBbqAyr0BuIG5GMfg/lCAJLTzcvwhsD7Qqe1YEqVMGX5nCLdxZt2/B6JUqVKlSxLaHVy8wry7irv8AgFwhCqgNrEcD5f6mdrbq3+VRgUXAEy9TzD8nX7eI7IfDYU8t/p4lfyIcULQHfUxjtSl1we37SjYL8P519SNgewVPau/rf1v6qi6gFz1iLX3AEPzflfBEZY929Ba2/b1U/r6X/GpXMuIvmgKr6CKX0KW+HHxd8kZp2zX+6bfLb5/mfAPL0RQLqMSxz2xqCA2PMBNLVrhjPKTMWst7pNOPxEMC3xHeUdQDzEFoHbF42eWCDdlvx9ojxLgAp0Eo1LJsvRCDXc5F/qN7n2rbFjVl8TFmnfME5cvcJJxXwE2HoNwkpBYJpmCX0NzEHxbhmjLvuFMqpZxEi1o7l1gvy1KS2nF6lIDxEQ7DY0DlgiTLDZeDPy1KURLUF8OvjHKTa1Hysr6ZmCa2T8feACWNGg+JX1qBFBa0ds6Hy/6iq25X+IdywOg28T2PLqKqKtNP1v6ZJUBWguObd9z+OPmpSbuWVaPP+lH1v+FQFaC2LaOktB3W9V/9jCqCgLe+I/mPZK2lXyv+G7A6JV0IA0asS2Hmni4+jEnZej8UPEPx9Lly/wCFfQgpABnPBEx24A6Fjgecow/vS0eTPrrxPX+BVFeDHEKJ7DonovzADRntgO2dAtl9nwQBojAso8xcLDtgmaxfOvtOzEtaFrruCSrkGX6CEXjDmf8AUamDabfzAzZPxMDg/MMr35hBDX4E2r4Df3gTRCCMSt8A3MAfFuAa2/eAl1giAtYJdg35dRRbt+PtAQPoBVyuAO4FDFg2Hgy/NQRvtUvMBx8YwS7UR8rKmPpRCfZjXyzkbOjUo/gErF8cso7eX+ottra8v0uXCBK63Cw2/BG1tW46PR/BPmpUqB1AEg6Nr1/bXmL1ad388fH3mVVyu3+IQIHBliPOTFHhfDiEuEDmXa/vKdrRBXgNB4P8IUC14JnFUWpeLPxx2kY1dIgeRw+FsPw2wUcqu5X86+gLQW9EzDMAoeHPtg8x8yMEPmkx6ZeYiRK1W1e1fo/4MpZoxL04/mBnz3CieC4J2344hCC1RHCwfBC7Z5WvtKorAWug3KI4chy/RFaBvM/PERERtcsCbZnqOOP2QW9vb9BGM30JtGnRv7wBr6CMat8Blmm/ugHvvmVAihaoJfg+zgindnrg+IV9dsZeCIF2Sz4zMWfBkx/Oj95sIqCfL/Cu5jdvRNw9GvmABQUfwqWazP0xxGLfg4/iZQIpZUxo7ihXH8ggRQUtfrDPwmqLyQ/A1+TGDqLUtXyv8glSuLVoXKr+rfEI5NIV9x+8QAx8IdaD/D6jBvp1Pi3b4LfEqCCxA27X929E2lDUni3639Ll/QJglxNkK9JLdvgt8QSgGE1Htf3Z8E3G9JPl/wAdcDEJUcGZcLaX5iO0AgtqjtjjVH/FSxb5nX2nEEgCrQZYjDNhy/iKHvzy/niJCIyrlYrNmz1HGP7ob327lB9GK+AmweA394E0VKgmbRz1zNB/dNJvl5+hFAtZoD24gS34HH8PcLMmrT8ooFg+E1nev9puwExf4VPOvRNu10P9wKMfwqCWgtn9kr5dTEALg38v8QWAgsg73+oYofP9CNra2u36X9Ftug9SpUtYJpah6vl8FsLrA0lg/wDH9Ir3QVbXH8gmI79Pa70E1RrzlZO344iemX0DQD+/8FfTCzbAD2mA9xwcXJK/Bj8B7ghJtUDoMD0fW/pf1CVLj4Q4QHtMDypHBPNZE94/B7RaVdAAdBgepf8AB/jX0rCnRDnfu75IDTzQagOmKM8QNq/HEGsBBbqJrUH/ABRDu17n/UBLUAS6DLEQZ4OX8cRk7ssr54iJEtrlYJNmz1zHQ/ugNb7dy5bGa+BHaw6IBqSmDmxZ65mHP7IAzz39KZgLWgg6HtxELXpxCKlSu4c5zSg+58Jrs4rKPeo9uZvSgi/B0fwqetcrg+8LRnzom9/wBhCUavAyviPXsRle2P03KlvoELYNrgjrLfB8H/eoxanb9Mv0qBKgKBtE9hdTDDw6D4N/KjwykxYOAOgMHx/HMCVKKbYN0drweXEz2/bh1w+jMEvoZQen7QOofyD6BV+8GA5V4POoirVxH8G3iVc+mvjjny2+frf0v6hAlzG30Un0EbnCwFOgs9LPkiIP2T2k5ebMv/DUSsTK0ZXibI2yrwLt4LYyA9kw9pr3Z9RPKWmr8ynioxBbXEP+IHRCPyT/AESiGFDQZZXEnGZ+OIxee9n88SyKo5VyxvN256JjD+6BG9vfMqBFaPQRNnwf7QLQVBQjaOeuZgzD8yhnnuUSmVWXUDQt3xHIXpxKlfR8yuB5Ws9N/CdQlpnvi9sQNel2HgOD1KlSpUBprRt0HzB9v2/9RC1fXR/ATCMAl0bXoleKnbP3cRyqtrtfpX0EEWq3B5j99DqOW7rXR6P4GIDAqPpgMqoA7V0TQNVasHy7+FHljZk0IegGD+GfpUqN9GkFfQRHwiwkeKv9saOu8Or3SB9PX81bHQFV6A3FFomsh+f0ZfBH2nbF6Vdv2frc9/XP0CfuCWo0B3KlDCgDxY4P3eIXSLJQ+56YPE1r/DUr6O1gswHtOB5YT2pSieXfwo9wwxiIB0GPoqHXKUf+BGbfY/QTOGgtgWgt7331GTkkZftiq2trtm5sW3o3NDj+Zi4MvLuX5ZSMU9BmVu/8G4BQomIE2j8czSYfmHs9/SpXcK6L98feOQr8cSkT6KEuSTKmPxf6T4lqJ3/czphC8HQGD4gSvodotS+nMDgubxwaOD6M3CCekHjMrx7zP/iKVVtdrL+lQtARq51Ehzds2q619alSoRa5ReOuWXBQVQsPfL4+8BKw2BQ+v7c/WpT9KlRfk0CjoDbLNMYQ34ezMa6WUtXu+DUbUii1ZV7X+FSiqFOAv+/oDKDcvSVxRAQrcECSy1+dPTFA3pal959FeEPgfRQS30VK+YFZftBpYUdyh5YJUfYhjJtKn4Pu4PMQOORpHzSYH3eWJDqrUtXtWB1K+ZUqV3KnqEVKlRjU25HoDcziPIZL0OPUt9SrhmxNnfJ+UyuD7fRQTEP4iUTE0BbDN9RfJ1Eynhcl7i1y7ds9swhnoZZ2PiNwBorzzKSkUr85Ni8W3ywDQVC4KbRz1zHXw/MCe++fpUwLcE0hfv8A2iZV6GD+C7jZG29J4X9JieIKT3ye2UGPRgHQYD6KlfT0W81GYGvX+/oqV9UhQtRHcYHc57ZT9Qg7ypjcnjX3nJcdcfRaE/cy3P2lYqgWtAWvoImeh5h++h+X1NYbta98/L6Mtbg256x6ClnEVW8RWg6DbNOMJtd1u+WvUNvlCPWFx6kEqfT0dqsTw+qn+5xZuqf7lf4FP9y5oz/9blfKnTf3Lut8P9zMFF+H+5pxwWPxLqCroG38THfyRvV0GfbHlL2oFN8NCvzeWFhI5HKru1j/AOtYmWi/L/UE4h3T/qVcF3gX+p0fF/oiW7Z4/wBMEOnj/TD95/8AOPLn/fECq+4f3KAz03yFtfAXH6/TeXd9fcfBGEfdNPlhW697/vF7zKs/Vcnn9BE/+Y/3MWP+HzG05dqSvxFH9/8A4hwB7UJ1EPADvK/qXRfCk/uVIQaB8WWPaVARHoJHptYeKHiUHJcuz7QAil7of1B4j5hd136OEJP7CAW7Oa/6lYKh/YPEEkLfJ7ge+YPUoxt6JylOjcIUKmZXcToZh/uJ+WCVUS8HMavgMv0QDQz3z9HtEXT7kMmKYVAPvMqnxQP3EMUV4RP+luWaL8P+oTn8n+o6J1Ct3bv4nGUc4fRfyh5lwUfQFE/4P/Uq5P8Ax1Olf+up5V/11B7UsBflcEC64QW70U/EErxAI/USNl8H+qf/AE3+oYv2oJp/nPM/A/bKvDNYF2osSTYOA9lt1Ly7nr/1iZt8H+2H9b/6y7Vfr/uZqC8sCq0fY/olzIC8j+ox6JCWPK09CyqgUdqj+szHgH/PEq4F88Jg78qv9wWrHumhVw+nB4/o/wBwZhtg5HzKUFSI+Ch+efEvAdZOXdy/ijxDIw9UK+xFt/d/6iEr8z+o6P8Aj9zNlfD/AL4ctu7X+53J7T9sbNvtX9sphTKQA+98MeYSMkRGZhdJjWL/ADGBqUR2OUHUV2nw/wBQq/qf6me/mp/qZLzd0/1P/mP9QNx9h/qA0HoItKPU9v7YzvUFldC7fAXxG3HeIea/lZ6hpXkpcJ8sU/2v9w/9x/udn3H+5/8Afz/77PJ+7L7fdMuWVGNmUW6Dyo0PKxDW5MhvLhfqvaXYGVgB4AwPUCVKlSpUqVKlSpVtGV1OPt7Twu3gtmgGtg7b8lsdb9oI+VlqlSpUr6tHV2gnF8o6DwFrMDbmQuqhJQL0/wC4P/gf9y+n6X+5gH3o/ctFBuEAB09wRQjwJZ/UII4Pof6lDe+LfsQQKK3yPgjDjdrAmOl/nDk9h/7i+z7X+5gguLUPasIptYGFHxLaFqwP/STp+wSiG3CnD8qo/Gg51dm3zxMedjQHQGD6lod4q0Wxb3gHD2xHOuBr6lfTUmGX0Z+yYHXx/aHAMfw9ZXmUHzg99Rznf/A9fvxKNGp5fbzKlSpX1Kx+2FLUAEs/+MtHmNzSG1k9/op5uVCKlSpUqX1L2eY5c2t+i5plm+u/M5fiP+O14OgY+H0qV9alQCKRrR7YD2jQ9pHGK2UInga/A8MHlyloHoMDwSpUolfSpUCUfRFP2BL4Ceb4AVdFZ6WfUBG+slL28+a0qVKlSpUqVKlfTEv6g4Adq4HlmPW8VH+56FEeninB8AYPojt+wD9TNeP5licoYNx8V+YP+4BrEKmNdE2jtP3j5ZSdeoSUcEuFXRyzFHzNvjiVWy1drf3lPj6TvFqPCce2N3A+I+XmCFBRwECcSvE847k5GgTarEe30i2+9/rFh0uC9Ax/cr61A6Lm/b6H9sFpk4P7lSpUrqUcwy1Q6OX0SmD6NvniGUKvfn6KlSpUuv8AcxKtyJf2f7qAsFXC3aPfHxUqVK+tT1Gqw5P0hn4fKRjII0Q/A1+T5iBFFqbV8rK/jUYyx8SgBdpgx8xXHNorO9v18TJzhGENAY/v6V/E+lwgj5ALjlxxFTcXevBv1b0gYGaX2wc+W3z/AIK+lwaxlAMyjwaYFxvj5p6ZQ8tNR+4+ijxCH+JSIrOkkvgNzECFGt4Awfuyz9NpPK2/f0uERahR19b/AIkd1Fwlo5XoGWLva9G/vDPEA19C7qmIHmb+CIuHYcv0GqGZb0R34JuJf9BywQoKOiASkqInDJcPtWCI+3Cn7nxxBGutreBv5+ivpUC2hb4g/tA/PUIR6D+2EV9agLrXcQ06c7PxDK99nLKlSpUqeswUQFhl6B/4eZUwvfK9dfH3ja38sqVKlSpZEjoNLZOr5fBb4mHq+N9i/wBvRHCBtVv5lSv4rOKohdHauA8tEwqpch3X9f5Q9bWyk8h+30qV/GpcPoagLV6xHRbSKL7a+VsOCu7yvmz88dB9a/mstWgt6IdQHF3oDL9Y8xzSFDPIOh6t8x+G2tR2rv8Ajmv5LBzE0EEz1PYdbvlolIgKgDzweIcuhaq1e1foQwFBsya/w3mEu8Ear0DLHneDb7wigqGNELhd1EEryW3wS2xXZyz2MoTcQp98fmMZfePlmNwHRCNEGUlcH3wO1cE+0sC9c3ohbU71nkP2lH8PAXHIqen/ACpWos3W3tlSvrUBWgmyfEf7mI10alfwqfuOBm1z+gz8I4dHgPwNfk+YwdyFW1fKyvpX0qYlyr349hcEccDdCH0b+VHhgkiKL0HQGj19K/jcaulML6EqcNAjXrifz5jYxe8DvcvpUr+NfQEoWyptx5T9mvNDyxLBxV6HIk+ynm/rX8q+iwzNC0N5X634nWsNR+0z7YeJgb1ddHQcHglf483QW9RsmdTW8Lv0RpjomU7bXtzF8vbYfjqP0qYlfzYsFTVq2dR2TiMG/vBMKgy4Ba1HU0+T4Id29mTAJcLYx6PI/wDk+6H5fbBKqI3zDEtDPKAbA7XiZH3r3X9RMQpoPvt/KB/CpY4PBliaFe9/dKlfWoF6jvtuiWPB0SpX1pmpdwe1ydHb6tmBq+PA+P8Aa/RGCt5Lf4VKlBEQilroDtXXzF3tN5EPt38KPLKBwJj0AwfyqYI8F9AqugNwRpqIPej932QAOGmh3wejUdIotTavav1v+WVoy8QErZHQ8SFv0fNTIwuEv3vZnyIhTbNR2rv+N/WpqLMKUtQwdq6PLifLsg3gz64eYAgYjhugwe9zP8bl/wAblYEZ1j2nAe40p2xy/k+NRQ+AalwBj6P8bl/S/pcWWrQWugl1mO2vza/RKbQlgPg33zDReCCILVRwjT/iiBdm+zCkGZjHo8j/AOTnr/8AqYZRoiRJkdEKrGht9+CZuk4yHrV6GYn4BxB9z5QK/hUS1l0f7mF0dEr+ASv/AGPmPxNq46NSpX8KIuFbTUPaxw6PjQeuXz9pb8zBfB0HBK+tfRRBrBoC2JxleTD3/wCnuHGhZDoe65fLb9K/hUwTeoPuLEvjPL5r5l5wiAB1wo+CN6W0EeV/nUqXOrfJ7q/rL0TDBXCL5Pyxhyn4ttDgOjwYlsu/5ViV9EKzQVV8BPMgBW/L+V8EZA2rk8vb8/zDR7/k6r6BUvolWYLAR4qwfzKQX0SeDK9y6/w39WLNI0KXjvweWNRqsvJ4f0SrHhnr8YN/RAKKMs43/gwQ1F9nMPoEVpb45Fm0eP8AYwRRA5h3lIWjBto1X4mfqdMW9av3isfjKD99/UA3rxGKp0F3/ATRl0f2xdjHRqGGNQ+tTE0jfvX3cx5d9HB8SpUr+FwjkVgHaupbg8iw/wB/hGBuNNB6DX8KlQIYxgAWr4CeVnIIfLo/L6j0FVeMerXPym5X8K+l9SrYFr2njt9VjzPVIRLvV7Oe5vag5a6Oj/BUWNlpvUD2q0PLRHBoelR5Svho8sxElAA6DHwl/wA6lTUHCjglNHAlDxxeaHuH0JTofgPFCf3/ABv+YZgwBClhTWPWz5YdE63QvP6CMrFaq1e1Y3K/xrDLVAAXnrEqELD+CfsYms4R4dXNEqpcq7v6mI6DLC5cDMCrWhlZy/jMr54hlGu+2CgVBMaptBqPgIS54Vv+nzmEHASl9x+KJeb5dv8AAIeLl6bjgrQ8P9wKKD6X9QgMZfGj5nI2dMH83qRoteA7XiKMtXCo+3n4+8qzqMR6D639KldwFQMq0e+o5XiE/M/tnxHoUFIsHnl6wePpX8KlTN0bmVl9Mxptb9WlkY7gtbu+5+J1tBgPWj4fW/41Ll6L6BT3QRZwijKdFYerPkh1nbLa7Tl5s+fofzCYIC6FroIVeclo+JZfr7kQsDCIv4vy8oxDbWo7V3D/ABgqha6CbLidj8dvBE9DwgQ9p+TmPMe0E+8v+AtuB5/hf8LlAVOCbLsXYeDn4feWdaVRXfAIqq7QR9v1v6fhfTZctDK+Jy/jMr/UAoZdrlfawHn6ALqIaXUAqvgJWQpdEv8AzmC4CpNDya9FRVkQ2rKvlh9CBMAs9MsU6PzAh9agTBrfR/bMY46NfPcr7fxqXpHiBdVzYe/9JdKFofwcvv6X9QgSok2uSlv+nzUa3gBtn6fFS3+VTURjYWQBtTB+/EURJ5Vnbv8AV6Jk5xhqGAHH9wfpcuW/UJYQyxKALV6KjVeIJQvi2PuMY0ELNPlz88dB/gqVNT1KV5gIvlc+N+ILX26Seb8sIXsMWXR0HB4JT9Mw/nUuKHM2IfaYIehuHI/l/wDiEg+GMuAMH+TEuLn3KeGTEHvRCLat/K7ypzOsOgwfwv6XFg8oUbX0TDfhP/iXiMtrlfaxeYQBALDa4AyrLRSUxPw690lBIUsH8/o+6Owe0Kr2rv6ECVFOro5i6wd8zbf5lfXMCbzL03ME4XB/bDpK/hUHMTABbGEocLCj5dH5fExm9aPt5+ZX0fpUD6BEDKnL6Bv9eYGPwB+P+mfMVVXK7X+NSpghpwzRdHauB5UJlPE0/X7z8o8cNrRvIft/gqagLQtlPeiqB5sv5o8sc3EVajpEmHgHm5f1v+NfRi4XCzoOVXAeXEW5zkE8GfWh5ZkE1QP0GD9/S/pf0WXLIQ+lxbAUAVZUKGWEVdDj0Mw1xv8AF6be/oy/rua+mPrRMEUi+noBV9BuY+6DlfFgf9c0sJnB5G0qVMfR+jKYYE2hayvz9MCDDz8RBerpUvFl9tEz7KtUTx/TnzFKSq1HtX6BBdS0oLdOB2+iK407dzK3z3CVK+gRGb9iNFGO4FwP4VEKKrwC/wBo5noX5f8Ab7RCJSlcHnZ/B4lfxI9RQI2sI+gyvVxurhwj8ND8sc56KWvtZX8a+mxQLJ9EDKtkOr0OPjnpjvUGQT3vX+AJiFrRlYVY9OnqRfxe0mHBcEPW83szB402tR2rv/BUr6OfmhUvQG5T0DIYHrL6cvqIDM2W+1OX5TMzH+GuZcFsZQBbesSm+qQelxeYIzlPR1f9REVVRlXKsuX/AAv639My4sMMbGJST9HtUuX5+0rQrCg9v6Rw82hU9qy5cuWRZuVLxLOYcnFEE4zG9rRCtRqw9P8A6fMtqjhMXz/vWZDOIJ7WBBsXrMZvEpkraHK+gjOD7PgcQLVbVtZYH1IRdjUf/ZmXcCVK+mGZWcRIUaWEt+jj5qMbSUhv2cPiv5VKjrsi0PV8vgt8RuqN018Fv/lRYo4tW10dH89RMlUBVegNy/A0KB6NPd+xAGmtfa3fB94lEVLVlXtf45/hc6Z0Xiq58FviYvl4jef8pYUgLW1wHR41/iuEVJoAuUHwp6HG33U+YwYdCoferxQ/jf8AgCAW9E3YkrQnWxeovxxQl7UwfzFmXaCPtmfqy5f1v6V9QWgjQRfupdDnLv4iDOxmffJ7nIyJ2HgOPq/xXFfXEJc9H6gm66VV8Db8AzSo4DT3p9rM34kcv3+hZ19PBmUecS7fRzMd/wBSo4lKmRtZWB9CEqKFqjjt9EU4eZz/AOJXLl7gQ+tfSgXrJyvo5lGvYZ+Lx+/MVara5Vyr/CoRU4RZogPK4IzxOWx+N/Kjww0hFDQOgMB6/iSvp4Nyl1CBeWiy/NfMqTUw5L4dHwRXE2xR5WVK+lfwJcIINug9paHliugcy1fS4+CnliiS0YB0GPhN/wCItQCroI6Y3V3oLL9Y7SWJrSJ5A0PVvmOcmzUdrz9b/wAFy452CujyqhDtoNJ4Of4jznEwPQYD/LcuAXzlQwHauvmY6dvtvzevxC+qMF8FG5f0v+RL+twMpg017vz7t6jtkxZdHQcHgioP6ODxFvQtrBNWPD+j/cyeW0tlQhCBL8Bq9r4OZgBtyD7DiFM5V2uWB9CEr6ItLb0Z+7GhRPLn8MUlVLtd/wAKgSo1aAtDrt696iuWl2IfYy/Fe5SuhR6AfyqV9KLVSvYPXb9Y8zXBsrqu9Xs57m+6Vp9HR/i1wZFT3git1AhLOhx8WfJDSs017uuXmz9K+nP0r619FlJNVHvr9ZfEERFhzDtN+/smDEyyq6Oj/IsUls4YDt6IaGSw6vh/RD2lLrcWH7f4z63FffQC2+K3DMMWJ4VcQ6HxoLuCqqtrtfq/S/43DxOYssgPkIaHwMtODC4D5BHCo/8ADEwhPIv6ZTjbeVPuSk+QiSbUaPdT3dgceqMT+qA/cWw+kf1L9Y7hJ2iggG1giGqDr/R/uFncu1l+iqlQlfRD7Bv56mbYD/wvMCtH8KlSoCgC0AKvoJxM3lKPen2v2S9U9Pbt79tsqV/Gp6mspmC5tb9WfUxA5wV3zPL8RlwUKh6DHw/wV9HCFQCq9YjjYQFC+Fr7jG0nDNPl/LjoJ4Nf4SKS9apZwe1cB5cR5e6dT5GfSh5ZoAswbocH8sSvpUqV9HhfQCq9FTNemG8BDT3HPnawd72efv8A5bh9g0EqJizUHk3DoKUol4VCuhtBPv8Azv8AhdfQviajnc2qPyGm35Ijo5hX4OyHvLAy18MqWnmzVSyxgwH9xUZVqB1WaliGgFi3lGXXqLVCZYDFUD8x60DvA/DDotQx9jAZaKnJmrNwX6sRVQ2tK9BjUMBI3/6kLafyH7IPmvyv7imL/b+p6XtH9Qd+AQP5mvyK5DgswQNyO1/dx8QDQUSpX1CUEvQbWjy9HcKag5qfk6/J8RTPZFr9jn5Ygn6KZUqVKjiFxxb0Pdpg+ftGUV9kR/Lf6zMziFVCgHGvn+Z9UKFspqVXovkuvNDyy4Lii0dIgw8U83L327/w19HE3QFVfiPppJt8h6FvqZSJYD4HK35T/lqDZwQhunSHWyLg2kc4djjEkLaCPlZf+OvpnUt/jGflYe4nP2h2xOy0YPoOPrfX8b+qzL9PczLlrgLXU2E5Fi+rlDFUa3xDlUYWm8MWJWp6cP3FBU6ZGZZRtVY+YEac07qMOKPl1NzzozEPLMvZHuq19ky5HNRqxRiW9sCC9u4PYOSf2R2wZQH6lwDPP6hixVwLv7hOurpT8RpVwW6iNQyFsWXBlCNF1QzMiAahGNe0f2RTVBusP4I6aPL/AEku1Q7sv2zAD7X+yDZLNlAvBBry4IAb7lWC9qn2KPE0oOMX+rgRaR2EPyTAN8Uv9yhb8o2R2JPt+lohYQum0NW9PLRLFfWsL1+8ygLQ+0jsP2lSpUqVK+lSoCtBa6CFLzVeFdhC36V2kHpPgEaq835IO+mzUdq7/wAYlywAQtcCiA7MtPNPTBFzYWX3n0UeJX+AFiV9crRl6gYyttc3a/qcoFZx3+4xIyaXgdAaP8y1NacqLjuGa/trXxY1PHPHVxY39Lly5cv64qefpcT+CDcTTNJJ9BBROUa19j9H3luoYLGuQV8e5/5a0IBQ3buGCLh5CCRTarfnow4LM6T8S3c9J/XcTbALQwEb15KUiaLm4rXuMy5arupUBRym4DZ2+iUBPnEqnd6B73BC7HR3GMotqMRrixmKmR1cbJq6uOrDkSJg+6uCqHD75tuAWh0rc8wnJmHxBqj9iUpMmVVNsFkuWiB5G086bQvIss0Cmj2DqDjWxaH4Yht/Gq/mLl+9UP6hF8PSf7hYUOzy+Rldh2mXawFW28REhIaEqLZjqm1gNFPnP9DKylPj+xItp+X9kDsN1ZfklJmOAfwME5FnZmekzmE8GWNVdoh3T28FviEpQeInl/L7U3pIZVdHR4hQNlvDepTKlfxqVAVoLeiKhmS6z4Mv1jtI60tCeTw+GfMXB9oVPav+UBtJQwO1dfMB+Tlf9qIqY7nr8ANy/rf0v/CdaqgBcwyEyK9RwhbZABLtXUYNFrUfK/Vc/wALlzP1Jn6rLbE9Sh9ZDQeT9srC2mtfi/8A5Lg02jZ+XiZFRVtVmq5nt+HU29DGuDax6o9c+4b6N1vhgqgsVngZsVlHhPDKFXwYES7Fx4ivvi16xFKmfDHNkDGOYzbhgwrxCSg5lxdAW4Ip2AH1ABe/B1FJsrR4mJK2VatdRmVVhjCUivZLnDShJaZR15laCjl8w+Llsdyr7QPqEGgTIZW1e7Kj117gPeckpManteM8o+F21ZHxGtKmdA+oTJkyqGzGlN7uCb63LyC3RzUR9ctb6yrngMZGniMFechLupBaD+IRgyUaeqiQYGP9lM2zuqsn7EdMEXan9JcGHIlb73KAmGRAv4EH8HSW4huwTCZqxI3WZUR9UA9QHdPlf6ZcWUd/6CFNo+2v3AhKdUP6ZbiJHtqWYLj7ygn76ixuaE8NXPgt8QBObHMu2/L7U3tuZWuA6+qpUqVKlRUr6scmgqr4CZGAtz2Gj+Yj16Yj3uX0v/LQAq0E30euDmr3AgUorTmsevm2w8BwfVnM0y/rdfW/pX0uWrRleoPfDxn5f63KcmtUL4H/ANYhmFgyvU5jA6tW/pmKCqzDlMU8w29MBGiuahXNYKbIrbKA+RiErcw2JgHof3H6Q48wKzisj6nNYNwCRXoRziNEqOG3BLndBrKFjYS9RXbtrwWWNKZXiOK7tKsxRGm3uYhjlKEmfDq59SgsBugkC0aprmZMCtIRiiDpykdw7rHVXCaL0pCiqpinRAEVoQ4mdAGYXk/huXYMsrBeROGHaRoYJ8wD5ZTUVwZvmBbBaepYreY+DmB2AtWgwyjx1LQn4grxj9wHLsgVlrUdZoqCW5Aa8xjbC6Wty2M6zoiKFHLyC4QKVaU3T9iLzd7198SutukfoypUmwCfkjNoGulfDAkNVYU93cINnBWX4CXXVxcldhHojwD9MbRhdv8A0RZVJ2v7QRacXdDrQy/szdaZwbC028rldw1Vh0ivsnUvdX4IjkXl/aZWm5A/pidff6Gngn4Jlr7yh5YncqY0ZYWCzghImyMj63v6l5UMML3w9RS02tVe1Zn6VK/nX8BYMekO1dSpLmK28uf+xPjRquMcypUuOJuVn6WV9a+j/BajOJpJPQRrphC/Aj9H3lNA4Qr24jhSyxqH+5VfW5q8sR8dwKqagHI9xx0UQR1DSOoWniFlhCcrCIpRfEY6OIpLCHMwMOe4L2KiFMd3EruGrebi18QW0gBWFgsItgOIttYF2VNpBUTOArJ4gUAtmOXddhcAzl3jmXZWSg3c7qhPHiGZ0UBguY3plXUFRsLW5C9MJdu06wtytO4DteuT3ubgk++Q2RYagbo8xxIsBBOaYprDmmvvLAJApZ6ubSlW1NIR1huhKGXysdm9yyOJwWC81xMwC2y7vxF0AN34jBrBSdrAtOzd4RAfxcmewP1MxUSwVdwSU4CcymYE3zczhwqbuKzWptgIhZpqoOHel0tTCuC+C3qEQXEsotcQGsm4N/MIBXkwz41C5TYWEjGnqNuwVvH0KI1GyLP/AISmyOrK+aioKusEz8jBlBNuQ+AjpRnCN/BF7gd4f2UAUgdX+iAwQeqP1CHg7/8ABjNnwr+wiVNA7P7ZdJIOMK9ixjcuUOm3HyubA1Rr6M4gDoRehv8AUscRUYemXuIy9SsS0SpUqX5+grXgBb9dxM5LY8NrX/ZjY+wxn4JStra7fo1KZ6lSpUd/Vr+Kwi4cEMdzBpTwd+3EqL2sw+L3+pgxcpxe+IqEVXK5Wa/hZFDPO4oOcTQvDuCKExxGjo4jbTMy1WIq7z0SkWiMsWypUqsSgXipakvcvO2CG8wTFgQsyxSNvMAL3L5NNRMuWLYc7eWZQdxctuolWB1HHbHdMpeX0ROelhQt1HYNnbEnw0YE6kBHbuynmW2s6+AiajV04DDwP7ixyGWR4lpQYaqFVUWl4i7UETmaFRNJis0MM+CXWYQUguhXMwqNbYtMB2arzLxALmMYBF7cVwSsByMaTMZOAXcvUGdgjBVyGi2YIzcG7hQswhoCHmS0i78s5gsdQeorVhZMYlIVrdinxN+oFrT3cyYC0bt9xbzLoeYgCqHMPmWkBVy2/tDqs8yVRzALm7XrxF50xr24we5jCiK3TxFZO6xs8wxsb2KZ1qArEBiCrVXJUd5JUBkFUGfgjAVaJ9lAw8jySAPlilqOrBRdbrhhs9RKnOBTT7l09zyfmD1Zqgo+WsRgH0j+ma4NNN+7mmTyH9xRhT2C/pIf7BfosQlU9Ufshzo+F/dRQst9r9MK8h7yf1Oz2A/ZHCqfLX7hNBcBX8xnU6Q9B3MQSyzzl6mafqlH2yhPL7TxUQODcvzKlRIn0V19GVKjF4MvEVLvnwHa8fuB3JsUs7p/uK1BgGPWczlZ8sHolVKlRj9LnZl4gWnHMFWZe4znczBrF/ETdB7gpbuHPvcM8QxDuHWEQaPlm1wBlhPCWH9wAIt1KrfFTMrJ3Bp95jmrBW4UeYzqDKqG0S/iBaDREvLrZBDnMoArGoU7vzOU+IJKd7ihTVDBMu1sT5cuo6CxKVoqkbikJ8cxFXmxcelgKi0aU6liMroyzgQmN3qGjiziZ/FKeNSsAUHxeI0A0BrnmNmAEUwE9p06WVsTiuF8wAaqgr6g0AxItgYwjCj2jIHUBFe5XVcWtFHUrxptd3xiEpOORj1AHhSrJ94oSEiU1rEpUctZVaqGXBgOS92wSNiC8PVwpFuhDAqi6ExRy3LBZZLNOswwlCllFVipmVyTo+8FJcuwL9xlauloBmqiu1WzlhxKHcClYXC5eAtadtwGxC1dGIMatIyrVOYzwRAu093AmClixxSRhBk4mfLD3xVByci9wpdaAF8lZeMWqKHdjzHOe6FcvV437jlAMPCdJDYX6tkDxf6nZes5usV/qAAT8razdVxCCPYqqrt4iSsrIWcupjmtKujoKcQpLva2t0W3l5qNbN0s1T3WWMO2qgu0N/MqyBgrSDHM8ZfHMxMJAV2PMpz9r6mEXpl1BlkI13hgVmqwa3V1m8z9qAf2QTo8C/pl7Knn9C4U4fvH7JSrAvI/uL3PQ/pjRn2g/qDtJvzj9xfzKyFsmfUdiIRS4mGfz9CDcT/VqR4Dc1iAL8SNej7ytx6cF7rUEHTh2vl5lEtXUXzrglVElSjmLx+IxEVO3V+4l3ZeaFtTEINAcYwR6pQq8UXGmeGCuBejX/jLCN12RDwdwNl0NhmCUwMPCTPJo1cIoZ6uCJWID5vMOkTaUKmH2gGLvcp4UHLmUghFAIwa+LfL6ltmOZdb5cVEDUQity7ePDDTGXUMAbO12CWEWIUQbaqvFM5T/uNWDPmCnAF6W0+X8GZWpC14hOVIupnuaZZyxAtoyKprGY0JQ5WUTL4SFVLY1mYoKMDtClMhsBd83LkWMIPuLokLtRZZ4WjxBfs4VnywrrgwIRw+4IR4OZhNjzmBpsy+IAzU3ncvtLVRANQpYWIsJ3lzFsacDfhgMCgGqHg+IgHyFsvULjtwDneB1MogRN2LKCpVnNtkfFTGq1SV86goVYOQKxdxvgcAab35iMJEybq+iZJ4BOTr1CEESg4V7uJWyGxK8lxh2gBqmireIAREpuy4wTIC4Q0PeIKXTVpaXxGOirUNvH5imFS0cDd+5ogl0W2ti7hwvFpqvAuyFTWMplya4YJnArGjaLAW/gOC/TGN1xMUXYlaYJhKS1b3mYGRLAU2F/6heb0rINdJAWZWhkrdJzMlrlOaXumWLpo8N2sCha2pNmYJAKHK1XV9E0QUkctvEc0riij3R5hcut28VEo9QHmQKoXXB2eoSs7eYzcsbYVxK0xNMAQCu2NFSzXhqr+ZhJYrXjL7gyyrJYhQUfMJLdSdAtacGZemw2JSjW7nWn2uF5qWgVFda8TgGQpEL40xKodf/GZTdxSZfsjvRuwGPhjYBPFf7gSvRP8Asihy8CD+yKVj7p/phKcVd8C3LHRuzBX5/ohxXglHkBcTKmJQn5GVlgvsP6iTQU7agW0ZZY6hB1PLH7lY6j0a7jRgyynz8TD6BFKJV4Z82BhFB6zKWZFbVb4gXrHgRSKXvMzTaAaQOHzKj2yw2F3/AHDLTDzWuCVABTwDyCn3aht2Cqo/hErFZtHyKSg5EDloP76jBpzxGSZILXxbAI9o5iGufTgAj+5gCq3TmWbw7hTT1W6C4V7OLghhcF3Qv9yy0xdLxBfvxtE5MDJ6BhToVbnEdIhpMgGsbQUQDW7XXiXBdktIk93Ksp2ebGtP9J4mQZcDuAAR3RzcNyXpGpdbXcFxeTRKKXZ+oRsYJdS5DQ5zDv2KOr9R5aVt5jMg8goDxCCVKF7erg545q7II+VqAT5CkaTYW+5gvYXRz8yxQKBRcEeTl4gHQoseMQoC5KtgVKovU8KuV14xpqccZK5amsXF/wBy6XsZUP8AcK5mBqEyYioD5EmIpd9KzEOlHS9DmOOCyt3fFzEKtDCd23FihwyBmKidyK6WHR/uYkGAV1zOeYOBOK7zuHoSVjQrd+e4VwwtAqm2+NyoRyeV1fUwoPY3ZnFu4rRQ7gt17ZtcuZSlUcY/Ec3TRmOXcCzZcWBfVRhZKWmaKjpM4MCcBzuJkyKptOGCQytHCuy/3LxspkDoDx7grXFdC9jACoavFVmPuDF7GACiIoDA1gwz+oYAi8ukyYPUbNFhlloPWIlghuJeV3GUnSXI3lfsJC0QBP8AiiWs7stVbQLvjEqI2AWzJbZKNVMo4aW/ibK6guxAquAqaFNK7VkliLtBadm/FSutXE6YyYgLiIZQFmoTdujQrPtlVHihWWCs/MDdOiQa4LrRKdOqXm1mc8aiv3EC2lU613EbBcADJdX4gAWJQLYXTEOoEqs08BgzEK8iikBAXqXAMpQIUNHMKhbQoO8VFBUoAnXnzLGwpS0NXVvqaOeFTbUxUfOi9de4GkGwEfxK1+AX9xS9/F1+xBX6R/plSkvaJEiF5RH7Jcsw8CWUuNHFVRcqBBczIyK9RS1YsHHnIRirQmCw0BcxMSyALunlncBRkKEIU2noiizQnatxrdTJqLAIadfaEV6SIKYgAWJ7EEBEfxAWrkZCsUd2GI6MFCvtMyAo4Rv9x4L45RCz5X7TGwWjECLs4MfZ5lhHAIoZrtwQZBEjpF3QmxJRyVhNNbQHGYBmhE0m991FUBe8rYwtW5HYXJ5uIsBRoqtdNvYqJW7QfY3+oa3vm4q0GechDL6aPaWVMsAA91aswQjkOVc6JkfPzeR8k0mcyjPZ+JlYiCZ8SrR8/Esofwg1i1ajtNiMkyEMOGEoZyXUoZOy6hUvKYxhZaEbYcxW0saLggKLMU7+Jm3s8QJR3ggpRuDV15uXFWbzLmFZM1MpW+Ccht1LKMhoPEaoaZWCWHtTLjvH4mcR5u5QVXgwsqy+jERKbyQayUq+Ya9k2nJha7cD3y5lFYti8VF3KtLoTFLgUui7l1mAN8XmojFC7Mj+JcFePlZb+go+HG4eWITy9yxpUJHAK8yuCCm1Rv5iFmgBQ+b/ADKVZI8Ktu3G5pUa6NBABRlf1AfUIUGgsduJngsEWaW3Tj8y+qUAzFI3o8RHK2vW0313b46lNNEVvpGCmY03armniMqmhUHaMBZoaRfLfXuOWqOG0YEdzEgTqhVCvErnR/TEwEAxQ4cRhjYlj2Sn/ZolUTODVMFSm4WLWUK0wEcZBAQpeCA6EXKuqqppcYF2w5itBDApLq6v4hXjBCiYui5kPW1OXlqLlVkRQmLt9SqYuVWTJl+JliUsWxSH2gicFDihun7QY22IOBPsEBoUvLRV4U1ANR3YEVbSGCOiKBV1tV8V9pgjYMYrho3v9TDwD5WBZYcNwY5wWMIAB0f+pWdhrQogDxqDy+QWs1F9vczFjqFg5GMbhWmUm00Jb5x9oyBCsigavqUxq6FG2sFSxCzCLLZRhZhMHCFF0en7ykOIXjaBdd1GVnqBRvjH7j4IVA9v9QBZhuYSU1fBAbR+ELtQ3CKfAMAG9NH4IMtDCWtJjHWJYNAqOcL3zEIZs/PSpmKU1gMvJeviYa2qIsrk5+IOnWCU3d1iAaoILvFjcs4WADsDA7hiXGkF1V3xMjLDRlWsdQMcAysF5XlW33K5X0YM89YglrwLAeZ0QQii4q7UI54uAkDuUgyh3qIRRJFXIDwj+YYdkbG6AvYJ4isghV1oH4hBAuzzU+Q+9SlcjZIKjwZV5olEK8+ArL5FFuuBzSFb19NlpRrRQaiMtSQUUJ+XlgnASrIOcnh+Vx8sN6IGkAayN0JzAwJSOR3AFiuLipWsIbSg197mTl8og7OSZMhOSZqOMZiaTa+YRqm+YiHMHhl3ClDwyt8KS+hHZHlntjwoHcuBuqyMTZtfvUwXyMVLg2KFhCobwb8dRsSsreJaBunbcNBY+zMD0YfMCK6wviWABZuIBQ6O4nLY0+IDRbV4DiLasixLWWMwWE0vEVM1JzuZa4r9xi+QeeMRyTtlk8ShN0bWtRwCnkzZ5gcXECygOZawwDgoPtMBRfA9u4w8gUTdwqV9j3B7K3Sn2g7apW7y/aPBW04dB2rKndGx9AcRSnCpDVbhcrxaLgRIEUKrvFmJVyLaULN5re4Gd8J+F4gk8ya66TkiSjNgoXLlhjICq2sK8UxEJLQjjGFhnoMn4lxhUoqvau4wdXTwkBzRX9wlHrNERAXZWtnwRPFg2UcVvjnzLorF3wJZQXvLGEnRYu5VrhqLGugbC7Kc8TlfxT0HjUYFhBCsFAY7b8+oBEpdZd8lqoo5gEGSlG7t2cQ3bAYHg0zDyUNht3eJZrIZFFmKd4ji0JBy7aDO6YqYhirFhQfqMqXwwprFYxEYmQUFppozr4l3ZMM8LqvfzDXXXRF4RMGMRGQ6utGRvu+viAOlBBd4aCVe+CBpHOkyQmq5BaqtdGqhVW0o4AbH7YiY4QErMzbC4pXVhWUgoC0QKnAG3HObj3m1rNsF3nOJbWWwBLjKuOJakjLUNFoXALzRaMd6htbwQoxVecuYoGypC0wAcncBuMcsrxTXUbeHlpVaGXLAU2ZTBaRuwuRaitb9+4bAvYFoq1T4lWzREGC6EyovmOnWrALRMIHB+5XEqG+71NX73KUJkbUbLY34IIhmt24tyVdZgUlbBVEaCNQIUGygzVc4+Yhqw2CgEcinDGyUxTALM8AKfM3glHTkUe2XoBQtgqg8dwEaJDgL1rNXXxEACP0UbBvHh+8EKYJmxhvjqvUuVV1VQGFHGJSpQDqAROC6zweY0dUkyoGuRgPvBvKCBvBm6uwGswcLWqzZbVYKcEBu6q1sKNfeUOKFKVa/iDU7pWDAHOQdQTVQaFos2OTovKR9htWtjsL1frBHpZhwbZ+LfiKHJoMqKaPUUClrVVpKArcPuftdRCq7cb/Ec2ZDorD6sPiJTi8q4YjS8sY7lXAIXX6glN6Dw3EUotdviVAMnMx1Yt8JSvUSW8uX/sYcc3iYRTWB/ERbQlhQWhWpQAtEKuxaB+YCl7OftEihdNNZ8uo9bgeUJOU6hmDn7almiggOLq8wEwAYajX367grhqqTyJubaFoC5fMsOwHW63uWqLK6xFK6N2jNYADhNYxKbEG3iNUKCWnvbAODSvrEMZw6sqoteGlzEycWhKVOaDMzkMnEZeIbB4g0Q0ibotyyqCWIDYDj8feJVcKAxKU3RTf2lYukZo/uEKKqvB1uIVIR51b4glhA9A4seGOSRU5K8eyJ7KvLGd8Mp6eh7PTkjWYTMCuGMcyY/cHQkFd82QHUYC0FdYgIggXrkmQhLhU1a1x1M6CxKLiD6lwqsscKbX1iIowCoCiW1uGwvULtxkdwJzbQilrQGCVYIVAKol2MEMooWiti0PDUp0sGVGtc5gKAmhK7sJrGoFU9ADQimOAWKdaQDgFFG8XnuIhCsEB3kdHGZzAAagjat+IEnFpKgwhl0fEtwKIqmbWzWCVrDJ1MphaxeJbsBpaLKl41MinAg7QjWveZcylQbaKBf+3Gvvl5Ytz4mUggLMG35xFUxvArst/5gVlDeoGqWrmEIMnJBlRdRaZSJMMW4ZQTgODRQNW1Dq+NEXtM+rcTZQl70ukW8MdNh3C97GrTMU4oypi6QisGhS1OcRjZMrgHFt6hEuWFC0tJfGZoXFgDi07qAXgRzo4x4xBDuuEGsYh+BGC0oDLRpgV1usQBoBOMwoDCSWSaH+5brs4gU0kQSQoCq7B1GdUAwBulZ+0IBatYM9usSwreK4xJZcVmvqpAbSjvXhlhLkAuyn3xqDqOcmABSvjxmNIHQgsChF6WRDioXZWgCz5xDb0WSLZWZUmW0ZLB4VzLP2kHQETNOolIqDak4DzywkwW+DQPQmJlcHrMdI6uhO5VxbmihSrBcPqVtnENAFUunLQQD44QsUT0sY7aImKmzeKyKxvBzDIEvlKgn8m8GNELgPkbF4sDGf8AUIitFPajwstV3KiKFCG20GNRVEjRm8bWzhmsDiGw3xansIevzCBHohmumuQ9tHcKIFRY8fMydrZ8O4hoUQLWLzX6i2FE0O+ZY8hm9YjfvTX9wD8mmsxy1mhOWWkuhscHcYJXSvEecOBXuO54YwmQvDocTBbsZ+MwN9BV/iGa0NiwHCSqPHUUMmXJGLoVLQbaOyrgXElqEVRLHC8x4aaw53sluNABW6r56+8yt5NW74igVN4szn3GTJaqrggCBZ47+81FStC/uM6zK0q6aaZ1It+S+fvCpno5Nm8w/FIHOqL9/qJMh0RNHBeu4e1TRcsnULqFMNILmcoBi3MxKKkAIqsXqUANEi7Q6m6RC0KU6O5VlRFtX8EWUAiU9niUF2NW2+agbuYFrhf6iUgG8hcSS1eDTFRU8a60G9fMTExT4D2VpGKzLvJ4IcM1LFQOGmo4ESpVeLuOgaBQD13G+NZb3WBPzA0rSlvBvcOBPgd97ZZoyxabuHgim1NoMBo5BxUpctobo8yxSeBTbBa1XGe3gJnZZC2kquKhRFmdb63GgRcA01W7jaUEVRzxuMdhWZfcCM1QVXBQ+YUCI0AKNbuY5mLngCCuLhZj6spReaNXLwkitDSlGNcS1ypC3ZoW39RyLajENq64xxKpI2eAymB8nzMDjyZStYeOepckVIdZ8N4GYnxWlYoYPtB9A5ZY3ZR4hC7xQIKQ24L8QCFGIBnSj1/9iIEWJgOVMf6gABl5h21du/FREbBAYXW+7lAi2iFa2itfHqXuzh0AK0YlqzoLzWcBUXvaAbAN0eHxD03VaAOzG3xFAYW9gLQD9xdJfzy2A551M+7lSW2sd81BYhUBELzU5xMs2jihLqxxKCxYqKNFa9cw3kxpQOdeoVlRQKKBb9bggFISboRt7u5gqJUw0Gd4rPvUSAXALWsrSbyRCgwwtqsPsxRx0pFFUoMEIWjIQAsADF/EyhfMSAAcmowogKrcwUviBBDCrZG1cbtJWFIHI3nhuAmFTb4G0OGcw2uTFUG2j7/iWgAtXEAKB2ftGhrGhoJECmeb8TUGgt6LGw0Gr7YUqXalTYFaa1gaiaymQThYJnLHcYjBXVHWdZ7mR/jYVQsKBTnVs0RC8Bgq+Qhb2pIEFB9NPLjzLpxdpyE7aOKN1KQ9bKhQN+1O7qERKSDUIuA5vLjC7bxBMaDBYdADVwsDg1oYsT+/MxnV+gKegp967gAIyJc1bxM4pC0lXiyKFTA1AhTba7LoJlMzgyPUqIEGWPYbcjfNxqAxxTYA9llPpAKnOcfMMpdFDVt4lkwtsOOD+/TLIGwfU3HHXmIAFlKxhoFRRsKxarxBbBwcbzTvcIVGDGawF0NRTnCxgVMtYus+I2K615WXUXuBy6vqIFp4FoY5XyCx9szRbFTSGyzPxEJe8LujdxVQUt9b/ohblLBxBXgtqIQRoyxQS3BsfSXRhD3w/EsAcaU6uAHigGvtBDChlqqfMSlDHNwQNn+3EFJa2bSAqlC4IIzqUK9RGBKsVjEFaShp3vmK3y34xxM9hwDWdcxFQK8qNUxTTsgE/MT5Ipaq4TVm1e6anECxlrdywQa3vEOmOAStWSafD/ib1KKO/wAQF0SuH/SCKGqaORzBAZXnQeoKqXNZ5zzF5OQrZMwy8KHx1B3C6oe7dQCgovQbR7j/ACVYTZK1FQURrPOamaqnKr+5dwBoNMAGQzbnMWiqtT65hC0uh5rOIBZxaFas43KNVrq/6YRGzmLQ8VAMNKbVV73LOpo4F5H7RSqYVSKyA9QSoyiFs7FnY0sB7r4mZttjZSzHGiYF63vIigmv1MqhVc5WAPJ3fxHr2C8gpzjX6lVzdG/GMt8fiZqC4AZxZeVg1irka62XES0sw2XmmBKHOSWF+z7sDDlAGbFPPmALANZBV1RovUp4FUvPXHGOIqUBVukaGnUtTezCy0pKzibISWUACWp6iAg1pXotrmWTAyEcle9QjygA1dlO6MEvG0FUS7v/AMShllEKetY3c5h8djFL5z94egQd6rsr0b5jdOgajjBw1M9LJKCiOA5jTBLbVgMjNUZ9wOCI4AcAGFxFZO2ko23TtzxL0FA6F4u3FF5MwSJxZ4Kz6ishsUEdgowPxDrrG+osAbXqDYVCloraul/MzgoVDSlD0xxmIBznUXSIcFzLRpi4bwH2/wCYNMKIKrd6SsdkGEQSveTNx+5vWgoYF5LP9ksUQCFotqsjZu4fE9tdKRZgD5c7xHmzAwAVEeAGGXrp3dHCMlUcHaKe3eFYVKWXDzjMubcV2UgoVnFeA9TlS06igs5C1wF3DKaUAprAzfCS+T0taFpt7zCWEgRUTK+9kaTD2ThMemedSSq0AbsXaxlJIAxzgMYuzGiOSbtQLpb4sw+IPjOlziOzO5hLkc70GXcqgEJkd1nqxiORQjsMbi4pAJQW2194gW2LHHNRpeijA4Z2grfHFRv5mZVvD91n1HoLAtju7OdY6jZFLWDy3DKnB+c1HpsOKus1qaUNN/7iXDNGO2Dd4v8A5gtbVdp4aqJQ4Mf+sUYCxYv1HDC2yOyWJbdYqX2z1BSFtK/1EptA9c3MpVCb/MQq7aXt5gXS7ykuMGu3DB1Ba8QToLcsQKRcBkqYUccbzGV2WaGjvDGIVta2TzECamweWtR26AarVXiMB831FVkRgdOovWlreOGAXZq/9ywYBMnzLkN0pSVdONVzxA0yGnrsnJKQMF0fEFVqHF1+ZbTjxAL1sw8zCXnXXzPSkKT5czW6WDLb5hrs03X3gIcrs9e49FWRUuizd0OCtVGvnqBZVuBaZWmpWS9wRs2eL5hsw+H3gKDK15ojKcHKYd8GIUZo0HUs7ZsFKT7wNOM+aw6g68F0NJ86gpvZLp9MwA2me3XcGhAMb/sgpbFVOj4qPQF668tRhcw2jmVQVhNw0wt6cTeCpyp01mIELCcLWAj15XCnatMB4mB5XYp1moq1rSgkKDocxhDVRsWi0dwUyBqGjZre4/KLliNUom/mYysN5FYWPeoicHgq0qmtqR7oeJjAt/eUC3LK7UV5MsWVVQZUW18vmFoKsJoosKd8blihDZajTSnGWIUp0Fh1Wc27hXSaSUe8vHmo5ykJnZSoGd+sy71/K4UukrNc8cEzZqXBuW6xzCRvhuWUyb5I13KIUgiY4/UEMTQgwqg4xlj7kDJRVdDSIdjG5YpfQbW2pL2ZmJ0+mjCU7qEepoihcUNZDiKhyKCqUneq85nM74Qgzh9KxqEtLJgVtDcBBANDdsps5vJ4I2ZQ11hXacUk5wsUzkWIXgujiPXIRqALWxWGiXzraKGAr3/7Cg5oLgUFc0c8kxPkM4UUtDJ8kuVLgLBOgVc4Ne+4LwoWUF+DtTEuuiUttVthZka89MQ7IgBO0S1OGcvTRQNl/QeZYM7TZcPJ50QcNLSCirrfDeGH0SpJDTDd35Vx1CIBuGW1AatM1qsbh9Yhb4ABxp8qiD31QpLpXY6LvmWJVciyKsy4bauCglEHFKIi0jXiVqWlL2NirdOIi2vVpRV5iUGbnmoJ8ie4BEq6q0XVvOItZngiYEser9OZqOkAsAwqbCi+4KTKhsceyUG3AZcm2lrFH9wC4raO3mJtGniUVR7GOAHN05gegO4gma+PMGKFGC8ysSyFOT1DO1lwaOoKauxs/wBxBqsOO8z7ga9TK0uwoO/iW65oOkoVVa/UAC8YIij7XX2hLL0y6ZUrG9QTJVsN1UQjdhy7j4LHT0xyAwFMc1cRnOm3fmUNHGnV+JljdY7o6mZckx3ersipcVI4vxFEmpanJnSSkdtUlnIwNAWVXnEFRRRjB/UoAdYTnzDIHexOH+54yFytMO9QIDkcNXiAhWBmKC3217ljh/Q8RBLu3YdEQsQ8sS4FlhK66CVXsVPf3gK6ib50RJqhRReW/wCoNE9U2iUINDTKjlNGeZVpeuY9ZRkeINgE2oxRSsHJ5gQjjk8Q2FHSRRbVy6IVcWCj0zIq2G0XHqBZYGcXmFAVoLmPqzLhOHcpRQefWmbrXqGiAsWld0rnTCADaQAZseFgc5mJthrGooQalgd4v2sRTevYLDm6glu8YFMAt6lQs00POK43VTNyXMkVLKeIBymABMi0P/dRyjnwAR1eMsGKOBVKFAC2L/8AZfaACoQqtMftCII2gacr31EctLDLIgzrrmMvWUQVLSnn+4GX3VEF6Xnwdy1gREtSrU4DxAZwmCADaWW2DXqWWbDUhUVDGD5jYODfB2Vvx3DnTZNq0CupXZyQeocPD6gqiRlpZ/LnzHoopW02hpV48y0XSBUNuLdYzGGZ7KmtmLeY2ZRVlJWVNsQ4LsgNtAUGrPymU5sgZI1jOa9TOx1a1NKW8y29RXQWLM7/AO6iBttUzjBKxdRk0LHQpsOFTGMbrKAYVm14iQiRTBU8jfzqN0VRTkYt4Kwv3BQLaKLaDXRcBJKyQMDa9KxzKZKCDbJLOOw4lLpNVWRBbELBpCGhNNbrB+ZTlAVaCKmzyYlqIzBYxo5y+6ZxUUCi6QDKUQi7DTIBeBcGK+5EBXVFeALN3s53EpFY1JQt8OB5xAx5wSRcFeLOO8mp02hY5zfFcG9S0xI5ooKGgWoIFpAWleK82B4gNsB7bJBXIqZlNwSbAyVLU0HpxAtL3HhAC8Cd51HHiKFhVwHBK7peoNOCs2b7/cFrGGvvX9xVmD3hbtCkQC0XYEczEXsMqfFEDBa5PUvWALuU4Dec9axKw8rTxKweVJm4NxpdcIguhmWIOCWTcmDh/MoHFViZ7M9/uMCg3ZWfiJFZVWDPepQTbt+YDVMPJqNtS6cSxhbHKoqi7/dwpmQAj3KnjPPlArGAuwiAumQi2+st1VzBThbzzUBDfK/+wWNAgK4IhkLblS1GCmZo7HTXtgHExtv8zIl0Ypz+pkWCbq+YhL0/vctd7I/VywFETD3HrdUO4VvNKHm9y7gvxqNncDFamINCemJect0/EbX5OY8L8lcSiF3nP75lUHdlpKc7YLtXTeOnqWF8v6mWbTeSGZOLznPjEDyCs3cSrZEBGIAV4EAd4puIwcC1d5qB3qGh1E2uFXjEM0FGWFc5jNZtp9EaAu/i0S9aWI1xDWyXbHdxSi52jS8eYSIkIYGcPcESgoXgyxnZJFGrMxKI2y7VRi4YCgRri3EC4CQtzgGo25aDayaoDBxXlsgaUtQjMLVbRota8xlypoaRVKcxkcGgFmdxNxkq+TV6jHSL6OyiIM5oZuuYQoMjZwxmClKdUmYB4sMVw6gCgq865zHqdHVqpbHzDIGzC80Eao20LQ25ruNv2mtkq+JkM2duc3OgLZ6zDQhQu6O0LYi9S5g1bj1MvkBVyGJ6wTyk6sWVx6lUYa1bdy4CEgmBogBFgC7G2ZxVdDaXa9Xn3FOq5afd78wlCNA7K4fExsYRB6b/AOiZuS3bu6Rrpsme7y/LABgBFm6tMAYoHQ4D1ll34qBRVqvV5lkrhbWSmHKALBTTWuCEQbANqL49SycyDe0Sn4iDQg1s1g/UMkEoWWWj94eTqwDN2ush9iAqDxhR1ZztghESAMAAEQ1QrVCd+r/UPB6cHAVfdQmFVwGbMzYHJTfuAoo2/uA4dn7jKKqu4RyOGYqbBCWi3z7gKwMMx1DJ6sSZtTInX/qWm3MbleS4C2s8viYL/wBzH8rAKAjbZ/4xBs7v+oBnWb/qJ58RUEbjARbom04qNTfAwgVK9TFV3Asoupmzu5gkxYifm/qIBBi4OncI3HX6gGiYx+5kL5c+cQiFY/smLm7iQq/8IgumczItxE2XnP6hG85T9c1lpXFxoEaV4jgTSQVLN5bjhhqZC5zc3OFzf9RwBq4BuNQ1FvNMAaHP9T//2Q=="
    st.markdown(
        "<figure style='margin:0 0 18px 0;'>"
        f"<img src='data:image/jpeg;base64,{_FS_PHOTO}' alt='Ground-mounted CdTe thin-film solar modules' "
        "style='width:100%;height:280px;object-fit:cover;object-position:center 62%;border-radius:12px;display:block;'/>"
        "<figcaption style='font-size:12px;color:#555;margin-top:6px;text-align:right;'>"
        "CdTe thin-film solar modules. Photo: First Solar, Inc. "
        "(<a href='https://www.firstsolar.com/Technology/CadTel' target='_blank' style='color:#2e7d32;'>firstsolar.com/Technology/CadTel</a>)"
        "</figcaption></figure>",
        unsafe_allow_html=True,
    )

    col_a, col_b = st.columns([1.2, 1])

    with col_a:
        st.markdown(
            "<h1 style='color:#1b5e20;font-size:32px;margin-bottom:4px;'>"
            "Critical Materials for Solar: The Tellurium Case</h1>"
            "<h3 style='color:#388e3c;font-weight:400;margin-top:0;'>"
            "Supply, demand, and circular economy of tellurium in CdTe panels</h3>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<p style='font-size:15px;line-height:1.8;'>"
            "This dashboard lets you explore how <b>Tellurium (Te)</b> — a critical material "
            "used in <b>CdTe solar panels</b> — is supplied and demanded. You will calculate "
            "the supply–demand gap and see how <b>Circular Economy</b> strategies can help "
            "close it.</p>",
            unsafe_allow_html=True,
        )

        st.markdown("<h3>What you will learn</h3>", unsafe_allow_html=True)
        steps = [
            ("1", "Why Tellurium is a critical material"),
            ("2", "What makes it a Hitchhiker resource (Cu &amp; Ni hosts)"),
            ("3", "How supply comes from direct mining and copper by-production"),
            ("4", "How PV demand and non-PV demand are calculated"),
            ("5", "What the supply–demand gap means (surplus vs. shortage)"),
            ("6", "How recycling (Circular Economy) changes the picture"),
        ]
        for num, desc in steps:
            st.markdown(
                f"<div style='display:flex;align-items:flex-start;margin-bottom:8px;'>"
                f"<div style='background:#2e7d32;color:white;border-radius:50%;"
                f"min-width:26px;height:26px;display:flex;align-items:center;"
                f"justify-content:center;font-weight:700;font-size:12px;"
                f"margin-right:10px;margin-top:2px;'>{num}</div>"
                f"<span style='font-size:14px;'>{desc}</span></div>",
                unsafe_allow_html=True,
            )

        info_box("<b>Tip:</b> Complete the pages <i>in order</i> using the sidebar. "
                 "Enter your name on <b>Student Info</b> first.")

    with col_b:
        st.markdown("<h3 style='color:#2e7d32;'>Linear vs. Circular Economy</h3>", unsafe_allow_html=True)
        st.markdown(
            "<div style='text-align:center;'>"
            "<img src=\'data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/6xaJSlACEQAAAAEAABZ/anVtYgAAAB5qdW1kYzJwYQARABCAAACqADibcQNjMnBhAAAAFllqdW1iAAAAR2p1bWRjMm1hABEAEIAAAKoAOJtxA3VybjpjMnBhOjc1ZWI0MjI5LTk3MTItNGMxNC1iZWE0LWQ5ZTIwMTg4MzVmMwAAAAOUanVtYgAAAClqdW1kYzJhcwARABCAAACqADibcQNjMnBhLmFzc2VydGlvbnMAAAAAuWp1bWIAAABEanVtZGNib3IAEQAQgAAAqgA4m3ETYzJwYS5pbmdyZWRpZW50LnYzAAAAABhjMnNob9ugXoaRWenKtqpDTFKqfAAAAG1jYm9yo2lkYzpmb3JtYXRqaW1hZ2UvanBlZ2ppbnN0YW5jZUlEeCx4bXA6aWlkOmQyMzZjZDlmLWJhOWMtNDhhZS05MDhhLTEzMzY5ZDczZTliNGxyZWxhdGlvbnNoaXBocGFyZW50T2YAAAHianVtYgAAAEFqdW1kY2JvcgARABCAAACqADibcRNjMnBhLmFjdGlvbnMudjIAAAAAGGMyc2i4yJrWEno8SyvSjQLXhN+EAAABmWNib3KiZ2FjdGlvbnOComZhY3Rpb25rYzJwYS5vcGVuZWRqcGFyYW1ldGVyc6FraW5ncmVkaWVudHOBomN1cmx4LXNlbGYjanVtYmY9YzJwYS5hc3NlcnRpb25zL2MycGEuaW5ncmVkaWVudC52M2RoYXNoWCDw4th+dmL4vjdiYhn2vYPRCE369X1aN7DSaijIZLAWwKRmYWN0aW9ueB1jb20uYW50aHJvcGljLmNsYXVkZS5wcm92aWRlZGpwYXJhbWV0ZXJzoXgfY29tLmFudGhyb3BpYy5vcmlnaW4tY29uZmlkZW5jZWd1bmtub3dua2Rlc2NyaXB0aW9ueGZDbGF1ZGUgcHJvdmlkZWQgdGhpcyBmaWxlIGF0IHRoZSByZXF1ZXN0IG9mIGEgdXNlciBhbmQgbWF5IGhhdmUgY3JlYXRlZCBvciBtb2RpZmllZCB0aGUgZmlsZSBjb250ZW50cy5tc29mdHdhcmVBZ2VudKFkbmFtZWZDbGF1ZGVyYWxsQWN0aW9uc0luY2x1ZGVk9QAAAMhqdW1iAAAAQGp1bWRjYm9yABEAEIAAAKoAOJtxE2MycGEuaGFzaC5kYXRhAAAAABhjMnNo3ei824NMm/QMgUKWDP1DHwAAAIBjYm9ypWNhbGdmc2hhMjU2Y3BhZE4AAAAAAAAAAAAAAAAAAGRoYXNoWCDLUigVnZPFSjou5stXri2qksYPPkWyghbgfu35k9LWvmRuYW1lbmp1bWJmIG1hbmlmZXN0amV4Y2x1c2lvbnOBomVzdGFydBRmbGVuZ3RoGRaLAAACPmp1bWIAAAAnanVtZGMyY2wAEQAQgAAAqgA4m3EDYzJwYS5jbGFpbS52MgAAAAIPY2JvcqVjYWxnZnNoYTI1NmlzaWduYXR1cmV4TXNlbGYjanVtYmY9L2MycGEvdXJuOmMycGE6NzVlYjQyMjktOTcxMi00YzE0LWJlYTQtZDllMjAxODgzNWYzL2MycGEuc2lnbmF0dXJlamluc3RhbmNlSUR4LHhtcDppaWQ6MTc1OWY5OTctNjkzYi00MmEyLWI1YmUtY2EzYTQxZjVjYTkycmNyZWF0ZWRfYXNzZXJ0aW9uc4OiY3VybHgtc2VsZiNqdW1iZj1jMnBhLmFzc2VydGlvbnMvYzJwYS5pbmdyZWRpZW50LnYzZGhhc2hYIPDi2H52Yvi+N2JiGfa9g9EITfr1fVo3sNJqKMhksBbAomN1cmx4KnNlbGYjanVtYmY9YzJwYS5hc3NlcnRpb25zL2MycGEuYWN0aW9ucy52MmRoYXNoWCCV4YwkWxdhX1BPYwNtPawXXFJI7MYsuxtHsg9YnPATfqJjdXJseClzZWxmI2p1bWJmPWMycGEuYXNzZXJ0aW9ucy9jMnBhLmhhc2guZGF0YWRoYXNoWCBz6zdRIBOUbcuSVsGyAyro72UpY/48fth2Lbe3kPuCLnRjbGFpbV9nZW5lcmF0b3JfaW5mb6NkbmFtZW9BbnRocm9waWMgRmlsZXNndmVyc2lvbmUxLjAuMGtzcGVjVmVyc2lvbmUyLjQuMAAAEDhqdW1iAAAAKGp1bWRjMmNzABEAEIAAAKoAOJtxA2MycGEuc2lnbmF0dXJlAAAAEAhjYm9y0oRZAhKiASYYIVkCCjCCAgYwggGNoAMCAQICFEDloAruwjnQvriD+gZCBT1nVRMAMAoGCCqGSM49BAMDMEkxFzAVBgNVBAoTDkFudGhyb3BpYywgUEJDMS4wLAYDVQQDEyVBbnRocm9waWMgQ29udGVudCBDcmVkZW50aWFscyBSb290IENBMB4XDTI2MDgwNzE4NDM1NloXDTI4MDgwNjE5NDM1NlowRDEXMBUGA1UEChMOQW50aHJvcGljLCBQQkMxKTAnBgNVBAMTIEFudGhyb3BpYyBDbGF1ZGUgQ29udGVudCBTaWduaW5nMFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEmHoKa8tQGAUU1TS9QqU5W0Tp2N3XsvlK7BfQt6YWKwEzd2R3/dzKPEUDdCjlLjp9fT+KFjRVnuZ9v0oXvTe3k6NYMFYwDgYDVR0PAQH/BAQDAgeAMBUGA1UdJQQOMAwGCisGAQQBg+heAgEwDAYDVR0TAQH/BAIwADAfBgNVHSMEGDAWgBTOUeIEgU5kWyP448TPmj6cwddcwjAKBggqhkjOPQQDAwNnADBkAjAxcx0UngF60stVjs5G4T2eiptsBk5mf9oCtfJPAUBl8qs/PEXa8+gk1/X5QJ2DVcYCMHBfXN31YapiSqYvlIWrDVDJKOvXMl+kkz37Wt0PBI8sw486Mq6JeOhT+lRR4b1HCaFjcGFkWQ2eAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA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qls/PPPPPPPPPPEvv/8A1bzzzzzzz2y0fzz7zzzzzzzzzyuvMfBscLf/AM8888888894770+X8888888/wBPPPPNvPPPPPPPPPK6wV7zSQVf/PPPPPPPPOnOciwKfPPPPPPPssc9PP8AzzzzzzzzzysEFYQkMFX/AM888888888fvNff03888886tQQJQhW8888888888rBBjIjrBB/888888888889//wDxmcfPPMNei0PTCfPPPPPPPPPPKWCl6wxTiPfPPPPPPPPPP9f/AKhv1joG+oW5zx74fzzzzzzzzzzzu65mQ0X/AO88888888888879/hG++++++H88886888888888888r/PPwFc//APPPPPPPPPPPPLEviE9suusuv/evO3PPPPPPPPPPPPK+d8/+u8//ADzzzzzzzzzzzz5UOP2++0dQixcd/wA888888888888rodnTu2i1+88888888888888dCcvcIydOVdc88888888888888u0UMPvet908888888888888888MBuFCT0/88888888888888888cG+//wBij/PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPHe7bPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP/EACsRAQACAgAEBAYDAQEAAAAAAAEAESExEDBBsSBRYXFAgZGh0fBQweFwkP/aAAgBAwEBPxD/AMXzeUB1E28OkgG4K/ixVwXU2HABSuG7+SN3wOxTUZh4FR/nnrAXn75urITu+EEuICrBU3GhHfHdzy7UxWJFXLxC1rr19IzdhwEZJhcHrC8s+XwZpUQ6lMS1fHdzj87EVvhFGyH0rv1iZlSoKrJ+V/MG886nbxVRB08IbRLQjHZzfWceg0w5IqYTBly4oDEu2v5VxBdaIOnFd2Z3MH6uJrjUffzguN0PkecrGFmqu/n0m146enO7UNoXNpVGqHEEfo4mSVwShXNWONsW56gjaOkoNe0wA6mZ2rgtBBXSfeHr0Lfa8RVe7f6iiWX26xlpGvTysJlrTevnLOaVuTXN7XFBKZlcWZDJgBrnJQLYr8DGiVeRwBcq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\' "
            "style=\'width:100%;border-radius:10px;\'/>"
            "<p style=\'font-size:12px;color:#555;margin-top:6px;\'>"
            "Linear Economy: Take → Make → Dispose &nbsp;|&nbsp; Circular Economy: Giving materials new life"
            "</p></div>",
            unsafe_allow_html=True,
        )

    st.markdown(
        "<div style='background:#2e7d32;padding:16px 24px;border-radius:10px;"
        "text-align:center;margin-top:20px;'>"
        "<p style='color:white;font-size:15px;font-weight:700;margin:0;'>"
        "Ready? Select <b>Student Info</b> in the sidebar to begin →</p></div>",
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: Student Info
# ─────────────────────────────────────────────────────────────────────────────
elif page == "👤 Student Info":
    st.header("Student Information", divider="grey")
    info_box("Fill in your details and choose your study period. Press <b>Save</b> to continue.")

    st.subheader("Your details")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input(
            "Your name *",
            value=st.session_state["student_name"],
            help="Enter your full name as it appears on your course roster.",
        )
    with col2:
        sid = st.text_input(
            "Student ID",
            value=st.session_state["student_id"],
            help="Optional — your MSU or course student ID.",
        )

    st.divider()
    st.subheader("Study period")
    col3, col4 = st.columns(2)
    with col3:
        sy = st.number_input(
            "Study start year *",
            min_value=2024,
            max_value=2050,
            step=1,
            value=st.session_state["start_year"],
            help="First year of your analysis (e.g. 2025).",
        )
    with col4:
        ey = st.number_input(
            "Study end year *",
            min_value=2025,
            max_value=2060,
            step=1,
            value=st.session_state["end_year"],
            help="Last year of your analysis. Must be after start year. Keep it short (5–10 yrs) for clarity.",
        )

    st.divider()
    st.markdown("<h3>Key facts about Tellurium (Te)</h3>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Te in 1 MWp CdTe PV", "67 kg/MWp", help="Average material requirement")
    c2.metric("World Te production", "~500 t/yr", help="Approximate global refinery output")
    c3.metric("Te in copper anode", "~110 ppm", help="Typical concentration")
    c4.metric("Non-PV Te demand", "~455 t (2024)", help="Electronics, alloys, etc.")

    info_box("<b>Hitchhiker resource:</b> Te is mainly produced as a <i>byproduct of copper "
             "electrorefining</i> — its supply is tied to copper production, not to Te demand directly.")

    if st.button("Save and continue →"):
        if name.strip() == "":
            st.error("Please enter your name before saving.")
        elif ey <= sy:
            st.error("End year must be greater than start year.")
        else:
            st.session_state["student_name"] = name.strip()
            st.session_state["student_id"] = sid.strip()
            st.session_state["start_year"] = int(sy)
            st.session_state["end_year"] = int(ey)
            st.session_state["calculated"] = False
            go_to_page("🔗 Hitchhiker Concept")

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: Material Supply

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: Hitchhiker Concept
# ─────────────────────────────────────────────────────────────────────────────
elif page == "🔗 Hitchhiker Concept":
    st.header("Hitchhiker Resources", divider="grey")
    info_box(
        "Before calculating supply and demand, it is essential to understand <b>why Tellurium supply "
        "is so constrained</b>. The answer lies in how it occurs in nature."
    )

    # ── Definition ────────────────────────────────────────────────────────────
    st.markdown(
        "<div style='background:#1b5e20;padding:18px 24px;border-radius:10px;margin-bottom:16px;'>"
        "<p style='color:#fff;font-size:16px;font-weight:700;margin:0 0 8px 0;'>"
        "What is a Hitchhiker Resource?</p>"
        "<p style='color:#e8f5e9;font-size:14px;line-height:1.8;margin:0;'>"
        "A <b>hitchhiker (or co-occurring) resource</b> is one whose access may be either "
        "<i>diminished or enhanced</i> by a change in the production of some <b>other commodity</b>. "
        "The hitchhiker element has no primary mine of its own — it "
        "<i>hitches a ride</i> on the production of a host metal."
        "</p></div>",
        unsafe_allow_html=True,
    )

    # ── Two host metals side by side ──────────────────────────────────────────
    st.subheader("The Two Main Hosts of Tellurium")
    st.markdown(
        "<p style='font-size:14px;'>Tellurium occurs naturally bonded with two host metals. "
        "When those metals are refined, Te can be extracted as a byproduct.</p>",
        unsafe_allow_html=True,
    )

    col_cu, col_ni = st.columns(2)

    with col_cu:
        st.markdown(
            "<div style='background:#fff8e1;border:2px solid #f9a825;border-radius:10px;"
            "padding:16px;min-height:280px;'>"
            "<h4 style='color:#e65100;text-align:center;margin:8px 0;'>Copper (Cu)</h4>"
            "<p style='font-size:13px;line-height:1.8;color:#333;'>"
            "<b>Primary host.</b> Copper electrorefining is the <b>dominant source</b> of Te globally. "
            "During refining, copper ore is purified in large electrolytic cells. "
            "Te concentrates in the <i>anode slimes</i> (residue left on the anode), "
            "from which it can be extracted.</p>"
            "<div style='background:#fff3cd;border-radius:6px;padding:8px 12px;margin-top:10px;'>"
            "<p style='font-size:12px;margin:0;color:#856404;'>"
            "Typical Te content: <b>~110 ppm</b> in copper anode<br>"
            "Accounts for <b>~75–80%</b> of world Te supply"
            "</p></div></div>",
            unsafe_allow_html=True,
        )

    with col_ni:
        st.markdown(
            "<div style='background:#e8eaf6;border:2px solid #3949ab;border-radius:10px;"
            "padding:16px;min-height:280px;'>"
            "<h4 style='color:#1a237e;text-align:center;margin:8px 0;'>Nickel (Ni)</h4>"
            "<p style='font-size:13px;line-height:1.8;color:#333;'>"
            "<b>Secondary host.</b> Some nickel ores also contain tellurium. "
            "In regions where nickel sulfide deposits are processed, Te is recovered "
            "as a secondary byproduct. This source is smaller but adds to the "
            "total available supply, especially in Canada and Russia.</p>"
            "<div style='background:#c5cae9;border-radius:6px;padding:8px 12px;margin-top:10px;'>"
            "<p style='font-size:12px;margin:0;color:#1a237e;'>"
            "Notable regions: <b>Canada, Russia, South Africa</b><br>"
            "Accounts for <b>~5–15%</b> of world Te supply"
            "</p></div></div>",
            unsafe_allow_html=True,
        )

    st.divider()

    # ── Consequence diagram ───────────────────────────────────────────────────
    st.subheader("Why This Matters — The Supply Constraint")
    st.markdown(
        "<p style='font-size:14px;'>Because Te is a hitchhiker, its supply is <b>not driven by "
        "Te demand</b> — it is driven by <b>copper and nickel production</b>. "
        "Even if Te demand doubles (e.g. due to more CdTe solar), Te supply cannot "
        "simply be ramped up without producing more copper or nickel first.</p>",
        unsafe_allow_html=True,
    )

    import plotly.graph_objects as _go2

    # Flow diagram on a 0-100 (across) by 0-44 (up) grid, about 10 px per unit vertically.
    # Boxes stretch with the page width; text and arrowheads keep a fixed, readable size.
    # Every arrow runs at the centre height of the boxes it connects, edge to edge.
    _hh_AMBER, _hh_AMBER_TXT = "#f9a825", "#e65100"
    _hh_INDIGO, _hh_INDIGO_TXT = "#3949ab", "#1a237e"
    _hh_GREEN, _hh_GREEN_TXT = "#2e7d32", "#1b5e20"
    _hh_CYAN, _hh_CYAN_TXT = "#00838f", "#006064"
    _hh_RED = "#c62828"

    _fig_hh = _go2.Figure()
    _hh_shapes, _hh_notes = [], []

    def _hh_box(x0, y0, x1, y1, fill, edge, title, sub, txt):
        """Filled box with a bold title and a lighter second line, both centred."""
        _hh_shapes.append(dict(type="rect", x0=x0, y0=y0, x1=x1, y1=y1,
                               fillcolor=fill, line=dict(color=edge, width=2.5)))
        xm, ym = (x0 + x1) / 2, (y0 + y1) / 2
        _hh_notes.append(dict(x=xm, y=ym + 1.6, text=f"<b>{title}</b>", showarrow=False,
                              xref="x", yref="y", font=dict(size=19, color=txt)))
        _hh_notes.append(dict(x=xm, y=ym - 1.7, text=sub, showarrow=False,
                              xref="x", yref="y", font=dict(size=15, color=txt)))

    def _hh_arrow(x_tail, y_tail, x_head, y_head, color, label=None, label_color=None):
        """Thick arrow from tail to head (data coordinates), optional label above the shaft."""
        _hh_notes.append(dict(x=x_head, y=y_head, ax=x_tail, ay=y_tail,
                              xref="x", yref="y", axref="x", ayref="y", text="",
                              showarrow=True, arrowhead=2, arrowsize=1.2, arrowwidth=3.5,
                              arrowcolor=color))
        if label:
            _hh_notes.append(dict(x=(x_tail + x_head) / 2, y=y_tail + 2.3,
                                  text=f"<i>{label}</i>", showarrow=False,
                                  xref="x", yref="y",
                                  font=dict(size=15, color=label_color or color)))

    # Sources (left), the Te supply pool (centre), and the CdTe panels it feeds (right)
    _hh_box(2, 27.5, 26, 38.5, "#ffe082", _hh_AMBER, "Copper Mining", "& Electrorefining", _hh_AMBER_TXT)
    _hh_box(2, 13.5, 26, 24.5, "#c5cae9", _hh_INDIGO, "Nickel Mining", "& Refining", _hh_INDIGO_TXT)
    _hh_box(42, 12, 66, 40, "#a5d6a7", _hh_GREEN, "Tellurium (Te)", "supply pool", _hh_GREEN_TXT)
    _hh_box(77, 19, 98, 33, "#b2ebf2", _hh_CYAN, "CdTe Solar", "panels", _hh_CYAN_TXT)

    _hh_arrow(26, 33, 42, 33, "#f57c00", "anode slimes", _hh_AMBER_TXT)
    _hh_arrow(26, 19, 42, 19, _hh_INDIGO, "residues", _hh_INDIGO_TXT)
    _hh_arrow(66, 26, 77, 26, _hh_GREEN)

    # Key constraint, tied to the supply pool by a short dotted connector
    _hh_shapes.append(dict(type="line", x0=54, y0=12, x1=54, y1=7.0,
                           line=dict(color=_hh_RED, width=2, dash="dot")))
    _hh_notes.append(dict(x=54, y=5, xref="x", yref="y", showarrow=False,
                          text="<b>Te supply is controlled by Cu & Ni output, not by Te demand</b>",
                          font=dict(size=16, color=_hh_RED), bgcolor="#ffebee",
                          bordercolor=_hh_RED, borderwidth=2, borderpad=9))

    _fig_hh.update_layout(
        shapes=_hh_shapes, annotations=_hh_notes,
        xaxis=dict(visible=False, range=[0, 100], fixedrange=True),
        yaxis=dict(visible=False, range=[0, 44], fixedrange=True),
        plot_bgcolor="#f9fbe7", paper_bgcolor="#e8f5e9",
        margin=dict(l=10, r=10, t=10, b=10), height=460, showlegend=False,
    )

    show_chart(_fig_hh, use_container_width=True, config={"staticPlot": True})



    st.divider()
    if st.button("Continue to Material Supply →"):
        go_to_page("⛏️ Material Supply")

# ─────────────────────────────────────────────────────────────────────────────
elif page == "⛏️ Material Supply":
    st.header("Material Supply", divider="grey")
    info_box("Tellurium supply has <b>two main sources</b>: direct mining and copper by-production. "
             "Recycling is covered on the Circular Economy page.")

    # ── Section 1: Direct Mining ──────────────────────────────────────────────
    st.subheader("1 — Direct Mining")
    st.markdown(
        "<p style='font-size:14px;'>A small amount of Te is mined directly. "
        "Its production grows at a fixed annual rate from the current baseline.</p>",
        unsafe_allow_html=True,
    )
    formula_box(
        "Direct Mining Supply (year n)",
        "Te_mine(n) = Current_Production × (1 + Growth_Rate/100) ^ n",
        "100 t × (1 + 0.05)^1 = 105.00 t",
    )

    col1, col2 = st.columns(2)
    with col1:
        mine_base = st.number_input(
            "Current production (tonnes/yr) *",
            min_value=0.0,
            max_value=5000.0,
            step=10.0,
            value=float(st.session_state["mine_base_production"]),
            help="How many tonnes of Tellurium are currently mined directly per year. "
                 "Lecture default ≈ 100 t.",
        )
    with col2:
        mine_gr = st.number_input(
            "Annual growth rate (%) *",
            min_value=0.0,
            max_value=30.0,
            step=0.5,
            value=float(st.session_state["mine_growth_rate"]),
            help="How fast direct mining grows each year. "
                 "Lecture default = 5%.",
        )

    # Show live preview for year 1
    preview_mine = mine_base * (1 + mine_gr / 100)
    st.markdown(
        f"<div style='background:#f1f8e9;padding:8px 14px;border-radius:6px;font-size:13px;'>"
        f"Mining supply in year 1 ({st.session_state['start_year'] + 1}): "
        f"<b>{preview_mine:.2f} tonnes</b></div>",
        unsafe_allow_html=True,
    )

    st.divider()

    # ── Section 2: By-production (fixed, display only) ────────────────────────
    st.subheader("2 — By-production from Copper Refining (fixed)")
    st.markdown(
        "<p style='font-size:14px;'>"
        "The dominant Te supply source. Te is extracted as a <i>byproduct</i> of copper "
        "electrorefining. The parameters below are fixed at typical global values from the lecture."
        "</p>",
        unsafe_allow_html=True,
    )
    formula_box(
        "By-production Supply",
        "Te_byp = Copper_Anode (t) × Te_Content (ppm) × 10⁻⁶ × Yield (%/100)",
        f"29,000,000 t × 110×10⁻⁶ × 0.50 = 1,595.00 t",
    )

    bp_cu   = st.session_state["bp_copper_anode"]
    bp_ppm  = st.session_state["bp_te_content"]
    bp_yld  = st.session_state["bp_yield"]
    bp_supply = bp_cu * 1e6 * bp_ppm * 1e-6 * (bp_yld / 100)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Copper anode production", f"{bp_cu:.2f} M t/yr")
    c2.metric("Te content in anode", f"{bp_ppm:.2f} ppm")
    c3.metric("Recovery yield", f"{bp_yld:.2f}%")
    c4.metric("By-production supply", f"{bp_supply:,.2f} t/yr")

    info_box("By-production parameters are fixed at lecture defaults. "
             "This reflects that Te supply is largely controlled by <b>copper production</b>, "
             "not by Te-specific demand.")

    st.divider()
    if st.button("Save supply inputs →"):
        st.session_state["mine_base_production"] = mine_base
        st.session_state["mine_growth_rate"] = mine_gr
        st.session_state["calculated"] = False
        go_to_page("☀️ Material Demand")

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: Material Demand
# ─────────────────────────────────────────────────────────────────────────────
elif page == "☀️ Material Demand":
    st.header("Material Demand", divider="grey")
    info_box("Tellurium is demanded by <b>CdTe solar panels (PV)</b> and by <b>other industries</b> "
             "(electronics, alloys, thermoelectrics).")

    # ── Section 1: PV Demand ──────────────────────────────────────────────────
    st.subheader("1 — PV Demand")
    st.markdown(
        "<p style='font-size:14px;'>As more CdTe solar panels are installed worldwide, "
        "demand for Tellurium increases.</p>",
        unsafe_allow_html=True,
    )
    formula_box(
        "Annual PV Demand for Te",
        "Te_PV = PV_Production (GWp) × CdTe_Market_Share (%) / 100 × Te_Intensity (kg/GWp) / 1000",
        "626.71 × 0.0727 × 24800/1000 = 1,129.93 t",
    )

    col1, col2 = st.columns(2)
    with col1:
        pv_prod = st.number_input(
            "Global PV production in start year (GWp) *",
            min_value=0.0,
            max_value=10000.0,
            step=10.0,
            value=float(st.session_state["pv_production_start"]),
            help="Total global PV capacity installed in the first year of your study. "
                 "Lecture default = 626.71 GWp (2025).",
        )
        pv_share = st.number_input(
            "CdTe market share in start year (%) *",
            min_value=0.0,
            max_value=100.0,
            step=0.1,
            value=float(st.session_state["pv_market_share_start"]),
            help="Fraction of all PV installations that use CdTe technology. "
                 "Lecture default = 7.27%.",
        )
        pv_ti = st.number_input(
            "Te intensity (kg/GWp) *",
            min_value=0.0,
            max_value=100000.0,
            step=100.0,
            value=float(st.session_state["pv_te_intensity"]),
            help="How much Tellurium is needed per GWp of CdTe PV installed. "
                 "Lecture default = 24,800 kg/GWp.",
        )
    with col2:
        pv_prod_gr = st.number_input(
            "Annual PV production growth rate (%) *",
            min_value=0.0,
            max_value=50.0,
            step=0.5,
            value=float(st.session_state["pv_production_growth"]),
            help="How fast global PV installations grow each year. "
                 "Default ≈ 10% (based on lecture projection).",
        )
        pv_share_gr = st.number_input(
            "Annual CdTe market share growth (% points/yr)",
            min_value=0.0,
            max_value=5.0,
            step=0.01,
            value=float(st.session_state["pv_share_growth"]),
            help="How much the CdTe market share increases each year (in percentage points). "
                 "Lecture default ≈ 0.38 pp/yr.",
        )

    # Live preview
    pv_dem_preview = pv_prod * (pv_share / 100) * (pv_ti / 1000)
    st.markdown(
        f"<div style='background:#f1f8e9;padding:8px 14px;border-radius:6px;font-size:13px;'>"
        f"PV demand in start year ({st.session_state['start_year']}): "
        f"<b>{pv_dem_preview:,.2f} tonnes</b></div>",
        unsafe_allow_html=True,
    )

    st.divider()

    # ── Section 2: Non-PV Demand ──────────────────────────────────────────────
    st.subheader("2 — Non-PV Demand")
    st.markdown(
        "<p style='font-size:14px;'>Other industries (electronics, alloys, thermoelectric devices) "
        "also consume Tellurium. This demand grows at a steady rate.</p>",
        unsafe_allow_html=True,
    )
    formula_box(
        "Non-PV Demand (year n)",
        "Te_nonPV(n) = Base_Demand × (1 + Growth_Rate/100) ^ n",
        "455 × (1 + 0.04)^1 = 473.20 t",
    )

    col3, col4 = st.columns(2)
    with col3:
        npv_base = st.number_input(
            "Non-PV demand in start year (tonnes/yr) *",
            min_value=0.0,
            max_value=5000.0,
            step=5.0,
            value=float(st.session_state["nonpv_base"]),
            help="Baseline non-PV Tellurium demand. Lecture default = 455 t (2024).",
        )
    with col4:
        npv_gr = st.number_input(
            "Annual non-PV growth rate (%) *",
            min_value=0.0,
            max_value=30.0,
            step=0.5,
            value=float(st.session_state["nonpv_growth"]),
            help="Annual growth of non-PV demand. Lecture default = 4%.",
        )

    npv_preview = npv_base * (1 + npv_gr / 100)
    st.markdown(
        f"<div style='background:#f1f8e9;padding:8px 14px;border-radius:6px;font-size:13px;'>"
        f"Non-PV demand in year 1 ({st.session_state['start_year'] + 1}): "
        f"<b>{npv_preview:,.2f} tonnes</b></div>",
        unsafe_allow_html=True,
    )

    st.divider()
    if st.button("Save demand inputs →"):
        st.session_state["pv_production_start"] = pv_prod
        st.session_state["pv_market_share_start"] = pv_share
        st.session_state["pv_te_intensity"] = pv_ti
        st.session_state["pv_production_growth"] = pv_prod_gr
        st.session_state["pv_share_growth"] = pv_share_gr
        st.session_state["nonpv_base"] = npv_base
        st.session_state["nonpv_growth"] = npv_gr
        st.session_state["calculated"] = False
        go_to_page("📊 Results & Gap")

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: Results & Gap
# ─────────────────────────────────────────────────────────────────────────────
elif page == "📊 Results & Gap":
    st.header("Results & Supply–Demand Gap", divider="grey")

    # ── Run calculation ───────────────────────────────────────────────────────
    sy = st.session_state["start_year"]
    ey = st.session_state["end_year"]
    years = list(range(sy, ey + 1))
    n_yrs = len(years)

    # Supply: Mining
    mine_base = st.session_state["mine_base_production"]
    mine_gr   = st.session_state["mine_growth_rate"] / 100
    mining    = [mine_base * (1 + mine_gr) ** i for i in range(n_yrs)]

    # Supply: By-production (fixed, constant over years — copper-tied, no growth assumed)
    bp_cu  = st.session_state["bp_copper_anode"]
    bp_ppm = st.session_state["bp_te_content"]
    bp_yld = st.session_state["bp_yield"] / 100
    bp_val = bp_cu * 1e6 * bp_ppm * 1e-6 * bp_yld
    byproduct = [bp_val] * n_yrs

    # Supply: Recycling (from CE page inputs, starts at 0 by default)
    rec_ret  = st.session_state["rec_retired_pv"]
    rec_ti   = st.session_state["rec_te_intensity"]
    rec_eff  = st.session_state["rec_efficiency"] / 100
    rec_col  = st.session_state["rec_collection"] / 100
    rec_rate = st.session_state["rec_rate"] / 100
    rec_val  = rec_ret * rec_ti * rec_eff * rec_col * rec_rate  # kg → need /1000 for tonnes
    # rec_ti is kg/MWp, rec_ret is GWp → GWp * kg/MWp = GWp * 1000 MWp/GWp * kg/MWp = 1000 * rec_ti * rec_ret kg
    rec_gr_r  = st.session_state.get("rec_retired_growth", 5.0) / 100
    recycling = [
        rec_ret * (1 + rec_gr_r)**i * 1000 * rec_ti * rec_eff * rec_col * rec_rate / 1000
        for i in range(n_yrs)
    ]

    total_supply = [mining[i] + byproduct[i] + recycling[i] for i in range(n_yrs)]

    # Demand: PV
    pv_prod0  = st.session_state["pv_production_start"]
    pv_shr0   = st.session_state["pv_market_share_start"]
    pv_ti     = st.session_state["pv_te_intensity"]
    pv_pgr    = st.session_state["pv_production_growth"] / 100
    pv_sgr    = st.session_state["pv_share_growth"]   # pp/yr

    pv_demand = []
    for i in range(n_yrs):
        prod_i  = pv_prod0 * (1 + pv_pgr) ** i
        share_i = min(pv_shr0 + pv_sgr * i, 100.0)
        dem_i   = prod_i * (share_i / 100) * (pv_ti / 1000)
        pv_demand.append(dem_i)

    # Demand: Non-PV
    npv_base = st.session_state["nonpv_base"]
    npv_gr   = st.session_state["nonpv_growth"] / 100
    nonpv_demand = [npv_base * (1 + npv_gr) ** i for i in range(n_yrs)]

    total_demand = [pv_demand[i] + nonpv_demand[i] for i in range(n_yrs)]
    gap          = [total_supply[i] - total_demand[i] for i in range(n_yrs)]

    st.session_state["calculated"] = True

    # ── Summary metrics ───────────────────────────────────────────────────────
    st.subheader(f"Summary — {sy} to {ey}")
    if st.session_state["student_name"]:
        st.markdown(
            f"<p style='font-size:14px;color:#555;'>Student: "
            f"<b>{st.session_state['student_name']}</b></p>",
            unsafe_allow_html=True,
        )

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Supply (start yr)", f"{total_supply[0]:,.2f} t")
    m2.metric("Demand (start yr)", f"{total_demand[0]:,.2f} t")
    gap0 = gap[0]
    m3.metric("Gap (start yr)", f"{gap0:+,.2f} t", delta="Surplus" if gap0 >= 0 else "Shortage")
    m4.metric("Gap (end yr)", f"{gap[-1]:+,.2f} t", delta="Surplus" if gap[-1] >= 0 else "Shortage")

    st.divider()

    # ── Detailed results table ────────────────────────────────────────────────
    st.subheader("Year-by-year Results")
    df = pd.DataFrame({
        "Year": years,
        "Mining (t)": [round(v, 2) for v in mining],
        "By-production (t)": [round(v, 2) for v in byproduct],
        "Recycling (t)": [round(v, 2) for v in recycling],
        "Total Supply (t)": [round(v, 2) for v in total_supply],
        "PV Demand (t)": [round(v, 2) for v in pv_demand],
        "Non-PV Demand (t)": [round(v, 2) for v in nonpv_demand],
        "Total Demand (t)": [round(v, 2) for v in total_demand],
        "Gap (t)": [round(v, 2) for v in gap],
    })
    st.dataframe(df.set_index("Year").style.format("{:,.2f}"), use_container_width=True)

    # ── Charts ────────────────────────────────────────────────────────────────
    st.divider()
    st.subheader("Supply vs. Demand")

    tab1, tab2, tab3 = st.tabs(["Supply & Demand Overview", "Supply Breakdown", "Gap Chart"])

    with tab1:
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(
            x=years, y=total_supply,
            name="Total Supply", mode="lines+markers",
            line=dict(color="#2e7d32", width=3),
            marker=dict(size=6),
        ))
        fig1.add_trace(go.Scatter(
            x=years, y=total_demand,
            name="Total Demand", mode="lines+markers",
            line=dict(color="#c62828", width=3, dash="dash"),
            marker=dict(size=6),
        ))
        fig1.update_layout(
            xaxis_title="Year", yaxis_title="Tellurium (tonnes)",
            legend=dict(orientation="h", y=1.08),
            plot_bgcolor="#f9fbe7", paper_bgcolor="#e8f5e9",
            font=dict(color="#1b5e20"),
            margin=dict(t=20),
        )
        fig1.update_xaxes(showline=True, mirror=True, ticks="outside",
                          tickmode="array", tickvals=years)
        fig1.update_yaxes(showline=True, mirror=True, ticks="outside", hoverformat=",.2f")
        show_chart(fig1, use_container_width=True)

    with tab2:
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(x=years, y=byproduct, name="By-production",
                              marker_color="#1565c0"))
        fig2.add_trace(go.Bar(x=years, y=mining, name="Direct mining",
                              marker_color="#388e3c"))
        fig2.add_trace(go.Bar(x=years, y=recycling, name="Recycling (CE)",
                              marker_color="#00897b"))
        fig2.update_layout(
            barmode="stack",
            xaxis_title="Year", yaxis_title="Tellurium (tonnes)",
            legend=dict(orientation="h", y=1.08),
            plot_bgcolor="#f9fbe7", paper_bgcolor="#e8f5e9",
            font=dict(color="#1b5e20"),
            margin=dict(t=20),
        )
        fig2.update_xaxes(showline=True, mirror=True, ticks="outside",
                          tickmode="array", tickvals=years)
        fig2.update_yaxes(showline=True, mirror=True, ticks="outside", hoverformat=",.2f")
        show_chart(fig2, use_container_width=True)

    with tab3:
        colors = ["#2e7d32" if g >= 0 else "#c62828" for g in gap]
        fig3 = go.Figure()
        fig3.add_bar(x=years, y=gap, marker_color=colors, name="Gap")
        fig3.add_hline(y=0, line_color="#555", line_width=1.5)
        fig3.update_layout(
            xaxis_title="Year", yaxis_title="Gap = Supply − Demand (tonnes)",
            plot_bgcolor="#f9fbe7", paper_bgcolor="#e8f5e9",
            font=dict(color="#1b5e20"),
            margin=dict(t=20),
        )
        fig3.update_xaxes(showline=True, mirror=True, ticks="outside",
                          tickmode="array", tickvals=years)
        fig3.update_yaxes(showline=True, mirror=True, ticks="outside", zeroline=True,
                          hoverformat=",.2f")
        show_chart(fig3, use_container_width=True)
        st.markdown(
            "<p style='font-size:13px;color:#555;'>Green bars = surplus (supply > demand) &nbsp;|&nbsp; "
            "Red bars = shortage (demand > supply)</p>",
            unsafe_allow_html=True,
        )

    st.divider()

    # ── Insight box ───────────────────────────────────────────────────────────
    final_gap = gap[-1]
    if final_gap >= 0:
        st.markdown(
            f"<div style='background:#e8f5e9;border-left:5px solid #2e7d32;"
            f"padding:14px 18px;border-radius:8px;'>"
            f"<b style='color:#1b5e20;'>Surplus in final year ({ey}): +{final_gap:,.2f} tonnes</b><br>"
            f"<span style='font-size:13px;'>Supply exceeds demand under your scenario. "
            f"Global stocks would be building up.</span></div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"<div style='background:#fff3e0;border-left:5px solid #e65100;"
            f"padding:14px 18px;border-radius:8px;'>"
            f"<b style='color:#bf360c;'>Shortage in final year ({ey}): {final_gap:,.2f} tonnes</b><br>"
            f"<span style='font-size:13px;'>Demand exceeds supply. Circular Economy strategies "
            f"(recycling) could help close this gap — explore the <b>Circular Economy</b> page.</span></div>",
            unsafe_allow_html=True,
        )

    # ── Download ──────────────────────────────────────────────────────────────
    st.divider()
    csv_data = df.to_csv(index=False, float_format="%.2f")
    fname = f"Te_gap_{st.session_state['student_name'].replace(' ','_')}_{sy}_{ey}.csv"
    st.download_button(
        label="Download results as CSV",
        data=csv_data,
        file_name=fname,
        mime="text/csv",
    )

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: Circular Economy
# ─────────────────────────────────────────────────────────────────────────────
elif page == "♻️ Circular Economy":
    st.header("Circular Economy & Recycling", divider="grey")
    info_box("In a <b>Circular Economy (CE)</b>, materials are kept in use as long as possible. "
             "For Tellurium, this means <b>recovering Te from retired CdTe solar panels</b> instead "
             "of letting it go to landfill. Adjust the sliders to see how much supply recycling adds.")

    # ── CE concept cards ──────────────────────────────────────────────────────
    c1, c2, c3 = st.columns(3)
    c1.markdown(
        "<div style='background:#f1f8e9;border-radius:8px;padding:14px;min-height:120px;'>"
        "<b style='color:#2e7d32;'>Recycle</b><br>"
        "<span style='font-size:13px;'>Recover Te from end-of-life CdTe panels. "
        "~90% recovery efficiency is technically achievable.</span></div>",
        unsafe_allow_html=True,
    )
    c2.markdown(
        "<div style='background:#f1f8e9;border-radius:8px;padding:14px;min-height:120px;'>"
        "<b style='color:#2e7d32;'>Urban Mining</b><br>"
        "<span style='font-size:13px;'>Recover Te from decommissioned panels and installed PV fleets, "
        "supplementing primary supply as stocks decline.</span></div>",
        unsafe_allow_html=True,
    )
    c3.markdown(
        "<div style='background:#f1f8e9;border-radius:8px;padding:14px;min-height:120px;'>"
        "<b style='color:#2e7d32;'>Reduce Intensity</b><br>"
        "<span style='font-size:13px;'>Technology improvements already cut Te intensity from "
        "~100 kg/MWp to ~24 kg/MWp. Further reductions directly cut PV demand.</span></div>",
        unsafe_allow_html=True,
    )

    st.divider()
    st.subheader("Recycling Calculator")
    formula_box(
        "Recycled Te from retired panels (year n)",
        "Te_rec(n) = Base_Retired × (1 + Growth/100)^n × 1000 × Te_Intensity × Eff × Collection × Rate / 1000",
        "10 GWp × (1.05)^1 × 1000 × 67 × 0.90 × 0.85 × 1.00 / 1000 = 538.18 t in year 1",
    )

    col1, col2 = st.columns(2)
    with col1:
        rec_ret = st.slider(
            "Retired PV — base year (GWp/yr)",
            min_value=0.0, max_value=500.0, step=5.0,
            value=float(st.session_state["rec_retired_pv"]),
            help="GWp of old CdTe panels decommissioned in the start year. Grows at the rate below.",
        )
        rec_ret_gr = st.slider(
            "Retired PV annual growth rate (%/yr)",
            min_value=0.0, max_value=30.0, step=1.0,
            value=float(st.session_state.get("rec_retired_growth", 5.0)),
            help="As more panels installed today reach end-of-life, the volume of retired panels "
                 "grows each year. Set to 0 for a constant retirement rate.",
        )
        rec_ti = st.slider(
            "Te intensity in panels (kg/MWp)",
            min_value=10.0, max_value=100.0, step=1.0,
            value=float(st.session_state["rec_te_intensity"]),
            help="Amount of Tellurium per MWp in the panels being retired. Default = 67 kg/MWp.",
        )
        rec_eff = st.slider(
            "Recycling efficiency (%)",
            min_value=50.0, max_value=99.0, step=1.0,
            value=float(st.session_state["rec_efficiency"]),
            help="How efficiently Te is extracted from collected panels. ~90% is state-of-the-art.",
        )
    with col2:
        rec_col = st.slider(
            "Module collection rate (%)",
            min_value=10.0, max_value=100.0, step=5.0,
            value=float(st.session_state["rec_collection"]),
            help="Fraction of retired panels actually collected for recycling vs landfill. "
                 "This is the key policy lever.",
        )
        rec_rate = st.slider(
            "Recycle rate of collected panels (%)",
            min_value=10.0, max_value=100.0, step=5.0,
            value=float(st.session_state["rec_rate"]),
            help="Of the panels collected, what % actually go through the recycling process.",
        )

    # Year-by-year recycling
    _sy_ce = st.session_state["start_year"]
    _ey_ce = st.session_state["end_year"]
    _n_ce  = _ey_ce - _sy_ce + 1
    rec_by_year = [
        rec_ret * (1 + rec_ret_gr/100)**i * 1000
        * rec_ti * (rec_eff/100) * (rec_col/100) * (rec_rate/100) / 1000
        for i in range(_n_ce)
    ]
    rec_supply = rec_by_year[0]

    import pandas as _pd_ce
    _rec_df = _pd_ce.DataFrame({
        "Year": list(range(_sy_ce, _ey_ce + 1)),
        "Retired PV (GWp)": [round(rec_ret*(1+rec_ret_gr/100)**i, 2) for i in range(_n_ce)],
        "Recycled Te (t)":  [round(v, 2) for v in rec_by_year],
    })
    st.dataframe(_rec_df.set_index("Year").style.format("{:,.2f}"), use_container_width=True)

    st.markdown(
        f"<div style='background:#e8f5e9;border:2px solid #2e7d32;border-radius:8px;"
        f"padding:14px 18px;margin:12px 0;font-size:15px;text-align:center;'>"
        f"<b>Recycled Te: {rec_supply:,.2f} t in {_sy_ce} → "
        f"{rec_by_year[-1]:,.2f} t in {_ey_ce}</b></div>",
        unsafe_allow_html=True,
    )

    # ── Impact on gap ─────────────────────────────────────────────────────────
    st.divider()
    st.subheader("Impact on the Supply–Demand Gap")

    if st.button("Apply recycling to Results page →"):
        st.session_state["rec_retired_pv"]     = rec_ret
        st.session_state["rec_retired_growth"] = rec_ret_gr
        st.session_state["rec_te_intensity"]   = rec_ti
        st.session_state["rec_efficiency"]     = rec_eff
        st.session_state["rec_collection"]     = rec_col
        st.session_state["rec_rate"]           = rec_rate
        st.session_state["calculated"]         = False
        go_to_page("📊 Results & Gap")

    # Quick comparison: with vs without recycling
    sy = st.session_state["start_year"]
    ey = st.session_state["end_year"]
    years = list(range(sy, ey + 1))
    n_yrs = len(years)

    mine_base = st.session_state["mine_base_production"]
    mine_gr   = st.session_state["mine_growth_rate"] / 100
    mining    = [mine_base * (1 + mine_gr) ** i for i in range(n_yrs)]
    bp_val    = (st.session_state["bp_copper_anode"] * 1e6
                 * st.session_state["bp_te_content"] * 1e-6
                 * st.session_state["bp_yield"] / 100)
    byproduct = [bp_val] * n_yrs

    pv_prod0 = st.session_state["pv_production_start"]
    pv_shr0  = st.session_state["pv_market_share_start"]
    pv_ti    = st.session_state["pv_te_intensity"]
    pv_pgr   = st.session_state["pv_production_growth"] / 100
    pv_sgr   = st.session_state["pv_share_growth"]
    pv_dem   = [pv_prod0 * (1 + pv_pgr)**i * min(pv_shr0 + pv_sgr*i, 100)/100 * pv_ti/1000
                for i in range(n_yrs)]
    npv_base = st.session_state["nonpv_base"]
    npv_gr   = st.session_state["nonpv_growth"] / 100
    npv_dem  = [npv_base * (1 + npv_gr)**i for i in range(n_yrs)]
    total_dem = [pv_dem[i] + npv_dem[i] for i in range(n_yrs)]

    _rec_gr_ce = st.session_state.get("rec_retired_growth", 5.0) / 100
    rec_yearly_ce = [
        st.session_state["rec_retired_pv"] * (1 + _rec_gr_ce)**i * 1000
        * st.session_state["rec_te_intensity"]
        * st.session_state["rec_efficiency"] / 100
        * st.session_state["rec_collection"] / 100
        * st.session_state["rec_rate"] / 100 / 1000
        for i in range(n_yrs)
    ]
    gap_no_rec   = [mining[i] + byproduct[i] - total_dem[i] for i in range(n_yrs)]
    gap_with_rec = [mining[i] + byproduct[i] + rec_yearly_ce[i] - total_dem[i] for i in range(n_yrs)]

    fig_ce = go.Figure()
    fig_ce.add_trace(go.Scatter(
        x=years, y=gap_no_rec,
        name="Gap without recycling", mode="lines+markers",
        line=dict(color="#c62828", width=2, dash="dash"),
    ))
    fig_ce.add_trace(go.Scatter(
        x=years, y=gap_with_rec,
        name="Gap with recycling", mode="lines+markers",
        line=dict(color="#2e7d32", width=2),
    ))
    fig_ce.add_hline(y=0, line_color="#555", line_width=1.5)
    fig_ce.update_layout(
        xaxis_title="Year",
        yaxis_title="Supply − Demand gap (tonnes)",
        legend=dict(orientation="h", y=1.08),
        plot_bgcolor="#f9fbe7", paper_bgcolor="#e8f5e9",
        font=dict(color="#1b5e20"),
        margin=dict(t=20),
    )
    fig_ce.update_xaxes(showline=True, mirror=True, ticks="outside",
                        tickmode="array", tickvals=years)
    fig_ce.update_yaxes(showline=True, mirror=True, ticks="outside", hoverformat=",.2f")
    show_chart(fig_ce, use_container_width=True)

    diff = rec_supply * n_yrs
    st.markdown(
        f"<p style='font-size:13px;color:#555;'>"
        f"With these settings, recycling grows from <b>{rec_by_year[0]:,.2f} t</b> "
        f"in year 1 to <b>{rec_by_year[-1]:,.2f} t</b> by {_ey_ce}, "
        f"improving the supply–demand gap each year.</p>",
        unsafe_allow_html=True,
    )

    # ── CE definition ─────────────────────────────────────────────────────────
    st.divider()
    st.markdown(
        "<div style='background:#1b5e20;padding:18px 24px;border-radius:10px;margin-bottom:12px;'>"
        "<p style='color:#fff;font-size:18px;font-weight:bold;margin:0;'>"
        "What is Circular Economy?</p></div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='font-size:14px;line-height:1.8;'>"
        "A <b>Circular Economy (CE)</b> is an economic model designed to eliminate waste and keep "
        "materials in use as long as possible. Unlike the traditional <em>linear</em> model "
        "(extract → manufacture → use → discard), CE closes the loop by <b>recovering and "
        "regenerating materials</b> at the end of each service life.</p>"
        "<p style='font-size:14px;line-height:1.8;'>"
        "For critical PV materials like Tellurium, CE strategies directly extend the supply "
        "available — as shown in the chart above. The three key levers are: "
        "<b>collection rate</b> (policy), <b>recycling efficiency</b> (technology), and "
        "<b>material intensity reduction</b> (R&D).</p>",
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: LCA of CdTe Solar
# ─────────────────────────────────────────────────────────────────────────────
elif page == "🌍 LCA of CdTe Solar":
    st.header("Life Cycle Assessment (LCA) of CdTe Solar", divider="grey")
    import plotly.graph_objects as _go_lca

    # ── What is LCA ───────────────────────────────────────────────────────────
    st.subheader("1 — What is Life Cycle Assessment?")
    st.markdown(
        "<p style='font-size:14px;line-height:1.8;'>"
        "Life Cycle Assessment (LCA) estimates the <b>total environmental footprint</b> "
        "of a product from raw material extraction to end of life. "
        "For CdTe solar modules, that means tracking the impact of every step: "
        "copper mining, smelting, electrorefining, anode slime processing, "
        "Te refining, and panel manufacturing. "
        "The key metric we focus on here is <b>Global Warming Potential (GWP)</b> — "
        "measured in kg CO₂-equivalent per functional unit.</p>",
        unsafe_allow_html=True,
    )

    st.divider()

    # ── System boundary diagram ───────────────────────────────────────────────
    st.subheader("2 — System Boundary: From Copper Mine to CdTe Solar Module")
    info_box(
        "This is the system boundary used by Hanna &amp; Anctil (2025). Everything inside the "
        "dashed line is counted in the LCA, from copper mining to the finished CdTe panel. "
        "Tellurium is mainly recovered as a <b>by-product of copper refining</b>: it comes out of the "
        "<b>anode slime</b> left behind during electrorefining. "
        "Shaded boxes are processes, white boxes are the products they make, and "
        "<b>T</b> marks transport between facilities."
    )

    import plotly.graph_objects as _go_sb

    # Drawing units are pixel-like (x to the right, y DOWN). The y-axis is reversed and locked
    # 1:1 to the x-axis, so circles stay round and boxes keep their proportions at any width.
    _sb_W = 600                          # canvas width
    _sb_BX0, _sb_BX1 = 70, 545           # dashed boundary: left / right edge
    _sb_X0, _sb_X1 = 145, 495            # process & product boxes: left / right edge
    _sb_XM = (_sb_X0 + _sb_X1) / 2       # centre line of the boxes
    _sb_XC = 108                         # x of the vertical transport connector
    _sb_PROC_H, _sb_PROD_H = 38, 22      # box heights
    _sb_PROD_GAP = 3                     # gap between stacked product boxes
    _sb_PD_GAP = 10                      # process -> its first product (arrow gap)
    _sb_GRP_GAP = 26                     # last product -> next process (T circle gap)
    _sb_TOP = 104                        # top edge of the first box

    _sb_LINE, _sb_PROC, _sb_TXT = "#37474f", "#c8e6c9", "#263238"
    _sb_BOUND, _sb_T = "#1b5e20", "#2e7d32"

    # (process, [products it makes]). The FIRST product in each list is the one that is
    # transported to the next process (shown by the T connector on the left).
    _sb_chain = [
        ("Copper Mining &amp;<br>Beneficiation", ["Copper Concentrate", "Molybdenum"]),
        ("Smelting",                             ["Copper Anode"]),
        ("Electrorefining",                      ["Anode Slime", "Copper Cathode"]),
        ("Anode Slime<br>Processing",            ["Copper Telluride", "Selenium", "Gold", "Silver", "Copper"]),
        ("Refining",                             ["SG-Te"]),
        ("SG-CdTe<br>Production",                ["SG-CdTe"]),
        ("CdTe PV<br>Production",                ["CdTe solar panel"]),
    ]

    # ── Work out every box position, top to bottom ────────────────────────────
    _sb_procs, _sb_prods, _sb_links = [], [], []
    _sb_y = _sb_TOP
    for _sb_i, (_sb_plabel, _sb_plist) in enumerate(_sb_chain):
        _sb_py0, _sb_py1 = _sb_y, _sb_y + _sb_PROC_H
        _sb_procs.append((_sb_plabel, _sb_py0, _sb_py1))
        _sb_y = _sb_py1 + _sb_PD_GAP
        for _sb_j, _sb_name in enumerate(_sb_plist):
            _sb_prods.append((_sb_name, _sb_y, _sb_y + _sb_PROD_H))
            if _sb_j == 0:
                _sb_first_mid = _sb_y + _sb_PROD_H / 2
            _sb_y += _sb_PROD_H + _sb_PROD_GAP
        _sb_last_bottom = _sb_y - _sb_PROD_GAP
        if _sb_i < len(_sb_chain) - 1:        # transport link to the next process
            _sb_next_mid = _sb_last_bottom + _sb_GRP_GAP + _sb_PROC_H / 2
            _sb_links.append((_sb_first_mid, _sb_next_mid, _sb_last_bottom + _sb_GRP_GAP / 2))
        _sb_y = _sb_last_bottom + _sb_GRP_GAP

    _sb_BY0, _sb_BY1 = 68, _sb_last_bottom + 28      # dashed boundary: top / bottom
    _sb_H = _sb_BY1 + 140                            # canvas height

    # ── Small drawing helpers ─────────────────────────────────────────────────
    _sb_shapes, _sb_notes = [], []

    def _sb_rrect(x0, y0, x1, y1, r):
        """SVG path for a rounded rectangle."""
        return (f"M {x0+r},{y0} L {x1-r},{y0} Q {x1},{y0} {x1},{y0+r} "
                f"L {x1},{y1-r} Q {x1},{y1} {x1-r},{y1} "
                f"L {x0+r},{y1} Q {x0},{y1} {x0},{y1-r} "
                f"L {x0},{y0+r} Q {x0},{y0} {x0+r},{y0} Z")

    def _sb_text(x, y, text, size=12, color=_sb_TXT, **kw):
        _sb_notes.append(dict(x=x, y=y, text=text, showarrow=False, xref="x", yref="y",
                              font=dict(size=size, color=color), **kw))

    def _sb_arrow(x_tail, y_tail, x_head, y_head, width=1.4):
        _sb_notes.append(dict(x=x_head, y=y_head, ax=x_tail, ay=y_tail,
                              xref="x", yref="y", axref="x", ayref="y",
                              showarrow=True, text="", arrowhead=2, arrowsize=1.1,
                              arrowwidth=width, arrowcolor=_sb_LINE))

    def _sb_line(path, width=1.4):
        _sb_shapes.append(dict(type="path", path=path, fillcolor="rgba(0,0,0,0)",
                               line=dict(color=_sb_LINE, width=width)))

    # ── Dashed system boundary (white inside, so "in" vs "out" is obvious) ────
    _sb_shapes.append(dict(type="path", path=_sb_rrect(_sb_BX0, _sb_BY0, _sb_BX1, _sb_BY1, 26),
                           fillcolor="#ffffff", layer="below",
                           line=dict(color=_sb_BOUND, width=2.2, dash="dash")))

    # "System Boundary" bracket + rotated label on the left edge
    _sb_ya, _sb_yb = _sb_BY0 + 60, _sb_BY0 + 205
    _sb_line(f"M {_sb_BX0},{_sb_ya} L {_sb_BX0-40},{_sb_ya} L {_sb_BX0-40},{_sb_yb} L {_sb_BX0},{_sb_yb}")
    _sb_text(_sb_BX0 - 20, (_sb_ya + _sb_yb) / 2, "<b>System Boundary</b>", size=13, textangle=-90)

    # ── Inputs (top) and outputs (bottom) ─────────────────────────────────────
    for _sb_x, _sb_lbl in zip((190, 320, 450), ("Chemicals", "Water", "Energy")):
        _sb_text(_sb_x, 24, _sb_lbl, size=13)
        _sb_arrow(_sb_x, 40, _sb_x, _sb_TOP - 6, width=1.9)
    for _sb_x, _sb_lbl in zip((208, 426), ("Waste", "Wastewater")):
        _sb_arrow(_sb_x, _sb_BY1 - 12, _sb_x, _sb_BY1 + 46, width=1.9)
        _sb_text(_sb_x, _sb_BY1 + 63, _sb_lbl, size=13)

    # ── Process boxes (shaded, rounded) with an arrow down to their first product ─
    for _sb_lbl, _sb_y0, _sb_y1 in _sb_procs:
        _sb_shapes.append(dict(type="path", path=_sb_rrect(_sb_X0, _sb_y0, _sb_X1, _sb_y1, 8),
                               fillcolor=_sb_PROC, line=dict(color=_sb_LINE, width=1.5)))
        _sb_text(_sb_XM, (_sb_y0 + _sb_y1) / 2, f"<b>{_sb_lbl}</b>", size=13)
        _sb_arrow(_sb_XM, _sb_y1, _sb_XM, _sb_y1 + _sb_PD_GAP, width=1.3)

    # ── Product boxes (white, square) ─────────────────────────────────────────
    for _sb_lbl, _sb_y0, _sb_y1 in _sb_prods:
        _sb_shapes.append(dict(type="rect", x0=_sb_X0, x1=_sb_X1, y0=_sb_y0, y1=_sb_y1,
                               fillcolor="#ffffff", line=dict(color=_sb_LINE, width=1.1)))
        _sb_text(_sb_XM, (_sb_y0 + _sb_y1) / 2, _sb_lbl, size=12.5)

    # ── Transport links: first product -> T -> next process ───────────────────
    for _sb_yf, _sb_yt, _sb_yc in _sb_links:
        _sb_line(f"M {_sb_X0},{_sb_yf} L {_sb_XC},{_sb_yf} L {_sb_XC},{_sb_yt}")
        _sb_arrow(_sb_XC, _sb_yt, _sb_X0, _sb_yt)
    for _sb_yf, _sb_yt, _sb_yc in _sb_links:
        _sb_shapes.append(dict(type="circle", x0=_sb_XC - 12, x1=_sb_XC + 12,
                               y0=_sb_yc - 12, y1=_sb_yc + 12,
                               fillcolor="#ffffff", line=dict(color=_sb_T, width=1.8)))
        _sb_text(_sb_XC, _sb_yc, "<b>T</b>", size=13, color=_sb_T)

    # ── Key (bottom) ──────────────────────────────────────────────────────────
    _sb_ky = _sb_BY1 + 112
    _sb_shapes.append(dict(type="path", path=_sb_rrect(75, _sb_ky - 10, 105, _sb_ky + 10, 5),
                           fillcolor=_sb_PROC, line=dict(color=_sb_LINE, width=1.3)))
    _sb_text(113, _sb_ky, "Process", size=12, xanchor="left")
    _sb_shapes.append(dict(type="rect", x0=205, x1=235, y0=_sb_ky - 10, y1=_sb_ky + 10,
                           fillcolor="#ffffff", line=dict(color=_sb_LINE, width=1.1)))
    _sb_text(243, _sb_ky, "Product", size=12, xanchor="left")
    _sb_shapes.append(dict(type="circle", x0=322, x1=346, y0=_sb_ky - 12, y1=_sb_ky + 12,
                           fillcolor="#ffffff", line=dict(color=_sb_T, width=1.8)))
    _sb_text(334, _sb_ky, "<b>T</b>", size=13, color=_sb_T)
    _sb_text(356, _sb_ky, "<i>Transportation of<br>intermediate products</i>", size=12, xanchor="left")

    # ── Assemble the figure ───────────────────────────────────────────────────
    _fig_sb = _go_sb.Figure()
    _fig_sb.update_layout(
        shapes=_sb_shapes, annotations=_sb_notes,
        xaxis=dict(range=[0, _sb_W], visible=False, constrain="domain", fixedrange=True),
        yaxis=dict(range=[_sb_H, 0], visible=False, scaleanchor="x", scaleratio=1,
                   constrain="domain", fixedrange=True),
        plot_bgcolor="#f9fbe7", paper_bgcolor="#e8f5e9",
        margin=dict(l=0, r=0, t=8, b=8), height=int(_sb_H) + 16, showlegend=False,
    )
    show_chart(_fig_sb, use_container_width=True, config={"staticPlot": True})
    st.caption(
        "Fig. 1 — System boundary from copper mining to CdTe solar panel production, "
        "redrawn from Hanna & Anctil (2025). Shaded boxes = processes, white boxes = products, "
        "T = transportation of intermediate products, SG = semiconductor grade."
    )

    st.divider()

    # ── Processing method comparison ──────────────────────────────────────────
    st.subheader("3 — Processing Method: Hydro vs. Hydro-Pyrometallurgy")
    st.markdown(
        "<p style='font-size:14px;line-height:1.8;'>"
        "Anode slimes can be treated using two main methods. The method chosen "
        "by the refinery significantly changes the environmental footprint of tellurium. "
        "Select a method below to see its relative impact.</p>",
        unsafe_allow_html=True,
    )

    _method = st.radio(
        "Select processing method:",
        ["Hydrometallurgy (HM)", "Hydro-Pyrometallurgy (HPM)"],
        horizontal=True,
        key="lca_method",
    )
    _is_hm = "Hydro-P" not in _method

    # Relative values: HPM = baseline (1.0), HM is higher by the % shown
    # Paper: HM increases GWP by ≥37%, water consumption by 34%, FW toxicity by 51%, ADP by 48%
    _impact_cats = ["Global Warming\nPotential (GWP)", "Water\nConsumption", "Freshwater\nToxicity", "Abiotic\nDepletion (ADP)"]
    _hm_increases = [37, 34, 51, 48]  # % higher than HPM
    _hpm_vals = [100, 100, 100, 100]
    _hm_vals  = [100 + d for d in _hm_increases]
    _selected_vals = _hm_vals if _is_hm else _hpm_vals
    _baseline_vals = _hpm_vals if _is_hm else _hm_vals
    _bar_colors = ["#c62828" if _is_hm else "#2e7d32"] * 4

    _fig_method = _go_lca.Figure()
    _fig_method.add_trace(_go_lca.Bar(
        x=_impact_cats, y=_selected_vals,
        marker_color=_bar_colors,
        text=[f"{v:.2f}" for v in _selected_vals],
        textposition="outside",
        name="Selected method",
    ))
    _fig_method.add_trace(_go_lca.Bar(
        x=_impact_cats, y=_baseline_vals,
        marker_color=["rgba(150,150,150,0.35)"] * 4,
        text=[f"{v:.2f}" for v in _baseline_vals],
        textposition="outside",
        name="Other method",
    ))
    _fig_method.update_layout(
        barmode="group",
        yaxis=dict(title="Relative impact (HPM baseline = 100)", range=[0, 175], hoverformat=".2f"),
        xaxis=dict(title="Impact category"),
        legend=dict(orientation="h", y=1.1),
        plot_bgcolor="#f9fbe7", paper_bgcolor="#e8f5e9",
        font=dict(color="#1b5e20"),
        margin=dict(t=30, b=10),
        height=340,
    )
    show_chart(_fig_method, use_container_width=True)

    if _is_hm:
        st.markdown(
            "<div style='background:#ffebee;border-left:5px solid #c62828;"
            "padding:12px 16px;border-radius:6px;font-size:13px;'>"
            "<b>Hydrometallurgy</b> uses more chemicals (HCl, H₂O₂, H₂SO₄, dibutyl carbitol) "
            "and recovers Te only at the <i>final</i> reduction step — after bearing the environmental "
            "cost of recovering silver, gold, and selenium first. This leads to "
            "<b>37–51% higher impacts</b> compared to hydro-pyrometallurgy.</div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            "<div style='background:#e8f5e9;border-left:5px solid #2e7d32;"
            "padding:12px 16px;border-radius:6px;font-size:13px;'>"
            "<b>Hydro-Pyrometallurgy</b> recovers tellurium early in the process "
            "(decopperization step), before silver and gold recovery. This means Te "
            "only bears the footprint of the first stage, not all subsequent steps. "
            "This is the method used in the <b>US (Rio Tinto/Kennecott) and Canada (Glencore CCR)</b>.</div>",
            unsafe_allow_html=True,
        )

    st.divider()

    # ── Location comparison ───────────────────────────────────────────────────
    st.subheader("4 — Location Matters: No Country Wins on Everything")
    info_box(
        "The environmental impact of CdTe depends heavily on <b>where</b> copper is mined and "
        "anode slimes are processed. Sourcing and treating anode slimes in Canada reduces the "
        "carbon footprint of SG-CdTe by up to <b>64%</b> compared to the worst-case scenario — "
        "but Canada has the <b>highest freshwater toxicity and abiotic depletion</b> due to its "
        "high copper ore concentration."
    )

    _location = st.selectbox(
        "Select production location:",
        ["China (CN) — Jiangxi Copper", "Canada (CA) — Glencore CCR",
         "Japan (JP) — JX Metals Saganoseki", "USA (US) — Rio Tinto Kennecott"],
        key="lca_location",
    )

    # Relative values by location (worst case = 100 per metric)
    _loc_data = {
        "China (CN) — Jiangxi Copper":        {"GWP": 85,  "Water Scarcity": 100, "FW Toxicity": 100, "ADP": 100},
        "Canada (CA) — Glencore CCR":         {"GWP": 36,  "Water Scarcity": 30,  "FW Toxicity": 95,  "ADP": 95},
        "Japan (JP) — JX Metals Saganoseki":  {"GWP": 100, "Water Scarcity": 65,  "FW Toxicity": 70,  "ADP": 70},
        "USA (US) — Rio Tinto Kennecott":     {"GWP": 55,  "Water Scarcity": 55,  "FW Toxicity": 57,  "ADP": 57},
    }
    _loc_vals = _loc_data[_location]
    _loc_cats = list(_loc_vals.keys())
    _loc_scores = list(_loc_vals.values())
    _loc_colors = ["#2e7d32" if v <= 50 else "#f57f17" if v <= 75 else "#c62828"
                   for v in _loc_scores]

    _fig_loc = _go_lca.Figure()
    _fig_loc.add_trace(_go_lca.Bar(
        x=_loc_cats, y=_loc_scores,
        marker_color=_loc_colors,
        text=[f"{v:.2f}" for v in _loc_scores],
        textposition="outside",
    ))
    _fig_loc.add_hline(y=50, line_dash="dot", line_color="#888",
                       annotation_text="50 — midpoint", annotation_position="right")
    _fig_loc.update_layout(
        yaxis=dict(title="Relative impact (worst case = 100)", range=[0, 120], hoverformat=".2f"),
        xaxis=dict(title="Impact category"),
        plot_bgcolor="#f9fbe7", paper_bgcolor="#e8f5e9",
        font=dict(color="#1b5e20"),
        margin=dict(t=20, b=10),
        height=320,
        showlegend=False,
    )
    show_chart(_fig_loc, use_container_width=True)

    # Per-location insight
    _loc_insights = {
        "China (CN) — Jiangxi Copper": (
            "#ffebee", "#c62828",
            "China has the <b>highest water scarcity footprint</b> — despite using less water than Canada, "
            "China's water scarcity characterization factor (CF) is 10× Canada's and 3× the US. "
            "It also leads in freshwater toxicity and abiotic depletion."
        ),
        "Canada (CA) — Glencore CCR": (
            "#e8f5e9", "#2e7d32",
            "Canada has the <b>lowest carbon footprint and energy demand</b> thanks to its clean electricity grid. "
            "However, Canada has the <b>highest freshwater toxicity and ADP</b> — driven by its very high "
            "copper sulfide ore concentration (low copper-to-molybdenum ratio = only 4.36% of mining impacts "
            "allocated to molybdenum, vs. >20% elsewhere)."
        ),
        "Japan (JP) — JX Metals Saganoseki": (
            "#fff8e1", "#e65100",
            "Japan (SC3) has the <b>highest carbon footprint of all scenarios</b> because it imports "
            "copper concentrate from Chile — ~20,000 km by sea + 174 km by truck. "
            "Transportation adds significant GWP despite Chile having a cleaner grid."
        ),
        "USA (US) — Rio Tinto Kennecott": (
            "#e3f2fd", "#1565c0",
            "The US has the <b>lowest freshwater toxicity and abiotic depletion</b> among all scenarios. "
            "This is because the US has the lowest copper concentration and highest molybdenum production "
            "from copper sulfide ores — distributing more environmental burden to molybdenum, less to Te. "
            "The US also benefits from a relatively low-carbon electricity grid."
        ),
    }
    _bg, _tc, _txt = _loc_insights[_location]
    st.markdown(
        f"<div style='background:{_bg};border-left:5px solid {_tc};"
        f"padding:12px 16px;border-radius:6px;font-size:13px;line-height:1.7;'>{_txt}</div>",
        unsafe_allow_html=True,
    )

    st.divider()

    # ── CO2 Calculator linked to student gap ──────────────────────────────────
    st.subheader("5 — Carbon Footprint of Your Te Supply Gap")
    info_box(
        "Your <b>Results & Gap</b> page calculated a supply–demand gap in tonnes of Tellurium. "
        "Here we translate that into a carbon footprint using the GWP of Te production — "
        "so you can see the real-world climate cost of supplying (or failing to supply) Te."
    )

    # Pull student gap from session state
    _co2_sy   = st.session_state["start_year"]
    _co2_ey   = st.session_state["end_year"]
    _co2_n    = _co2_ey - _co2_sy + 1
    _co2_mine = [st.session_state["mine_base_production"] * (1 + st.session_state["mine_growth_rate"]/100)**i
                 for i in range(_co2_n)]
    _co2_bp   = (st.session_state["bp_copper_anode"] * 1e6
                 * st.session_state["bp_te_content"] * 1e-6
                 * st.session_state["bp_yield"] / 100)
    _co2_rec_gr = st.session_state.get("rec_retired_growth", 5.0) / 100
    _co2_rec  = [st.session_state["rec_retired_pv"] * (1 + _co2_rec_gr)**i * 1000
                 * st.session_state["rec_te_intensity"]
                 * st.session_state["rec_efficiency"] / 100
                 * st.session_state["rec_collection"] / 100
                 * st.session_state["rec_rate"] / 100 / 1000
                 for i in range(_co2_n)]
    _co2_sup  = [_co2_mine[i] + _co2_bp + _co2_rec[i] for i in range(_co2_n)]
    _co2_pv   = [st.session_state["pv_production_start"] * (1 + st.session_state["pv_production_growth"]/100)**i
                 * min(st.session_state["pv_market_share_start"] + st.session_state["pv_share_growth"]*i, 100)/100
                 * st.session_state["pv_te_intensity"] / 1000
                 for i in range(_co2_n)]
    _co2_npv  = [st.session_state["nonpv_base"] * (1 + st.session_state["nonpv_growth"]/100)**i
                 for i in range(_co2_n)]
    _co2_dem  = [_co2_pv[i] + _co2_npv[i] for i in range(_co2_n)]
    _co2_gap  = [_co2_sup[i] - _co2_dem[i] for i in range(_co2_n)]

    # GWP per kg Te by location and method (kg CO2-eq per kg Te)
    # Values derived from LCA literature for SG-grade Te
    # HPM: CA~5, US~12, JP~25, CN~22 kg CO2/kg Te (approximate from Fig.3 scale)
    # HM is ~37% higher
    st.markdown(
        "<p style='font-size:13px;color:#555;margin-bottom:8px;'>"
        "Select the sourcing location and processing method to see the carbon intensity "
        "of Te production — then see how your gap translates into kg CO₂.</p>",
        unsafe_allow_html=True,
    )

    _co2_col1, _co2_col2 = st.columns(2)
    with _co2_col1:
        _co2_loc = st.selectbox(
            "Production location",
            ["Canada (CA)", "USA (US)", "Japan (JP)", "China (CN)"],
            key="co2_loc",
        )
    with _co2_col2:
        _co2_method = st.radio(
            "Processing method",
            ["Hydro-Pyrometallurgy (HPM)", "Hydrometallurgy (HM)"],
            horizontal=True,
            key="co2_method",
        )

    # GWP intensity (kg CO2-eq per kg Te) — HPM baseline, HM is 37% higher
    _gwp_hpm = {"Canada (CA)": 5.0, "USA (US)": 12.0, "Japan (JP)": 25.0, "China (CN)": 22.0}
    _gwp_base = _gwp_hpm[_co2_loc]
    _gwp_te   = _gwp_base * 1.37 if "HM" in _co2_method and "HPM" not in _co2_method else _gwp_base

    # Total Te supplied over study period × GWP intensity = total carbon footprint
    _co2_total_supply_t = sum(_co2_sup)   # tonnes
    _co2_kg_co2 = _co2_total_supply_t * 1000 * _gwp_te  # tonnes Te → kg Te → kg CO2
    _co2_gap_end = _co2_gap[-1]
    _co2_gap_impact = abs(_co2_gap_end) * 1000 * _gwp_te  # kg CO2 for the gap

    _co2_m1, _co2_m2, _co2_m3 = st.columns(3)
    _co2_m1.metric(
        "Te GWP intensity",
        f"{_gwp_te:.2f} kg CO₂/kg Te",
        help="Carbon footprint per kg of semiconductor-grade Te produced",
    )
    _co2_m2.metric(
        f"Total CO₂ from Te supply ({_co2_sy}–{_co2_ey})",
        f"{_co2_kg_co2/1e6:,.2f} kt CO₂",
        help="Cumulative carbon footprint of all Te supplied over your study period",
    )
    _co2_m3.metric(
        f"CO₂ impact of gap in {_co2_ey}",
        f"{_co2_gap_impact/1e6:,.2f} kt CO₂",
        delta="surplus saves this CO₂" if _co2_gap_end >= 0 else "shortage needs this CO₂",
        help="Carbon cost of the supply–demand gap in the final year",
    )

    # Year-by-year CO2 chart
    _co2_yearly = [s * 1000 * _gwp_te / 1e6 for s in _co2_sup]  # kt CO2 per year
    _fig_co2 = _go_lca.Figure()
    _fig_co2.add_trace(_go_lca.Bar(
        x=list(range(_co2_sy, _co2_ey + 1)),
        y=_co2_yearly,
        name="CO₂ from Te supply",
        marker_color="#c62828",
        text=[f"{v:,.2f}" for v in _co2_yearly],
        textposition="outside",
    ))
    _fig_co2.update_layout(
        xaxis=dict(title="Year", tickmode="array",
                   tickvals=list(range(_co2_sy, _co2_ey + 1))),
        yaxis=dict(title="kt CO₂-eq per year", hoverformat=",.2f"),
        plot_bgcolor="#f9fbe7", paper_bgcolor="#e8f5e9",
        font=dict(color="#1b5e20"),
        margin=dict(t=20, b=10), height=280, showlegend=False,
    )
    show_chart(_fig_co2, use_container_width=True)

    st.markdown(
        f"<div style='background:#f1f8e9;border-left:4px solid #2e7d32;padding:10px 14px;"
        f"border-radius:6px;font-size:13px;'>"
        f"<b>Connection to your supply gap:</b> Your scenario shows a gap of "
        f"<b>{_co2_gap_end:+,.2f} t</b> in {_co2_ey}. "
        f"At {_gwp_te:.2f} kg CO₂/kg Te ({_co2_loc}, {_co2_method.split()[0]}), "
        f"sourcing that Te would produce "
        f"<b>{_co2_gap_impact/1e6:,.2f} kt CO₂</b>. "
        f"Switching to a lower-GWP location or method directly reduces this burden.</div>",
        unsafe_allow_html=True,
    )

    st.divider()

    # ── Key takeaways ─────────────────────────────────────────────────────────
    st.subheader("6 — Key Takeaways")
    _takeaways = [
        ("Your Te supply has a calculable carbon cost",
         "The GWP of Te ranges from ~5 kg CO₂/kg (Canada, HPM) to ~34 kg CO₂/kg (Japan, HM). "
         "Your sourcing choice has a direct, calculable impact on total CO₂ emissions."),
        ("Circular Economy reduces the burden",
         "Recycling retired CdTe panels reduces demand for newly mined Te — directly cutting "
         "the upstream environmental impacts shown here."),
    ]
    for title, desc in _takeaways:
        st.markdown(
            f"<div style='display:flex;align-items:flex-start;gap:14px;"
            f"background:#f1f8e9;border-radius:8px;padding:12px 16px;margin-bottom:8px;'>"
            f"<div><b style='color:#1b5e20;font-size:14px;'>{title}</b>"
            f"<p style='font-size:13px;color:#333;margin:4px 0 0 0;line-height:1.6;'>{desc}</p>"
            f"</div></div>",
            unsafe_allow_html=True,
        )


# ─────────────────────────────────────────────────────────────────────────────
# PAGE: Scenario Analysis
# ─────────────────────────────────────────────────────────────────────────────
elif page == "🔍 Scenario Analysis":
    st.header("Scenario Analysis — Tellurium Supply Strategy", divider="grey")
    info_box(
        "You have studied the supply chain, demand projections, supply–demand gap, "
        "circular economy strategies, and LCA impacts of CdTe solar. "
        "Now <b>synthesize your findings</b> and answer the questions below "
        "to build a complete supply strategy recommendation."
    )


    # ── Auto-pull student's own numbers ──────────────────────────────────────
    st.subheader("Your Scenario Summary")
    st.markdown(
        "<p style='font-size:13px;color:#555;'>These numbers come from <b>your inputs</b> "
        "on the Supply, Demand, Results, and Circular Economy pages. "
        "If they look wrong, go back and update those pages first.</p>",
        unsafe_allow_html=True,
    )

    # Recalculate from session state
    _sy  = st.session_state["start_year"]
    _ey  = st.session_state["end_year"]
    _yrs = list(range(_sy, _ey + 1))
    _n   = len(_yrs)

    _mine_base = st.session_state["mine_base_production"]
    _mine_gr   = st.session_state["mine_growth_rate"] / 100
    _mining    = [_mine_base * (1 + _mine_gr) ** i for i in range(_n)]

    _bp_val    = (st.session_state["bp_copper_anode"] * 1e6
                  * st.session_state["bp_te_content"] * 1e-6
                  * st.session_state["bp_yield"] / 100)
    _byp       = [_bp_val] * _n

    _rec_gr_sa = st.session_state.get("rec_retired_growth", 5.0) / 100
    _rec = [
        st.session_state["rec_retired_pv"] * (1 + _rec_gr_sa)**i * 1000
        * st.session_state["rec_te_intensity"]
        * st.session_state["rec_efficiency"] / 100
        * st.session_state["rec_collection"] / 100
        * st.session_state["rec_rate"] / 100 / 1000
        for i in range(_n)
    ]
    _rec_supply = _rec[0]

    _tot_sup = [_mining[i] + _byp[i] + _rec[i] for i in range(_n)]

    _pv_pgr  = st.session_state["pv_production_growth"] / 100
    _pv_sgr  = st.session_state["pv_share_growth"]
    _pv_dem  = [
        st.session_state["pv_production_start"] * (1 + _pv_pgr) ** i
        * min(st.session_state["pv_market_share_start"] + _pv_sgr * i, 100) / 100
        * st.session_state["pv_te_intensity"] / 1000
        for i in range(_n)
    ]
    _npv_dem = [
        st.session_state["nonpv_base"] * (1 + st.session_state["nonpv_growth"] / 100) ** i
        for i in range(_n)
    ]
    _tot_dem = [_pv_dem[i] + _npv_dem[i] for i in range(_n)]
    _gap     = [_tot_sup[i] - _tot_dem[i] for i in range(_n)]

    _gap_start = _gap[0]
    _gap_end   = _gap[-1]
    _gap_trend = "improving" if _gap_end > _gap_start else "worsening"
    _gap_label = "surplus" if _gap_end >= 0 else "shortage"
    _gap_color = "#2e7d32" if _gap_end >= 0 else "#c62828"

    # Summary cards
    _sc1, _sc2, _sc3, _sc4 = st.columns(4)
    _sc1.metric("Study period", f"{_sy} – {_ey}")
    _sc2.metric(f"Gap in {_sy}", f"{_gap_start:+,.2f} t")
    _sc3.metric(f"Gap in {_ey}", f"{_gap_end:+,.2f} t", delta=_gap_trend)
    _sc4.metric("Recycling supply", f"{_rec_supply:,.2f} t/yr")

    # Mini sparkline chart
    import plotly.graph_objects as _go_pb
    _fig_spark = _go_pb.Figure()
    _fig_spark.add_trace(_go_pb.Scatter(
        x=_yrs, y=_tot_sup, name="Supply", mode="lines",
        line=dict(color="#2e7d32", width=2),
    ))
    _fig_spark.add_trace(_go_pb.Scatter(
        x=_yrs, y=_tot_dem, name="Demand", mode="lines",
        line=dict(color="#c62828", width=2, dash="dash"),
    ))
    _fig_spark.add_trace(_go_pb.Scatter(
        x=_yrs, y=_gap, name="Gap", mode="lines+markers",
        line=dict(color="#1565c0", width=1.5),
        marker=dict(size=5),
    ))
    _fig_spark.add_hline(y=0, line_color="#888", line_width=1, line_dash="dot")
    _fig_spark.update_layout(
        height=220, margin=dict(t=10, b=10, l=0, r=0),
        plot_bgcolor="#f9fbe7", paper_bgcolor="#e8f5e9",
        font=dict(size=11, color="#1b5e20"),
        legend=dict(orientation="h", y=1.12),
        xaxis=dict(tickmode="array", tickvals=_yrs),
        yaxis=dict(title="Tonnes", hoverformat=",.2f"),
    )
    show_chart(_fig_spark, use_container_width=True)

    st.divider()

    # ── Brief instructions ────────────────────────────────────────────────────
    st.markdown(
        "<div style='background:#1b5e20;padding:16px 22px;border-radius:10px;margin-bottom:16px;'>"
        "<p style='color:white;font-size:15px;font-weight:700;margin:0 0 6px 0;'>"
        "Your Task</p>"
        "<p style='color:#e8f5e9;font-size:13px;line-height:1.8;margin:0;'>"
        "You are an engineering advisor writing a brief for a decision-maker at the US Department of Energy. "
        "Based on your analysis across all pages of this dashboard, answer the five questions below. "
        "Each answer should be <b>2–4 sentences</b>. Use evidence from your numbers and the LCA findings. "
        "There is no single right answer — you are being assessed on your <b>reasoning and justification</b>."
        "</p></div>",
        unsafe_allow_html=True,
    )

    # ── Five structured questions ──────────────────────────────────────────────
    st.subheader("Question 1 — Sourcing Strategy")
    st.markdown(
        "<p style='font-size:13px;color:#555;'>"
        "Based on the LCA results (location comparison), which country or region should the US "
        "prioritize for sourcing copper anode slimes to minimize environmental impact? "
        "Consider the trade-offs — no location wins on every impact category. "
        "Justify your choice by referencing at least two impact categories.</p>",
        unsafe_allow_html=True,
    )
    pb_sourcing = st.text_area(
        "Your answer:",
        value=st.session_state["pb_sourcing"],
        height=110,
        placeholder="e.g. I would recommend sourcing from Canada because... however this comes at the cost of...",
        key="ta_sourcing",
    )

    st.subheader("Question 2 — Processing Method")
    st.markdown(
        "<p style='font-size:13px;color:#555;'>"
        "Hydro-pyrometallurgical processing has a lower environmental footprint "
        "than hydrometallurgy across all four impact categories. Should all refineries switch to "
        "hydro-pyrometallurgy? What barriers or trade-offs might exist in practice?</p>",
        unsafe_allow_html=True,
    )
    pb_method = st.text_area(
        "Your answer:",
        value=st.session_state["pb_method"],
        height=110,
        placeholder="e.g. While hydro-pyrometallurgy is clearly preferable from an LCA standpoint, switching would require...",
        key="ta_method",
    )

    st.subheader("Question 3 — Circular Economy Strategy")
    st.markdown(
        "<p style='font-size:13px;color:#555;'>"
        "Your Results page shows a supply–demand gap of "
        f"<b>{_gap_end:+,.2f} tonnes in {_ey}</b>. "
        "Your recycling setting adds <b>{:.2f} tonnes/yr</b>. ".format(_rec_supply) +
        "Is recycling alone sufficient to close this gap? "
        "What combination of CE strategies (collection rate, recycling efficiency, "
        "material intensity reduction) would you recommend, and why?</p>",
        unsafe_allow_html=True,
    )
    pb_ce = st.text_area(
        "Your answer:",
        value=st.session_state["pb_ce"],
        height=110,
        placeholder="e.g. With my current settings, recycling provides X tonnes/yr which is [sufficient/insufficient] because...",
        key="ta_ce",
    )

    st.subheader("Question 4 — Supply Chain Risk")
    st.markdown(
        "<p style='font-size:13px;color:#555;'>"
        "Tellurium is a hitchhiker resource — its supply is controlled by copper production, "
        "not by Te demand. What does this mean for supply chain risk as CdTe solar scales up rapidly? "
        "Suggest one policy or industry action that could reduce this risk.</p>",
        unsafe_allow_html=True,
    )
    pb_risk = st.text_area(
        "Your answer:",
        value=st.session_state["pb_risk"],
        height=110,
        placeholder="e.g. Because Te supply cannot be directly increased in response to PV demand, the risk is... One policy response could be...",
        key="ta_risk",
    )

    st.subheader("Question 5 — Stress-Testing Your Strategy")
    st.markdown(
        "<p style='font-size:13px;color:#555;'>"
        "On the Circularity Reality Check page you saw how your recycling numbers change "
        "under three stress conditions: longer panel lifetime, thinner Te layers, and "
        "low collection rates. Does your circular economy strategy from Question 3 still "
        "hold under those conditions? If not, what would you change — and what "
        "trade-offs does that involve?</p>",
        unsafe_allow_html=True,
    )
    pb_stress = st.text_area(
        "Your answer:",
        value=st.session_state.get("pb_stress", ""),
        height=120,
        placeholder="e.g. Under 40-year panel lifetime, recycled Te does not arrive until 2065, so my CE strategy alone cannot close the 2035 gap. I would therefore also recommend...",
        key="ta_stress",
    )

    st.divider()

    # ── Save + generate PDF-ready report ─────────────────────────────────────
    col_btn1, col_btn2 = st.columns([1, 1])
    with col_btn1:
        if st.button("Save answers"):
            st.session_state["pb_sourcing"]       = pb_sourcing
            st.session_state["pb_method"]         = pb_method
            st.session_state["pb_ce"]             = pb_ce
            st.session_state["pb_risk"]           = pb_risk
            st.session_state["pb_stress"]         = pb_stress
            st.session_state["pb_submitted"]      = True
            st.success("Answers saved!")

    with col_btn2:
        # Build downloadable text report
        _name  = st.session_state["student_name"] or "Student"
        _sid   = st.session_state["student_id"]   or "—"
        _report = f"""SCENARIO ANALYSIS — TELLURIUM SUPPLY STRATEGY FOR US CdTe SOLAR
{'='*62}
Student : {_name}
ID      : {_sid}
Period  : {_sy} – {_ey}
Date    : Generated from Critical Materials for Solar: The Tellurium Case

SCENARIO SUMMARY
{'─'*40}
Gap in {_sy}  : {_gap_start:+,.2f} tonnes
Gap in {_ey}  : {_gap_end:+,.2f} tonnes  ({_gap_trend})
Recycling     : {_rec_supply:,.2f} tonnes/yr

QUESTION 1 — SOURCING STRATEGY
{'─'*40}
{pb_sourcing if pb_sourcing.strip() else '[Not answered]'}

QUESTION 2 — PROCESSING METHOD
{'─'*40}
{pb_method if pb_method.strip() else '[Not answered]'}

QUESTION 3 — CIRCULAR ECONOMY STRATEGY
{'─'*40}
{pb_ce if pb_ce.strip() else '[Not answered]'}

QUESTION 4 — SUPPLY CHAIN RISK
{'─'*40}
{pb_risk if pb_risk.strip() else '[Not answered]'}

QUESTION 5 — STRESS-TESTING YOUR STRATEGY
{'─'*40}
{st.session_state.get('pb_stress','') or '[Not answered]'}

{'='*62}
Source: Critical Materials for Solar: The Tellurium Case
"""
        _fname = f"ScenarioAnalysis_{_name.replace(' ','_')}_{_sy}_{_ey}.txt"
        st.download_button(
            label="Download scenario analysis (.txt)",
            data=_report,
            file_name=_fname,
            mime="text/plain",
        )

    st.divider()

    # ── Rubric ────────────────────────────────────────────────────────────────
    with st.expander("View grading rubric"):
        st.markdown(
            "<p style='font-size:13px;color:#555;margin-bottom:10px;'>"
            "Each question is worth 4 points. Total = 20 points.</p>",
            unsafe_allow_html=True,
        )
        _rubric = [
            ("4 — Excellent",   "#e8f5e9", "#2e7d32",
             "Answer uses specific numbers from the dashboard, "
             "explicitly addresses trade-offs, and gives a clear justified recommendation."),
            ("3 — Good",        "#f1f8e9", "#388e3c",
             "Answer is correct and references relevant concepts but may lack "
             "specific numbers or miss one trade-off."),
            ("2 — Developing",  "#fff8e1", "#f57f17",
             "Answer is partially correct or overly general. "
             "Concepts are identified but not connected to evidence."),
            ("1 — Beginning",   "#ffebee", "#c62828",
             "Answer is vague, incorrect, or simply restates the question "
             "without analysis or justification."),
            ("0 — Not answered","#f5f5f5", "#888",
             "No response provided."),
        ]
        for score, bg, tc, desc in _rubric:
            st.markdown(
                f"<div style='background:{bg};border-left:4px solid {tc};"
                f"padding:8px 14px;border-radius:6px;margin-bottom:6px;'>"
                f"<b style='color:{tc};font-size:13px;'>{score}</b>"
                f"<p style='font-size:12px;color:#333;margin:4px 0 0 0;'>{desc}</p>"
                f"</div>",
                unsafe_allow_html=True,
            )


# ─────────────────────────────────────────────────────────────────────────────
# PAGE: Circularity Reality Check
# ─────────────────────────────────────────────────────────────────────────────
elif page == "⚠️ Circularity Reality Check":
    st.header("Circularity Reality Check", divider="grey")
    st.markdown(
        "<div style='background:#fff3e0;border-left:5px solid #e65100;"
        "padding:14px 18px;border-radius:8px;margin-bottom:16px;'>"
        "<b style='color:#bf360c;font-size:15px;'>Challenge your assumptions</b><br>"
        "<p style='color:#333;font-size:14px;line-height:1.8;margin:8px 0 0 0;'>"
        "On the previous page you calculated how much Te recycling can recover. "
        "That calculation assumed ideal conditions. "
        "This page asks: <b>what happens when one assumption changes?</b> "
        "Real circular economy systems rarely operate under ideal conditions."
        "</p></div>",
        unsafe_allow_html=True,
    )

    import plotly.graph_objects as _go_crc
    import pandas as _pd_crc

    # ── Pull student's CE settings ─────────────────────────────────────────────
    _sy   = st.session_state["start_year"]
    _ey   = st.session_state["end_year"]
    _yrs  = list(range(_sy, _ey + 1))
    _n    = len(_yrs)

    _ret_base = st.session_state["rec_retired_pv"]
    _ret_gr   = st.session_state.get("rec_retired_growth", 5.0) / 100
    _ti_base  = st.session_state["rec_te_intensity"]
    _eff      = st.session_state["rec_efficiency"] / 100
    _col      = st.session_state["rec_collection"] / 100
    _rate     = st.session_state["rec_rate"] / 100

    def _calc_rec(ret_base, ret_gr, ti, eff, col, rate, n):
        return [
            ret_base * (1 + ret_gr)**i * 1000 * ti * eff * col * rate / 1000
            for i in range(n)
        ]

    # Base scenario (student's settings)
    _rec_base = _calc_rec(_ret_base, _ret_gr, _ti_base, _eff, _col, _rate, _n)

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 1 — Stress Test Your Numbers
    # ══════════════════════════════════════════════════════════════════════════
    st.subheader("1 — Stress Test: What If One Assumption Changes?")
    info_box(
        "Your CE page calculated recycled Te under your chosen settings. "
        "Below, three stress scenarios automatically recalculate that number. "
        "No new inputs needed — just see what happens."
    )

    # ── Stress scenario controls ───────────────────────────────────────────────
    _sc1, _sc2, _sc3 = st.columns(3)
    with _sc1:
        _lifetime = st.selectbox(
            "Panel lifetime",
            [25, 30, 35, 40],
            index=0,
            key="crc_lifetime",
            help="If panels last longer, the retirement wave arrives later — "
                 "delaying when recycled Te enters the supply chain.",
        )
    with _sc2:
        _ti_scenario = st.selectbox(
            "Te intensity trajectory",
            ["Constant (67 kg/MWp)",
             "Decreasing 2%/yr (technology improves slowly)",
             "Decreasing 5%/yr (technology improves fast)"],
            key="crc_ti_scenario",
            help="As CdTe efficiency improves, panels use less Te per MWp. "
                 "Retired panels in 2040 may contain far less Te than panels installed today.",
        )
    with _sc3:
        _col_stress = st.slider(
            "Collection rate (stress test)",
            min_value=0.0, max_value=100.0, step=5.0,
            value=10.0,
            key="crc_col_stress",
            help="Current US collection rate is ~10%. "
                 "Your CE page may have used a higher optimistic rate. "
                 "Drag this to see how collection rate affects recycled Te.",
        )

    # ── Compute stressed scenarios ─────────────────────────────────────────────
    # Scenario 1: Long lifetime — retirement delayed
    # Shift retirement wave: panels installed now retire in 'lifetime' years
    # Approximate: scale retired PV by fraction available given lifetime delay
    _delay_factor = 25.0 / _lifetime  # relative to 25-yr baseline
    _rec_s1 = _calc_rec(
        _ret_base * _delay_factor, _ret_gr, _ti_base, _eff, _col, _rate, _n
    )

    # Scenario 2: Declining Te intensity
    if "2%" in _ti_scenario:
        _ti_decline = 0.02
    elif "5%" in _ti_scenario:
        _ti_decline = 0.05
    else:
        _ti_decline = 0.0
    _rec_s2 = [
        _ret_base * (1 + _ret_gr)**i * 1000
        * (_ti_base * (1 - _ti_decline)**i)
        * _eff * _col * _rate / 1000
        for i in range(_n)
    ]

    # Scenario 3: Low collection rate (stress test slider)
    _rec_s3 = _calc_rec(
        _ret_base, _ret_gr, _ti_base, _eff, _col_stress / 100, _rate, _n
    )

    # ── Chart: 4 scenarios side by side ──────────────────────────────────────
    _fig_stress = _go_crc.Figure()
    _colors = ["#2e7d32", "#1565c0", "#e65100", "#c62828"]
    _labels = [
        f"Your settings ({_col*100:.2f}% collection, {_lifetime}-yr life, {_ti_base:.2f} kg/MWp)",
        f"Long lifetime ({_lifetime}-yr → delayed retirement wave)",
        f"Thin film ({_ti_scenario.split('(')[1].rstrip(')')})",
        f"Low collection ({_col_stress:.2f}% — current US reality)",
    ]
    _scenarios = [_rec_base, _rec_s1, _rec_s2, _rec_s3]

    for label, vals, color in zip(_labels, _scenarios, _colors):
        _fig_stress.add_trace(_go_crc.Scatter(
            x=_yrs, y=vals,
            name=label, mode="lines+markers",
            line=dict(color=color, width=2),
            marker=dict(size=5),
        ))

    _fig_stress.update_layout(
        xaxis=dict(title="Year", tickmode="array", tickvals=_yrs),
        yaxis=dict(title="Recycled Te (tonnes/yr)", hoverformat=",.2f"),
        legend=dict(orientation="h", y=-0.35, font=dict(size=10)),
        plot_bgcolor="#f9fbe7", paper_bgcolor="#e8f5e9",
        font=dict(color="#1b5e20"),
        margin=dict(t=20, b=10),
        height=360,
    )
    show_chart(_fig_stress, use_container_width=True)

    # ── Summary comparison table ───────────────────────────────────────────────
    _end_vals = [s[-1] for s in _scenarios]
    _pct_change = [
        (v - _rec_base[-1]) / max(_rec_base[-1], 0.001) * 100
        for v in _end_vals
    ]
    _stress_df = _pd_crc.DataFrame({
        "Scenario": [
            "Your settings (base)",
            f"Long lifetime ({_lifetime} yrs)",
            f"Thin film ({_ti_scenario.split('(')[0].strip()})",
            f"Low collection ({_col_stress:.2f}%)",
        ],
        f"Recycled Te in {_ey} (t)": [round(v, 2) for v in _end_vals],
        "Change vs. base": [
            "—",
            f"{_pct_change[1]:+.2f}%",
            f"{_pct_change[2]:+.2f}%",
            f"{_pct_change[3]:+.2f}%",
        ],
    })
    st.dataframe(
        _stress_df.set_index("Scenario").style.format({f"Recycled Te in {_ey} (t)": "{:,.2f}"}),
        use_container_width=True,
    )

    # ── Reflection prompt ──────────────────────────────────────────────────────
    _worst = min(_end_vals[1], _end_vals[2], _end_vals[3])
    _best  = _rec_base[-1]
    st.markdown(
        f"<div style='background:#fff8e1;border-left:5px solid #f57f17;"
        f"padding:12px 16px;border-radius:6px;font-size:13px;margin-top:8px;'>"
        f"<b>Think about this:</b> Your optimistic recycling scenario recovers "
        f"<b>{_best:,.2f} t/yr</b> by {_ey}. "
        f"Under the most stressed condition, that drops to <b>{_worst:,.2f} t/yr</b> — "
        f"a reduction of <b>{(1 - _worst/max(_best,0.001))*100:.2f}%</b>. "
        f"Does your supply strategy still work at that level?</div>",
        unsafe_allow_html=True,
    )

    st.divider()

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 2 — The Timing Mismatch
    # ══════════════════════════════════════════════════════════════════════════
    st.subheader("2 — The Timing Problem: When Does Recycled Te Actually Arrive?")
    st.markdown(
        "<p style='font-size:14px;line-height:1.8;'>"
        "Even if recycling works perfectly, it can only recover Te from panels that have "
        "already been <b>retired</b>. Panels installed today won't retire for 25–40 years. "
        "The Te shortage is projected for the <b>2030s</b>. "
        "That means recycled Te may arrive too late to close the gap when it matters most."
        "</p>",
        unsafe_allow_html=True,
    )

    _lt_sel = st.select_slider(
        "Panel lifetime (years) — drag to see when recycled Te becomes available:",
        options=[25, 30, 35, 40],
        value=25,
        key="crc_timing_lt",
    )

    # Timeline: install year 2025, retirement = 2025 + lifetime
    _install_yr   = 2025
    _retire_yr    = _install_yr + _lt_sel
    _shortage_yr  = 2035  # projected demand peak / shortage window

    # Build timeline figure
    _fig_time = _go_crc.Figure()
    _fig_time.update_layout(
        xaxis=dict(range=[2022, 2075], title="Year",
                   tickmode="array",
                   tickvals=list(range(2025, 2075, 5)),
                   showgrid=True, gridcolor="#e0e0e0"),
        yaxis=dict(visible=False, range=[0, 5]),
        plot_bgcolor="#f9fbe7", paper_bgcolor="#e8f5e9",
        font=dict(color="#1b5e20"),
        margin=dict(t=30, b=10),
        height=260,
        showlegend=True,
        legend=dict(orientation="h", y=1.12, font=dict(size=11)),
    )

    # Panel installation bar
    _fig_time.add_shape(type="rect", x0=2025, y0=2.6, x1=2027, y1=3.4,
                        fillcolor="#a5d6a7", line_color="#2e7d32", line_width=1.5)
    _fig_time.add_annotation(x=2026, y=3.0, text="<b>Panels<br>installed</b>",
                             showarrow=False, font=dict(size=10, color="#2e7d32"),
                             xref="x", yref="y")

    # In-use bar
    _fig_time.add_shape(type="rect", x0=2027, y0=2.6, x1=_retire_yr, y1=3.4,
                        fillcolor="#e8f5e9", line_color="#2e7d32",
                        line_width=1, line_dash="dot")
    _mid_use = (2027 + _retire_yr) / 2
    _fig_time.add_annotation(x=_mid_use, y=3.0,
                             text=f"In use ({_lt_sel} yrs)",
                             showarrow=False, font=dict(size=10, color="#555"),
                             xref="x", yref="y")

    # Recycled Te available bar
    _fig_time.add_shape(type="rect", x0=_retire_yr, y0=2.6, x1=_retire_yr+10, y1=3.4,
                        fillcolor="#b2ebf2", line_color="#006064", line_width=1.5)
    _fig_time.add_annotation(x=_retire_yr+5, y=3.0,
                             text="<b>Recycled Te<br>available</b>",
                             showarrow=False, font=dict(size=10, color="#006064"),
                             xref="x", yref="y")

    # Shortage window
    _fig_time.add_shape(type="rect", x0=2030, y0=1.4, x1=2045, y1=2.2,
                        fillcolor="#ffcdd2", line_color="#c62828", line_width=1.5)
    _fig_time.add_annotation(x=2037.5, y=1.8,
                             text="<b>Shortage window</b> (Te demand 7× by 2040)",
                             showarrow=False, font=dict(size=10, color="#c62828"),
                             xref="x", yref="y")

    # Overlap or gap indicator
    _overlap = _retire_yr <= 2045
    _fig_time.add_annotation(
        x=2048, y=3.0,
        text=(
            f"Recycled Te arrives in {_retire_yr}<br>"
            f"Overlaps shortage window"
            if _overlap else
            f"Recycled Te arrives in {_retire_yr}<br>"
            f"Too late for shortage window"
        ),
        showarrow=False,
        font=dict(size=11, color="#2e7d32" if _overlap else "#c62828"),
        bgcolor="#e8f5e9" if _overlap else "#ffebee",
        bordercolor="#2e7d32" if _overlap else "#c62828",
        borderwidth=1,
        xref="x", yref="y",
    )

    # Year markers
    for yr, label, color in [
        (_shortage_yr, "Shortage\nbegins", "#c62828"),
        (_retire_yr,   f"Panels\nretire ({_lt_sel}yr)", "#006064"),
    ]:
        _fig_time.add_vline(x=yr, line_color=color, line_width=1.5, line_dash="dash")
        _fig_time.add_annotation(x=yr, y=4.5, text=f"<b>{label}</b>",
                                 showarrow=False, font=dict(size=9, color=color),
                                 xref="x", yref="y")

    show_chart(_fig_time, use_container_width=True)

    if _lt_sel <= 30:
        st.markdown(
            f"<div style='background:#e8f5e9;border-left:5px solid #2e7d32;"
            f"padding:10px 14px;border-radius:6px;font-size:13px;'>"
            f"With a {_lt_sel}-year lifetime, panels installed in 2025 retire in {_retire_yr} — "
            f"within the shortage window. Recycling can contribute to closing the gap in time.</div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"<div style='background:#ffebee;border-left:5px solid #c62828;"
            f"padding:10px 14px;border-radius:6px;font-size:13px;'>"
            f"With a {_lt_sel}-year lifetime, panels installed in 2025 retire in {_retire_yr} — "
            f"<b>after the projected shortage window</b>. Recycling alone cannot address "
            f"the 2030s supply gap. Other strategies (friendshoring, substitution, Te stockpiling) "
            f"would be needed for that period.</div>",
            unsafe_allow_html=True,
        )

    st.divider()

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 3 — Cadmium Liability
    # ══════════════════════════════════════════════════════════════════════════
    st.subheader("3 — The Cadmium Liability: What Is Not Collected Becomes a Risk")
    st.markdown(
        "<p style='font-size:14px;line-height:1.8;'>"
        "Te recycling and Cd management are inseparable — they are in the same absorber layer. "
        "Every panel that is <b>not collected</b> for recycling is not just a missed Te "
        "recovery opportunity. It is a potential environmental liability: "
        "studies show that <b>62% of Cd in CdTe panels leaches into water within 360 days</b> "
        "of landfill exposure."
        "</p>",
        unsafe_allow_html=True,
    )

    _col_rate_cd = st.slider(
        "What collection rate do you think is realistic for your scenario? (%)",
        min_value=0.0, max_value=100.0, step=5.0,
        value=float(st.session_state["rec_collection"]),
        key="crc_cd_col",
        help="Move this to see how much Cd is at risk depending on collection rate.",
    )

    # Use student's retired PV (base year) × Cd content per GWp
    # Cd content: 64.4 kg/MWp = 64,400 kg/GWp
    _cd_per_gwp    = 64.4 * 1000  # kg/GWp
    _total_ret_gwp = _ret_base      # base year
    _cd_total      = _total_ret_gwp * _cd_per_gwp / 1000  # tonnes
    _cd_collected  = _cd_total * (_col_rate_cd / 100)
    _cd_not_col    = _cd_total * (1 - _col_rate_cd / 100)
    _cd_at_risk    = _cd_not_col * 0.62  # 62% leaching rate

    _cd1, _cd2, _cd3 = st.columns(3)
    _cd1.metric("Retired PV (base yr)", f"{_total_ret_gwp:.2f} GWp",
                help="From your CE page settings")
    _cd2.metric("Cd NOT collected", f"{_cd_not_col:,.2f} t",
                help=f"At {_col_rate_cd:.2f}% collection, {100-_col_rate_cd:.2f}% of panels go to landfill")
    _cd3.metric("Cd at risk of leaching", f"{_cd_at_risk:,.2f} t",
                delta=f"{_cd_at_risk:,.2f} t into water (360 days)",
                delta_color="inverse",
                help="62% of Cd in landfilled CdTe panels leaches into water within 360 days")

    # Visual: donut showing collected vs not collected
    _fig_cd = _go_crc.Figure(data=[_go_crc.Pie(
        labels=["Collected & recycled safely", "Not collected (landfill risk)"],
        values=[_col_rate_cd, 100 - _col_rate_cd],
        hole=0.55,
        marker_colors=["#2e7d32", "#c62828"],
        text=[f"{_col_rate_cd:.2f}%", f"{100 - _col_rate_cd:.2f}%"],
        textinfo="label+text",
        hovertemplate="%{label}<br>%{text}<extra></extra>",
        textfont=dict(size=12),
    )])
    _fig_cd.update_layout(
        plot_bgcolor="#f9fbe7", paper_bgcolor="#e8f5e9",
        font=dict(color="#1b5e20"),
        margin=dict(t=10, b=10),
        height=280,
        showlegend=False,
        annotations=[dict(text=f"{_col_rate_cd:.2f}%<br>collected",
                          x=0.5, y=0.5, font_size=14, showarrow=False,
                          font_color="#2e7d32")],
    )
    show_chart(_fig_cd, use_container_width=True)

    st.markdown(
        "<p style='font-size:13px;color:#555;'>"
        "This means the circular economy for CdTe is not just about Te supply security — "
        "it is also a <b>toxicity management obligation</b>. "
        "Low collection rates are not neutral: they actively create environmental harm.</p>",
        unsafe_allow_html=True,
    )

    st.divider()

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 4 — The Three Conditions
    # ══════════════════════════════════════════════════════════════════════════
    st.subheader("4 — Three Conditions for Circularity to Work")
    st.markdown(
        "<p style='font-size:14px;line-height:1.8;'>"
        "Circular economy works for CdTe <b>if and only if</b> three conditions are met "
        "simultaneously. A failure in any one of them undermines the whole system.</p>",
        unsafe_allow_html=True,
    )

    _conditions = [
        (
            "1", "Collection rate must be high",
            "> 60% needed for meaningful Te recovery",
            "Currently ~10% in the US",
            "Requires mandatory take-back policy or manufacturer responsibility laws",
            "#e3f2fd", "#1565c0",
            "Policy lever",
        ),
        (
            "2", "Timing must align with demand",
            "Recycled Te must arrive when the shortage exists",
            "Longer lifetimes push retirement — and recycled Te — decades into the future",
            "Strategic reserves, friendshoring, or substitution needed for the 2030s gap",
            "#fff8e1", "#f57f17",
            "Structural constraint",
        ),
        (
            "3", "Recycling process must be clean",
            "H₂SO₄/H₂O₂ leaching has its own LCA footprint",
            "Current process contributes 3–4% of total CdTe module lifecycle impact",
            "Emerging electrochemical recycling (in-situ H₂O₂ generation) may reduce this",
            "#fce4ec", "#c62828",
            "Technology lever",
        ),
    ]

    for num, title, need, problem, solution, bg, tc, lever in _conditions:
        st.markdown(
            f"<div style='background:{bg};border-left:6px solid {tc};"
            f"border-radius:8px;padding:14px 18px;margin-bottom:12px;'>"
            f"<div style='display:flex;align-items:center;gap:10px;margin-bottom:8px;'>"
            f"<div style='background:{tc};color:white;border-radius:50%;"
            f"min-width:28px;height:28px;display:flex;align-items:center;"
            f"justify-content:center;font-weight:700;font-size:13px;'>{num}</div>"
            f"<b style='color:{tc};font-size:15px;'>{title}</b>"
            f"<span style='background:{tc};color:white;padding:2px 10px;"
            f"border-radius:12px;font-size:11px;margin-left:auto;'>{lever}</span>"
            f"</div>"
            f"<div style='display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;"
            f"font-size:13px;color:#333;'>"
            f"<div><b style='color:{tc};'>What is needed</b><br>{need}</div>"
            f"<div><b style='color:{tc};'>The problem</b><br>{problem}</div>"
            f"<div><b style='color:{tc};'>The response</b><br>{solution}</div>"
            f"</div></div>",
            unsafe_allow_html=True,
        )

    st.divider()

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 5 — Overall Picture
    # ══════════════════════════════════════════════════════════════════════════
    st.subheader("5 — The Honest Picture: Circularity Is Conditional")

    # Spider / radar chart: how well does student's scenario meet each condition?
    _col_score   = min(100, (_col / 1.0) * 100)          # 0–100 based on their collection rate
    _timing_score = max(0, min(100, (45 - _lt_sel) / 20 * 100))  # 100 at 25yr, 0 at 45yr
    _eff_score   = (_eff * 100)                            # recycling efficiency as score

    _fig_radar = _go_crc.Figure()
    _fig_radar.add_trace(_go_crc.Scatterpolar(
        r=[_col_score, _timing_score, _eff_score, _col_score],
        theta=["Collection\nRate", "Timing\nAlignment", "Process\nCleanness", "Collection\nRate"],
        fill="toself",
        fillcolor="rgba(46,125,50,0.25)",
        line_color="#2e7d32",
        name="Your scenario",
    ))
    _fig_radar.add_trace(_go_crc.Scatterpolar(
        r=[60, 60, 60, 60],
        theta=["Collection\nRate", "Timing\nAlignment", "Process\nCleanness", "Collection\nRate"],
        fill="toself",
        fillcolor="rgba(198,40,40,0.08)",
        line=dict(color="#c62828", dash="dot", width=1.5),
        name="Minimum threshold",
    ))
    _fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], hoverformat=".2f",
                            ticksuffix="%", tickfont=dict(size=10)),
            bgcolor="#f9fbe7",
        ),
        paper_bgcolor="#e8f5e9",
        font=dict(color="#1b5e20"),
        legend=dict(orientation="h", y=-0.15),
        margin=dict(t=20, b=20),
        height=340,
    )
    show_chart(_fig_radar, use_container_width=True)

    _all_pass = _col_score >= 60 and _timing_score >= 60 and _eff_score >= 60
    if _all_pass:
        st.markdown(
            "<div style='background:#e8f5e9;border-left:5px solid #2e7d32;"
            "padding:12px 16px;border-radius:6px;font-size:13px;'>"
            "<b>Your scenario meets all three conditions.</b> "
            "Circular economy is likely to be effective under your assumptions. "
            "Now consider: are those assumptions realistic for the actual US policy and "
            "technology landscape?</div>",
            unsafe_allow_html=True,
        )
    else:
        _fails = []
        if _col_score < 60:
            _fails.append("collection rate is below the 60% threshold")
        if _timing_score < 60:
            _fails.append("panel lifetime creates a timing mismatch with the shortage window")
        if _eff_score < 60:
            _fails.append("recycling efficiency is below the minimum effective level")
        st.markdown(
            f"<div style='background:#fff3e0;border-left:5px solid #e65100;"
            f"padding:12px 16px;border-radius:6px;font-size:13px;'>"
            f"<b>Your scenario fails {len(_fails)} condition(s):</b> "
            f"{'; '.join(_fails)}. "
            f"This does not mean circularity is impossible — it means specific interventions "
            f"are needed before recycling can close the supply gap effectively.</div>",
            unsafe_allow_html=True,
        )

    st.markdown(
        "<div style='background:#1b5e20;padding:16px 22px;border-radius:10px;margin-top:16px;'>"
        "<p style='color:white;font-size:14px;font-weight:700;margin:0 0 6px 0;'>"
        "Key insight</p>"
        "<p style='color:#e8f5e9;font-size:13px;line-height:1.8;margin:0;'>"
        "Circular economy is not a default solution — it is a <b>conditional strategy</b>. "
        "It requires simultaneous progress on policy (collection), infrastructure (timing), "
        "and technology (clean recycling). Engineering judgment means knowing "
        "which condition is the binding constraint in a given context — "
        "and designing an intervention that targets that constraint specifically."
        "</p></div>",
        unsafe_allow_html=True,
    )

    st.divider()
    if st.button("Continue to LCA of CdTe Solar →"):
        go_to_page("🌍 LCA of CdTe Solar")
