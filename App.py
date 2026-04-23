import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import hashlib

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

# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: #f8fafc;
    }
    
    .premium-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 1rem 1.5rem;
        margin-bottom: 1.5rem;
        color: white;
    }
    
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
    
    .premium-divider {
        height: 1px;
        background: #e2e8f0;
        margin: 1.5rem 0;
    }
    
    .premium-footer {
        text-align: center;
        padding: 1.5rem;
        margin-top: 2rem;
        border-top: 1px solid #e2e8f0;
        color: #94a3b8;
        font-size: 0.75rem;
    }
    
    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e2e8f0;
    }
    
    .stTextInput > div > div > input, 
    .stNumberInput > div > div > input,
    .stTextArea > div > textarea {
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        color: #0f172a !important;
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
        st.error("Demo hanya 1x per 24 jam!")
        st.markdown(f'<a href="{CHECKOUT_LINK}" target="_blank" class="btn-primary" style="display:block;">Beli Premium</a>', unsafe_allow_html=True)
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
        <p style="color: #64748b; margin-bottom: 1rem;">Analisa Iklan TikTok & Shopee</p>
        <div class="badge-chip" style="margin-bottom: 2rem;">Hanya Rp147rb (sekali bayar)</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        with st.form("login"):
            st.markdown("### Login Premium")
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.form_submit_button("Login", use_container_width=True):
                if u == ADMIN_USERNAME and p == ADMIN_PASSWORD:
                    st.session_state["authenticated"] = True
                    st.session_state["demo_mode"] = False
                    st.rerun()
                else:
                    st.error("Username atau password salah!")
    
    with col2:
        st.markdown("### Coba Demo 5 Menit")
        st.markdown(f"Maks {MAX_DEMO_ANALYSIS} analisis, {MAX_DEMO_GENERATOR} generate")
        if st.button("Mulai Demo Gratis", use_container_width=True):
            start_demo()
    
    st.markdown(f"""
    <div class="premium-divider"></div>
    <a href="{CHECKOUT_LINK}" target="_blank" class="btn-primary" style="display:block; text-align:center;">Beli Premium Sekarang</a>
    """, unsafe_allow_html=True)
    st.stop()

if is_demo_expired():
    st.warning("Demo habis! Beli premium untuk akses penuh.")
    st.markdown(f'<a href="{CHECKOUT_LINK}" target="_blank" class="btn-primary" style="display:block;">Beli Premium</a>', unsafe_allow_html=True)
    st.stop()

# ==================== HEADER ====================
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
            <div class="badge-chip" style="background: rgba(255,255,255,0.2); color: white;">{'DEMO MODE' if not is_premium() else 'PREMIUM'}</div>
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
            <p style="margin: 0; font-size: 0.7rem; color: #475569;">Demo Mode</p>
            <p style="margin: 0; font-size: 1.2rem; font-weight: 700; color: #0f172a;">{rem//60}:{rem%60:02d}</p>
            <p style="margin: 0; font-size: 0.6rem; color: #64748b;">Analisis: {st.session_state.get('demo_analysis_count',0)}/{MAX_DEMO_ANALYSIS}</p>
        </div>
        """, unsafe_allow_html=True)
    
    menu = st.radio("Menu", ["Dashboard", "Database Produk", "Kalkulator BEP"], label_visibility="collapsed")
    
    st.markdown("---")
    
    # Database Produk
    if menu == "Database Produk":
        st.markdown("### Database Produk")
        if is_premium():
            products = load_products()
            with st.expander("Tambah Produk"):
                nama = st.text_input("Nama Produk", key="nama_input")
                hj = st.number_input("Harga Jual", min_value=1000, value=100000, step=5000, key="hj_input")
                modal = st.number_input("Modal", min_value=500, value=60000, step=5000, key="modal_input")
                admin = st.slider("Admin %", 5, 30, 20, key="admin_input")
                if st.button("Simpan", key="simpan") and nama:
                    admin_nom = hj * admin/100
                    laba = hj - modal - admin_nom
                    roas_bep_val = hj / laba if laba > 0 else 999
                    save_product({"nama": nama, "harga_jual": hj, "modal": modal, "admin_persen": admin, "laba_kotor": laba, "roas_bep": roas_bep_val})
                    st.success("Tersimpan")
            if products:
                pilih = st.selectbox("Pilih produk", ["--"] + [p["nama"] for p in products], key="pilih")
                if pilih != "--":
                    prod = next(p for p in products if p["nama"] == pilih)
                    harga_jual = prod["harga_jual"]
                    modal = prod["modal"]
                    admin_persen = prod["admin_persen"]
                    laba_kotor = prod["laba_kotor"]
                    roas_bep = prod["roas_bep"]
                    st.info(f"ROAS BEP: {roas_bep:.1f}x | Laba: Rp{laba_kotor:,.0f}")
                    if st.button("Hapus", key="hapus"):
                        delete_product(pilih)
                        st.rerun()
                else:
                    harga_jual = st.number_input("Harga Jual", min_value=1000, value=100000, step=5000, key="hj_manual")
                    modal = st.number_input("Modal", min_value=500, value=60000, step=5000, key="modal_manual")
                    admin_persen = st.slider("Admin %", 5, 30, 20, key="admin_manual")
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
            st.info("Fitur Premium. Beli premium untuk menyimpan produk.")
            harga_jual = st.number_input("Harga Jual", min_value=1000, value=100000, step=5000, key="hj_demo")
            modal = st.number_input("Modal", min_value=500, value=60000, step=5000, key="modal_demo")
            admin_persen = st.slider("Admin %", 5, 30, 20, key="admin_demo")
            admin_nom = harga_jual * admin_persen/100
            laba_kotor = harga_jual - modal - admin_nom
            roas_bep = harga_jual / laba_kotor if laba_kotor > 0 else 999
        
        st.markdown("---")
        st.markdown(f'<a href="{CHECKOUT_LINK}" target="_blank" class="btn-primary" style="display:block; text-align:center;">Upgrade ke Premium</a>', unsafe_allow_html=True)
    
    # Kalkulator BEP
    elif menu == "Kalkulator BEP":
        st.markdown("### Kalkulator ROAS BEP")
        col_bep1, col_bep2 = st.columns(2)
        with col_bep1:
            hj_bep = st.number_input("Harga Jual", min_value=1000, value=100000, step=5000, key="bep_hj")
            modal_bep = st.number_input("Modal", min_value=500, value=60000, step=5000, key="bep_modal")
        with col_bep2:
            admin_bep = st.slider("Admin %", 5, 30, 20, key="bep_admin")
            target_profit_bep = st.number_input("Target Profit", min_value=0, value=0, step=5000, key="bep_profit")
        
        admin_nom_bep = hj_bep * admin_bep / 100
        laba_kotor_bep = hj_bep - modal_bep - admin_nom_bep - target_profit_bep
        roas_bep_val = hj_bep / laba_kotor_bep if laba_kotor_bep > 0 else 999
        
        st.markdown(f"""
        <div style="background: #f8fafc; border-radius: 16px; padding: 1rem; margin-top: 0.5rem;">
            <p style="color: #64748b; margin: 0;">HASIL</p>
            <p style="font-size: 1.5rem; font-weight: 700; color: #0f172a;">ROAS BEP = {roas_bep_val:.1f}x</p>
        </div>
        """, unsafe_allow_html=True)

# ==================== DASHBOARD ====================
if menu == "Dashboard":
    st.markdown("### Input Data Iklan")
    
    if not is_premium() and not can_do_demo_analysis():
        st.warning(f"Demo terbatas {MAX_DEMO_ANALYSIS}x analisis. Beli premium untuk unlimited!")
        st.markdown(f'<a href="{CHECKOUT_LINK}" target="_blank" class="btn-primary" style="display:block;">Beli Premium</a>', unsafe_allow_html=True)
        st.stop()
    
    colA, colB = st.columns(2)
    with colA:
        impressions = st.number_input("Impressions", min_value=0, value=10000, step=1000, key="imp")
        clicks = st.number_input("Clicks", min_value=0, value=300, step=50, key="cl")
        budget_set = st.number_input("Budget Setting (Rp)", min_value=0, value=100000, step=10000, key="bs")
    with colB:
        budget_spent = st.number_input("Budget Terserap (Rp)", min_value=0, value=90000, step=5000, key="bsp")
        target_roas = st.number_input("Target ROAS", min_value=1.0, value=6.0, step=0.5, key="tr")
        sales = st.number_input("Omset (Rp)", min_value=0, value=600000, step=50000, key="sales")
        orders = st.number_input("Jumlah Order", min_value=0, value=6, step=1, key="ord")
        platform = st.selectbox("Platform", ["Shopee", "TikTok"], key="plat")
    
    analize = st.button("Analisis Iklan", use_container_width=True, key="analize")
    
    if analize:
        if not is_premium():
            inc_demo_analysis()
        
        if clicks > 0 and impressions > 0:
            ctr = (clicks / impressions * 100)
            roas_aktual = sales / budget_spent if budget_spent > 0 else 0
            budget_terserap_persen = (budget_spent / budget_set * 100) if budget_set > 0 else 0
            profit_estimasi = (laba_kotor * orders) - budget_spent if orders > 0 else -budget_spent
        else:
            ctr = 0; roas_aktual = 0; budget_terserap_persen = 0; profit_estimasi = -budget_spent
        
        def format_rp(angka):
            if angka >= 1_000_000:
                return f"Rp{angka/1_000_000:.1f}JT"
            elif angka >= 1000:
                return f"Rp{angka/1000:.0f}RB"
            return f"Rp{angka:,.0f}"
        
        # Metric Cards
        st.markdown("### Dashboard Performa")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class="metric-premium">
                <h3>TOTAL BELANJA</h3>
                <h2>{format_rp(budget_spent)}</h2>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-premium">
                <h3>TOTAL OMSET</h3>
                <h2>{format_rp(sales)}</h2>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="metric-premium">
                <h3>ROAS AKTUAL</h3>
                <h2>{roas_aktual:.1f}x</h2>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            warna_profit = "#10b981" if profit_estimasi > 0 else "#ef4444"
            st.markdown(f"""
            <div class="metric-premium">
                <h3>ESTIMASI PROFIT</h3>
                <h2 style="color: {warna_profit};">{format_rp(profit_estimasi)}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        # Rekomendasi
        st.markdown("---")
        st.markdown("### Kesimpulan & Rekomendasi")
        
        rekomendasi_tindakan = ""
        new_target = target_roas
        new_budget = budget_set
        
        if clicks > 50 and budget_terserap_persen >= 80 and orders == 0:
            rekomendasi_tindakan = f"HENTIKAN IKLAN! Data: {clicks} klik, budget terserap {budget_terserap_persen:.0f}%, 0 order. Perbaiki produk terlebih dahulu."
        elif budget_terserap_persen >= 85 and roas_aktual >= roas_bep * 1.2:
            new_budget = budget_set * 1.3
            rekomendasi_tindakan = f"SIAP SCALE! Naikkan BUDGET 30% menjadi Rp{new_budget:,.0f}. Tunggu 3 hari tanpa perubahan."
        elif roas_aktual >= roas_bep and budget_terserap_persen < 85:
            new_target = target_roas - 0.5
            rekomendasi_tindakan = f"OPTIMASI! Turunkan target ROAS 0.5 poin menjadi {new_target:.1f}x. Tunggu 3 hari."
        elif roas_aktual < roas_bep and roas_aktual > 0:
            new_target = roas_bep + 0.5
            rekomendasi_tindakan = f"IKLAN RUGI! Naikkan target ROAS 0.5 poin menjadi {new_target:.1f}x. Tunggu 3 hari."
        elif roas_aktual >= roas_bep:
            rekomendasi_tindakan = f"PERFORMA SEHAT. Pertahankan setting, pantau 3-5 hari."
        
        if ctr < 2 and clicks > 0:
            rekomendasi_tindakan += f"\n\nCTR Rendah ({ctr:.1f}% < 2%). Ganti visual iklan."
        
        st.markdown(f"""
        <div style="background: #f8fafc; border-radius: 16px; padding: 1rem; margin: 1rem 0;">
            <p>{rekomendasi_tindakan}</p>
            <div class="premium-divider"></div>
            <p><strong>Budget rekomendasi:</strong> {format_rp(new_budget)} | <strong>Target ROAS rekomendasi:</strong> {new_target:.1f}x</p>
        </div>
        """, unsafe_allow_html=True)

# ==================== GENERATOR ====================
if menu == "Dashboard":
    st.markdown("---")
    st.markdown("### Generator Konten")
    
    def generator_access():
        if is_premium():
            return True
        if can_do_demo_generator():
            return True
        st.warning("Demo hanya 2x generate. Beli premium untuk unlimited!")
        return False
    
    mode_gen = st.radio("Pilih Mode:", ["Mode Shopee", "Mode TikTok"], horizontal=True, key="mode_gen")
    
    tab1, tab2, tab3 = st.tabs(["SEO Title", "Deskripsi", "Hook Video"])
    
    if mode_gen == "Mode Shopee":
        with tab1:
            nama_prod = st.text_input("Nama Produk", key="seo_prod")
            if st.button("Generate Judul SEO", key="gen_seo"):
                if generator_access():
                    if not is_premium():
                        inc_demo_generator()
                    if nama_prod:
                        titles = [
                            f"🔥 {nama_prod} - Kualitas Premium",
                            f"💯 {nama_prod} BEST SELLER",
                            f"✨ WAJIB PUNYA! {nama_prod}",
                            f"🎯 {nama_prod} Dijamin Nyaman"
                        ]
                        for t in titles:
                            st.markdown(f"- {t}")
        with tab2:
            nama_prod = st.text_input("Nama Produk", key="desc_prod")
            if st.button("Generate Deskripsi", key="gen_desc"):
                if generator_access():
                    if not is_premium():
                        inc_demo_generator()
                    if nama_prod:
                        desc = f"✨ {nama_prod} - Kualitas Premium!\n✅ Bahan berkualitas\n✅ Desain modern\n✅ Garansi 100%"
                        st.code(desc, language="markdown")
        with tab3:
            nama_prod = st.text_input("Nama Produk", key="hook_prod")
            if st.button("Generate Hook", key="gen_hook"):
                if generator_access():
                    if not is_premium():
                        inc_demo_generator()
                    if nama_prod:
                        hooks = [f"🛍️ {nama_prod} - Kualitas Premium!", f"📦 {nama_prod} - FREE ONGKIR!"]
                        for h in hooks:
                            st.markdown(f"- 🎬 {h}")
    else:
        with tab1:
            nama_prod = st.text_input("Nama Produk", key="seo_tiktok_prod")
            if st.button("Generate Judul Viral", key="gen_seo_tiktok"):
                if generator_access():
                    if not is_premium():
                        inc_demo_generator()
                    if nama_prod:
                        titles = [
                            f"😭 STOP! Jangan beli {nama_prod}",
                            f"🔥 VIRAL! {nama_prod}",
                            f"💯 WAJIB PUNYA! {nama_prod}"
                        ]
                        for t in titles:
                            st.markdown(f"- 🎥 {t}")
        with tab2:
            nama_prod = st.text_input("Nama Produk", key="desc_tiktok_prod")
            if st.button("Generate Deskripsi", key="gen_desc_tiktok"):
                if generator_access():
                    if not is_premium():
                        inc_demo_generator()
                    if nama_prod:
                        desc = f"Dulu aku... TAPI setelah pake {nama_prod}\n✨ Bahan premium\n🔥 PROMO TERBATAS!"
                        st.code(desc, language="markdown")
        with tab3:
            nama_prod = st.text_input("Nama Produk", key="hook_tiktok_prod")
            if st.button("Generate Hook Viral", key="gen_hook_tiktok"):
                if generator_access():
                    if not is_premium():
                        inc_demo_generator()
                    if nama_prod:
                        hooks = [f"😫 Capek cari {nama_prod}? STOP!", f"🔥 DISKON 50% {nama_prod}!"]
                        for h in hooks:
                            st.markdown(f"- 🎬 {h}")

# ==================== FOOTER ====================
st.markdown("""
<div class="premium-footer">
    <p>🩺 DOCTOR ADS SHOPEE & TIKTOK PREMIUM</p>
    <p>© 2024 Arkidigital</p>
</div>
""", unsafe_allow_html=True)
