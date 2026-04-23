import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import hashlib
import requests
import json

# ==================== 1. ULTRA-PREMIUM INTERFACE ENGINE ====================
def apply_ultra_premium_ui():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700;800&display=swap');
    
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; color: #F8FAFC; }
    .stApp { background: radial-gradient(circle at 2% 2%, #1e1b4b 0%, #020617 100%); }

    /* Luxury Card Design */
    .premium-card {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 24px;
        padding: 35px;
        margin-bottom: 30px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    }
    
    .gold-text { background: linear-gradient(135deg, #FFD700 0%, #B8860B 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; }
    .emerald-glow { color: #00E5A0; text-shadow: 0 0 10px rgba(0, 229, 160, 0.5); font-weight: 800; }
    
    /* Input Styling */
    .stNumberInput input, .stTextInput input, .stSelectbox div { 
        background: rgba(0,0,0,0.4) !important; 
        border: 1px solid rgba(255,255,255,0.1) !important; 
        border-radius: 12px !important; 
        color: white !important; 
    }

    /* Premium Button Action */
    .stButton>button {
        background: linear-gradient(135deg, #00E5A0 0%, #00a878 100%);
        color: #020617 !important; font-weight: 800; border: none; border-radius: 15px;
        padding: 20px; transition: all 0.4s ease; text-transform: uppercase; letter-spacing: 1.5px;
        box-shadow: 0 10px 20px rgba(0, 229, 160, 0.2);
    }
    .stButton>button:hover { transform: translateY(-3px); box-shadow: 0 15px 35px rgba(0, 229, 160, 0.4); }
    </style>
    """, unsafe_allow_html=True)

# ==================== 2. CORE LOGIC & AI CONFIG ====================
for key, val in {
    "authenticated": False, "demo_mode": False, "products": [], 
    "demo_analysis_count": 0, "demo_generator_count": 0
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
        r = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=20)
        return r.json()["candidates"][0]["content"]["parts"][0]["text"]
    except: return "AI sedang dalam pemeliharaan. Silakan coba lagi nanti."

def format_rp(n):
    return f"Rp{n:,.0f}"

# ==================== 3. LOGIN INTERFACE ====================
def show_login():
    apply_ultra_premium_ui()
    st.markdown('<div style="text-align:center; padding-top:100px;">', unsafe_allow_html=True)
    st.markdown('<h1 class="gold-text" style="font-size:4rem; margin-bottom:0;">DOCTOR ADS</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#94A3B8; font-size:1.5rem; font-weight:300;">Elite Ad Intelligence & Profit Optimization Portfolio</p>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2, gap="large")
    with c1:
        with st.form("login"):
            st.markdown("### 🔐 Member Access")
            u = st.text_input("ID Access")
            p = st.text_input("Security Key", type="password")
            if st.form_submit_button("UNLOCK DASHBOARD"):
                if u == ADMIN_USERNAME and p == ADMIN_PASSWORD:
                    st.session_state.authenticated = True; st.rerun()
                else: st.error("Access Denied.")
    with c2:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown("### 🎁 Exclusive Demo")
        st.write("Coba fitur analisis cerdas kami selama 5 menit secara gratis.")
        if st.button("START FREE TRIAL"):
            st.session_state.demo_mode = True; st.session_state["demo_start_time"] = datetime.now(); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ==================== 4. MAIN ELITE DASHBOARD ====================
def main():
    st.set_page_config(page_title="Doctor Ads Premium", page_icon="🩺", layout="wide")
    apply_ultra_premium_ui()
    
    if not st.session_state.authenticated and not st.session_state.demo_mode:
        show_login(); st.stop()

    # --- HEADER ---
    st.markdown('<h1 class="gold-text">🩺 DOCTOR ADS ELITE</h1>', unsafe_allow_html=True)
    
    # ==================== FITUR 1 & 2: PINDAH KE HALAMAN UTAMA ====================
    col_main1, col_main2 = st.columns([2, 1], gap="medium")
    
    with col_main1:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown("### 🎯 Elite ROAS BEP Calculator")
        st.write("Tentukan batas aman iklan Anda sebelum melakukan pengeluaran budget.")
        c_b1, c_b2, c_b3 = st.columns(3)
        with c_b1:
            hj_main = st.number_input("Harga Jual (Rp)", value=150000, step=5000)
        with c_b2:
            cost_main = st.number_input("Modal / HPP (Rp)", value=75000, step=5000)
        with c_b3:
            adm_main = st.slider("Admin Marketplace %", 5, 30, 20)
        
        target_p = st.number_input("Target Profit Bersih per Produk (Rp)", value=0, step=5000)
        
        laba_bersih = hj_main - cost_main - (hj_main * adm_main/100) - target_p
        roas_bep_main = hj_main / laba_bersih if laba_bersih > 0 else 999
        
        st.markdown(f"""
            <div style="background: rgba(0, 229, 160, 0.05); border-radius: 15px; padding: 20px; border: 1px solid rgba(0, 229, 160, 0.2); text-align: center;">
                <p style="margin:0; color:#94A3B8;">TARGET ROAS BEP ANDA</p>
                <h2 class="emerald-glow" style="margin:0; font-size:3rem;">{roas_bep_main:.2f}x</h2>
                <p style="margin:0; color:#00E5A0; font-size:0.9rem;">Laba Kotor per Produk: {format_rp(hj_main - cost_main - (hj_main * adm_main/100))}</p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_main2:
        st.markdown('<div class="premium-card" style="height: 100%;">', unsafe_allow_html=True)
        st.markdown("### 📋 Kelayakan Produk")
        st.write("Audit kelayakan sebelum iklan.")
        pernah = st.radio("Pernah Laku?", ["Ya", "Tidak"], horizontal=True)
        if pernah == "Tidak":
            st.error("❌ Belum layak iklan. Fokus pada organik / review.")
        else:
            terjual = st.number_input("Terjual/Bulan", value=500)
            h_komp = st.number_input("Harga Kompetitor", value=140000)
            if hj_main > h_komp * 1.2: st.warning("⚠️ Harga terlalu tinggi.")
            elif laba_bersih < 5000: st.error("❌ Margin terlalu tipis.")
            else: st.success("✅ Produk Layak Scale-Up!")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- FITUR 3: INPUT DATA IKLAN ---
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.markdown("### 📊 Performance Ad Matrix")
    c_a1, c_a2, c_a3 = st.columns(3)
    with c_a1:
        imp = st.number_input("👁️ Impressions", value=25000)
        clk = st.number_input("🖱️ Clicks", value=750)
    with c_a2:
        spent = st.number_input("💸 Total Spent (Rp)", value=250000)
        rev = st.number_input("💰 Sales Revenue (Rp)", value=1500000)
    with c_a3:
        ords = st.number_input("📦 Total Orders", value=15)
        b_set = st.number_input("💵 Daily Budget Setting", value=300000)
    
    analyze_btn = st.button("RUN DEEP ANALYTICS & AI AUDIT", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if analyze_btn:
        ctr = (clk/imp*100) if imp > 0 else 0
        roas_akt = (rev/spent) if spent > 0 else 0
        s_rate = (spent/b_set*100) if b_set > 0 else 0
        
        # Dashboard Metrik
        m1, m2, m3, m4 = st.columns(4)
        m1.markdown(f'<div class="premium-card"><small>CTR</small><h3>{ctr:.2f}%</h3></div>', unsafe_allow_html=True)
        m2.markdown(f'<div class="premium-card"><small>ROAS</small><h3 class="emerald-glow">{roas_akt:.2f}x</h3></div>', unsafe_allow_html=True)
        m3.markdown(f'<div class="premium-card"><small>NET PROFIT</small><h3>{format_rp((laba_bersih + target_p)*ords - spent)}</h3></div>', unsafe_allow_html=True)
        m4.markdown(f'<div class="premium-card"><small>ADS STATUS</small><h3>{"PROFITS" if roas_akt >= roas_bep_main else "LOSS"}</h3></div>', unsafe_allow_html=True)

        # REKOMENDASI TEKNIS ASLI (Aturan 1-5)
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.subheader("🎯 Elite Recommendation")
        if clk > 50 and s_rate >= 80 and ords == 0:
            st.error(f"🔴 STOP SEGERA! Budget terserap {s_rate:.0f}% tapi 0 Order. [span_3](start_span)Produk belum siap pasar.")[span_3](end_span)
        elif s_rate >= 85 and roas_akt >= roas_bep_main * 1.2:
            [span_4](start_span)st.success(f"🟢 SCALE UP! Naikkan budget ke {format_rp(b_set*1.3)} (30%). ROAS sangat sehat.")[span_4](end_span)
        elif roas_akt >= roas_bep_main and s_rate < 85:
            [span_5](start_span)st.warning(f"🟡 OPTIMASI. Turunkan target ROAS 0.5 poin agar budget terserap maksimal.")[span_5](end_span)
        
        if GEMINI_API_KEY:
            with st.spinner("AI sedang merancang strategi..."):
                advice = call_gemini(f"Analisis iklan ROAS {roas_akt:.1f}x vs BEP {roas_bep_main:.1f}x. CTR {ctr:.1f}%. Berikan strategi teknis mendalam dalam 2 paragraf.")
                st.info(f"💡 AI STRATEGY: {advice}")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- FITUR 4: AI GENERATOR LAB (DEEP VERSION) ---
    st.markdown("### ✨ Elite Copywriting Lab")
    p_name = st.text_input("🏷️ Product Name", placeholder="Masukkan Nama Produk Anda...")
    tabs = st.tabs(["🛍️ Shopee SEO Elite", "🎥 TikTok Viral Story", "🎬 Visual Hooks", "#️⃣ Smart Hashtags"])
    
    with tabs[0]:
        if st.button("Generate Professional SEO Titles"):
            with st.spinner("Analyzing Keywords..."):
                res = call_gemini(f"Buat 5 Judul Shopee SEO untuk {p_name}. Gunakan format premium: [Emoji] [Brand] [Keyword] [Benefit] [Scarcity].")
                [span_6](start_span)st.code(res, language="text")[span_6](end_span)
    
    with tabs[1]:
        if st.button("Generate Emotional Storytelling"):
            with st.spinner("Writing Story..."):
                res = call_gemini(f"Buat copy TikTok storytelling emosional untuk {p_name}. Fokus pada solusi masalah pembeli.")
                [span_7](start_span)st.code(res, language="markdown")[span_7](end_span)
    
    with tabs[2]:
        style = st.selectbox("Hook Style", ["Pattern Interrupt", "Problem Solver", "Extreme Scarcity"])
        if st.button("Generate Viral Hooks"):
            [span_8](start_span)res = call_gemini(f"Buat 5 Hook Video TikTok gaya {style} untuk {p_name}. Harus bikin stop scrolling.")[span_8](end_span)
            st.info(res)

    st.markdown(f'<div style="text-align:center; padding:50px; color:#475569;">© 2026 Arkidigital Premier Ad Suite - <a href="{CHECKOUT_LINK}" style="color:#00E5A0; text-decoration:none;">Upgrade Access</a></div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
