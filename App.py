import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import hashlib
import requests
import json
import io
import time

# 1. SET PAGE CONFIG
st.set_page_config(
    page_title="Advertising Command Center",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. CSS
hide_st_style = """
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
.stAppDeployButton {display:none;}
[data-testid="stToolbar"] {display:none;}

/* TAMPILKAN TOMBOL SIDEBAR */
button[kind="header"] {
    visibility: visible !important;
    display: flex !important;
    position: fixed !important;
    top: 10px !important;
    left: 10px !important;
    z-index: 999999 !important;
    background: linear-gradient(135deg, #00E5A0 0%, #00a878 100%) !important;
    border-radius: 50% !important;
    width: 48px !important;
    height: 48px !important;
    box-shadow: 0 4px 15px rgba(0, 229, 160, 0.5) !important;
    border: 2px solid rgba(255, 255, 255, 0.3) !important;
    cursor: pointer !important;
}

button[kind="header"]:hover {
    transform: scale(1.05) !important;
    background: linear-gradient(135deg, #00FFB0 0%, #00c890 100%) !important;
}

button[kind="header"] svg {
    fill: #020617 !important;
    stroke: #020617 !important;
    width: 24px !important;
    height: 24px !important;
}

/* SIDEBAR FULL HEIGHT */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #020617 100%) !important;
    border-right: 2px solid rgba(0, 229, 160, 0.3) !important;
    padding-top: 0 !important;
    margin-top: 0 !important;
    top: 0 !important;
    height: 100vh !important;
}

/* BOTTOM NAVIGATION BAR */
.bottom-nav {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: linear-gradient(180deg, #0f172a 0%, #020617 100%);
    border-top: 1px solid rgba(0, 229, 160, 0.3);
    padding: 10px 0;
    z-index: 99999;
    display: flex;
    justify-content: space-around;
    backdrop-filter: blur(10px);
}

.nav-item {
    text-align: center;
    cursor: pointer;
    padding: 5px 15px;
    border-radius: 30px;
    transition: all 0.3s ease;
}

.nav-item:hover {
    background: rgba(0, 229, 160, 0.2);
}

.nav-item.active {
    background: linear-gradient(135deg, #00E5A0 0%, #00a878 100%);
}

.nav-item.active .nav-label {
    color: #020617 !important;
    font-weight: bold;
}

.nav-icon {
    font-size: 1.5rem;
}

.nav-label {
    font-size: 0.7rem;
    color: #94A3B8;
    margin-top: 2px;
}

/* Mobile responsive */
@media (max-width: 768px) {
    .premium-card { padding: 15px !important; }
    .gold-header { font-size: 1.5rem !important; }
    .stButton button { font-size: 0.9rem !important; }
    .nav-label { font-size: 0.6rem; }
    .nav-icon { font-size: 1.2rem; }
}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# ==================== UI STYLE ====================
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
    
    .stApp { 
        background: radial-gradient(circle at 2% 2%, #1e1b4b 0%, #020617 100%); 
        padding-bottom: 80px !important;
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

    .stNumberInput input, .stTextInput input, .stSelectbox div, .stTextArea textarea {
        background: rgba(15, 25, 45, 0.9) !important; 
        border: 1px solid rgba(255, 255, 255, 0.2) !important; 
        border-radius: 12px !important; 
        color: #FFFFFF !important;
        font-size: 1rem !important;
        padding: 10px !important;
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
    
    .rekom-warning {
        background: linear-gradient(135deg, #451a03 0%, #78350f 100%);
        border-left: 5px solid #f59e0b;
        border-radius: 16px;
        padding: 20px;
        margin: 15px 0;
    }
    
    .rekom-success {
        background: linear-gradient(135deg, #064e3b 0%, #0d9488 100%);
        border-left: 5px solid #10b981;
        border-radius: 16px;
        padding: 20px;
        margin: 15px 0;
    }
    
    .rekom-info {
        background: linear-gradient(135deg, #0c4a6e 0%, #0284c7 100%);
        border-left: 5px solid #3b82f6;
        border-radius: 16px;
        padding: 20px;
        margin: 15px 0;
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
    
    .analytics-wrapper {
        background: rgba(15, 25, 45, 0.6);
        border-radius: 20px;
        padding: 20px;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

apply_premium_style()

# ==================== SESSION STATE ====================
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
if "api_error" not in st.session_state:
    st.session_state["api_error"] = None
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "dashboard"

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
    if not GEMINI_API_KEY:
        st.session_state.api_error = "❌ API Key tidak ditemukan!"
        return None
    
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            text = result["candidates"][0]["content"]["parts"][0]["text"]
            st.session_state.api_error = None
            return text
        else:
            error_msg = f"⚠️ API Error {response.status_code}"
            if response.status_code == 503:
                error_msg = "⚠️ Server sibuk, coba lagi nanti."
            st.session_state.api_error = error_msg
            return None
    except Exception as e:
        st.session_state.api_error = f"⚠️ Error: {str(e)[:100]}"
        return None

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
    st.session_state.products = [p for p in st.session_state.products if p["nama"] != nama]

def export_products():
    if st.session_state.products:
        df = pd.DataFrame(st.session_state.products)
        return df.to_csv(index=False).encode('utf-8')
    return None

def import_products(file):
    try:
        df = pd.read_csv(file)
        for _, row in df.iterrows():
            save_product(row.to_dict())
        return True
    except Exception as e:
        st.error(f"Gagal import: {e}")
        return False

# ==================== FUNGSI REKOMENDASI ====================
def generate_rekomendasi(roas_aktual, roas_bep, s_rate, clicks, orders, budget_set, target_roas, budget_spent, ctr):
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

**Yang harus dilakukan:**
1. Cek harga produk dengan kompetitor
2. Tambah review & rating (target 10-20 review positif)
3. Perbaiki deskripsi — fokus ke MANFAAT"""
    
    elif s_rate >= 85 and roas_aktual >= roas_bep * 1.2:
        prioritas = "🟢 PRIORITAS 4 - SIAP SCALE"
        warna = "success"
        rekom_budget = budget_set * 1.3
        rekom_tindakan = f"""🚀 **SIAP SCALE!**

📈 ROAS {roas_aktual:.1f}x > BEP {roas_bep:.1f}x (untung)
💰 Budget terserap {s_rate:.0f}% (hampir habis)

✅ Naikkan **BUDGET 30%** menjadi {format_rp(rekom_budget)}"""
    
    elif roas_aktual >= roas_bep and s_rate < 85:
        prioritas = "🟡 PRIORITAS 2 - OPTIMASI"
        warna = "warning"
        rekom_roas = target_roas - 0.5
        rekom_tindakan = f"""⚡ **OPTIMASI BUDGET**

✅ ROAS {roas_aktual:.1f}x ≥ BEP {roas_bep:.1f}x (untung)
📊 Budget terserap {s_rate:.0f}%

✅ Turunkan target ROAS **0.5 poin** menjadi **{rekom_roas:.1f}x**"""
    
    elif roas_aktual < roas_bep and roas_aktual > 0:
        prioritas = "🔴 PRIORITAS 3 - IKLAN RUGI"
        warna = "danger"
        rekom_roas = roas_bep + 0.5
        rekom_budget = budget_set * 0.7
        rekom_tindakan = f"""💸 **IKLAN RUGI!**

📉 ROAS {roas_aktual:.1f}x < BEP {roas_bep:.1f}x

✅ Naikkan target ROAS **0.5 poin** menjadi **{rekom_roas:.1f}x**
🔻 Turunkan budget **30%** menjadi {format_rp(rekom_budget)}"""
    
    else:
        prioritas = "🟢 PRIORITAS 5 - PANTAU"
        rekom_tindakan = f"""✅ **PERFORMA SEHAT**

📈 ROAS {roas_aktual:.1f}x ≥ BEP {roas_bep:.1f}x
💰 Budget terserap {s_rate:.0f}%

⏰ Pantau selama **3-5 hari** tanpa perubahan"""
    
    if ctr < 2 and clicks > 0 and "Stop Iklan" not in rekom_tindakan:
        rekom_tindakan += f"\n\n📸 CTR {ctr:.1f}% < 2% → Ganti visual iklan."
    
    return rekom_tindakan, rekom_budget, rekom_roas, prioritas, warna

# ==================== LOGIN ====================
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
            submitted = st.form_submit_button("MASUK", use_container_width=True)
            
            if submitted:
                if u == ADMIN_USERNAME and p == ADMIN_PASSWORD:
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("❌ Username atau Password salah!")
    st.stop()

# ==================== HEADER ====================
if st.session_state.api_error:
    st.error(f"{st.session_state.api_error}")

st.markdown("""
<div style="text-align: center; margin-bottom: 20px;">
    <h1 class="gold-header" style="font-size: 2.5rem; margin-bottom: 0;">🩺 ADVERTISING COMMAND CENTER</h1>
    <p style="color: #00E5A0; font-size: 0.9rem; letter-spacing: 2px; margin-top: 5px;">Powered by Arkidigital</p>
</div>
""", unsafe_allow_html=True)

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown('<div style="text-align:center; background:rgba(0,229,160,0.2); padding:15px; border-radius:40px; margin-bottom:20px;"><span style="color:#00E5A0; font-weight:bold;">⭐ PREMIUM MEMBER ⭐</span></div>', unsafe_allow_html=True)
    
    if st.button("🚪 LOGOUT", use_container_width=True):
        st.session_state.clear()
        st.rerun()
    
    with st.expander("ℹ️ Panduan Cepat", expanded=False):
        st.markdown("""
        **📌 Langkah Penggunaan:**
        1. Masukkan data produk di **ROAS BEP Calculator**
        2. Input performa iklan di **Ad Performance Matrix**
        3. Klik **RUN DEEP ANALYTICS**
        """)

# ==================== BOTTOM NAVIGATION ====================
def render_bottom_nav():
    pages = {
        "dashboard": {"icon": "🏠", "label": "Dashboard"},
        "gmvmax": {"icon": "🚀", "label": "GMV Max"},
        "generator": {"icon": "✨", "label": "Generator"},
        "database": {"icon": "📦", "label": "Database"}
    }
    
    nav_html = '<div class="bottom-nav">'
    for page_id, page_info in pages.items():
        active_class = 'active' if st.session_state.current_page == page_id else ''
        nav_html += f"""
        <div class="nav-item {active_class}" onclick="parent.postMessage({{type: 'streamlit:setComponentValue', value: '{page_id}'}}, '*')">
            <div class="nav-icon">{page_info['icon']}</div>
            <div class="nav-label">{page_info['label']}</div>
        </div>
        """
    nav_html += '</div>'
    
    st.markdown(nav_html, unsafe_allow_html=True)
    
    # JavaScript untuk handle klik
    st.markdown("""
    <script>
    window.addEventListener('message', function(e) {
        if (e.data.type === 'streamlit:setComponentValue') {
            // Ini akan trigger rerun di Streamlit
            console.log('Navigasi ke:', e.data.value);
        }
    });
    </script>
    """, unsafe_allow_html=True)

# ==================== HALAMAN DASHBOARD ====================
def render_dashboard():
    # ROAS BEP Calculator
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
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_audit:
        st.markdown('<div class="premium-card" style="height:100%;"><h3>📋 Kelayakan Iklan</h3>', unsafe_allow_html=True)
        pernah = st.radio("Produk Pernah Laku?", ["Ya", "Tidak"], horizontal=True, key="pernah_laku_main")
        if pernah == "Tidak": 
            st.error("❌ Belum layak iklan! Kumpulkan minimal 10 review positif terlebih dahulu.")
        else:
            h_komp = st.number_input("Harga Kompetitor", min_value=1000, value=140000, key="harga_komp_main")
            if hj > h_komp * 1.2: 
                st.warning("⚠️ Harga terlalu mahal.")
            elif laba_kotor_p < 5000: 
                st.error("❌ Margin terlalu tipis.")
            else:
                st.success("✅ Produk layak beriklan!")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Ad Performance Matrix
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
        
        if profit_est_p > 0 and roas_akt_p >= roas_bep_p:
            st.balloons()
        
        st.markdown('<div class="analytics-wrapper">', unsafe_allow_html=True)
        
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(f'<div class="premium-card"><p style="color:#94A3B8; margin:0;">📈 CTR</p><h2 style="color:#FFFFFF; margin:0;">{ctr_p:.2f}%</h2></div>', unsafe_allow_html=True)
        with m2:
            st.markdown(f'<div class="premium-card"><p style="color:#94A3B8; margin:0;">💰 ROAS</p><h2 style="color:#00E5A0; margin:0;">{roas_akt_p:.2f}x</h2></div>', unsafe_allow_html=True)
        with m3:
            profit_color = "#00E5A0" if profit_est_p > 0 else "#FF6B6B"
            st.markdown(f'<div class="premium-card"><p style="color:#94A3B8; margin:0;">💎 PROFIT</p><h2 style="color:{profit_color}; margin:0;">{format_rp(profit_est_p)}</h2></div>', unsafe_allow_html=True)
        with m4:
            st.markdown(f'<div class="premium-card"><p style="color:#94A3B8; margin:0;">🎯 BEP</p><h2 style="color:#FFFFFF; margin:0;">{roas_bep_p:.2f}x</h2></div>', unsafe_allow_html=True)
        
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
            <hr style="margin:15px 0;">
            <p><strong>💰 Budget Rekomendasi:</strong> {format_rp(rekom_budget)} | <strong>🎯 Target ROAS:</strong> {rekom_roas:.1f}x</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Prediksi
    if st.session_state.analysis_done and st.session_state.last_roas >= st.session_state.last_roas_bep * 1.2:
        st.markdown('<div class="premium-card"><h3 style="color:#FFD700;">📈 Prediksi Scale</h3>', unsafe_allow_html=True)
        new_budget_pred = st.session_state.last_budget_set * 1.3
        prediksi_profit = st.session_state.last_profit * 1.25
        st.markdown(f"""
        <div style="background:rgba(0,229,160,0.1); border-radius:16px; padding:1.5rem;">
            <p><strong>💰 Budget 30%:</strong> {format_rp(new_budget_pred)}/hari</p>
            <p><strong>💎 Estimasi Profit:</strong> {format_rp(prediksi_profit)}/hari</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ==================== HALAMAN GMV MAX ====================
def render_gmvmax():
    st.markdown('<div class="premium-card"><h3 style="color:#FFD700;">🚀 GMV MAX - Panduan Strategi Iklan untuk Pemula</h3>', unsafe_allow_html=True)
    
    st.markdown("""
    ### 📌 Apa itu GMV Max?
    **GMV Max** adalah strategi iklan untuk memaksimalkan **Gross Merchandise Value** (total penjualan kotor) melalui platform TikTok Shop dan Shopee.
    
    ---
    
    ### 🎯 Strategi Beriklan TikTok Shop untuk Pemula
    
    #### 1. Budget Harian Ideal
    | Level | Budget Harian | Target ROAS |
    |-------|---------------|-------------|
    | Pemula | Rp50.000 - Rp100.000 | 3x - 4x |
    | Menengah | Rp150.000 - Rp300.000 | 4x - 5x |
    | Lanjutan | Rp500.000+ | 5x - 7x |
    
    #### 2. Waktu Terbaik Pasang Iklan
    - ⏰ **Pagi:** 07.00 - 09.00 (orang bersiap kerja/sekolah)
    - 🍽️ **Siang:** 12.00 - 13.00 (jam istirahat)
    - 🌙 **Malam:** 19.00 - 22.00 (waktu santai, intensitas tinggi)
    
    #### 3. Tips Memilih Produk untuk GMV Max
    - ✅ Harga jual Rp50.000 - Rp200.000 (mudah konversi)
    - ✅ Margin minimal 40%
    - ✅ Stok mencukupi (minimal 100 pcs)
    - ✅ Punya review minimal 10 bintang 4-5
    
    ---
    
    ### 🎯 Strategi Beriklan Shopee untuk Pemula
    
    #### 1. Setting Iklan Produk
    - **Kata Kunci:** Gunakan 10-15 keyword relevan
    - **Target Audiens:** Sesuaikan dengan usia & gender pembeli
    - **Budget Harian:** Mulai dari Rp50.000
    
    #### 2. Optimasi Konversi
    - 📸 Foto produk: 5-10 foto dari berbagai sudut
    - 📝 Deskripsi: Sertakan manfaat, spesifikasi, size chart
    - ⭐ Rating: Minimal 4.5 bintang
    - 💬 Respon chat: Dalam 1 jam
    
    ---
    
    ### 💡 Tips & Trik GMV Max
    
    | Tips | Penjelasan |
    |------|------------|
    | **Hook 3 Detik** | 3 detik pertama video harus BIKIN PENASARAN |
    | **CTA Kuat** | "Klik link di bio!", "Buruan stok terbatas!" |
    | **Testimoni** | Tampilkan video unboxing dari pembeli |
    | **Follow Up** | Chat buyer tanya kepuasan, minta rating |
    | **Retargeting** | Pasang iklan ulang untuk yang sudah klik tapi belum beli |
    
    ---
    
    ### 📈 Target ROAS Ideal Berdasarkan Margin
    
    | Margin Produk | Target ROAS Minimal | Target ROAS Ideal |
    |---------------|---------------------|-------------------|
    | 30% - 40% | 3.0x | 4.0x |
    | 40% - 50% | 2.5x | 3.5x |
    | 50% - 60% | 2.0x | 3.0x |
    | 60%+ | 1.8x | 2.5x |
    
    ---
    
    ### ⚠️ Kesalahan Umum Pemula
    
    1. ❌ Budget terlalu kecil (<Rp30.000/hari) → data tidak cukup
    2. ❌ Target ROAS terlalu tinggi (>7x) → iklan tidak akan jalan
    3. ❌ Video tanpa hook → viewer scroll dalam 1 detik
    4. ❌ Tidak follow up chat buyer → peluang repeat order hilang
    
    ---
    
    ### 🚀 Next Step Setelah GMV Max Berhasil
    
    1. ✅ Naikkan budget 20-30% setiap 3 hari
    2. ✅ Buat 3-5 variasi kreatif iklan baru
    3. ✅ Ekspansi ke produk lain dalam niche yang sama
    4. ✅ Bangun komunitas (Group Telegram/WhatsApp)
    """)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== HALAMAN GENERATOR ====================
def render_generator():
    st.markdown("<h2 class='gold-header'>✨ Elite Copywriter Lab</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#94A3B8; margin-bottom:20px;'>Copywriting profesional ala ahli advertising 10 tahun</p>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📝 SEO Title", "📄 Deskripsi", "🎬 Hook Video", "#️⃣ Hashtag"])
    
    with tab1:
        with st.container():
            p_name = st.text_input("🏷️ Nama Produk", placeholder="Contoh: Kaos Oversize Premium", key="seo_name")
            if st.button("✨ Generate SEO Title", key="gen_seo", use_container_width=True):
                with st.spinner("🧠 AI copywriter sedang merancang judul..."):
                    if p_name:
                        prompt = f"""[System: Premium E-commerce SEO Specialist]
Role: Senior Copywriter untuk TikTok Shop & Shopee.
Task: Buat 5 judul produk dengan FORMULA WAJIB:

FORMULA: [Nama Produk] + [Kategori] + [Atribut/Bahan] + [Manfaat]

Produk: '{p_name}'

Aturan:
1. Setiap judul HARUS mengikuti formula di atas (4 elemen wajib ada)
2. Tambahkan 1 emoji di awal judul
3. Maksimal 70 karakter
4. Manfaat: fokus ke solusi masalah atau keunggulan produk
5. Output langsung 5 judul, satu per baris, tanpa penjelasan

Contoh format:
🔥 Kaos Oversize Premium | Atasan Wanita | Katun Combed 30s | Adem Tidak Panas
✨ Jaket Parka Pria | Outer Musim Hujan | Waterproof | Anti Angin Dingin

Output:"""
                        res = call_gemini_api(prompt)
                        if res:
                            st.code(res, language="text")
                        else:
                            st.code(f"🔥 {p_name} | Fashion | Premium Quality | Best Seller\n✨ {p_name} | Atasan | Bahan Adem | Nyaman Dipakai", language="text")
                    else:
                        st.warning("Masukkan nama produk.")
    
    with tab2:
        with st.container():
            p_name_desc = st.text_input("🏷️ Nama Produk", placeholder="Contoh: Kaos Oversize Premium", key="desc_name")
            manfaat = st.text_area("Manfaat (pisahkan koma)", placeholder="Contoh: adem, nyaman, tidak panas, anti kusut", key="manfaat_desc")
            if st.button("✨ Generate Deskripsi", key="gen_desc", use_container_width=True):
                with st.spinner("🧠 AI copywriter sedang menulis deskripsi..."):
                    if p_name_desc:
                        prompt = f"""[System: Premium E-commerce Copywriter]
Role: Senior Brand Manager for Fashion & Lifestyle.
Task: Write a high-conversion product description for '{p_name_desc}'.

Product Specs: {manfaat if manfaat else 'Premium Quality, Modern Design'}.

Structure Guidelines:
1. Headline: [Brand Name] + [Main Category] + [Key Features].
2. Hook: 1-2 sentences about the 'Siluet' or 'Feeling' when wearing it.
3. Value Proposition: Highlight the fabric and versatility.
4. Product Details: Use ✦ SPESIFIKASI PRODUK ✦ with bullet points.
5. Colors & Size: ✦ PILIHAN WARNA ✦ & ✦ SIZE GUIDE ✦
6. Trust Signals: ✦ BRAND STANDARDS ✦
7. Logistics & CTA: Shipping info and Unboxing requirement.

Style: Clean, professional, minimalis, focus on 'Modern Women' aesthetic.
Constraint: Use clear separators (✦), professional emojis, and Indonesian language.
Output: Direct full description only."""
                        res = call_gemini_api(prompt)
                        if res:
                            st.code(res, language="markdown")
                        else:
                            st.code(f"✨ {p_name_desc} - Kualitas Premium!\n✅ {manfaat if manfaat else 'Bahan premium, nyaman dipakai'}\n🔥 Promo terbatas! KLIK SEKARANG!", language="markdown")
                    else:
                        st.warning("Masukkan nama produk.")
    
    with tab3:
        with st.container():
            p_name_hook = st.text_input("🏷️ Nama Produk", placeholder="Contoh: Kaos Oversize Premium", key="hook_name")
            gaya = st.selectbox("Gaya Hook", ["Problem Solver", "Diskon", "Bukti Sosial", "Curiosity", "Emosional"], key="gaya_hook")
            if st.button("✨ Generate Hook Video", key="gen_hook", use_container_width=True):
                with st.spinner("🧠 AI creative director sedang membuat hook..."):
                    if p_name_hook:
                        prompt = f"""[System: Creative Director TikTok]
Role: Expert in viral hooks for TikTok Shop.
Task: Buat 5 hook 3 detik pertama untuk produk '{p_name_hook}' dengan gaya {gaya}.

Aturan:
- Hook harus bikin orang BERHENTI SCROLL
- Maksimal 10 kata per hook
- Format: [Masalah] + [Solusi] + [Urgency]
- Target: retention rate tinggi

Contoh:
- "Capek cari kaos adem? STOP! Ini solusinya!"
- "DISKON 50% HARI INI! Buruan!"

Output: Langsung 5 hook, satu per baris, tanpa penjelasan."""
                        res = call_gemini_api(prompt)
                        if res:
                            for line in res.strip().split('\n'):
                                if line.strip():
                                    st.markdown(f"- 🎬 {line.strip()}")
                        else:
                            st.markdown(f"- 🎬 😫 Capek cari {p_name_hook}? STOP!")
                            st.markdown(f"- 🎬 🔥 DISKON 50% {p_name_hook}!")
                            st.markdown(f"- 🎬 🏆 {p_name_hook} BEST SELLER!")
                    else:
                        st.warning("Masukkan nama produk.")
    
    with tab4:
        with st.container():
            p_name_hash = st.text_input("🏷️ Nama Produk", placeholder="Contoh: Kaos Oversize Premium", key="hash_name")
            niche_hash = st.selectbox("Niche", ["Fashion", "Kosmetik", "Makanan", "Elektronik", "Olahraga"], key="niche_hash")
            if st.button("✨ Generate Hashtag Viral", key="gen_hash", use_container_width=True):
                with st.spinner("🧠 AI trend analyst sedang meracik hashtag..."):
                    if p_name_hash:
                        prompt = f"""[System: Trend Analyst TikTok]
Role: Hashtag Specialist for TikTok Shop.
Task: Buat 20 hashtag untuk produk '{p_name_hash}', niche {niche_hash}.

Kombinasi:
- 5 trending hashtag (hari ini)
- 5 niche hashtag (spesifik produk)
- 5 broad hashtag (#viral #fyp #fypシ)
- 5 lokasi/event hashtag (#promo #diskon #gratisongkir)

Output: Langsung 20 hashtag dalam satu baris, dipisah spasi."""
                        res = call_gemini_api(prompt)
                        if res:
                            st.code(res, language="text")
                        else:
                            st.code("#fyp #viral #rekomendasi #shopee #tiktokshop #promo #diskon #murah #berkualitas #premium", language="text")
                    else:
                        st.warning("Masukkan nama produk.")

# ==================== HALAMAN DATABASE ====================
def render_database():
    with st.expander("📦 **Database Produk**", expanded=True):
        col_prod1, col_prod2 = st.columns([1, 1])
        
        with col_prod1:
            st.markdown("### ➕ Simpan Produk Baru")
            nama_produk_db = st.text_input("Nama Produk", placeholder="Contoh: Kaos Premium", key="nama_produk_dash")
            hj_db = st.number_input("Harga Jual (Rp)", min_value=1000, value=100000, key="hj_dash")
            modal_db = st.number_input("Modal (Rp)", min_value=500, value=60000, key="modal_dash")
            admin_db = st.slider("Admin Platform %", 5, 30, 20, key="admin_dash")
            
            if st.button("💾 Simpan ke Database", key="simpan_dash") and nama_produk_db:
                admin_nom = hj_db * admin_db / 100
                laba_db = hj_db - modal_db - admin_nom
                roas_db = hj_db / laba_db if laba_db > 0 else 999
                save_product({
                    "nama": nama_produk_db, 
                    "harga_jual": hj_db, 
                    "modal": modal_db, 
                    "admin_persen": admin_db, 
                    "laba_kotor": laba_db, 
                    "roas_bep": roas_db
                })
                st.success(f"✅ {nama_produk_db} tersimpan!")
                st.rerun()
        
        with col_prod2:
            st.markdown("### 📋 Produk Tersimpan")
            
            search_term = st.text_input("🔍 Cari produk", placeholder="Ketik nama produk...")
            
            col_exp, col_imp = st.columns(2)
            with col_exp:
                csv_data = export_products()
                if csv_data:
                    st.download_button(
                        label="📥 Export CSV",
                        data=csv_data,
                        file_name="produk_database.csv",
                        mime="text/csv"
                    )
            with col_imp:
                uploaded_file = st.file_uploader("📤 Import CSV", type="csv")
                if uploaded_file:
                    if import_products(uploaded_file):
                        st.success("Import berhasil!")
                        st.rerun()
            
            filtered_products = st.session_state.products
            if search_term:
                filtered_products = [p for p in st.session_state.products if search_term.lower() in p["nama"].lower()]
            
            if filtered_products:
                for idx, prod in enumerate(filtered_products):
                    col_a, col_b = st.columns([3, 1])
                    with col_a:
                        st.markdown(f"**{prod['nama']}**  \nBEP: {prod['roas_bep']:.1f}x | Profit: Rp{prod['laba_kotor']:,.0f}")
                    with col_b:
                        if st.button("🗑️", key=f"hapus_{idx}"):
                            delete_product(prod['nama'])
                            st.rerun()
                    st.markdown("---")
            else:
                if search_term:
                    st.info(f"Tidak ada produk dengan nama '{search_term}'")
                else:
                    st.info("Belum ada produk tersimpan.")

# ==================== RENDER PAGE ====================
# Bottom navigation (menggunakan radio untuk menghindari JS)
nav_cols = st.columns(4)
nav_items = [
    {"page": "dashboard", "icon": "🏠", "label": "Dashboard"},
    {"page": "gmvmax", "icon": "🚀", "label": "GMV Max"},
    {"page": "generator", "icon": "✨", "label": "Generator"},
    {"page": "database", "icon": "📦", "label": "Database"}
]

for idx, nav in enumerate(nav_items):
    with nav_cols[idx]:
        is_active = st.session_state.current_page == nav["page"]
        button_style = "primary" if is_active else "secondary"
        if st.button(f"{nav['icon']} {nav['label']}", key=f"nav_{nav['page']}", use_container_width=True):
            st.session_state.current_page = nav["page"]
            st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# Tampilkan halaman sesuai pilihan
if st.session_state.current_page == "dashboard":
    render_dashboard()
elif st.session_state.current_page == "gmvmax":
    render_gmvmax()
elif st.session_state.current_page == "generator":
    render_generator()
elif st.session_state.current_page == "database":
    render_database()

# ==================== FOOTER ====================
st.markdown("""
<div style="text-align: center; padding: 40px 20px 20px 20px; margin-top: 40px; border-top: 1px solid rgba(255,255,255,0.1);">
    <p style="color: #94A3B8; font-size: 0.8rem;">
        Powered by <span style="color: #00E5A0; font-weight: bold;">Arkidigital</span> © 2025
    </p>
</div>
""", unsafe_allow_html=True)