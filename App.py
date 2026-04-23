import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import hashlib
import time

# ==================== INISIALISASI SESSION STATE ====================
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "demo_mode" not in st.session_state:
    st.session_state["demo_mode"] = False
if "demo_start_time" not in st.session_state:
    st.session_state["demo_start_time"] = None
if "demo_analysis_count" not in st.session_state:
    st.session_state["demo_analysis_count"] = 0
if "demo_generator_count" not in st.session_state:
    st.session_state["demo_generator_count"] = 0
if "products" not in st.session_state:
    st.session_state["products"] = []
if "demo_history" not in st.session_state:
    st.session_state["demo_history"] = {}

# ==================== KONFIGURASI ====================
ADMIN_USERNAME = "arkidigital"
ADMIN_PASSWORD = "Arkidigital2026"
CHECKOUT_LINK = "https://muhammad-masruri.myscalev.com/checkout-pageku"
DEMO_DURATION_MINUTES = 5
MAX_DEMO_ANALYSIS = 2
MAX_DEMO_GENERATOR = 2

# ==================== AI CONFIG (Opsional) ====================
AI_AVAILABLE = False  # Nonaktifkan AI sementara

# ==================== CUSTOM CSS (WARNA ASLI - FRIENDLY) ====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Background putih bersih */
    .stApp {
        background: #f8fafc;
    }
    
    /* Card putih dengan bayangan lembut */
    .glass-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
    }
    
    /* Metric card premium */
    .metric-premium {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    }
    
    .metric-premium h3 {
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        color: #64748b;
        margin-bottom: 0.5rem;
    }
    
    .metric-premium h2 {
        font-size: 1.6rem;
        font-weight: 700;
        color: #0f172a;
        margin: 0;
    }
    
    /* Tombol primary - hijau segar */
    .btn-primary {
        background: #10b981;
        color: white;
        padding: 12px 24px;
        border-radius: 40px;
        text-align: center;
        font-weight: 600;
        font-size: 1rem;
        text-decoration: none;
        display: inline-block;
        transition: all 0.3s ease;
        width: 100%;
        border: none;
        cursor: pointer;
    }
    
    .btn-primary:hover {
        background: #059669;
        transform: translateY(-1px);
    }
    
    /* Tombol secondary */
    .btn-secondary {
        background: #f1f5f9;
        color: #334155;
        padding: 12px 24px;
        border-radius: 40px;
        text-align: center;
        font-weight: 600;
        font-size: 0.9rem;
        text-decoration: none;
        display: inline-block;
        transition: all 0.3s ease;
        border: 1px solid #e2e8f0;
        width: 100%;
    }
    
    .btn-secondary:hover {
        background: #e2e8f0;
    }
    
    /* Header premium */
    .premium-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 1rem 1.5rem;
        margin-bottom: 1.5rem;
        color: white;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e2e8f0;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #1e293b;
    }
    
    /* Input field styling */
    .stTextInput > div > div > input, 
    .stNumberInput > div > div > input,
    .stTextArea > div > textarea,
    .stSelectbox > div > div {
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        color: #0f172a !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 2px rgba(102,126,234,0.1) !important;
    }
    
    /* Badge chip */
    .badge-chip {
        background: #f1f5f9;
        border: 1px solid #e2e8f0;
        border-radius: 40px;
        padding: 4px 12px;
        font-size: 0.7rem;
        font-weight: 500;
        display: inline-block;
        color: #475569;
    }
    
    /* Divider */
    .premium-divider {
        height: 1px;
        background: #e2e8f0;
        margin: 1.5rem 0;
    }
    
    /* Footer */
    .premium-footer {
        text-align: center;
        padding: 1.5rem;
        margin-top: 2rem;
        border-top: 1px solid #e2e8f0;
        color: #94a3b8;
        font-size: 0.75rem;
    }
    
    /* Teks umum */
    h1, h2, h3, h4, p {
        color: #0f172a;
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background-color: #10b981;
    }
