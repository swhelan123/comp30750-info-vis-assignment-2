import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

# -- page config --
st.set_page_config(
    page_title="Lichess Insights Dashboard",
    page_icon="♟️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# light theme css
st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,300;0,8..60,400;0,8..60,600;0,8..60,700;1,8..60,400&family=Inter:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

    /* ===== FORCE LIGHT on every Streamlit surface ===== */
    .stApp,
    .stApp > header,
    .main .block-container {
        background: #ffffff !important;
        color: #1e293b !important;
    }

    /* top toolbar / header bar */
    header[data-testid="stHeader"] {
        background: #ffffff !important;
        border-bottom: 1px solid #e2e8f0;
    }
    /* deploy button area */
    .stDeployButton,
    header[data-testid="stHeader"] button,
    header[data-testid="stHeader"] [data-testid="stToolbar"] {
        color: #94a3b8 !important;
    }

    /* sidebar */
    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] > div:first-child {
        background: #f8fafc !important;
        border-right: 1px solid #e2e8f0 !important;
    }
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown li,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stMarkdown span {
        color: #475569 !important;
    }
    section[data-testid="stSidebar"] hr {
        border-color: #e2e8f0 !important;
    }

    /* force all body text */
    .stMarkdown, .stMarkdown p, .stMarkdown li,
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #1e293b !important;
    }

    /* main title */
    .hero-title {
        font-family: 'Source Serif 4', Georgia, serif;
        font-size: 2.4rem;
        font-weight: 700;
        color: #0f172a !important;
        text-align: center;
        padding: 0.5rem 0 0.2rem 0;
        letter-spacing: -0.5px;
        line-height: 1.2;
    }
    .hero-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.05rem;
        color: #64748b !important;
        text-align: center;
        margin-bottom: 1.5rem;
        font-weight: 400;
        letter-spacing: 0;
    }

    /* kpi cards */
    .kpi-container {
        display: flex;
        gap: 1rem;
        justify-content: center;
        flex-wrap: wrap;
        margin: 1.2rem 0 2rem 0;
    }
    .kpi-card {
        background: #f8fafc !important;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.2rem 1.8rem;
        text-align: center;
        min-width: 180px;
        flex: 1;
        transition: all 0.2s ease;
        position: relative;
        overflow: hidden;
    }
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: #4f46e5;
        border-radius: 12px 12px 0 0;
    }
    .kpi-card:hover {
        border-color: #c7d2fe;
        box-shadow: 0 4px 16px rgba(79,70,229,0.08);
    }
    .kpi-icon {
        font-size: 1.8rem;
        margin-bottom: 0.3rem;
    }
    .kpi-value {
        font-family: 'Source Serif 4', Georgia, serif;
        font-size: 1.7rem;
        font-weight: 700;
        color: #1e293b !important;
    }
    .kpi-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem;
        color: #94a3b8 !important;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-top: 0.2rem;
        font-weight: 500;
    }

    /* section headers */
    .section-header {
        font-family: 'Source Serif 4', Georgia, serif;
        font-size: 1.35rem;
        font-weight: 700;
        color: #0f172a !important;
        padding: 1rem 0 0.3rem 0;
        border-bottom: 2px solid #e2e8f0;
        margin: 2.5rem 0 0.5rem 0;
        display: flex;
        align-items: center;
        gap: 0.6rem;
    }
    .section-header .num {
        background: #4f46e5;
        color: #fff !important;
        font-size: 0.8rem;
        padding: 0.2rem 0.6rem;
        border-radius: 6px;
        font-weight: 700;
        font-family: 'Inter', sans-serif;
    }
    .section-desc {
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
        color: #64748b !important;
        margin: 0.4rem 0 1.2rem 0;
        line-height: 1.7;
        font-weight: 400;
    }

    /* insight callouts */
    .insight-box {
        background: #f0fdf4 !important;
        border-left: 3px solid #16a34a;
        border-radius: 0 8px 8px 0;
        padding: 0.9rem 1.2rem;
        margin: 0.8rem 0 1.5rem 0;
        font-family: 'Inter', sans-serif;
        font-size: 0.88rem;
        color: #14532d !important;
        line-height: 1.7;
    }
    .insight-box strong {
        color: #15803d !important;
    }

    /* warning callout */
    .warning-box {
        background: #fffbeb !important;
        border-left: 3px solid #f59e0b;
        border-radius: 0 8px 8px 0;
        padding: 0.9rem 1.2rem;
        margin: 0.8rem 0 1.5rem 0;
        font-family: 'Inter', sans-serif;
        font-size: 0.88rem;
        color: #78350f !important;
        line-height: 1.7;
    }

    /* divider */
    .section-divider {
        height: 1px;
        background: #e2e8f0;
        margin: 2rem 0;
        border: none;
    }

    /* footer */
    .footer {
        text-align: center;
        color: #94a3b8 !important;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.75rem;
        margin-top: 3rem;
        padding: 1.5rem 0;
        border-top: 1px solid #e2e8f0;
    }

    /* ===== Streamlit widget overrides ===== */
    .stSelectbox label, .stMultiSelect label, .stSlider label, .stRadio label {
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        color: #334155 !important;
    }
    /* toggle label */
    .stCheckbox label span,
    div[data-testid="stToggle"] label span {
        color: #334155 !important;
    }
    div[data-testid="stMetric"] {
        background: #f8fafc !important;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: transparent !important;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        color: #94a3b8 !important;
        background: transparent !important;
        border-radius: 8px 8px 0 0;
        padding: 0.5rem 1.2rem;
    }
    .stTabs [aria-selected="true"] {
        color: #4f46e5 !important;
        border-bottom: 2px solid #4f46e5 !important;
    }

    /* multiselect pills */
    span[data-baseweb="tag"] {
        background: #eef2ff !important;
        color: #3730a3 !important;
        border: 1px solid #c7d2fe !important;
    }
    span[data-baseweb="tag"] span[role="presentation"] {
        color: #4f46e5 !important;
    }

    /* slider */
    div[data-baseweb="slider"] div {
        color: #475569 !important;
    }

    /* info boxes */
    .stAlert, div[data-testid="stNotification"] {
        background: #f8fafc !important;
        color: #334155 !important;
        border: 1px solid #e2e8f0 !important;
    }
