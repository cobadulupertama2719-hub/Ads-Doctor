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
    
    html, body, [class*="css"] { 
        font-family: 'Plus Jakarta Sans', sans-serif; 
        color: #FFFFFF !important; 
    }
    
    .stApp { 
        background: radial-gradient(circle at 2% 2%, #1e1b4b 0%, #020617 100%); 
    }

    .premium-card {
        background: rgba(255, 255, 255, 0.07); 
        backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.3); 
        border-radius: 24px;
        padding: 30px;
        margin-bottom: 25px;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.7);
    }
    
    .gold-header {
        background: linear-gradient(135deg, #FFD700 0%, #B8860B 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }

    /* Kontras Tinggi untuk Form & Label */
    label, .stMarkdown p, .stMarkdown h3, .stMarkdown h2 {
        color: #FFFFFF !important;
        font-weight: 700 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.8);
    }

    .stNumberInput input, .stTextInput input, .stSelectbox div, .stTextArea textarea {
        background: rgba(0,0,0,0.7) !important; 
        border: 1px solid rgba(255,255,255,0.5) !important; 
        border-radius: 12px !important; 
        color: #FFFFFF !important;
        font-size: 1rem !important;
    }

    /* High-Contrast Metrics */
    .metric-val { color: #FFFFFF !important; font-size: 2.5rem !important; font-weight: 800 !important; margin: 0; }
    .metric-lab { color: #00E5A0 !important; font-size: 0.9rem !important; font-weight: 700 !important; text-transform: uppercase; margin-bottom: 5px; }

    .stButton>button {
        background: linear-gradient(135deg, #00E5A0 0%, #00a878 100%);
        color: #020617 !important; 
        font-weight: 800; 
        border: none; border-radius: 15px; padding: 20px;
        text-transform: uppercase; letter-spacing: 1.5px; width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# ==================== 2. CORE LOGIC ====================
if "authenticated" not in st.session_state: st.session_state["authenticated"] = False
if "demo_mode" not in st.session_state: st.session_state["demo_mode"] = False
if "demo_start_time" not in st.session_state: st.session_state["demo_start_time"] = None
if "demo_analysis_count" not in st.session_state: st.session_state["demo_analysis_count"] = 0
if "demo_generator_count" not in st.session_state: st.session_state["demo_generator_count"] = 0

ADMIN_USERNAME = "arkidigital"
ADMIN_PASSWORD = "Arkidigital2026"
CHECKOUT_LINK = "https://muhammad-masruri.myscalev.com/checkout-pageku"

# API Key dari Secrets
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")

def call_gemini(prompt):
    if not GEMINI_API_KEY: return None
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    try:
        r = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=25)
        return r.json()["candidates"][0]["content"]["parts"][0]["text"]
    except: return None

def format_rp(angka):
    if angka >= 1_000_000: return f"Rp{angka/1_000_000:.1f}JT"
    if angka >= 1000: return f"Rp{angka/1000:.0f}RB"
    return f"Rp{angka:,.0f}"

# ==================== 3. MAIN APP ====================
st.set_page_config(page_title="Doctor Ads Elite", page_icon="🩺", layout="wide")
apply_premium_style()

# Authentication Logic
if not st.session_state.authenticated and not st.session_state.demo_mode:
    st.markdown('<div style="text-align:center; padding-top:100px;">', unsafe_allow_html=True)
    st.markdown('<h1 class="gold-header" style="font-size:4rem;">🩺 DOCTOR ADS</h1>', unsafe_allow_html=True)
    col1, col2 = st.columns(2, gap="large")
    with col1:
        with st.form("login"):
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.form_submit_button("LOGIN PREMIUM"):
                if u == ADMIN_USERNAME and p == ADMIN_PASSWORD:
                    st.session_state.authenticated = True; st.rerun()
                else: st.error("Salah!")
    with col2:
        st.markdown('<div class="premium-card"><h3>🎁 Demo 5 Menit</h3>', unsafe_allow_html=True)
        if st.button("MULAI DEMO"):
            st.session_state.demo_mode = True; st.session_state.demo_start_time = datetime.now(); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- HEADER UTAMA ---
st.markdown('<h1 class="gold-header">🩺 ADVERTISING COMMAND CENTER</h1>', unsafe_allow_html=True)

# 🎯 KALKULATOR BEP & KELAYAKAN
c1, c2 = st.columns([2, 1])
with c1:
    st.markdown('<div class="premium-card"><h3>🎯 ROAS BEP Calculator</h3>', unsafe_allow_html=True)
    cb1, cb2, cb3 = st.columns(3)
    hj = cb1.number_input("Harga Jual (Rp)", value=150000)
    modal = cb2.number_input("Modal (Rp)", value=75000)
    admin_p = cb3.slider("Admin %", 5, 30, 20)
    target_p = st.number_input("Target Profit (Rp)", value=0)
    laba = hj - modal - (hj * admin_p/100) - target_p
    roas_bep = hj / laba if laba > 0 else 999
    st.markdown(f'<div style="text-align:center;"><p class="metric-lab">TARGET ROAS BEP</p><h1 style="color:#00E5A0; font-size:4rem;">{roas_bep:.2f}x</h1></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="premium-card" style="height:100%;"><h3>📋 Cek Kelayakan</h3>', unsafe_allow_html=True)
    pernah = st.radio("Pernah Laku?", ["Ya", "Tidak"], horizontal=True)
    if pernah == "Tidak": st.error("❌ Belum layak iklan!")
    else:
        h_komp = st.number_input("Harga Kompetitor", value=140000)
        if hj > h_komp * 1.2: st.warning("⚠️ Harga Terlalu Tinggi.")
        elif laba < 5000: st.error("❌ Margin Tipis.")
        else: st.success("✅ Siap Iklan!")
    st.markdown('</div>', unsafe_allow_html=True)

# 📊 INPUT DATA IKLAN
st.markdown('<div class="premium-card"><h3>📊 Ad Performance Matrix</h3>', unsafe_allow_html=True)
ip1, ip2, ip3 = st.columns(3)
imp = ip1.number_input("👁️ Impressions", value=20000)
clk = ip1.number_input("🖱️ Clicks", value=600)
spent = ip2.number_input("💸 Spent (Rp)", value=150000)
rev = ip2.number_input("💰 Omset (Rp)", value=900000)
ords = ip3.number_input("📦 Orders", value=8)
b_set = ip3.number_input("Daily Budget", value=200000)

if st.button("RUN DEEP ANALYTICS", use_container_width=True):
    ctr = (clk/imp*100) if imp > 0 else 0
    roas = (rev/spent) if spent > 0 else 0
    s_rate = (spent/b_set*100) if b_set > 0 else 0
    profit_est = (laba * ords) - spent

    # METRICS DISPLAY (ULTRA CONTRAST)
    m1, m2, m3, m4 = st.columns(4)
    m1.markdown(f'<div class="premium-card"><p class="metric-lab">CTR</p><p class="metric-val">{ctr:.2f}%</p></div>', unsafe_allow_html=True)
    m2.markdown(f'<div class="premium-card"><p class="metric-lab">ROAS AKTUAL</p><p class="metric-val" style="color:#00E5A0 !important;">{roas:.2f}x</p></div>', unsafe_allow_html=True)
    m3.markdown(f'<div class="premium-card"><p class="metric-lab">NET PROFIT</p><p class="metric-val">{format_rp(profit_est)}</p></div>', unsafe_allow_html=True)
    m4.markdown(f'<div class="premium-card"><p class="metric-lab">STATUS</p><p class="metric-val">{"PROFIT" if roas >= roas_bep else "LOSS"}</p></div>', unsafe_allow_html=True)

    # 🎯 LOGIC KERJA (ATURAN 1-5 ASLI)
    st.markdown("### 🎯 Rekomendasi Strategis")
    if clk > 50 and s_rate >= 80 and ords == 0:
        st.error(f"🔴 PRIORITAS 1 - STOP IKLAN! Klik {clk}, Budget terserap {s_rate:.0f}%, tapi 0 Order.")
    elif s_rate >= 85 and roas >= roas_bep * 1.2:
        st.success(f"🟢 PRIORITAS 4 - SCALE UP! Naikkan budget ke {format_rp(b_set*1.3)} (30%).")
    elif roas >= roas_bep and s_rate < 85:
        st.warning("🟡 PRIORITAS 2 - OPTIMASI. Turunkan target ROAS 0.5 poin.")
    elif roas < roas_bep and roas > 0:
        st.error("🔴 PRIORITAS 3 - IKLAN RUGI. Naikkan target ROAS 0.5 poin.")
    
    if ctr < 2: st.info(f"📸 CTR RENDAH ({ctr:.1f}%). Ganti Visual/Hook Video!")

    if GEMINI_API_KEY:
        with st.spinner("AI sedang merancang strategi..."):
            advice = call_gemini(f"Audit: ROAS {roas:.2f}x vs BEP {roas_bep:.2f}x. CTR {ctr:.1f}%. Beri strategi scale up/perbaikan tajam.")
            if advice: st.info(f"💡 AI STRATEGY: {advice}")
st.markdown('</div>', unsafe_allow_html=True)

# ✨ AI GENERATOR (NYAMBUNG KE API)
st.markdown("<h2 class='gold-header'>✨ Elite Copywriting Lab</h2>", unsafe_allow_html=True)
p_name = st.text_input("🏷️ Nama Produk", placeholder="Contoh: Kaos Oversize Premium")
tabs = st.tabs(["🛍️ Shopee SEO", "🎥 TikTok Story", "🎬 Hooks"])

with tabs[0]:
    if st.button("Generate SEO Titles"):
        with st.spinner("AI Menulis..."):
            res = call_gemini(f"Buat 5 Judul Shopee SEO Premium untuk {p_name}")
            st.code(res if res else "API Error", language="text")

with tabs[1]:
    if st.button("Generate TikTok Viral Copy"):
        with st.spinner("AI Menulis..."):
            res = call_gemini(f"Buat copy TikTok storytelling viral untuk {p_name}")
            st.code(res if res else "API Error", language="markdown")

with tabs[2]:
    if st.button("Generate Viral Hooks"):
        with st.spinner("AI Menulis..."):
            res = call_gemini(f"Buat 5 hook video TikTok yang bikin stop scrolling untuk {p_name}")
            st.info(res if res else "API Error")

st.markdown(f'<div style="text-align:center; padding:50px; color:#FFFFFF; opacity:0.8;">© 2026 Arkidigital Premier | <a href="{CHECKOUT_LINK}" style="color:#00E5A0; text-decoration:none;">UPGRADE ACCESS</a></div>', unsafe_allow_html=True)
[cite_start]
