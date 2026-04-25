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
    initial_sidebar_state="expanded"
)

# 2. CSS untuk menyembunyikan header default Streamlit
hide_st_style = """
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
.stAppDeployButton {display:none;}
[data-testid="stToolbar"] {display:none;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# ==================== 1. ULTRA-PREMIUM UI CONFIGURATION ====================
def apply_premium_style():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700;800&display=swap');
    
    html, body, [class*="css"] { 
        font-family: 'Plus Jakarta Sans', sans-serif; 
        color: #E2E8F0 !important; 
    }
    
    h1, h2, h3, h4, h5, h6, p, label, .stMarkdown {
        color: #E2E8F0 !important;
    }
    
    .premium-card, .premium-card p, .premium-card h1, .premium-card h2, .premium-card h3 {
        color: #E2E8F0 !important;
    }
    
    .stApp { 
        background: radial-gradient(circle at 2% 2%, #1e1b4b 0%, #020617 100%); 
    }

    .premium-card {
        background: rgba(255, 255, 255, 0.08); 
        backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.2); 
        border-radius: 24px;
        padding: 30px;
        margin-bottom: 25px;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.7);
    }
    
    .gold-header {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        text-shadow: none;
    }
    
    .text-profit {
        color: #00E5A0 !important;
        font-weight: bold;
    }
    
    .text-loss {
        color: #FF6B6B !important;
        font-weight: bold;
    }

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

    .stNumberInput input, .stTextInput input, .stSelectbox div, .stTextArea textarea {
        background: rgba(15, 25, 45, 0.9) !important; 
        border: 1px solid rgba(255, 255, 255, 0.2) !important; 
        border-radius: 12px !important; 
        color: #FFFFFF !important;
        font-size: 1rem !important;
        padding: 10px !important;
    }
    
    .stNumberInput input:focus, .stTextInput input:focus, .stSelectbox div:focus {
        border-color: #00E5A0 !important;
        box-shadow: 0 0 0 2px rgba(0, 229, 160, 0.2) !important;
    }
    
    .stButton button {
        background: linear-gradient(135deg, #00E5A0 0%, #00a878 100%) !important;
        color: #020617 !important;
        font-weight: 800 !important;
        font-size: 1.2rem !important;
        padding: 12px 30px !important;
        border-radius: 40px !important;
        border: none !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        box-shadow: 0 5px 15px rgba(0, 229, 160, 0.3) !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(0, 229, 160, 0.5) !important;
    }
    
    .rekom-danger {
        background: linear-gradient(135deg, #450a0a 0%, #7f1d1d 100%);
        border-left: 5px solid #ef4444;
        border-radius: 16px;
        padding: 20px;
        margin: 15px 0;
    }
    
    .rekom-danger h3, .rekom-danger p, .rekom-danger strong {
        color: #fecaca !important;
    }
    
    .rekom-warning {
        background: linear-gradient(135deg, #451a03 0%, #78350f 100%);
        border-left: 5px solid #f59e0b;
        border-radius: 16px;
        padding: 20px;
        margin: 15px 0;
    }
    
    .rekom-warning h3, .rekom-warning p, .rekom-warning strong {
        color: #fde68a !important;
    }
    
    .rekom-success {
        background: linear-gradient(135deg, #064e3b 0%, #0d9488 100%);
        border-left: 5px solid #10b981;
        border-radius: 16px;
        padding: 20px;
        margin: 15px 0;
    }
    
    .rekom-success h3, .rekom-success p, .rekom-success strong {
        color: #a7f3d0 !important;
    }
    
    .rekom-info {
        background: linear-gradient(135deg, #0c4a6e 0%, #0284c7 100%);
        border-left: 5px solid #3b82f6;
        border-radius: 16px;
        padding: 20px;
        margin: 15px 0;
    }
    
    .rekom-info h3, .rekom-info p, .rekom-info strong {
        color: #bae6fd !important;
    }
    
    .generator-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        border-radius: 20px;
        padding: 20px;
        margin: 10px 0;
        transition: all 0.3s ease;
    }
    
    .generator-card:hover {
        border-color: #00E5A0;
        transform: translateY(-2px);
    }
    
    .stCodeBlock {
        background: #0f172a !important;
        border-radius: 12px !important;
        border: 1px solid #334155 !important;
    }
    
    .stCodeBlock div {
        color: #E2E8F0 !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(15, 25, 45, 0.5);
        border-radius: 40px;
        padding: 6px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 32px;
        padding: 8px 20px;
        font-weight: 600;
        color: #94A3B8 !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00E5A0 0%, #00a878 100%) !important;
        color: #020617 !important;
    }
    
    .metric-value {
        color: #FFFFFF !important;
        font-size: 2rem;
        font-weight: bold;
    }
    
    .metric-label {
        color: #94A3B8 !important;
        font-size: 0.8rem;
    }
    
    .stAlert {
        color: #000000 !important;
    }
    
    .analytics-wrapper {
        background: rgba(15, 25, 45, 0.6);
        border-radius: 20px;
        padding: 20px;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

apply_premium_style()

# ==================== 2. SESSION STATE ====================
if "authenticated" not in st.session_state: 
    st.session_state["authenticated"] = False
if "products" not in st.session_state: 
    st.session_state["products"] = []
if "analysis_done" not in st.session_state: 
    st.session_state["analysis_done"] = False
if "last_ctr" not in st.session_state: 
    st.session_state["last_ctr"] = 0
if "last_roas" not in st.session_state: 
    st.session_state["last_roas"] = 0
if "last_roas_bep" not in st.session_state: 
    st.session_state["last_roas_bep"] = 0
if "last_s_rate" not in st.session_state: 
    st.session_state["last_s_rate"] = 0
if "last_clicks" not in st.session_state: 
    st.session_state["last_clicks"] = 0
if "last_orders" not in st.session_state: 
    st.session_state["last_orders"] = 0
if "last_profit" not in st.session_state: 
    st.session_state["last_profit"] = 0
if "last_budget_set" not in st.session_state: 
    st.session_state["last_budget_set"] = 0
if "last_target_roas" not in st.session_state: 
    st.session_state["last_target_roas"] = 0
if "last_budget_spent" not in st.session_state: 
    st.session_state["last_budget_spent"] = 0

ADMIN_USERNAME = st.secrets.get("ADMIN_USERNAME", "arkidigital")
ADMIN_PASSWORD = st.secrets.get("ADMIN_PASSWORD", "Arkidigital2026")
CHECKOUT_LINK = "https://muhammad-masruri.myscalev.com/checkout-pageku"
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")

def format_rp(angka):
    if angka >= 1_000_000: 
        return f"Rp{angka/1_000_000:.1f}JT"
    if angka >= 1000: 
        return f"Rp{angka/1000:.0f}RB"
    return f"Rp{angka:,.0f}"

# ==================== FUNGSI CALL GEMINI API ====================
def call_gemini_api(prompt):
    """Panggil Gemini API via HTTP - DEBUG VERSION"""
    if not GEMINI_API_KEY:
        return "❌ API Key tidak ditemukan di secrets"
    
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=30)
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("**🤖 API Debug Info:**")
        st.sidebar.write(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            try:
                text = result["candidates"][0]["content"]["parts"][0]["text"]
                st.sidebar.success("✅ API berhasil!")
                return text
            except Exception as e:
                st.sidebar.error(f"Parse error: {e}")
                return f"❌ Gagal parsing response: {e}"
        else:
            st.sidebar.error(f"HTTP {response.status_code}")
            st.sidebar.write(f"Response: {response.text[:300]}")
            return f"❌ API Error {response.status_code}"
            
    except requests.exceptions.Timeout:
        st.sidebar.error("⏰ Timeout (30 detik)")
        return "❌ Timeout, coba lagi"
    except Exception as e:
        st.sidebar.error(f"Exception: {type(e).__name__}")
        st.sidebar.write(f"Detail: {str(e)[:200]}")
        return f"❌ Error: {str(e)[:100]}"

# ==================== DATABASE PRODUK ====================
def save_product(p):
    products = st.session_state.products
    for i, prod in enumerate(products):
        if prod["nama"] == p["nama"]:
            products[i] = p
            st.session_state.products = products
            return
    products.append(p)
    st.session_state.products = products

def delete_product(nama):
    products = st.session_state.products
    st.session_state.products = [p for p in products if p["nama"] != nama]

# ==================== FUNGSI REKOMENDASI ====================
def generate_rekomendasi(roas_aktual, roas_bep, s_rate, clicks, orders, budget_set, target_roas, budget_spent, ctr):
    """Menghasilkan rekomendasi berdasarkan aturan 1-5"""
    rekom_tindakan = ""
    rekom_roas = target_roas
    rekom_budget = budget_set
    prioritas = ""
    warna = "info"
    
    if clicks > 50 and s_rate >= 80 and orders == 0:
        prioritas = "🔴 PRIORITAS 1 - URGENT (Stop Iklan)"
        warna = "danger"
        rekom_budget = 0
        rekom_tindakan = f"""🚨 **HENTIKAN IKLAN SEGERA!**

