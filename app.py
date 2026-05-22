"""
Manufacturing Inventory & Raw Material Predictor
Master Group of Industries — Internal Supply Chain Intelligence Platform
Author: Portfolio Project | Built with Python, Streamlit, Pandas, NumPy, Plotly
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# ─────────────────────────────────────────────
#  PAGE CONFIG — Must be the first Streamlit call
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="MGI Supply Chain Intelligence",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  GLOBAL STYLES — Premium corporate dark theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Import premium fonts ── */
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&family=Syne:wght@700;800&display=swap');

    /* ── Root palette ── */
    :root {
        --bg-base:       #0a0e1a;
        --bg-card:       #111827;
        --bg-card-hover: #1a2236;
        --border:        #1e2d45;
        --border-light:  #243352;
        --accent-blue:   #3b82f6;
        --accent-cyan:   #06b6d4;
        --accent-amber:  #f59e0b;
        --accent-red:    #ef4444;
        --accent-green:  #10b981;
        --text-primary:  #f0f4ff;
        --text-secondary:#8b9ab8;
        --text-muted:    #4a5a78;
    }

    /* ── Base overrides ── */
    .stApp {
        background-color: var(--bg-base) !important;
        font-family: 'DM Sans', sans-serif !important;
    }
    .main .block-container {
        padding: 1.5rem 2rem 3rem;
        max-width: 1400px;
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1525 0%, #0a0e1a 100%) !important;
        border-right: 1px solid var(--border) !important;
    }
    section[data-testid="stSidebar"] .block-container { padding: 2rem 1.2rem; }

    /* ── Typography ── */
    h1, h2, h3, h4 { font-family: 'Syne', sans-serif !important; }
    p, span, div, label { font-family: 'DM Sans', sans-serif !important; }

    /* ── Metric cards ── */
    div[data-testid="metric-container"] {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1rem 1.25rem !important;
        transition: border-color 0.2s;
    }
    div[data-testid="metric-container"]:hover { border-color: var(--border-light); }
    div[data-testid="metric-container"] label {
        color: var(--text-secondary) !important;
        font-size: 0.72rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
    }
    div[data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: var(--text-primary) !important;
        font-family: 'Syne', sans-serif !important;
        font-size: 1.9rem !important;
    }
    div[data-testid="metric-container"] [data-testid="stMetricDelta"] {
        font-size: 0.75rem !important;
    }

    /* ── Section headings ── */
    .section-title {
        font-family: 'Syne', sans-serif;
        font-size: 1rem;
        font-weight: 700;
        color: var(--text-secondary);
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin: 0.25rem 0 1rem;
    }

    /* ── Hero banner ── */
    .hero-banner {
        background: linear-gradient(135deg, #0d1a33 0%, #111827 50%, #0d1a2e 100%);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 2rem 2.5rem;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    .hero-banner::before {
        content: '';
        position: absolute;
        top: -60px; right: -60px;
        width: 200px; height: 200px;
        background: radial-gradient(circle, rgba(59,130,246,0.12) 0%, transparent 70%);
        border-radius: 50%;
    }
    .hero-title {
        font-family: 'Syne', sans-serif;
        font-size: 1.75rem;
        font-weight: 800;
        color: #f0f4ff;
        margin: 0 0 0.3rem;
        letter-spacing: -0.02em;
    }
    .hero-sub {
        font-size: 0.85rem;
        color: var(--text-secondary);
        font-weight: 400;
        margin: 0;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(59,130,246,0.15);
        border: 1px solid rgba(59,130,246,0.3);
        color: #93c5fd;
        font-size: 0.65rem;
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        padding: 0.25rem 0.6rem;
        border-radius: 20px;
        margin-bottom: 0.75rem;
    }

    /* ── Data table ── */
    .stDataFrame { border-radius: 10px; overflow: hidden; }
    div[data-testid="stDataFrame"] { border: 1px solid var(--border); border-radius: 10px; }

    /* ── Alert boxes ── */
    div[data-testid="stAlert"] {
        border-radius: 10px !important;
        border-left-width: 4px !important;
    }

    /* ── Divider ── */
    hr { border-color: var(--border) !important; margin: 1.75rem 0 !important; }

    /* ── Sidebar labels ── */
    .sidebar-label {
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: var(--text-muted);
        margin-bottom: 0.4rem;
    }
    .sidebar-section {
        background: rgba(255,255,255,0.03);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
    }

    /* ── Status pill ── */
    .pill {
        display: inline-block;
        padding: 0.2rem 0.65rem;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 0.04em;
    }
    .pill-critical { background: rgba(239,68,68,0.15); color: #fca5a5; border: 1px solid rgba(239,68,68,0.3); }
    .pill-warning  { background: rgba(245,158,11,0.15); color: #fcd34d; border: 1px solid rgba(245,158,11,0.3); }
    .pill-ok       { background: rgba(16,185,129,0.12); color: #6ee7b7; border: 1px solid rgba(16,185,129,0.25); }

    /* ── Footer ── */
    .footer {
        text-align: center;
        color: var(--text-muted);
        font-size: 0.72rem;
        letter-spacing: 0.05em;
        margin-top: 3rem;
        padding-top: 1.5rem;
        border-top: 1px solid var(--border);
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  SYNTHETIC DATA — Realistic foam/mattress warehouse
# ─────────────────────────────────────────────
@st.cache_data
def load_inventory_data() -> pd.DataFrame:
    """
    Generate realistic raw material inventory data for a foam & mattress
    manufacturing plant (modelled on Master MoltyFoam operations).
    Returns a DataFrame with one row per material.
    """
    data = {
        "Material": [
            "Polyurethane Chemical",
            "TDI (Toluene Diisocyanate)",
            "Polymer Resin",
            "Cotton Fabric",
            "Steel Springs",
        ],
        "Category": [
            "Chemical", "Chemical", "Chemical", "Textile", "Metal"
        ],
        # Current on-hand stock in metric tons
        "Current_Stock_Tons": [
            142.5, 38.2, 87.6, 210.0, 54.3
        ],
        # Minimum stock level that triggers a purchase order (tons)
        "Reorder_Threshold_Tons": [
            80.0, 45.0, 50.0, 120.0, 60.0
        ],
        # How many tons the plant burns through per production day
        "Avg_Daily_Consumption_Tons": [
            6.8, 3.1, 4.2, 9.5, 2.7
        ],
        # Calendar days from PO placement to warehouse arrival
        "Supplier_Lead_Time_Days": [
            14, 21, 10, 7, 18
        ],
        # PKR cost per metric ton (converted at ~280 PKR/USD)
        "Unit_Cost_PKR_per_Ton": [
            420_000, 980_000, 310_000, 185_000, 560_000
        ],
        # Primary supplier names for authenticity
        "Supplier": [
            "BASF Pakistan Ltd.",
            "Lanxess Chemicals",
            "Reliance Industries",
            "Kohinoor Textile Mills",
            "Agha Steel Industries",
        ],
    }
    df = pd.DataFrame(data)
    return df


# ─────────────────────────────────────────────
#  CALCULATIONS — Core supply chain metrics
# ─────────────────────────────────────────────
def compute_metrics(df: pd.DataFrame, spike_factor: float) -> pd.DataFrame:
    """
    Derive all KPI columns from base data, applying the production spike
    multiplier to simulate elevated consumption scenarios.

    spike_factor: 1.0 = baseline, 1.5 = 50% more consumption, etc.
    """
    df = df.copy()

    # Simulated daily consumption after spike
    df["Simulated_Consumption_Tons"] = (
        df["Avg_Daily_Consumption_Tons"] * spike_factor
    ).round(2)

    # Days of supply remaining at the simulated burn rate
    df["Days_Until_Stockout"] = (
        df["Current_Stock_Tons"] / df["Simulated_Consumption_Tons"]
    ).round(1)

    # Total inventory value for each line
    df["Inventory_Value_PKR"] = (
        df["Current_Stock_Tons"] * df["Unit_Cost_PKR_per_Ton"]
    ).round(0).astype(int)

    # Reorder days: how many days until stock hits the reorder threshold
    df["Days_To_Reorder_Level"] = (
        (df["Current_Stock_Tons"] - df["Reorder_Threshold_Tons"])
        / df["Simulated_Consumption_Tons"]
    ).round(1)

    # Alert classification
    def classify(row):
        if row["Days_Until_Stockout"] < row["Supplier_Lead_Time_Days"]:
            return "CRITICAL"
        elif row["Days_Until_Stockout"] < row["Supplier_Lead_Time_Days"] * 1.4:
            return "WARNING"
        else:
            return "OK"

    df["Alert_Status"] = df.apply(classify, axis=1)

    # Stock coverage ratio (current vs reorder threshold)
    df["Stock_vs_Threshold_Pct"] = (
        (df["Current_Stock_Tons"] / df["Reorder_Threshold_Tons"]) * 100
    ).round(1)

    return df


# ─────────────────────────────────────────────
#  PLOTLY CHARTS
# ─────────────────────────────────────────────
DARK_BG    = "#111827"
GRID_COLOR = "#1e2d45"
FONT_COLOR = "#8b9ab8"

def chart_stock_vs_threshold(df: pd.DataFrame) -> go.Figure:
    """
    Grouped bar chart: Current Stock vs Reorder Threshold per material.
    Color-encodes alert status for instant visual triage.
    """
    status_color = {"CRITICAL": "#ef4444", "WARNING": "#f59e0b", "OK": "#10b981"}
    bar_colors = [status_color[s] for s in df["Alert_Status"]]

    fig = go.Figure()

    # Current stock bars
    fig.add_trace(go.Bar(
        name="Current Stock (Tons)",
        x=df["Material"],
        y=df["Current_Stock_Tons"],
        marker=dict(
            color=bar_colors,
            opacity=0.85,
            line=dict(color="rgba(255,255,255,0.05)", width=1),
        ),
        text=df["Current_Stock_Tons"].apply(lambda v: f"{v:.1f}T"),
        textposition="outside",
        textfont=dict(family="DM Mono", size=11, color="#c9d4ef"),
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Current Stock: <b>%{y:.1f} Tons</b><br>"
            "<extra></extra>"
        ),
    ))

    # Reorder threshold line markers
    fig.add_trace(go.Scatter(
        name="Reorder Threshold",
        x=df["Material"],
        y=df["Reorder_Threshold_Tons"],
        mode="markers+lines",
        marker=dict(symbol="diamond", size=10, color="#3b82f6",
                    line=dict(color="#93c5fd", width=1.5)),
        line=dict(color="#3b82f6", width=1.5, dash="dot"),
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Reorder Threshold: <b>%{y:.1f} Tons</b><br>"
            "<extra></extra>"
        ),
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=DARK_BG,
        font=dict(family="DM Sans", color=FONT_COLOR),
        title=dict(
            text="Stock Levels vs Reorder Thresholds",
            font=dict(family="Syne", size=15, color="#e2eaff"),
            x=0.01, xanchor="left", pad=dict(b=16),
        ),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02,
            xanchor="right", x=1,
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=11),
        ),
        xaxis=dict(
            showgrid=False, zeroline=False,
            tickfont=dict(size=11, family="DM Sans"),
        ),
        yaxis=dict(
            title="Metric Tons",
            gridcolor=GRID_COLOR, zeroline=False,
            tickfont=dict(size=11, family="DM Mono"),
        ),
        margin=dict(l=10, r=10, t=60, b=10),
        bargap=0.35,
        height=380,
    )
    return fig


def chart_days_until_stockout(df: pd.DataFrame) -> go.Figure:
    """
    Horizontal bar chart showing days until stockout vs supplier lead time.
    A red band marks the danger zone (below lead time).
    """
    status_color = {"CRITICAL": "#ef4444", "WARNING": "#f59e0b", "OK": "#10b981"}
    bar_colors = [status_color[s] for s in df["Alert_Status"]]

    df_sorted = df.sort_values("Days_Until_Stockout")

    fig = go.Figure()

    # Supplier lead time reference bars (background)
    fig.add_trace(go.Bar(
        name="Supplier Lead Time",
        y=df_sorted["Material"],
        x=df_sorted["Supplier_Lead_Time_Days"],
        orientation="h",
        marker=dict(color="rgba(59,130,246,0.12)",
                    line=dict(color="rgba(59,130,246,0.3)", width=1)),
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Lead Time: <b>%{x} days</b><br>"
            "<extra></extra>"
        ),
    ))

    # Days until stockout bars
    fig.add_trace(go.Bar(
        name="Days Until Stockout",
        y=df_sorted["Material"],
        x=df_sorted["Days_Until_Stockout"],
        orientation="h",
        marker=dict(
            color=[status_color[s] for s in df_sorted["Alert_Status"]],
            opacity=0.9,
            line=dict(color="rgba(255,255,255,0.05)", width=1),
        ),
        text=df_sorted["Days_Until_Stockout"].apply(lambda v: f"  {v:.0f}d"),
        textposition="outside",
        textfont=dict(family="DM Mono", size=11, color="#c9d4ef"),
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Days Until Stockout: <b>%{x:.1f} days</b><br>"
            "<extra></extra>"
        ),
    ))

    fig.update_layout(
        barmode="overlay",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=DARK_BG,
        font=dict(family="DM Sans", color=FONT_COLOR),
        title=dict(
            text="Days Until Stockout vs Supplier Lead Time",
            font=dict(family="Syne", size=15, color="#e2eaff"),
            x=0.01, xanchor="left", pad=dict(b=16),
        ),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02,
            xanchor="right", x=1,
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=11),
        ),
        xaxis=dict(
            title="Calendar Days",
            gridcolor=GRID_COLOR, zeroline=False,
            tickfont=dict(size=11, family="DM Mono"),
        ),
        yaxis=dict(
            showgrid=False,
            tickfont=dict(size=11, family="DM Sans"),
        ),
        margin=dict(l=10, r=60, t=60, b=10),
        height=380,
    )
    return fig


def chart_inventory_value(df: pd.DataFrame) -> go.Figure:
    """
    Donut chart showing distribution of total inventory value by material.
    """
    colors = ["#3b82f6", "#06b6d4", "#8b5cf6", "#f59e0b", "#10b981"]

    fig = go.Figure(go.Pie(
        labels=df["Material"],
        values=df["Inventory_Value_PKR"],
        hole=0.62,
        marker=dict(colors=colors, line=dict(color=DARK_BG, width=3)),
        textinfo="label+percent",
        textfont=dict(family="DM Sans", size=10, color="#c9d4ef"),
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Value: <b>PKR %{value:,.0f}</b><br>"
            "Share: <b>%{percent}</b><br>"
            "<extra></extra>"
        ),
    ))

    total_value = df["Inventory_Value_PKR"].sum()
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color=FONT_COLOR),
        title=dict(
            text="Inventory Value Distribution",
            font=dict(family="Syne", size=15, color="#e2eaff"),
            x=0.01, xanchor="left",
        ),
        annotations=[dict(
            text=f"<b>PKR {total_value/1e6:.1f}M</b><br><span style='font-size:10px'>Total Value</span>",
            x=0.5, y=0.5, showarrow=False,
            font=dict(family="Syne", size=13, color="#e2eaff"),
            align="center",
        )],
        showlegend=False,
        margin=dict(l=10, r=10, t=60, b=10),
        height=380,
    )
    return fig


def chart_consumption_heatmap(df: pd.DataFrame) -> go.Figure:
    """
    7-day simulated daily consumption forecast per material as an area chart.
    """
    days = [f"Day {i+1}" for i in range(7)]
    fig = go.Figure()
    colors = ["#3b82f6", "#ef4444", "#10b981", "#f59e0b", "#8b5cf6"]

    for i, row in df.iterrows():
        # Add slight random variance to make the forecast look realistic
        np.random.seed(i * 7)
        daily = row["Simulated_Consumption_Tons"] * (
            1 + np.random.uniform(-0.08, 0.12, 7)
        )
        fig.add_trace(go.Scatter(
            x=days, y=daily.round(2),
            name=row["Material"].split(" ")[0],
            mode="lines+markers",
            line=dict(color=colors[i], width=2),
            marker=dict(size=5),
            fill="tozeroy",
            fillcolor=colors[i].replace(")", ",0.05)").replace("rgb", "rgba")
                        if "rgb" in colors[i] else f"rgba({int(colors[i][1:3],16)},{int(colors[i][3:5],16)},{int(colors[i][5:7],16)},0.07)",
            hovertemplate=(
                f"<b>{row['Material']}</b><br>"
                "%{x}: <b>%{y:.2f} Tons</b><br>"
                "<extra></extra>"
            ),
        ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=DARK_BG,
        font=dict(family="DM Sans", color=FONT_COLOR),
        title=dict(
            text="7-Day Consumption Forecast (Simulated)",
            font=dict(family="Syne", size=15, color="#e2eaff"),
            x=0.01, xanchor="left", pad=dict(b=16),
        ),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02,
            xanchor="right", x=1,
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=11),
        ),
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(
            title="Tons / Day",
            gridcolor=GRID_COLOR, zeroline=False,
            tickfont=dict(size=11, family="DM Mono"),
        ),
        margin=dict(l=10, r=10, t=60, b=10),
        height=300,
    )
    return fig


# ─────────────────────────────────────────────
#  HELPER — Format large PKR numbers
# ─────────────────────────────────────────────
def fmt_pkr(value: float) -> str:
    if value >= 1_000_000_000:
        return f"PKR {value/1_000_000_000:.2f}B"
    elif value >= 1_000_000:
        return f"PKR {value/1_000_000:.1f}M"
    else:
        return f"PKR {value:,.0f}"


# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; margin-bottom:1.5rem;'>
        <div style='font-family:Syne,sans-serif; font-size:1.15rem;
                    font-weight:800; color:#f0f4ff; letter-spacing:-0.01em;'>
            🏭 MGI Supply Chain
        </div>
        <div style='font-size:0.7rem; color:#4a5a78; letter-spacing:0.08em;
                    text-transform:uppercase; margin-top:0.25rem;'>
            Intelligence Platform
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Production Spike Simulator ──
    st.markdown("""
    <div class='sidebar-label'>⚡ Production Spike Simulator</div>
    """, unsafe_allow_html=True)

    spike_pct = st.slider(
        label="Daily Consumption Increase",
        min_value=0, max_value=100, value=0, step=5,
        help="Simulate a surge in production demand. "
             "0% = normal operations. 50% = peak season overload.",
        format="%d%%",
    )
    spike_factor = 1.0 + (spike_pct / 100.0)

    if spike_pct == 0:
        st.info("📊 Baseline operations. Adjust slider to simulate demand spikes.", icon=None)
    elif spike_pct <= 20:
        st.warning(f"⚠️ +{spike_pct}% demand surge — monitor critical materials.", icon=None)
    elif spike_pct <= 50:
        st.error(f"🔴 +{spike_pct}% spike — reorder windows collapsing!", icon=None)
    else:
        st.error(f"🚨 +{spike_pct}% EXTREME SPIKE — production bottleneck risk!", icon=None)

    st.markdown("---")

    # ── Filters ──
    st.markdown("<div class='sidebar-label'>🔽 Filter Materials</div>", unsafe_allow_html=True)

    base_df = load_inventory_data()
    selected_materials = st.multiselect(
        "Select Materials",
        options=base_df["Material"].tolist(),
        default=base_df["Material"].tolist(),
        help="Focus the dashboard on specific raw materials.",
    )

    st.markdown("---")

    # ── Info block ──
    st.markdown(f"""
    <div class='sidebar-section'>
        <div style='font-size:0.68rem; color:#4a5a78; text-transform:uppercase;
                    letter-spacing:0.08em; margin-bottom:0.6rem;'>System Status</div>
        <div style='font-size:0.78rem; color:#6ee7b7; margin-bottom:0.3rem;'>
            ● Live Data Feed Active
        </div>
        <div style='font-size:0.72rem; color:#8b9ab8;'>
            Last refreshed:<br>
            <span style='font-family:DM Mono; color:#c9d4ef;'>
                {datetime.now().strftime("%d %b %Y — %H:%M")}
            </span>
        </div>
        <div style='font-size:0.72rem; color:#8b9ab8; margin-top:0.5rem;'>
            Spike Factor:&nbsp;
            <span style='font-family:DM Mono; color:#fcd34d;'>×{spike_factor:.2f}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  DATA PIPELINE
