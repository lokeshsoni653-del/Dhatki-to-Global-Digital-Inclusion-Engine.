"""
Akhuwat Aid Distribution & M&E Engine
A sophisticated command-center dashboard for monitoring and evaluating
Akhuwat's micro-grant, health, education, and crisis relief operations.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
from datetime import datetime, timedelta
import random

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Akhuwat | Aid Distribution & M&E Engine",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  GLOBAL CSS INJECTION
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"] {
    font-family: 'Sora', sans-serif !important;
    background-color: #080c14 !important;
    color: #c9d4e8 !important;
}

/* Streamlit chrome */
.stApp { background: #080c14 !important; }
.block-container { padding: 1.5rem 2rem 4rem 2rem !important; max-width: 100% !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1525 0%, #091020 100%) !important;
    border-right: 1px solid #1a2540 !important;
}
[data-testid="stSidebar"] .css-1d391kg { padding: 1.5rem 1rem !important; }

.sidebar-logo {
    display: flex; align-items: center; gap: 10px;
    padding: 0 0 1.5rem 0;
    border-bottom: 1px solid #1e2f50;
    margin-bottom: 1.5rem;
}
.sidebar-logo-mark {
    width: 38px; height: 38px; border-radius: 10px;
    background: linear-gradient(135deg, #c9a227 0%, #f0c84d 100%);
    display: flex; align-items: center; justify-content: center;
    font-size: 18px; font-weight: 800; color: #080c14; flex-shrink: 0;
}
.sidebar-logo-text { line-height: 1.15; }
.sidebar-logo-text .name { font-size: 14px; font-weight: 700; color: #e8d48c; letter-spacing: 0.04em; }
.sidebar-logo-text .sub  { font-size: 10px; color: #556b8c; letter-spacing: 0.08em; text-transform: uppercase; }

.sidebar-label {
    font-size: 9px; font-weight: 700; letter-spacing: 0.14em;
    text-transform: uppercase; color: #3d5273; margin: 1.2rem 0 0.4rem 0;
}

/* Streamlit widget overrides */
[data-testid="stSelectbox"] label,
[data-testid="stSlider"] label,
[data-testid="stMultiSelect"] label { color: #7a94b8 !important; font-size: 12px !important; font-weight: 600 !important; letter-spacing: 0.06em !important; }

div[data-baseweb="select"] > div {
    background: #0f1c30 !important; border-color: #1e3154 !important;
    border-radius: 8px !important; color: #c9d4e8 !important;
}
div[data-baseweb="select"] > div:hover { border-color: #c9a227 !important; }

/* Slider thumb */
[data-testid="stSlider"] [role="slider"] { background: #c9a227 !important; }
[data-testid="stSlider"] [data-testid="stTickBarMin"],
[data-testid="stSlider"] [data-testid="stTickBarMax"] { color: #556b8c !important; }

/* ── Header Banner ── */
.header-banner {
    background: linear-gradient(135deg, #0d1a2e 0%, #0f2040 50%, #091428 100%);
    border: 1px solid #1a2e50;
    border-radius: 16px;
    padding: 1.6rem 2rem;
    margin-bottom: 1.8rem;
    position: relative;
    overflow: hidden;
}
.header-banner::before {
    content: '';
    position: absolute; top: 0; right: 0;
    width: 300px; height: 100%;
    background: radial-gradient(ellipse at right center, rgba(201,162,39,0.12) 0%, transparent 70%);
    pointer-events: none;
}
.header-title {
    font-size: 22px; font-weight: 800; color: #e8d48c; letter-spacing: -0.02em; line-height: 1.2;
}
.header-title span { color: #c9a227; }
.header-sub {
    font-size: 12px; color: #4a6480; margin-top: 4px;
    font-family: 'JetBrains Mono', monospace; letter-spacing: 0.06em;
}
.header-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(201,162,39,0.12); border: 1px solid rgba(201,162,39,0.3);
    border-radius: 20px; padding: 4px 12px; font-size: 11px; color: #c9a227; font-weight: 600;
    margin-top: 10px;
}
.header-badge::before { content: '●'; font-size: 8px; animation: pulse 2s infinite; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.3} }

/* ── KPI Cards ── */
.kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 1.8rem; }

.kpi-card {
    background: linear-gradient(145deg, #0d1a2e, #0a1525);
    border: 1px solid #1a2e50;
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    position: relative; overflow: hidden;
    transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
    cursor: default;
}
.kpi-card:hover {
    transform: translateY(-3px);
    border-color: #c9a227;
    box-shadow: 0 8px 32px rgba(201,162,39,0.15);
}
.kpi-card::after {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    border-radius: 14px 14px 0 0;
}
.kpi-card.gold::after   { background: linear-gradient(90deg, #c9a227, #f0c84d); }
.kpi-card.teal::after   { background: linear-gradient(90deg, #0ea5a5, #28d4d4); }
.kpi-card.rose::after   { background: linear-gradient(90deg, #d45c5c, #f08080); }
.kpi-card.indigo::after { background: linear-gradient(90deg, #5c7fd4, #80a0f0); }

.kpi-icon {
    width: 36px; height: 36px; border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 17px; margin-bottom: 10px;
}
.kpi-card.gold .kpi-icon   { background: rgba(201,162,39,0.15); }
.kpi-card.teal .kpi-icon   { background: rgba(14,165,165,0.15); }
.kpi-card.rose .kpi-icon   { background: rgba(212,92,92,0.15); }
.kpi-card.indigo .kpi-icon { background: rgba(92,127,212,0.15); }

.kpi-label { font-size: 10px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: #3d5273; margin-bottom: 5px; }
.kpi-value { font-size: 28px; font-weight: 800; letter-spacing: -0.03em; line-height: 1; }
.kpi-card.gold   .kpi-value { color: #e8d48c; }
.kpi-card.teal   .kpi-value { color: #7ee8e8; }
.kpi-card.rose   .kpi-value { color: #f0a0a0; }
.kpi-card.indigo .kpi-value { color: #a0b8f0; }

.kpi-delta {
    display: inline-flex; align-items: center; gap: 4px;
    font-size: 11px; font-weight: 600; margin-top: 6px;
    font-family: 'JetBrains Mono', monospace;
}
.kpi-delta.up   { color: #4caf90; }
.kpi-delta.down { color: #d45c5c; }

/* ── Section Headers ── */
.section-header {
    display: flex; align-items: center; gap: 10px;
    margin: 2rem 0 1rem 0;
}
.section-header-line { flex: 1; height: 1px; background: linear-gradient(90deg, #1a2e50, transparent); }
.section-header-text {
    font-size: 11px; font-weight: 700; letter-spacing: 0.16em;
    text-transform: uppercase; color: #c9a227; white-space: nowrap;
    display: flex; align-items: center; gap: 8px;
}
.section-dot { width: 6px; height: 6px; border-radius: 50%; background: #c9a227; }

/* ── Map Container ── */
.map-outer {
    background: #0d1a2e;
    border: 1px solid #1a2e50;
    border-radius: 14px;
    overflow: hidden;
    padding: 0;
    margin-bottom: 1.8rem;
}
.map-header {
    display: flex; align-items: center; justify-content: space-between;
    padding: 12px 18px;
    background: #091428;
    border-bottom: 1px solid #1a2e50;
}
.map-title { font-size: 12px; font-weight: 700; color: #8aa8cc; letter-spacing: 0.08em; text-transform: uppercase; }
.map-coord { font-family: 'JetBrains Mono', monospace; font-size: 10px; color: #3d5273; }
.map-status-dot { width: 8px; height: 8px; border-radius: 50%; background: #4caf90; display: inline-block; margin-right: 6px; animation: pulse 2s infinite; }

/* ── Chart Cards ── */
.chart-card {
    background: linear-gradient(145deg, #0d1a2e, #0a1525);
    border: 1px solid #1a2e50;
    border-radius: 14px;
    padding: 1.2rem 1.4rem 0.5rem 1.4rem;
    margin-bottom: 1.4rem;
    transition: border-color 0.2s;
}
.chart-card:hover { border-color: #2a4060; }
.chart-title { font-size: 11px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: #556b8c; margin-bottom: 10px; }

/* ── Simulator Panel ── */
.simulator-panel {
    background: linear-gradient(145deg, #0d1a2e, #091020);
    border: 1px solid #1e3154;
    border-radius: 16px;
    padding: 1.8rem 2rem;
    margin-top: 1rem;
    position: relative; overflow: hidden;
}
.simulator-panel::before {
    content: '';
    position: absolute; bottom: -40px; right: -40px;
    width: 200px; height: 200px; border-radius: 50%;
    background: radial-gradient(circle, rgba(201,162,39,0.06) 0%, transparent 70%);
    pointer-events: none;
}
.sim-metric-box {
    background: #091428;
    border: 1px solid #1a2e50;
    border-radius: 12px;
    padding: 1.2rem;
    text-align: center;
}
.sim-metric-value {
    font-size: 32px; font-weight: 800; letter-spacing: -0.03em; line-height: 1.1;
}
.sim-metric-label { font-size: 11px; font-weight: 600; color: #3d5273; text-transform: uppercase; letter-spacing: 0.1em; margin-top: 6px; }
.sim-metric-sub   { font-size: 10px; color: #283d58; margin-top: 3px; }

/* ── Program Tags ── */
.program-tag {
    display: inline-flex; align-items: center; gap: 5px;
    padding: 4px 10px; border-radius: 20px;
    font-size: 10px; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase;
    margin-right: 6px;
}
.tag-micro  { background: rgba(201,162,39,0.15); color: #c9a227; border: 1px solid rgba(201,162,39,0.3); }
.tag-health { background: rgba(14,165,165,0.12); color: #0ea5a5; border: 1px solid rgba(14,165,165,0.25); }
.tag-edu    { background: rgba(92,127,212,0.12); color: #7090d4; border: 1px solid rgba(92,127,212,0.25); }
.tag-crisis { background: rgba(212,92,92,0.12); color: #d45c5c; border: 1px solid rgba(212,92,92,0.25); }

/* Streamlit container backgrounds */
.stTabs [data-baseweb="tab-list"] { background: transparent !important; gap: 0 !important; border-bottom: 1px solid #1a2e50 !important; }
.stTabs [data-baseweb="tab"] { background: transparent !important; color: #3d5273 !important; border: none !important; font-size: 12px !important; font-weight: 600 !important; letter-spacing: 0.06em !important; padding: 8px 16px !important; border-radius: 0 !important; }
.stTabs [aria-selected="true"] { color: #c9a227 !important; border-bottom: 2px solid #c9a227 !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 5px; background: #080c14; }
::-webkit-scrollbar-thumb { background: #1a2e50; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #c9a227; }

/* Folium iframe */
iframe { border-radius: 0 0 13px 13px !important; }

/* Remove streamlit widget borders */
[data-testid="stVerticalBlock"] > div { gap: 0 !important; }
.stMarkdown p { color: #c9d4e8; }

div.stButton > button {
    background: linear-gradient(135deg, #c9a227, #f0c84d) !important;
    color: #080c14 !important; font-weight: 700 !important; font-size: 12px !important;
    border: none !important; border-radius: 8px !important; padding: 8px 20px !important;
    letter-spacing: 0.06em !important; text-transform: uppercase !important;
    transition: opacity 0.2s !important;
}
div.stButton > button:hover { opacity: 0.85 !important; }

/* Status indicator row */
.status-row { display: flex; align-items: center; gap: 20px; flex-wrap: wrap; margin-top: 8px; }
.status-item { display: flex; align-items: center; gap: 6px; font-size: 10px; color: #556b8c; font-family: 'JetBrains Mono', monospace; }
.status-dot-green  { width: 6px; height: 6px; border-radius: 50%; background: #4caf90; }
.status-dot-gold   { width: 6px; height: 6px; border-radius: 50%; background: #c9a227; }
.status-dot-blue   { width: 6px; height: 6px; border-radius: 50%; background: #5c7fd4; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  SYNTHETIC DATA GENERATION
# ─────────────────────────────────────────────
np.random.seed(42)
random.seed(42)

REGIONS = {
    "Lahore":     {"lat": 31.5204, "lon": 74.3587, "province": "Punjab"},
    "Karachi":    {"lat": 24.8607, "lon": 67.0011, "province": "Sindh"},
    "Peshawar":   {"lat": 34.0150, "lon": 71.5249, "province": "KPK"},
    "Tharparkar": {"lat": 24.7136, "lon": 69.8008, "province": "Sindh"},
    "Multan":     {"lat": 30.1575, "lon": 71.5249, "province": "Punjab"},
    "Quetta":     {"lat": 30.1798, "lon": 66.9750, "province": "Balochistan"},
}

PROGRAMS = ["Microfinance", "Education", "Health", "Crisis Relief"]

PROGRAM_COLORS = {
    "Microfinance":  "#c9a227",
    "Education":     "#5c7fd4",
    "Health":        "#0ea5a5",
    "Crisis Relief": "#d45c5c",
}

PROGRAM_ICONS = {
    "Microfinance":  "💰",
    "Education":     "📚",
    "Health":        "🏥",
    "Crisis Relief": "🆘",
}

@st.cache_data
def generate_grants_data():
    rows = []
    for region, info in REGIONS.items():
        for prog in PROGRAMS:
            months = pd.date_range("2023-01-01", periods=18, freq="MS")
            base = np.random.randint(200, 900)
            for i, m in enumerate(months):
                trend = base + i * np.random.randint(5, 25)
                noise = np.random.randint(-40, 60)
                rows.append({
                    "region": region, "program": prog,
                    "month": m,
                    "grants_disbursed": max(0, int(trend + noise)),
                    "amount_pkr": max(0, int((trend + noise) * np.random.randint(15000, 35000))),
                    "beneficiaries": max(0, int((trend + noise) * np.random.uniform(1.1, 2.3))),
                    "province": info["province"],
                })
    return pd.DataFrame(rows)

@st.cache_data
def generate_supply_chain_data():
    categories = ["Last-Mile Delivery", "Warehouse Ops", "Procurement", "Cold Chain", "Volunteer Logistics", "Admin Overhead"]
    data = {}
    for prog in PROGRAMS:
        vals = np.random.dirichlet(np.ones(len(categories)) * 2) * 100
        data[prog] = dict(zip(categories, vals.tolist()))
    return data

@st.cache_data
def generate_cluster_points(region, program, n=18):
    info = REGIONS[region]
    pts = []
    for _ in range(n):
        lat = info["lat"] + np.random.uniform(-0.35, 0.35)
        lon = info["lon"] + np.random.uniform(-0.35, 0.35)
        intensity = np.random.randint(1, 5)
        pts.append({"lat": lat, "lon": lon, "intensity": intensity,
                    "label": f"{program} Unit #{np.random.randint(100, 999)}"})
    return pts

@st.cache_data
def generate_route_points(region):
    info = REGIONS[region]
    routes = []
    for _ in range(3):
        origin = [info["lat"] + np.random.uniform(-0.5, 0.5),
                  info["lon"] + np.random.uniform(-0.5, 0.5)]
        dest   = [info["lat"] + np.random.uniform(-0.5, 0.5),
                  info["lon"] + np.random.uniform(-0.5, 0.5)]
        routes.append((origin, dest))
    return routes

df_grants  = generate_grants_data()
sc_data    = generate_supply_chain_data()

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
      <div class="sidebar-logo-mark">ا</div>
      <div class="sidebar-logo-text">
        <div class="name">AKHUWAT</div>
        <div class="sub">M&E Command Center</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-label">Focus Program</div>', unsafe_allow_html=True)
    selected_program = st.selectbox(
        "", PROGRAMS, label_visibility="collapsed", key="prog_select"
    )

    st.markdown('<div class="sidebar-label">Focus Region</div>', unsafe_allow_html=True)
    selected_region = st.selectbox(
        "", list(REGIONS.keys()), label_visibility="collapsed", key="region_select"
    )

    st.markdown('<div class="sidebar-label">Date Range</div>', unsafe_allow_html=True)
    date_options = ["Last 6 Months", "Last 12 Months", "All Time"]
    selected_period = st.selectbox(
        "", date_options, label_visibility="collapsed", key="date_select"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    prog_color = PROGRAM_COLORS[selected_program]
    prog_icon  = PROGRAM_ICONS[selected_program]
    st.markdown(f"""
    <div style="background:#091428; border:1px solid #1a2e50; border-radius:12px; padding:14px; margin-top:6px;">
      <div style="font-size:10px; text-transform:uppercase; letter-spacing:0.1em; color:#3d5273; margin-bottom:8px;">Active Context</div>
      <div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">
        <span style="font-size:16px;">{prog_icon}</span>
        <span style="font-size:13px; font-weight:700; color:#e8d48c;">{selected_program}</span>
      </div>
      <div style="font-size:11px; color:#556b8c;">📍 {selected_region} · {REGIONS[selected_region]['province']}</div>
      <div style="font-size:11px; color:#556b8c; margin-top:4px;">🕐 {selected_period}</div>
      <div style="height:2px; background:linear-gradient(90deg, {prog_color}, transparent); border-radius:2px; margin-top:12px;"></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    ts = datetime.now().strftime("%d %b %Y · %H:%M")
    st.markdown(f"""
    <div style="font-size:9px; color:#283d58; text-align:center; font-family:'JetBrains Mono', monospace;">
      SYSTEM LIVE · {ts}<br>
      <span style="color:#c9a227;">● TELEMETRY ACTIVE</span>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  FILTER DATA
# ─────────────────────────────────────────────
months_map = {"Last 6 Months": 6, "Last 12 Months": 12, "All Time": 99}
n_months   = months_map[selected_period]
cutoff     = df_grants["month"].max() - pd.DateOffset(months=n_months)

df_filtered = df_grants[
    (df_grants["region"]  == selected_region) &
    (df_grants["program"] == selected_program) &
    (df_grants["month"]   >= cutoff)
]

df_all_regions = df_grants[
    (df_grants["program"] == selected_program) &
    (df_grants["month"]   >= cutoff)
]

# ─────────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="header-banner">
  <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:12px;">
    <div>
      <div class="header-title">Akhuwat <span>Aid Distribution</span> & M&E Engine</div>
      <div class="header-sub">AID-DISTRIB-ENGINE · v2.1.0 · OPERATIONAL DASHBOARD</div>
      <div class="header-badge">● LIVE MONITORING ACTIVE</div>
    </div>
    <div style="text-align:right;">
      <div class="status-row" style="justify-content:flex-end;">
        <div class="status-item"><div class="status-dot-green"></div>DATA FEED</div>
        <div class="status-item"><div class="status-dot-gold"></div>M&E ENGINE</div>
        <div class="status-item"><div class="status-dot-blue"></div>GIS MODULE</div>
      </div>
      <div style="margin-top:10px; display:flex; gap:6px; justify-content:flex-end; flex-wrap:wrap;">
        <span class="program-tag tag-micro">💰 Microfinance</span>
        <span class="program-tag tag-health">🏥 Health</span>
        <span class="program-tag tag-edu">📚 Education</span>
        <span class="program-tag tag-crisis">🆘 Crisis Relief</span>
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  KPI CARDS
# ─────────────────────────────────────────────
total_grants     = df_grants[df_grants["program"] == "Microfinance"]["grants_disbursed"].sum()
health_centers   = 47 + (list(REGIONS.keys()).index(selected_region) * 6)
supplies_managed = 12_847 + (PROGRAMS.index(selected_program) * 1_230)
me_score         = round(74.2 + np.random.uniform(-3, 8), 1)

st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi-card gold">
    <div class="kpi-icon">💰</div>
    <div class="kpi-label">Micro-Grants Active</div>
    <div class="kpi-value">{total_grants:,}</div>
    <div class="kpi-delta up">▲ 12.4% vs last quarter</div>
  </div>
  <div class="kpi-card teal">
    <div class="kpi-icon">🏥</div>
    <div class="kpi-label">Operational Health Centers</div>
    <div class="kpi-value">{health_centers}</div>
    <div class="kpi-delta up">▲ 3 new this month</div>
  </div>
  <div class="kpi-card rose">
    <div class="kpi-icon">📦</div>
    <div class="kpi-label">Total Relief Supplies</div>
    <div class="kpi-value">{supplies_managed:,}</div>
    <div class="kpi-delta down">▼ 2.1% chain latency up</div>
  </div>
  <div class="kpi-card indigo">
    <div class="kpi-icon">📊</div>
    <div class="kpi-label">M&E Optimization Score</div>
    <div class="kpi-value">{me_score}%</div>
    <div class="kpi-delta up">▲ +1.8pts this cycle</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SECTION: GIS MAP
# ─────────────────────────────────────────────
st.markdown("""
<div class="section-header">
  <div class="section-header-line"></div>
  <div class="section-header-text"><div class="section-dot"></div> OPERATIONAL GIS — LIVE FIELD ACTIVITY</div>
  <div class="section-header-line"></div>
</div>
""", unsafe_allow_html=True)

region_info = REGIONS[selected_region]
prog_color_hex = PROGRAM_COLORS[selected_program]

m = folium.Map(
    location=[region_info["lat"], region_info["lon"]],
    zoom_start=11,
    tiles=None,
)

folium.TileLayer(
    tiles="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
    attr="CartoDB",
    name="Dark Matter",
    max_zoom=19,
).add_to(m)

# Cluster points
cluster_pts = generate_cluster_points(selected_region, selected_program, n=20)
icon_map = {
    "Microfinance":  ("money-bill-wave", "gold"),
    "Education":     ("graduation-cap", "blue"),
    "Health":        ("plus-square",    "darkgreen"),
    "Crisis Relief": ("exclamation-circle", "red"),
}
fa_icon, fa_color = icon_map[selected_program]

for pt in cluster_pts:
    radius = 7 + pt["intensity"] * 4
    popup_html = f"""
    <div style='font-family:monospace; font-size:11px; background:#0d1a2e; color:#c9d4e8; padding:8px 12px; border-radius:6px; border:1px solid #1a2e50; min-width:150px;'>
      <b style='color:#c9a227;'>{pt['label']}</b><br>
      Program: {selected_program}<br>
      Region: {selected_region}<br>
      Activity Level: {'●' * pt['intensity']}{'○' * (5 - pt['intensity'])}
    </div>
    """
    folium.CircleMarker(
        location=[pt["lat"], pt["lon"]],
        radius=radius,
        color=prog_color_hex,
        fill=True,
        fill_color=prog_color_hex,
        fill_opacity=0.45,
        weight=1.5,
        popup=folium.Popup(popup_html, max_width=220),
    ).add_to(m)

# Supply routes
routes = generate_route_points(selected_region)
for origin, dest in routes:
    folium.PolyLine(
        [origin, dest],
        color=prog_color_hex,
        weight=2,
        opacity=0.5,
        dash_array="6 4",
    ).add_to(m)

# Main center marker
folium.Marker(
    location=[region_info["lat"], region_info["lon"]],
    popup=folium.Popup(f"<b>{selected_region} — Regional HQ</b><br>{selected_program} Command Node", max_width=200),
    icon=folium.Icon(color="orange", icon="star", prefix="fa"),
).add_to(m)

st.markdown(f"""
<div class="map-outer">
  <div class="map-header">
    <div class="map-title">
      <span class="map-status-dot"></span>
      {selected_program} Field Operations · {selected_region}, {region_info['province']}
    </div>
    <div class="map-coord">
      LAT {region_info['lat']:.4f} · LON {region_info['lon']:.4f}
    </div>
  </div>
""", unsafe_allow_html=True)

st_folium(m, height=440, use_container_width=True, returned_objects=[])

st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SECTION: M&E ANALYTICS
# ─────────────────────────────────────────────
st.markdown("""
<div class="section-header">
  <div class="section-header-line"></div>
  <div class="section-header-text"><div class="section-dot"></div> M&E EFFICIENCY INSIGHTS</div>
  <div class="section-header-line"></div>
</div>
""", unsafe_allow_html=True)

col_left, col_right = st.columns([3, 2], gap="medium")

with col_left:
    # Burn rate bar chart by region (all regions for selected program)
    burn_df = df_all_regions.groupby("region")["amount_pkr"].sum().reset_index()
    burn_df.columns = ["Region", "Total Disbursed (PKR)"]
    burn_df = burn_df.sort_values("Total Disbursed (PKR)", ascending=True)
    burn_df["Highlight"] = burn_df["Region"].apply(lambda r: "Selected" if r == selected_region else "Other")

    fig_burn = go.Figure()
    for _, row in burn_df.iterrows():
        color = prog_color_hex if row["Region"] == selected_region else "#1e3154"
        border= prog_color_hex if row["Region"] == selected_region else "#2a4568"
        fig_burn.add_trace(go.Bar(
            x=[row["Total Disbursed (PKR)"]],
            y=[row["Region"]],
            orientation="h",
            marker=dict(color=color, line=dict(color=border, width=1.5)),
            text=[f"PKR {row['Total Disbursed (PKR)']/1e6:.1f}M"],
            textposition="outside",
            textfont=dict(color="#7a94b8", size=10, family="JetBrains Mono"),
            showlegend=False,
        ))

    fig_burn.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=60, t=10, b=10),
        height=260,
        xaxis=dict(
            showgrid=True, gridcolor="#0f1e33", gridwidth=1,
            zeroline=False, tickfont=dict(color="#3d5273", size=9, family="JetBrains Mono"),
            showticklabels=False,
        ),
        yaxis=dict(
            tickfont=dict(color="#7a94b8", size=11, family="Sora"),
            showgrid=False,
        ),
        barmode="relative",
    )

    st.markdown(f'<div class="chart-card"><div class="chart-title">💸 {selected_program} Micro-Grant Burn Rate by Region</div>', unsafe_allow_html=True)
    st.plotly_chart(fig_burn, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

    # Trend line
    trend_df = df_filtered.groupby("month")[["grants_disbursed", "beneficiaries"]].sum().reset_index()
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=trend_df["month"], y=trend_df["grants_disbursed"],
        mode="lines+markers",
        name="Grants Disbursed",
        line=dict(color=prog_color_hex, width=2.5, shape="spline"),
        marker=dict(size=5, color=prog_color_hex),
        fill="tozeroy", fillcolor=f"rgba{tuple(int(prog_color_hex.lstrip('#')[i:i+2], 16) for i in (0,2,4)) + (0.08,)}",
    ))
    fig_trend.add_trace(go.Scatter(
        x=trend_df["month"], y=trend_df["beneficiaries"],
        mode="lines",
        name="Beneficiaries",
        line=dict(color="#5c7fd4", width=1.8, dash="dot", shape="spline"),
    ))
    fig_trend.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=10, b=0),
        height=210,
        legend=dict(font=dict(color="#556b8c", size=10), bgcolor="rgba(0,0,0,0)", x=0.02, y=1),
        xaxis=dict(
            showgrid=False, zeroline=False,
            tickfont=dict(color="#3d5273", size=9, family="JetBrains Mono"),
        ),
        yaxis=dict(
            showgrid=True, gridcolor="#0f1e33", gridwidth=1,
            zeroline=False, tickfont=dict(color="#3d5273", size=9, family="JetBrains Mono"),
        ),
    )
    st.markdown(f'<div class="chart-card"><div class="chart-title">📈 Disbursement Trend · {selected_region}</div>', unsafe_allow_html=True)
    st.plotly_chart(fig_trend, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

with col_right:
    # Supply chain latency donut
    sc_vals = sc_data[selected_program]
    labels  = list(sc_vals.keys())
    values  = list(sc_vals.values())

    donut_colors = ["#c9a227", "#5c7fd4", "#0ea5a5", "#d45c5c", "#8a6fd4", "#4caf90"]
    fig_donut = go.Figure(go.Pie(
        labels=labels, values=values,
        hole=0.62,
        marker=dict(colors=donut_colors, line=dict(color="#080c14", width=2.5)),
        textfont=dict(color="#c9d4e8", size=10, family="Sora"),
        hovertemplate="<b>%{label}</b><br>%{percent}<extra></extra>",
    ))
    fig_donut.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=10, b=0),
        height=270,
        legend=dict(
            font=dict(color="#556b8c", size=9, family="Sora"),
            bgcolor="rgba(0,0,0,0)",
            orientation="v", x=0.62, y=0.5,
            traceorder="normal",
        ),
        annotations=[dict(
            text=f"<b>{selected_program[:6]}.</b><br>Latency",
            x=0.29, y=0.5, font_size=11, showarrow=False,
            font=dict(color="#7a94b8", family="Sora"),
        )],
    )
    st.markdown('<div class="chart-card"><div class="chart-title">🔄 Relief Supply Chain Latency Breakdown</div>', unsafe_allow_html=True)
    st.plotly_chart(fig_donut, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

    # Beneficiary coverage gauge
    coverage_pct = round(55 + PROGRAMS.index(selected_program) * 7 + list(REGIONS.keys()).index(selected_region) * 2.5, 1)
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=coverage_pct,
        delta={"reference": 60, "increasing": {"color": "#4caf90"}, "decreasing": {"color": "#d45c5c"}},
        number={"suffix": "%", "font": {"size": 28, "color": "#e8d48c", "family": "Sora"}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "#3d5273", "tickfont": {"size": 9, "color": "#3d5273"}},
            "bar": {"color": prog_color_hex, "thickness": 0.22},
            "bgcolor": "#0d1a2e",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 40],   "color": "#0a1525"},
                {"range": [40, 70],  "color": "#0f1e33"},
                {"range": [70, 100], "color": "#132540"},
            ],
            "threshold": {"line": {"color": "#4caf90", "width": 2}, "thickness": 0.7, "value": 75},
        },
        title={"text": "Beneficiary<br>Coverage", "font": {"size": 10, "color": "#556b8c", "family": "Sora"}},
    ))
    fig_gauge.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=20, b=10),
        height=220,
    )
    st.markdown('<div class="chart-card"><div class="chart-title">🎯 Beneficiary Coverage Rate</div>', unsafe_allow_html=True)
    st.plotly_chart(fig_gauge, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SECTION: LOGISTICAL SIMULATOR
# ─────────────────────────────────────────────
st.markdown("""
<div class="section-header">
  <div class="section-header-line"></div>
  <div class="section-header-text"><div class="section-dot"></div> SUPPLY CHAIN OPTIMIZATION SIMULATOR</div>
  <div class="section-header-line"></div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="simulator-panel">', unsafe_allow_html=True)

sim_col1, sim_col2 = st.columns([1, 1], gap="large")

with sim_col1:
    st.markdown("""
    <div style="margin-bottom:16px;">
      <div style="font-size:11px; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; color:#c9a227; margin-bottom:4px;">
        ⚙️ Logistical Parameter Control
      </div>
      <div style="font-size:12px; color:#4a6480; line-height:1.5;">
        Adjust active distribution centers to simulate trade-offs between delivery speed and operational cost across the {selected_region} operational zone.
      </div>
    </div>
    """.format(selected_region=selected_region), unsafe_allow_html=True)

    n_centers = st.slider(
        "Number of Active Distribution Centers",
        min_value=1, max_value=50, value=15, step=1,
        help="More centers → faster delivery, higher cost. Fewer → slower, cheaper."
    )

    # Optimization curve visualization
    x_range = np.arange(1, 51)
    avg_time_curve = 180 / np.sqrt(x_range) + 8
    cost_curve     = 280_000 + x_range * 42_000

    fig_opt = go.Figure()
    fig_opt.add_trace(go.Scatter(
        x=x_range, y=avg_time_curve,
        mode="lines", name="Avg Relief Time (hrs)",
        line=dict(color="#d45c5c", width=2, shape="spline"),
        yaxis="y",
    ))
    fig_opt.add_trace(go.Scatter(
        x=x_range, y=cost_curve / 1e6,
        mode="lines", name="Total Cost (PKR M)",
        line=dict(color="#4caf90", width=2, shape="spline"),
        yaxis="y2",
    ))
    fig_opt.add_vline(
        x=n_centers,
        line=dict(color=prog_color_hex, width=1.5, dash="dash"),
        annotation_text=f"  n={n_centers}",
        annotation_font=dict(color=prog_color_hex, size=10, family="JetBrains Mono"),
    )
    fig_opt.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=40, t=10, b=0),
        height=200,
        legend=dict(font=dict(color="#556b8c", size=9), bgcolor="rgba(0,0,0,0)", x=0.5, y=1),
        xaxis=dict(
            title=dict(text="Distribution Centers", font=dict(color="#3d5273", size=9)),
            showgrid=True, gridcolor="#0f1e33", zeroline=False,
            tickfont=dict(color="#3d5273", size=9, family="JetBrains Mono"),
        ),
        yaxis=dict(
            showgrid=True, gridcolor="#0f1e33", gridwidth=1, zeroline=False,
            tickfont=dict(color="#d45c5c", size=9, family="JetBrains Mono"),
        ),
        yaxis2=dict(
            overlaying="y", side="right", showgrid=False, zeroline=False,
            tickfont=dict(color="#4caf90", size=9, family="JetBrains Mono"),
        ),
    )
    st.plotly_chart(fig_opt, use_container_width=True, config={"displayModeBar": False})

