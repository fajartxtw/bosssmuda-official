"""
🚀 bosssmuda — Dashboard Kepemilikan Saham IDX
================================================
Entry point utama (modular).
Jalankan: streamlit run app.py
"""

import streamlit as st

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
# IMPORTS
# =============================================
from ui.login_page import show_login_page
from ui.landing_page import show_landing_page
from ui.styles import inject_dashboard_css
from ui.components import render_metric_cards, render_sidebar
from core.data_loader import muat_data, format_angka
from views.tab_emiten import render_tab_emiten
from views.tab_investor import render_tab_investor
from views.tab_ranking import render_tab_ranking
from views.tab_network import render_tab_network
from views.tab_market import render_tab_market
from views.tab_export import render_tab_export

# =============================================
# AUTH GATE: Landing → Login → Dashboard
# =============================================
if not st.session_state.get('authenticated', False):
    if st.session_state.get('show_login', False):
        show_login_page()
    else:
        show_landing_page()
    st.stop()

# =============================================
# DASHBOARD (authenticated users only)
# =============================================

# Inject CSS
inject_dashboard_css()

import os

# Sidebar
selected_page = render_sidebar()

# Header removed per user request


# Hardcoded data path
file_path = "data/Data.xlsx"
if not os.path.exists(file_path):
    file_path = "Data.xlsx"

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
# PAGE CONTENT (from Sidebar Navigation)
# =============================================
daftar_kode = sorted(df['KODE'].unique().tolist()) if 'KODE' in df.columns else []

if selected_page == "🔍 Stock Screener":
    render_tab_emiten(df, daftar_kode)
elif selected_page == "👤 Investor Screener":
    render_tab_investor(df)
elif selected_page == "🏆 Rankings":
    render_tab_ranking(df)
elif selected_page == "🕸️ Network Graph":
    render_tab_network(df, daftar_kode)
elif selected_page == "📈 Market Data":
    render_tab_market(df, daftar_kode)
elif selected_page == "📊 Statistik & Event":
    from views.tab_statistik import render_tab_statistik
    render_tab_statistik()
elif selected_page == "📰 Berita Pasar":
    from views.tab_news import render_tab_news
    render_tab_news()
elif selected_page == "📄 PDF Export":
    render_tab_export(df, daftar_kode)

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
