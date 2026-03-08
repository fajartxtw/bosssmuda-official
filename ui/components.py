"""
Reusable UI components for bosssmuda dashboard.
"""
import streamlit as st
import os
import tempfile


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


def render_sidebar():
    """Render the dashboard sidebar with branding, file picker, and user info."""
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

        st.markdown('<div class="sidebar-nav-container">', unsafe_allow_html=True)
        selected_page = st.radio(
            "Navigation",
            options=[
                "🔍 Stock Screener",
                "👤 Investor Screener",
                "🏆 Rankings",
                "🕸️ Network Graph",
                "📈 Market Data",
                "📊 Statistik & Event",
                "📰 Berita Pasar",
                "📄 PDF Export"
            ],
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        


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

    return selected_page
