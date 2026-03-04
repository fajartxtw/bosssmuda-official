"""
🚀 bosssmuda — Dashboard Kepemilikan Saham IDX
================================================
Jalankan: streamlit run app_streamlit.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import sys
import tempfile

# =============================================
# KONFIGURASI HALAMAN
# =============================================
st.set_page_config(
    page_title="bosssmuda | Kepemilikan Saham IDX",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================
# AUTHENTICATION MIDDLEWARE
# =============================================

def _get_credentials():
    """Ambil kredensial dari secrets.toml atau fallback default."""
    try:
        return dict(st.secrets["passwords"])
    except Exception:
        # Fallback jika secrets.toml tidak tersedia (development lokal)
        return {"admin": "admin123", "demo": "demo123"}


def _check_login(username, password):
    """Verifikasi username dan password."""
    credentials = _get_credentials()
    if username in credentials and credentials[username] == password:
        return True
    return False


def _show_login_page():
    """Tampilkan halaman login dengan UI estetik."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    [data-testid="stAppViewContainer"] {
        background: #0a0e1a !important;
        background-image:
            radial-gradient(ellipse at 30% 20%, rgba(139,92,246,0.08) 0%, transparent 50%),
            radial-gradient(ellipse at 70% 60%, rgba(6,182,212,0.06) 0%, transparent 50%),
            radial-gradient(ellipse at 50% 90%, rgba(236,72,153,0.04) 0%, transparent 50%) !important;
    }

    #MainMenu, footer, header { visibility: hidden; }
    .stDeployButton { display: none; }
    [data-testid="stSidebar"] { display: none !important; }

    .login-container {
        max-width: 340px;
        margin: 8vh auto;
        padding: 2.5rem 2rem;
        background: #0a0e1a; /* Solid background instead of glass */
        border: 1px solid rgba(139,92,246,0.3);
        border-radius: 16px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.5); /* Simpler shadow */
    }

    .login-header {
        text-align: center;
        margin-bottom: 2rem;
    }

    .login-header h2 {
        font-family: 'Inter', sans-serif;
        font-size: 1.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #8b5cf6, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }

    .login-header p {
        color: #64748b;
        font-size: 0.85rem;
        margin-top: 0.3rem;
        font-family: 'Inter', sans-serif;
    }

    .login-footer {
        text-align: center;
        margin-top: 1.5rem;
        color: #475569;
        font-size: 0.75rem;
        font-family: 'Inter', sans-serif;
    }

    /* Override Streamlit input styling in login */
    .login-container [data-testid="stTextInput"] > div > div > input {
        background: #111827 !important; /* Solid dark instead of semi-transparent */
        border: 1px solid rgba(139,92,246,0.3) !important;
        border-radius: 10px !important;
        color: #f1f5f9 !important;
        font-family: 'Inter', sans-serif !important;
        padding: 0.6rem 1rem !important;
    }

    .login-container [data-testid="stTextInput"] > div > div > input:focus {
        border-color: #8b5cf6 !important;
        box-shadow: 0 0 0 3px rgba(139,92,246,0.2) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Login form
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown("""
    <div class="login-header">
        <div style="margin:0 auto;width:60px;height:60px;">
            <svg viewBox="0 0 60 60" fill="none" xmlns="http://www.w3.org/2000/svg" style="width:60px;height:60px;filter:drop-shadow(0 0 15px rgba(139,92,246,0.5));">
                <defs>
                    <linearGradient id="lockGrad" x1="0" y1="0" x2="1" y2="1">
                        <stop offset="0%" stop-color="#8b5cf6"/>
                        <stop offset="100%" stop-color="#ec4899"/>
                    </linearGradient>
                </defs>
                <circle cx="30" cy="30" r="28" stroke="url(#lockGrad)" stroke-width="1.5" fill="rgba(139,92,246,0.06)">
                    <animate attributeName="r" values="26;28;26" dur="3s" repeatCount="indefinite"/>
                    <animate attributeName="opacity" values="0.4;0.8;0.4" dur="3s" repeatCount="indefinite"/>
                </circle>
                <path d="M22 28V24C22 19.6 25.6 16 30 16C34.4 16 38 19.6 38 24V28" stroke="url(#lockGrad)" stroke-width="2.5" stroke-linecap="round" fill="none"/>
                <rect x="19" y="28" width="22" height="16" rx="4" fill="url(#lockGrad)" opacity="0.85"/>
                <circle cx="30" cy="36" r="2.5" fill="#0a0e1a"/>
                <line x1="30" y1="38" x2="30" y2="41" stroke="#0a0e1a" stroke-width="2" stroke-linecap="round"/>
            </svg>
        </div>
        <h2>Selamat Datang</h2>
        <p>Silakan login untuk melanjutkan</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("👤 Username", placeholder="Masukkan username...")
        password = st.text_input("🔑 Password", type="password", placeholder="Masukkan password...")
        submitted = st.form_submit_button("🚀 Masuk", use_container_width=True)

        if submitted:
            if username and password:
                if _check_login(username, password):
                    st.session_state['authenticated'] = True
                    st.session_state['username'] = username
                    st.rerun()
                else:
                    st.error("❌ Username atau password salah!")
            else:
                st.warning("Silakan isi username dan password.")

    st.markdown("""
    <div class="login-footer">
        bosssmuda &bull; Akses terbatas
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# --- AUTH GATE: Cek apakah sudah login ---
if not st.session_state.get('authenticated', False):
    _show_login_page()
    st.stop()

# =============================================
# CUSTOM CSS — ULTRA AESTHETIC DARK THEME
# =============================================
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

/* ====== HEADER AREA ====== */
.main-header {
    text-align: center;
    padding: 2rem 1rem 1.5rem;
    margin-bottom: 1.5rem;
    position: relative;
}

.main-header h1 {
    font-size: 2.8rem;
    font-weight: 800;
    background: var(--gradient-main);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.5px;
    margin-bottom: 0.3rem;
    animation: fadeInDown 0.8s ease-out;
}

.main-header .subtitle {
    font-size: 1rem;
    color: var(--text-muted);
    font-weight: 400;
    letter-spacing: 0.3px;
    animation: fadeInUp 0.8s ease-out 0.2s both;
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


# =============================================
# HELPER FUNCTIONS
# =============================================

@st.cache_data(show_spinner=False)
def muat_data(file_path):
    """Memuat dan membersihkan data dari file Excel/CSV."""
    try:
        if file_path.lower().endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)

        kolom_angka = ['HOLDINGS_SCRIPLESS', 'HOLDINGS_SCRIP', 'TOTAL_HOLDING_SHARES']
        for col in kolom_angka:
            if col in df.columns:
                df[col] = df[col].astype(str).str.replace('.', '', regex=False)
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        if 'PERCENTAGE' in df.columns:
            df['PERCENTAGE'] = df['PERCENTAGE'].astype(str).str.replace(',', '.', regex=False)
            df['PERCENTAGE'] = pd.to_numeric(df['PERCENTAGE'], errors='coerce').fillna(0.0)

        rename_mapping = {
            'DATE': 'TGL', 'SHARE_CODE': 'KODE', 'ISSUER_NAME': 'EMITEN',
            'INVESTOR_NAME': 'INVESTOR', 'INVESTOR_TYPE': 'TIPE',
            'LOCAL_FOREIGN': 'L/F', 'NATIONALITY': 'ASAL', 'DOMICILE': 'DOMISILI',
            'HOLDINGS_SCRIPLESS': 'SCRIPLESS', 'HOLDINGS_SCRIP': 'SCRIP',
            'TOTAL_HOLDING_SHARES': 'TOTAL_SAHAM', 'PERCENTAGE': 'PERSEN(%)'
        }
        df = df.rename(columns=rename_mapping)

        if 'INVESTOR' in df.columns:
            df['INVESTOR'] = df['INVESTOR'].fillna('UNKNOWN')

        return df
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
        return None


def tambah_free_float(data, kode_saham):
    """Menambahkan baris free float jika total < 100%."""
    total_persen = data['PERSEN(%)'].sum()
    if total_persen < 99.9:
        sisa = 100.0 - total_persen
        baris_ff = {col: '-' for col in data.columns}
        baris_ff['KODE'] = kode_saham
        baris_ff['INVESTOR'] = 'MASYARAKAT / FREE FLOAT'
        baris_ff['PERSEN(%)'] = sisa
        baris_ff['TOTAL_SAHAM'] = 0
        baris_ff['EMITEN'] = data['EMITEN'].iloc[0] if 'EMITEN' in data.columns else kode_saham
        data = pd.concat([data, pd.DataFrame([baris_ff])], ignore_index=True)
        data = data.sort_values(by='PERSEN(%)', ascending=False)
    return data


def format_angka(n):
    """Format angka besar ke bahasa Indonesia."""
    if n >= 1e12:
        return f"{n/1e12:,.2f} T"
    elif n >= 1e9:
        return f"{n/1e9:,.2f} M"
    elif n >= 1e6:
        return f"{n/1e6:,.1f} Jt"
    else:
        return f"{n:,.0f}"


def render_metric_cards(metrics):
    """Render metric cards menggunakan HTML."""
    cards_html = '<div class="metric-container">'
    for m in metrics:
        cards_html += f'''
        <div class="metric-card">
            <div class="metric-icon">{m["icon"]}</div>
            <div class="metric-value">{m["value"]}</div>
            <div class="metric-label">{m["label"]}</div>
        </div>'''
    cards_html += '</div>'
    st.markdown(cards_html, unsafe_allow_html=True)


# =============================================
# SIDEBAR
# =============================================

with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0 0.5rem;">
        <div style="margin: 0 auto 0.5rem; width: 56px; height: 56px;">
            <svg viewBox="0 0 56 56" fill="none" xmlns="http://www.w3.org/2000/svg" style="width:56px;height:56px;filter:drop-shadow(0 0 12px rgba(139,92,246,0.4));">
                <defs>
                    <linearGradient id="barGrad1" x1="0" y1="1" x2="0" y2="0">
                        <stop offset="0%" stop-color="#8b5cf6"/>
                        <stop offset="100%" stop-color="#ec4899"/>
                    </linearGradient>
                    <linearGradient id="barGrad2" x1="0" y1="1" x2="0" y2="0">
                        <stop offset="0%" stop-color="#06b6d4"/>
                        <stop offset="100%" stop-color="#8b5cf6"/>
                    </linearGradient>
                    <linearGradient id="barGrad3" x1="0" y1="1" x2="0" y2="0">
                        <stop offset="0%" stop-color="#ec4899"/>
                        <stop offset="100%" stop-color="#f59e0b"/>
                    </linearGradient>
                    <linearGradient id="circleGrad" x1="0" y1="0" x2="1" y2="1">
                        <stop offset="0%" stop-color="rgba(139,92,246,0.15)"/>
                        <stop offset="100%" stop-color="rgba(6,182,212,0.08)"/>
                    </linearGradient>
                </defs>
                <circle cx="28" cy="28" r="27" stroke="url(#barGrad2)" stroke-width="1.5" fill="url(#circleGrad)" opacity="0.6"/>
                <rect x="10" y="30" width="7" height="14" rx="2" fill="url(#barGrad1)" opacity="0.9">
                    <animate attributeName="height" values="4;14;4" dur="2.5s" repeatCount="indefinite" begin="0s"/>
                    <animate attributeName="y" values="40;30;40" dur="2.5s" repeatCount="indefinite" begin="0s"/>
                </rect>
                <rect x="20" y="18" width="7" height="26" rx="2" fill="url(#barGrad2)" opacity="0.9">
                    <animate attributeName="height" values="10;26;10" dur="2.5s" repeatCount="indefinite" begin="0.3s"/>
                    <animate attributeName="y" values="34;18;34" dur="2.5s" repeatCount="indefinite" begin="0.3s"/>
                </rect>
                <rect x="30" y="22" width="7" height="22" rx="2" fill="url(#barGrad3)" opacity="0.9">
                    <animate attributeName="height" values="6;22;6" dur="2.5s" repeatCount="indefinite" begin="0.6s"/>
                    <animate attributeName="y" values="38;22;38" dur="2.5s" repeatCount="indefinite" begin="0.6s"/>
                </rect>
                <rect x="40" y="12" width="7" height="32" rx="2" fill="url(#barGrad1)" opacity="0.9">
                    <animate attributeName="height" values="12;32;12" dur="2.5s" repeatCount="indefinite" begin="0.9s"/>
                    <animate attributeName="y" values="32;12;32" dur="2.5s" repeatCount="indefinite" begin="0.9s"/>
                </rect>
                <line x1="8" y1="44" x2="49" y2="44" stroke="#94a3b8" stroke-width="1.2" stroke-linecap="round" opacity="0.4"/>
            </svg>
        </div>
        <h2 style="font-size: 1.2rem; font-weight: 700; background: linear-gradient(135deg, #8b5cf6, #ec4899);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0;">
        bosssmuda</h2>
        <p style="color: #64748b; font-size: 0.75rem; margin-top: 0.2rem;">Dashboard Kepemilikan Saham IDX</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

    # File picker
    st.markdown("##### 📁 Sumber Data")

    file_default = None
    for f in ['Data.xlsx', 'Data.csv', 'Data_Kepemilikan_Saham_27_Feb_2026_FULL.xlsx - Sheet1.csv']:
        if os.path.exists(f):
            file_default = f
            break

    uploaded_file = st.file_uploader("Upload file", type=['xlsx', 'xls', 'csv'],
                                      label_visibility='collapsed')

    if uploaded_file:
        # Simpan ke temp
        tmp_path = os.path.join(tempfile.gettempdir(), uploaded_file.name)
        with open(tmp_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())
        file_path = tmp_path
        st.success(f"✓ {uploaded_file.name}")
    elif file_default:
        file_path = file_default
        st.info(f"📄 {file_default}")
    else:
        file_path = None
        st.warning("Belum ada file data.")

    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
    st.markdown("##### ℹ️ Tentang")
    st.markdown("""
    <div class="info-box">
        Dashboard interaktif untuk analisis kepemilikan saham di Bursa Efek Indonesia (IDX).
        Dibangun dengan Python, Streamlit & Plotly.
    </div>
    """, unsafe_allow_html=True)

    # User info & Logout
    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
    current_user = st.session_state.get('username', 'unknown')
    st.markdown(f"""
    <div style="text-align:center;padding:0.5rem 0;">
        <span style="color:#94a3b8;font-size:0.8rem;">Login sebagai:</span><br>
        <span style="color:#8b5cf6;font-weight:700;font-size:0.95rem;">👤 {current_user}</span>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🚪 Logout", use_container_width=True, key="btn_logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


# =============================================
# MAIN CONTENT
# =============================================

# Header
st.markdown("""
<div class="main-header">
    <h1>bosssmuda</h1>
    <div class="subtitle">Dashboard Analisis Kepemilikan Saham Bursa Efek Indonesia</div>
</div>
""", unsafe_allow_html=True)

if file_path is None:
    st.markdown("""
    <div style="text-align:center; padding: 4rem 2rem;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">📂</div>
        <h3 style="color: var(--text-secondary);">Upload file data di sidebar untuk memulai</h3>
        <p style="color: var(--text-muted);">Format yang didukung: .xlsx, .xls, .csv</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# Load data
with st.spinner("⏳ Memuat dan membersihkan data..."):
    df = muat_data(file_path)

if df is None:
    st.stop()

# =============================================
# OVERVIEW METRICS
# =============================================
total_emiten = df['KODE'].nunique() if 'KODE' in df.columns else 0
total_investor = df['INVESTOR'].nunique() if 'INVESTOR' in df.columns else 0
total_baris = len(df)
total_lokal = df[df['L/F'].str.upper().isin(['L', 'LOKAL', 'LOCAL'])].shape[0] if 'L/F' in df.columns else 0
total_asing = df[df['L/F'].str.upper().isin(['F', 'ASING', 'FOREIGN'])].shape[0] if 'L/F' in df.columns else 0

render_metric_cards([
    {"icon": "🏢", "value": format_angka(total_emiten), "label": "Total Emiten"},
    {"icon": "👤", "value": format_angka(total_investor), "label": "Total Investor"},
    {"icon": "📋", "value": format_angka(total_baris), "label": "Total Records"},
    {"icon": "🇮🇩", "value": format_angka(total_lokal), "label": "Investor Lokal"},
    {"icon": "🌍", "value": format_angka(total_asing), "label": "Investor Asing"},
])

st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

# =============================================
# TABS
# =============================================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🔍 Cari Emiten",
    "👤 Cari Investor",
    "🏆 Ranking",
    "🕸️ Network Graph",
    "📈 Data Pasar",
    "📄 Ekspor PDF"
])

# =============================================
# TAB 1: CARI EMITEN
# =============================================
with tab1:
    st.markdown('<div class="section-title">🔍 Analisis Per Emiten</div>', unsafe_allow_html=True)

    daftar_kode = sorted(df['KODE'].unique().tolist()) if 'KODE' in df.columns else []
    col_sel, col_info = st.columns([1, 2])

    with col_sel:
        kode_selected = st.selectbox("Pilih Kode Emiten", daftar_kode,
                                     index=0 if daftar_kode else None,
                                     key="emiten_select")

    if kode_selected:
        data_emiten = df[df['KODE'] == kode_selected].copy()
        data_emiten = data_emiten.sort_values(by='PERSEN(%)', ascending=False)
        data_emiten = tambah_free_float(data_emiten, kode_selected)

        emiten_name = data_emiten['EMITEN'].iloc[0] if 'EMITEN' in data_emiten.columns else kode_selected

        with col_info:
            st.markdown(f"""
            <div class="info-box">
                <strong>{kode_selected}</strong> — {emiten_name}<br>
                Jumlah pemegang saham: <strong>{len(data_emiten)}</strong> &nbsp;|&nbsp;
                Total persentase: <strong>{data_emiten['PERSEN(%)'].sum():.2f}%</strong>
            </div>
            """, unsafe_allow_html=True)

        # Charts
        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            # Donut chart
            top8 = data_emiten.head(8).copy()
            if len(data_emiten) > 8:
                sisa_persen = data_emiten.iloc[8:]['PERSEN(%)'].sum()
                others = pd.DataFrame([{'INVESTOR': 'Lainnya', 'PERSEN(%)': sisa_persen}])
                top8 = pd.concat([top8, others], ignore_index=True)

            fig_donut = go.Figure(data=[go.Pie(
                labels=top8['INVESTOR'].apply(lambda x: str(x)[:28]).tolist(),
                values=top8['PERSEN(%)'].tolist(),
                hole=0.55,
                marker=dict(colors=COLOR_SEQUENCE[:len(top8)],
                            line=dict(color='#0a0e1a', width=2)),
                textfont=dict(size=11, color='#f1f5f9'),
                hovertemplate='<b>%{label}</b><br>Kepemilikan: %{value:.2f}%<extra></extra>',
                textinfo='percent',
                textposition='outside'
            )])
            fig_donut.update_layout(
                **PLOTLY_LAYOUT,
                title=dict(text=f"Komposisi Kepemilikan {kode_selected}",
                           font=dict(size=15, color='#f1f5f9')),
                height=420,
                showlegend=True,
            )
            fig_donut.update_layout(
                legend=dict(font=dict(size=10, color='#94a3b8'),
                            bgcolor='rgba(0,0,0,0)', x=1.05)
            )
            fig_donut.add_annotation(
                text=f"<b>{kode_selected}</b>",
                showarrow=False,
                font=dict(size=18, color='#8b5cf6', family='Inter'),
                x=0.5, y=0.5
            )
            st.plotly_chart(fig_donut, use_container_width=True)

        with chart_col2:
            # Horizontal bar
            top10bar = data_emiten.head(10).copy()
            top10bar = top10bar.sort_values(by='PERSEN(%)', ascending=True)

            fig_bar = go.Figure(data=[go.Bar(
                y=top10bar['INVESTOR'].apply(lambda x: str(x)[:30]).tolist(),
                x=top10bar['PERSEN(%)'].tolist(),
                orientation='h',
                marker=dict(
                    color=top10bar['PERSEN(%)'].tolist(),
                    colorscale=[[0, '#06b6d4'], [0.5, '#8b5cf6'], [1, '#ec4899']],
                    line=dict(width=0)
                ),
                hovertemplate='<b>%{y}</b><br>Kepemilikan: %{x:.2f}%<extra></extra>',
                text=top10bar['PERSEN(%)'].apply(lambda x: f'{x:.2f}%').tolist(),
                textposition='outside',
                textfont=dict(size=11, color='#94a3b8')
            )])
            fig_bar.update_layout(**PLOTLY_LAYOUT)
            fig_bar.update_layout(
                title=dict(text=f"Top 10 Pemegang Saham {kode_selected}",
                           font=dict(size=15, color='#f1f5f9')),
                height=420,
                xaxis=dict(title="Persentase (%)", gridcolor='rgba(148,163,184,0.08)'),
                showlegend=False
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        # Tabel detail
        with st.expander("📋 Lihat Tabel Detail Lengkap", expanded=False):
            kolom_tampil = [c for c in ['INVESTOR', 'TIPE', 'L/F', 'ASAL', 'SCRIPLESS',
                                         'SCRIP', 'TOTAL_SAHAM', 'PERSEN(%)'] if c in data_emiten.columns]
            st.dataframe(data_emiten[kolom_tampil].reset_index(drop=True),
                         use_container_width=True, height=400)


# =============================================
# TAB 2: CARI INVESTOR
# =============================================
with tab2:
    st.markdown('<div class="section-title">👤 Portofolio Investor</div>', unsafe_allow_html=True)

    nama_input = st.text_input("Masukkan nama investor atau instansi",
                                placeholder="Contoh: BLACKROCK, GARIBALDI, VANGUARD...",
                                key="investor_input")

    if nama_input:
        nama_upper = nama_input.upper()
        hasil_inv = df[df['INVESTOR'].str.upper().str.contains(nama_upper, na=False)].copy()

        if hasil_inv.empty:
            st.warning(f"Tidak ada portofolio untuk investor '{nama_input}'.")
        else:
            hasil_inv = hasil_inv.sort_values(by='PERSEN(%)', ascending=False)

            # Metrics
            jumlah_emiten_inv = hasil_inv['KODE'].nunique()
            total_lembar_inv = hasil_inv['TOTAL_SAHAM'].sum()
            avg_persen = hasil_inv['PERSEN(%)'].mean()

            render_metric_cards([
                {"icon": "🏢", "value": str(jumlah_emiten_inv), "label": "Emiten Dimiliki"},
                {"icon": "📊", "value": format_angka(total_lembar_inv), "label": "Total Lembar"},
                {"icon": "📈", "value": f"{avg_persen:.2f}%", "label": "Rata-rata Kepemilikan"},
                {"icon": "📋", "value": str(len(hasil_inv)), "label": "Total Records"},
            ])

            st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

            # Bar chart portofolio
            top15 = hasil_inv.head(15).copy()
            top15_sorted = top15.sort_values(by='PERSEN(%)', ascending=True)

            fig_inv = go.Figure(data=[go.Bar(
                y=top15_sorted['KODE'].tolist(),
                x=top15_sorted['PERSEN(%)'].tolist(),
                orientation='h',
                marker=dict(
                    color=top15_sorted['PERSEN(%)'].tolist(),
                    colorscale=[[0, '#10b981'], [0.5, '#06b6d4'], [1, '#8b5cf6']],
                    line=dict(width=0)
                ),
                hovertemplate='<b>%{y}</b><br>Kepemilikan: %{x:.2f}%<extra></extra>',
                text=top15_sorted['PERSEN(%)'].apply(lambda x: f'{x:.2f}%').tolist(),
                textposition='outside',
                textfont=dict(size=11, color='#94a3b8')
            )])
            fig_inv.update_layout(**PLOTLY_LAYOUT)
            fig_inv.update_layout(
                title=dict(text=f"Porsi {nama_input.upper()} di Berbagai Emiten",
                           font=dict(size=15, color='#f1f5f9')),
                height=max(350, len(top15) * 35),
                xaxis=dict(title="Persentase (%)", gridcolor='rgba(148,163,184,0.08)'),
                showlegend=False
            )
            st.plotly_chart(fig_inv, use_container_width=True)

            # Tabel
            with st.expander("📋 Lihat Tabel Detail", expanded=False):
                kolom_inv = [c for c in ['KODE', 'EMITEN', 'TIPE', 'L/F', 'TOTAL_SAHAM',
                                          'PERSEN(%)'] if c in hasil_inv.columns]
                st.dataframe(hasil_inv[kolom_inv].reset_index(drop=True),
                             use_container_width=True, height=400)


# =============================================
# TAB 3: RANKING
# =============================================
with tab3:
    st.markdown('<div class="section-title">🏆 Peringkat Investor</div>', unsafe_allow_html=True)

    rank_mode = st.radio("Pilih jenis ranking:",
                         ["Total Lembar Saham Terbanyak", "Portofolio Emiten Terbanyak (Diversifikasi)"],
                         horizontal=True, key="rank_radio")

    top_n_rank = st.slider("Jumlah top investor:", min_value=10, max_value=50, value=20, key="rank_slider")

    df_valid = df[~df['INVESTOR'].str.upper().isin(['UNKNOWN', 'MASYARAKAT / FREE FLOAT'])]

    if rank_mode == "Total Lembar Saham Terbanyak":
        peringkat = df_valid.groupby('INVESTOR')['TOTAL_SAHAM'].sum().reset_index()
        peringkat = peringkat.sort_values(by='TOTAL_SAHAM', ascending=False).head(top_n_rank)

        peringkat_sorted = peringkat.sort_values(by='TOTAL_SAHAM', ascending=True)

        fig_rank = go.Figure(data=[go.Bar(
            y=peringkat_sorted['INVESTOR'].apply(lambda x: str(x)[:35]).tolist(),
            x=peringkat_sorted['TOTAL_SAHAM'].tolist(),
            orientation='h',
            marker=dict(
                color=peringkat_sorted['TOTAL_SAHAM'].tolist(),
                colorscale=[[0, '#f59e0b'], [0.5, '#ec4899'], [1, '#8b5cf6']],
                line=dict(width=0)
            ),
            hovertemplate='<b>%{y}</b><br>Total: %{x:,.0f} lembar<extra></extra>',
            text=peringkat_sorted['TOTAL_SAHAM'].apply(lambda x: format_angka(x)).tolist(),
            textposition='outside',
            textfont=dict(size=10, color='#94a3b8')
        )])
        fig_rank.update_layout(**PLOTLY_LAYOUT)
        fig_rank.update_layout(
            title=dict(text=f"Top {top_n_rank} Investor — Total Lembar Saham",
                       font=dict(size=15, color='#f1f5f9')),
            height=max(450, top_n_rank * 28),
            xaxis=dict(title="Total Lembar Saham", gridcolor='rgba(148,163,184,0.08)'),
            showlegend=False
        )
        st.plotly_chart(fig_rank, use_container_width=True)

    else:
        peringkat = df_valid.groupby('INVESTOR')['KODE'].nunique().reset_index()
        peringkat.columns = ['INVESTOR', 'TOTAL_EMITEN']
        peringkat = peringkat.sort_values(by='TOTAL_EMITEN', ascending=False).head(top_n_rank)

        peringkat_sorted = peringkat.sort_values(by='TOTAL_EMITEN', ascending=True)

        fig_rank = go.Figure(data=[go.Bar(
            y=peringkat_sorted['INVESTOR'].apply(lambda x: str(x)[:35]).tolist(),
            x=peringkat_sorted['TOTAL_EMITEN'].tolist(),
            orientation='h',
            marker=dict(
                color=peringkat_sorted['TOTAL_EMITEN'].tolist(),
                colorscale=[[0, '#06b6d4'], [0.5, '#10b981'], [1, '#8b5cf6']],
                line=dict(width=0)
            ),
            hovertemplate='<b>%{y}</b><br>Jumlah emiten: %{x}<extra></extra>',
            text=peringkat_sorted['TOTAL_EMITEN'].tolist(),
            textposition='outside',
            textfont=dict(size=11, color='#94a3b8')
        )])
        fig_rank.update_layout(**PLOTLY_LAYOUT)
        fig_rank.update_layout(
            title=dict(text=f"Top {top_n_rank} Investor — Diversifikasi Portofolio",
                       font=dict(size=15, color='#f1f5f9')),
            height=max(450, top_n_rank * 28),
            xaxis=dict(title="Jumlah Emiten", gridcolor='rgba(148,163,184,0.08)'),
            showlegend=False
        )
        st.plotly_chart(fig_rank, use_container_width=True)

    with st.expander("📋 Lihat Tabel Ranking", expanded=False):
        st.dataframe(peringkat.reset_index(drop=True), use_container_width=True)


# =============================================
# TAB 4: NETWORK GRAPH
# =============================================
with tab4:
    st.markdown('<div class="section-title">🕸️ Visualisasi Network Graph</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box">
        Buat visualisasi jaring laba-laba interaktif untuk melihat koneksi antara investor dan emiten.
        Graph akan dibuka di tab browser baru.
    </div>
    """, unsafe_allow_html=True)

    net_mode = st.radio("Mode Network:", ["🏢 Cari berdasarkan Emiten", "👤 Cari berdasarkan Investor"],
                        horizontal=True, key="net_radio")

    if net_mode == "🏢 Cari berdasarkan Emiten":
        kode_net = st.selectbox("Pilih Kode Emiten", daftar_kode, key="net_emiten_select")
        if st.button("🕸️ Generate Network Graph", key="btn_net_emiten"):
            try:
                from network_graph import buat_network_emiten
                with st.spinner("Membuat network graph..."):
                    filepath = buat_network_emiten(df, kode_net)
                if filepath and os.path.exists(filepath):
                    st.success(f"✓ Network graph berhasil dibuat!")
                    with open(filepath, 'r', encoding='utf-8') as f:
                        html_content = f.read()
                    st.components.v1.html(html_content, height=650, scrolling=True)
            except ImportError:
                st.error("Modul `networkx` atau `pyvis` belum terinstall. Jalankan: `pip install networkx pyvis`")
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        nama_net = st.text_input("Nama Investor", placeholder="Contoh: BLACKROCK", key="net_inv_input")
        if nama_net and st.button("🕸️ Generate Network Graph", key="btn_net_inv"):
            try:
                from network_graph import buat_network_investor
                with st.spinner("Membuat network graph..."):
                    filepath = buat_network_investor(df, nama_net)
                if filepath and os.path.exists(filepath):
                    st.success(f"✓ Network graph berhasil dibuat!")
                    with open(filepath, 'r', encoding='utf-8') as f:
                        html_content = f.read()
                    st.components.v1.html(html_content, height=650, scrolling=True)
            except ImportError:
                st.error("Modul `networkx` atau `pyvis` belum terinstall. Jalankan: `pip install networkx pyvis`")
            except Exception as e:
                st.error(f"Error: {e}")


# =============================================
# TAB 5: DATA PASAR (COMPREHENSIVE)
# =============================================
with tab5:
    st.markdown('<div class="section-title">📈 Data Pasar Komprehensif (Yahoo Finance)</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box">
        Analisis mendalam data pasar saham real-time dari Yahoo Finance.<br>
        Kode saham otomatis dikonversi ke format <code>.JK</code> untuk Bursa Efek Indonesia.
    </div>
    """, unsafe_allow_html=True)

    col_yf1, col_yf2 = st.columns([1, 1])

    with col_yf1:
        kode_yf = st.selectbox("Pilih Kode Emiten", daftar_kode, key="yf_select")

    with col_yf2:
        period_yf = st.selectbox("Periode Histori", ["1mo", "3mo", "6mo", "1y", "ytd", "5y"],
                                 index=0, key="yf_period")

    if st.button("📊 Ambil Seluruh Data Pasar", key="btn_yf"):
        try:
            import yfinance as yf

            ticker_symbol = f"{kode_yf}.JK"

            with st.spinner(f"Mengambil data komprehensif {ticker_symbol}..."):
                ticker = yf.Ticker(ticker_symbol)
                info = ticker.info or {}
                hist = ticker.history(period=period_yf)

                # Pre-fetch all data
                try:
                    financials = ticker.financials
                except Exception:
                    financials = pd.DataFrame()
                try:
                    quarterly_financials = ticker.quarterly_financials
                except Exception:
                    quarterly_financials = pd.DataFrame()
                try:
                    balance_sheet = ticker.balance_sheet
                except Exception:
                    balance_sheet = pd.DataFrame()
                try:
                    quarterly_balance_sheet = ticker.quarterly_balance_sheet
                except Exception:
                    quarterly_balance_sheet = pd.DataFrame()
                try:
                    cashflow = ticker.cashflow
                except Exception:
                    cashflow = pd.DataFrame()
                try:
                    quarterly_cashflow = ticker.quarterly_cashflow
                except Exception:
                    quarterly_cashflow = pd.DataFrame()
                try:
                    dividends = ticker.dividends
                except Exception:
                    dividends = pd.Series(dtype='float64')
                try:
                    splits = ticker.splits
                except Exception:
                    splits = pd.Series(dtype='float64')
                try:
                    news = ticker.news
                except Exception:
                    news = []
                try:
                    recommendations = ticker.recommendations
                except Exception:
                    recommendations = pd.DataFrame()

            # Store in session state
            st.session_state['yf_data'] = {
                'info': info, 'hist': hist, 'ticker_symbol': ticker_symbol,
                'financials': financials, 'quarterly_financials': quarterly_financials,
                'balance_sheet': balance_sheet, 'quarterly_balance_sheet': quarterly_balance_sheet,
                'cashflow': cashflow, 'quarterly_cashflow': quarterly_cashflow,
                'dividends': dividends, 'splits': splits,
                'news': news, 'recommendations': recommendations,
                'kode': kode_yf, 'period': period_yf
            }
            st.success(f"Data {ticker_symbol} berhasil dimuat!")

        except ImportError:
            st.error("Modul `yfinance` belum terinstall. Jalankan: `pip install yfinance`")
        except Exception as e:
            st.error(f"Error mengambil data: {e}")

    # ---- RENDER DATA IF AVAILABLE ----
    if 'yf_data' in st.session_state:
        yfd = st.session_state['yf_data']
        info = yfd['info']
        hist = yfd['hist']
        kode_display = yfd['kode']
        period_display = yfd['period']

        # Sub-tabs for organized display
        yf_tab1, yf_tab2, yf_tab3, yf_tab4, yf_tab5, yf_tab6, yf_tab7 = st.tabs([
            "📊 Overview & Harga",
            "📋 Key Statistics",
            "📈 Laporan Keuangan",
            "🔔 Corporate Actions",
            "📰 News & Sentimen",
            "🏢 Profil Perusahaan",
            "🎯 Rekomendasi Analis"
        ])

        # ---- SUB-TAB 1: OVERVIEW & PRICE CHART ----
        with yf_tab1:
            if info:
                harga = info.get('regularMarketPrice', info.get('previousClose', 0))
                prev = info.get('previousClose', 0)
                volume = info.get('regularMarketVolume', info.get('volume', 0))
                mcap = info.get('marketCap', 0)
                high52 = info.get('fiftyTwoWeekHigh', 0)
                low52 = info.get('fiftyTwoWeekLow', 0)

                change = harga - prev if harga and prev else 0
                change_pct = (change / prev * 100) if prev and prev != 0 else 0
                change_icon = "🟢" if change >= 0 else "🔴"

                render_metric_cards([
                    {"icon": "💰", "value": f"Rp {harga:,.0f}" if harga else 'N/A', "label": "Harga Terakhir"},
                    {"icon": change_icon, "value": f"{change:+,.0f} ({change_pct:+.2f}%)", "label": "Perubahan Harian"},
                    {"icon": "📊", "value": format_angka(volume) if volume else 'N/A', "label": "Volume"},
                    {"icon": "🏦", "value": format_angka(mcap) if mcap else 'N/A', "label": "Market Cap"},
                    {"icon": "📈", "value": f"Rp {high52:,.0f}" if high52 else 'N/A', "label": "52W High"},
                    {"icon": "📉", "value": f"Rp {low52:,.0f}" if low52 else 'N/A', "label": "52W Low"},
                ])

            if hist is not None and not hist.empty:
                st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

                # Candlestick chart
                fig_candle = go.Figure(data=[go.Candlestick(
                    x=hist.index,
                    open=hist['Open'], high=hist['High'],
                    low=hist['Low'], close=hist['Close'],
                    increasing_line_color='#10b981',
                    decreasing_line_color='#ef4444',
                    increasing_fillcolor='rgba(16,185,129,0.5)',
                    decreasing_fillcolor='rgba(239,68,68,0.5)',
                )])
                fig_candle.update_layout(**PLOTLY_LAYOUT)
                fig_candle.update_layout(
                    title=dict(text=f"Candlestick {kode_display} ({period_display})",
                               font=dict(size=15, color='#f1f5f9')),
                    height=450,
                    xaxis=dict(title="Tanggal", rangeslider=dict(visible=False)),
                    yaxis=dict(title="Harga (IDR)")
                )
                st.plotly_chart(fig_candle, use_container_width=True)

                # Volume chart
                vol_colors = ['#10b981' if c >= o else '#ef4444'
                              for c, o in zip(hist['Close'], hist['Open'])]
                fig_vol = go.Figure(data=[go.Bar(
                    x=hist.index, y=hist['Volume'],
                    marker=dict(color=vol_colors, opacity=0.7, line=dict(width=0)),
                    hovertemplate='%{x}<br>Volume: %{y:,.0f}<extra></extra>'
                )])
                fig_vol.update_layout(**PLOTLY_LAYOUT)
                fig_vol.update_layout(
                    title=dict(text=f"Volume Transaksi {kode_display}",
                               font=dict(size=14, color='#f1f5f9')),
                    height=220,
                    xaxis=dict(title="Tanggal"),
                    yaxis=dict(title="Volume")
                )
                st.plotly_chart(fig_vol, use_container_width=True)
            else:
                st.warning(f"Data histori tidak tersedia untuk {kode_display}.")

        # ---- SUB-TAB 2: KEY STATISTICS ----
        with yf_tab2:
            st.markdown('<div class="section-title">📋 Key Statistics</div>', unsafe_allow_html=True)

            if info:
                stats_data = {
                    'Valuasi': {
                        'Market Cap': format_angka(info.get('marketCap', 0)) if info.get('marketCap') else 'N/A',
                        'Enterprise Value': format_angka(info.get('enterpriseValue', 0)) if info.get('enterpriseValue') else 'N/A',
                        'Trailing P/E': f"{info.get('trailingPE', 'N/A'):.2f}" if isinstance(info.get('trailingPE'), (int, float)) else 'N/A',
                        'Forward P/E': f"{info.get('forwardPE', 'N/A'):.2f}" if isinstance(info.get('forwardPE'), (int, float)) else 'N/A',
                        'PEG Ratio': f"{info.get('pegRatio', 'N/A'):.2f}" if isinstance(info.get('pegRatio'), (int, float)) else 'N/A',
                        'Price/Sales (TTM)': f"{info.get('priceToSalesTrailing12Months', 'N/A'):.2f}" if isinstance(info.get('priceToSalesTrailing12Months'), (int, float)) else 'N/A',
                        'Price/Book': f"{info.get('priceToBook', 'N/A'):.2f}" if isinstance(info.get('priceToBook'), (int, float)) else 'N/A',
                        'EV/Revenue': f"{info.get('enterpriseToRevenue', 'N/A'):.2f}" if isinstance(info.get('enterpriseToRevenue'), (int, float)) else 'N/A',
                        'EV/EBITDA': f"{info.get('enterpriseToEbitda', 'N/A'):.2f}" if isinstance(info.get('enterpriseToEbitda'), (int, float)) else 'N/A',
                    },
                    'Profitabilitas': {
                        'Profit Margin': f"{info.get('profitMargins', 0)*100:.2f}%" if isinstance(info.get('profitMargins'), (int, float)) else 'N/A',
                        'Operating Margin': f"{info.get('operatingMargins', 0)*100:.2f}%" if isinstance(info.get('operatingMargins'), (int, float)) else 'N/A',
                        'ROE': f"{info.get('returnOnEquity', 0)*100:.2f}%" if isinstance(info.get('returnOnEquity'), (int, float)) else 'N/A',
                        'ROA': f"{info.get('returnOnAssets', 0)*100:.2f}%" if isinstance(info.get('returnOnAssets'), (int, float)) else 'N/A',
                        'Revenue (TTM)': format_angka(info.get('totalRevenue', 0)) if info.get('totalRevenue') else 'N/A',
                        'Gross Profit': format_angka(info.get('grossProfits', 0)) if info.get('grossProfits') else 'N/A',
                        'EBITDA': format_angka(info.get('ebitda', 0)) if info.get('ebitda') else 'N/A',
                        'Net Income': format_angka(info.get('netIncomeToCommon', 0)) if info.get('netIncomeToCommon') else 'N/A',
                        'EPS (TTM)': f"Rp {info.get('trailingEps', 'N/A'):,.0f}" if isinstance(info.get('trailingEps'), (int, float)) else 'N/A',
                    },
                    'Dividen & Saham': {
                        'Dividend Rate': f"Rp {info.get('dividendRate', 0):,.0f}" if info.get('dividendRate') else 'N/A',
                        'Dividend Yield': f"{info.get('dividendYield', 0)*100:.2f}%" if isinstance(info.get('dividendYield'), (int, float)) else 'N/A',
                        'Payout Ratio': f"{info.get('payoutRatio', 0)*100:.2f}%" if isinstance(info.get('payoutRatio'), (int, float)) else 'N/A',
                        'Beta': f"{info.get('beta', 'N/A'):.2f}" if isinstance(info.get('beta'), (int, float)) else 'N/A',
                        'Shares Outstanding': format_angka(info.get('sharesOutstanding', 0)) if info.get('sharesOutstanding') else 'N/A',
                        'Float Shares': format_angka(info.get('floatShares', 0)) if info.get('floatShares') else 'N/A',
                    },
                    'Trading': {
                        'Open': f"Rp {info.get('regularMarketOpen', 0):,.0f}" if info.get('regularMarketOpen') else 'N/A',
                        'Day High': f"Rp {info.get('dayHigh', 0):,.0f}" if info.get('dayHigh') else 'N/A',
                        'Day Low': f"Rp {info.get('dayLow', 0):,.0f}" if info.get('dayLow') else 'N/A',
                        'Avg Volume (10d)': format_angka(info.get('averageVolume10days', 0)) if info.get('averageVolume10days') else 'N/A',
                        'Avg Volume (3mo)': format_angka(info.get('averageVolume', 0)) if info.get('averageVolume') else 'N/A',
                        '50-Day MA': f"Rp {info.get('fiftyDayAverage', 0):,.0f}" if info.get('fiftyDayAverage') else 'N/A',
                        '200-Day MA': f"Rp {info.get('twoHundredDayAverage', 0):,.0f}" if info.get('twoHundredDayAverage') else 'N/A',
                    },
                }

                cols_stats = st.columns(2)
                for idx, (category, items) in enumerate(stats_data.items()):
                    with cols_stats[idx % 2]:
                        st.markdown(f"**{category}**")
                        stats_df = pd.DataFrame(list(items.items()), columns=['Metrik', 'Nilai'])
                        st.dataframe(stats_df, use_container_width=True, hide_index=True, height=min(400, len(items) * 40 + 40))
            else:
                st.warning("Data key statistics tidak tersedia.")

        # ---- SUB-TAB 3: FINANCIAL STATEMENTS ----
        with yf_tab3:
            st.markdown('<div class="section-title">📈 Laporan Keuangan</div>', unsafe_allow_html=True)

            fin_view = st.radio("Periode:", ["Tahunan", "Kuartalan"], horizontal=True, key="fin_view_radio")

            fin_tab_a, fin_tab_b, fin_tab_c = st.tabs(["💰 Income Statement", "📊 Balance Sheet", "💵 Cash Flow"])

            with fin_tab_a:
                fin_data = yfd['financials'] if fin_view == "Tahunan" else yfd['quarterly_financials']
                if fin_data is not None and not fin_data.empty:
                    display_df = fin_data.copy()
                    display_df.columns = [str(c.date()) if hasattr(c, 'date') else str(c) for c in display_df.columns]
                    st.dataframe(display_df, use_container_width=True, height=500)

                    # Revenue & Net Income chart
                    try:
                        revenue_row = None
                        income_row = None
                        for label in ['Total Revenue', 'Operating Revenue']:
                            if label in fin_data.index:
                                revenue_row = fin_data.loc[label]
                                break
                        for label in ['Net Income', 'Net Income Common Stockholders']:
                            if label in fin_data.index:
                                income_row = fin_data.loc[label]
                                break

                        if revenue_row is not None:
                            fig_fin = go.Figure()
                            dates = [str(c.date()) if hasattr(c, 'date') else str(c) for c in revenue_row.index]
                            fig_fin.add_trace(go.Bar(x=dates, y=revenue_row.values, name='Revenue',
                                                      marker=dict(color='#8b5cf6', opacity=0.8)))
                            if income_row is not None:
                                fig_fin.add_trace(go.Bar(x=dates, y=income_row.values, name='Net Income',
                                                          marker=dict(color='#10b981', opacity=0.8)))
                            fig_fin.update_layout(**PLOTLY_LAYOUT)
                            fig_fin.update_layout(
                                title=dict(text="Revenue vs Net Income", font=dict(size=14, color='#f1f5f9')),
                                height=350, barmode='group',
                                xaxis=dict(title="Periode"),
                                yaxis=dict(title="IDR")
                            )
                            st.plotly_chart(fig_fin, use_container_width=True)
                    except Exception:
                        pass
                else:
                    st.info("Data income statement tidak tersedia untuk emiten ini.")

            with fin_tab_b:
                bs_data = yfd['balance_sheet'] if fin_view == "Tahunan" else yfd['quarterly_balance_sheet']
                if bs_data is not None and not bs_data.empty:
                    display_bs = bs_data.copy()
                    display_bs.columns = [str(c.date()) if hasattr(c, 'date') else str(c) for c in display_bs.columns]
                    st.dataframe(display_bs, use_container_width=True, height=500)

                    # Assets vs Liabilities chart
                    try:
                        asset_row = None
                        liab_row = None
                        equity_row = None
                        for label in ['Total Assets']:
                            if label in bs_data.index:
                                asset_row = bs_data.loc[label]
                                break
                        for label in ['Total Liabilities Net Minority Interest', 'Total Liab']:
                            if label in bs_data.index:
                                liab_row = bs_data.loc[label]
                                break
                        for label in ['Total Equity Gross Minority Interest', 'Stockholders Equity', 'Total Stockholder Equity']:
                            if label in bs_data.index:
                                equity_row = bs_data.loc[label]
                                break

                        if asset_row is not None:
                            fig_bs = go.Figure()
                            dates = [str(c.date()) if hasattr(c, 'date') else str(c) for c in asset_row.index]
                            fig_bs.add_trace(go.Bar(x=dates, y=asset_row.values, name='Total Assets',
                                                     marker=dict(color='#8b5cf6', opacity=0.8)))
                            if liab_row is not None:
                                fig_bs.add_trace(go.Bar(x=dates, y=liab_row.values, name='Total Liabilities',
                                                         marker=dict(color='#ef4444', opacity=0.8)))
                            if equity_row is not None:
                                fig_bs.add_trace(go.Bar(x=dates, y=equity_row.values, name='Equity',
                                                         marker=dict(color='#10b981', opacity=0.8)))
                            fig_bs.update_layout(**PLOTLY_LAYOUT)
                            fig_bs.update_layout(
                                title=dict(text="Assets vs Liabilities vs Equity", font=dict(size=14, color='#f1f5f9')),
                                height=350, barmode='group',
                                xaxis=dict(title="Periode"),
                                yaxis=dict(title="IDR")
                            )
                            st.plotly_chart(fig_bs, use_container_width=True)
                    except Exception:
                        pass
                else:
                    st.info("Data balance sheet tidak tersedia untuk emiten ini.")

            with fin_tab_c:
                cf_data = yfd['cashflow'] if fin_view == "Tahunan" else yfd['quarterly_cashflow']
                if cf_data is not None and not cf_data.empty:
                    display_cf = cf_data.copy()
                    display_cf.columns = [str(c.date()) if hasattr(c, 'date') else str(c) for c in display_cf.columns]
                    st.dataframe(display_cf, use_container_width=True, height=500)

                    # Cash flow chart
                    try:
                        operating_cf = None
                        investing_cf = None
                        financing_cf = None
                        for label in ['Operating Cash Flow', 'Total Cash From Operating Activities']:
                            if label in cf_data.index:
                                operating_cf = cf_data.loc[label]
                                break
                        for label in ['Investing Cash Flow', 'Total Cashflows From Investing Activities']:
                            if label in cf_data.index:
                                investing_cf = cf_data.loc[label]
                                break
                        for label in ['Financing Cash Flow', 'Total Cash From Financing Activities']:
                            if label in cf_data.index:
                                financing_cf = cf_data.loc[label]
                                break

                        if operating_cf is not None:
                            fig_cf = go.Figure()
                            dates = [str(c.date()) if hasattr(c, 'date') else str(c) for c in operating_cf.index]
                            fig_cf.add_trace(go.Bar(x=dates, y=operating_cf.values, name='Operating',
                                                     marker=dict(color='#10b981', opacity=0.8)))
                            if investing_cf is not None:
                                fig_cf.add_trace(go.Bar(x=dates, y=investing_cf.values, name='Investing',
                                                         marker=dict(color='#f59e0b', opacity=0.8)))
                            if financing_cf is not None:
                                fig_cf.add_trace(go.Bar(x=dates, y=financing_cf.values, name='Financing',
                                                         marker=dict(color='#ec4899', opacity=0.8)))
                            fig_cf.update_layout(**PLOTLY_LAYOUT)
                            fig_cf.update_layout(
                                title=dict(text="Cash Flow Breakdown", font=dict(size=14, color='#f1f5f9')),
                                height=350, barmode='group',
                                xaxis=dict(title="Periode"),
                                yaxis=dict(title="IDR")
                            )
                            st.plotly_chart(fig_cf, use_container_width=True)
                    except Exception:
                        pass
                else:
                    st.info("Data cash flow tidak tersedia untuk emiten ini.")

        # ---- SUB-TAB 4: CORPORATE ACTIONS ----
        with yf_tab4:
            st.markdown('<div class="section-title">🔔 Corporate Actions (Dividen & Stock Split)</div>', unsafe_allow_html=True)

            ca_col1, ca_col2 = st.columns(2)

            with ca_col1:
                st.markdown("**Histori Dividen**")
                divs = yfd['dividends']
                if divs is not None and len(divs) > 0:
                    div_df = divs.reset_index()
                    div_df.columns = ['Tanggal', 'Dividen (IDR)']
                    div_df['Tanggal'] = pd.to_datetime(div_df['Tanggal']).dt.date
                    st.dataframe(div_df.sort_values('Tanggal', ascending=False), use_container_width=True, hide_index=True)

                    # Dividend chart
                    fig_div = go.Figure(data=[go.Bar(
                        x=div_df['Tanggal'], y=div_df['Dividen (IDR)'],
                        marker=dict(color='#10b981', opacity=0.8, line=dict(width=0)),
                        hovertemplate='%{x}<br>Dividen: Rp %{y:,.0f}<extra></extra>'
                    )])
                    fig_div.update_layout(**PLOTLY_LAYOUT)
                    fig_div.update_layout(
                        title=dict(text="Histori Dividen", font=dict(size=14, color='#f1f5f9')),
                        height=300,
                        xaxis=dict(title="Tanggal"),
                        yaxis=dict(title="Dividen per Saham (IDR)")
                    )
                    st.plotly_chart(fig_div, use_container_width=True)
                else:
                    st.info("Tidak ada data dividen untuk emiten ini.")

            with ca_col2:
                st.markdown("**Histori Stock Split**")
                splt = yfd['splits']
                if splt is not None and len(splt) > 0:
                    split_df = splt.reset_index()
                    split_df.columns = ['Tanggal', 'Rasio Split']
                    split_df['Tanggal'] = pd.to_datetime(split_df['Tanggal']).dt.date
                    st.dataframe(split_df.sort_values('Tanggal', ascending=False), use_container_width=True, hide_index=True)
                else:
                    st.info("Tidak ada data stock split untuk emiten ini.")

        # ---- SUB-TAB 5: NEWS & SENTIMENT ----
        with yf_tab5:
            st.markdown('<div class="section-title">📰 Berita & Sentimen Terkini</div>', unsafe_allow_html=True)

            news_data = yfd.get('news', [])
            if news_data and len(news_data) > 0:
                for i, article in enumerate(news_data[:15]):
                    # Handle different news data structures from yfinance
                    if isinstance(article, dict):
                        title = article.get('title', article.get('headline', 'No Title'))
                        link = article.get('link', article.get('url', '#'))
                        publisher = article.get('publisher', article.get('source', 'Unknown'))
                        pub_time = article.get('providerPublishTime', article.get('publishedAt', ''))
                        summary = article.get('summary', article.get('description', ''))
                        thumbnail = article.get('thumbnail', {})

                        # Format timestamp
                        time_str = ''
                        if isinstance(pub_time, (int, float)):
                            from datetime import datetime
                            try:
                                time_str = datetime.fromtimestamp(pub_time).strftime('%Y-%m-%d %H:%M')
                            except Exception:
                                time_str = str(pub_time)
                        elif pub_time:
                            time_str = str(pub_time)

                        # Sentiment color based on keywords
                        title_lower = title.lower() if title else ''
                        if any(w in title_lower for w in ['naik', 'untung', 'positif', 'growth', 'profit', 'rise', 'gain', 'surge', 'bullish', 'up']):
                            sentiment_badge = '<span style="background:#10b981;color:white;padding:2px 8px;border-radius:6px;font-size:0.7rem;font-weight:600;">POSITIF</span>'
                        elif any(w in title_lower for w in ['turun', 'rugi', 'negatif', 'loss', 'drop', 'fall', 'decline', 'bearish', 'down', 'crash']):
                            sentiment_badge = '<span style="background:#ef4444;color:white;padding:2px 8px;border-radius:6px;font-size:0.7rem;font-weight:600;">NEGATIF</span>'
                        else:
                            sentiment_badge = '<span style="background:#64748b;color:white;padding:2px 8px;border-radius:6px;font-size:0.7rem;font-weight:600;">NETRAL</span>'

                        st.markdown(f"""
                        <div style="background:rgba(26,31,54,0.6);border:1px solid rgba(139,92,246,0.15);
                            border-radius:12px;padding:1rem 1.2rem;margin-bottom:0.8rem;">
                            <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:0.5rem;">
                                <a href="{link}" target="_blank" style="color:#f1f5f9;text-decoration:none;font-weight:600;font-size:0.95rem;line-height:1.4;">
                                    {title}
                                </a>
                                {sentiment_badge}
                            </div>
                            <div style="color:#64748b;font-size:0.78rem;margin-top:0.4rem;">
                                {publisher} &bull; {time_str}
                            </div>
                            {"<p style='color:#94a3b8;font-size:0.85rem;margin-top:0.5rem;line-height:1.5;'>" + summary[:200] + "...</p>" if summary else ""}
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("Tidak ada berita terkini dari Yahoo Finance untuk emiten ini.")

        # ---- SUB-TAB 6: COMPANY PROFILE ----
        with yf_tab6:
            st.markdown('<div class="section-title">🏢 Profil Perusahaan</div>', unsafe_allow_html=True)

            if info:
                profile_items = {
                    'Nama Lengkap': info.get('longName', info.get('shortName', 'N/A')),
                    'Sektor': info.get('sector', 'N/A'),
                    'Industri': info.get('industry', 'N/A'),
                    'Negara': info.get('country', 'N/A'),
                    'Kota': info.get('city', 'N/A'),
                    'Alamat': info.get('address1', 'N/A'),
                    'Website': info.get('website', 'N/A'),
                    'Telepon': info.get('phone', 'N/A'),
                    'Jumlah Karyawan': f"{info.get('fullTimeEmployees', 'N/A'):,}" if isinstance(info.get('fullTimeEmployees'), (int, float)) else 'N/A',
                    'Tipe Kuotasi': info.get('quoteType', 'N/A'),
                    'Mata Uang': info.get('currency', 'N/A'),
                    'Bursa': info.get('exchange', 'N/A'),
                }

                prof_col1, prof_col2 = st.columns(2)
                prof_keys = list(profile_items.keys())
                mid = len(prof_keys) // 2

                with prof_col1:
                    for k in prof_keys[:mid]:
                        v = profile_items[k]
                        if k == 'Website' and v != 'N/A':
                            st.markdown(f"**{k}:** [{v}]({v})")
                        else:
                            st.markdown(f"**{k}:** {v}")

                with prof_col2:
                    for k in prof_keys[mid:]:
                        v = profile_items[k]
                        st.markdown(f"**{k}:** {v}")

                # Business Summary
                biz_summary = info.get('longBusinessSummary', '')
                if biz_summary:
                    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
                    st.markdown("**Deskripsi Bisnis:**")
                    st.markdown(f"""
                    <div class="info-box" style="max-height:300px;overflow-y:auto;">
                        {biz_summary}
                    </div>
                    """, unsafe_allow_html=True)

                # Officers/Management
                officers = info.get('companyOfficers', [])
                if officers:
                    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
                    st.markdown("**Manajemen Perusahaan:**")
                    officer_data = []
                    for off in officers[:10]:
                        officer_data.append({
                            'Nama': off.get('name', 'N/A'),
                            'Jabatan': off.get('title', 'N/A'),
                            'Umur': off.get('age', 'N/A'),
                            'Kompensasi': format_angka(off.get('totalPay', 0)) if off.get('totalPay') else 'N/A',
                        })
                    st.dataframe(pd.DataFrame(officer_data), use_container_width=True, hide_index=True)
            else:
                st.warning("Data profil perusahaan tidak tersedia.")

        # ---- SUB-TAB 7: ANALYST RECOMMENDATIONS ----
        with yf_tab7:
            st.markdown('<div class="section-title">🎯 Rekomendasi Analis</div>', unsafe_allow_html=True)

            recs = yfd.get('recommendations')
            if recs is not None and not recs.empty:
                st.dataframe(recs.tail(20).sort_index(ascending=False), use_container_width=True, height=400)

                # Recommendation distribution chart
                try:
                    if 'To Grade' in recs.columns:
                        grade_col = 'To Grade'
                    elif 'period' in recs.columns:
                        grade_col = None  # Different format
                    else:
                        grade_col = recs.columns[-1] if len(recs.columns) > 0 else None

                    if grade_col and grade_col in recs.columns:
                        grade_counts = recs[grade_col].value_counts().head(8)

                        grade_colors = {
                            'Buy': '#10b981', 'Strong Buy': '#059669',
                            'Outperform': '#34d399', 'Overweight': '#6ee7b7',
                            'Hold': '#f59e0b', 'Neutral': '#fbbf24', 'Market Perform': '#fcd34d',
                            'Sell': '#ef4444', 'Underperform': '#f87171', 'Underweight': '#fca5a5',
                        }
                        bar_colors = [grade_colors.get(g, '#8b5cf6') for g in grade_counts.index]

                        fig_rec = go.Figure(data=[go.Bar(
                            x=grade_counts.index.tolist(),
                            y=grade_counts.values.tolist(),
                            marker=dict(color=bar_colors, line=dict(width=0)),
                            hovertemplate='%{x}: %{y} analis<extra></extra>'
                        )])
                        fig_rec.update_layout(**PLOTLY_LAYOUT)
                        fig_rec.update_layout(
                            title=dict(text="Distribusi Rekomendasi Analis", font=dict(size=14, color='#f1f5f9')),
                            height=350,
                            xaxis=dict(title="Rekomendasi"),
                            yaxis=dict(title="Jumlah")
                        )
                        st.plotly_chart(fig_rec, use_container_width=True)
                except Exception:
                    pass

                # Summary stats
                if info:
                    rec_summary = {
                        'Target Harga Rata-rata': f"Rp {info.get('targetMeanPrice', 0):,.0f}" if info.get('targetMeanPrice') else 'N/A',
                        'Target Harga Tertinggi': f"Rp {info.get('targetHighPrice', 0):,.0f}" if info.get('targetHighPrice') else 'N/A',
                        'Target Harga Terendah': f"Rp {info.get('targetLowPrice', 0):,.0f}" if info.get('targetLowPrice') else 'N/A',
                        'Target Harga Median': f"Rp {info.get('targetMedianPrice', 0):,.0f}" if info.get('targetMedianPrice') else 'N/A',
                        'Jumlah Analis': str(info.get('numberOfAnalystOpinions', 'N/A')),
                        'Rekomendasi Rata-rata': info.get('recommendationKey', 'N/A'),
                    }
                    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
                    st.markdown("**Target Harga Analis:**")
                    render_metric_cards([
                        {"icon": "🎯", "value": rec_summary['Target Harga Rata-rata'], "label": "Target Mean"},
                        {"icon": "📈", "value": rec_summary['Target Harga Tertinggi'], "label": "Target High"},
                        {"icon": "📉", "value": rec_summary['Target Harga Terendah'], "label": "Target Low"},
                        {"icon": "👥", "value": rec_summary['Jumlah Analis'], "label": "Jumlah Analis"},
                    ])
            else:
                st.info("Data rekomendasi analis tidak tersedia untuk emiten ini.")


# =============================================
# TAB 6: EKSPOR PDF
# =============================================
with tab6:
    st.markdown('<div class="section-title">📄 Ekspor Laporan PDF</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box">
        Generate laporan PDF otomatis lengkap dengan tabel pemegang saham, grafik komposisi, dan data pasar.
        File siap digunakan sebagai lampiran skripsi.
    </div>
    """, unsafe_allow_html=True)

    kode_pdf = st.selectbox("Pilih Kode Emiten", daftar_kode, key="pdf_select")
    include_harga = st.checkbox("Sertakan data harga pasar (yfinance)", value=False, key="pdf_harga")

    if st.button("📄 Generate Laporan PDF", key="btn_pdf"):
        try:
            from pdf_report import buat_laporan_pdf

            info_harga = None
            if include_harga:
                try:
                    from stock_data import ambil_data_saham
                    with st.spinner("Mengambil data pasar..."):
                        info_harga = ambil_data_saham(kode_pdf)
                except ImportError:
                    st.warning("yfinance tidak tersedia, PDF dibuat tanpa data pasar.")

            with st.spinner("Membuat laporan PDF..."):
                output_path = buat_laporan_pdf(df, kode_pdf, info_harga=info_harga)

            if output_path and os.path.exists(output_path):
                st.success(f"✓ Laporan berhasil dibuat: {output_path}")
                with open(output_path, 'rb') as pdf_file:
                    st.download_button(
                        label="⬇️ Download Laporan PDF",
                        data=pdf_file.read(),
                        file_name=os.path.basename(output_path),
                        mime='application/pdf'
                    )
            else:
                st.error("Gagal membuat laporan PDF.")
        except ImportError:
            st.error("Modul `fpdf2` atau `matplotlib` belum terinstall. Jalankan: `pip install fpdf2 matplotlib`")
        except Exception as e:
            st.error(f"Error: {e}")


# =============================================
# FOOTER
# =============================================
st.markdown("""
<div style="text-align: center; padding: 2rem 0 1rem; margin-top: 2rem; border-top: 1px solid rgba(139,92,246,0.1);">
    <p style="color: #64748b; font-size: 0.8rem; margin: 0;">
        bosssmuda &nbsp;•&nbsp; Built with Python, Streamlit & Plotly
    </p>
    <p style="color: #475569; font-size: 0.7rem; margin-top: 0.3rem;">
        Data bersumber dari KSEI melalui file Excel/CSV yang diunggah
    </p>
</div>
""", unsafe_allow_html=True)
