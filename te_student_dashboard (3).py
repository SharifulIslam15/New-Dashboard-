import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Material Availability Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

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
hr { border-color: #a5d6a7 !important; }
[data-testid="stDataFrame"] { background-color: #f1f8e9 !important; }
.stDownloadButton > button {
    background-color: #66bb6a !important;
    color: white !important;
    border: none !important;
    border-radius: 6px !important;
}
</style>
""", unsafe_allow_html=True)

# ── Helpers ───────────────────────────────────────────────────────────────────
def info_box(text: str):
    st.markdown(
        f"<div style='background:#e8f5e9;border-left:4px solid #2e7d32;"
        f"padding:10px 14px;border-radius:6px;margin:8px 0;font-size:14px;'>{text}</div>",
        unsafe_allow_html=True,
    )

def go_to_page(name: str):
    """Save target page to session state and rerun — sidebar selectbox will follow."""
    st.session_state["_current_page"] = name
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
    # Policy Brief responses
    "pb_sourcing": "",
    "pb_method": "",
    "pb_ce": "",
    "pb_risk": "",
    "pb_recommendation": "",
    "pb_submitted": False,
    # Navigation
    "_current_page": "🏠 Welcome",
}

for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Sidebar navigation ────────────────────────────────────────────────────────
st.sidebar.title("Material Availability Dashboard")
st.sidebar.divider()

PAGES = [
    "🏠 Welcome",
    "👤 Student Info",
    "🔗 Hitchhiker Concept",
    "⛏️ Material Supply",
    "☀️ Material Demand",
    "📊 Results & Gap",
    "♻️ Circular Economy",
    "🌍 LCA of CdTe Solar",
    "🔍 Scenario Analysis",
]

# Session-state-driven navigation so go_to_page() works instantly
_idx = PAGES.index(st.session_state["_current_page"]) if st.session_state["_current_page"] in PAGES else 0
page = st.sidebar.selectbox("Navigate to", PAGES, index=_idx, key="_nav_select")
# Sync back if user manually clicks sidebar
if page != st.session_state["_current_page"]:
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
    "7. Study <b>LCA of CdTe Solar</b><br>"
    "8. Complete <b>Scenario Analysis</b></small>",
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: Welcome
# ─────────────────────────────────────────────────────────────────────────────
if page == "🏠 Welcome":
    col_a, col_b = st.columns([1.2, 1])

    with col_a:
        st.markdown(
            "<h1 style='color:#1b5e20;font-size:32px;margin-bottom:4px;'>"
            "🌞 Material Availability Dashboard</h1>"
            "<h3 style='color:#388e3c;font-weight:400;margin-top:0;'>"
            "Tellurium (Te) for CdTe Solar</h3>",
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

        info_box("⚠️ <b>Tip:</b> Complete the pages <i>in order</i> using the sidebar. "
                 "Enter your name on <b>Student Info</b> first.")

    with col_b:
        st.markdown("<h3 style='color:#2e7d32;'>Linear vs. Circular Economy</h3>", unsafe_allow_html=True)
        import plotly.graph_objects as _go

        # ── Use data coordinates throughout (xref/yref="x"/"y") ─────────────
        # All shapes, annotations, and scatter arrows live in the same x[0,10] y[0,10] space.
        _fig_ce = _go.Figure()
        _fig_ce.update_layout(
            xaxis=dict(visible=False, range=[0, 10]),
            yaxis=dict(visible=False, range=[0, 10]),
            plot_bgcolor="#f9fbe7", paper_bgcolor="#e8f5e9",
            margin=dict(l=8, r=8, t=8, b=8),
            height=430,
            showlegend=False,
        )

        def _rect(x0,y0,x1,y1,fill,line):
            _fig_ce.add_shape(type="rect",x0=x0,y0=y0,x1=x1,y1=y1,
                              fillcolor=fill,line_color=line,line_width=1.8)

        def _label(x,y,txt,color,size=11):
            _fig_ce.add_annotation(x=x,y=y,text=txt,showarrow=False,
                                   font=dict(size=size,color=color),xref="x",yref="y",align="center")

        def _arrow(x0,y0,x1,y1,color):
            # Draw arrow as scatter line ending with marker (triangle)
            _fig_ce.add_trace(_go.Scatter(
                x=[x0,x1], y=[y0,y1], mode="lines",
                line=dict(color=color, width=2.2),
                hoverinfo="skip",
            ))
            # Arrowhead as a triangle marker at the end point
            _fig_ce.add_trace(_go.Scatter(
                x=[x1], y=[y1], mode="markers",
                marker=dict(symbol="arrow", size=12, color=color,
                            angleref="previous", angle=0),
                hoverinfo="skip",
            ))

        # ── Section label: LINEAR ─────────────────────────────────────────────
        _label(5, 9.5, "<b>LINEAR — take → make → dispose</b>", "#555", 12)

        # Linear boxes
        _rect(0.1, 8.0, 2.1, 8.9, "#ef9a9a", "#b71c1c")
        _label(1.1, 8.5, "<b>Extract</b>", "#b71c1c", 11)
        _label(1.1, 8.15,"(mine Te)", "#b71c1c", 9)

        _rect(3.0, 8.0, 5.4, 8.9, "#ffe082", "#e65100")
        _label(4.2, 8.5, "<b>Manufacture</b>", "#e65100", 11)
        _label(4.2, 8.15,"PV panels", "#e65100", 9)

        _rect(6.3, 8.0, 8.3, 8.9, "#a5d6a7", "#2e7d32")
        _label(7.3, 8.5, "<b>In Use</b>", "#2e7d32", 11)
        _label(7.3, 8.15,"25 years", "#2e7d32", 9)

        _rect(8.7, 8.0, 9.9, 8.9, "#b0bec5", "#546e7a")
        _label(9.3, 8.5, "<b>🗑</b>", "#c62828", 13)
        _label(9.3, 8.15,"landfill", "#546e7a", 9)

        # Linear arrows (simple horizontal)
        for x0,x1 in [(2.1,3.0),(5.4,6.3),(8.3,8.7)]:
            _arrow(x0, 8.45, x1, 8.45, "#888")

        # Divider
        _fig_ce.add_shape(type="line", x0=0, y0=7.55, x1=10, y1=7.55,
                          line=dict(color="#ccc", width=1, dash="dot"))

        # ── Section label: CIRCULAR ───────────────────────────────────────────
        _label(5, 7.2, "<b>CIRCULAR — keep materials in use</b>", "#1565c0", 12)

        # Circular nodes (hexagon layout): top=Mine, right=Manufacture, right-low=In Use,
        # bottom=End of Life, left-low=Collect & Recycle, left=Recovered Material
        # Laid out as a two-row grid for clarity
        # Row 1 (y≈5.8): Mine | Manufacture | In Use
        # Row 2 (y≈3.5): Recovered | Collect | End of Life
        _cx = [1.2, 5.0, 8.8,   8.8, 5.0, 1.2]
        _cy = [5.8, 5.8, 5.8,   3.5, 3.5, 3.5]
        _clabels = ["Mining/<br>Byproduct", "Manufacture<br>PV Panel", "In Use<br>25+ yrs",
                    "End of<br>Life", "Collect &<br>Recycle Te", "Recovered<br>Material"]
        _cfill   = ["#ef9a9a","#ffe082","#a5d6a7","#ce93d8","#80cbc4","#b2dfdb"]
        _cline   = ["#b71c1c","#e65100","#2e7d32","#7b1fa2","#004d40","#00695c"]
        _ctxt    = ["#b71c1c","#e65100","#1b5e20","#4a148c","#004d40","#00695c"]

        for cx,cy,cl,cf,cln,ct in zip(_cx,_cy,_clabels,_cfill,_cline,_ctxt):
            _rect(cx-1.0, cy-0.55, cx+1.0, cy+0.55, cf, cln)
            lines = cl.split("<br>")
            offsets = [0.22, -0.18] if len(lines)==2 else [0]
            for line_txt, off in zip(lines, offsets):
                _label(cx, cy+off, f"<b>{line_txt}</b>", ct, 10)

        # Circular arrows: row1 left→right, then right col down, row2 right→left, then left col up
        # (0)Mine→(1)Manufacture, (1)→(2)InUse, (2)→(3)EndOfLife, (3)→(4)Collect, (4)→(5)Recovered, (5)→(1)Manufacture
        _flow = [(0,1),(1,2),(2,3),(3,4),(4,5),(5,0)]
        _flow_colors = ["#1565c0","#1565c0","#1565c0","#1565c0","#2e7d32","#2e7d32"]
        for (s,e),fc in zip(_flow, _flow_colors):
            sx,sy = _cx[s], _cy[s]
            ex,ey = _cx[e], _cy[e]
            # Midpoint routing to avoid overlap with boxes
            if sy == ey:  # horizontal
                _arrow(sx+1.0, sy, ex-1.0, ey, fc)
            elif sx == ex and sy > ey:  # downward right column
                _arrow(sx, sy-0.55, ex, ey+0.55, fc)
            elif sx == ex and sy < ey:  # upward left column
                _arrow(sx, sy+0.55, ex, ey-0.55, fc)
            else:
                _arrow(sx, sy, ex, ey, fc)

        # CE loop highlight label
        _label(5.0, 2.6, "♻️  CE loop reduces need for virgin mining", "#1565c0", 11)

        st.plotly_chart(_fig_ce, use_container_width=True)

    st.markdown(
        "<div style='background:#2e7d32;padding:16px 24px;border-radius:10px;"
        "text-align:center;margin-top:20px;'>"
        "<p style='color:white;font-size:15px;font-weight:700;margin:0;'>"
        "🚀 Ready? Select <b>Student Info</b> in the sidebar to begin →</p></div>",
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: Student Info
# ─────────────────────────────────────────────────────────────────────────────
elif page == "👤 Student Info":
    st.header("Student Information", divider="grey")
    info_box("Fill in your details and choose your study period. Press <b>Save</b> to continue.")

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input(
            "Your name *",
            value=st.session_state["student_name"],
            help="Enter your full name as it appears on your course roster.",
        )
        sid = st.text_input(
            "Student ID",
            value=st.session_state["student_id"],
            help="Optional — your MSU or course student ID.",
        )
    with col2:
        sy = st.number_input(
            "Study start year *",
            min_value=2024,
            max_value=2050,
            step=1,
            value=st.session_state["start_year"],
            help="First year of your analysis (e.g. 2025).",
        )
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

    info_box("💡 <b>Hitchhiker resource:</b> Te is mainly produced as a <i>byproduct of copper "
             "electrorefining</i> — its supply is tied to copper production, not to Te demand directly.")

    if st.button("💾 Save and continue →"):
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
        "🔗 What is a Hitchhiker Resource?</p>"
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
            "<div style='font-size:36px;text-align:center;'>🟠</div>"
            "<h4 style='color:#e65100;text-align:center;margin:8px 0;'>Copper (Cu)</h4>"
            "<p style='font-size:13px;line-height:1.8;color:#333;'>"
            "<b>Primary host.</b> Copper electrorefining is the <b>dominant source</b> of Te globally. "
            "During refining, copper ore is purified in large electrolytic cells. "
            "Te concentrates in the <i>anode slimes</i> (residue left on the anode), "
            "from which it can be extracted.</p>"
            "<div style='background:#fff3cd;border-radius:6px;padding:8px 12px;margin-top:10px;'>"
            "<p style='font-size:12px;margin:0;color:#856404;'>"
            "⚡ Typical Te content: <b>~110 ppm</b> in copper anode<br>"
            "🏭 Accounts for <b>~75–80%</b> of world Te supply"
            "</p></div></div>",
            unsafe_allow_html=True,
        )

    with col_ni:
        st.markdown(
            "<div style='background:#e8eaf6;border:2px solid #3949ab;border-radius:10px;"
            "padding:16px;min-height:280px;'>"
            "<div style='font-size:36px;text-align:center;'>⚫</div>"
            "<h4 style='color:#1a237e;text-align:center;margin:8px 0;'>Nickel (Ni)</h4>"
            "<p style='font-size:13px;line-height:1.8;color:#333;'>"
            "<b>Secondary host.</b> Some nickel ores also contain tellurium. "
            "In regions where nickel sulfide deposits are processed, Te is recovered "
            "as a secondary byproduct. This source is smaller but adds to the "
            "total available supply, especially in Canada and Russia.</p>"
            "<div style='background:#c5cae9;border-radius:6px;padding:8px 12px;margin-top:10px;'>"
            "<p style='font-size:12px;margin:0;color:#1a237e;'>"
            "🌍 Notable regions: <b>Canada, Russia, South Africa</b><br>"
            "📊 Accounts for <b>~5–15%</b> of world Te supply"
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
    _fig_hh = _go2.Figure()

    # Background
    _fig_hh.update_layout(
        xaxis=dict(visible=False, range=[0, 10]),
        yaxis=dict(visible=False, range=[0, 5]),
        plot_bgcolor="#f9fbe7", paper_bgcolor="#e8f5e9",
        margin=dict(l=10, r=10, t=10, b=10),
        height=260,
    )

    # Cu box
    _fig_hh.add_shape(type="rect", x0=0.2, y0=1.8, x1=2.8, y1=3.2,
                      fillcolor="#ffe082", line_color="#f9a825", line_width=2)
    _fig_hh.add_annotation(x=1.5, y=2.7, text="<b>Copper Mining</b>", showarrow=False,
                            font=dict(size=13, color="#e65100"))
    _fig_hh.add_annotation(x=1.5, y=2.3, text="& Electrorefining", showarrow=False,
                            font=dict(size=11, color="#e65100"))

    # Ni box
    _fig_hh.add_shape(type="rect", x0=0.2, y0=0.3, x1=2.8, y1=1.6,
                      fillcolor="#c5cae9", line_color="#3949ab", line_width=2)
    _fig_hh.add_annotation(x=1.5, y=1.1, text="<b>Nickel Mining</b>", showarrow=False,
                            font=dict(size=13, color="#1a237e"))
    _fig_hh.add_annotation(x=1.5, y=0.65, text="& Refining", showarrow=False,
                            font=dict(size=11, color="#1a237e"))

    # Arrow Cu → Te
    _fig_hh.add_annotation(x=4.5, y=2.7, ax=2.8, ay=2.7,
                            xref="x", yref="y", axref="x", ayref="y",
                            showarrow=True, arrowhead=2, arrowwidth=2.5, arrowcolor="#f9a825",
                            text="")
    _fig_hh.add_annotation(x=3.65, y=2.9, text="anode slimes", showarrow=False,
                            font=dict(size=10, color="#e65100"))

    # Arrow Ni → Te
    _fig_hh.add_annotation(x=4.5, y=1.1, ax=2.8, ay=1.1,
                            xref="x", yref="y", axref="x", ayref="y",
                            showarrow=True, arrowhead=2, arrowwidth=2.5, arrowcolor="#3949ab",
                            text="")
    _fig_hh.add_annotation(x=3.65, y=1.3, text="residues", showarrow=False,
                            font=dict(size=10, color="#1a237e"))

    # Te supply box
    _fig_hh.add_shape(type="rect", x0=4.5, y0=1.3, x1=7.0, y1=2.7,
                      fillcolor="#a5d6a7", line_color="#2e7d32", line_width=2)
    _fig_hh.add_annotation(x=5.75, y=2.2, text="<b>Tellurium (Te)</b>", showarrow=False,
                            font=dict(size=13, color="#1b5e20"))
    _fig_hh.add_annotation(x=5.75, y=1.75, text="supply pool", showarrow=False,
                            font=dict(size=11, color="#1b5e20"))

    # Arrow Te → CdTe
    _fig_hh.add_annotation(x=9.2, y=2.0, ax=7.0, ay=2.0,
                            xref="x", yref="y", axref="x", ayref="y",
                            showarrow=True, arrowhead=2, arrowwidth=2.5, arrowcolor="#2e7d32",
                            text="")

    # CdTe PV box
    _fig_hh.add_shape(type="rect", x0=7.2, y0=1.3, x1=9.8, y1=2.7,
                      fillcolor="#b2ebf2", line_color="#00838f", line_width=2)
    _fig_hh.add_annotation(x=8.5, y=2.2, text="<b>CdTe Solar</b>", showarrow=False,
                            font=dict(size=13, color="#006064"))
    _fig_hh.add_annotation(x=8.5, y=1.75, text="panels", showarrow=False,
                            font=dict(size=11, color="#006064"))

    # Key constraint label
    _fig_hh.add_annotation(
        x=5.75, y=3.5,
        text="⚠️  Te supply is controlled by Cu & Ni output, not by Te demand",
        showarrow=False, font=dict(size=11, color="#c62828"),
        bgcolor="#ffebee", bordercolor="#c62828", borderwidth=1,
    )

    st.plotly_chart(_fig_hh, use_container_width=True)



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
        "100 t × (1 + 0.05)^1 = 105 t",
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
        f"📌 Mining supply in year 1 ({st.session_state['start_year'] + 1}): "
        f"<b>{preview_mine:.1f} tonnes</b></div>",
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
        f"29,000,000 t × 110×10⁻⁶ × 0.50 = 1,595 t",
    )

    bp_cu   = st.session_state["bp_copper_anode"]
    bp_ppm  = st.session_state["bp_te_content"]
    bp_yld  = st.session_state["bp_yield"]
    bp_supply = bp_cu * 1e6 * bp_ppm * 1e-6 * (bp_yld / 100)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Copper anode production", f"{bp_cu:.0f} M t/yr")
    c2.metric("Te content in anode", f"{bp_ppm:.0f} ppm")
    c3.metric("Recovery yield", f"{bp_yld:.0f}%")
    c4.metric("By-production supply", f"{bp_supply:,.0f} t/yr")

    info_box("🔒 By-production parameters are fixed at lecture defaults. "
             "This reflects that Te supply is largely controlled by <b>copper production</b>, "
             "not by Te-specific demand.")

    st.divider()
    if st.button("💾 Save supply inputs →"):
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
        "626.71 × 0.0727 × 24800/1000 = 1,129 t",
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
        f"📌 PV demand in start year ({st.session_state['start_year']}): "
        f"<b>{pv_dem_preview:,.0f} tonnes</b></div>",
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
        "455 × (1 + 0.04)^1 = 473.2 t",
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
        f"📌 Non-PV demand in year 1 ({st.session_state['start_year'] + 1}): "
        f"<b>{npv_preview:,.1f} tonnes</b></div>",
        unsafe_allow_html=True,
    )

    st.divider()
    if st.button("💾 Save demand inputs →"):
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
    rec_val_t = rec_ret * 1000 * rec_ti * rec_eff * rec_col * rec_rate / 1000  # convert kg to tonnes
    recycling = [rec_val_t] * n_yrs

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
    m1.metric("Supply (start yr)", f"{total_supply[0]:,.0f} t")
    m2.metric("Demand (start yr)", f"{total_demand[0]:,.0f} t")
    gap0 = gap[0]
    m3.metric("Gap (start yr)", f"{gap0:+,.0f} t", delta="Surplus" if gap0 >= 0 else "Shortage")
    m4.metric("Gap (end yr)", f"{gap[-1]:+,.0f} t", delta="Surplus" if gap[-1] >= 0 else "Shortage")

    st.divider()

    # ── Detailed results table ────────────────────────────────────────────────
    st.subheader("Year-by-year Results")
    df = pd.DataFrame({
        "Year": years,
        "Mining (t)": [round(v, 1) for v in mining],
        "By-production (t)": [round(v, 1) for v in byproduct],
        "Recycling (t)": [round(v, 1) for v in recycling],
        "Total Supply (t)": [round(v, 1) for v in total_supply],
        "PV Demand (t)": [round(v, 1) for v in pv_demand],
        "Non-PV Demand (t)": [round(v, 1) for v in nonpv_demand],
        "Total Demand (t)": [round(v, 1) for v in total_demand],
        "Gap (t)": [round(v, 1) for v in gap],
    })
    st.dataframe(df.set_index("Year"), use_container_width=True)

    # ── Charts ────────────────────────────────────────────────────────────────
    st.divider()
    st.subheader("Supply vs. Demand")

    tab1, tab2, tab3 = st.tabs(["📈 Supply & Demand Overview", "🔍 Supply Breakdown", "⚖️ Gap Chart"])

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
        fig1.update_yaxes(showline=True, mirror=True, ticks="outside")
        st.plotly_chart(fig1, use_container_width=True)

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
        fig2.update_yaxes(showline=True, mirror=True, ticks="outside")
        st.plotly_chart(fig2, use_container_width=True)

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
        fig3.update_yaxes(showline=True, mirror=True, ticks="outside", zeroline=True)
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown(
            "<p style='font-size:13px;color:#555;'>🟢 Green bars = surplus (supply > demand) &nbsp;|&nbsp; "
            "🔴 Red bars = shortage (demand > supply)</p>",
            unsafe_allow_html=True,
        )

    st.divider()

    # ── Insight box ───────────────────────────────────────────────────────────
    final_gap = gap[-1]
    if final_gap >= 0:
        st.markdown(
            f"<div style='background:#e8f5e9;border-left:5px solid #2e7d32;"
            f"padding:14px 18px;border-radius:8px;'>"
            f"<b style='color:#1b5e20;'>✅ Surplus in final year ({ey}): +{final_gap:,.0f} tonnes</b><br>"
            f"<span style='font-size:13px;'>Supply exceeds demand under your scenario. "
            f"Global stocks would be building up.</span></div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"<div style='background:#fff3e0;border-left:5px solid #e65100;"
            f"padding:14px 18px;border-radius:8px;'>"
            f"<b style='color:#bf360c;'>⚠️ Shortage in final year ({ey}): {final_gap:,.0f} tonnes</b><br>"
            f"<span style='font-size:13px;'>Demand exceeds supply. Circular Economy strategies "
            f"(recycling) could help close this gap — explore the <b>Circular Economy</b> page.</span></div>",
            unsafe_allow_html=True,
        )

    # ── Download ──────────────────────────────────────────────────────────────
    st.divider()
    csv_data = df.to_csv(index=False)
    fname = f"Te_gap_{st.session_state['student_name'].replace(' ','_')}_{sy}_{ey}.csv"
    st.download_button(
        label="⬇️ Download results as CSV",
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
        "<b style='color:#2e7d32;'>♻️ Recycle</b><br>"
        "<span style='font-size:13px;'>Recover Te from end-of-life CdTe panels. "
        "~90% recovery efficiency is technically achievable.</span></div>",
        unsafe_allow_html=True,
    )
    c2.markdown(
        "<div style='background:#f1f8e9;border-radius:8px;padding:14px;min-height:120px;'>"
        "<b style='color:#2e7d32;'>⛏️ Urban Mining</b><br>"
        "<span style='font-size:13px;'>Recover Te from decommissioned panels and installed PV fleets, "
        "supplementing primary supply as stocks decline.</span></div>",
        unsafe_allow_html=True,
    )
    c3.markdown(
        "<div style='background:#f1f8e9;border-radius:8px;padding:14px;min-height:120px;'>"
        "<b style='color:#2e7d32;'>🔬 Reduce Intensity</b><br>"
        "<span style='font-size:13px;'>Technology improvements already cut Te intensity from "
        "~100 kg/MWp to ~24 kg/MWp. Further reductions directly cut PV demand.</span></div>",
        unsafe_allow_html=True,
    )

    st.divider()
    st.subheader("Recycling Calculator")
    formula_box(
        "Recycled Te from retired panels",
        "Te_rec = Retired_PV (GWp) × 1000 × Te_Intensity (kg/MWp) × Rec_Eff × Collection_Rate × Recycle_Rate / 1000",
        "10 GWp × 1000 × 67 kg/MWp × 0.90 × 0.85 × 1.00 / 1000 = 512.6 t",
    )

    col1, col2 = st.columns(2)
    with col1:
        rec_ret = st.slider(
            "Retired PV capacity (GWp/yr)",
            min_value=0.0, max_value=500.0, step=5.0,
            value=float(st.session_state["rec_retired_pv"]),
            help="How many GWp of old CdTe panels are decommissioned each year and available for recycling.",
        )
        rec_ti = st.slider(
            "Te intensity in panels (kg/MWp)",
            min_value=10.0, max_value=100.0, step=1.0,
            value=float(st.session_state["rec_te_intensity"]),
            help="Amount of Tellurium per MWp in the panels being retired. Lecture default = 67 kg/MWp.",
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
            help="What fraction of retired panels are actually collected for recycling (vs going to landfill). "
                 "This is the key policy lever.",
        )
        rec_rate = st.slider(
            "Recycle rate of collected panels (%)",
            min_value=10.0, max_value=100.0, step=5.0,
            value=float(st.session_state["rec_rate"]),
            help="Of the panels collected, what % actually go through the recycling process.",
        )

    # Live recycling calculation
    rec_supply = rec_ret * 1000 * rec_ti * (rec_eff / 100) * (rec_col / 100) * (rec_rate / 100) / 1000

    st.markdown(
        f"<div style='background:#e8f5e9;border:2px solid #2e7d32;border-radius:8px;"
        f"padding:14px 18px;margin:12px 0;font-size:15px;text-align:center;'>"
        f"♻️ <b>Recycled Te supply: {rec_supply:,.1f} tonnes/yr</b></div>",
        unsafe_allow_html=True,
    )

    # ── Impact on gap ─────────────────────────────────────────────────────────
    st.divider()
    st.subheader("Impact on the Supply–Demand Gap")

    if st.button("💾 Apply recycling to Results page →"):
        st.session_state["rec_retired_pv"]  = rec_ret
        st.session_state["rec_te_intensity"] = rec_ti
        st.session_state["rec_efficiency"]   = rec_eff
        st.session_state["rec_collection"]   = rec_col
        st.session_state["rec_rate"]         = rec_rate
        st.session_state["calculated"]       = False
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

    gap_no_rec = [mining[i] + byproduct[i] - total_dem[i] for i in range(n_yrs)]
    gap_with_rec = [mining[i] + byproduct[i] + rec_supply - total_dem[i] for i in range(n_yrs)]

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
    fig_ce.update_yaxes(showline=True, mirror=True, ticks="outside")
    st.plotly_chart(fig_ce, use_container_width=True)

    diff = rec_supply * n_yrs
    st.markdown(
        f"<p style='font-size:13px;color:#555;'>"
        f"With these recycling settings, recycling adds <b>{rec_supply:,.1f} t/yr</b> of Te supply, "
        f"improving the gap by <b>{rec_supply:,.1f} t</b> each year.</p>",
        unsafe_allow_html=True,
    )

    # ── CE definition ─────────────────────────────────────────────────────────
    st.divider()
    st.markdown(
        "<div style='background:#1b5e20;padding:18px 24px;border-radius:10px;margin-bottom:12px;'>"
        "<p style='color:#fff;font-size:18px;font-weight:bold;margin:0;'>"
        "♻️ What is Circular Economy?</p></div>",
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

    # ── What is LCA ───────────────────────────────────────────────────────────
    st.subheader("1 — What is Life Cycle Assessment?")
    st.markdown(
        "<p style='font-size:14px;line-height:1.8;'>"
        "Life Cycle Assessment (LCA) is a method to estimate the <b>total environmental "
        "footprint</b> of a product — from raw material extraction all the way to end of life. "
        "For CdTe solar modules, that means tracking the environmental cost of every step: "
        "mining copper, smelting, electrorefining, processing anode slimes, refining tellurium, "
        "and finally manufacturing the solar panel.</p>",
        unsafe_allow_html=True,
    )

    # 4-phase LCA cards
    phases = [
        ("1", "Goal & Scope", "Define what you are studying and where the system boundary is. "
         "This study covers copper mining → CdTe solar module.",
         "#e8f5e9", "#2e7d32"),
        ("2", "Life Cycle Inventory (LCI)", "Collect all material and energy inputs/outputs at "
         "each stage. Chemicals, electricity, water, waste.",
         "#e3f2fd", "#1565c0"),
        ("3", "Impact Assessment (LCIA)", "Convert the inventory into environmental impact scores: "
         "GWP, water use, freshwater toxicity, abiotic depletion.",
         "#fff8e1", "#f57f17"),
        ("4", "Interpretation", "Compare scenarios, identify hotspots, draw conclusions "
         "for decision-makers and policymakers.",
         "#fce4ec", "#c62828"),
    ]
    cols = st.columns(4)
    for col, (num, title, desc, bg, tc) in zip(cols, phases):
        col.markdown(
            f"<div style='background:{bg};border-radius:8px;padding:14px;min-height:160px;'>"
            f"<div style='background:{tc};color:white;border-radius:50%;width:26px;height:26px;"
            f"display:flex;align-items:center;justify-content:center;font-weight:700;"
            f"font-size:12px;margin-bottom:8px;'>{num}</div>"
            f"<b style='color:{tc};font-size:13px;'>{title}</b>"
            f"<p style='font-size:12px;color:#333;margin-top:6px;line-height:1.6;'>{desc}</p>"
            f"</div>",
            unsafe_allow_html=True,
        )

    st.divider()

    # ── System boundary diagram ───────────────────────────────────────────────
    st.subheader("2 — System Boundary: 7 Stages from Mine to Module")
    info_box(
        "The study tracks the full supply chain. The arrow below shows where environmental "
        "impact accumulates — <b>copper mining & beneficiation dominates all impact categories</b>, "
        "followed by anode slime processing."
    )

    _stages = [
        ("Cu Mining &\nBeneficiation", "#ef9a9a", "#b71c1c", "LARGEST\ncontributor"),
        ("Cu Concentrate\nSmelting",    "#ffe082", "#e65100", ""),
        ("Cu Anode\nElectrorefining",   "#fff9c4", "#f57f17", ""),
        ("Anode Slime\nProcessing",     "#ce93d8", "#6a1b9a", "2nd largest\ncontributor"),
        ("Te Refining\n(SG-Te)",        "#a5d6a7", "#2e7d32", ""),
        ("SG-CdTe\nProduction",         "#80cbc4", "#00695c", ""),
        ("CdTe Solar\nModule (PV)",     "#b2ebf2", "#006064", "Final\nproduct"),
    ]

    import plotly.graph_objects as _go_lca
    _fig_sb = _go_lca.Figure()
    _fig_sb.update_layout(
        xaxis=dict(visible=False, range=[0, 15.5]),
        yaxis=dict(visible=False, range=[0, 3.2]),
        plot_bgcolor="#f9fbe7", paper_bgcolor="#e8f5e9",
        margin=dict(l=5, r=5, t=5, b=5),
        height=160, showlegend=False,
    )
    for i, (label, bg, tc, note) in enumerate(_stages):
        x0, x1 = i * 2.2, i * 2.2 + 1.9
        _fig_sb.add_shape(type="rect", x0=x0, y0=0.6, x1=x1, y1=2.4,
                          fillcolor=bg, line_color=tc, line_width=1.8)
        for j, ln in enumerate(label.split("\n")):
            _fig_sb.add_annotation(x=(x0+x1)/2, y=1.8 - j*0.55, text=f"<b>{ln}</b>",
                                   showarrow=False, font=dict(size=9, color=tc), xref="x", yref="y")
        if note:
            for j, ln in enumerate(note.split("\n")):
                _fig_sb.add_annotation(x=(x0+x1)/2, y=0.38 - j*0.28, text=ln,
                                       showarrow=False, font=dict(size=8, color=tc), xref="x", yref="y")
        if i < len(_stages) - 1:
            _fig_sb.add_trace(_go_lca.Scatter(
                x=[x1, x1+0.15], y=[1.5, 1.5], mode="lines",
                line=dict(color="#555", width=1.8), hoverinfo="skip",
            ))
            _fig_sb.add_trace(_go_lca.Scatter(
                x=[x1+0.15], y=[1.5], mode="markers",
                marker=dict(symbol="arrow", size=10, color="#555", angle=90),
                hoverinfo="skip",
            ))
    st.plotly_chart(_fig_sb, use_container_width=True)

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
        ["⚗️ Hydrometallurgy (HM)", "🔥 Hydro-Pyrometallurgy (HPM)"],
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
        text=[f"{v}" for v in _selected_vals],
        textposition="outside",
        name="Selected method",
    ))
    _fig_method.add_trace(_go_lca.Bar(
        x=_impact_cats, y=_baseline_vals,
        marker_color=["rgba(150,150,150,0.35)"] * 4,
        text=[f"{v}" for v in _baseline_vals],
        textposition="outside",
        name="Other method",
    ))
    _fig_method.update_layout(
        barmode="group",
        yaxis=dict(title="Relative impact (HPM baseline = 100)", range=[0, 175]),
        xaxis=dict(title="Impact category"),
        legend=dict(orientation="h", y=1.1),
        plot_bgcolor="#f9fbe7", paper_bgcolor="#e8f5e9",
        font=dict(color="#1b5e20"),
        margin=dict(t=30, b=10),
        height=340,
    )
    st.plotly_chart(_fig_method, use_container_width=True)

    if _is_hm:
        st.markdown(
            "<div style='background:#ffebee;border-left:5px solid #c62828;"
            "padding:12px 16px;border-radius:6px;font-size:13px;'>"
            "⚗️ <b>Hydrometallurgy</b> uses more chemicals (HCl, H₂O₂, H₂SO₄, dibutyl carbitol) "
            "and recovers Te only at the <i>final</i> reduction step — after bearing the environmental "
            "cost of recovering silver, gold, and selenium first. This leads to "
            "<b>37–51% higher impacts</b> compared to hydro-pyrometallurgy.</div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            "<div style='background:#e8f5e9;border-left:5px solid #2e7d32;"
            "padding:12px 16px;border-radius:6px;font-size:13px;'>"
            "🔥 <b>Hydro-Pyrometallurgy</b> recovers tellurium early in the process "
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
        text=[f"{v}" for v in _loc_scores],
        textposition="outside",
    ))
    _fig_loc.add_hline(y=50, line_dash="dot", line_color="#888",
                       annotation_text="50 — midpoint", annotation_position="right")
    _fig_loc.update_layout(
        yaxis=dict(title="Relative impact (worst case = 100)", range=[0, 120]),
        xaxis=dict(title="Impact category"),
        plot_bgcolor="#f9fbe7", paper_bgcolor="#e8f5e9",
        font=dict(color="#1b5e20"),
        margin=dict(t=20, b=10),
        height=320,
        showlegend=False,
    )
    st.plotly_chart(_fig_loc, use_container_width=True)

    # Per-location insight
    _loc_insights = {
        "China (CN) — Jiangxi Copper": (
            "#ffebee", "#c62828",
            "🇨🇳 China has the <b>highest water scarcity footprint</b> — despite using less water than Canada, "
            "China's water scarcity characterization factor (CF) is 10× Canada's and 3× the US. "
            "It also leads in freshwater toxicity and abiotic depletion."
        ),
        "Canada (CA) — Glencore CCR": (
            "#e8f5e9", "#2e7d32",
            "🇨🇦 Canada has the <b>lowest carbon footprint and energy demand</b> thanks to its clean electricity grid. "
            "However, Canada has the <b>highest freshwater toxicity and ADP</b> — driven by its very high "
            "copper sulfide ore concentration (low copper-to-molybdenum ratio = only 4.36% of mining impacts "
            "allocated to molybdenum, vs. >20% elsewhere)."
        ),
        "Japan (JP) — JX Metals Saganoseki": (
            "#fff8e1", "#e65100",
            "🇯🇵 Japan (SC3) has the <b>highest carbon footprint of all scenarios</b> because it imports "
            "copper concentrate from Chile — ~20,000 km by sea + 174 km by truck. "
            "Transportation adds significant GWP despite Chile having a cleaner grid."
        ),
        "USA (US) — Rio Tinto Kennecott": (
            "#e3f2fd", "#1565c0",
            "🇺🇸 The US has the <b>lowest freshwater toxicity and abiotic depletion</b> among all scenarios. "
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

    # ── Literature underestimation ────────────────────────────────────────────
    st.subheader("5 — Why Prior Estimates Were Wrong")
    st.markdown(
        "<p style='font-size:14px;line-height:1.8;'>"
        "Most previous LCA studies used <b>proxy data from electronic scrap processing</b> to model "
        "anode slime treatment — not actual commercial tellurium recovery processes. "
        "This led to systematic underestimation of Te's environmental footprint.</p>",
        unsafe_allow_html=True,
    )

    _underest = [
        ("Carbon footprint\n(SG-Te)", 46, "Previous studies underestimate Te carbon footprint by up to 46%"),
        ("Cumulative\nEnergy Demand", 78, "Cumulative energy demand underestimated by up to 78%"),
        ("Freshwater\nToxicity (module)", 35, "CdTe module freshwater toxicity underestimated by 35%"),
        ("Abiotic Depletion\nPotential (module)", 50, "CdTe module ADP underestimated by 50%"),
    ]

    _fig_ue = _go_lca.Figure()
    _fig_ue.add_trace(_go_lca.Bar(
        x=[u[0] for u in _underest],
        y=[u[1] for u in _underest],
        marker_color=["#e65100", "#f57f17", "#c62828", "#880e4f"],
        text=[f"Up to {u[1]}% underestimated" for u in _underest],
        textposition="outside",
        customdata=[u[2] for u in _underest],
        hovertemplate="%{customdata}<extra></extra>",
    ))
    _fig_ue.update_layout(
        yaxis=dict(title="Underestimation (%)", range=[0, 95]),
        xaxis=dict(title="Impact category"),
        plot_bgcolor="#f9fbe7", paper_bgcolor="#e8f5e9",
        font=dict(color="#1b5e20"),
        margin=dict(t=20, b=10),
        height=320,
        showlegend=False,
    )
    st.plotly_chart(_fig_ue, use_container_width=True)

    st.markdown(
        "<p style='font-size:13px;color:#555;'>"
        "Two root causes: (1) ecoinvent allocated mining impacts using <b>global average</b> "
        "copper-to-molybdenum ratios instead of country-specific ones; "
        "(2) the ecoinvent inventory <b>excluded key chemicals</b> used in anode slime leaching "
        "(H₂SO₄, HCl, H₂O₂, dibutyl carbitol, oxalic acid).</p>",
        unsafe_allow_html=True,
    )

    st.divider()

    # ── Real-world scale ───────────────────────────────────────────────────────
    st.subheader("6 — Putting It in Perspective")
    st.markdown(
        "<p style='font-size:14px;'>What does the underestimation actually mean at US scale?</p>",
        unsafe_allow_html=True,
    )

    _c1, _c2, _c3 = st.columns(3)
    _c1.markdown(
        "<div style='background:#fff8e1;border-radius:8px;padding:16px;text-align:center;'>"
        "<div style='font-size:32px;'>⚡</div>"
        "<p style='font-size:13px;color:#e65100;margin:6px 0;'><b>US CdTe PV in 2024</b></p>"
        "<p style='font-size:22px;font-weight:700;color:#e65100;'>8.82 GW</p>"
        "<p style='font-size:12px;color:#555;'>CdTe PV installations<br>(21% US market share)</p>"
        "</div>", unsafe_allow_html=True,
    )
    _c2.markdown(
        "<div style='background:#ffebee;border-radius:8px;padding:16px;text-align:center;'>"
        "<div style='font-size:32px;'>🏭</div>"
        "<p style='font-size:13px;color:#c62828;margin:6px 0;'><b>Carbon underestimation</b></p>"
        "<p style='font-size:22px;font-weight:700;color:#c62828;'>0.11 M tonnes</p>"
        "<p style='font-size:12px;color:#555;'>equivalent to burning<br>0.11 million tonnes of coal</p>"
        "</div>", unsafe_allow_html=True,
    )
    _c3.markdown(
        "<div style='background:#fce4ec;border-radius:8px;padding:16px;text-align:center;'>"
        "<div style='font-size:32px;'>⛏️</div>"
        "<p style='font-size:13px;color:#880e4f;margin:6px 0;'><b>ADP underestimation</b></p>"
        "<p style='font-size:22px;font-weight:700;color:#880e4f;'>352 tonnes</p>"
        "<p style='font-size:12px;color:#555;'>of silver-equivalent<br>resource depletion missed</p>"
        "</div>", unsafe_allow_html=True,
    )

    st.divider()

    # ── Key takeaways ─────────────────────────────────────────────────────────
    st.subheader("7 — Key Takeaways")
    _takeaways = [
        ("🌱", "Location matters",
         "Sourcing and processing anode slimes in Canada or the US reduces carbon footprint and water scarcity — "
         "supporting reshoring and friendshoring strategies."),
        ("⚗️", "Method matters",
         "Hydro-pyrometallurgical processing consistently outperforms hydrometallurgy across all "
         "four impact categories. The US and Canada both already use this method."),
        ("📊", "Old data underestimates impact",
         "Prior LCA studies missed key chemicals and used global-average allocation. "
         "This underestimates Te's carbon footprint by up to 46% and the module's ADP by 50%."),
        ("♻️", "Circular Economy reduces the burden",
         "Recycling retired CdTe panels reduces demand for newly mined Te — directly cutting "
         "the upstream environmental impacts shown here."),
    ]
    for icon, title, desc in _takeaways:
        st.markdown(
            f"<div style='display:flex;align-items:flex-start;gap:14px;"
            f"background:#f1f8e9;border-radius:8px;padding:12px 16px;margin-bottom:8px;'>"
            f"<div style='font-size:24px;'>{icon}</div>"
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

    _rec_supply = (st.session_state["rec_retired_pv"] * 1000
                   * st.session_state["rec_te_intensity"]
                   * st.session_state["rec_efficiency"] / 100
                   * st.session_state["rec_collection"] / 100
                   * st.session_state["rec_rate"] / 100
                   / 1000)
    _rec = [_rec_supply] * _n

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
    _sc2.metric(f"Gap in {_sy}", f"{_gap_start:+,.0f} t")
    _sc3.metric(f"Gap in {_ey}", f"{_gap_end:+,.0f} t", delta=_gap_trend)
    _sc4.metric("Recycling supply", f"{_rec_supply:,.1f} t/yr")

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
        yaxis=dict(title="Tonnes"),
    )
    st.plotly_chart(_fig_spark, use_container_width=True)

    st.divider()

    # ── Brief instructions ────────────────────────────────────────────────────
    st.markdown(
        "<div style='background:#1b5e20;padding:16px 22px;border-radius:10px;margin-bottom:16px;'>"
        "<p style='color:white;font-size:15px;font-weight:700;margin:0 0 6px 0;'>"
        "📋 Your Task</p>"
        "<p style='color:#e8f5e9;font-size:13px;line-height:1.8;margin:0;'>"
        "You are an engineering advisor writing a brief for a decision-maker at the US Department of Energy. "
        "Based on your analysis across all pages of this dashboard, answer the five questions below. "
        "Each answer should be <b>2–4 sentences</b>. Use evidence from your numbers and the LCA findings. "
        "There is no single right answer — you are being assessed on your <b>reasoning and justification</b>."
        "</p></div>",
        unsafe_allow_html=True,
    )

    # ── Five structured questions ─────────────────────────────────────────────
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
        "Research shows that hydro-pyrometallurgical processing has a lower environmental footprint "
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
        f"<b>{_gap_end:+,.0f} tonnes in {_ey}</b>. "
        "Your recycling setting adds <b>{:.1f} tonnes/yr</b>. ".format(_rec_supply) +
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

    st.subheader("Question 5 — Overall Recommendation")
    st.markdown(
        "<p style='font-size:13px;color:#555;'>"
        "Imagine you must write one paragraph for a policymaker who has 60 seconds to read it. "
        "Summarize your overall recommendation for a sustainable US tellurium supply strategy "
        "for CdTe solar. Integrate sourcing, processing method, circular economy, and LCA considerations. "
        "Be specific and decisive — a policymaker needs a clear recommendation, not a list of uncertainties.</p>",
        unsafe_allow_html=True,
    )
    pb_recommendation = st.text_area(
        "Your recommendation:",
        value=st.session_state["pb_recommendation"],
        height=150,
        placeholder="e.g. To support sustainable growth of US CdTe solar manufacturing, I recommend...",
        key="ta_recommendation",
    )

    st.divider()

    # ── Save + generate PDF-ready report ─────────────────────────────────────
    col_btn1, col_btn2 = st.columns([1, 1])
    with col_btn1:
        if st.button("💾 Save answers"):
            st.session_state["pb_sourcing"]       = pb_sourcing
            st.session_state["pb_method"]         = pb_method
            st.session_state["pb_ce"]             = pb_ce
            st.session_state["pb_risk"]           = pb_risk
            st.session_state["pb_recommendation"] = pb_recommendation
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
Date    : Generated from Material Availability Dashboard

SCENARIO SUMMARY
{'─'*40}
Gap in {_sy}  : {_gap_start:+,.1f} tonnes
Gap in {_ey}  : {_gap_end:+,.1f} tonnes  ({_gap_trend})
Recycling     : {_rec_supply:,.1f} tonnes/yr

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

QUESTION 5 — OVERALL RECOMMENDATION
{'─'*40}
{pb_recommendation if pb_recommendation.strip() else '[Not answered]'}

{'='*62}
Source: Material Availability Dashboard
"""
        _fname = f"ScenarioAnalysis_{_name.replace(' ','_')}_{_sy}_{_ey}.txt"
        st.download_button(
            label="⬇️ Download scenario analysis (.txt)",
            data=_report,
            file_name=_fname,
            mime="text/plain",
        )

    st.divider()

    # ── Rubric ────────────────────────────────────────────────────────────────
    with st.expander("📏 View grading rubric"):
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

