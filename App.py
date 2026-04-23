import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import hashlib
import requests
import json

# 1. SET PAGE CONFIG (WAJIB DI PALING ATAS)
st.set_page_config(
    page_title="Advertising Command Center",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== 1. ULTRA-PREMIUM UI CONFIGURATION ====================
def apply_premium_style():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700;800&display=swap');
    
    /* Global Text Visibility & Contrast */
    html, body, [class*="css"] { 
        font-family: 'Plus Jakarta Sans', sans-serif; 
        color: #FFFFFF !important; 
    }
    
    .stApp { 
        background: radial-gradient(circle at 2% 2%, #1e1b4b 0%, #020617 100%); 
    }

    /* Luxury Glassmorphism Card */
    .premium-card {
        background: rgba(255, 255, 255, 0.07); 
        backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.25); 
        border-radius: 24px;
        padding: 30px;
        margin-bottom: 25px;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.7);
    }
    
    /* Headers & Gold Text */
    .gold-header {
        background: linear-gradient(135deg, #FFD700 0%, #B8860B 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }

    /* Ensure all Labels & Markdown are White */
    label, .stMarkdown p, .stMarkdown h3, .stMarkdown h2, .stMarkdown h5, div[data-testid="stMarkdownContainer"] p {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }

    /* Input & Select Contrast */
    .stNumberInput input, .stTextInput input, .stSelectbox div, .stTextArea textarea {
        background: rgba(0,0,0,0.6) !important; 
        border: 1px solid rgba(255,255,255,0.4) !important; 
        border-radius: 12px !important; 
        color: #FFFFFF !important;
    }

    /* Radio Button Fix (Pernah Laku) */
    div[class*="stRadio"] label {
        color: #FFFFFF !important;
        font-weight: 500 !important;
    }

    /* CTA UPGRADE PREMIUM - DESIGNED FOR CONVERSION */
    .cta-upgrade {
        background: linear-gradient(135deg, #00E5A0 0%, #00a878 100%);
        color: #020617 !important;
        text-align: center;
        padding: 25px;
        border-radius: 20px;
        text-decoration: none;
        display: block;
        font-size: 1.6rem;
        font-weight: 900;
        margin: 25px 0;
        box-shadow: 0 15px 40px rgba(0, 229, 160, 0.5);
        transition: all 0.3s ease;
        border: none;
        width: 100%;
    }
    .cta-upgrade:hover {
        transform: scale(1.02);
        box-shadow: 0 20px 50px rgba(0, 229, 160, 0.7);
    }

    /* Custom Metric Display */
    .metric-label { color: #00E5A0 !important; font-size: 0.9rem !important; font-weight: 700 !important; text-transform: uppercase; }
    .metric-value { color: #FFFFFF !important; font-size: 2.4rem !important; font-weight: 800 !important; margin: 0; }

    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stAppDeployButton {display:none;}
    [data-testid="stToolbar"] {display:none;}
    </style>
    """, unsafe_allow_html=True)

apply_premium_style()

# ==================== 2. SESSION & LOCK SYSTEM ====================
if "authenticated" not in st.session_state: st.session_state["authenticated"] = False
if "demo_mode" not in st.session_state: st.session_state["demo_mode"] = False
if "demo_start_time" not in st.session_state: st.session_state["demo_start_time"] = None
if "demo_analysis_count" not in st.session_state: st.session_state["demo_analysis_count"] = 0
if "products" not in st.session_state: st.session_state["products"] = []
if "analysis_done" not in st.session_state: st.session_state["analysis_done"] = False

ADMIN_USERNAME = "arkidigital"
ADMIN_PASSWORD = "Arkidigital2026"
CHECKOUT_LINK = "https://muhammad-masruri.myscalev.com/checkout-pageku"

# ==================== API KEY CONFIGURATION ====================
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")

def call_gemini_api(prompt):
    if not GEMINI_API_KEY: return None
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    try:
        response = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=30)
        if response.status_code == 200:
            result = response.json()
            return result["candidates"][0]["content"]["parts"][0]["text"]
        return None
    except: return None

def format_rp(angka):
    if angka >= 1_000_000: return f"Rp{angka/1_000_000:.1f}JT"
    if angka >= 1000: return f"Rp{angka/1000:.0f}RB"
    return f"Rp{angka:,.0f}"

# ==================== FUNGSI REKOMENDASI (1-5) ====================
def generate_rekomendasi(roas_aktual, roas_bep, s_rate, clicks, orders, budget_set, target_roas, budget_spent, ctr):
    rekom_tindakan = ""
    rekom_roas = target_roas
    rekom_budget = budget_set
    prioritas = ""
    warna = "info"
    
    if clicks > 50 and s_rate >= 80 and orders == 0:
        prioritas = "🔴 PRIORITAS 1 - URGENT (Stop Iklan)"
        warna = "danger"
        rekom_tindakan = f"🚨 **HENTIKAN IKLAN SEGERA!**\nData: {clicks} klik, budget terserap {s_rate:.0f}%, tapi 0 order. Produk belum layak iklan. Cek harga, review, dan manfaat produk."
    elif s_rate >= 85 and roas_aktual >= roas_bep * 1.2:
        prioritas = "🟢 PRIORITAS 4 - SIAP SCALE"
        warna = "success"
        rekom_budget = budget_set * 1.3
        rekom_tindakan = f"🚀 **SIAP SCALE!**\nROAS {roas_aktual:.1f}x > BEP {roas_bep:.1f}x (untung). Naikkan budget 30% ke {format_rp(rekom_budget)}. Pantau 3 hari."
    elif roas_aktual >= roas_bep and s_rate < 85:
        prioritas = "🟡 PRIORITAS 2 - OPTIMASI"
        warna = "warning"
        rekom_roas = target_roas - 0.5
        rekom_tindakan = f"⚡ **OPTIMASI BUDGET**\nROAS {roas_aktual:.1f}x ≥ BEP {roas_bep:.1f}x. Budget belum habis terserap. Turunkan target ROAS 0.5 poin menjadi {rekom_roas:.1f}x."
    elif roas_aktual < roas_bep and roas_aktual > 0:
        prioritas = "🔴 PRIORITAS 3 - IKLAN RUGI"
        warna = "danger"
        rekom_roas = roas_bep + 0.5
        rekom_tindakan = f"💸 **IKLAN RUGI!**\nROAS {roas_aktual:.1f}x < BEP {roas_bep:.1f}x. Naikkan target ROAS ke {rekom_roas:.1f}x untuk menjaga margin."
    elif roas_aktual >= roas_bep:
        prioritas = "🟢 PRIORITAS 5 - PANTAU"
        rekom_tindakan = f"✅ **PERFORMA SEHAT**\nROAS {roas_aktual:.1f}x ≥ BEP {roas_bep:.1f}x. Pertahankan setting saat ini dan pantau 3-5 hari."
    
    if ctr < 2 and clicks > 0 and "Stop Iklan" not in rekom_tindakan:
        rekom_tindakan += f"\n\n📸 **MASALAH CTR RENDAH!** CTR {ctr:.1f}% < 2%. Ganti Visual/Hook Video!"
    
    return rekom_tindakan, rekom_budget, rekom_roas, prioritas, warna

# ==================== 3. ACCESS CONTROL ====================
demo_expired = False
if st.session_state.demo_mode and st.session_state.demo_start_time:
    elapsed = (datetime.now() - st.session_state.demo_start_time).total_seconds()
    if elapsed > 300 or st.session_state.demo_analysis_count >= 2:
        demo_expired = True

if (not st.session_state.authenticated and not st.session_state.demo_mode) or demo_expired:
    st.markdown('<div style="text-align:center; padding-top:50px;">', unsafe_allow_html=True)
    if demo_expired:
        st.markdown('<h1 class="gold-header">⏰ TRIAL SELESAI</h1>', unsafe_allow_html=True)
        st.markdown('<h3>Akses demo habis. Upgrade sekarang untuk kontrol penuh!</h3>', unsafe_allow_html=True)
    else:
        st.markdown('<h1 class="gold-header" style="font-size:4.5rem;">🩺 DOCTOR ADS</h1>', unsafe_allow_html=True)
    
    st.markdown(f'<a href="{CHECKOUT_LINK}" target="_blank" class="cta-upgrade">💎 UNLOCK PREMIUM SEKARANG - RP147RB</a>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        with st.form("login"):
            st.markdown("### 🔐 Member Login")
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.form_submit_button("MASUK DASHBOARD"):
                if u == ADMIN_USERNAME and p == ADMIN_PASSWORD:
                    st.session_state.authenticated = True; st.session_state.demo_mode = False; st.rerun()
                else: st.error("Login Gagal!")
    with c2:
        if not demo_expired:
            st.markdown('<div class="premium-card"><h3>🎁 Demo Mode</h3>', unsafe_allow_html=True)
            if st.button("MULAI TRIAL"):
                st.session_state.demo_mode = True; st.session_state.demo_start_time = datetime.now(); st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ==================== 4. MAIN ELITE DASHBOARD ====================
st.markdown('<h1 class="gold-header">🩺 ADVERTISING COMMAND CENTER</h1>', unsafe_allow_html=True)

# --- FINANSIAL AUDIT ---
col_calc, col_audit = st.columns([2, 1])
with col_calc:
    st.markdown('<div class="premium-card"><h3>🎯 ROAS BEP Calculator</h3>', unsafe_allow_html=True)
    cb1, cb2, cb3 = st.columns(3)
    hj = cb1.number_input("Harga Jual (Rp)", value=150000)
    modal = cb2.number_input("Modal (Rp)", value=75000)
    admin_p = cb3.slider("Admin Platform %", 5, 30, 20)
    target_p = st.number_input("Target Profit (Rp)", value=0)
    
    laba_kotor_p = hj - modal - (hj * admin_p / 100)
    laba_setelah_p = laba_kotor_p - target_p
    roas_bep_p = hj / laba_setelah_p if laba_setelah_p > 0 else 999
    
    st.markdown(f'<div style="text-align:center;"><h1 style="color:#00E5A0; font-size:4rem; margin:0;">{roas_bep_p:.2f}x</h1><p style="color:#888;">TARGET ROAS BEP ANDA</p></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_audit:
    st.markdown('<div class="premium-card" style="height:100%;"><h3>📋 Kelayakan Produk</h3>', unsafe_allow_html=True)
    pernah = st.radio("Produk Pernah Laku?", ["Ya", "Tidak"], horizontal=True)
    if pernah == "Tidak": st.error("❌ Belum layak iklan!")
    else: st.success("✅ Produk layak beriklan!")
    st.markdown('</div>', unsafe_allow_html=True)

# --- ANALISIS IKLAN ---
st.markdown('<div class="premium-card"><h3>📊 Ad Performance Matrix</h3>', unsafe_allow_html=True)
ip1, ip2, ip3 = st.columns(3)
impressions = ip1.number_input("👁️ Impressions", value=20000)
clicks = ip1.number_input("🖱️ Clicks", value=600)
budget_spent = ip2.number_input("💸 Spent (Rp)", value=150000)
sales = ip2.number_input("💰 Revenue (Rp)", value=900000)
orders = ip3.number_input("📦 Orders", value=8)
budget_set = ip3.number_input("Budget Setting", value=200000)
target_roas_p = st.number_input("🎯 Target ROAS", value=6.0)

if st.button("RUN DEEP ANALYTICS", use_container_width=True):
    if st.session_state.demo_mode: st.session_state.demo_analysis_count += 1
    
    ctr_p = (clicks/impressions*100) if impressions > 0 else 0
    roas_akt_p = (sales/budget_spent) if budget_spent > 0 else 0
    s_rate_p = (budget_spent/budget_set*100) if budget_set > 0 else 0
    profit_est_p = (laba_kotor_p * orders) - budget_spent
    
    st.session_state.analysis_done = True
    
    m1, m2, m3, m4 = st.columns(4)
    m1.markdown(f'<div class="premium-card"><p class="metric-label">CTR</p><h2 class="metric-value">{ctr_p:.2f}%</h2></div>', unsafe_allow_html=True)
    m2.markdown(f'<div class="premium-card"><p class="metric-label">ROAS</p><h2 class="metric-value" style="color:#00E5A0;">{roas_akt_p:.2f}x</h2></div>', unsafe_allow_html=True)
    m3.markdown(f'<div class="premium-card"><p class="metric-label">PROFIT</p><h2 class="metric-value">{format_rp(profit_est_p)}</h2></div>', unsafe_allow_html=True)
    m4.markdown(f'<div class="premium-card"><p class="metric-label">BEP</p><h2 class="metric-value">{roas_bep_p:.2f}x</h2></div>', unsafe_allow_html=True)
    
    rekom_tindakan, rekom_budget, rekom_roas, prioritas, warna = generate_rekomendasi(
        roas_akt_p, roas_bep_p, s_rate_p, clicks, orders, budget_set, target_roas_p, budget_spent, ctr_p
    )
    
    bg_c = {"danger":"#fee2e2", "warning":"#fef3c7", "success":"#d1fae5", "info":"#dbeafe"}.get(warna, "#f0f0ff")
    br_c = {"danger":"#dc2626", "warning":"#f59e0b", "success":"#10b981", "info":"#3b82f6"}.get(warna, "#667eea")
    
    st.markdown(f"""
    <div style="background:{bg_c}; border-radius:1rem; padding:2rem; border-left:10px solid {br_c}; margin:1rem 0; color: #1a1a1a;">
        <h3 style="margin:0; font-weight: 800;">{prioritas}</h3>
        <p style="font-size:1.1rem; line-height:1.6;">{rekom_tindakan.replace(chr(10), '<br>')}</p>
        <p><strong>💰 Budget Rekomendasi:</strong> {format_rp(rekom_budget)} | <strong>🎯 Target ROAS:</strong> {rekom_roas:.1f}x</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ✨ AI LAB
st.markdown("<h2 class='gold-header'>✨ Elite AI Copywriter</h2>", unsafe_allow_html=True)
tab1, tab2, tab3 = st.tabs(["📝 SEO Title", "🎥 TikTok Viral", "🎬 Hooks"])
with tab1:
    p_name = st.text_input("🏷️ Nama Produk", placeholder="Contoh: Kaos Oversize Premium")
    if st.button("Generate SEO Titles"):
        with st.spinner("AI Merancang..."):
            res = call_gemini_api(f"Buat 5 Judul Shopee SEO untuk {p_name}")
            st.code(res if res else f"🔥 {p_name} Best Seller", language="text")

st.markdown(f'<div style="text-align:center; padding:60px;"><a href="{CHECKOUT_LINK}" target="_blank" class="cta-upgrade">💎 UPGRADE PREMIUM - AKSES TANPA BATAS</a></div>', unsafe_allow_html=True)