📊 Data: {clicks} klik, budget terserap {s_rate:.0f}%, tapi 0 order.

**Penyebab:** Produk belum layak iklan.

**Yang harus dilakukan:**
1. Cek harga produk — bandingkan dengan kompetitor
2. Tambah review & rating (target 10-20 review positif)
3. Perbaiki deskripsi — fokus ke MANFAAT
4. Pastikan stok aman

**Setelah produk siap, restart iklan dengan budget kecil (Rp50-100rb/hari).**"""
    
    elif s_rate >= 85 and roas_aktual >= roas_bep * 1.2:
        prioritas = "🟢 PRIORITAS 4 - SIAP SCALE"
        warna = "success"
        rekom_budget = budget_set * 1.3
        rekom_tindakan = f"""🚀 **SIAP SCALE!**

📈 ROAS {roas_aktual:.1f}x > BEP {roas_bep:.1f}x (untung)
💰 Budget terserap {s_rate:.0f}% (hampir habis)

**Aturan SCALE yang benar:**
✅ Naikkan **BUDGET 30%** menjadi {format_rp(rekom_budget)}
✅ **PERTAHANKAN** target ROAS di {target_roas:.1f}x

⏰ **Tunggu 3 hari** tanpa perubahan apapun."""
    
    elif roas_aktual >= roas_bep and s_rate < 85:
        prioritas = "🟡 PRIORITAS 2 - OPTIMASI"
        warna = "warning"
        rekom_roas = target_roas - 0.5
        rekom_tindakan = f"""⚡ **OPTIMASI BUDGET**

