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

# dark theme css
st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    /* global dark theme */
    .stApp {
        background: linear-gradient(160deg, #0a0a0f 0%, #0d1117 40%, #0f0a1a 70%, #0a0a0f 100%);
        color: #e6edf3;
    }

    /* sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1117 0%, #161b22 50%, #0d1117 100%) !important;
        border-right: 1px solid rgba(99, 102, 241, 0.15);
    }
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown li,
    section[data-testid="stSidebar"] label {
        color: #c9d1d9 !important;
    }

    /* main title */
    .hero-title {
        font-family: 'Orbitron', monospace;
        font-size: 2.6rem;
        font-weight: 900;
        background: linear-gradient(135deg, #a78bfa 0%, #818cf8 25%, #6366f1 50%, #c084fc 75%, #a78bfa 100%);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradient-shift 4s ease infinite;
        text-align: center;
        padding: 0.5rem 0 0.2rem 0;
        letter-spacing: 2px;
        line-height: 1.2;
    }
    .hero-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.05rem;
        color: #8b949e;
        text-align: center;
        margin-bottom: 1.5rem;
        font-weight: 300;
        letter-spacing: 0.5px;
    }

    @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
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
        background: linear-gradient(135deg, rgba(99,102,241,0.08) 0%, rgba(139,92,246,0.05) 100%);
        border: 1px solid rgba(99,102,241,0.2);
        border-radius: 16px;
        padding: 1.2rem 1.8rem;
        text-align: center;
        min-width: 180px;
        flex: 1;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
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
        background: linear-gradient(90deg, #6366f1, #a78bfa, #c084fc);
        border-radius: 16px 16px 0 0;
    }
    .kpi-card:hover {
        border-color: rgba(99,102,241,0.5);
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(99,102,241,0.15);
    }
    .kpi-icon {
        font-size: 1.8rem;
        margin-bottom: 0.3rem;
    }
    .kpi-value {
        font-family: 'Orbitron', monospace;
        font-size: 1.7rem;
        font-weight: 700;
        background: linear-gradient(135deg, #a78bfa, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .kpi-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.78rem;
        color: #8b949e;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-top: 0.2rem;
        font-weight: 500;
    }

    /* section headers */
    .section-header {
        font-family: 'Orbitron', monospace;
        font-size: 1.35rem;
        font-weight: 700;
        color: #c9d1d9;
        padding: 1rem 0 0.3rem 0;
        border-bottom: 2px solid rgba(99,102,241,0.3);
        margin: 2.5rem 0 0.5rem 0;
        display: flex;
        align-items: center;
        gap: 0.6rem;
    }
    .section-header .num {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: #fff;
        font-size: 0.8rem;
        padding: 0.2rem 0.6rem;
        border-radius: 6px;
        font-weight: 700;
    }
    .section-desc {
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
        color: #8b949e;
        margin: 0.4rem 0 1.2rem 0;
        line-height: 1.6;
        font-weight: 300;
    }

    /* insight callouts */
    .insight-box {
        background: linear-gradient(135deg, rgba(34,197,94,0.06) 0%, rgba(16,185,129,0.04) 100%);
        border-left: 3px solid #22c55e;
        border-radius: 0 12px 12px 0;
        padding: 0.9rem 1.2rem;
        margin: 0.8rem 0 1.5rem 0;
        font-family: 'Inter', sans-serif;
        font-size: 0.88rem;
        color: #a7f3d0;
        line-height: 1.6;
    }
    .insight-box strong {
        color: #4ade80;
    }

    /* warning callout */
    .warning-box {
        background: linear-gradient(135deg, rgba(251,191,36,0.06) 0%, rgba(245,158,11,0.04) 100%);
        border-left: 3px solid #f59e0b;
        border-radius: 0 12px 12px 0;
        padding: 0.9rem 1.2rem;
        margin: 0.8rem 0 1.5rem 0;
        font-family: 'Inter', sans-serif;
        font-size: 0.88rem;
        color: #fde68a;
        line-height: 1.6;
    }

    /* divider */
    .section-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(99,102,241,0.3), transparent);
        margin: 2rem 0;
        border: none;
    }

    /* footer */
    .footer {
        text-align: center;
        color: #484f58;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        margin-top: 3rem;
        padding: 1.5rem 0;
        border-top: 1px solid rgba(99,102,241,0.1);
    }

    /* streamlit overrides */
    .stSelectbox label, .stMultiSelect label, .stSlider label, .stRadio label {
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        color: #c9d1d9 !important;
    }
    div[data-testid="stMetric"] {
        background: rgba(99,102,241,0.05);
        border: 1px solid rgba(99,102,241,0.15);
        border-radius: 12px;
        padding: 1rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        color: #8b949e;
        background: transparent;
        border-radius: 8px 8px 0 0;
        padding: 0.5rem 1.2rem;
    }
    .stTabs [aria-selected="true"] {
        color: #a78bfa !important;
        border-bottom: 2px solid #6366f1;
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
    df_ply = pd.read_csv("task4_ply_by_tier.csv")
    df_upsets = pd.read_csv("task5_upsets.csv")
    df_time = pd.read_csv("task6_time_victory.csv")
    return df_scatter, df_tiers, df_openings, df_ply, df_upsets, df_time


df_scatter, df_tiers, df_openings, df_ply, df_upsets, df_time = load_data()

# -- shared plotly layout for the dark theme --
PLOTLY_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(13,17,23,0.6)",
    font=dict(family="Inter, sans-serif", color="#c9d1d9", size=12),
    title_font=dict(family="Orbitron, monospace", size=16, color="#e6edf3"),
    legend=dict(
        bgcolor="rgba(22,27,34,0.8)",
        bordercolor="rgba(99,102,241,0.2)",
        borderwidth=1,
        font=dict(size=11),
    ),
    margin=dict(t=60, b=50, l=60, r=30),
    hoverlabel=dict(
        bgcolor="#1c2128",
        bordercolor="rgba(99,102,241,0.4)",
        font=dict(family="JetBrains Mono, monospace", size=12, color="#e6edf3"),
    ),
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
st.markdown('<div class="hero-title">♟️ LICHESS INSIGHTS</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-subtitle">Exploring patterns in 20,000 online chess games from the Lichess database</div>',
    unsafe_allow_html=True,
)

# -- top-level KPI cards --
total_games = len(df_scatter)
avg_turns = df_scatter["turns"].mean()
avg_rating_diff = df_scatter["rating_diff"].abs().mean()
mate_pct = len(df_scatter[df_scatter["victory_status"] == "mate"]) / total_games * 100
resign_pct = (
    len(df_scatter[df_scatter["victory_status"] == "resign"]) / total_games * 100
)
white_wins_total = df_tiers[df_tiers["winner"] == "white"]["game_count"].sum()
black_wins_total = df_tiers[df_tiers["winner"] == "black"]["game_count"].sum()
white_adv = white_wins_total / (white_wins_total + black_wins_total) * 100

st.markdown(
    f"""
<div class="kpi-container">
    <div class="kpi-card">
        <div class="kpi-icon">🎮</div>
        <div class="kpi-value">{total_games:,}</div>
        <div class="kpi-label">Games Analyzed</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon">⚔️</div>
        <div class="kpi-value">{avg_turns:.0f}</div>
        <div class="kpi-label">Avg Turns / Game</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon">📊</div>
        <div class="kpi-value">{avg_rating_diff:.0f}</div>
        <div class="kpi-label">Avg Rating Gap</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon">🏁</div>
        <div class="kpi-value">{mate_pct:.1f}%</div>
        <div class="kpi-label">End in Checkmate</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon">🏳️</div>
        <div class="kpi-value">{resign_pct:.1f}%</div>
        <div class="kpi-label">End in Resign</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon">⚪</div>
        <div class="kpi-value">{white_adv:.1f}%</div>
        <div class="kpi-label">White Win Rate</div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

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

    st.markdown("---")
    st.markdown("### 📊 Task 2 Options")
    show_draws_task2 = st.checkbox("Include Draws", value=True, help="Show draw counts")
    show_net_advantage = st.checkbox(
        "Show Net Advantage", value=True, help="Overlay net white advantage"
    )

    st.markdown("---")
    st.markdown("### 🫧 Task 3 Options")
    top_n_openings = st.slider(
        "Number of Openings",
        min_value=5,
        max_value=15,
        value=12,
        help="How many openings to display",
    )
    show_draw_rates = st.checkbox(
        "Show Draw Rates", value=False, help="Overlay draw rates on the chart"
    )

    st.markdown("---")
    st.markdown("### 🎻 Task 4 Options")
    ply_chart_type = st.radio(
        "Chart Style",
        options=["Violin", "Box"],
        index=0,
        help="Choose between violin or box plot",
        horizontal=True,
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
    st.markdown("### ⏱️ Task 6 Options")
    time_chart_mode = st.radio(
        "Chart Mode",
        options=["Stacked Bar", "Heatmap"],
        index=0,
        help="How to display time control vs outcome",
        horizontal=True,
    )

    st.markdown("---")
    st.markdown(
        """
    <div style="text-align:center; color:#484f58; font-size:0.75rem; margin-top:1rem;">
        Built with Streamlit & Plotly<br/>
        Data: Lichess Open Database
    </div>
    """,
        unsafe_allow_html=True,
    )

# -----------------------------------------------
# Task 1: Scatterplot - rating diff vs game length
# -----------------------------------------------
st.markdown(
    '<div class="section-header"><span class="num">01</span> Rating Gap vs. Game Length</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-desc">Looking at whether a bigger skill gap between players leads to shorter games. The scatter plot maps rating difference against the number of turns, coloured by how each game ended.</div>',
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

tab1a, tab1b, tab1c = st.tabs(
    ["🔬 Scatter Plot", "🌡️ Heatmap Density", "📈 Distribution"]
)

with tab1a:
    fig1 = px.scatter(
        filtered_scatter,
        x="rating_diff",
        y="turns",
        color="victory_status",
        opacity=0.4,
        title="Game Length vs. Skill Gap",
        labels={
            "rating_diff": "Rating Differential (White − Black)",
            "turns": "Number of Turns",
            "victory_status": "Victory Reason",
        },
        color_discrete_map=VICTORY_COLORS,
    )
    fig1.update_traces(marker=dict(size=4, line=dict(width=0)))
    fig1.update_layout(**PLOTLY_LAYOUT)
    fig1.update_layout(
        xaxis=dict(
            gridcolor="rgba(99,102,241,0.07)",
            zeroline=True,
            zerolinecolor="rgba(255,255,255,0.15)",
            zerolinewidth=1,
        ),
        yaxis=dict(gridcolor="rgba(99,102,241,0.07)"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    # highlight the zone where players are roughly equal
    fig1.add_vrect(
        x0=-50,
        x1=50,
        fillcolor="rgba(99,102,241,0.04)",
        layer="below",
        line_width=0,
        annotation_text="Evenly Matched",
        annotation_position="top",
        annotation_font=dict(size=10, color="#6366f1"),
    )
    st.plotly_chart(fig1, use_container_width=True)

with tab1b:
    fig1_heat = go.Figure()
    fig1_heat.add_trace(
        go.Histogram2d(
            x=filtered_scatter["rating_diff"],
            y=filtered_scatter["turns"],
            colorscale=[
                [0, "rgba(13,17,23,1)"],
                [0.1, "#1e1b4b"],
                [0.3, "#4338ca"],
                [0.5, "#6366f1"],
                [0.7, "#a78bfa"],
                [0.9, "#c084fc"],
                [1, "#f0abfc"],
            ],
            nbinsx=80,
            nbinsy=60,
            colorbar=dict(title="Count", tickfont=dict(color="#8b949e")),
            hovertemplate="Rating Diff: %{x}<br>Turns: %{y}<br>Count: %{z}<extra></extra>",
        )
    )
    fig1_heat.update_layout(**PLOTLY_LAYOUT)
    fig1_heat.update_layout(
        title="Density Heatmap of Games",
        xaxis_title="Rating Differential (White − Black)",
        yaxis_title="Number of Turns",
        xaxis=dict(gridcolor="rgba(99,102,241,0.05)"),
        yaxis=dict(gridcolor="rgba(99,102,241,0.05)"),
    )
    st.plotly_chart(fig1_heat, use_container_width=True)

with tab1c:
    # show distributions of turns and rating diff side by side
    fig1_dist = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=("Turns Distribution by Outcome", "Rating Diff Distribution"),
        horizontal_spacing=0.08,
    )
    for vs in sorted(filtered_scatter["victory_status"].unique()):
        subset = filtered_scatter[filtered_scatter["victory_status"] == vs]
        color = VICTORY_COLORS.get(vs, "#6366f1")
        fig1_dist.add_trace(
            go.Violin(
                y=subset["turns"],
                name=vs.title(),
                line_color=color,
                fillcolor=color,
                opacity=0.6,
                meanline_visible=True,
                box_visible=True,
                showlegend=True,
            ),
            row=1,
            col=1,
        )
    fig1_dist.add_trace(
        go.Histogram(
            x=filtered_scatter["rating_diff"],
            nbinsx=80,
            marker_color="#6366f1",
            opacity=0.7,
            name="Rating Diff",
            showlegend=False,
            hovertemplate="Rating Diff: %{x}<br>Count: %{y}<extra></extra>",
        ),
        row=1,
        col=2,
    )
    fig1_dist.update_layout(**PLOTLY_LAYOUT)
    fig1_dist.update_layout(
        title="Distribution Breakdown",
        height=450,
        showlegend=True,
        legend=dict(
            orientation="h", yanchor="bottom", y=1.08, xanchor="center", x=0.25
        ),
    )
    fig1_dist.update_yaxes(
        title_text="Turns", row=1, col=1, gridcolor="rgba(99,102,241,0.07)"
    )
    fig1_dist.update_yaxes(
        title_text="Count", row=1, col=2, gridcolor="rgba(99,102,241,0.07)"
    )
    fig1_dist.update_xaxes(gridcolor="rgba(99,102,241,0.07)", row=1, col=1)
    fig1_dist.update_xaxes(
        title_text="Rating Diff",
        gridcolor="rgba(99,102,241,0.07)",
        row=1,
        col=2,
    )
    st.plotly_chart(fig1_dist, use_container_width=True)

# quick stats for the insight box
mate_games = filtered_scatter[filtered_scatter["victory_status"] == "mate"]
resign_games = filtered_scatter[filtered_scatter["victory_status"] == "resign"]
avg_mate_turns = mate_games["turns"].mean() if len(mate_games) > 0 else 0
avg_resign_turns = resign_games["turns"].mean() if len(resign_games) > 0 else 0

st.markdown(
    f"""<div class="insight-box">
    💡 <strong>Observation:</strong> Checkmates take about <strong>{avg_mate_turns:.0f} turns</strong> on average,
    while resignations average <strong>{avg_resign_turns:.0f} turns</strong>. Players tend to resign before
    the actual mate happens, especially in mismatched games. You can also see how games with big rating
    gaps cluster towards shorter turn counts in the corners of the plot.
</div>""",
    unsafe_allow_html=True,
)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# -----------------------------------------------
# Task 2: White vs Black wins by tier
# -----------------------------------------------
st.markdown(
    '<div class="section-header"><span class="num">02</span> White\'s First-Move Advantage</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-desc">Checking whether White really does win more often, and if the effect is the same across different skill levels.</div>',
    unsafe_allow_html=True,
)

tab2a, tab2b = st.tabs(["📊 Diverging Bar Chart", "🎯 Win Rate Comparison"])

tier_order = [
    "1. Novice (<1200)",
    "2. Intermediate (1200-1499)",
    "3. Advanced (1500-1799)",
    "4. Master (1800+)",
]

with tab2a:
    fig2 = go.Figure()

    for tier in tier_order:
        tier_data = df_tiers[df_tiers["rating_tier"] == tier]
        white_count = tier_data[tier_data["winner"] == "white"]["game_count"].values
        black_count = tier_data[tier_data["winner"] == "black"]["game_count"].values
        draw_count = tier_data[tier_data["winner"] == "draw"]["game_count"].values
        wc = int(white_count[0]) if len(white_count) > 0 else 0
        bc = int(black_count[0]) if len(black_count) > 0 else 0
        dc = int(draw_count[0]) if len(draw_count) > 0 else 0

        friendly = tier.split(". ")[1] if ". " in tier else tier

        # white wins go to the right (positive)
        fig2.add_trace(
            go.Bar(
                y=[friendly],
                x=[wc],
                orientation="h",
                name="White Wins" if tier == tier_order[0] else None,
                marker=dict(
                    color="#f0d9b5",
                    line=dict(color="#dfc198", width=1.5),
                ),
                text=[f"⚪ {wc:,}"],
                textposition="inside",
                textfont=dict(color="#1a1207", size=12, family="JetBrains Mono"),
                hovertemplate=f"<b>{friendly}</b><br>White Wins: {wc:,}<extra></extra>",
                showlegend=(tier == tier_order[0]),
                legendgroup="white",
            )
        )

        # black wins go to the left (negative)
        fig2.add_trace(
            go.Bar(
                y=[friendly],
                x=[-bc],
                orientation="h",
                name="Black Wins" if tier == tier_order[0] else None,
                marker=dict(
                    color="#6366f1",
                    line=dict(color="#818cf8", width=1),
                ),
                text=[f"⚫ {bc:,}"],
                textposition="inside",
                textfont=dict(color="#e6edf3", size=12, family="JetBrains Mono"),
                hovertemplate=f"<b>{friendly}</b><br>Black Wins: {bc:,}<extra></extra>",
                showlegend=(tier == tier_order[0]),
                legendgroup="black",
            )
        )

    # add clean right-side annotations for net advantage and draws
    for tier in tier_order:
        tier_data = df_tiers[df_tiers["rating_tier"] == tier]
        white_count = tier_data[tier_data["winner"] == "white"]["game_count"].values
        black_count = tier_data[tier_data["winner"] == "black"]["game_count"].values
        draw_count = tier_data[tier_data["winner"] == "draw"]["game_count"].values
        wc = int(white_count[0]) if len(white_count) > 0 else 0
        bc = int(black_count[0]) if len(black_count) > 0 else 0
        dc = int(draw_count[0]) if len(draw_count) > 0 else 0
        net = wc - bc
        friendly = tier.split(". ")[1] if ". " in tier else tier
        total = wc + bc
        pct = (wc / total * 100) if total > 0 else 50
        sign = "+" if net > 0 else ""

        if show_net_advantage:
            fig2.add_annotation(
                xref="paper",
                x=1.01,
                y=friendly,
                text=f"<b>{pct:.1f}%</b> W ({sign}{net})",
                showarrow=False,
                xanchor="left",
                yshift=8 if show_draws_task2 else 0,
                font=dict(
                    size=11,
                    color="#22c55e" if net > 0 else "#ef4444",
                    family="JetBrains Mono",
                ),
            )

        if show_draws_task2 and dc > 0:
            fig2.add_annotation(
                xref="paper",
                x=1.01,
                y=friendly,
                text=f"½ {dc:,} draws",
                showarrow=False,
                xanchor="left",
                yshift=-8 if show_net_advantage else 0,
                font=dict(
                    size=10,
                    color="#f59e0b",
                    family="JetBrains Mono",
                ),
            )

    fig2.update_layout(**PLOTLY_LAYOUT)
    fig2.update_layout(
        barmode="relative",
        title="White vs. Black Wins by Skill Tier",
        xaxis=dict(
            title="← Black Wins  |  White Wins →",
            gridcolor="rgba(99,102,241,0.07)",
            zeroline=True,
            zerolinecolor="rgba(255,255,255,0.2)",
            zerolinewidth=2,
        ),
        yaxis=dict(
            title="",
            categoryorder="array",
            categoryarray=[t.split(". ")[1] for t in tier_order],
        ),
        height=420,
        margin=dict(t=60, b=50, l=60, r=160),
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5),
    )
    st.plotly_chart(fig2, use_container_width=True)

with tab2b:
    # dumbbell chart comparing white vs black win rates
    fig2b = go.Figure()

    for i, tier in enumerate(tier_order):
        tier_data = df_tiers[df_tiers["rating_tier"] == tier]
        white_count = tier_data[tier_data["winner"] == "white"]["game_count"].values
        black_count = tier_data[tier_data["winner"] == "black"]["game_count"].values
        draw_count = tier_data[tier_data["winner"] == "draw"]["game_count"].values
        wc = int(white_count[0]) if len(white_count) > 0 else 0
        bc = int(black_count[0]) if len(black_count) > 0 else 0
        dc = int(draw_count[0]) if len(draw_count) > 0 else 0
        total = wc + bc + dc
        w_pct = wc / total * 100
        b_pct = bc / total * 100
        d_pct = dc / total * 100
        friendly = tier.split(". ")[1] if ". " in tier else tier

        # connecting line between the two dots
        fig2b.add_trace(
            go.Scatter(
                x=[b_pct, w_pct],
                y=[friendly, friendly],
                mode="lines",
                line=dict(color="rgba(99,102,241,0.4)", width=3),
                showlegend=False,
                hoverinfo="skip",
            )
        )

        # white dot
        fig2b.add_trace(
            go.Scatter(
                x=[w_pct],
                y=[friendly],
                mode="markers+text",
                marker=dict(
                    size=18, color="#f0d9b5", line=dict(color="#dfc198", width=2)
                ),
                text=[f"{w_pct:.1f}%"],
                textposition="top center",
                textfont=dict(color="#f0d9b5", size=11, family="JetBrains Mono"),
                name="White Win %" if i == 0 else None,
                showlegend=(i == 0),
                legendgroup="white_pct",
                hovertemplate=f"<b>{friendly}</b><br>White: {w_pct:.1f}%<extra></extra>",
            )
        )

        # black dot
        fig2b.add_trace(
            go.Scatter(
                x=[b_pct],
                y=[friendly],
                mode="markers+text",
                marker=dict(
                    size=18, color="#6366f1", line=dict(color="#818cf8", width=2)
                ),
                text=[f"{b_pct:.1f}%"],
                textposition="bottom center",
                textfont=dict(color="#a78bfa", size=11, family="JetBrains Mono"),
                name="Black Win %" if i == 0 else None,
                showlegend=(i == 0),
                legendgroup="black_pct",
                hovertemplate=f"<b>{friendly}</b><br>Black: {b_pct:.1f}%<extra></extra>",
            )
        )

    # 50% reference line
    fig2b.add_vline(
        x=50,
        line_width=1,
        line_dash="dot",
        line_color="rgba(255,255,255,0.15)",
        annotation_text="50%",
        annotation_font=dict(color="#484f58", size=10),
    )

    fig2b.update_layout(**PLOTLY_LAYOUT)
    fig2b.update_layout(
        title="Dumbbell Chart: White vs. Black Win Rate by Tier",
        xaxis=dict(
            title="Win Rate (%)",
            range=[25, 65],
            gridcolor="rgba(99,102,241,0.07)",
        ),
        yaxis=dict(
            title="",
            categoryorder="array",
            categoryarray=[t.split(". ")[1] for t in tier_order],
        ),
        height=420,
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5),
    )
    st.plotly_chart(fig2b, use_container_width=True)

# compute which tier has biggest/smallest white advantage
tier_advantages = []
for tier in tier_order:
    td = df_tiers[df_tiers["rating_tier"] == tier]
    wc = td[td["winner"] == "white"]["game_count"].values
    bc = td[td["winner"] == "black"]["game_count"].values
    w = int(wc[0]) if len(wc) > 0 else 0
    b = int(bc[0]) if len(bc) > 0 else 0
    total = w + b
    tier_advantages.append((tier.split(". ")[1], w / total * 100 if total > 0 else 50))

max_adv_tier = max(tier_advantages, key=lambda x: x[1])
min_adv_tier = min(tier_advantages, key=lambda x: x[1])

st.markdown(
    f"""<div class="insight-box">
    💡 <strong>Observation:</strong> White does win more often across all tiers. The biggest edge is at the
    <strong>{max_adv_tier[0]}</strong> level ({max_adv_tier[1]:.1f}% white win rate), while
    <strong>{min_adv_tier[0]}</strong> has the smallest gap ({min_adv_tier[1]:.1f}%).
    So the first-move advantage seems pretty consistent regardless of skill level.
</div>""",
    unsafe_allow_html=True,
)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# -----------------------------------------------
# Task 3: Opening analysis
# -----------------------------------------------
st.markdown(
    '<div class="section-header"><span class="num">03</span> Opening Popularity vs. Win Rate</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-desc">Comparing how popular each opening is against how well White actually does with it. Bubble size shows how many games used that opening. The red dashed line at 50% marks the break-even point.</div>',
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
df_ops_top = df_ops.head(top_n_openings).sort_values("total_games", ascending=True)

tab3a, tab3b = st.tabs(["🫧 Bubble Chart", "⚖️ Win Rate Breakdown"])

with tab3a:
    fig3 = go.Figure()

    fig3.add_trace(
        go.Scatter(
            x=df_ops_top["white_wr"],
            y=df_ops_top["opening"],
            mode="markers+text",
            marker=dict(
                size=df_ops_top["total_games"] / df_ops_top["total_games"].max() * 50
                + 10,
                color=df_ops_top["white_wr"],
                colorscale=[
                    [0, "#ef4444"],
                    [0.35, "#f97316"],
                    [0.5, "#eab308"],
                    [0.65, "#22d3ee"],
                    [1, "#22c55e"],
                ],
                cmin=df_ops_top["white_wr"].min() - 2,
                cmax=df_ops_top["white_wr"].max() + 2,
                colorbar=dict(
                    title=dict(text="White WR%", font=dict(size=11, color="#8b949e")),
                    tickfont=dict(color="#8b949e"),
                    thickness=12,
                    len=0.6,
                ),
                line=dict(color="rgba(255,255,255,0.15)", width=1),
            ),
            text=[f" {wr:.1f}%" for wr in df_ops_top["white_wr"]],
            textposition="middle right",
            textfont=dict(color="#c9d1d9", size=10, family="JetBrains Mono"),
            hovertemplate="<b>%{y}</b><br>White WR: %{x:.1f}%<br>Games: %{customdata:,}<extra></extra>",
            customdata=df_ops_top["total_games"],
        )
    )

    if show_draw_rates:
        for _, row in df_ops_top.iterrows():
            fig3.add_annotation(
                x=row["white_wr"],
                y=row["opening"],
                text=f"½ {row['draw_rate']:.1f}%",
                showarrow=False,
                xanchor="left",
                xshift=35,
                font=dict(color="#f59e0b", size=9, family="JetBrains Mono"),
            )

    # 50% line
    fig3.add_vline(
        x=50,
        line_width=2,
        line_dash="dash",
        line_color="#ef4444",
        annotation_text="50% - Neutral",
        annotation_position="top right",
        annotation_font=dict(size=10, color="#ef4444"),
    )

    # shade the "favours white" and "favours black" zones
    fig3.add_vrect(
        x0=50,
        x1=df_ops_top["white_wr"].max() + 5,
        fillcolor="rgba(34,197,94,0.03)",
        layer="below",
        line_width=0,
    )
    fig3.add_vrect(
        x0=df_ops_top["white_wr"].min() - 5,
        x1=50,
        fillcolor="rgba(239,68,68,0.03)",
        layer="below",
        line_width=0,
    )

    fig3.update_layout(**PLOTLY_LAYOUT)
    fig3.update_layout(
        title="White Win Rate by Opening (bubble size = popularity)",
        xaxis=dict(
            title="White Win Rate (%)",
            gridcolor="rgba(99,102,241,0.07)",
            range=[
                df_ops_top["white_wr"].min() - 5,
                df_ops_top["white_wr"].max() + 10,
            ],
        ),
        yaxis=dict(title="", gridcolor="rgba(99,102,241,0.04)"),
        height=500,
    )
    st.plotly_chart(fig3, use_container_width=True)

with tab3b:
    # stacked bar showing white/draw/black split for each opening
    fig3b = go.Figure()

    fig3b.add_trace(
        go.Bar(
            y=df_ops_top["opening"],
            x=df_ops_top["white_wr"],
            orientation="h",
            name="White Win %",
            marker=dict(color="#f0d9b5", line=dict(color="#dfc198", width=0.5)),
            text=[f"{v:.1f}%" for v in df_ops_top["white_wr"]],
            textposition="inside",
            textfont=dict(color="#1a1207", size=10, family="JetBrains Mono"),
            hovertemplate="White: %{x:.1f}%<extra></extra>",
        )
    )

    fig3b.add_trace(
        go.Bar(
            y=df_ops_top["opening"],
            x=df_ops_top["draw_rate"],
            orientation="h",
            name="Draw %",
            marker=dict(color="#f59e0b", line=dict(color="#fbbf24", width=0.5)),
            text=[f"{v:.1f}%" for v in df_ops_top["draw_rate"]],
            textposition="inside",
            textfont=dict(color="#0d1117", size=10, family="JetBrains Mono"),
            hovertemplate="Draw: %{x:.1f}%<extra></extra>",
        )
    )

    fig3b.add_trace(
        go.Bar(
            y=df_ops_top["opening"],
            x=df_ops_top["black_wr"],
            orientation="h",
            name="Black Win %",
            marker=dict(color="#6366f1", line=dict(color="#818cf8", width=0.5)),
            text=[f"{v:.1f}%" for v in df_ops_top["black_wr"]],
            textposition="inside",
            textfont=dict(color="#e6edf3", size=10, family="JetBrains Mono"),
            hovertemplate="Black: %{x:.1f}%<extra></extra>",
        )
    )

    fig3b.update_layout(**PLOTLY_LAYOUT)
    fig3b.update_layout(
        barmode="stack",
        title="Full Win/Draw/Loss Breakdown by Opening",
        xaxis=dict(
            title="Percentage",
            gridcolor="rgba(99,102,241,0.07)",
            range=[0, 100],
        ),
        yaxis=dict(title=""),
        height=500,
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5),
    )
    st.plotly_chart(fig3b, use_container_width=True)

# find the best/worst/most popular openings for the insight
best_opening = df_ops_top.loc[df_ops_top["white_wr"].idxmax()]
worst_opening = df_ops_top.loc[df_ops_top["white_wr"].idxmin()]
most_popular = df_ops_top.loc[df_ops_top["total_games"].idxmax()]
highest_draw = df_ops_top.loc[df_ops_top["draw_rate"].idxmax()]

st.markdown(
    f"""<div class="insight-box">
    💡 <strong>Observation:</strong> White does best with <strong>{best_opening["opening"]}</strong>
    ({best_opening["white_wr"]:.1f}% win rate), and worst with <strong>{worst_opening["opening"]}</strong>
    ({worst_opening["white_wr"]:.1f}%). The most played opening is
    <strong>{most_popular["opening"]}</strong> ({most_popular["total_games"]} games), which isn't the same as the
    most effective one. <strong>{highest_draw["opening"]}</strong> leads to the most draws at {highest_draw["draw_rate"]:.1f}%.
</div>""",
    unsafe_allow_html=True,
)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# -----------------------------------------------
# Task 4: Opening theory depth (ply) by tier
# -----------------------------------------------
st.markdown(
    '<div class="section-header"><span class="num">04</span> Opening Theory Depth by Skill Tier</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-desc">Opening ply measures how many moves into the game a known book line was followed. This chart compares that depth across the four skill tiers to see if stronger players use more theory.</div>',
    unsafe_allow_html=True,
)

tier_order_labels = {
    "1. Novice (<1200)": "Novice (<1200)",
    "2. Intermediate (1200-1499)": "Intermediate (1200-1499)",
    "3. Advanced (1500-1799)": "Advanced (1500-1799)",
    "4. Master (1800+)": "Master (1800+)",
}
df_ply["tier_label"] = df_ply["rating_tier"].map(tier_order_labels)
tier_label_order = list(tier_order_labels.values())

tier_colors_map = {
    "Novice (<1200)": "#22d3ee",
    "Intermediate (1200-1499)": "#6366f1",
    "Advanced (1500-1799)": "#a78bfa",
    "Master (1800+)": "#c084fc",
}

fig4 = go.Figure()

for tier_label in tier_label_order:
    subset = df_ply[df_ply["tier_label"] == tier_label]["opening_ply"]
    color = tier_colors_map[tier_label]

    if ply_chart_type == "Violin":
        fig4.add_trace(
            go.Violin(
                y=subset,
                name=tier_label,
                line_color=color,
                fillcolor=color,
                opacity=0.6,
                meanline_visible=True,
                box_visible=True,
                points=False,
                scalemode="width",
                hoverinfo="y+name",
            )
        )
    else:
        fig4.add_trace(
            go.Box(
                y=subset,
                name=tier_label,
                marker_color=color,
                line_color=color,
                fillcolor=f"rgba({int(color[1:3], 16)},{int(color[3:5], 16)},{int(color[5:7], 16)},0.3)",
                boxmean="sd",
                hoverinfo="y+name",
            )
        )

fig4.update_layout(**PLOTLY_LAYOUT)
fig4.update_layout(
    title=f"Opening Ply Distribution by Skill Tier ({ply_chart_type} Plot)",
    yaxis=dict(
        title="Opening Ply (Book Depth)",
        gridcolor="rgba(99,102,241,0.07)",
    ),
    xaxis=dict(title=""),
    height=480,
    showlegend=False,
)
st.plotly_chart(fig4, use_container_width=True)

# grab the tier with the deepest/shallowest average theory
ply_means = df_ply.groupby("tier_label")["opening_ply"].mean()
deepest_tier = ply_means.idxmax()
shallowest_tier = ply_means.idxmin()

st.markdown(
    f"""<div class="insight-box">
    💡 <strong>Observation:</strong> <strong>{deepest_tier}</strong> players use the deepest opening theory on
    average ({ply_means[deepest_tier]:.1f} ply), while <strong>{shallowest_tier}</strong> players go the
    shallowest ({ply_means[shallowest_tier]:.1f} ply). Higher-rated players also have a wider spread,
    meaning they sometimes go very deep into prep but also sometimes play uncommon lines early.
</div>""",
    unsafe_allow_html=True,
)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# -----------------------------------------------
# Task 5: Upsets - lower rated player winning
# -----------------------------------------------
st.markdown(
    '<div class="section-header"><span class="num">05</span> Upset Frequency</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-desc">How often does the lower-rated player actually win? This section bins games by rating gap and tracks how the upset rate changes as the gap gets bigger.</div>',
    unsafe_allow_html=True,
)

tab5a, tab5b = st.tabs(["📉 Upset Rate Curve", "📊 Volume Breakdown"])

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

with tab5a:
    fig5a = make_subplots(specs=[[{"secondary_y": True}]])

    # upset rate line
    fig5a.add_trace(
        go.Scatter(
            x=upset_by_bin["gap_bin"],
            y=upset_by_bin["upset_rate"],
            mode="lines+markers",
            name="Upset Rate %",
            line=dict(color="#ef4444", width=3),
            marker=dict(size=7, color="#ef4444", line=dict(color="#fca5a5", width=1)),
            fill="tozeroy",
            fillcolor="rgba(239,68,68,0.08)",
            hovertemplate="Gap: %{x}<br>Upset Rate: %{y:.1f}%<extra></extra>",
        ),
        secondary_y=False,
    )

    # volume bars in background
    fig5a.add_trace(
        go.Bar(
            x=upset_by_bin["gap_bin"],
            y=upset_by_bin["total"],
            name="Games in Bin",
            marker=dict(
                color="rgba(99,102,241,0.2)",
                line=dict(color="rgba(99,102,241,0.4)", width=1),
            ),
            hovertemplate="Gap: %{x}<br>Games: %{y:,}<extra></extra>",
        ),
        secondary_y=True,
    )

    # 50% reference
    fig5a.add_hline(
        y=50,
        line_width=1,
        line_dash="dot",
        line_color="rgba(255,255,255,0.15)",
        annotation_text="50% (coin flip)",
        annotation_font=dict(color="#484f58", size=10),
        secondary_y=False,
    )

    fig5a.update_layout(**PLOTLY_LAYOUT)
    fig5a.update_layout(
        title="Upset Probability vs. Rating Gap",
        height=450,
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5),
    )
    fig5a.update_xaxes(
        title_text=f"Rating Gap (binned by {gap_bin_size})",
        gridcolor="rgba(99,102,241,0.07)",
    )
    fig5a.update_yaxes(
        title_text="Upset Rate (%)",
        gridcolor="rgba(99,102,241,0.07)",
        range=[0, 60],
        secondary_y=False,
    )
    fig5a.update_yaxes(
        title_text="Number of Games",
        gridcolor="rgba(99,102,241,0.04)",
        showgrid=False,
        secondary_y=True,
    )
    st.plotly_chart(fig5a, use_container_width=True)

with tab5b:
    fig5b = go.Figure()
    fig5b.add_trace(
        go.Bar(
            x=upset_by_bin["gap_bin"],
            y=upset_by_bin["upsets"],
            name="Upsets (Lower Rated Won)",
            marker=dict(color="#ef4444", line=dict(color="#fca5a5", width=0.5)),
            hovertemplate="Gap: %{x}<br>Upsets: %{y:,}<extra></extra>",
        )
    )
    fig5b.add_trace(
        go.Bar(
            x=upset_by_bin["gap_bin"],
            y=upset_by_bin["total"] - upset_by_bin["upsets"],
            name="Expected (Higher Rated Won)",
            marker=dict(color="#6366f1", line=dict(color="#818cf8", width=0.5)),
            hovertemplate="Gap: %{x}<br>Expected: %{y:,}<extra></extra>",
        )
    )
    fig5b.update_layout(**PLOTLY_LAYOUT)
    fig5b.update_layout(
        barmode="stack",
        title="Upset vs. Expected Outcome Volume by Rating Gap",
        xaxis=dict(
            title=f"Rating Gap (binned by {gap_bin_size})",
            gridcolor="rgba(99,102,241,0.07)",
        ),
        yaxis=dict(title="Number of Games", gridcolor="rgba(99,102,241,0.07)"),
        height=450,
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5),
    )
    st.plotly_chart(fig5b, use_container_width=True)

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
    💡 <strong>Observation:</strong> Overall, <strong>{overall_upset_pct:.1f}%</strong> of decisive games are upsets.
    When players are close in rating (gap of 50 or less), it's basically a coin flip at <strong>{close_upset_pct:.1f}%</strong>.
    But once the gap hits 400+, upsets only happen <strong>{big_gap_upset_pct:.1f}%</strong> of the time, so
    rating is a pretty good predictor at that point.
</div>""",
    unsafe_allow_html=True,
)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# -----------------------------------------------
# Task 6: Time control vs how games end
# -----------------------------------------------
st.markdown(
    '<div class="section-header"><span class="num">06</span> Time Control vs. Game Outcome</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-desc">Different time controls lead to very different game endings. Faster formats like bullet have way more timeouts, while longer games tend to end in checkmate or resignation more often.</div>',
    unsafe_allow_html=True,
)


# classify time controls using the lichess formula (base + 40*increment)
def classify_time_control(tc_string):
    try:
        parts = tc_string.split("+")
        base_sec = int(parts[0]) * 60
        inc_sec = int(parts[1]) if len(parts) > 1 else 0
        estimated = base_sec + 40 * inc_sec
        if estimated < 180:
            return "Bullet (<3m)"
        elif estimated < 480:
            return "Blitz (3-8m)"
        elif estimated < 1500:
            return "Rapid (8-25m)"
        else:
            return "Classical (25m+)"
    except (ValueError, IndexError):
        return "Other"


df_time["tc_category"] = df_time["time_increment"].apply(classify_time_control)

tc_order = ["Bullet (<3m)", "Blitz (3-8m)", "Rapid (8-25m)", "Classical (25m+)"]
vs_order = ["mate", "resign", "outoftime", "draw"]
vs_colors = {
    "mate": "#ef4444",
    "resign": "#f97316",
    "outoftime": "#22d3ee",
    "draw": "#a78bfa",
}

# aggregate counts by time control category
tc_agg = (
    df_time.groupby(["tc_category", "victory_status"])["game_count"].sum().reset_index()
)

# percentages within each category
tc_totals = tc_agg.groupby("tc_category")["game_count"].sum().reset_index()
tc_totals.columns = ["tc_category", "tc_total"]
tc_agg = tc_agg.merge(tc_totals, on="tc_category")
tc_agg["pct"] = tc_agg["game_count"] / tc_agg["tc_total"] * 100

if time_chart_mode == "Stacked Bar":
    fig6 = go.Figure()
    for vs in vs_order:
        sub = tc_agg[tc_agg["victory_status"] == vs]
        # make sure all categories are present even if 0
        sub = sub.set_index("tc_category").reindex(tc_order).fillna(0).reset_index()
        fig6.add_trace(
            go.Bar(
                x=sub["tc_category"],
                y=sub["pct"],
                name=vs.title(),
                marker=dict(
                    color=vs_colors[vs],
                    line=dict(color="rgba(255,255,255,0.1)", width=0.5),
                ),
                text=[f"{v:.1f}%" for v in sub["pct"]],
                textposition="inside",
                textfont=dict(
                    color="#e6edf3" if vs != "draw" else "#0d1117",
                    size=10,
                    family="JetBrains Mono",
                ),
                hovertemplate=f"<b>{vs.title()}</b><br>%{{x}}<br>%{{y:.1f}}%<extra></extra>",
            )
        )

    fig6.update_layout(**PLOTLY_LAYOUT)
    fig6.update_layout(
        barmode="stack",
        title="How Games End by Time Control",
        xaxis=dict(
            title="Time Control",
            categoryorder="array",
            categoryarray=tc_order,
        ),
        yaxis=dict(
            title="Percentage of Games (%)",
            gridcolor="rgba(99,102,241,0.07)",
            range=[0, 100],
        ),
        height=480,
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5),
    )
    st.plotly_chart(fig6, use_container_width=True)