with sim_col2:
    avg_relief_time = round(180 / np.sqrt(n_centers) + 8, 1)
    total_cost      = int(280_000 + n_centers * 42_000)
    efficiency_idx  = round(100 - (avg_relief_time / 2 + total_cost / 500_000), 1)
    efficiency_idx  = max(10, min(99, efficiency_idx))

    st.markdown(f"""
    <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-bottom:12px;">
      <div class="sim-metric-box">
        <div style="font-size:20px; margin-bottom:4px;">⏱️</div>
        <div class="sim-metric-value" style="color:#d45c5c;">{avg_relief_time}</div>
        <div class="sim-metric-label">Avg Relief Time</div>
        <div class="sim-metric-sub">hours · field delivery</div>
      </div>
      <div class="sim-metric-box">
        <div style="font-size:20px; margin-bottom:4px;">💵</div>
        <div class="sim-metric-value" style="color:#4caf90;">{total_cost/1e6:.2f}M</div>
        <div class="sim-metric-label">Total Cost PKR</div>
        <div class="sim-metric-sub">monthly operational</div>
      </div>
    </div>
    <div class="sim-metric-box">
      <div style="font-size:10px; text-transform:uppercase; letter-spacing:0.1em; color:#3d5273; margin-bottom:8px; font-weight:700;">
        Composite Efficiency Index
      </div>
      <div style="display:flex; align-items:center; gap:12px;">
        <div class="sim-metric-value" style="color:#c9a227; font-size:36px;">{efficiency_idx:.1f}%</div>
        <div style="flex:1;">
          <div style="height:6px; background:#0a1525; border-radius:3px; overflow:hidden;">
            <div style="width:{efficiency_idx}%; height:100%; background:linear-gradient(90deg, #c9a227, #f0c84d); border-radius:3px; transition:width 0.4s ease;"></div>
          </div>
          <div style="font-size:9px; color:#3d5273; margin-top:5px; font-family:'JetBrains Mono', monospace;">
            {'●' * int(efficiency_idx//10)}{'○' * (10 - int(efficiency_idx//10))} COMPOSITE SCORE
          </div>
        </div>
      </div>
      <div style="margin-top:8px; font-size:10px; color:#283d58; font-family:'JetBrains Mono', monospace; line-height:1.6;">
        Centers: {n_centers} &nbsp;|&nbsp; Zone: {selected_region} &nbsp;|&nbsp; Program: {selected_program[:6]}.
      </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown(f"""
<div style="margin-top:2.5rem; padding:1.2rem 1.6rem; background:#0a1020; border:1px solid #111d30; border-radius:12px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
  <div style="font-size:10px; color:#283d58; font-family:'JetBrains Mono', monospace;">
    AKHUWAT AID ENGINE · BUILD 2.1.0-RC · ALL DATA SIMULATED FOR DEMONSTRATION
  </div>
  <div style="font-size:10px; color:#c9a227; font-family:'JetBrains Mono', monospace; display:flex; align-items:center; gap:8px;">
    <span style="animation:pulse 2s infinite; display:inline-block;">●</span>
    SYSTEM NOMINAL · {datetime.now().strftime('%d %b %Y %H:%M UTC')}
  </div>
</div>
""", unsafe_allow_html=True)