✅ ROAS {roas_aktual:.1f}x ≥ BEP {roas_bep:.1f}x (untung)
📊 Budget terserap {s_rate:.0f}% (masih ada sisa Rp{budget_set - budget_spent:,.0f})

**Agar budget habis dan order maksimal:**
✅ Turunkan target ROAS **0.5 poin** menjadi **{rekom_roas:.1f}x**
✅ **JANGAN UBAH BUDGET** (tetap {format_rp(budget_set)})

⏰ **Tunggu 3 hari** tanpa perubahan apapun."""
    
    elif roas_aktual < roas_bep and roas_aktual > 0:
        prioritas = "🔴 PRIORITAS 3 - IKLAN RUGI"
        warna = "danger"
        rekom_roas = roas_bep + 0.5
        rekom_budget = budget_set * 0.7
        rekom_tindakan = f"""💸 **IKLAN RUGI!**

📉 ROAS {roas_aktual:.1f}x < BEP {roas_bep:.1f}x

**Solusi:**
✅ Naikkan target ROAS **0.5 poin** menjadi **{rekom_roas:.1f}x**
🔻 Turunkan budget **30%** menjadi {format_rp(rekom_budget)} untuk mengurangi kerugian"""
    
    elif roas_aktual >= roas_bep:
        prioritas = "🟢 PRIORITAS 5 - PANTAU"
        rekom_tindakan = f"""✅ **PERFORMA SEHAT**

📈 ROAS {roas_aktual:.1f}x ≥ BEP {roas_bep:.1f}x
💰 Budget terserap {s_rate:.0f}%

**Rekomendasi:**
✅ Pertahankan setting saat ini
⏰ Pantau selama **3-5 hari** tanpa perubahan"""
    
    if ctr < 2 and clicks > 0 and "Stop Iklan" not in rekom_tindakan:
        rekom_tindakan += f"""

---
📸 **MASALAH CTR RENDAH!**