</style>
""",
    unsafe_allow_html=True,
)


# -- load data (cached so it only runs once) --


@st.cache_data
def load_data():
    df_scatter = pd.read_csv("task1_scatter.csv")
    df_tiers = pd.read_csv("task2_tiers.csv")
    df_openings = pd.read_csv("task3_openings.csv")
    df_upsets = pd.read_csv("task5_upsets.csv")
    return df_scatter, df_tiers, df_openings, df_upsets


df_scatter, df_tiers, df_openings, df_upsets = load_data()

# -- shared plotly layout for the light theme --
PLOTLY_LAYOUT = dict(
    template="plotly_white",
    paper_bgcolor="rgba(255,255,255,0)",
    plot_bgcolor="rgba(255,255,255,0)",
    font=dict(family="Inter, sans-serif", color="#334155", size=12),
    title_font=dict(family="Source Serif 4, Georgia, serif", size=16, color="#0f172a"),
    legend=dict(
        bgcolor="rgba(255,255,255,0.9)",
        bordercolor="#e2e8f0",
        borderwidth=1,
        font=dict(size=11, color="#475569"),
    ),
    margin=dict(t=60, b=50, l=60, r=30),
    hoverlabel=dict(
        bgcolor="#ffffff",
        bordercolor="#cbd5e1",
        font=dict(family="IBM Plex Mono, monospace", size=12, color="#1e293b"),
    ),
    xaxis=dict(gridcolor="rgba(0,0,0,0.04)"),
    yaxis=dict(gridcolor="rgba(0,0,0,0.04)"),
)

COLORS = {
    "primary": "#6366f1",
    "secondary": "#a78bfa",
    "accent": "#c084fc",
    "success": "#22c55e",
    "warning": "#f59e0b",
    "danger": "#ef4444",
    "white_piece": "#f0d9b5",
    "black_piece": "#6366f1",
    "draw": "#f59e0b",
    "mate": "#ef4444",
    "resign": "#f97316",
    "outoftime": "#22d3ee",
    "draw_status": "#a78bfa",
}

VICTORY_COLORS = {
    "mate": "#ef4444",
    "resign": "#f97316",
    "outoftime": "#22d3ee",
    "draw": "#a78bfa",
}

# -- header --
st.markdown('<div class="hero-title">♟️ Lichess Insights</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-subtitle">Does moving first give White a meaningful advantage, and what factors strengthen or weaken it?</div>',
    unsafe_allow_html=True,
)

# -- top-level stats (kept for use in insight boxes, but no KPI cards shown) --
total_games = len(df_scatter)
avg_turns = df_scatter["turns"].mean()
avg_rating_diff = df_scatter["rating_diff"].abs().mean()
mate_pct = len(df_scatter[df_scatter["victory_status"] == "mate"]) / total_games * 100
resign_pct = (
    len(df_scatter[df_scatter["victory_status"] == "resign"]) / total_games * 100
)
white_wins_total = df_tiers[df_tiers["winner"] == "white"]["game_count"].sum()
black_wins_total = df_tiers[df_tiers["winner"] == "black"]["game_count"].sum()
draw_total = df_tiers[df_tiers["winner"] == "draw"]["game_count"].sum()
white_adv = white_wins_total / (white_wins_total + black_wins_total + draw_total) * 100

# -- sidebar filters --
with st.sidebar:
    st.markdown("## ♟️ Dashboard Controls")
    st.markdown("---")

    st.markdown("### 🎯 Task 1 Filters")
    status_filter = st.multiselect(
        "Victory Status",
        options=sorted(df_scatter["victory_status"].unique()),
        default=sorted(df_scatter["victory_status"].unique()),
        help="Filter game outcomes in the scatterplot",
    )

    max_turns_limit = int(df_scatter["turns"].max())
    turn_range = st.slider(
        "Turn Range",
        min_value=1,
        max_value=max_turns_limit,
        value=(1, max_turns_limit),
        help="Filter games by number of turns",
    )

    rating_diff_abs_max = int(df_scatter["rating_diff"].abs().max())
    rating_diff_range = st.slider(
        "Absolute Rating Difference",
        min_value=0,
        max_value=rating_diff_abs_max,
        value=(0, rating_diff_abs_max),
        help="Filter by absolute rating gap between players",
    )

    heatmap_view = st.radio(
        "Heatmap View",
        ["Combined", "Split by Outcome"],
        index=0,
        help="Show a single combined heatmap or separate heatmaps per game-end reason. In split mode, hovering over any cell shows counts for all outcome types at that location.",
    )

    st.markdown("---")
    st.markdown("### 🫧 Task 3 Options")
    top_n_openings = st.slider(
        "Top N Most-Played Openings",
        min_value=5,
        max_value=15,
        value=12,
        help="Select the N most frequently played openings in the dataset. They are then ranked by White win rate on the chart.",
    )

    st.markdown("---")
    st.markdown("### 🏆 Task 5 Options")
    gap_bin_size = st.slider(
        "Rating Gap Bin Width",
        min_value=25,
        max_value=100,
        value=50,
        step=25,
        help="Controls granularity of upset rate bins",
    )
    max_gap_display = st.slider(
        "Max Rating Gap to Display",
        min_value=200,
        max_value=1600,
        value=800,
        step=100,
        help="Limit the x-axis range",
    )

    st.markdown("---")
    st.markdown(
        """
    <div style="text-align:center; color:#94a3b8; font-size:0.75rem; margin-top:1rem;">
        Built with Streamlit & Plotly<br/>
        Data: Lichess Open Database + Chess.com
    </div>
    """,
        unsafe_allow_html=True,
    )

# -----------------------------------------------
# Task 1: Scatterplot - rating diff vs game length
# -----------------------------------------------
st.markdown(
    '<div class="section-header"><span class="num">01</span> Setting the Scene: Skill Gap &amp; Game Length</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-desc">Before measuring White\'s advantage, it is necessary to understand the underlying dataset. Does the skill gap between players affect how long games last and how they end? Large mismatches may overshadow any first-move effect, so establishing this context is important when interpreting the subsequent analyses.</div>',
    unsafe_allow_html=True,
)

# apply sidebar filters
filtered_scatter = df_scatter[
    (df_scatter["victory_status"].isin(status_filter))
    & (df_scatter["turns"] >= turn_range[0])
    & (df_scatter["turns"] <= turn_range[1])
    & (df_scatter["rating_diff"].abs() >= rating_diff_range[0])
    & (df_scatter["rating_diff"].abs() <= rating_diff_range[1])
]

if heatmap_view == "Combined":
    # ---- single combined heatmap (original view) ----
    fig1 = go.Figure()
    fig1.add_trace(
        go.Histogram2d(
            x=filtered_scatter["rating_diff"],
            y=filtered_scatter["turns"],
            colorscale=[
                [0, "rgba(255,255,255,0)"],
                [0.05, "#eef2ff"],
                [0.15, "#c7d2fe"],
                [0.3, "#a5b4fc"],
                [0.5, "#6366f1"],
                [0.7, "#4f46e5"],
                [0.9, "#3730a3"],
                [1, "#1e1b4b"],
            ],
            nbinsx=100,
            nbinsy=80,
            colorbar=dict(
                title=dict(text="Games", font=dict(size=11, color="#64748b")),
                tickfont=dict(color="#64748b"),
                thickness=12,
                len=0.6,
            ),
            hovertemplate="Rating Diff: %{x}<br>Turns: %{y}<br>Count: %{z}<extra></extra>",
        )
    )

    fig1.update_layout(**PLOTLY_LAYOUT)
    fig1.update_layout(
        title="Game Length vs. Skill Gap: Where Do Games Concentrate?",
        xaxis=dict(
            title="Rating Differential (White − Black)",
            gridcolor="rgba(0,0,0,0.04)",
            zeroline=True,
            zerolinecolor="rgba(0,0,0,0.12)",
            zerolinewidth=1,
        ),
        yaxis=dict(
            title="Number of Turns",
            gridcolor="rgba(0,0,0,0.04)",
        ),
        height=520,
    )
    fig1.add_vrect(
        x0=-50,
        x1=50,
        fillcolor="rgba(79,70,229,0.04)",
        layer="below",
        line_width=0,
        annotation_text="Evenly Matched",
        annotation_position="top",
        annotation_font=dict(size=10, color="#4f46e5"),
    )
    st.plotly_chart(fig1, use_container_width=True)

else:
    # ---- split heatmaps by victory_status with cross-panel tooltips ----
    _SPLIT_STATUS_COLORS = {
        "mate": [
            [0, "rgba(255,255,255,0)"],
            [0.05, "#fef2f2"],
            [0.15, "#fecaca"],
            [0.3, "#fca5a5"],
            [0.5, "#ef4444"],
            [0.7, "#dc2626"],
            [0.9, "#b91c1c"],
            [1, "#7f1d1d"],
        ],
        "resign": [
            [0, "rgba(255,255,255,0)"],
            [0.05, "#fff7ed"],
            [0.15, "#fed7aa"],
            [0.3, "#fdba74"],
            [0.5, "#f97316"],
            [0.7, "#ea580c"],
            [0.9, "#c2410c"],
            [1, "#7c2d12"],
        ],
        "outoftime": [
            [0, "rgba(255,255,255,0)"],
            [0.05, "#ecfeff"],
            [0.15, "#a5f3fc"],
            [0.3, "#67e8f9"],
            [0.5, "#22d3ee"],
            [0.7, "#06b6d4"],
            [0.9, "#0891b2"],
            [1, "#155e75"],
        ],
        "draw": [
            [0, "rgba(255,255,255,0)"],
            [0.05, "#f5f3ff"],
            [0.15, "#ddd6fe"],
            [0.3, "#c4b5fd"],
            [0.5, "#a78bfa"],
            [0.7, "#8b5cf6"],
            [0.9, "#7c3aed"],
            [1, "#4c1d95"],
        ],
    }

    _SPLIT_STATUS_LABELS = {
        "mate": "Checkmate",
        "resign": "Resignation",
        "outoftime": "Out of Time",
        "draw": "Draw",
    }

    _SPLIT_STATUS_ORDER = ["draw", "mate", "resign", "outoftime"]
    active_statuses = [
        s
        for s in _SPLIT_STATUS_ORDER
        if s in filtered_scatter["victory_status"].unique()
    ]

    if len(active_statuses) == 0:
        st.info("No games match the current filters.")
    else:
        # --- pre-compute shared 2-D bins across all statuses ---
        x_vals = filtered_scatter["rating_diff"].values
        y_vals = filtered_scatter["turns"].values
        nbx, nby = 60, 50
        x_edges = np.linspace(x_vals.min(), x_vals.max(), nbx + 1)
        y_edges = np.linspace(y_vals.min(), y_vals.max(), nby + 1)
        x_centers = (x_edges[:-1] + x_edges[1:]) / 2
        y_centers = (y_edges[:-1] + y_edges[1:]) / 2

        status_grids: dict[str, np.ndarray] = {}
        for s in active_statuses:
            mask = (filtered_scatter["victory_status"] == s).values
            H, _, _ = np.histogram2d(
                x_vals[mask], y_vals[mask], bins=[x_edges, y_edges]
            )
            status_grids[s] = H.T  # shape (nby, nbx)

        # --- subplot grid: single row, all panels side by side ---
        n = len(active_statuses)
        ncols = n
        nrows = 1

        fig1 = make_subplots(
            rows=1,
            cols=ncols,
            subplot_titles=[
                _SPLIT_STATUS_LABELS.get(s, s.capitalize()) for s in active_statuses
            ],
            shared_xaxes=True,
            shared_yaxes=True,
            horizontal_spacing=0.04,
        )

        for idx, s in enumerate(active_statuses):
            row = 1
            col = idx + 1

            z = status_grids[s]

            # build customdata with counts from every *other* status
            other_statuses = [os for os in active_statuses if os != s]
            if other_statuses:
                cd = np.stack([status_grids[os] for os in other_statuses], axis=-1)
            else:
                cd = np.zeros((*z.shape, 1))

            # hover template: show this panel's count bolded, plus all others
            ht_lines = [
                "Rating Diff: %{x:.0f}<br>Turns: %{y:.0f}<br>",
                f"<b>{_SPLIT_STATUS_LABELS.get(s, s.capitalize())}: %{{z:.0f}}</b>",
            ]
            for i, os in enumerate(other_statuses):
                ht_lines.append(
                    f"{_SPLIT_STATUS_LABELS.get(os, os.capitalize())}: %{{customdata[{i}]:.0f}}"
                )
            hovertemplate = "<br>".join(ht_lines) + "<extra></extra>"

            fig1.add_trace(
                go.Heatmap(
                    z=z,
                    x=x_centers,
                    y=y_centers,
                    colorscale=_SPLIT_STATUS_COLORS.get(
                        s,
                        [
                            [0, "rgba(255,255,255,0)"],
                            [0.5, "#6366f1"],
                            [1, "#1e1b4b"],
                        ],
                    ),
                    customdata=cd,
                    hovertemplate=hovertemplate,
                    showscale=False,
                    name=_SPLIT_STATUS_LABELS.get(s, s.capitalize()),
                ),
                row=row,
                col=col,
            )

        fig1.update_layout(**PLOTLY_LAYOUT)
        fig1.update_layout(
            title="Game Length vs. Skill Gap — Split by Outcome",
            height=500,
            hovermode="closest",
        )

        # enable cross-subplot spike lines (crosshairs) on every axis
        fig1.update_xaxes(
            showspikes=True,
            spikemode="across",
            spikesnap="cursor",
            spikethickness=1,
            spikecolor="#94a3b8",
            spikedash="dot",
            gridcolor="rgba(0,0,0,0.04)",
        )
        fig1.update_yaxes(
            showspikes=True,
            spikemode="across",
            spikesnap="cursor",
            spikethickness=1,
            spikecolor="#94a3b8",
            spikedash="dot",
            gridcolor="rgba(0,0,0,0.04)",
        )

        # x-axis label on every panel (single row, all visible)
        for col_idx in range(1, ncols + 1):
            x_key = "xaxis" if col_idx == 1 else f"xaxis{col_idx}"
            fig1.update_layout(**{x_key: dict(title="Rating Diff (White − Black)")})

        # y-axis label only on the first (leftmost) panel
        fig1.update_layout(yaxis=dict(title="Number of Turns"))

        st.plotly_chart(fig1, use_container_width=True)

# quick stats for the insight box
mate_games = filtered_scatter[filtered_scatter["victory_status"] == "mate"]
resign_games = filtered_scatter[filtered_scatter["victory_status"] == "resign"]
avg_mate_turns = mate_games["turns"].mean() if len(mate_games) > 0 else 0
avg_resign_turns = resign_games["turns"].mean() if len(resign_games) > 0 else 0

st.markdown(
    f"""<div class="insight-box">
    💡 <strong>Context:</strong> Checkmates average <strong>{avg_mate_turns:.0f} turns</strong>, whilst
    resignations average <strong>{avg_resign_turns:.0f}</strong>. Players tend to concede before the actual
    mate, particularly when the skill gap is large. Games with substantial rating differences cluster towards
    shorter turn counts, confirming that mismatched games are a confounding variable. To account for this,
    the following section breaks down White's advantage across skill tiers.
