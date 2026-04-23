import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import hashlib
import requests
import json

# ==================== 1. ELITE UI CONFIGURATION ====================
def apply_premium_style():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700;800&display=swap');
    
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; color: #F8FAFC; }
    .stApp { background: radial-gradient(circle at 2% 2%, #1e1b4b 0%, #020617 100%); }

    .premium-card {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 30px;
        margin-bottom: 25px;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5);
    }
    
    .gold-header {
        background: linear-gradient(135deg, #FFD700 0%, #B8860B 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }

    .stButton>button {
        background: linear-gradient(135deg, #00E5A0 0%, #00a878 100%);
        color: #020617 !important; font-weight: 800; border: none; border-radius: 15px;
        padding: 18px; transition: all 0.3s ease; text-transform: uppercase; letter-spacing: 1.5px;
        width: 100%;
    }
    .stButton>button:hover { transform: translateY(-3px); box-shadow: 0 15px 35px rgba(0, 229, 160, 0.4); }

    .stNumberInput input, .stTextInput input, .stSelectbox div {
        background: rgba(0,0,0,0.4) !important; border-radius: 12px !important; color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ==================== 2. CORE LOGIC & SECURITY ====================
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
    st.markdown('<p style="color:#94A3B8; font-size:1.2rem;">Advanced Ad Intelligence & Profit Optimization Portfolio</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="large")
    with col1:
        with st.form("login"):
            st.markdown("### 🔐 Member Access")
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.form_submit_button("UNLOCK DASHBOARD"):
                if u == ADMIN_USERNAME and p == ADMIN_PASSWORD:
                    st.session_state.authenticated = True; st.rerun()
                else: st.error("Wrong Password!")
    with col2:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown("### 🎁 Trial Access")
        st.write("Dapatkan analisis cerdas kami selama 5 menit secara gratis.")
        if st.button("START FREE TRIAL"):
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
            st.warning("Trial Expired! Beli Premium untuk akses penuh."); 
            st.markdown(f'<a href="{CHECKOUT_LINK}" target="_blank" style="text-decoration:none;"><div class="stButton"><button>💎 BELI PREMIUM SEKARANG</button></div></a>', unsafe_allow_html=True)
            st.stop()

    # --- TOP SECTION: FINANCIAL AUDIT ---
    st.markdown('<h1 class="gold-header">🩺 DASHBOARD UTAMA</h1>', unsafe_allow_html=True)
    
    c_f1, c_f2 = st.columns([2, 1])
    with c_f1:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown("### 🎯 Elite ROAS BEP Calculator")
        col_b1, col_b2, col_b3 = st.columns(3)
        hj = col_b1.number_input("Harga Jual (Rp)", value=150000, step=5000)
        modal = col_b2.number_input("Modal / HPP (Rp)", value=75000, step=5000)
        admin_p = col_b3.slider("Admin %", 5, 30, 20)
        target_p = st.number_input("Target Profit (Rp)", value=0)
        
        laba = hj - modal - (hj * admin_p/100) - target_p
        roas_bep = hj / laba if laba > 0 else 999
        st.markdown(f'<h2 style="color:#00E5A0; text-align:center; font-size:3rem;">TARGET ROAS BEP: {roas_bep:.2f}x</h2>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c_f2:
        st.markdown('<div class="premium-card" style="height:100%;">', unsafe_allow_html=True)
        st.markdown("### 📋 Kelayakan Produk")
        pernah = st.radio("Pernah Laku?", ["Ya", "Tidak"], horizontal=True)
        if pernah == "Tidak": st.error("❌ Jangan iklan dulu! Fokus pada review organik.")
        else:
            h_komp = st.number_input("Harga Kompetitor", value=140000)
            if hj > h_komp * 1.2: st.warning("⚠️ Harga terlalu tinggi.")
            elif laba < 5000: st.error("❌ Margin terlalu tipis.")
            else: st.success("✅ Layak Iklan!")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- MAIN SECTION: AD PERFORMANCE ---
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.markdown("### 📊 Ad Performance Matrix")
    c_p1, c_p2, c_p3 = st.columns(3)
    imp = c_p1.number_input("👁️ Impressions", value=20000)
    clk = c_p1.number_input("🖱️ Clicks", value=600)
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
        with m3: st.markdown(f'<div class="premium-card"><small>NET PROFIT</small><h3>{format_rp(laba * ords - spent)}</h3></div>', unsafe_allow_html=True)
        with m4: st.markdown(f'<div class="premium-card"><small>ADS STATUS</small><h3>{"SAFE" if roas >= roas_bep else "LOSS"}</h3></div>', unsafe_allow_html=True)

        st.markdown("### 🎯 Strategic Recommendation")
        if clk > 50 and s_rate >= 80 and ords == 0:
            st.error(f"🔴 PRIORITAS 1: STOP IKLAN! Klik tinggi ({clk}), Budget terserap {s_rate:.0f}%, tapi 0 Order. Produk belum siap.")
        elif s_rate >= 85 and roas >= roas_bep * 1.2:
            st.success(f"🟢 PRIORITAS 4: SCALE UP! Naikkan budget harian menjadi {format_rp(b_set*1.3)} (30%).")
        elif roas >= roas_bep and s_rate < 85:
            st.warning("🟡 PRIORITAS 2: OPTIMASI. Turunkan target ROAS 0.5 poin agar budget maksimal.")
        
        if ctr < 2: st.info(f"📸 CTR Rendah ({ctr:.1f}%). Solusi: Ganti Visual Creative segera!")
        
        if GEMINI_API_KEY:
            with st.spinner("AI sedang merancang strategi..."):
                advice = call_gemini(f"Analisis iklan ROAS {roas:.1f}x (BEP {roas_bep:.1f}x). Berikan strategi teknis mendalam.")
                if advice: st.info(f"💡 AI STRATEGY: {advice}")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- AI COPYWRITING LAB ---
    st.markdown("### ✨ Elite Copywriting Lab")
    p_name = st.text_input("🏷️ Nama Produk untuk AI", placeholder="Contoh: Kaos Oversize Premium")
    tabs = st.tabs(["🛍️ Shopee SEO", "🎥 TikTok Story", "🎬 Hooks", "#️⃣ Hashtags"])
    
    with tabs[0]:
        if st.button("Generate Elite Shopee Title"):
            res = call_gemini(f"Buat 5 Judul Shopee SEO Premium untuk {p_name}")
            st.code(res if res else f"🔥 {p_name} Best Seller - Premium Quality", language="text")
    
    with tabs[1]:
        if st.button("Generate TikTok Viral Story"):
            res = call_gemini(f"Buat copy TikTok storytelling emosional untuk {p_name}")
            st.code(res if res else "Dulu aku kesulitan cari produk yang pas, tapi sejak pakai ini...", language="markdown")

    st.markdown(f'<div style="text-align:center; padding:50px; color:#64748B;">© 2026 Arkidigital Premier Ad Suite - <a href="{CHECKOUT_LINK}" style="color:#00E5A0; text-decoration:none;">Upgrade Access</a></div>', unsafe_allow_html=True)

if __name__ == "__main__": 
    main()