CTR {ctr:.1f}% < 2% → Iklan kurang menarik.

**Solusi:** Ganti visual (foto utama / video hook 3 detik pertama). Buat 3 variasi kreatif baru."""
    
    return rekom_tindakan, rekom_budget, rekom_roas, prioritas, warna

# ==================== 3. ACCESS CONTROL (PREMIUM ONLY) ====================
if not st.session_state.authenticated:
    st.markdown('<div style="text-align:center; padding-top:50px;">', unsafe_allow_html=True)
    st.markdown('<h1 class="gold-header" style="font-size:4.5rem;">🩺 DOCTOR ADS</h1>', unsafe_allow_html=True)
    st.markdown('<h3 style="margin-bottom:30px;">Premium Advertising Command Center</h3>', unsafe_allow_html=True)
    
    st.markdown(f'<a href="{CHECKOUT_LINK}" target="_blank" class="cta-upgrade">💎 UNLOCK PREMIUM - RP147RB</a>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        with st.form("login_form"):
            st.markdown("### 🔐 Member Login")
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                submitted = st.form_submit_button("MASUK", use_container_width=True)
            with col_btn2:
                if st.form_submit_button("LOGOUT", use_container_width=True):
                    st.session_state.clear()
                    st.rerun()
            
            if submitted:
                if u == ADMIN_USERNAME and p == ADMIN_PASSWORD:
                    st.session_state.authenticated = True
                    st.session_state.analysis_done = False
                    st.rerun()
                else:
                    st.error("❌ Username atau Password salah!")
    
    st.stop()

# ==================== 4. MAIN PREMIUM DASHBOARD ====================
st.markdown('<h1 class="gold-header">🩺 ADVERTISING COMMAND CENTER</h1>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 📦 **Produk Database**")
    
    with st.expander("➕ Simpan Produk Baru"):
        nama_produk_db = st.text_input("Nama Produk", key="nama_produk_db")
        hj_db = st.number_input("Harga Jual", min_value=1000, value=100000, key="hj_db")
        modal_db = st.number_input("Modal", min_value=500, value=60000, key="modal_db")
        admin_db = st.slider("Admin %", 5, 30, 20, key="admin_db")
        if st.button("💾 Simpan ke Database", key="simpan_db") and nama_produk_db:
            admin_nom = hj_db * admin_db / 100
            laba_db = hj_db - modal_db - admin_nom
            roas_db = hj_db / laba_db if laba_db > 0 else 999
            save_product({"nama": nama_produk_db, "harga_jual": hj_db, "modal": modal_db, "admin_persen": admin_db, "laba_kotor": laba_db, "roas_bep": roas_db})
            st.success(f"✅ {nama_produk_db} tersimpan!")
    
    if st.session_state.products:
        pilih_produk = st.selectbox("Pilih Produk", ["-- Pilih --"] + [p["nama"] for p in st.session_state.products], key="pilih_produk_sidebar")
        if pilih_produk != "-- Pilih --":
            prod = next(p for p in st.session_state.products if p["nama"] == pilih_produk)
            st.info(f"ROAS BEP: {prod['roas_bep']:.1f}x | Laba: Rp{prod['laba_kotor']:,.0f}")
            if st.button("🗑️ Hapus Produk", key="hapus_produk_sidebar"):
                delete_product(pilih_produk)
                st.rerun()
    
    st.markdown("---")
    st.markdown('<div style="text-align:center; background:rgba(0,229,160,0.2); padding:10px; border-radius:40px;"><span style="color:#00E5A0;">⭐ PREMIUM MEMBER ⭐</span></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button("🚪 LOGOUT", use_container_width=True):
        st.session_state.clear()
        st.rerun()

col_calc, col_audit = st.columns([2, 1])
with col_calc:
    st.markdown('<div class="premium-card"><h3>🎯 ROAS BEP Calculator</h3>', unsafe_allow_html=True)
    cb1, cb2, cb3 = st.columns(3)
    hj = cb1.number_input("Harga Jual (Rp)", min_value=1000, value=150000, key="hj_main")
    modal = cb2.number_input("Modal (Rp)", min_value=500, value=75000, key="modal_main")
    admin_p = cb3.slider("Admin Platform %", 5, 30, 20, key="admin_main")
    target_p = st.number_input("Target Profit (Rp)", min_value=0, value=0, key="target_main")
    
    laba_kotor_p = hj - modal - (hj * admin_p / 100)
    laba_setelah_p = laba_kotor_p - target_p
    roas_bep_p = hj / laba_setelah_p if laba_setelah_p > 0 else 999
    
    st.markdown(f'<div style="text-align:center;"><h1 style="color:#00E5A0; font-size:4rem; margin:0;">{roas_bep_p:.2f}x</h1><p style="color:#94A3B8;">TARGET ROAS BEP ANDA</p></div>', unsafe_allow_html=True)
    
    if st.session_state.products:
        st.markdown("---")
        st.markdown("**📋 Produk Tersimpan:**")
        for prod in st.session_state.products:
            st.markdown(f"- {prod['nama']} → BEP: {prod['roas_bep']:.1f}x | Profit: Rp{prod['laba_kotor']:,.0f}")
    
    st.markdown('</div>', unsafe_allow_html=True)

with col_audit:
    st.markdown('<div class="premium-card" style="height:100%;"><h3>📋 Kelayakan Iklan</h3>', unsafe_allow_html=True)
    pernah = st.radio("Produk Pernah Laku?", ["Ya", "Tidak"], horizontal=True, key="pernah_laku_main")
    if pernah == "Tidak": 
        st.error("❌ Belum layak iklan! Validasi produk dulu.")
        st.info("💡 Saran: Kumpulkan minimal 10 review positif terlebih dahulu.")
    else:
        h_komp = st.number_input("Harga Kompetitor", min_value=1000, value=140000, key="harga_komp_main")
        if hj > h_komp * 1.2: 
            st.warning("⚠️ Harga terlalu mahal. Turunkan atau tambah value produk.")
        elif laba_kotor_p < 5000: 
            st.error("❌ Margin terlalu tipis. Cari produk lain atau naikkan harga.")
        else:
            st.success("✅ Produk layak beriklan!")
            if laba_kotor_p > 20000:
                st.balloons()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="premium-card"><h3>📊 Ad Performance Matrix</h3>', unsafe_allow_html=True)
ip1, ip2, ip3 = st.columns(3)
impressions = ip1.number_input("👁️ Impressions", min_value=0, value=20000, key="imp_main")
clicks = ip1.number_input("🖱️ Clicks", min_value=0, value=600, key="clicks_main")
budget_spent = ip2.number_input("💸 Spent (Rp)", min_value=0, value=150000, key="spent_main")
sales = ip2.number_input("💰 Revenue (Rp)", min_value=0, value=900000, key="sales_main")
orders = ip3.number_input("📦 Orders", min_value=0, value=8, key="orders_main")
budget_set = ip3.number_input("Budget Setting (Rp)", min_value=0, value=200000, key="budget_set_main")
target_roas_p = st.number_input("🎯 Target ROAS", min_value=0.5, value=6.0, step=0.5, key="target_roas_main")

col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    analize_clicked = st.button("⚡ RUN DEEP ANALYTICS", use_container_width=True, key="run_analytics")

if analize_clicked:
    ctr_p = (clicks / impressions * 100) if impressions > 0 else 0
    roas_akt_p = (sales / budget_spent) if budget_spent > 0 else 0
    s_rate_p = (budget_spent / budget_set * 100) if budget_set > 0 else 0
    profit_est_p = (laba_kotor_p * orders) - budget_spent if orders > 0 else -budget_spent
    
    st.session_state.analysis_done = True
    st.session_state.last_ctr = ctr_p
    st.session_state.last_roas = roas_akt_p
    st.session_state.last_roas_bep = roas_bep_p
    st.session_state.last_s_rate = s_rate_p
    st.session_state.last_clicks = clicks
    st.session_state.last_orders = orders
    st.session_state.last_profit = profit_est_p
    st.session_state.last_budget_set = budget_set
    st.session_state.last_budget_spent = budget_spent
    st.session_state.last_target_roas = target_roas_p
    
    st.markdown('<div class="analytics-wrapper">', unsafe_allow_html=True)
    
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f'<div class="premium-card"><p style="color:#94A3B8; margin:0;">📈 CTR</p><h2 style="color:#FFFFFF; margin:0;">{ctr_p:.2f}%</h2><p style="color:#94A3B8; font-size:0.8rem;">{"✅ Normal" if ctr_p >= 2 else "⚠️ Rendah"}</p></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="premium-card"><p style="color:#94A3B8; margin:0;">💰 ROAS</p><h2 style="color:#00E5A0; margin:0;">{roas_akt_p:.2f}x</h2><p style="color:#94A3B8; font-size:0.8rem;">{"🟢 Profit" if roas_akt_p >= roas_bep_p else "🔴 Rugi"}</p></div>', unsafe_allow_html=True)
    with m3:
        profit_color = "#00E5A0" if profit_est_p > 0 else "#FF6B6B"
        st.markdown(f'<div class="premium-card"><p style="color:#94A3B8; margin:0;">💎 PROFIT</p><h2 style="color:{profit_color}; margin:0;">{format_rp(profit_est_p)}</h2><p style="color:#94A3B8; font-size:0.8rem;">{"Untung" if profit_est_p > 0 else "Rugi"}</p></div>', unsafe_allow_html=True)
    with m4:
        st.markdown(f'<div class="premium-card"><p style="color:#94A3B8; margin:0;">🎯 BEP</p><h2 style="color:#FFFFFF; margin:0;">{roas_bep_p:.2f}x</h2><p style="color:#94A3B8; font-size:0.8rem;">{"✅ Aman" if roas_akt_p >= roas_bep_p else "⚠️ Dibawah"}</p></div>', unsafe_allow_html=True)
    
    if GEMINI_API_KEY:
        with st.spinner("🤖 AI sedang menganalisis..."):
            summary_prompt = f"""Berdasarkan data iklan:
