"""
CSS styles and Plotly theme for bosssmuda dashboard.
"""
import streamlit as st


def inject_dashboard_css():
    """Inject the ultra-aesthetic dark theme CSS for the dashboard."""
    st.markdown("""
<style>
/* ====== GOOGLE FONTS ====== */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');

/* ====== ROOT VARIABLES ====== */
:root {
    --bg-primary: #0a0e1a;
    --bg-secondary: #111827;
    --bg-card: #1a1f36;
    --bg-card-hover: #222845;
    --accent-purple: #8b5cf6;
    --accent-pink: #ec4899;
    --accent-cyan: #06b6d4;
    --accent-emerald: #10b981;
    --accent-amber: #f59e0b;
    --accent-red: #ef4444;
    --text-primary: #f1f5f9;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
    --border-color: rgba(139, 92, 246, 0.15);
    --glow-purple: rgba(139, 92, 246, 0.4);
    --glow-cyan: rgba(6, 182, 212, 0.3);
    --gradient-main: linear-gradient(135deg, #8b5cf6, #ec4899, #06b6d4);
    --gradient-card: linear-gradient(145deg, rgba(139,92,246,0.08), rgba(6,182,212,0.05));
}

/* ====== GLOBAL ====== */
html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Inter', -apple-system, sans-serif !important;
    background: var(--bg-primary) !important;
    color: var(--text-primary) !important;
}

[data-testid="stAppViewContainer"] {
    background: var(--bg-primary) !important;
    background-image:
        radial-gradient(ellipse at 15% 10%, rgba(139,92,246,0.06) 0%, transparent 50%),
        radial-gradient(ellipse at 85% 20%, rgba(6,182,212,0.04) 0%, transparent 50%),
        radial-gradient(ellipse at 50% 80%, rgba(236,72,153,0.03) 0%, transparent 50%) !important;
}

/* ====== SIDEBAR ====== */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f1629 0%, #111827 50%, #0d1220 100%) !important;
    border-right: 1px solid var(--border-color) !important;
}

[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    color: var(--text-primary) !important;
}

[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] .stMarkdown label {
    color: var(--text-secondary) !important;
}

/* ====== TOP HEADER AREA ====== */
.top-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75rem 1.5rem;
    border-bottom: 1px solid var(--border-color);
    background: var(--bg-primary);
    margin-bottom: 1.5rem;
    margin-top: -3rem;
    border-radius: 12px;
}

.search-container {
    display: flex;
    align-items: center;
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 0.5rem 1rem;
    width: 400px;
    max-width: 100%;
}

.search-icon {
    font-size: 1.2rem;
    margin-right: 0.5rem;
}

.search-input {
    background: transparent;
    border: none;
    color: var(--text-primary);
    width: 100%;
    outline: none;
    font-size: 0.9rem;
    font-family: inherit;
}

.search-input::placeholder {
    color: var(--text-muted);
}

.header-actions {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.action-btn {
    background: transparent;
    border: none;
    cursor: pointer;
    font-size: 1.2rem;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s;
}

.notifications {
    position: relative;
}

.indicator {
    position: absolute;
    top: -2px;
    right: -2px;
    width: 8px;
    height: 8px;
    background: var(--accent-red);
    border-radius: 50%;
    border: 2px solid var(--bg-primary);
}

.v-divider {
    width: 1px;
    height: 32px;
    background: var(--border-color);
    margin: 0 0.5rem;
}

.user-profile {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.user-details {
    text-align: right;
}

.user-name {
    display: block;
    font-size: 0.85rem;
    font-weight: 700;
    color: var(--text-primary);
}

.user-role {
    display: block;
    font-size: 0.65rem;
    font-weight: 800;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.user-avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: rgba(139,92,246,0.2);
    border: 2px solid rgba(139,92,246,0.3);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
}

@media (max-width: 768px) {
    .hide-mobile, .search-container {
        display: none !important;
    }
}

/* ====== SIDEBAR RADIO NAV ====== */
[data-testid="stSidebar"] [data-testid="stRadio"] > div {
    gap: 0.25rem;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    padding: 0.75rem 1rem !important;
    border-radius: 8px !important;
    transition: all 0.2s !important;
    cursor: pointer !important;
    background: transparent !important;
    box-shadow: none !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: var(--bg-card) !important;
    color: var(--text-primary) !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label[data-checked="true"] {
    background: rgba(139,92,246,0.1) !important;
    border-left: 4px solid var(--accent-purple) !important;
    border-radius: 0 8px 8px 0 !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label[data-checked="true"] div[data-testid="stMarkdownContainer"] p {
    color: var(--accent-purple) !important;
    font-weight: 700 !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radio"] {
    display: none !important; /* Hide radio circles */
}

[data-testid="stSidebar"] [data-testid="stRadio"] label > div:nth-child(2) {
    margin-left: 0 !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] p {
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    color: var(--text-secondary) !important;
    margin: 0 !important;
}

/* ====== METRICS CARDS ====== */
.metric-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin: 1.5rem 0;
}

.metric-card {
    background: var(--gradient-card);
    backdrop-filter: blur(20px);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    padding: 1.4rem 1.5rem;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 3px;
    background: var(--gradient-main);
    opacity: 0;
    transition: opacity 0.3s ease;
}

.metric-card:hover {
    transform: translateY(-3px);
    border-color: rgba(139,92,246,0.3);
    box-shadow: 0 8px 30px rgba(139,92,246,0.15);
}

.metric-card:hover::before {
    opacity: 1;
}

.metric-icon {
    font-size: 1.8rem;
    margin-bottom: 0.5rem;
}

.metric-value {
    font-size: 1.8rem;
    font-weight: 800;
    color: var(--text-primary);
    font-family: 'JetBrains Mono', monospace;
    line-height: 1.2;
}

.metric-label {
    font-size: 0.78rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 1.2px;
    font-weight: 600;
    margin-top: 0.3rem;
}

/* ====== DATA TABLES ====== */
[data-testid="stDataFrame"] {
    border-radius: 12px !important;
    overflow: hidden !important;
    border: 1px solid var(--border-color) !important;
}

.stDataFrame [data-testid="StyledLinkIconContainer"] {
    color: var(--text-primary) !important;
}

/* ====== TABS ====== */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    gap: 0.5rem;
    background: transparent;
    border-bottom: 2px solid rgba(139,92,246,0.1);
    padding-bottom: 0;
}

[data-testid="stTabs"] [data-baseweb="tab"] {
    background: transparent !important;
    border: none !important;
    color: var(--text-muted) !important;
    font-weight: 600;
    font-size: 0.9rem;
    padding: 0.7rem 1.3rem;
    border-radius: 8px 8px 0 0;
    transition: all 0.25s ease;
}

[data-testid="stTabs"] [data-baseweb="tab"]:hover {
    color: var(--accent-purple) !important;
    background: rgba(139,92,246,0.08) !important;
}

[data-testid="stTabs"] [aria-selected="true"] {
    color: var(--accent-purple) !important;
    border-bottom: 3px solid var(--accent-purple) !important;
    background: rgba(139,92,246,0.06) !important;
}

/* ====== BUTTONS ====== */
.stButton > button {
    background: linear-gradient(135deg, var(--accent-purple), var(--accent-pink)) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 1.8rem !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.3px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 4px 15px rgba(139,92,246,0.3) !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(139,92,246,0.45) !important;
}

/* ====== SELECT / INPUT ====== */
[data-testid="stSelectbox"] > div > div,
[data-testid="stTextInput"] > div > div > input {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
}

[data-testid="stSelectbox"] > div > div:focus-within,
[data-testid="stTextInput"] > div > div:focus-within {
    border-color: var(--accent-purple) !important;
    box-shadow: 0 0 0 3px var(--glow-purple) !important;
}

/* ====== EXPANDER ====== */
[data-testid="stExpander"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 12px !important;
}

/* ====== DOWNLOAD BUTTON ====== */
.stDownloadButton > button {
    background: linear-gradient(135deg, var(--accent-emerald), var(--accent-cyan)) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 15px rgba(16,185,129,0.3) !important;
}

.stDownloadButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(16,185,129,0.45) !important;
}

/* ====== DIVIDER LINE ====== */
.gradient-divider {
    height: 2px;
    background: var(--gradient-main);
    border: none;
    border-radius: 1px;
    margin: 1.5rem 0;
    opacity: 0.5;
}

/* ====== SECTION TITLE ====== */
.section-title {
    font-size: 1.3rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* ====== INFO BOX ====== */
.info-box {
    background: var(--gradient-card);
    border: 1px solid var(--border-color);
    border-left: 4px solid var(--accent-purple);
    border-radius: 0 12px 12px 0;
    padding: 1rem 1.3rem;
    margin: 1rem 0;
    color: var(--text-secondary);
    font-size: 0.9rem;
    line-height: 1.6;
}

/* ====== ANIMATIONS ====== */
@keyframes fadeInDown {
    from { opacity: 0; transform: translateY(-20px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(15px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes pulseGlow {
    0%, 100% { box-shadow: 0 0 20px rgba(139,92,246,0.1); }
    50% { box-shadow: 0 0 30px rgba(139,92,246,0.25); }
}

/* ====== SCROLLBAR ====== */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--accent-purple); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent-pink); }

/* ====== HIDE STREAMLIT DEFAULTS ====== */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ====== PLOTLY CHART CONTAINERS ====== */
.js-plotly-plot { border-radius: 12px !important; overflow: hidden; }
</style>
""", unsafe_allow_html=True)


# =============================================
# PLOTLY THEME
# =============================================
PLOTLY_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(26,31,54,0.6)',
    font=dict(family="Inter, sans-serif", color="#f1f5f9", size=12),
    margin=dict(l=40, r=20, t=50, b=40),
    xaxis=dict(gridcolor='rgba(148,163,184,0.08)', zerolinecolor='rgba(148,163,184,0.08)'),
    yaxis=dict(gridcolor='rgba(148,163,184,0.08)', zerolinecolor='rgba(148,163,184,0.08)'),
    hoverlabel=dict(
        bgcolor="#1a1f36",
        font_size=12,
        font_family="Inter, sans-serif",
        font_color="#f1f5f9",
        bordercolor="#8b5cf6"
    ),
    legend=dict(
        bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94a3b8', size=11)
    )
)

COLOR_SEQUENCE = [
    '#8b5cf6', '#ec4899', '#06b6d4', '#10b981', '#f59e0b',
    '#ef4444', '#3b82f6', '#a78bfa', '#f472b6', '#22d3ee',
    '#34d399', '#fbbf24', '#f87171', '#60a5fa', '#c084fc'
]
