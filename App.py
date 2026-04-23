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

    /* Kontras Tinggi untuk Form & Label */
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

    .stButton>button {
        background: linear-gradient(135deg, #00E5A0 0%, #00a878 100%);
        color: #020617 !important; 
        font-weight: 800; border: none; border-radius: 15px; padding: 20px;
        text-transform: uppercase; letter-spacing: 1.5px; width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# ==================== 2. CORE LOGIC ====================
if "authenticated" not in st.session_state: st.session_state["authenticated"] = False
if "demo_mode" not in st.session_state: st.session_state["demo_mode"] = False
if "demo_start_time" not in st.session_state: st.session_state["demo_start_time"] = None

ADMIN_USERNAME = "arkidigital"
ADMIN_PASSWORD = "Arkidigital2026"
CHECKOUT_LINK = "https://muhammad-masruri.myscalev.com/checkout-pageku"

# Ambil API KEY
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
GEMINI_AVAILABLE = True if GEMINI_API_KEY else False

def call_gemini_api(prompt):
    if not GEMINI_API_KEY: return None
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    try:
        r = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=25)
        res = r.json()
        return res["candidates"][0]["content"]["parts"][0]["text"]
    except: return None

def format_rp(angka):
    if angka >= 1_000_000: return f"Rp{angka/1_000_000:.1f}JT"
    if angka >= 1000: return f"Rp{angka/1000:.0f}RB"
    return f"Rp{angka:,.0f}"

# ==================== 3. APP INTERFACE ====================
st.set_page_config(page_title="Doctor Ads Elite", page_icon="🩺", layout="wide")
apply_premium_style()

if not st.session_state.authenticated and not st.session_state.demo_mode:
    st.markdown('<div style="text-align:center; padding-top:80px;">', unsafe_allow_html=True)
    st.markdown('<h1 class="gold-header" style="font-size:4rem;">🩺 DOCTOR ADS</h1>', unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap="large")
    with c1:
        with st.form("login"):
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.form_submit_button("LOGIN PREMIUM"):
                if u == ADMIN_USERNAME and p == ADMIN_PASSWORD:
                    st.session_state.authenticated = True; st.rerun()
                else: st.error("Salah!")
    with c2:
        st.markdown('<div class="premium-card"><h3>🎁 Demo Mode</h3>', unsafe_allow_html=True)
        if st.button("MULAI COBA GRATIS"):
            st.session_state.demo_mode = True; st.session_state.demo_start_time = datetime.now(); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- HEADER ---
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

# 📊 INPUT DATA IKLAN
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
    ctr = (clicks/impressions*100) if impressions > 0 else 0
    roas_aktual = (sales/budget_spent) if budget_spent > 0 else 0
    budget_terserap_persen = (budget_spent/budget_set*100) if budget_set > 0 else 0
    profit_estimasi = (laba_kotor * orders) - budget_spent

    # METRICS DISPLAY
    m1, m2, m3, m4 = st.columns(4)
    m1.markdown(f'<div class="premium-card"><p class="metric-lab">CTR</p><p class="metric-val">{ctr:.2f}%</p></div>', unsafe_allow_html=True)
    m2.markdown(f'<div class="premium-card"><p class="metric-lab">ROAS AKTUAL</p><p class="metric-val" style="color:#00E5A0 !important;">{roas_aktual:.2f}x</p></div>', unsafe_allow_html=True)
    m3.markdown(f'<div class="premium-card"><p class="metric-lab">EST. NET PROFIT</p><p class="metric-val">{format_rp(profit_estimasi)}</p></div>', unsafe_allow_html=True)
    m4.markdown(f'<div class="premium-card"><p class="metric-lab">ROAS BEP</p><p class="metric-val">{roas_bep:.2f}x</p></div>', unsafe_allow_html=True)

    # ==================== LOGIC REKOMENDASI KERJA ====================
    st.markdown("---")
    st.subheader("🎯 **Kesimpulan & Rekomendasi**")
    
    rekomendasi_tindakan = ""
    rekomendasi_roas = target_roas
    rekomendasi_budget = budget_set
    prioritas = ""
    warna = "info"
    
    if clicks > 50 and budget_terserap_persen >= 80 and orders == 0:
        rekomendasi_tindakan = f"""
        🔴 **PRIORITAS 1 - HENTIKAN IKLAN SEGERA!** 📊 Data: {clicks} klik, budget terserap {budget_terserap_persen:.0f}%, tapi 0 order.  
        **Penyebab:** Produk belum layak iklan.  
        **Yang harus dilakukan:** 1. Cek harga produk — apakah lebih murah atau setara kompetitor?  
        2. Tambah review & rating (minimal 10-20 review positif)  
        3. Perbaiki deskripsi — fokus ke MANFAAT  
        4. Pastikan stok aman dan produk dibutuhkan pasar  
        **Setelah produk siap, restart iklan dengan budget kecil (Rp50-100rb/hari).**
        """
        prioritas = "🔴 PRIORITAS 1 - URGENT (Stop Iklan)"
        warna = "danger"
    elif budget_terserap_persen >= 85 and roas_aktual >= roas_bep * 1.2:
        new_budget = budget_set * 1.3
        rekomendasi_tindakan = f"""
        🟢 **PRIORITAS 4 - SIAP SCALE** ROAS {roas_aktual:.1f}x > BEP {roas_bep:.1f}x (untung)  
        Budget terserap {budget_terserap_persen:.0f}% (hampir habis)  
        ✅ Naikkan **BUDGET 30%** menjadi Rp{new_budget:,.0f}  
        ✅ **PERTAHANKAN** target ROAS di {target_roas:.1f}x  
        ⏰ Tunggu **3 hari** tanpa perubahan apapun.
        """
        rekomendasi_budget = new_budget
        prioritas = "🟢 PRIORITAS 4 - SCALE (Naik Budget 30%)"
        warna = "success"
    elif roas_aktual >= roas_bep and budget_terserap_persen < 85:
        new_target = target_roas - 0.5
        rekomendasi_tindakan = f"""
        🟡 **PRIORITAS 2 - OPTIMASI** ROAS {roas_aktual:.1f}x ≥ BEP {roas_bep:.1f}x (untung)  
        Budget terserap {budget_terserap_persen:.0f}% (masih sisa)  
        ✅ Turunkan target ROAS **0.5 poin** menjadi **{new_target:.1f}x** ✅ **JANGAN UBAH BUDGET** (tetap Rp{budget_set:,.0f})  
        ⏰ Tunggu **3 hari** tanpa perubahan.
        """
        rekomendasi_roas = new_target
        prioritas = "🟡 PRIORITAS 2 - OPTIMASI (Turun ROAS)"
        warna = "warning"
    elif roas_aktual < roas_bep and roas_aktual > 0:
        new_target = roas_bep + 0.5
        rekomendasi_tindakan = f"""
        🔴 **PRIORITAS 3 - IKLAN RUGI** ROAS {roas_aktual:.1f}x < BEP {roas_bep:.1f}x  
        ✅ Naikkan target ROAS **0.5 poin** menjadi **{new_target:.1f}x** ✅ **JANGAN UBAH BUDGET** (tetap Rp{budget_set:,.0f})  
        ⏰ Tunggu **3 hari** tanpa perubahan.
        """
        rekomendasi_roas = new_target
        prioritas = "🔴 PRIORITAS 3 - URGENT (Naik ROAS)"
        warna = "danger"
    elif roas_aktual >= roas_bep:
        rekomendasi_tindakan = f"""
        ✅ **PERFORMA SEHAT** ROAS {roas_aktual:.1f}x ≥ BEP {roas_bep:.1f}x  
        Budget terserap {budget_terserap_persen:.0f}%  
        ✅ Pertahankan setting saat ini  
        ⏰ Pantau 3-5 hari tanpa perubahan
        """
        prioritas = "🟢 PRIORITAS 5 - PANTAU"
        warna = "info"

    if ctr < 2 and clicks > 0 and "Stop Iklan" not in rekomendasi_tindakan:
        rekomendasi_tindakan += f"\n\n---\n📸 **CTR Rendah** ({ctr:.1f}% < 2%)\nSolusi: Ganti visual (foto/video hook). Buat 3 variasi kreatif baru."

    bg_color = {"danger":"#fee2e2", "warning":"#fef3c7", "success":"#d1fae5", "info":"#dbeafe"}.get(warna, "#f0f0ff")
    border_color = {"danger":"#dc2626", "warning":"#f59e0b", "success":"#10b981", "info":"#3b82f6"}.get(warna, "#667eea")
    
    st.markdown(f"""
    <div style="background:{bg_color}; border-radius:1rem; padding:1.5rem; border-left:8px solid {border_color}; margin:1rem 0; color: #1a1a1a;">
        <h4 style="margin:0 0 0.5rem 0; font-weight: 800;">{prioritas}</h4>
        <div style="font-size: 1rem; line-height: 1.6;">{rekomendasi_tindakan.replace(chr(10), '<br>')}</div>
        <hr style="border: 0.5px solid {border_color}; opacity: 0.3;">
        <p style="margin:0;"><strong>💰 Budget rekomendasi:</strong> {format_rp(rekomendasi_budget)} &nbsp;|&nbsp; <strong>🎯 Target ROAS rekomendasi:</strong> {rekomendasi_roas:.1f}x</p>
    </div>
    """, unsafe_allow_html=True)

    # AI INSIGHTS
    if GEMINI_AVAILABLE and roas_aktual > 0:
        st.markdown("---")
        with st.spinner("AI sedang merancang strategi..."):
            advice = call_gemini_api(f"Analisis iklan: ROAS {roas_aktual:.1f}x (BEP {roas_bep:.1f}x). Berikan strategi scale harian.")
            if advice: st.info(f"💡 AI STRATEGY: {advice}")

st.markdown('</div>', unsafe_allow_html=True)

# ✨ AI GENERATOR
st.markdown("<h2 class='gold-header'>✨ Elite Copywriting Lab</h2>", unsafe_allow_html=True)
p_name = st.text_input("🏷️ Nama Produk", placeholder="Contoh: Kaos Oversize Premium")
tabs = st.tabs(["🛍️ Shopee SEO", "🎥 TikTok Viral Story", "🎬 Hooks"])

with tabs[0]:
    if st.button("Generate SEO Titles"):
        with st.spinner("AI Menulis..."):
            res = call_gemini_api(f"Buat 5 Judul Shopee SEO Premium untuk {p_name}")
            st.code(res if res else "API ERROR: Periksa koneksi atau API Key Anda.", language="text")

with tabs[1]:
    if st.button("Generate TikTok Viral Copy"):
        with st.spinner("AI Menulis..."):
            res = call_gemini_api(f"Buat copy TikTok storytelling viral untuk {p_name}")
            st.code(res if res else "API ERROR: Periksa koneksi atau API Key Anda.", language="markdown")

with tabs[2]:
    if st.button("Generate Viral Hooks"):
        with st.spinner("AI Menulis..."):
            res = call_gemini_api(f"Buat 5 hook video TikTok yang bikin stop scrolling untuk {p_name}")
            st.info(res if res else "API ERROR: Periksa koneksi atau API Key Anda.")

st.markdown(f'<div style="text-align:center; padding:50px; color:#FFFFFF; opacity:0.8;">© 2026 Arkidigital Premier | <a href="{CHECKOUT_LINK}" style="color:#00E5A0; text-decoration:none;">UPGRADE ACCESS</a></div>', unsafe_allow_html=True)