- CTR: {ctr_p:.1f}%
- ROAS: {roas_akt_p:.1f}x
- BEP: {roas_bep_p:.1f}x
- Budget terserap: {s_rate_p:.0f}%
- Order: {orders} dari {clicks} klik
- Profit: {format_rp(profit_est_p)}

Buat kesimpulan SINGKAT (maks 60 kata) dalam bahasa Indonesia. Sebutkan apakah iklan UNTUNG atau RUGI, dan rekomendasi singkat.
"""
            ai_summary = call_gemini_api(summary_prompt)
            if ai_summary and not ai_summary.startswith("❌"):
                st.markdown(f'<div class="premium-card"><h3 style="color:#FFD700;">🤖 AI Insight</h3><p style="font-size:1rem;">{ai_summary}</p></div>', unsafe_allow_html=True)
    
    st.markdown("### 🎯 Rekomendasi Strategis")
    
    rekom_tindakan, rekom_budget, rekom_roas, prioritas, warna = generate_rekomendasi(
        roas_akt_p, roas_bep_p, s_rate_p, clicks, orders, 
        budget_set, target_roas_p, budget_spent, ctr_p
    )
    
    if warna == "danger":
        rekom_class = "rekom-danger"
    elif warna == "warning":
        rekom_class = "rekom-warning"
    elif warna == "success":
        rekom_class = "rekom-success"
    else:
        rekom_class = "rekom-info"
    
    st.markdown(f"""
    <div class="{rekom_class}">
        <h3 style="margin:0 0 10px 0;">{prioritas}</h3>
        <p style="font-size:1rem; line-height:1.6;">{rekom_tindakan.replace(chr(10), '<br>')}</p>
        <hr style="border:0.5px solid rgba(255,255,255,0.2); margin:15px 0;">
        <p><strong>💰 Budget Rekomendasi:</strong> {format_rp(rekom_budget)} | <strong>🎯 Target ROAS:</strong> {rekom_roas:.1f}x</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.analysis_done and st.session_state.last_roas >= st.session_state.last_roas_bep * 1.2:
    st.markdown('<div class="premium-card"><h3 style="color:#FFD700;">📈 Prediksi Scale</h3>', unsafe_allow_html=True)
    new_budget_pred = st.session_state.last_budget_set * 1.3
    prediksi_profit = st.session_state.last_profit * 1.25
    
    st.markdown(f"""
    <div style="background:rgba(0,229,160,0.1); border-radius:16px; padding:1.5rem;">
        <p><strong>💰 Jika Naikkan Budget 30%:</strong> {format_rp(new_budget_pred)}/hari</p>
        <p><strong>📈 Estimasi ROAS:</strong> {st.session_state.last_roas * 0.95:.1f}x - {st.session_state.last_roas * 1.05:.1f}x</p>
        <p><strong>💎 Estimasi Profit:</strong> {format_rp(prediksi_profit)}/hari</p>
        <p><strong>⚠️ Level Resiko:</strong> Rendah</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.analysis_done and st.session_state.last_roas > 0:
    st.markdown('<div class="premium-card"><h3 style="color:#FFD700;">📊 Prediksi 7 Hari ke Depan</h3>', unsafe_allow_html=True)
    
    if st.session_state.last_roas >= st.session_state.last_roas_bep:
        trend = "stabil" if st.session_state.last_s_rate > 70 else "meningkat"
        prediksi = f"💰 Kemungkinan ROAS akan {trend} di kisaran {st.session_state.last_roas * 0.9:.1f}x - {st.session_state.last_roas * 1.1:.1f}x"
    else:
        prediksi = f"⚠️ ROAS saat ini di bawah BEP. Segera ambil tindakan koreksi sesuai rekomendasi di atas."
    
    st.markdown(f"""
    <div style="background:rgba(255,215,0,0.1); border-radius:16px; padding:1.5rem;">
        <p>{prediksi}</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.analysis_done and st.session_state.last_roas > 0:
    st.markdown('<div class="premium-card"><h3 style="color:#FFD700;">💰 Rekomendasi Budget Besok</h3>', unsafe_allow_html=True)
    
    if st.session_state.last_s_rate >= 85 and st.session_state.last_roas >= st.session_state.last_roas_bep:
        rekom_budget_bsk = st.session_state.last_budget_set * 1.3
        pesan = f"🚀 Naikkan menjadi {format_rp(rekom_budget_bsk)} karena performa bagus & budget habis"
    elif st.session_state.last_s_rate < 50:
        rekom_budget_bsk = st.session_state.last_budget_set
        pesan = f"🔻 Pertahankan {format_rp(rekom_budget_bsk)}. Turunkan target ROAS dulu agar budget terserap."
    elif st.session_state.last_roas < st.session_state.last_roas_bep:
        rekom_budget_bsk = st.session_state.last_budget_set * 0.7
        pesan = f"🔻 Turunkan menjadi {format_rp(rekom_budget_bsk)} untuk mengurangi kerugian"
    else:
        rekom_budget_bsk = st.session_state.last_budget_set
        pesan = f"✅ Pertahankan {format_rp(rekom_budget_bsk)}. Performa sehat, pantau 3-5 hari."
    
    st.markdown(f"""
    <div style="background:rgba(0,229,160,0.1); border-radius:16px; padding:1.5rem;">
        <p><strong>📌 {pesan}</strong></p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="premium-card"><h3 style="color:#FFD700;">💬 Tanya AI (Konsultasi Iklan)</h3>', unsafe_allow_html=True)
user_question = st.text_input("Pertanyaan kamu:", placeholder="Contoh: ROAS saya turun drastis, harus gimana?", key="chatbot_question")
if st.button("🤖 Tanya AI", use_container_width=True, key="ask_ai"):
    if user_question:
        with st.spinner("AI sedang berpikir..."):
            prompt = f"""Anda adalah pakar iklan TikTok & Shopee. Jawab pertanyaan seller pemula ini dengan singkat (maks 100 kata) dan mudah dipahami.

Pertanyaan: {user_question}

Jawab dengan bahasa Indonesia yang ramah, profesional, dan berikan solusi praktis.
"""
            answer = call_gemini_api(prompt)
            if answer and not answer.startswith("❌"):
                st.info(f"💡 {answer}")
            else:
                st.warning("Maaf, AI sedang sibuk. Coba lagi nanti.")
    else:
        st.warning("Masukkan pertanyaan dulu.")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<h2 class='gold-header'>✨ Elite Copywriter Lab</h2>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["📝 SEO Title", "📄 Deskripsi", "🎬 Hook Video", "#️⃣ Hashtag"])

with tab1:
    st.markdown('<div class="generator-card">', unsafe_allow_html=True)
    p_name = st.text_input("🏷️ Nama Produk", placeholder="Contoh: Kaos Oversize Premium", key="seo_name")
    if st.button("✨ Generate Elite SEO Title", key="gen_seo", use_container_width=True):
        with st.spinner("🧠 AI sedang merancang judul..."):
            if p_name:
                res = call_gemini_api(f"Buat 5 judul untuk '{p_name}' di Shopee. Judul menarik, ada emoji, fokus manfaat. Output per baris.")
                if res and not res.startswith("❌"):
                    st.code(res, language="text")
                else:
                    st.code(f"🔥 {p_name} - Kualitas Premium\n💯 {p_name} BEST SELLER\n✨ WAJIB PUNYA! {p_name}", language="text")
            else:
                st.warning("Masukkan nama produk.")
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="generator-card">', unsafe_allow_html=True)
    p_name_desc = st.text_input("🏷️ Nama Produk", placeholder="Contoh: Kaos Oversize Premium", key="desc_name")
    manfaat = st.text_area("Manfaat (pisahkan koma)", placeholder="Contoh: adem, nyaman, tidak panas", key="manfaat_desc")
    if st.button("✨ Generate Elite Deskripsi", key="gen_desc", use_container_width=True):
        with st.spinner("🧠 AI sedang menulis deskripsi..."):
            if p_name_desc:
                prompt = f"Buat deskripsi untuk '{p_name_desc}' di Shopee. Manfaat: {manfaat}. Gunakan emoji, ajakan beli."
                res = call_gemini_api(prompt)
                if res and not res.startswith("❌"):
                    st.code(res, language="markdown")
                else:
                    st.code(f"✨ {p_name_desc} - Kualitas Premium!\n✅ {manfaat if manfaat else 'Bahan premium'}\n🔥 Promo terbatas!", language="markdown")
            else:
                st.warning("Masukkan nama produk.")
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="generator-card">', unsafe_allow_html=True)
    p_name_hook = st.text_input("🏷️ Nama Produk", placeholder="Contoh: Kaos Oversize Premium", key="hook_name")
    gaya = st.selectbox("Gaya Hook", ["Problem Solver", "Diskon", "Bukti Sosial", "Curiosity", "Emosional"], key="gaya_hook")
    if st.button("✨ Generate Elite Hook", key="gen_hook", use_container_width=True):
        with st.spinner("🧠 AI sedang membuat hook..."):
            if p_name_hook:
                prompt = f"Buat 5 hook untuk '{p_name_hook}' di TikTok. Gaya: {gaya}. Hook 3 detik pertama."
                res = call_gemini_api(prompt)
                if res and not res.startswith("❌"):
                    for line in res.strip().split('\n'):
                        if line.strip():
                            st.markdown(f"- 🎬 {line.strip()}")
                else:
                    st.markdown(f"- 🎬 😫 Capek cari {p_name_hook}? STOP!")
                    st.markdown(f"- 🎬 🔥 DISKON 50% {p_name_hook}!")
                    st.markdown(f"- 🎬 🏆 {p_name_hook} BEST SELLER!")
            else:
                st.warning("Masukkan nama produk.")
    st.markdown('</div>', unsafe_allow_html=True)

with tab4:
    st.markdown('<div class="generator-card">', unsafe_allow_html=True)
    p_name_hash = st.text_input("🏷️ Nama Produk", placeholder="Contoh: Kaos Oversize Premium", key="hash_name")
    niche_hash = st.selectbox("Niche", ["Fashion", "Kosmetik", "Makanan", "Elektronik", "Olahraga"], key="niche_hash")
    if st.button("✨ Generate Hashtag Viral", key="gen_hash", use_container_width=True):
        with st.spinner("🧠 AI sedang membuat hashtag..."):
            if p_name_hash:
                prompt = f"Buat 15 hashtag TikTok untuk '{p_name_hash}', niche {niche_hash}. Format: #fyp #viral #namaproduk"
                res = call_gemini_api(prompt)
                if res and not res.startswith("❌"):
                    st.code(res, language="text")
                else:
                    st.code("#fyp #viral #rekomendasi #shopee #tiktokshop #promo #diskon #murah #berkualitas #premium", language="text")
            else:
                st.warning("Masukkan nama produk.")
    st.markdown('</div>', unsafe_allow_html=True)