else:
    # heatmap mode
    pivot = tc_agg.pivot_table(
        index="victory_status", columns="tc_category", values="pct", fill_value=0
    )
    pivot = pivot.reindex(index=vs_order, columns=tc_order, fill_value=0)

    fig6 = go.Figure(
        go.Heatmap(
            z=pivot.values,
            x=tc_order,
            y=[v.title() for v in vs_order],
            colorscale=[
                [0, "rgba(13,17,23,1)"],
                [0.2, "#1e1b4b"],
                [0.4, "#4338ca"],
                [0.6, "#6366f1"],
                [0.8, "#a78bfa"],
                [1, "#f0abfc"],
            ],
            text=[[f"{v:.1f}%" for v in row] for row in pivot.values],
            texttemplate="%{text}",
            textfont=dict(size=13, family="JetBrains Mono", color="#e6edf3"),
            colorbar=dict(
                title=dict(text="%", font=dict(size=11, color="#8b949e")),
                tickfont=dict(color="#8b949e"),
                thickness=12,
            ),
            hovertemplate="<b>%{y}</b> in <b>%{x}</b><br>%{z:.1f}% of games<extra></extra>",
        )
    )
    fig6.update_layout(**PLOTLY_LAYOUT)
    fig6.update_layout(
        title="Victory Status Heatmap by Time Control",
        xaxis=dict(title="Time Control"),
        yaxis=dict(title=""),
        height=380,
    )
    st.plotly_chart(fig6, use_container_width=True)