</style>
""", unsafe_allow_html=True)

# ==================== FUNGSI DEMO ====================
def get_device_fingerprint():
    user_agent = st.context.headers.get('User-Agent', 'unknown')
    ip = st.context.headers.get('X-Forwarded-For', 'unknown')
    return hashlib.md5(f"{user_agent}_{ip}".encode()).hexdigest()

def load_demo_history():
    return st.session_state.demo_history

def can_start_demo(fingerprint):
    history = load_demo_history()
    now = datetime.now()
    if fingerprint not in history:
        history[fingerprint] = {"attempts": []}
    history[fingerprint]["attempts"] = [t for t in history[fingerprint]["attempts"] if now - datetime.fromisoformat(t) < timedelta(hours=24)]
    return len(history[fingerprint]["attempts"]) < 1

def record_demo_start(fingerprint):
    history = load_demo_history()
    if fingerprint not in history:
        history[fingerprint] = {"attempts": []}
    history[fingerprint]["attempts"].append(datetime.now().isoformat())
    st.session_state.demo_history = history

def start_demo():
    fingerprint = get_device_fingerprint()
    if not can_start_demo(fingerprint):
        st.error("⚠️ Demo hanya 1x per 24 jam!")
        st.markdown(f'<a href="{CHECKOUT_LINK}" target="_blank" class="btn-primary" style="display:block;">💎 Beli Premium</a>', unsafe_allow_html=True)
        return False
    record_demo_start(fingerprint)
    st.session_state["demo_mode"] = True
    st.session_state["demo_start_time"] = datetime.now()
    st.session_state["demo_analysis_count"] = 0
    st.session_state["demo_generator_count"] = 0
    st.session_state["authenticated"] = False
    st.rerun()
    return True

def is_demo_expired():
    if not st.session_state.get("demo_mode", False):
        return False
    start = st.session_state.get("demo_start_time")
    if start is None:
        return True
    if datetime.now() - start > timedelta(minutes=DEMO_DURATION_MINUTES):
        st.session_state["demo_mode"] = False
        return True
    return False

def get_demo_remaining():
    if not st.session_state.get("demo_mode", False):
        return 0
    elapsed = (datetime.now() - st.session_state["demo_start_time"]).total_seconds()
    return max(0, DEMO_DURATION_MINUTES * 60 - int(elapsed))

def can_do_demo_analysis():
    return st.session_state.get("demo_analysis_count", 0) < MAX_DEMO_ANALYSIS

def can_do_demo_generator():
    return st.session_state.get("demo_generator_count", 0) < MAX_DEMO_GENERATOR

def inc_demo_analysis():
    if st.session_state.get("demo_mode", False):
        st.session_state["demo_analysis_count"] = st.session_state.get("demo_analysis_count", 0) + 1

def inc_demo_generator():
    if st.session_state.get("demo_mode", False):
        st.session_state["demo_generator_count"] = st.session_state.get("demo_generator_count", 0) + 1

def is_premium():
    return st.session_state.get("authenticated", False)

# ==================== DATABASE PRODUK ====================
def load_products():
    return st.session_state.products

def save_product(p):
    products = load_products()
    for i, prod in enumerate(products):
        if prod["nama"] == p["nama"]:
            products[i] = p
            st.session_state.products = products
            return
    products.append(p)
    st.session_state.products = products

def delete_product(nama):
    products = load_products()
    st.session_state.products = [p for p in products if p["nama"] != nama]

# ==================== PAGE CONFIG ====================
st.set_page_config(page_title="Doctor Ads Premium", page_icon="🩺", layout="wide")

# ==================== CEK AKSES ====================
if not is_premium() and not st.session_state.get("demo_mode", False):
    # Login Page
    st.markdown("""
    <div style="text-align:center; padding:3rem 1rem;">
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 60px; width: 80px; height: 80px; display: flex; align-items: center; justify-content: center; margin: 0 auto 1.5rem auto;">
            <span style="font-size: 40px;">🩺</span>
        </div>
        <h1 style="font-size: 2rem; font-weight: 800; color: #1e293b;">DOCTOR ADS PREMIUM</h1>
        <p style="color: #64748b; margin-bottom: 1rem;">Analisa Iklan TikTok & Shopee → Rekomendasi Perbaikan Instan</p>
        <div class="badge-chip" style="margin-bottom: 2rem;">✨ Hanya Rp147rb (sekali bayar) + Konsultasi GRATIS!</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        with st.form("login"):
            st.markdown("### 🔐 **Login Premium**")
            u = st.text_input("Username", placeholder="Masukkan username")
            p = st.text_input("Password", type="password", placeholder="Masukkan password")
            if st.form_submit_button("🔓 Login", use_container_width=True):
                if u == ADMIN_USERNAME and p == ADMIN_PASSWORD:
                    st.session_state["authenticated"] = True
                    st.session_state["demo_mode"] = False
                    st.rerun()
                else:
                    st.error("❌ Username atau password salah!")
    
    with col2:
        st.markdown("### 🎁 **Coba Demo 5 Menit**")
        st.markdown(f"""
        <div style="background: #f8fafc; border-radius: 16px; padding: 1rem; margin-bottom: 1rem;">
            <small>✅ Maks {MAX_DEMO_ANALYSIS} analisis<br>
            ✅ Maks {MAX_DEMO_GENERATOR} generate<br>
            ✅ 1x per 24 jam</small>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚀 Mulai Demo Gratis", use_container_width=True):
            start_demo()
    
    st.markdown(f"""
    <div class="premium-divider"></div>
    <a href="{CHECKOUT_LINK}" target="_blank" class="btn-primary" style="display:block; text-align:center;">💎 Beli Premium Sekarang</a>
    """, unsafe_allow_html=True)
    st.stop()

if is_demo_expired():
    st.warning("⏰ Demo habis! Beli premium untuk akses penuh.")
    st.markdown(f'<a href="{CHECKOUT_LINK}" target="_blank" class="btn-primary" style="display:block;">💎 Beli Premium Rp147rb</a>', unsafe_allow_html=True)
    st.stop()

# ==================== HEADER PREMIUM ====================
st.markdown(f"""
<div class="premium-header">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="background: rgba(255,255,255,0.15); border-radius: 16px; padding: 8px 14px;">
                <span style="font-size: 24px;">🩺</span>
            </div>
            <div>
                <h1 style="margin: 0; font-size: 1.3rem; font-weight: 700; color: white;">DOCTOR ADS PREMIUM</h1>
                <p style="margin: 0; font-size: 0.7rem; color: rgba(255,255,255,0.8);">Analisa Iklan TikTok & Shopee</p>
            </div>
        </div>
        <div style="display: flex; align-items: center; gap: 12px;">
            <div class="badge-chip" style="background: rgba(255,255,255,0.2); color: white;">{'🎁 DEMO MODE' if not is_premium() else '⭐ PREMIUM MEMBER'}</div>
            <div class="badge-chip" style="background: rgba(255,255,255,0.2); color: white;">{datetime.now().strftime('%d %b %Y')}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0; border-bottom: 1px solid #e2e8f0; margin-bottom: 1rem;">
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 20px; width: 50px; height: 50px; display: flex; align-items: center; justify-content: center; margin: 0 auto 0.8rem auto;">
            <span style="font-size: 28px;">🩺</span>
        </div>
        <h3 style="margin: 0; font-size: 0.9rem; color: #1e293b;">ARKIDIGITAL</h3>
        <p style="margin: 0; font-size: 0.6rem; color: #64748b;">Digital Marketing Solution</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not is_premium():
        rem = get_demo_remaining()
        st.markdown(f"""
        <div style="background: #f1f5f9; border-radius: 16px; padding: 0.8rem; margin-bottom: 1rem; text-align: center;">
            <p style="margin: 0; font-size: 0.7rem; color: #475569;">⏱️ Demo Mode</p>
            <p style="margin: 0; font-size: 1.2rem; font-weight: 700; color: #0f172a;">{rem//60}:{rem%60:02d}</p>
            <p style="margin: 0; font-size: 0.6rem; color: #64748b;">Analisis: {st.session_state.get('demo_analysis_count',0)}/{MAX_DEMO_ANALYSIS} | Generate: {st.session_state.get('demo_generator_count',0)}/{MAX_DEMO_GENERATOR}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Menu sidebar
    st.markdown("### 📋 **Menu**")
    menu = st.radio("", ["📊 Dashboard", "📦 Database Produk", "🎯 Kalkulator BEP", "📋 Cek Produk"], label_visibility="collapsed")
    
    st.markdown("---")
    
    # Database Produk
    if menu == "📦 Database Produk":
        st.markdown("### 📦 **Database Produk**")
        if is_premium():
            products = load_products()
            with st.expander("➕ Tambah/Edit Produk"):
                nama = st.text_input("Nama Produk", key="nama_produk_input")
                hj = st.number_input("Harga Jual", min_value=1000, value=100000, step=5000, key="hj_input")
                modal = st.number_input("Modal", min_value=500, value=60000, step=5000, key="modal_input")
                admin = st.slider("Admin %", 5, 30, 20, key="admin_input")
                if st.button("💾 Simpan", key="simpan_produk") and nama:
                    admin_nom = hj * admin/100
                    laba = hj - modal - admin_nom
                    roas_bep_prod = hj / laba if laba > 0 else 999
                    save_product({"nama": nama, "harga_jual": hj, "modal": modal, "admin_persen": admin, "laba_kotor": laba, "roas_bep": roas_bep_prod})
                    st.success("Tersimpan")
            if products:
                pilih = st.selectbox("Pilih produk", ["--"] + [p["nama"] for p in products], key="pilih_produk")
                if pilih != "--":
                    prod = next(p for p in products if p["nama"] == pilih)
                    harga_jual = prod["harga_jual"]
                    modal = prod["modal"]
                    admin_persen = prod["admin_persen"]
                    laba_kotor = prod["laba_kotor"]
                    roas_bep = prod["roas_bep"]
                    st.info(f"ROAS BEP: {roas_bep:.1f}x | Laba: Rp{laba_kotor:,.0f}")
                    if st.button("🗑️ Hapus", key="hapus_produk"):
                        delete_product(pilih)
                        st.rerun()
                else:
                    harga_jual = st.number_input("Harga Jual", min_value=1000, value=100000, step=5000, key="manual_hj_sidebar")
                    modal = st.number_input("Modal", min_value=500, value=60000, step=5000, key="manual_modal_sidebar")
                    admin_persen = st.slider("Admin %", 5, 30, 20, key="manual_admin_sidebar")
                    admin_nom = harga_jual * admin_persen/100
                    laba_kotor = harga_jual - modal - admin_nom
                    roas_bep = harga_jual / laba_kotor if laba_kotor > 0 else 999
            else:
                harga_jual = st.number_input("Harga Jual", min_value=1000, value=100000, step=5000, key="hj_default")
                modal = st.number_input("Modal", min_value=500, value=60000, step=5000, key="modal_default")
                admin_persen = st.slider("Admin %", 5, 30, 20, key="admin_default")
                admin_nom = harga_jual * admin_persen/100
                laba_kotor = harga_jual - modal - admin_nom
                roas_bep = harga_jual / laba_kotor if laba_kotor > 0 else 999
        else:
            st.info("🔒 Fitur Premium. Beli premium untuk menyimpan produk.")
            harga_jual = st.number_input("Harga Jual", min_value=1000, value=100000, step=5000, key="hj_demo_sidebar")
            modal = st.number_input("Modal", min_value=500, value=60000, step=5000, key="modal_demo_sidebar")
            admin_persen = st.slider("Admin %", 5, 30, 20, key="admin_demo_sidebar")
            admin_nom = harga_jual * admin_persen/100
            laba_kotor = harga_jual - modal - admin_nom
            roas_bep = harga_jual / laba_kotor if laba_kotor > 0 else 999
        
        st.markdown("---")
        st.markdown(f'<a href="{CHECKOUT_LINK}" target="_blank" class="btn-primary" style="display:block; text-align:center;">💎 Upgrade ke Premium</a>', unsafe_allow_html=True)
    
    # Kalkulator BEP
    elif menu == "🎯 Kalkulator BEP":
        st.markdown("### 🎯 **Kalkulator ROAS BEP**")
        col_bep1, col_bep2 = st.columns(2)
        with col_bep1:
            hj_bep = st.number_input("💰 Harga Jual", min_value=1000, value=100000, step=5000, key="bep_hj")
            modal_bep = st.number_input("🏭 Modal", min_value=500, value=60000, step=5000, key="bep_modal")
        with col_bep2:
            admin_bep = st.slider("Admin %", 5, 30, 20, key="bep_admin")
            target_profit_bep = st.number_input("🎯 Target Profit", min_value=0, value=0, step=5000, key="bep_profit")
        
        admin_nom_bep = hj_bep * admin_bep / 100
        laba_kotor_bep = hj_bep - modal_bep - admin_nom_bep - target_profit_bep
        roas_bep_hasil = hj_bep / laba_kotor_bep if laba_kotor_bep > 0 else 999
        
        st.markdown(f"""
        <div style="background: #f8fafc; border-radius: 16px; padding: 1rem; margin-top: 0.5rem;">
            <p style="color: #64748b; margin: 0;">📊 HASIL</p>
            <p style="font-size: 1.5rem; font-weight: 700; color: #0f172a;">ROAS BEP = {roas_bep_hasil:.1f}x</p>
            <p style="font-size: 0.7rem; color: #64748b;">Setiap Rp1 iklan harus menghasilkan minimal Rp{roas_bep_hasil:.1f} penjualan agar tidak rugi.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Cek Produk
    elif menu == "📋 Cek Produk":
        st.markdown("### 📋 **Cek Kelayakan Produk**")
        pernah = st.radio("Produk pernah laku?", ["Ya","Tidak"], horizontal=True, key="pernah_laku")
        if pernah == "Tidak":
            st.error("❌ Jangan iklan dulu!")
        else:
            terjual = st.number_input("Terjual/bulan", 0, 100000, 500, key="terjual")
            if terjual < 1000:
                st.warning("⚠️ Kurang kuat, tes kecil dulu.")
            harga_komp = st.number_input("Harga kompetitor", min_value=1000, value=90000, step=5000, key="harga_komp")
            if 'harga_jual' in locals() and harga_jual > harga_komp * 1.2:
                st.warning("⚠️ Harga terlalu tinggi.")
            if 'laba_kotor' in locals():
                if laba_kotor <= 0:
                    st.error("❌ Margin h
