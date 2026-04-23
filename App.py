import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import hashlib
import requests
import json

# ==================== 1. ULTRA-CONTRAST PREMIUM UI ====================
def apply_premium_style():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700;800&display=swap');
    
    /* Global Body & Text Contrast */
    html, body, [class*="css"] { 
        font-family: 'Plus Jakarta Sans', sans-serif; 
        color: #FFFFFF !important; /* Putih murni untuk teks utama */
    }
    
    .stApp { 
        background: radial-gradient(circle at 2% 2%, #1e1b4b 0%, #020617 100%); 
    }

    /* Luxury Card Design */
    .premium-card {
        background: rgba(255, 255, 255, 0.05); 
        backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.2); 
        border-radius: 24px;
        padding: 30px;
        margin-bottom: 25px;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.6);
    }
    
    /* Header Gold */
    .gold-header {
        background: linear-gradient(135deg, #FFD700 0%, #B8860B 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }

    /* Memastikan Semua Label & Teks Input Putih Terang */
    label, .stMarkdown p, .stMarkdown h3, .stMarkdown h2, .stMarkdown h1 {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }

    /* Radio Button Text (Pernah Laku) */
    div[data-testid="stMarkdownContainer"] p {
        color: #FFFFFF !important;
    }
    
    div[class*="stRadio"] label {
        color: #FFFFFF !important;
        font-weight: 500 !important;
    }

    /* Input Field & Placeholder Contrast */
    .stNumberInput input, .stTextInput input, .stSelectbox div {
        background: rgba(0,0,0,0.6) !important; 
        border: 1px solid rgba(255,255,255,0.4) !important; 
        border-radius: 12px !important; 
        color: #FFFFFF !important;
        font-weight: 500;
    }
    
    ::placeholder {
        color: #A0AEC0 !important; /* Placeholder sedikit abu agar beda tapi tetap terbaca */
        opacity: 1;
    }

    /* Premium Button */
    .stButton>button {
        background: linear-gradient(135deg, #00E5A0 0%, #00a878 100%);
        color: #020617 !important; 
        font-weight: 800; 
        border: none; 
        border-radius: 15px;
        padding: 18px; 
        text-transform: uppercase; 
        letter-spacing: 1.5px;
        width: 100%;
    }

    /* Metric Contrast */
    [data-testid="stMetricValue"] {
        color: #FFFFFF !important;
        font-weight: 800 !important;
    }
    [data-testid="stMetricLabel"] {
        color: #E2E8F0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ==================== 2. CORE LOGIC ====================
for key, val in {
    "authenticated": False, "demo_mode": False, "demo_start_time": None,
    "demo_analysis_count": 0, "demo_generator_count": 0, "products": []
}.items():
    if key not in st.session_state: st.session_state[key] = val

ADMIN_USERNAME = "arkidigital"
ADMIN_PASSWORD = "Arkidigital2026"
CHECKOUT_LINK = "https://muhammad-masruri.myscalev.com/checkout-pageku"
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")

def call_gemini(prompt):
    if not GEMINI_API_KEY: return None
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    try:
        r = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=15)
        return r.json()["candidates"][0]["content"]["parts"][0]["text"]
    except: return None

def format_rp(angka):
    if angka >= 1_000_000: return f"Rp{angka/1_000_000:.1f}JT"
    if angka >= 1000: return f"Rp{angka/1000:.0f}RB"
    return f"Rp{angka:,.0f}"

# ==================== 3. LOGIN INTERFACE ====================
def show_login():
    apply_premium_style()
    st.markdown('<div style="text-align:center; padding-top:80px;">', unsafe_allow_html=True)
    st.markdown('<h1 class="gold-header" style="font-size:3.5rem;">🩺 DOCTOR ADS ELITE</h1>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:1.2rem;">Predictive Ad Analytics & AI Strategy Portfolio</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="large")
    with col1:
        with st.form("login"):
            st.markdown("### 🔐 Member Access")
            u = st.text_input("Username", placeholder="Input ID...")
            p = st.text_input("Password", type="password", placeholder="Input Key...")
            if st.form_submit_button("UNLOCK DASHBOARD"):
                if u == ADMIN_USERNAME and p == ADMIN_PASSWORD:
                    st.session_state.authenticated = True; st.rerun()
                else: st.error("Wrong Credentials.")
    with col2:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown("### 🎁 Exclusive Trial")
        st.write("Coba analisis performa iklan Anda selama 5 menit secara gratis.")
        if st.button("START EXPERIENCE"):
            st.session_state.demo_mode = True; st.session_state.demo_start_time = datetime.now(); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ==================== 4. MAIN ELITE DASHBOARD ====================
def main():
    st.set_page_config(page_title="Doctor Ads Elite", page_icon="🩺", layout="wide")
    apply_premium_style()

    if not st.session_state.authenticated and not st.session_state.demo_mode:
        show_login(); st.stop()

    if st.session_state.demo_mode:
        elapsed = (datetime.now() - st.session_state.demo_start_time).total_seconds()
        if elapsed > 300: 
            st.warning("Trial Session Expired!"); 
            st.markdown(f'<a href="{CHECKOUT_LINK}" target="_blank" style="text-decoration:none;"><div class="stButton"><button>💎 GET UNLIMITED ACCESS NOW</button></div></a>', unsafe_allow_html=True)
            st.stop()

    st.markdown('<h1 class="gold-header">🩺 ADVERTISING INTELLIGENCE</h1>', unsafe_allow_html=True)
    
    c_f1, c_f2 = st.columns([2, 1])
    with c_f1:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown("### 🎯 Elite ROAS BEP Calculator")
        col_b1, col_b2, col_b3 = st.columns(3)
        hj = col_b1.number_input("Harga Jual (Rp)", value=150000, step=5000)
        modal = col_b2.number_input("Modal / HPP (Rp)", value=75000, step=5000)
        admin_p = col_b3.slider("Admin Platform %", 5, 30, 20)
        target_p = st.number_input("Target Profit (Rp)", value=0)
        
        laba = hj - modal - (hj * admin_p/100) - target_p
        roas_bep = hj / laba if laba > 0 else 999
        st.markdown(f'<h2 style="color:#00E5A0; text-align:center; font-size:3.5rem; text-shadow: 0 0 15px rgba(0,229,160,0.3);">ROAS BEP: {roas_bep:.2f}x</h2>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c_f2:
        st.markdown('<div class="premium-card" style="height:100%;">', unsafe_allow_html=True)
        st.markdown("### 📋 Kelayakan Iklan")
        pernah = st.radio("Produk Pernah Laku?", ["Ya", "Tidak"], horizontal=True)
        if pernah == "Tidak": st.error("❌ Belum layak iklan. Fokus pada validasi review.")
        else:
            h_komp = st.number_input("Harga Kompetitor", value=140000)
            if hj > h_komp * 1.2: st.warning("⚠️ Harga Terlalu Tinggi.")
            elif laba < 5000: st.error("❌ Margin Terlalu Tipis.")
            else: st.success("✅ Layak Beriklan!")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.markdown("### 📊 Performance Ad Matrix")
    c_p1, c_p2, c_p3 = st.columns(3)
    imp = c_p1.number_input("👁️ Impressions", value=20000)
    clk = c_p1.number_input("🖱️ Total Clicks", value=600)
    spent = c_p2.number_input("💸 Total Spent (Rp)", value=150000)
    rev = c_p2.number_input("💰 Sales Revenue (Rp)", value=900000)
    ords = c_p3.number_input("📦 Total Orders", value=8)
    b_set = c_p3.number_input("💵 Daily Budget Setting", value=200000)
    
    if st.button("RUN DEEP ANALYTICS & AI AUDIT", use_container_width=True):
        ctr = (clk/imp*100) if imp > 0 else 0
        roas = (rev/spent) if spent > 0 else 0
        s_rate = (spent/b_set*100) if b_set > 0 else 0
        
        m1, m2, m3, m4 = st.columns(4)
        with m1: st.markdown(f'<div class="premium-card"><small>CTR</small><h3>{ctr:.2f}%</h3></div>', unsafe_allow_html=True)
        with m2: st.markdown(f'<div class="premium-card"><small>ROAS</small><h3 style="color:#00E5A0;">{roas:.2f}x</h3></div>', unsafe_allow_html=True)
        with m3: st.markdown(f'<div class="premium-card"><small>EST. NET PROFIT</small><h3>{format_rp(laba * ords - spent)}</h3></div>', unsafe_allow_html=True)
        with m4: st.markdown(f'<div class="premium-card"><small>STATUS</small><h3>{"PROFIT" if roas >= roas_bep else "LOSS"}</h3></div>', unsafe_allow_html=True)

        if clk > 50 and s_rate >= 80 and ords == 0:
            st.error(f"🔴 STOP! Budget terserap {s_rate:.0f}% tapi 0 Order.")
        elif s_rate >= 85 and roas >= roas_bep * 1.2:
            st.success(f"🟢 SCALE UP! Naikkan budget ke {format_rp(b_set*1.3)}.")
        
        if GEMINI_API_KEY:
            with st.spinner("AI sedang merancang strategi..."):
                advice = call_gemini(f"Analisis: ROAS {roas:.1f}x (BEP {roas_bep:.1f}x). Berikan strategi teknis.")
                if advice: st.info(f"💡 AI INSIGHT: {advice}")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<h2 class='gold-header' style='font-size:2rem;'>✨ Elite Copywriting Lab</h2>", unsafe_allow_html=True)
    p_name = st.text_input("🏷️ Product Name", placeholder="Input Nama Produk...")
    tabs = st.tabs(["🛍️ Shopee SEO", "🎥 TikTok Story", "🎬 Hooks", "#️⃣ Hashtags"])
    
    with tabs[0]:
        if st.button("Generate SEO Titles"):
            res = call_gemini(f"Buat 5 Judul Shopee SEO untuk {p_name}")
            st.code(res if res else f"🔥 {p_name} Best Seller", language="text")
    
    with tabs[1]:
        if st.button("Generate Viral Copy"):
            res = call_gemini(f"Buat copy TikTok viral untuk {p_name}")
            st.code(res if res else "Dulu aku...", language="markdown")

    st.markdown(f'<div style="text-align:center; padding:50px; color:#FFFFFF; font-size:0.9rem; opacity:0.8;">© 2026 Arkidigital Premier | <a href="{CHECKOUT_LINK}" style="color:#00E5A0; text-decoration:none;">UPGRADE ACCESS</a></div>', unsafe_allow_html=True)

if __name__ == "__main__": 
    main()