# ─────────────────────────────────────────────
raw_df  = load_inventory_data()

# Apply filter
if selected_materials:
    raw_df = raw_df[raw_df["Material"].isin(selected_materials)].reset_index(drop=True)
else:
    st.warning("No materials selected. Showing all materials.", icon="⚠️")
    raw_df = load_inventory_data()

# Compute all derived metrics with the simulator spike
df = compute_metrics(raw_df, spike_factor)

# Aggregate KPIs
total_inventory_value   = df["Inventory_Value_PKR"].sum()
critical_alert_count    = (df["Alert_Status"] == "CRITICAL").sum()
warning_alert_count     = (df["Alert_Status"] == "WARNING").sum()
avg_days_of_supply      = df["Days_Until_Stockout"].mean()
total_stock_tons        = df["Current_Stock_Tons"].sum()


# ─────────────────────────────────────────────
#  HERO BANNER
# ─────────────────────────────────────────────
st.markdown(f"""
<div class='hero-banner'>
    <div class='hero-badge'>Master Group of Industries — Restricted Internal Platform</div>
    <div class='hero-title'>Manufacturing Inventory &amp; Raw Material Predictor</div>
    <div class='hero-sub'>
        Foam &amp; Mattress Division &nbsp;·&nbsp; Karachi Central Warehouse &nbsp;·&nbsp;
        Production Spike: <b style='color:#fcd34d;'>+{spike_pct}%</b>
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  SECTION 1 — EXECUTIVE KPI CARDS
# ─────────────────────────────────────────────
st.markdown("<div class='section-title'>📊 Executive KPI Dashboard</div>", unsafe_allow_html=True)

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

with kpi1:
    st.metric(
        label="Total Inventory Value",
        value=fmt_pkr(total_inventory_value),
        delta="Live valuation",
    )

with kpi2:
    alert_label = "🔴 CRITICAL" if critical_alert_count > 0 else "✅ None"
    st.metric(
        label="Critical Alerts",
        value=str(critical_alert_count),
        delta=f"{warning_alert_count} warnings",
        delta_color="inverse" if critical_alert_count > 0 else "normal",
    )

with kpi3:
    st.metric(
        label="Avg Days of Supply",
        value=f"{avg_days_of_supply:.1f} days",
        delta=f"Spike ×{spike_factor:.2f} applied",
        delta_color="off",
    )

with kpi4:
    st.metric(
        label="Total Stock on Hand",
        value=f"{total_stock_tons:,.1f} T",
        delta=f"{len(df)} materials tracked",
        delta_color="off",
    )

with kpi5:
    most_critical = df.loc[df["Days_Until_Stockout"].idxmin(), "Material"].split(" ")[0]
    min_days = df["Days_Until_Stockout"].min()
    st.metric(
        label="Most Urgent Material",
        value=most_critical,
        delta=f"{min_days:.1f} days remaining",
        delta_color="inverse",
    )

st.markdown("---")


# ─────────────────────────────────────────────
#  SECTION 2 — DYNAMIC REORDER ALERTS
# ─────────────────────────────────────────────
st.markdown("<div class='section-title'>🚨 Dynamic Reorder Alerts</div>", unsafe_allow_html=True)

critical_df = df[df["Alert_Status"] == "CRITICAL"]
warning_df  = df[df["Alert_Status"] == "WARNING"]
ok_df       = df[df["Alert_Status"] == "OK"]

if critical_df.empty and warning_df.empty:
    st.success(
        "✅ **All Clear — No Reorder Alerts.** "
        "All materials have sufficient stock relative to supplier lead times. "
        "Continue monitoring under current production rates.",
        icon=None,
    )
else:
    # CRITICAL alerts
    for _, row in critical_df.iterrows():
        shortfall = row["Supplier_Lead_Time_Days"] - row["Days_Until_Stockout"]
        st.error(
            f"🔴 **CRITICAL — {row['Material']}** | "
            f"Stockout in **{row['Days_Until_Stockout']:.1f} days** · "
            f"Lead time: **{row['Supplier_Lead_Time_Days']} days** · "
            f"Shortfall: **{shortfall:.1f} days** · "
            f"Stock: **{row['Current_Stock_Tons']:.1f}T** vs Threshold: **{row['Reorder_Threshold_Tons']:.1f}T** · "
            f"Supplier: {row['Supplier']} — **Issue PO immediately!**",
            icon=None,
        )

    # WARNING alerts
    for _, row in warning_df.iterrows():
        buffer = row["Days_Until_Stockout"] - row["Supplier_Lead_Time_Days"]
        st.warning(
            f"⚠️ **WARNING — {row['Material']}** | "
            f"Stockout in **{row['Days_Until_Stockout']:.1f} days** · "
            f"Lead time: **{row['Supplier_Lead_Time_Days']} days** · "
            f"Buffer: **{buffer:.1f} days** · "
            f"Supplier: {row['Supplier']} — **Schedule reorder within 48 hrs.**",
            icon=None,
        )

# OK materials summary
if not ok_df.empty:
    ok_names = " · ".join(ok_df["Material"].tolist())
    st.success(f"✅ **Adequate Stock:** {ok_names}", icon=None)

st.markdown("---")


# ─────────────────────────────────────────────
#  SECTION 3 — INTERACTIVE VISUALIZATIONS
# ─────────────────────────────────────────────
st.markdown("<div class='section-title'>📈 Interactive Visualizations</div>", unsafe_allow_html=True)

chart_col1, chart_col2 = st.columns(2, gap="medium")

with chart_col1:
    st.plotly_chart(chart_stock_vs_threshold(df), use_container_width=True, config={"displayModeBar": False})

with chart_col2:
    st.plotly_chart(chart_days_until_stockout(df), use_container_width=True, config={"displayModeBar": False})

chart_col3, chart_col4 = st.columns([1, 1], gap="medium")

with chart_col3:
    st.plotly_chart(chart_inventory_value(df), use_container_width=True, config={"displayModeBar": False})

with chart_col4:
    st.plotly_chart(chart_consumption_heatmap(df), use_container_width=True, config={"displayModeBar": False})

st.markdown("---")


# ─────────────────────────────────────────────
#  SECTION 4 — PREDICTIVE ANALYTICS TABLE
# ─────────────────────────────────────────────
st.markdown("<div class='section-title'>🔬 Predictive Burn Rate Analytics</div>", unsafe_allow_html=True)

# Build display table with status pills embedded as text labels
display_df = df[[
    "Material", "Category", "Current_Stock_Tons",
    "Simulated_Consumption_Tons", "Days_Until_Stockout",
    "Supplier_Lead_Time_Days", "Days_To_Reorder_Level",
    "Inventory_Value_PKR", "Alert_Status", "Supplier",
]].copy()

display_df.rename(columns={
    "Current_Stock_Tons":           "Stock (T)",
    "Simulated_Consumption_Tons":   "Sim. Burn/Day (T)",
    "Days_Until_Stockout":          "Days to Stockout",
    "Supplier_Lead_Time_Days":      "Lead Time (Days)",
    "Days_To_Reorder_Level":        "Days to Reorder Lvl",
    "Inventory_Value_PKR":          "Value (PKR)",
    "Alert_Status":                 "Status",
}, inplace=True)

# Format value column
display_df["Value (PKR)"] = display_df["Value (PKR)"].apply(lambda v: f"{v:,.0f}")

def color_status(val):
    """Colour-code the Status column in the dataframe."""
    colors = {
        "CRITICAL": "background-color:#3d0f0f; color:#fca5a5; font-weight:700;",
        "WARNING":  "background-color:#3d2d0a; color:#fcd34d; font-weight:700;",
        "OK":       "background-color:#0a2d1f; color:#6ee7b7; font-weight:700;",
    }
    return colors.get(val, "")

styled = (
    display_df.style
    .applymap(color_status, subset=["Status"])
    .format({
        "Stock (T)":              "{:.1f}",
        "Sim. Burn/Day (T)":      "{:.2f}",
        "Days to Stockout":       "{:.1f}",
        "Days to Reorder Lvl":    "{:.1f}",
    })
    .set_properties(**{
        "font-family":  "DM Sans, sans-serif",
        "font-size":    "0.82rem",
        "color":        "#c9d4ef",
        "background":   "#111827",
        "border-color": "#1e2d45",
    })
    .set_table_styles([
        {"selector": "th", "props": [
            ("background-color", "#0d1525"),
            ("color", "#8b9ab8"),
            ("font-size", "0.7rem"),
            ("font-weight", "700"),
            ("letter-spacing", "0.07em"),
            ("text-transform", "uppercase"),
            ("border-bottom", "1px solid #1e2d45"),
        ]},
    ])
    .highlight_min(subset=["Days to Stockout"], color="#3d0f0f")
    .highlight_max(subset=["Days to Stockout"], color="#0a2d1f")
)

st.dataframe(styled, use_container_width=True, height=250)

st.markdown("---")


# ─────────────────────────────────────────────
#  SECTION 5 — SCENARIO SUMMARY CALLOUT
# ─────────────────────────────────────────────
st.markdown("<div class='section-title'>📋 Scenario Impact Summary</div>", unsafe_allow_html=True)

sum_col1, sum_col2, sum_col3 = st.columns(3, gap="medium")

with sum_col1:
    reorder_urgency_days = df["Days_To_Reorder_Level"].min()
    st.markdown(f"""
    <div style='background:{DARK_BG}; border:1px solid {GRID_COLOR};
                border-radius:12px; padding:1.2rem;'>
        <div style='font-size:0.68rem; color:#4a5a78; text-transform:uppercase;
                    letter-spacing:0.1em; margin-bottom:0.5rem;'>Most Urgent Reorder</div>
        <div style='font-family:Syne; font-size:1.5rem; color:#f0f4ff; font-weight:800;'>
            {reorder_urgency_days:.1f} days
        </div>
        <div style='font-size:0.75rem; color:#8b9ab8; margin-top:0.25rem;'>
            Until first material hits reorder threshold
        </div>
    </div>
    """, unsafe_allow_html=True)

with sum_col2:
    total_daily_burn = df["Simulated_Consumption_Tons"].sum()
    st.markdown(f"""
    <div style='background:{DARK_BG}; border:1px solid {GRID_COLOR};
                border-radius:12px; padding:1.2rem;'>
        <div style='font-size:0.68rem; color:#4a5a78; text-transform:uppercase;
                    letter-spacing:0.1em; margin-bottom:0.5rem;'>Total Daily Burn Rate</div>
        <div style='font-family:Syne; font-size:1.5rem; color:#f0f4ff; font-weight:800;'>
            {total_daily_burn:.2f} T/day
        </div>
        <div style='font-size:0.75rem; color:#8b9ab8; margin-top:0.25rem;'>
            Combined across all {len(df)} active materials
        </div>
    </div>
    """, unsafe_allow_html=True)

with sum_col3:
    extra_cost_per_day = (
        df["Simulated_Consumption_Tons"] * df["Unit_Cost_PKR_per_Ton"]
    ).sum()
    st.markdown(f"""
    <div style='background:{DARK_BG}; border:1px solid {GRID_COLOR};
                border-radius:12px; padding:1.2rem;'>
        <div style='font-size:0.68rem; color:#4a5a78; text-transform:uppercase;
                    letter-spacing:0.1em; margin-bottom:0.5rem;'>Est. Daily Material Cost</div>
        <div style='font-family:Syne; font-size:1.5rem; color:#f0f4ff; font-weight:800;'>
            {fmt_pkr(extra_cost_per_day)}
        </div>
        <div style='font-size:0.75rem; color:#8b9ab8; margin-top:0.25rem;'>
            At ×{spike_factor:.2f} production load
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown(f"""
<div class='footer'>
    Master Group of Industries — Supply Chain Intelligence Platform &nbsp;·&nbsp;
    Foam & Mattress Division &nbsp;·&nbsp; Build v2.1.0 &nbsp;·&nbsp;
    Powered by Python · Streamlit · Plotly &nbsp;·&nbsp;
    {datetime.now().strftime("%Y")} MGI Internal Systems. All rights reserved.
</div>
""", unsafe_allow_html=True)
