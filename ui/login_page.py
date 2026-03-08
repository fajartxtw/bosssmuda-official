"""
Login page UI for bosssmuda dashboard.
"""
import streamlit as st
import streamlit.components.v1 as components
from core.auth import check_login


def show_login_page():
    """Tampilkan halaman login split-screen."""

    # Hide all Streamlit chrome
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;700;900&display=swap');

    #MainMenu, footer, header, [data-testid="stHeader"] { display: none !important; }
    .stDeployButton { display: none; }
    [data-testid="stSidebar"] { display: none !important; }
    .stApp > header { display: none !important; }
    section[data-testid="stMain"] > div { padding: 0 !important; }
    .block-container { padding: 0 !important; max-width: 100% !important; }
    [data-testid="stAppViewContainer"] { background: white !important; }
    [data-testid="stAppViewContainer"] [data-testid="stVerticalBlockBorderWrapper"] { background: white !important; }
    iframe { border: none !important; }

    /* Force right column white background */
    [data-testid="stAppViewContainer"] [data-testid="stHorizontalBlock"] > div:nth-child(2) {
        background: white !important;
    }

    /* Right column form styling - force all text colors for dark theme */
    .login-form-wrap {
        max-width: 380px;
        margin: 0 auto;
        padding: 2rem 0.5rem;
        font-family: 'Manrope', sans-serif;
    }
    .login-form-wrap h2 {
        font-family: 'Manrope', sans-serif;
        font-size: 2.2rem; font-weight: 900;
        color: #0f172a !important; margin-bottom: 0.2rem;
        letter-spacing: -0.03em;
    }
    .login-form-wrap .sub {
        font-size: 0.9rem; color: #64748b !important; margin-bottom: 1.5rem;
    }
    .login-form-wrap .footer-text {
        text-align: center; font-size: 0.78rem; color: #94a3b8 !important;
        margin-top: 2rem; letter-spacing: 0.03em;
        font-family: 'Manrope', sans-serif;
    }

    /* Override ALL Streamlit dark theme text in login area */
    .login-form-wrap, .login-form-wrap * {
        color: #0f172a !important;
    }
    .login-form-wrap .sub { color: #64748b !important; }
    .login-form-wrap .footer-text { color: #94a3b8 !important; }

    /* Streamlit form border override */
    .login-form-wrap [data-testid="stForm"] {
        background: white !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
    }

    /* Streamlit input styling */
    .login-form-wrap [data-testid="stTextInput"] > label {
        font-family: 'Manrope', sans-serif !important;
        font-weight: 600 !important; font-size: 0.82rem !important;
        color: #334155 !important;
    }
    .login-form-wrap [data-testid="stTextInput"] > div > div > input {
        background: #f8fafc !important;
        border: 1.5px solid #e2e8f0 !important;
        border-radius: 10px !important;
        color: #0f172a !important;
        font-family: 'Manrope', sans-serif !important;
        padding: 0.7rem 1rem !important;
        height: 48px !important; font-size: 0.9rem !important;
    }
    .login-form-wrap [data-testid="stTextInput"] > div > div > input:focus {
        border-color: #4211d4 !important;
        box-shadow: 0 0 0 3px rgba(66,17,212,0.12) !important;
    }
    .login-form-wrap [data-testid="stTextInput"] > div > div > input::placeholder {
        color: #94a3b8 !important;
    }

    /* Submit button */
    .login-form-wrap [data-testid="stFormSubmitButton"] > button {
        background: #4211d4 !important; color: white !important;
        border: none !important; border-radius: 10px !important;
        height: 48px !important; font-size: 0.95rem !important;
        font-weight: 700 !important;
        font-family: 'Manrope', sans-serif !important;
        box-shadow: 0 4px 14px rgba(66,17,212,0.25) !important;
        transition: all 0.2s !important;
    }
    .login-form-wrap [data-testid="stFormSubmitButton"] > button:hover {
        background: #3610b0 !important;
        box-shadow: 0 6px 20px rgba(66,17,212,0.35) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Split layout using st.columns
    left_col, right_col = st.columns([1, 1], gap="small")

    with left_col:
        # Decorative left panel (iframe, no interactivity needed)
        left_html = """
        <html><head>
        <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;700;900&display=swap" rel="stylesheet"/>
        <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: 'Manrope', sans-serif; height: 100vh; }
        .left {
            height: 100vh; display: flex; flex-direction: column; justify-content: space-between;
            background: #0d0820;
            background-image:
                radial-gradient(ellipse at 50% 30%, rgba(66,17,212,0.30) 0%, transparent 60%),
                radial-gradient(ellipse at 80% 70%, rgba(99,50,230,0.20) 0%, transparent 50%),
                radial-gradient(ellipse at 20% 80%, rgba(139,92,246,0.12) 0%, transparent 50%);
            position: relative; overflow: hidden; padding: 2rem;
        }
        .left::before {
            content: ''; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
            width: 500px; height: 500px;
            background: radial-gradient(circle, rgba(66,17,212,0.15) 0%, transparent 70%);
            border-radius: 50%; filter: blur(80px);
        }
        .geo-deco {
            position: absolute; top: 50%; left: 50%; transform: translate(-50%, -55%);
            width: 320px; height: 320px; opacity: 0.6;
        }
        .brand { position: relative; z-index: 2; display: flex; align-items: center; gap: 0.6rem; }
        .brand svg { width: 26px; height: 26px; color: #7c3aed; }
        .brand span { font-size: 1.1rem; font-weight: 700; color: white; }
        .quote-card {
            position: relative; z-index: 2; max-width: 400px;
            background: rgba(0,0,0,0.45); backdrop-filter: blur(16px);
            border: 1px solid rgba(255,255,255,0.08); border-radius: 16px;
            padding: 2rem; box-shadow: 0 20px 60px rgba(0,0,0,0.5); margin-bottom: 2rem;
        }
        .quote-card h1 { font-size: 2.5rem; font-weight: 900; color: white; line-height: 1.1; margin-bottom: 1rem; }
        .quote-card p { font-size: 0.92rem; color: #c0b8d8; line-height: 1.65; }
        .quote-card .author { font-weight: 700; color: #a78bfa; margin-top: 0.6rem; display: inline-block; }
        </style></head><body>
        <div class="left">
            <div class="brand">
                <svg fill="none" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
                    <path d="M13.8 30.6C16.7 29.9 20.2 29.5 24 29.5C27.8 29.5 31.3 29.9 34.2 30.6C36.9 31.2 40 32.8 41.4 33.8L24.8 7.4C24.5 6.7 23.5 6.7 23.2 7.4L6.6 33.8C8 32.8 11.1 31.2 13.8 30.6Z" fill="currentColor"/>
                    <path d="M40 35.8C40 35.7 40 35.7 40 35.7C38.5 34.3 36 33.1 33.7 32.5C31 31.9 27.6 31.5 24 31.5C20.4 31.5 17 31.9 14.3 32.5C12 33.1 9.4 34.3 8.2 35.2C8.2 35.2 8 35.6 8 35.7C8 35.8 8 36.1 8.7 36.6C9.3 37.2 10.4 37.8 11.9 38.3C14.9 39.3 19.2 40 24 40C28.8 40 33.1 39.3 36.1 38.3C37.6 37.8 38.7 37.2 39.3 36.6C39.9 36.1 40 35.9 40 35.8Z" fill="currentColor"/>
                </svg>
                <span>bo$$$muda</span>
            </div>
            <svg class="geo-deco" viewBox="0 0 400 400" fill="none" xmlns="http://www.w3.org/2000/svg">
                <polygon points="200,40 340,110 340,250 200,320 60,250 60,110" stroke="rgba(124,58,237,0.3)" stroke-width="1.5" fill="none">
                    <animateTransform attributeName="transform" type="rotate" values="0 200 200;360 200 200" dur="60s" repeatCount="indefinite"/>
                </polygon>
                <polygon points="200,80 300,130 300,230 200,280 100,230 100,130" stroke="rgba(124,58,237,0.2)" stroke-width="1" fill="rgba(66,17,212,0.05)">
                    <animateTransform attributeName="transform" type="rotate" values="360 200 200;0 200 200" dur="45s" repeatCount="indefinite"/>
                </polygon>
                <circle cx="200" cy="180" r="60" fill="rgba(66,17,212,0.08)"/>
                <line x1="60" y1="300" x2="120" y2="260" stroke="rgba(167,139,250,0.3)" stroke-width="1"/>
                <line x1="120" y1="260" x2="180" y2="290" stroke="rgba(167,139,250,0.3)" stroke-width="1"/>
                <line x1="180" y1="290" x2="240" y2="230" stroke="rgba(167,139,250,0.4)" stroke-width="1"/>
                <line x1="240" y1="230" x2="300" y2="250" stroke="rgba(167,139,250,0.3)" stroke-width="1"/>
                <line x1="300" y1="250" x2="360" y2="200" stroke="rgba(167,139,250,0.2)" stroke-width="1"/>
                <circle cx="60" cy="300" r="3" fill="#a78bfa" opacity="0.5"/>
                <circle cx="120" cy="260" r="3" fill="#a78bfa" opacity="0.6"/>
                <circle cx="180" cy="290" r="3" fill="#a78bfa" opacity="0.5"/>
                <circle cx="240" cy="230" r="4" fill="#a78bfa" opacity="0.8"/>
                <circle cx="300" cy="250" r="3" fill="#a78bfa" opacity="0.5"/>
                <circle cx="360" cy="200" r="3" fill="#a78bfa" opacity="0.4"/>
            </svg>
            <div class="quote-card">
                <h1>Master the<br/>Markets.</h1>
                <p>"The stock market is a device for transferring money from the impatient to the patient."<br/>
                <span class="author">— Warren Buffett</span></p>
            </div>
        </div>
        </body></html>
        """
        components.html(left_html, height=650, scrolling=False)

    with right_col:
        # Native Streamlit form (works without iframe restrictions)
        st.markdown('<div class="login-form-wrap">', unsafe_allow_html=True)
        st.markdown('<h2>Welcome Back</h2>', unsafe_allow_html=True)
        st.markdown('<p class="sub">Silakan masukkan detail Anda untuk login.</p>', unsafe_allow_html=True)

        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("Username", placeholder="Masukkan username...")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            submitted = st.form_submit_button("Log In", use_container_width=True)

            if submitted:
                if username and password:
                    if check_login(username, password):
                        st.session_state['authenticated'] = True
                        st.session_state['username'] = username
                        st.rerun()
                    else:
                        st.error("❌ Username atau password salah!")
                else:
                    st.warning("Silakan isi username dan password.")

        st.markdown('<p class="footer-text">bo$$$muda &bull; Akses terbatas</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