</div>""",
    unsafe_allow_html=True,
)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# -----------------------------------------------
# Task 2: White vs Black wins by tier
# -----------------------------------------------
st.markdown(
    '<div class="section-header"><span class="num">02</span> The White Advantage: Real or Myth?</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-desc">White moves first in every game of chess. Does that translate into a measurable win-rate advantage across 20,000 online games, and does it hold equally across all skill levels, or does it diminish as players improve?</div>',
    unsafe_allow_html=True,
)

tier_order = [
    "1. Novice (<1200)",
    "2. Intermediate (1200-1499)",
    "3. Advanced (1500-1799)",
    "4. Master (1800+)",
]

# build per-tier percentages (denominator = ALL games including draws)
t2_rows = []
for tier in tier_order:
    tier_data = df_tiers[df_tiers["rating_tier"] == tier]
    white_count = tier_data[tier_data["winner"] == "white"]["game_count"].values
    black_count = tier_data[tier_data["winner"] == "black"]["game_count"].values
    draw_count = tier_data[tier_data["winner"] == "draw"]["game_count"].values
    wc = int(white_count[0]) if len(white_count) > 0 else 0
    bc = int(black_count[0]) if len(black_count) > 0 else 0
    dc = int(draw_count[0]) if len(draw_count) > 0 else 0
    total = wc + bc + dc
    friendly = tier.split(". ")[1] if ". " in tier else tier
    t2_rows.append(
        {
            "tier": friendly,
            "White Win %": wc / total * 100 if total else 0,
            "Draw %": dc / total * 100 if total else 0,
            "Black Win %": bc / total * 100 if total else 0,
            "wc": wc,
            "bc": bc,
            "dc": dc,
            "total": total,
        }
    )

fig2 = go.Figure()

tier_labels = [r["tier"] for r in t2_rows]

fig2.add_trace(
    go.Bar(
        x=tier_labels,
        y=[r["White Win %"] for r in t2_rows],
        name="White Wins",
        marker=dict(color="#f0d9b5", line=dict(color="#dfc198", width=0.5)),
        text=[f"{r['White Win %']:.1f}%" for r in t2_rows],
        textposition="outside",
        textfont=dict(color="#78716c", size=11, family="IBM Plex Mono"),
        hovertemplate="<b>%{x}</b><br>White: %{y:.1f}% (%{customdata:,} games)<extra></extra>",
        customdata=[r["wc"] for r in t2_rows],
    )
)
fig2.add_trace(
    go.Bar(
        x=tier_labels,
        y=[r["Black Win %"] for r in t2_rows],
        name="Black Wins",
        marker=dict(color="#4f46e5", line=dict(color="#6366f1", width=0.5)),
        text=[f"{r['Black Win %']:.1f}%" for r in t2_rows],
        textposition="outside",
        textfont=dict(color="#6366f1", size=11, family="IBM Plex Mono"),
        hovertemplate="<b>%{x}</b><br>Black: %{y:.1f}% (%{customdata:,} games)<extra></extra>",
        customdata=[r["bc"] for r in t2_rows],
    )
)
fig2.add_trace(
    go.Bar(
        x=tier_labels,
        y=[r["Draw %"] for r in t2_rows],
        name="Draws",
        marker=dict(color="#e2e8f0", line=dict(color="#cbd5e1", width=0.5)),
        text=[f"{r['Draw %']:.1f}%" for r in t2_rows],
        textposition="outside",
        textfont=dict(color="#94a3b8", size=10, family="IBM Plex Mono"),
        hovertemplate="<b>%{x}</b><br>Draw: %{y:.1f}% (%{customdata:,} games)<extra></extra>",
        customdata=[r["dc"] for r in t2_rows],
    )
)

fig2.update_layout(**PLOTLY_LAYOUT)
fig2.update_layout(
    barmode="group",
    title="Win Rate by Skill Tier (% of all games)",
    xaxis=dict(
        title="",
        categoryorder="array",
        categoryarray=tier_labels,
    ),
    yaxis=dict(
        title="% of Games",
        gridcolor="rgba(0,0,0,0.04)",
        range=[0, max(r["White Win %"] for r in t2_rows) + 8],
    ),
    height=460,
    bargap=0.25,
    bargroupgap=0.08,
    legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5),
)
st.plotly_chart(fig2, use_container_width=True)

# compute which tier has biggest/smallest white advantage (consistent denominator: W+B+D)
tier_advantages = []
for tier in tier_order:
    td = df_tiers[df_tiers["rating_tier"] == tier]
    wc = td[td["winner"] == "white"]["game_count"].values
    bc = td[td["winner"] == "black"]["game_count"].values
    dc = td[td["winner"] == "draw"]["game_count"].values
    w = int(wc[0]) if len(wc) > 0 else 0
    b = int(bc[0]) if len(bc) > 0 else 0
    d = int(dc[0]) if len(dc) > 0 else 0
    total = w + b + d
    w_pct = w / total * 100 if total > 0 else 50
    b_pct = b / total * 100 if total > 0 else 50
    d_pct = d / total * 100 if total > 0 else 0
    tier_advantages.append((tier.split(". ")[1], w_pct, b_pct, d_pct))

max_adv_tier = max(tier_advantages, key=lambda x: x[1])
min_adv_tier = min(tier_advantages, key=lambda x: x[1])

# draw rate at highest tier
max_draw_tier = max(tier_advantages, key=lambda x: x[3])

st.markdown(
    f"""<div class="insight-box">
    💡 <strong>Finding:</strong> The answer depends on how the results are counted. White wins more
    <em>decisive</em> games at every tier; however, once draws are included, the picture changes. Only
    <strong>{max_adv_tier[0]}</strong> ({max_adv_tier[1]:.1f}%) shows White clearly above 50% of all games.
    At <strong>{min_adv_tier[0]}</strong> level, White's overall win rate drops to just
    <strong>{min_adv_tier[1]:.1f}%</strong>, as draws reach {max_draw_tier[3]:.1f}%, which is sufficient to
    erase the first-move edge entirely. The advantage is real but fragile: stronger players neutralise it
    by steering towards drawn positions.
