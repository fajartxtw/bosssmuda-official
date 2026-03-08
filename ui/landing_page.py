"""
Landing page UI for bosssmuda dashboard.
"""
import streamlit as st
import streamlit.components.v1 as components


def show_landing_page():
    """Tampilkan landing page yang estetik sebelum login."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/icon?family=Material+Icons');

    [data-testid="stAppViewContainer"] {
        background: #f8f9fa !important;
    }

    #MainMenu, footer, header { visibility: hidden; }
    .stDeployButton { display: none; }
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="stHeader"] { display: none !important; }

    .landing-root * { box-sizing: border-box; }
    .landing-root {
        font-family: 'Inter', sans-serif;
        color: #1a1a2e;
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 1.5rem;
    }

    /* ===== RESPONSIVE ===== */
    @media (max-width: 768px) {
        .lp-features { grid-template-columns: 1fr; }
        .lp-highlight { flex-direction: column; }
        .lp-subcards { grid-template-columns: 1fr; }
        .lp-pricing { grid-template-columns: 1fr; }
        .lp-stats { grid-template-columns: repeat(2, 1fr); }
        .lp-nav-links { display: none; }
    }
    </style>
    """, unsafe_allow_html=True)

    # --- NATIVE STREAMLIT NAVBAR ---
    st.markdown("""
    <style>
    div[data-testid="stHorizontalBlock"]:first-of-type {
        background: #f8f9fa; padding: 0.8rem 1.5rem; margin: -1rem -1rem 0;
        border-bottom: 1px solid #e2e8f0;
    }
    .lp-brand-text {
        font-family: 'Inter', sans-serif; font-weight: 800; font-size: 1.2rem;
        color: #1a1a2e; letter-spacing: -0.02em; padding-top: 0.4rem;
    }
    .lp-nav-text {
        font-family: 'Inter', sans-serif; font-size: 0.85rem; font-weight: 500;
        color: #4a5568; padding-top: 0.5rem;
    }
    /* Style the Login button */
    div[data-testid="stHorizontalBlock"]:first-of-type button[kind="secondary"] {
        background: #3f1b63 !important; color: white !important;
        border: none !important; border-radius: 9999px !important;
        padding: 0.4rem 1.5rem !important; font-weight: 600 !important;
        box-shadow: 0 3px 10px rgba(63,27,99,0.25) !important;
    }
    div[data-testid="stHorizontalBlock"]:first-of-type button[kind="secondary"]:hover {
        opacity: 0.88 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    nav_c1, nav_c2, nav_c3 = st.columns([2, 5, 1])
    with nav_c1:
        st.markdown('<div class="lp-brand-text">📈 bo$$$muda</div>', unsafe_allow_html=True)
    with nav_c2:
        st.markdown('<div class="lp-nav-text">Fitur &nbsp;&bull;&nbsp; Harga &nbsp;&bull;&nbsp; Tentang</div>', unsafe_allow_html=True)
    with nav_c3:
        if st.button("Login", key="btn_nav_login", use_container_width=True):
            st.session_state['show_login'] = True
            st.rerun()

    # Hero section via components.html (bypasses Streamlit sanitization)
    hero_html = """
    <html><head>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet"/>
    <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Inter', sans-serif; color: #1a1a2e; background: #f8f9fa; }
    .root { max-width: 1100px; margin: 0 auto; padding: 0 1.5rem; }
    .hero { text-align: center; padding: 4rem 0 3rem; position: relative; overflow: hidden; }
    .hero::before { content: ''; position: absolute; top: -5rem; right: -5rem; width: 24rem; height: 24rem; background: rgba(110,69,180,0.08); border-radius: 50%; filter: blur(80px); pointer-events: none; }
    .hero::after { content: ''; position: absolute; bottom: -5rem; left: -5rem; width: 20rem; height: 20rem; background: rgba(139,92,246,0.06); border-radius: 50%; filter: blur(80px); pointer-events: none; }
    .hero h1 { font-size: clamp(2.5rem, 5vw, 4rem); font-weight: 800; line-height: 1.1; margin-bottom: 1.2rem; letter-spacing: -0.03em; }
    .hero h1 .gradient { background: linear-gradient(135deg, #3f1b63, #805ad5); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .hero p { font-size: 1.1rem; color: #64748b; max-width: 560px; margin: 0 auto 2rem; line-height: 1.6; }
    .stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 2rem; margin-top: 2rem; padding-top: 2rem; border-top: 1px solid #e2e8f0; }
    .stats .val { font-size: 2rem; font-weight: 800; margin-bottom: 0.2rem; }
    .stats .lbl { font-size: 0.78rem; color: #94a3b8; }
    @media (max-width: 768px) { .stats { grid-template-columns: repeat(2, 1fr); } }
    </style></head><body>
    <div class="root">
    <section class="hero">
        <h1>Analisis Mendalam<br/><span class="gradient">Data Keuangan Indonesia</span></h1>
        <p>Platform screening saham canggih dengan data real-time, visualisasi network graph, laporan keuangan, dan analisis kepemilikan saham di Bursa Efek Indonesia.</p>
        <div class="stats">
            <div><div class="val">955+</div><div class="lbl">Emiten Tercatat</div></div>
            <div><div class="val">4,964+</div><div class="lbl">Investor Terdaftar</div></div>
            <div><div class="val">7,238+</div><div class="lbl">Records Data</div></div>
            <div><div class="val">99.9%</div><div class="lbl">Uptime</div></div>
        </div>
    </section>
    </div>
    </body></html>
    """
    components.html(hero_html, height=450, scrolling=False)

    # Streamlit button (must be outside iframe for interactivity)
    col_hero1, col_hero2, col_hero3 = st.columns([2, 1, 2])
    with col_hero2:
        if st.button("🚀 Mulai Screening", key="btn_landing_start", use_container_width=True):
            st.session_state['show_login'] = True
            st.rerun()

    # Features section - use components.html to avoid Streamlit HTML sanitization
    features_html = """
    <html>
    <head>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet"/>
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet"/>
    <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Inter', sans-serif; color: #1a1a2e; background: #f8f9fa; }
    .root { max-width: 1100px; margin: 0 auto; padding: 0 1.5rem; }

    .section-bg { background: white; border-radius: 2rem; padding: 3.5rem 2.5rem; margin: 1rem 0 2rem; }
    .badge {
        display: inline-block; font-size: 0.7rem; font-weight: 700; letter-spacing: 0.08em;
        text-transform: uppercase; color: #3f1b63; background: #e9d8fd; padding: 0.3rem 0.8rem;
        border-radius: 9999px; margin-bottom: 1rem;
    }
    h2 { font-size: 2rem; font-weight: 800; margin-bottom: 0.6rem; }
    .subtitle { color: #64748b; max-width: 550px; margin: 0 auto 2.5rem; font-size: 0.9rem; }
    .features { display: grid; grid-template-columns: repeat(3,1fr); gap: 1.2rem; }
    .card { background: #f8f9fa; padding: 1.8rem; border-radius: 1.2rem; border: 1px solid #f0f0f5; transition: all 0.3s; }
    .card:hover { box-shadow: 0 8px 25px rgba(0,0,0,0.06); transform: translateY(-2px); }
    .card-icon { width: 44px; height: 44px; background: white; border-radius: 0.7rem; display: flex; align-items: center; justify-content: center; margin-bottom: 1rem; box-shadow: 0 2px 6px rgba(0,0,0,0.04); }
    .card-icon .material-icons { color: #3f1b63; font-size: 1.3rem; }
    .card h3 { font-size: 1.05rem; font-weight: 700; margin-bottom: 0.5rem; }
    .card p { font-size: 0.82rem; color: #64748b; line-height: 1.6; }

    .highlight { background: #3f1b63; color: white; border-radius: 1.5rem; padding: 2.5rem; display: flex; align-items: center; gap: 2.5rem; overflow: hidden; position: relative; margin: 2rem 0 1.5rem; }
    .highlight::after { content: ''; position: absolute; top: -3rem; right: -3rem; width: 14rem; height: 14rem; background: rgba(128,90,213,0.3); border-radius: 50%; filter: blur(60px); }
    .highlight-text { flex: 1; z-index: 1; }
    .highlight h3 { font-size: 1.6rem; font-weight: 800; margin-bottom: 0.8rem; }
    .highlight p { color: #d6bcfa; margin-bottom: 1.2rem; line-height: 1.6; font-size: 0.9rem; }
    .btn-white { background: white; color: #3f1b63; padding: 0.6rem 1.3rem; border-radius: 9999px; font-weight: 600; font-size: 0.85rem; text-decoration: none; display: inline-block; }
    .chart-mock { flex: 1; height: 180px; background: rgba(255,255,255,0.1); border-radius: 1rem; border: 1px solid rgba(255,255,255,0.2); display: flex; align-items: flex-end; gap: 6px; padding: 1rem; z-index: 1; position: relative; }
    .bar { border-radius: 3px 3px 0 0; flex: 1; }
    .bar.g { background: rgba(72,187,120,0.8); }
    .bar.r { background: rgba(245,101,101,0.8); }

    .subcards { display: grid; grid-template-columns: 1fr 1fr; gap: 1.2rem; }
    .subcard { background: white; border: 1px solid #e2e8f0; border-radius: 1.5rem; padding: 1.8rem; display: flex; flex-direction: column; }
    .subcard.lav { background: #e9d8fd; border-color: #d6bcfa; }
    .subcard h3 { font-size: 1.2rem; font-weight: 700; margin-bottom: 0.3rem; }
    .subcard > p { font-size: 0.82rem; color: #64748b; margin-bottom: 1.2rem; }
    .mock-table { background: #f8f9fa; border-radius: 0.7rem; border: 1px solid #f0f0f5; overflow: hidden; margin-top: auto; }
    .mock-row { display: flex; padding: 0.6rem 0.8rem; font-size: 0.82rem; border-bottom: 1px solid #f0f0f5; }
    .mock-row:last-child { border-bottom: none; }
    .mock-row.hdr { font-weight: 600; font-size: 0.7rem; color: #94a3b8; }
    .mock-row > div { flex: 1; }
    .mock-row > div:not(:first-child) { text-align: right; }
    .green { color: #48bb78; } .red { color: #f56565; } .ticker { font-weight: 700; }

    .alert-item { background: white; padding: 0.9rem; border-radius: 0.7rem; display: flex; align-items: center; gap: 0.8rem; box-shadow: 0 2px 6px rgba(0,0,0,0.04); margin-bottom: 0.6rem; }
    .alert-icon { width: 34px; height: 34px; border-radius: 0.4rem; display: flex; align-items: center; justify-content: center; }
    .alert-icon.gbg { background: #c6f6d5; } .alert-icon.bbg { background: #bee3f8; }
    .alert-icon.gbg .material-icons { color: #38a169; font-size: 0.9rem; }
    .alert-icon.bbg .material-icons { color: #3182ce; font-size: 0.9rem; }
    .alert-title { font-size: 0.82rem; font-weight: 700; } .alert-desc { font-size: 0.72rem; color: #94a3b8; }

    .pricing { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; max-width: 750px; margin: 0 auto; }
    .price-card { background: white; border: 1px solid #e2e8f0; border-radius: 1.5rem; padding: 2.2rem; display: flex; flex-direction: column; }
    .price-card.pro { background: #3f1b63; color: white; border: none; position: relative; overflow: hidden; box-shadow: 0 12px 35px rgba(63,27,99,0.25); }
    .price-card.pro .pop { position: absolute; top: 0; right: 0; background: #805ad5; color: white; font-size: 0.6rem; font-weight: 700; padding: 0.25rem 0.7rem; border-radius: 0 0 0 0.5rem; }
    .price-card h3 { font-size: 1.3rem; font-weight: 700; margin-bottom: 0.2rem; }
    .price-card .desc { font-size: 0.82rem; color: #94a3b8; margin-bottom: 1.2rem; }
    .price-card.pro .desc { color: #d6bcfa; }
    .price-card .price { font-size: 2.2rem; font-weight: 800; margin-bottom: 1.2rem; }
    .price-card .price span { font-size: 0.9rem; font-weight: 400; color: #94a3b8; }
    .price-card.pro .price span { color: #d6bcfa; }
    .price-card ul { list-style: none; padding: 0; margin: 0 0 1.5rem; flex-grow: 1; }
    .price-card ul li { display: flex; align-items: center; gap: 0.6rem; font-size: 0.82rem; padding: 0.4rem 0; }
    .price-card ul li .material-icons { font-size: 1rem; color: #48bb78; }
    .price-card.pro ul li .material-icons { color: #d6bcfa; }
    .price-btn { display: block; text-align: center; padding: 0.7rem; border-radius: 9999px; font-weight: 600; font-size: 0.85rem; text-decoration: none; }
    .price-btn.basic { background: #f0f0f5; color: #1a1a2e; } .price-btn.pro { background: white; color: #3f1b63; }

    .lp-footer { border-top: 1px solid #e2e8f0; padding: 2.5rem 0 1.5rem; display: flex; flex-direction: column; align-items: center; gap: 1rem; margin-top: 2rem; }
    .lp-footer-links { display: flex; gap: 1.5rem; } .lp-footer-links a { font-size: 0.82rem; color: #94a3b8; text-decoration: none; } .lp-footer-links a:hover { color: #3f1b63; }
    .lp-footer-copy { font-size: 0.7rem; color: #cbd5e0; }

    @media (max-width: 768px) { .features,.subcards,.pricing { grid-template-columns: 1fr; } .highlight { flex-direction: column; } }
    </style>
    </head>
    <body>
    <div class="root">

    <div class="section-bg">
        <div style="text-align:center"><span class="badge">Keunggulan</span>
        <h2>Alat Analisis Strategis Anda</h2>
        <p class="subtitle">Kami menyediakan semua alat yang diperlukan untuk menganalisis pasar secara mendalam.</p></div>
        <div class="features">
            <div class="card"><div class="card-icon"><span class="material-icons">speed</span></div><h3>Analisa Statistik</h3><p>Menyediakan tools menghitung event study terhadap efek historis</p></div>
            <div class="card"><div class="card-icon"><span class="material-icons">account_tree</span></div><h3>Network Graph</h3><p>Visualisasi jaring laba-laba interaktif untuk melacak gurita bisnis konglomerat dan hubungan kepemilikan saham.</p></div>
            <div class="card"><div class="card-icon"><span class="material-icons">candlestick_chart</span></div><h3>Analisis Keuangan</h3><p>Laporan keuangan lengkap: income statement, balance sheet, cash flow, key statistics, dan rekomendasi analis.</p></div>
        </div>
    </div>

    <div style="text-align:center;padding:3rem 0 0"><span class="badge">Fitur</span>
    <h2>Alat Powerful yang Anda Butuhkan</h2>
    <p class="subtitle">Dari ringkasan cepat hingga analisis mendalam, platform kami menyesuaikan workflow Anda.</p></div>

    <div class="highlight">
        <div class="highlight-text"><h3>Interactive Charting</h3><p>Visualisasi candlestick, volume, dan indikator teknikal dengan grafik Plotly yang responsif dan bisa di-zoom.</p><a class="btn-white" href="#">Lihat Demo</a></div>
        <div class="chart-mock">
            <div class="bar g" style="height:33%"></div><div class="bar r" style="height:25%"></div><div class="bar g" style="height:50%"></div><div class="bar g" style="height:75%"></div><div class="bar r" style="height:60%"></div><div class="bar g" style="height:90%"></div>
        </div>
    </div>

    <div class="subcards">
        <div class="subcard"><h3>Screening Investor</h3><p>Cari dan analisis portofolio investor besar di BEI.</p>
            <div class="mock-table">
                <div class="mock-row hdr"><div>Kode</div><div>Harga</div><div>Vol</div></div>
                <div class="mock-row"><div class="ticker">BBCA</div><div class="green">9,850</div><div style="color:#94a3b8">54M</div></div>
                <div class="mock-row"><div class="ticker">ADRO</div><div class="red">2,310</div><div style="color:#94a3b8">22M</div></div>
                <div class="mock-row"><div class="ticker">MBMA</div><div class="green">620</div><div style="color:#94a3b8">48M</div></div>
            </div>
        </div>
        <div class="subcard lav"><h3>Smart Alerts</h3><p>Notifikasi instan saat saham memenuhi kriteria Anda.</p>
            <div style="margin-top:auto">
                <div class="alert-item"><div class="alert-icon gbg"><span class="material-icons">notifications_active</span></div><div><div class="alert-title">Volume Breakout</div><div class="alert-desc">ADRO crossed 200% avg vol</div></div></div>
                <div class="alert-item"><div class="alert-icon bbg"><span class="material-icons">trending_up</span></div><div><div class="alert-title">Pemegang Baru</div><div class="alert-desc">BlackRock masuk ke BBCA</div></div></div>
            </div>
        </div>
    </div>

    <div style="text-align:center;padding:4rem 0 0"><span class="badge">Harga</span>
    <h2>Paket Fleksibel untuk Semua Trader</h2>
    <p class="subtitle">Mulai gratis, upgrade ketika Anda butuh lebih banyak fitur.</p></div>

    <div class="pricing">
        <div class="price-card"><h3>Basic</h3><div class="desc">Alat esensial untuk investor santai.</div><div class="price">Gratis</div>
            <ul><li><span class="material-icons">check_circle</span> Data kepemilikan saham</li><li><span class="material-icons">check_circle</span> Screening emiten & investor</li><li><span class="material-icons">check_circle</span> Network graph dasar</li><li><span class="material-icons">check_circle</span> Ekspor PDF</li></ul>
            <a class="price-btn basic" href="#">Mulai Gratis</a>
        </div>
        <div class="price-card pro"><div class="pop">POPULER</div><h3>Pro</h3><div class="desc">Fitur lanjutan untuk data researcher, mahasiswa, dan trader aktif.</div><div class="price">Rp50K<span> / bulan</span></div>
            <ul><li><span class="material-icons">check_circle</span> Data pasar real-time</li><li><span class="material-icons">check_circle</span> Laporan keuangan lengkap</li><li><span class="material-icons">check_circle</span> Rekomendasi analis</li><li><span class="material-icons">check_circle</span> Berita & sentimen pasar</li><li><span class="material-icons">check_circle</span> Profil perusahaan detail</li><li><span class="material-icons">check_circle</span> Akses Beta</li><li><span class="material-icons">check_circle</span> Integrasi AI</li></ul>
            <a class="price-btn pro" href="#">Coba 14 Hari Gratis</a>
        </div>
    </div>

    <footer class="lp-footer">
        <div style="display:flex;align-items:center;gap:0.4rem"><span class="material-icons" style="color:#3f1b63;font-size:1.3rem">ssid_chart</span><span style="font-weight:800;font-size:1rem">bosssmuda</span></div>
        <div class="lp-footer-links"><a href="#">Tentang</a><a href="#">Fitur</a><a href="#">Harga</a><a href="#">Kontak</a></div>
        <div class="lp-footer-copy">&copy; 2026 bosssmuda. All rights reserved.</div>
    </footer>

    </div>
    </body></html>
    """
    components.html(features_html, height=2200, scrolling=False)