# pull some numbers for the insight
bullet_timeout = tc_agg[
    (tc_agg["tc_category"] == "Bullet (<3m)")
    & (tc_agg["victory_status"] == "outoftime")
]
classical_mate = tc_agg[
    (tc_agg["tc_category"] == "Classical (25m+)") & (tc_agg["victory_status"] == "mate")
]
bullet_to_pct = float(bullet_timeout["pct"].values[0]) if len(bullet_timeout) > 0 else 0
classical_m_pct = (
    float(classical_mate["pct"].values[0]) if len(classical_mate) > 0 else 0
)

st.markdown(
    f"""<div class="insight-box">
    💡 <strong>Observation:</strong> In Bullet games, <strong>{bullet_to_pct:.1f}%</strong> end on time,
    which makes sense given how little time players have. In Classical games, checkmates make up
    <strong>{classical_m_pct:.1f}%</strong> of results. Basically, the less time pressure there is,
    the more games are decided by actual chess rather than the clock.
</div>""",
    unsafe_allow_html=True,
)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# -----------------------------------------------
# Bonus: Radar chart for comparing openings
# -----------------------------------------------
st.markdown(
    '<div class="section-header"><span class="num">✦</span> Bonus: Opening Profiles</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-desc">A radar chart for comparing openings across a few different dimensions. Pick some openings and see how they stack up against each other.</div>',
    unsafe_allow_html=True,
)