</div>""",
    unsafe_allow_html=True,
)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# -----------------------------------------------
# Task 3: Opening analysis
# -----------------------------------------------
st.markdown(
    '<div class="section-header"><span class="num">03</span> Does Opening Choice Affect White\'s Edge?</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-desc">White has the initiative to dictate the opening. Do certain openings amplify the first-move advantage more than others? The slider selects the <strong>N most popular openings</strong> (ranked by total number of games played). Those openings are then displayed ordered by White\'s win rate so you can compare effectiveness across the most common choices. Bubble size encodes game count and colour indicates the opening type (1.e4, 1.d4, or Flank / Irregular).</div>',
    unsafe_allow_html=True,
)

# aggregate opening stats from the raw data
opening_stats = []
for name in df_openings["opening_name"].unique():
    subset = df_openings[df_openings["opening_name"] == name]
    total = subset["total_games"].iloc[0]
    white_wins = subset[subset["winner"] == "white"]["outcome_count"].values
    black_wins = subset[subset["winner"] == "black"]["outcome_count"].values
    draws = subset[subset["winner"] == "draw"]["outcome_count"].values
    ww = int(white_wins[0]) if len(white_wins) > 0 else 0
    bw = int(black_wins[0]) if len(black_wins) > 0 else 0
    dd = int(draws[0]) if len(draws) > 0 else 0
    opening_stats.append(
        {
            "opening": name,
            "total_games": total,
            "white_wins": ww,
            "black_wins": bw,
            "draws": dd,
            "white_wr": ww / total * 100 if total > 0 else 50,
            "black_wr": bw / total * 100 if total > 0 else 50,
            "draw_rate": dd / total * 100 if total > 0 else 0,
        }
    )

df_ops = pd.DataFrame(opening_stats).sort_values("total_games", ascending=False)
df_ops_top = df_ops.head(top_n_openings).sort_values("white_wr", ascending=True)


# classify openings by first-move type
def classify_opening_type(name):
    """Classify an opening name into 1.e4, 1.d4, or Flank/Irregular."""
    e4_keywords = [
        "Sicilian",
        "French",
        "Caro-Kann",
        "Scandinavian",
        "Italian",
        "Scotch",
        "Philidor",
        "Ruy Lopez",
        "Petrov",
        "Pirc",
        "Alekhine",
        "King's Gambit",
        "Vienna",
        "Bishop's Opening",
    ]
    d4_keywords = [
        "Queen's Pawn",
        "Queen's Gambit",
        "Indian",
        "Slav",
        "Dutch",
        "Benoni",
        "Grunfeld",
        "Nimzo",
        "Bogo",
        "Catalan",
        "Trompowsky",
        "London",
        "Torre",
        "Colle",
    ]
    for kw in e4_keywords:
        if kw.lower() in name.lower():
            return "1.e4"
    for kw in d4_keywords:
        if kw.lower() in name.lower():
            return "1.d4"
    return "Flank / Irregular"


df_ops_top["opening_type"] = df_ops_top["opening"].apply(classify_opening_type)

OPENING_TYPE_COLORS = {
    "1.e4": "#e11d48",
    "1.d4": "#2563eb",
    "Flank / Irregular": "#16a34a",
}

fig3 = go.Figure()

# lollipop stalks — horizontal lines from 50% to each data point
for _, row in df_ops_top.iterrows():
    stalk_color = OPENING_TYPE_COLORS[row["opening_type"]]
    fig3.add_shape(
        type="line",
        x0=50,
        x1=row["white_wr"],
        y0=row["opening"],
        y1=row["opening"],
        line=dict(color=stalk_color, width=3, dash="solid"),
        layer="below",
        opacity=0.25,
    )

# one trace per opening type so the legend shows categories
max_games = df_ops_top["total_games"].max()
for op_type in ["1.e4", "1.d4", "Flank / Irregular"]:
    subset = df_ops_top[df_ops_top["opening_type"] == op_type]
    if subset.empty:
        continue
    color = OPENING_TYPE_COLORS[op_type]
    fig3.add_trace(
        go.Scatter(
            x=subset["white_wr"],
            y=subset["opening"],
            mode="markers+text",
            name=op_type,
            legendgroup=op_type,
            marker=dict(
                size=subset["total_games"] / max_games * 45 + 12,
                color=color,
                line=dict(color="#ffffff", width=2),
            ),
            text=[
                f" {wr:.1f}%"
                for wr, _ in zip(subset["white_wr"], subset["total_games"])
            ],
            textposition="middle right",
            textfont=dict(color="#334155", size=10, family="IBM Plex Mono"),
            hovertemplate="<b>%{y}</b><br>Type: "
            + op_type
            + "<br>White WR: %{x:.1f}%<br>Games: %{customdata:,}<extra></extra>",
            customdata=subset["total_games"],
        )
    )


# 50% reference line — strong and clear
fig3.add_vline(
    x=50,
    line_width=2.5,
    line_dash="solid",
    line_color="rgba(0,0,0,0.35)",
    annotation_text="50%: No Advantage",
    annotation_position="top right",
    annotation_font=dict(size=10, color="#64748b"),
)

# shade the "favours white" and "favours black" zones
fig3.add_vrect(
    x0=50,
    x1=df_ops_top["white_wr"].max() + 5,
    fillcolor="rgba(34,197,94,0.04)",
    layer="below",
    line_width=0,
)
fig3.add_vrect(
    x0=df_ops_top["white_wr"].min() - 5,
    x1=50,
    fillcolor="rgba(239,68,68,0.04)",
    layer="below",
    line_width=0,
)

fig3.update_layout(**PLOTLY_LAYOUT)
fig3.update_layout(
    title="White Win Rate by Opening (colour = opening type, size = popularity)",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.05,
        xanchor="center",
        x=0.5,
        title=dict(text="Opening Type  ", font=dict(size=11)),
    ),
    xaxis=dict(
        title="White Win Rate (%)",
        gridcolor="rgba(0,0,0,0.04)",
        range=[
            df_ops_top["white_wr"].min() - 5,
            df_ops_top["white_wr"].max() + 14,
        ],
    ),
    yaxis=dict(
        title="",
        gridcolor="rgba(0,0,0,0.02)",
        categoryorder="array",
        categoryarray=df_ops_top["opening"].tolist(),
    ),
    height=max(450, top_n_openings * 40),
)
st.plotly_chart(fig3, use_container_width=True)

# find the best/worst/most popular openings for the insight
best_opening = df_ops_top.loc[df_ops_top["white_wr"].idxmax()]
worst_opening = df_ops_top.loc[df_ops_top["white_wr"].idxmin()]
most_popular = df_ops_top.loc[df_ops_top["total_games"].idxmax()]
highest_draw = df_ops_top.loc[df_ops_top["draw_rate"].idxmax()]

st.markdown(
    f"""<div class="insight-box">
    💡 <strong>Finding:</strong> Opening choice clearly modulates White's edge. White performs best with
    <strong>{best_opening["opening"]}</strong> ({best_opening["white_wr"]:.1f}% WR) and worst with
    <strong>{worst_opening["opening"]}</strong> ({worst_opening["white_wr"]:.1f}%). Notably, the most frequently
    played opening, <strong>{most_popular["opening"]}</strong> ({most_popular["total_games"]} games), is not the
    most effective for White. This suggests that popularity is driven by familiarity rather than competitive advantage.
