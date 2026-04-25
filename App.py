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

.logout-btn {
    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
    color: white;
    border: none;
    border-radius: 30px;
    padding: 8px 20px;
    font-size: 0.8rem;
    cursor: pointer;
    margin-top: 10px;
    transition: all 0.3s ease;
}

.logout-btn:hover {
    transform: scale(1.02);
    opacity: 0.9;
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
    .gmv-card {
        background: rgba(0, 229, 160, 0.05);
        border-left: 3px solid #00E5A0;
        border-radius: 12px;
        padding: 15px;
        margin: 10px 0;
    }
    
    .gmv-highlight {
        background: rgba(0, 229, 160, 0.15);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin: 20px 0;
    }
    
    .gmv-quote {
        font-size: 1.2rem;
        font-style: italic;
        color: #00E5A0;
        text-align: center;
        padding: 20px;
        border-top: 1px solid rgba(255,255,255,0.1);
        border-bottom: 1px solid rgba(255,255,255,0.1);
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

📈 ROAS {roas_aktual:.1f}x > BEP {roas_bep:.1f}x (UNTUNG)
💰 Budget terserap {s_rate:.0f}% (HAMPIR HABIS)

**ATURAN SCALE:**
✅ Naikkan **BUDGET 30%** dari {format_rp(budget_set)} menjadi {format_rp(rekom_budget)}
✅ **PERTAHANKAN** target ROAS di {target_roas:.1f}x

⏰ **Tunggu 3 hari** tanpa perubahan apapun."""
    
    elif roas_aktual >= roas_bep and s_rate < 85:
        prioritas = "🟡 PRIORITAS 2 - OPTIMASI BUDGET"
        warna = "warning"
        rekom_roas = target_roas - 0.5
        rekom_tindakan = f"""⚡ **OPTIMASI BUDGET AGAR HABIS & ORDER MAKSIMAL!**

✅ ROAS {roas_aktual:.1f}x ≥ BEP {roas_bep:.1f}x (PROFIT)
📊 Budget terserap HANYA {s_rate:.0f}% = masih sisa Rp{budget_set - budget_spent:,.0f}

**SOLUSI:**
✅ Turunkan target ROAS **0.5 poin** menjadi **{rekom_roas:.1f}x**
✅ **PERTAHANKAN** budget tetap {format_rp(budget_set)}

⏰ **Tunggu 3 hari** dengan setting baru ini."""
    
    elif roas_aktual < roas_bep and roas_aktual > 0:
        prioritas = "🔴 PRIORITAS 3 - IKLAN RUGI (ROAS < BEP)"
        warna = "danger"
        rekom_roas = roas_bep + 0.5
        rekom_budget = budget_set * 0.7
        rekom_tindakan = f"""💸 **IKLAN SEDANG RUGI!**

📉 ROAS {roas_aktual:.1f}x < BEP {roas_bep:.1f}x

**SOLUSI:**
✅ Naikkan target ROAS **0.5 poin** menjadi **{rekom_roas:.1f}x**
🔻 Turunkan budget **30%** dari {format_rp(budget_set)} menjadi {format_rp(rekom_budget)}"""
    
    else:
        prioritas = "🟢 PRIORITAS 5 - PERFORMA SEHAT"
        rekom_tindakan = f"""✅ **PERFORMA IKLAN SEHAT**

📈 ROAS {roas_aktual:.1f}x ≥ BEP {roas_bep:.1f}x (PROFIT)
💰 Budget terserap {s_rate:.0f}%

**REKOMENDASI:**
✅ Pertahankan setting saat ini
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

# ==================== BOTTOM NAVIGATION ====================
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
        if st.button(f"{nav['icon']} {nav['label']}", key=f"nav_{nav['page']}", use_container_width=True):
            st.session_state.current_page = nav["page"]
            st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

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
    st.markdown('<p style="color:#94A3B8;">Panduan lengkap memahami algoritma GMV Max TikTok & Shopee</p>', unsafe_allow_html=True)
    
    # Poin 1
    with st.expander("⚙️ 1. STRUKTUR DASAR ALGORITMA (INPUT-PROCESS-OUTPUT)", expanded=False):
        st.markdown("""
        **GMV Max bekerja pakai 3 layer utama:**
        
        **📥 INPUT** (yang kamu kasih ke sistem)
        - Budget
        - Target ROAS / ROI
        - Produk (harga, margin)
        - Konten / listing (CTR & CVR)
        - Data pixel (event pembelian)
        
        **⚙️ PROCESS** (yang sistem lakukan)
        - Distribusi iklan ke banyak audience
        - Mengukur respon: CTR (klik), CVR (beli), CPA (biaya per order)
        - Membandingkan dengan target ROAS
        
        **📤 OUTPUT** (hasil akhir)
        - Spend terserap / tidak
        - Order masuk / tidak
        - ROAS naik / turun
        
        > 🔥 **Intinya:** GMV Max = sistem probabilitas pembeli, bukan targeting manual
        """)
    
    # Poin 2
    with st.expander("🧠 2. LOGIKA INTI ALGORITMA (CTR, CVR, CPA)", expanded=False):
        st.markdown("""
        **Cara AI mikir:** "Dari semua orang yang lihat iklan ini, siapa yang paling mungkin beli dengan biaya murah?"
        
        **Algoritma pakai 3 sinyal utama:**
        
        | Sinyal | Fungsi |
        |--------|--------|
        | **CTR** | "Apakah orang tertarik?" → Tinggi = disebar luas / Rendah = dipersempit |
        | **CVR** | "Apakah orang beli?" → Klik tinggi tapi gak beli = produk lemah |
        | **CPA** | "Berapa biaya dapetin 1 order?" → **INI YANG PALING PENTING** |
        
        > 🔥 **Rumus dalam kepala algoritma:** Profit ≈ Revenue – Cost, tapi sistem pakai pendekatan ROAS target vs CPA real
        """)
    
    # Poin 3
    with st.expander("🎯 3. PERAN ROAS DI DALAM ALGORITMA", expanded=False):
        st.markdown("""
        **Banyak orang salah kaprah!** ROAS itu bukan target profit, tapi **constraint (batasan sistem)**.
        
        **Cara sistem membaca ROAS:**
        
        | Setting ROAS | Perilaku Algoritma |
        |--------------|-------------------|
        | **Tinggi** | Sistem cari buyer yang "paling pasti beli" → traffic kecil tapi mahal kualitas |
        | **Rendah** | Sistem lebih agresif → traffic luas tapi risk tinggi |
        
        > 🔥 **Kesimpulan:** ROAS = filter kualitas traffic
        """)
    
    # Poin 4
    with st.expander("💸 4. HUBUNGAN ROAS vs BUDGET (MEKANISME DISTRIBUSI)", expanded=False):
        st.markdown("""
        **Cara sistem ambil keputusan:**
        
        1. Cek peluang beli (dari data historis)
        2. Bandingkan dengan target ROAS
        3. Kalau lolos → iklan ditampilkan / Kalau tidak → skip audience itu
        
        | Setting | Respon Algoritma |
        |---------|------------------|
        | ROAS tinggi | selektif |
        | ROAS rendah | eksplorasi |
        | Budget besar | butuh audience luas |
        | Budget kecil | distribusi terbatas |
        
        > 🔥 **Insight:** Budget besar + ROAS tinggi = sistem "bingung" (gak bisa spend)
        """)
    
    # Poin 5
    with st.expander("🔄 5. LEARNING PHASE (PROSES BELAJAR AI)", expanded=False):
        st.markdown("""
        **Apa yang terjadi di dalam?**
        
        Algoritma:
        - Test banyak audience
        - Test banyak placement
        - Kumpulin data CTR & CVR
        - Cari pola pembeli
        
        **Kenapa performa naik turun?** Karena sistem lagi: eksplorasi → gagal → refine → ulangi
        
        > 🔥 **Syarat stabil:** Conversion cukup (±30–50), tidak sering diubah, budget cukup untuk sampling
        
        **❌ Kalau kamu ganggu:** Edit ROAS, ganti budget drastis, pause terlalu cepat → Model reset → balik ke nol
        """)
    
    # Poin 6
    with st.expander("🧪 6. MEKANISME OPTIMISASI OTOMATIS", expanded=False):
        st.markdown("""
        Setelah learning, sistem masuk fase **EXPLOIT MODE**
        
        Algoritma akan:
        - Fokus ke audience yang paling profitable
        - Naikkan distribusi ke segmen itu
        - Kurangi yang tidak perform
        
        > 🔥 **Ini yang disebut:** "Scaling otomatis oleh AI"
        """)
    
    # Poin 7
    with st.expander("📉 7. KENAPA IKLAN BISA DROP?", expanded=False):
        st.markdown("""
        **Karena algoritma bukan statis**
        
        | Penyebab | Penjelasan |
        |----------|------------|
        | Audience fatigue | Audience yang sama sudah jenuh |
        | Kompetitor naik | Auction jadi lebih mahal |
        | Data berubah | Buyer behavior berubah |
        
        > 🔥 **Yang terjadi di sistem:** AI harus cari ulang pola → perform drop sementara
        """)
    
    # Poin 8
    with st.expander("🧠 8. HUBUNGAN PRODUK DENGAN ALGORITMA", expanded=False):
        st.markdown("""
        **Ini yang sering diremehkan!**
        
        Algoritma **TIDAK bisa menyelamatkan produk jelek**
        
        Kenapa? Karena:
        - CTR rendah → sistem stop distribusi
        - CVR rendah → dianggap tidak layak
        
        > 🔥 **Jadi:** Produk = bahan bakar, Algoritma = mesin. Kalau bahan bakar jelek → mesin gak jalan
        """)
    
    # Poin 9
    with st.expander("🎯 9. FLOW KERJA ALGORITMA (END-TO-END)", expanded=False):
        st.markdown("""
        **Versi paling ringkas tapi dalam:**
        
        1. Iklan jalan
        2. Sistem tes audience
        3. Ukur CTR → tertarik?
        4. Ukur CVR → beli?
        5. Hitung CPA
        6. Bandingkan dengan target ROAS
        7. Kalau cocok → scale / Kalau tidak → stop distribusi
        """)
    
    # Poin 10
    with st.expander("🔥 10. RUMUS BESAR GMV MAX (VERSI SISTEM)", expanded=False):
        st.markdown("""
        **Yang sebenarnya terjadi:**
        
        ```
        Profit = (CTR × CVR × AOV) – CPA
        ```
        
        **Tapi sistem menyederhanakan jadi:**
        
        > "Apakah ROAS tercapai?"
        """)
    
    # Poin 11
    with st.expander("⚠️ 11. KESALAHAN YANG BERTENTANGAN DENGAN ALGORITMA", expanded=False):
        st.markdown("""
        **Ini penting banget!**
        
        | ❌ Kesalahan | ✅ Yang Benar |
        |--------------|---------------|
        | Terlalu sering edit | Biarkan sistem belajar (3-5 hari) |
        | Fokus ROAS tinggi dari awal | Mulai dengan ROAS sedang untuk kumpulkan data |
        | Budget terlalu kecil | Pastikan budget cukup untuk sampling |
        | Produk belum valid | Validasi produk dulu sebelum iklan |
        """)
    
    # Poin 12
    with st.expander("🔥 12. KESIMPULAN BESAR", expanded=False):
        st.markdown("""
        **Cara berpikir yang benar:**
        
        Kamu bukan "ngontrol iklan"
        
        Kamu "ngontrol input agar algoritma bekerja optimal"
        
        **3 kontrol utama kamu:**
        - **ROAS** → arahkan kualitas
        - **Budget** → atur volume
        - **Produk & konten** → tentukan hasil
        """)
    
    # Penutup
    st.markdown("""
    <div class="gmv-quote">
    💡 <strong>Inti Satu Kalimat:</strong><br>
    GMV Max adalah sistem distribusi traffic berbasis probabilitas pembelian yang dikontrol oleh constraint ROAS dan diberi makan oleh data CTR & CVR.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== HALAMAN GENERATOR (VERTIKAL) ====================
def render_generator():
    st.markdown("<h2 class='gold-header'>✨ Elite Copywriter Lab</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#94A3B8; margin-bottom:20px;'>Copywriting profesional ala ahli advertising 10 tahun</p>", unsafe_allow_html=True)
    
    # ========== 1. SEO TITLE ==========
    with st.container():
        st.markdown('<div class="generator-card">', unsafe_allow_html=True)
        st.markdown("### 📝 SEO Title")
        st.markdown("Buat judul produk yang menarik dan SEO-friendly")
        
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
4. Output langsung 5 judul, satu per baris, tanpa penjelasan

Contoh format:
🔥 Kaos Oversize Premium | Atasan Wanita | Katun Combed 30s | Adem Tidak Panas

Output:"""
                    res = call_gemini_api(prompt)
                    if res:
                        st.code(res, language="text")
                    else:
                        st.code(f"🔥 {p_name} | Fashion | Premium Quality | Best Seller", language="text")
                else:
                    st.warning("Masukkan nama produk.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ========== 2. DESKRIPSI ==========
    with st.container():
        st.markdown('<div class="generator-card">', unsafe_allow_html=True)
        st.markdown("### 📄 Deskripsi Produk")
        st.markdown("Buat deskripsi produk yang persuasif dan informatif")
        
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

Style: Clean, professional, minimalis.
Output: Direct full description only."""
                    res = call_gemini_api(prompt)
                    if res:
                        st.code(res, language="markdown")
                    else:
                        st.code(f"✨ {p_name_desc} - Kualitas Premium!\n✅ {manfaat if manfaat else 'Bahan premium, nyaman dipakai'}", language="markdown")
                else:
                    st.warning("Masukkan nama produk.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ========== 3. HOOK VIDEO ==========
    with st.container():
        st.markdown('<div class="generator-card">', unsafe_allow_html=True)
        st.markdown("### 🎬 Hook Video")
        st.markdown("Buat hook 3 detik pertama yang bikin orang berhenti scroll")
        
        p_name_hook = st.text_input("🏷️ Nama Produk", placeholder="Contoh: Kaos Oversize Premium", key="hook_name")
        gaya = st.selectbox("Gaya Hook", ["Problem Solver", "Diskon", "Bukti Sosial", "Curiosity", "Emosional"], key="gaya_hook")
        
        if st.button("✨ Generate Hook Video", key="gen_hook", use_container_width=True):
            with st.spinner("🧠 AI creative director sedang membuat hook..."):
                if p_name_hook:
                    prompt = f"""[System: Creative Director TikTok]
Task: Buat 5 hook 3 detik pertama untuk produk '{p_name_hook}' dengan gaya {gaya}.

Aturan:
- Hook harus bikin orang BERHENTI SCROLL
- Maksimal 10 kata per hook
- Format: [Masalah] + [Solusi] + [Urgency]

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
                else:
                    st.warning("Masukkan nama produk.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ========== 4. HASHTAG ==========
    with st.container():
        st.markdown('<div class="generator-card">', unsafe_allow_html=True)
        st.markdown("### #️⃣ Hashtag Viral")
        st.markdown("Buat hashtag yang tepat sasaran dan viral")
        
        p_name_hash = st.text_input("🏷️ Nama Produk", placeholder="Contoh: Kaos Oversize Premium", key="hash_name")
        niche_hash = st.selectbox("Niche", ["Fashion", "Kosmetik", "Makanan", "Elektronik", "Olahraga"], key="niche_hash")
        
        if st.button("✨ Generate Hashtag Viral", key="gen_hash", use_container_width=True):
            with st.spinner("🧠 AI trend analyst sedang meracik hashtag..."):
                if p_name_hash:
                    prompt = f"""[System: Trend Analyst TikTok]
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
                        st.code("#fyp #viral #rekomendasi #shopee #tiktokshop #promo #diskon", language="text")
                else:
                    st.warning("Masukkan nama produk.")
        st.markdown('</div>', unsafe_allow_html=True)

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
<div class="custom-footer">
    <p style="color: #94A3B8; font-size: 0.8rem;">
        Powered by <span style="color: #00E5A0; font-weight: bold;">Arkidigital</span> © 2025
    </p>
</div>
""", unsafe_allow_html=True)

# Tombol logout di footer
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🚪 LOGOUT", key="logout_footer", use_container_width=True):
        st.session_state.clear()
        st.rerun()
