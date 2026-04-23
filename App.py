import streamlit as st

# 1. SELALU taruh set_page_config di baris pertama setelah import
st.set_page_config(
    page_title="Advertising Command Center",
    layout="wide", # Membuat tampilan lebih luas ke samping
    initial_sidebar_state="collapsed"
)

# 2. Masukkan kode CSS untuk menyembunyikan header di sini
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
            .stAppDeployButton {display:none;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import hashlib
import requests
import json

# ==================== 1. ULTRA-CONTRAST & PREMIUM UI ====================
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
        background: rgba(255, 255, 255, 0.08); 
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

    label, .stMarkdown p, .stMarkdown h3, .stMarkdown h2 {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }

    .stNumberInput input, .stTextInput input, .stSelectbox div {
        background: rgba(0,0,0,0.7) !important; 
        border: 1px solid rgba(255,255,255,0.5) !important; 
        border-radius: 12px !important; 
        color: #FFFFFF !important;
    }

    /* Metric Visual Styles */
    .metric-lab { color: #00E5A0 !important; font-size: 0.9rem !important; font-weight: 700 !important; text-transform: uppercase; margin-bottom: 5px; }
    .metric-val { color: #FFFFFF !important; font-size: 2.4rem !important; font-weight: 800 !important; margin: 0; }

    /* CTA UPGRADE BESAR */
    .cta-upgrade {
        background: linear-gradient(135deg, #00E5A0 0%, #00a878 100%);
        color: #020617 !important;
        text-align: center;
        padding: 25px;
        border-radius: 20px;
        text-decoration: none;
        display: block;
        font-size: 1.5rem;
        font-weight: 900;
        margin: 20px 0;
        box-shadow: 0 15px 35px rgba(0, 229, 160, 0.4);
        transition: all 0.3s ease;
        border: none;
        cursor: pointer;
        width: 100%;
    }
    .cta-upgrade:hover {
        transform: scale(1.03);
        box-shadow: 0 20px 45px rgba(0, 229, 160, 0.6);
    }

    .stButton>button {
        background: linear-gradient(135deg, #00E5A0 0%, #00a878 100%);
        color: #020617 !important; 
        font-weight: 800; border: none; border-radius: 15px; padding: 20px;
        text-transform: uppercase; letter-spacing: 1.5px; width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# ==================== 2. SESSION & LOCK SYSTEM ====================
if "authenticated" not in st.session_state: st.session_state["authenticated"] = False
if "demo_mode" not in st.session_state: st.session_state["demo_mode"] = False
if "demo_start_time" not in st.session_state: st.session_state["demo_start_time"] = None
if "demo_analysis_count" not in st.session_state: st.session_state["demo_analysis_count"] = 0
if "demo_generator_count" not in st.session_state: st.session_state["demo_generator_count"] = 0

ADMIN_USERNAME = "arkidigital"
ADMIN_PASSWORD = "Arkidigital2026"
CHECKOUT_LINK = "https://muhammad-masruri.myscalev.com/checkout-pageku"

GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")

def call_gemini_api(prompt):
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

# ==================== 3. LOGIN & TRIAL RECALL ====================
st.set_page_config(page_title="Doctor Ads Elite", page_icon="🩺", layout="wide")
apply_premium_style()

# Cek apakah demo habis (Limit 2x Analisis atau 5 Menit)
demo_expired = False
if st.session_state.demo_mode:
    elapsed = (datetime.now() - st.session_state.demo_start_time).total_seconds()
    if elapsed > 300 or st.session_state.demo_analysis_count >= 2:
        demo_expired = True

if (not st.session_state.authenticated and not st.session_state.demo_mode) or demo_expired:
    st.markdown('<div style="text-align:center; padding-top:50px;">', unsafe_allow_html=True)
    if demo_expired:
        st.markdown('<h1 class="gold-header">⏰ TRIAL SELESAI</h1>', unsafe_allow_html=True)
        st.markdown('<h3>Upgrade ke Premium untuk Akses Tanpa Batas & Konsultasi Gratis!</h3>', unsafe_allow_html=True)
    else:
        st.markdown('<h1 class="gold-header" style="font-size:4rem;">🩺 DOCTOR ADS</h1>', unsafe_allow_html=True)
    
    st.markdown(f'<a href="{CHECKOUT_LINK}" target="_blank" class="cta-upgrade">💎 BELI AKSES PREMIUM SEKARANG - RP147RB</a>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="large")
    with col1:
        with st.form("login"):
            st.markdown("### 🔐 Member Login")
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.form_submit_button("MASUK DASHBOARD"):
                if u == ADMIN_USERNAME and p == ADMIN_PASSWORD:
                    st.session_state.authenticated = True; st.session_state.demo_mode = False; st.rerun()
                else: st.error("Salah!")
    with col2:
        if not demo_expired:
            st.markdown('<div class="premium-card"><h3>🎁 Coba Demo</h3>', unsafe_allow_html=True)
            st.write("Maksimal 2x analisis & durasi 5 menit.")
            if st.button("MULAI TRIAL"):
                st.session_state.demo_mode = True; st.session_state.demo_start_time = datetime.now(); st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- HEADER DASHBOARD ---
st.markdown('<h1 class="gold-header">🩺 ADVERTISING COMMAND CENTER</h1>', unsafe_allow_html=True)

# 🎯 BEP & KELAYAKAN
col_bep, col_audit = st.columns([2, 1])
with col_bep:
    st.markdown('<div class="premium-card"><h3>🎯 ROAS BEP Calculator</h3>', unsafe_allow_html=True)
    cb1, cb2, cb3 = st.columns(3)
    hj = cb1.number_input("Harga Jual (Rp)", value=150000)
    modal = cb2.number_input("Modal (Rp)", value=75000)
    admin_p = cb3.slider("Admin %", 5, 30, 20)
    target_p = st.number_input("Target Profit (Rp)", value=0)
    laba_kotor = hj - modal - (hj * admin_p/100)
    laba_setelah_profit = laba_kotor - target_p
    roas_bep = hj / laba_setelah_profit if laba_setelah_profit > 0 else 999
    st.markdown(f'<div style="text-align:center;"><p class="metric-lab">TARGET ROAS BEP</p><h1 style="color:#00E5A0; font-size:4rem;">{roas_bep:.2f}x</h1></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_audit:
    st.markdown('<div class="premium-card" style="height:100%;"><h3>📋 Kelayakan</h3>', unsafe_allow_html=True)
    pernah = st.radio("Pernah Laku?", ["Ya", "Tidak"], horizontal=True)
    if pernah == "Tidak": st.error("❌ Belum layak iklan!")
    else:
        h_komp = st.number_input("Harga Kompetitor", value=140000)
        if hj > h_komp * 1.2: st.warning("⚠️ Harga Terlalu Tinggi.")
        elif laba_kotor < 5000: st.error("❌ Margin Tipis.")
        else: st.success("✅ Siap Iklan!")
    st.markdown('</div>', unsafe_allow_html=True)

# 📊 ANALISIS IKLAN
st.markdown('<div class="premium-card"><h3>📊 Ad Performance Matrix</h3>', unsafe_allow_html=True)
ip1, ip2, ip3 = st.columns(3)
impressions = ip1.number_input("👁️ Impressions", value=20000)
clicks = ip1.number_input("🖱️ Clicks", value=600)
budget_spent = ip2.number_input("💸 Spent (Rp)", value=150000)
sales = ip2.number_input("💰 Sales Revenue (Rp)", value=900000)
orders = ip3.number_input("📦 Orders", value=8)
budget_set = ip3.number_input("Daily Budget", value=200000)
target_roas = st.number_input("🎯 Target ROAS Setting", value=5.0)

if st.button("RUN DEEP ANALYTICS", use_container_width=True):
    if st.session_state.demo_mode:
        st.session_state.demo_analysis_count += 1
    
    ctr = (clicks/impressions*100) if impressions > 0 else 0
    roas_aktual = (sales/budget_spent) if budget_spent > 0 else 0
    budget_terserap_persen = (budget_spent/budget_set*100) if budget_set > 0 else 0
    profit_estimasi = (laba_kotor * orders) - budget_spent

    m1, m2, m3, m4 = st.columns(4)
    m1.markdown(f'<div class="premium-card"><p class="metric-lab">CTR</p><p class="metric-val">{ctr:.2f}%</p></div>', unsafe_allow_html=True)
    m2.markdown(f'<div class="premium-card"><p class="metric-lab">ROAS AKTUAL</p><p class="metric-val" style="color:#00E5A0 !important;">{roas_aktual:.2f}x</p></div>', unsafe_allow_html=True)
    m3.markdown(f'<div class="premium-card"><p class="metric-lab">EST. NET PROFIT</p><p class="metric-val">{format_rp(profit_estimasi)}</p></div>', unsafe_allow_html=True)
    m4.markdown(f'<div class="premium-card"><p class="metric-lab">ROAS BEP</p><p class="metric-val">{roas_bep:.2f}x</p></div>', unsafe_allow_html=True)

    # REKOMENDASI (WARNA KONTRAS)
    st.markdown("### 🎯 Rekomendasi & Kesimpulan")
    rekomendasi_tindakan = ""
    rekomendasi_roas = target_roas
    rekomendasi_budget = budget_set
    prioritas = ""
    
    if clicks > 50 and budget_terserap_persen >= 80 and orders == 0:
        prioritas = "🔴 PRIORITAS 1 - URGENT (Stop Iklan)"
        rekomendasi_tindakan = f"Data: {clicks} klik, budget terserap {budget_terserap_persen:.0f}%, tapi 0 order. Produk belum layak. Cek harga, review, dan deskripsi."
    elif budget_terserap_persen >= 85 and roas_aktual >= roas_bep * 1.2:
        prioritas = "🟢 PRIORITAS 4 - SIAP SCALE"
        rekomendasi_budget = budget_set * 1.3
        rekomendasi_tindakan = f"ROAS {roas_aktual:.1f}x untung. Naikkan BUDGET 30% ke {format_rp(rekomendasi_budget)}. Tunggu 3 hari."
    elif roas_aktual >= roas_bep:
        prioritas = "🟢 PRIORITAS 5 - PANTAU"
        rekomendasi_tindakan = "Performa sehat. Pertahankan setting saat ini dan pantau 3-5 hari."

    st.markdown(f"""
    <div class="premium-card" style="border-left: 10px solid #00E5A0;">
        <h4 style="color:#00E5A0;">{prioritas}</h4>
        <p style="font-size:1.1rem; line-height:1.6; color:white;">{rekomendasi_tindakan}</p>
        <hr style="border:0.5px solid rgba(255,255,255,0.2);">
        <p><strong>💰 Budget Rekomendasi:</strong> {format_rp(rekomendasi_budget)} | <strong>🎯 Target ROAS:</strong> {rekomendasi_roas:.1f}x</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ✨ AI GENERATOR
st.markdown("<h2 class='gold-header'>✨ Elite Copywriting Lab</h2>", unsafe_allow_html=True)
p_name = st.text_input("🏷️ Nama Produk", placeholder="Contoh: Kaos Oversize Premium")
tabs = st.tabs(["🛍️ Shopee SEO", "🎥 TikTok Viral", "🎬 Hooks"])

with tabs[0]:
    if st.button("Generate SEO Titles"):
        if st.session_state.demo_mode: st.session_state.demo_generator_count += 1
        with st.spinner("AI Menulis..."):
            res = call_gemini_api(f"Buat 5 Judul Shopee SEO untuk {p_name}")
            st.code(res if res else "API Error", language="text")

st.markdown(f'<div style="text-align:center; padding:50px;"><a href="{CHECKOUT_LINK}" target="_blank" class="cta-upgrade">💎 UPGRADE PREMIUM - AKSES TANPA BATAS</a></div>', unsafe_allow_html=True)
