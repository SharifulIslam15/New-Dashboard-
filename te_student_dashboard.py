import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Tellurium Supply & Demand – Student Dashboard",
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

def save_banner(next_page: str):
    st.markdown(
        f"<div style='background:#e8f5e9;border-left:4px solid #2e7d32;"
        f"padding:10px 14px;border-radius:6px;margin-top:8px;'>"
        f"✅ <b>Saved!</b> Now go to <b>{next_page}</b> in the sidebar to continue.</div>",
        unsafe_allow_html=True,
    )

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
}

for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Sidebar navigation ────────────────────────────────────────────────────────
st.sidebar.title("📊 Te Supply & Demand Dashboard")
st.sidebar.caption("ENE 371 · Sustainable Civil & Environmental Systems")
st.sidebar.divider()

PAGES = [
    "🏠 Welcome",
    "👤 Student Info",
    "⛏️ Material Supply",
    "☀️ Material Demand",
    "📊 Results & Gap",
    "♻️ Circular Economy",
]
page = st.sidebar.selectbox("Navigate to", PAGES)

st.sidebar.divider()
st.sidebar.markdown(
    "<small style='color:#2e7d32;font-weight:600;'>How to use</small><br>"
    "<small>1. Enter your name on <b>Student Info</b><br>"
    "2. Set supply parameters<br>"
    "3. Set demand parameters<br>"
    "4. View <b>Results & Gap</b><br>"
    "5. Explore <b>Circular Economy</b></small>",
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
            "🌞 Tellurium Supply & Demand</h1>"
            "<h3 style='color:#388e3c;font-weight:400;margin-top:0;'>"
            "Interactive Student Dashboard</h3>",
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
            ("1", "Why Tellurium is a critical & hitchhiker resource"),
            ("2", "How supply comes from direct mining and copper by-production"),
            ("3", "How PV demand and non-PV demand are calculated"),
            ("4", "What the supply–demand gap means (surplus vs. shortage)"),
            ("5", "How recycling (Circular Economy) changes the picture"),
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
        st.markdown("<h3 style='color:#2e7d32;'>Circular Economy Concept</h3>", unsafe_allow_html=True)
        st.markdown("""
        <svg viewBox="0 0 400 430" xmlns="http://www.w3.org/2000/svg" width="100%">
          <defs>
            <marker id="a1" markerWidth="9" markerHeight="6" refX="8" refY="3" orient="auto">
              <polygon points="0 0, 9 3, 0 6" fill="#1b5e20"/>
            </marker>
            <marker id="a2" markerWidth="9" markerHeight="6" refX="8" refY="3" orient="auto">
              <polygon points="0 0, 9 3, 0 6" fill="#1565c0"/>
            </marker>
          </defs>
          <rect width="400" height="430" fill="#f9fbe7" rx="14"/>
          <text x="200" y="22" text-anchor="middle" font-size="12" font-weight="bold"
                fill="#1b5e20" font-family="Arial">LINEAR vs CIRCULAR ECONOMY</text>
          <text x="14" y="46" font-size="9" fill="#888" font-family="Arial" font-weight="bold">LINEAR (take → make → dispose)</text>
          <rect x="12" y="54" width="60" height="30" rx="5" fill="#ef9a9a"/>
          <text x="42" y="73" text-anchor="middle" font-size="9" font-weight="bold" fill="#b71c1c" font-family="Arial">Extract</text>
          <line x1="72" y1="69" x2="84" y2="69" stroke="#555" stroke-width="1.5" marker-end="url(#a1)"/>
          <rect x="84" y="54" width="72" height="30" rx="5" fill="#ffe082"/>
          <text x="120" y="66" text-anchor="middle" font-size="9" font-weight="bold" fill="#e65100" font-family="Arial">Manufacture</text>
          <text x="120" y="77" text-anchor="middle" font-size="8" fill="#e65100" font-family="Arial">PV Panels</text>
          <line x1="156" y1="69" x2="168" y2="69" stroke="#555" stroke-width="1.5" marker-end="url(#a1)"/>
          <rect x="168" y="54" width="54" height="30" rx="5" fill="#a5d6a7"/>
          <text x="195" y="73" text-anchor="middle" font-size="9" font-weight="bold" fill="#1b5e20" font-family="Arial">In Use</text>
          <line x1="222" y1="69" x2="234" y2="69" stroke="#555" stroke-width="1.5" marker-end="url(#a1)"/>
          <rect x="234" y="54" width="68" height="30" rx="5" fill="#b0bec5"/>
          <text x="268" y="66" text-anchor="middle" font-size="9" font-weight="bold" fill="#37474f" font-family="Arial">Dispose</text>
          <text x="268" y="77" text-anchor="middle" font-size="8" fill="#37474f" font-family="Arial">(Landfill)</text>
          <text x="318" y="73" font-size="16" fill="#c62828" font-weight="bold" font-family="Arial">✕</text>
          <line x1="14" y1="100" x2="386" y2="100" stroke="#ccc" stroke-width="0.8"/>
          <text x="14" y="118" font-size="9" fill="#888" font-family="Arial" font-weight="bold">CIRCULAR (keep materials in use)</text>
          <rect x="14" y="132" width="80" height="38" rx="6" fill="#ef9a9a"/>
          <text x="54" y="147" text-anchor="middle" font-size="9" font-weight="bold" fill="#b71c1c" font-family="Arial">Extract / Mine</text>
          <text x="54" y="160" text-anchor="middle" font-size="8" fill="#b71c1c" font-family="Arial">Virgin material</text>
          <rect x="306" y="132" width="80" height="38" rx="6" fill="#ffe082"/>
          <text x="346" y="147" text-anchor="middle" font-size="9" font-weight="bold" fill="#e65100" font-family="Arial">Manufacture</text>
          <text x="346" y="160" text-anchor="middle" font-size="8" fill="#e65100" font-family="Arial">PV Panels</text>
          <rect x="316" y="248" width="76" height="38" rx="6" fill="#a5d6a7"/>
          <text x="354" y="263" text-anchor="middle" font-size="9" font-weight="bold" fill="#1b5e20" font-family="Arial">In Use</text>
          <text x="354" y="276" text-anchor="middle" font-size="8" fill="#1b5e20" font-family="Arial">25+ years</text>
          <rect x="152" y="350" width="96" height="38" rx="6" fill="#ce93d8"/>
          <text x="200" y="365" text-anchor="middle" font-size="9" font-weight="bold" fill="#4a148c" font-family="Arial">End of Life</text>
          <text x="200" y="378" text-anchor="middle" font-size="8" fill="#4a148c" font-family="Arial">Collection</text>
          <rect x="8" y="248" width="80" height="38" rx="6" fill="#80cbc4"/>
          <text x="48" y="263" text-anchor="middle" font-size="9" font-weight="bold" fill="#004d40" font-family="Arial">Recycle / Reuse</text>
          <text x="48" y="276" text-anchor="middle" font-size="8" fill="#004d40" font-family="Arial">Recover Te</text>
          <path d="M 94 148 Q 200 128 306 148" fill="none" stroke="#1b5e20" stroke-width="1.8" marker-end="url(#a1)"/>
          <text x="200" y="133" text-anchor="middle" font-size="8" fill="#1b5e20" font-family="Arial">material input</text>
          <path d="M 348 170 Q 358 210 354 248" fill="none" stroke="#1b5e20" stroke-width="1.8" marker-end="url(#a1)"/>
          <path d="M 330 286 Q 298 330 252 358" fill="none" stroke="#1b5e20" stroke-width="1.8" marker-end="url(#a1)"/>
          <text x="310" y="335" text-anchor="middle" font-size="8" fill="#555" font-family="Arial">retire</text>
          <path d="M 152 369 Q 100 372 88 286" fill="none" stroke="#1565c0" stroke-width="2.5" marker-end="url(#a2)"/>
          <text x="94" y="358" text-anchor="middle" font-size="8" fill="#1565c0" font-family="Arial">recycle</text>
          <path d="M 88 248 Q 88 195 306 162" fill="none" stroke="#1565c0" stroke-width="2.5" marker-end="url(#a2)"/>
          <text x="170" y="196" text-anchor="middle" font-size="8" fill="#1565c0" font-family="Arial">recovered material</text>
          <rect x="118" y="208" width="164" height="24" rx="10" fill="#1565c0"/>
          <text x="200" y="224" text-anchor="middle" font-size="9" font-weight="bold" fill="white" font-family="Arial">CE loop — reduces virgin mining</text>
        </svg>
        """, unsafe_allow_html=True)

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
            save_banner("Material Supply")

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: Material Supply
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
        save_banner("Material Demand")

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
        save_banner("Results & Gap")

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
        st.success("Recycling inputs saved! Go to **Results & Gap** to see the updated chart.")

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