# let the user pick which openings to compare
available_openings = df_ops.sort_values("total_games", ascending=False)[
    "opening"
].tolist()
selected_openings = st.multiselect(
    "Select openings to compare:",
    options=available_openings,
    default=available_openings[:3],
    max_selections=6,
)

if selected_openings:
    radar_colors = ["#6366f1", "#22c55e", "#f59e0b", "#ef4444", "#22d3ee", "#c084fc"]
    categories = ["White WR", "Black WR", "Draw Rate", "Popularity", "Decisiveness"]

    fig_radar = go.Figure()

    max_games = df_ops["total_games"].max()

    for i, opening in enumerate(selected_openings):
        row = df_ops[df_ops["opening"] == opening].iloc[0]
        # normalise popularity to 0-100 so it fits on the same scale
        popularity_norm = row["total_games"] / max_games * 100
        decisiveness = 100 - row["draw_rate"]

        values = [
            row["white_wr"],
            row["black_wr"],
            row["draw_rate"],
            popularity_norm,
            decisiveness,
        ]
        values.append(values[0])  # close the polygon
        cats = categories + [categories[0]]

        hex_color = radar_colors[i % len(radar_colors)]
        r_val = int(hex_color[1:3], 16)
        g_val = int(hex_color[3:5], 16)
        b_val = int(hex_color[5:7], 16)
        fill_rgba = f"rgba({r_val},{g_val},{b_val},0.1)"

        fig_radar.add_trace(
            go.Scatterpolar(
                r=values,
                theta=cats,
                fill="toself",
                name=opening,
                line=dict(color=hex_color, width=2),
                fillcolor=fill_rgba,
                marker=dict(size=6),
            )
        )

    fig_radar.update_layout(**PLOTLY_LAYOUT)
    fig_radar.update_layout(
        title="Opening Profile Comparison",
        polar=dict(
            bgcolor="rgba(13,17,23,0.6)",
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor="rgba(99,102,241,0.1)",
                tickfont=dict(size=9, color="#484f58"),
            ),
            angularaxis=dict(
                gridcolor="rgba(99,102,241,0.15)",
                tickfont=dict(size=12, color="#c9d1d9", family="Inter"),
            ),
        ),
        height=500,
        legend=dict(
            font=dict(size=11),
            bgcolor="rgba(22,27,34,0.8)",
            bordercolor="rgba(99,102,241,0.2)",
            borderwidth=1,
        ),
    )
    st.plotly_chart(fig_radar, use_container_width=True)

    st.markdown(
        """<div class="warning-box">
        ⚡ <strong>How to read this:</strong> Each axis is a different property of the opening.
        <b>White WR / Black WR</b> are the win percentages for each side. <b>Draw Rate</b> is how often
        the game ends in a draw. <b>Popularity</b> is scaled relative to the most-played opening.
        <b>Decisiveness</b> is just 100 minus the draw rate (higher = fewer draws).
    </div>""",
        unsafe_allow_html=True,
    )
else:
    st.info("☝️ Select at least one opening above to see the radar comparison.")

# -- footer --
st.markdown(
    """<div class="footer">
    ♟️ LICHESS INSIGHTS DASHBOARD · Built with Streamlit + Plotly · Data: Lichess Open Database (20k games) · Shane Whelan 2026
</div>""",
    unsafe_allow_html=True,
)
