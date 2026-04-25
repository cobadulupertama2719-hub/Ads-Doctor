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
    initial_sidebar_state="collapsed"
)

# 2. CSS
hide_st_style = """
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
.stAppDeployButton {display:none;}
[data-testid="stToolbar"] {display:none;}

/* HILANGKAN SIDEBAR SEPENUHNYA */
[data-testid="stSidebar"] {
    display: none !important;
}

[data-testid="stSidebarContent"] {
    display: none !important;
}

/* MAIN CONTENT MELEBAR FULL */
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 80px;
    max-width: 100%;
}

/* BOTTOM NAVIGATION BAR */
.bottom-nav {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: linear-gradient(180deg, #0f172a 0%, #020617 100%);
    border-top: 1px solid rgba(0, 229, 160, 0.5);
    padding: 8px 0;
    z-index: 99999;
    display: flex;
    justify-content: space-around;
    backdrop-filter: blur(10px);
}

.nav-item {
    text-align: center;
    cursor: pointer;
    padding: 8px 20px;
    border-radius: 30px;
    transition: all 0.3s ease;
    background: transparent;
    border: none;
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
    .nav-item { padding: 5px 10px; }
}

/* Footer styling */
.custom-footer {
    text-align: center;
    padding: 30px 20px 20px 20px;
    margin-top: 40px;
    border-top: 1px solid rgba(255,255,255,0.1);
}

/* Executive dashboard styling */
.executive-card {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 20px;
    padding: 20px;
    margin: 15px 0;
    border-left: 4px solid #FFD700;
}

.executive-stat {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    border-radius: 16px;
    padding: 15px;
    text-align: center;
}

.profit-total {
    font-size: 2rem;
    font-weight: bold;
    color: #00E5A0;
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
        font-size: 1rem !important;
        padding: 10px 20px !important;
        border-radius: 40px !important;
        border: none !important;
        transition: all 0.3s ease !important;
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
        padding: 25px;
        margin: 15px 0;
        transition: all 0.3s ease;
    }
    
    .generator-card:hover {
        border-color: #00E5A0;
        transform: translateY(-2px);
    }
    
    .analytics-wrapper {
        background: rgba(15, 25, 45, 0.6);
        border-radius: 20px;
        padding: 20px;
        margin-top: 20px;
    }

    /* GMV Max styling */
    .gmv-quote {
        font-size: 1.2rem;
        font-style: italic;
        color: #00E5A0;
        text-align: center;
        padding: 20px;
        border-top: 1px solid rgba(255,255,255,0.1);
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Executive dashboard */
    .executive-stat {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        border: 1px solid rgba(255,215,0,0.3);
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
if "executive_results" not in st.session_state:
    st.session_state["executive_results"] = None

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

# ==================== FUNGSI REKOMENDASI (TIDAK DIUBAH) ====================
def generate_rekomendasi(roas_aktual, roas_bep, s_rate, clicks, orders, budget_set, target_roas, budget_spent, ctr):
    rekom_tindakan = ""
    rekom_roas = target_roas
    rekom_budget = budget_set
    prioritas = ""
    warna = "info"
    
    if clicks > 50 and s_rate >= 80 and orders == 0:
        prioritas = "🔴 URGENT STOP IKLAN"
        warna = "danger"
        rekom_budget = 0
        rekom_tindakan = f"HENTIKAN IKLAN! {clicks} klik tapi 0 order. Produk belum layak iklan."
    
    elif s_rate >= 85 and roas_aktual >= roas_bep * 1.2:
        prioritas = "🟢 SIAP SCALE"
        warna = "success"
        rekom_budget = budget_set * 1.3
        rekom_tindakan = f"Scale 30% budget menjadi {format_rp(rekom_budget)}"
    
    elif roas_aktual >= roas_bep and s_rate < 85:
        prioritas = "🟡 OPTIMASI BUDGET"
        warna = "warning"
        rekom_roas = target_roas - 0.5
        rekom_tindakan = f"Turunkan target ROAS 0.5x menjadi {rekom_roas:.1f}x"
    
    elif roas_aktual < roas_bep and roas_aktual > 0:
        prioritas = "🔴 IKLAN RUGI"
        warna = "danger"
        rekom_roas = roas_bep + 0.5
        rekom_budget = budget_set * 0.7
        rekom_tindakan = f"Turunkan budget 30% + naikkan target ROAS ke {rekom_roas:.1f}x"
    
    else:
        prioritas = "🟢 PERFORMA SEHAT"
        rekom_tindakan = "Pertahankan setting, pantau 3-5 hari"
    
    if ctr < 2 and clicks > 0 and "Stop" not in rekom_tindakan:
        rekom_tindakan += " | CTR rendah (<2%), ganti visual iklan"
    
    return rekom_tindakan, rekom_budget, rekom_roas, prioritas, warna

# ==================== FUNGSI ANALISIS BATCH UNTUK EXECUTIVE ====================
def calculate_roas_bep(harga_jual, modal, admin_persen, target_profit=0):
    laba_kotor = harga_jual - modal - (harga_jual * admin_persen / 100)
    laba_setelah = laba_kotor - target_profit
    return harga_jual / laba_setelah if laba_setelah > 0 else 999

def analyze_batch_product(row):
    """Analisis satu produk untuk executive dashboard"""
    try:
        nama = row.get('nama_produk', row.get('Nama Produk', row.get('product', 'Unknown')))
        impressions = float(row.get('impressions', row.get('Impressions', 0)))
        clicks = float(row.get('clicks', row.get('Clicks', 0)))
        budget_spent = float(row.get('budget_spent', row.get('Spent', row.get('Budget Spent', 0))))
        sales = float(row.get('sales', row.get('Revenue', row.get('Sales', 0))))
        orders = float(row.get('orders', row.get('Orders', 0)))
        budget_set = float(row.get('budget_set', row.get('Budget Setting', row.get('Budget Set', 0))))
        target_roas = float(row.get('target_roas', row.get('Target ROAS', 6.0)))
        
        # Parameter untuk ROAS BEP (default jika tidak ada)
        harga_jual = float(row.get('harga_jual', row.get('Harga Jual', 150000)))
        modal = float(row.get('modal', row.get('Modal', 75000)))
        admin_persen = float(row.get('admin_persen', row.get('Admin %', 20)))
        
        # Hitung metrik
        ctr = (clicks / impressions * 100) if impressions > 0 else 0
        roas_aktual = (sales / budget_spent) if budget_spent > 0 else 0
        s_rate = (budget_spent / budget_set * 100) if budget_set > 0 else 0
        roas_bep = calculate_roas_bep(harga_jual, modal, admin_persen)
        profit = (harga_jual - modal - (harga_jual * admin_persen / 100)) * orders - budget_spent if orders > 0 else -budget_spent
        
        # Dapatkan rekomendasi
        rekom, rekom_budget, rekom_roas, prioritas, warna = generate_rekomendasi(
            roas_aktual, roas_bep, s_rate, clicks, orders, budget_set, target_roas, budget_spent, ctr
        )
        
        return {
            'nama_produk': nama,
            'impressions': impressions,
            'clicks': clicks,
            'ctr': ctr,
            'budget_spent': budget_spent,
            'sales': sales,
            'roas_aktual': roas_aktual,
            'roas_bep': roas_bep,
            's_rate': s_rate,
            'orders': orders,
            'profit': profit,
            'target_roas': target_roas,
            'rekomendasi': rekom,
            'prioritas': prioritas,
            'warna': warna,
            'rekom_budget': rekom_budget,
            'rekom_roas': rekom_roas
        }
    except Exception as e:
        return None

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

# ==================== BOTTOM NAVIGATION (5 MENU) ====================
nav_cols = st.columns(5)
nav_items = [
    {"page": "dashboard", "icon": "🏠", "label": "Dashboard"},
    {"page": "gmvmax", "icon": "🚀", "label": "GMV Max"},
    {"page": "generator", "icon": "✨", "label": "Generator"},
    {"page": "database", "icon": "📦", "label": "Database"},
    {"page": "executive", "icon": "👑", "label": "Executive"}
]

for idx, nav in enumerate(nav_items):
    with nav_cols[idx]:
        is_active = st.session_state.current_page == nav["page"]
        if st.button(f"{nav['icon']} {nav['label']}", key=f"nav_{nav['page']}", use_container_width=True):
            st.session_state.current_page = nav["page"]
            st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# ==================== HALAMAN DASHBOARD (TIDAK DIUBAH) ====================
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
            elif laba_kotor_p < 50