</div>""",
    unsafe_allow_html=True,
)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# -----------------------------------------------
# Task 4: Upsets - lower rated player winning
# -----------------------------------------------
st.markdown(
    '<div class="section-header"><span class="num">04</span> Rating Gap &amp; Upset Rate: When Does Skill Override Everything?</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-desc">A sufficiently large rating gap between players can dwarf any colour advantage. This section tracks how often the lower-rated player wins as the skill gap grows, and identifies the point at which rating becomes a near-certain predictor of outcome.</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="warning-box">📖 <strong>Definition:</strong> For the purposes of this analysis, an <em>upset</em> is defined as a match in which the lower-rated player wins.</div>',
    unsafe_allow_html=True,
)

# bin the rating gaps
df_upsets_filtered = df_upsets[df_upsets["rating_gap"] <= max_gap_display].copy()
df_upsets_filtered["gap_bin"] = (
    (df_upsets_filtered["rating_gap"] // gap_bin_size) * gap_bin_size
).astype(int)

upset_by_bin = (
    df_upsets_filtered.groupby("gap_bin")
    .apply(
        lambda g: pd.Series(
            {
                "total": len(g),
                "upsets": (g["outcome_type"] == "Upset (Lower Rated Won)").sum(),
                "upset_rate": (g["outcome_type"] == "Upset (Lower Rated Won)").mean()
                * 100,
            }
        ),
        include_groups=False,
    )
    .reset_index()
)

fig5a = make_subplots(specs=[[{"secondary_y": True}]])

upset_rates = upset_by_bin["upset_rate"].values
game_counts = upset_by_bin["total"].values
gap_bins = upset_by_bin["gap_bin"].values

# build human-readable range labels for each bin (e.g. "0–49", "50–99")
bin_labels = [f"{int(b)}–{int(b + gap_bin_size - 1)}" for b in gap_bins]

# bars showing number of games in each bin (primary y-axis)
fig5a.add_trace(
    go.Bar(
        x=bin_labels,
        y=game_counts,
        name="Games in Bin",
        marker=dict(
            color="rgba(99,102,241,0.25)",
            line=dict(color="rgba(99,102,241,0.4)", width=1),
        ),
        hovertemplate=("<b>Rating Gap: %{x}</b><br>Games: %{y:,}<extra></extra>"),
        width=0.85,
    ),
    secondary_y=False,
)

# upset rate line on secondary y-axis
fig5a.add_trace(
    go.Scatter(
        x=bin_labels,
        y=upset_rates,
        mode="lines+markers+text",
        name="Upset Rate %",
        line=dict(color="#ef4444", width=4, shape="spline"),
        marker=dict(
            size=10,
            color="#ef4444",
            line=dict(color="#ffffff", width=2),
            symbol="circle",
        ),
        text=[f"{r:.0f}%" for r in upset_rates],
        textposition="top center",
        textfont=dict(color="#334155", size=10, family="IBM Plex Mono, monospace"),
        hovertemplate=(
            "<b>Rating Gap: %{x}</b><br>Upset Rate: %{y:.1f}%<extra></extra>"
        ),
    ),
    secondary_y=True,
)

fig5a.update_layout(**PLOTLY_LAYOUT)
fig5a.update_layout(
    title="How Likely Is an Upset as the Rating Gap Grows?",
    height=500,
    legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5),
    margin=dict(t=60, b=50, l=60, r=30),
    bargap=0.08,
)
fig5a.update_xaxes(
    title_text="Rating Gap Between Players",
    gridcolor="rgba(0,0,0,0.04)",
    categoryorder="array",
    categoryarray=bin_labels,
    tickangle=0,
)
fig5a.update_yaxes(
    title_text="Number of Games",
    gridcolor="rgba(0,0,0,0.04)",
    secondary_y=False,
)
fig5a.update_yaxes(
    title_text="Upset Rate (%)",
    gridcolor="rgba(0,0,0,0.02)",
    range=[0, max(55, max(upset_rates) + 8)],
    dtick=10,
    showgrid=False,
    secondary_y=True,
)

st.plotly_chart(fig5a, use_container_width=True)

# upset stats for the insight
total_upsets = (df_upsets["outcome_type"] == "Upset (Lower Rated Won)").sum()
total_decisive = len(df_upsets)
overall_upset_pct = total_upsets / total_decisive * 100
close_games = df_upsets[df_upsets["rating_gap"] <= 50]
close_upset_pct = (
    (close_games["outcome_type"] == "Upset (Lower Rated Won)").mean() * 100
    if len(close_games) > 0
    else 0
)
big_gap = df_upsets[df_upsets["rating_gap"] >= 400]
big_gap_upset_pct = (
    (big_gap["outcome_type"] == "Upset (Lower Rated Won)").mean() * 100
    if len(big_gap) > 0
    else 0
)

st.markdown(
    f"""<div class="insight-box">
    💡 <strong>Finding:</strong> Overall, <strong>{overall_upset_pct:.1f}%</strong> of decisive games are upsets.
    When players are near-equal in rating (gap ≤50), the outcome approaches a coin flip at
    <strong>{close_upset_pct:.1f}%</strong>, meaning colour alone could tip the balance. However, once the gap
    reaches 400+, upsets drop to just <strong>{big_gap_upset_pct:.1f}%</strong>, at which point rating
    dominates over any first-move effect.
</div>""",
    unsafe_allow_html=True,
)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)


# -- footer --
st.markdown(
    """<div class="footer">
    ♟️ Lichess Insights · Built with Streamlit + Plotly · Data: Lichess Open Database (20k games) + Chess.com Personal Data · Shane Whelan 2026
</div>""",
    unsafe_allow_html=True,
)
