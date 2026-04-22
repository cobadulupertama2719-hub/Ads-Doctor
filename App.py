import streamlit as st
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import hashlib
import webbrowser

st.set_page_config(page_title="Doctor Ads Shopee & TikTok Premium", page_icon="🩺", layout="wide")

# ==================== KONFIGURASI ====================
ADMIN_USERNAME = "arkidigital"
ADMIN_PASSWORD = "Arkidigital2026"

# Nomor WhatsApp Mas
WA_NUMBER = "6288228878258"
WA_LINK = f"https://wa.me/{WA_NUMBER}?text=Halo%20Arkidigital%2C%20saya%20mau%20beli%20Doctor%20Ads%20Premium%20Rp147rb"

# Konfigurasi Demo
DEMO_DURATION_MINUTES = 5  # 5 menit demo
MAX_DEMO_ANALYSIS = 2  # Maks 2 kali analisis di mode demo
MAX_DEMO_GENERATOR = 2  # Maks 2 kali generate di mode demo

# ==================== FUNGSI DEMO DENGAN LIMIT PER AKUN ====================
def get_device_fingerprint():
    """Membuat fingerprint unik berdasarkan browser & IP (sederhana)"""
    user_agent = st.context.headers.get('User-Agent', 'unknown')
    ip = st.context.headers.get('X-Forwarded-For', 'unknown')
    fingerprint = hashlib.md5(f"{user_agent}_{ip}".encode()).hexdigest()
    return fingerprint

def load_demo_history():
    """Muat history demo dari session state (simulasi database)"""
    if "demo_history" not in st.session_state:
        st.session_state.demo_history = {}
    return st.session_state.demo_history

def save_demo_attempt(fingerprint):
    """Simpan percobaan demo"""
    history = load_demo_history()
    now = datetime.now()
    
    if fingerprint not in history:
        history[fingerprint] = {
            "attempts": [],
            "total_attempts": 0
        }
    
    # Hapus percobaan yang sudah lebih dari 24 jam
    history[fingerprint]["attempts"] = [
        t for t in history[fingerprint]["attempts"] 
        if now - datetime.fromisoformat(t) < timedelta(hours=24)
    ]
    
    return history

def can_start_demo(fingerprint):
    """Cek apakah device bisa mulai demo baru"""
    history = load_demo_history()
    save_demo_attempt(fingerprint)
    
    if fingerprint not in history:
        return True
    
    # Maks 1 kali demo per 24 jam
    return len(history[fingerprint]["attempts"]) < 1

def record_demo_start(fingerprint):
    """Catat bahwa device sudah mulai demo"""
    history = load_demo_history()
    now = datetime.now().isoformat()
    
    if fingerprint not in history:
        history[fingerprint] = {"attempts": [], "total_attempts": 0}
    
    history[fingerprint]["attempts"].append(now)
    history[fingerprint]["total_attempts"] += 1
    st.session_state.demo_history = history

def start_demo():
    """Memulai sesi demo"""
    fingerprint = get_device_fingerprint()
    
    if not can_start_demo(fingerprint):
        st.error("⚠️ **Anda sudah pernah mencoba demo!** Demo hanya bisa 1x per 24 jam.")
        st.info("💎 Beli premium untuk akses penuh tanpa batasan!")
        
        # Tombol WA di sini
        wa_button = f'''
        <a href="{WA_LINK}" target="_blank">
            <button style="background: linear-gradient(135deg, #25D366 0%, #128C7E 100%); color: white; border: none; padding: 0.6rem 1rem; border-radius: 0.5rem; font-weight: bold; width: 100%; cursor: pointer; margin-top: 0.5rem;">
                💬 Hubungi Kami via WhatsApp
            </button>
        </a>
        '''
        st.markdown(wa_button, unsafe_allow_html=True)
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
    """Cek apakah demo sudah habis"""
    if not st.session_state.get("demo_mode", False):
        return False
    start_time = st.session_state.get("demo_start_time")
    if start_time is None:
        return True
    expired = datetime.now() - start_time > timedelta(minutes=DEMO_DURATION_MINUTES)
    if expired:
        st.session_state["demo_mode"] = False
    return expired

def get_demo_remaining_time():
    """Mendapatkan sisa waktu demo"""
    if not st.session_state.get("demo_mode", False):
        return 0
    start_time = st.session_state.get("demo_start_time")
    if start_time is None:
        return 0
    elapsed = datetime.now() - start_time
    remaining = max(0, DEMO_DURATION_MINUTES * 60 - elapsed.total_seconds())
    return int(remaining)

def can_do_demo_analysis():
    """Cek apakah masih bisa melakukan analisis di mode demo"""
    count = st.session_state.get("demo_analysis_count", 0)
    return count < MAX_DEMO_ANALYSIS

def can_do_demo_generator():
    """Cek apakah masih bisa melakukan generate di mode demo"""
    count = st.session_state.get("demo_generator_count", 0)
    return count < MAX_DEMO_GENERATOR

def increment_demo_analysis():
    """Menambah hitungan analisis demo"""
    if st.session_state.get("demo_mode", False):
        st.session_state["demo_analysis_count"] = st.session_state.get("demo_analysis_count", 0) + 1

def increment_demo_generator():
    """Menambah hitungan generator demo"""
    if st.session_state.get("demo_mode", False):
        st.session_state["demo_generator_count"] = st.session_state.get("demo_generator_count", 0) + 1

def is_premium_user():
    """Cek apakah user premium (login asli)"""
    return st.session_state.get("authenticated", False)

# ==================== LOGIN + DEMO BUTTON ====================
def show_login_or_demo():
    """Menampilkan pilihan login atau demo"""
    
    st.markdown("""
    <div style="text-align: center; padding: 2rem;">
        <h1>🩺 DOCTOR ADS SHOPEE & TIKTOK PREMIUM</h1>
        <p>Analisa Iklan TikTok & Shopee → Rekomendasi Perbaikan</p>
        <p style="color: #666; font-size: 0.8rem;">Hanya Rp147rb (sekali bayar) + Konsultasi GRATIS!</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.form("Login Form"):
            st.markdown("### 🔐 **Login Premium**")
            username = st.text_input("Username", placeholder="Masukkan username")
            password = st.text_input("Password", type="password", placeholder="Masukkan password")
            submitted = st.form_submit_button("🔓 Login", use_container_width=True)
            if submitted:
                if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                    st.session_state["authenticated"] = True
                    st.session_state["demo_mode"] = False
                    st.rerun()
                else:
                    st.error("❌ Username atau password salah!")
    
    with col2:
        st.markdown("### 🎁 **Coba Demo 5 Menit**")
        st.markdown(f"""
        <div style="background: #f0f0ff; padding: 1rem; border-radius: 0.8rem;">
            <small>✅ Gratis 5 menit akses penuh<br>
            ✅ Maks {MAX_DEMO_ANALYSIS} kali analisis<br>
            ✅ Maks {MAX_DEMO_GENERATOR} kali generate<br>
            ✅ 1x demo per 24 jam per device<br>
            ❌ Data tidak tersimpan</small>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚀 Mulai Demo Gratis", use_container_width=True):
            start_demo()
    
    st.markdown("---")
    
    # Tombol WhatsApp di halaman login
    wa_button = f'''
    <div style="background: #f8f9fa; padding: 1rem; border-radius: 0.8rem; text-align: center;">
        <p>💬 <strong>Butuh bantuan atau mau order?</strong><br>
        Hubungi kami langsung via WhatsApp</p>
        <a href="{WA_LINK}" target="_blank">
            <button style="background: linear-gradient(135deg, #25D366 0%, #128C7E 100%); color: white; border: none; padding: 0.6rem 1rem; border-radius: 0.5rem; font-weight: bold; width: 100%; cursor: pointer;">
                💬 Chat Admin via WhatsApp
            </button>
        </a>
        <p style="font-size: 0.7rem; margin-top: 0.5rem;">Respon cepat: 08:00 - 22:00</p>
    </div>
    '''
    st.markdown(wa_button, unsafe_allow_html=True)
    
    return False

# ==================== DEMO TIMER ====================
def show_demo_timer():
    """Menampilkan timer demo di sidebar"""
    if st.session_state.get("demo_mode", False):
        remaining = get_demo_remaining_time()
        minutes = remaining // 60
        seconds = remaining % 60
        analysis_left = MAX_DEMO_ANALYSIS - st.session_state.get("demo_analysis_count", 0)
        generator_left = MAX_DEMO_GENERATOR - st.session_state.get("demo_generator_count", 0)
        
        # Peringatan jika tinggal 1 menit
        if remaining <= 60:
            st.sidebar.markdown(f"""
            <div style="background: #fee2e2; padding: 0.5rem; border-radius: 0.5rem; text-align: center; margin-bottom: 1rem;">
                <small>⏰ <strong>Demo akan berakhir!</strong><br>
                Sisa: {minutes:02d}:{seconds:02d}<br>
                Analisis: {analysis_left} kesempatan<br>
                Generate: {generator_left} kesempatan</small>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.sidebar.markdown(f"""
            <div style="background: #f0f0ff; padding: 0.5rem; border-radius: 0.5rem; text-align: center; margin-bottom: 1rem;">
                <small>🎁 <strong>Mode Demo</strong><br>
                Sisa: {minutes:02d}:{seconds:02d}<br>
                Analisis: {analysis_left}/{MAX_DEMO_ANALYSIS}<br>
                Generate: {generator_left}/{MAX_DEMO_GENERATOR}</small>
            </div>
            """, unsafe_allow_html=True)
        
        # Tombol WA di sidebar demo
        wa_button = f'''
        <a href="{WA_LINK}" target="_blank">
            <button style="background: linear-gradient(135deg, #25D366 0%, #128C7E 100%); color: white; border: none; padding: 0.5rem; border-radius: 0.5rem; font-weight: bold; width: 100%; cursor: pointer; font-size: 0.8rem;">
                💬 Beli Premium Rp147rb
            </button>
        </a>
        '''
        st.sidebar.markdown(wa_button, unsafe_allow_html=True)

# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0.8rem 1.2rem;
        border-radius: 1rem;
        color: white;
        margin-bottom: 1rem;
    }
    .logo-container { display: flex; align-items: center; gap: 0.8rem; }
    .logo-text h1 { font-size: 1.2rem; margin: 0; font-weight: 700; }
    .logo-text p { margin: 0; font-size: 0.65rem; opacity: 0.85; }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0.6rem;
        border-radius: 0.8rem;
        color: white;
        text-align: center;
    }
    .metric-card h3 { font-size: 0.6rem; margin-bottom: 0.2rem; }
    .metric-card h2 { font-size: 1.1rem; margin: 0; }
    .badge-success { background: #d1fae5; color: #059669; padding: 0.15rem 0.5rem; border-radius: 2rem; font-size: 0.6rem; }
    .badge-danger { background: #fee2e2; color: #dc2626; padding: 0.15rem 0.5rem; border-radius: 2rem; font-size: 0.6rem; }
    .badge-warning { background: #fef3c7; color: #d97706; padding: 0.15rem 0.5rem; border-radius: 2rem; font-size: 0.6rem; }
    .badge-info { background: #dbeafe; color: #2563eb; padding: 0.15rem 0.5rem; border-radius: 2rem; font-size: 0.6rem; }
    .divider { height: 2px; background: linear-gradient(90deg, #667eea, #764ba2, #667eea); border-radius: 2px; margin: 0.8rem 0; }
    .footer { text-align: center; color: #888; font-size: 0.6rem; padding: 0.8rem 0 0.2rem; border-top: 1px solid #eee; margin-top: 0.8rem; }
    .stButton > button { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 0.5rem; font-weight: 600; width: 100%; }
    .premium-badge { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 0.2rem 0.6rem; border-radius: 2rem; font-size: 0.6rem; display: inline-block; }
    .demo-limit-warning { background: #fef3c7; border-left: 3px solid #f59e0b; padding: 0.5rem; border-radius: 0.5rem; margin: 0.5rem 0; font-size: 0.7rem; }
</style>
""", unsafe_allow_html=True)

# ==================== CEK AKSES ====================
if not is_premium_user() and not st.session_state.get("demo_mode", False):
    show_login_or_demo()
    st.stop()

# Jika demo expired
if is_demo_expired():
    st.warning("⏰ **Demo Anda telah berakhir!** Beli premium untuk akses penuh tanpa batasan.")
    
    wa_button = f'''
    <a href="{WA_LINK}" target="_blank">
        <button style="background: linear-gradient(135deg, #25D366 0%, #128C7E 100%); color: white; border: none; padding: 0.6rem; border-radius: 0.5rem; font-weight: bold; width: 100%; cursor: pointer;">
            💬 Beli Premium Rp147rb via WhatsApp
        </button>
    </a>
    '''
    st.markdown(wa_button, unsafe_allow_html=True)
    st.stop()

# Tampilkan timer demo di sidebar
if st.session_state.get("demo_mode", False):
    show_demo_timer()

# ==================== TAMPILAN UTAMA ====================
col_logout1, col_logout2, col_logout3 = st.columns([6, 1, 1])
with col_logout3:
    if is_premium_user():
        if st.button("🚪 Logout"):
            st.session_state["authenticated"] = False
            st.rerun()
    elif st.session_state.get("demo_mode", False):
        st.markdown('<span class="premium-badge">🎁 DEMO MODE (5 menit)</span>', unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <div class="logo-container">
        <div style="background: white; border-radius: 0.6rem; padding: 0.2rem 0.6rem;"><span style="font-size: 1.2rem;">🩺</span></div>
        <div class="logo-text"><h1>Arkidigital</h1><p>Solusi Digital Marketing Terbaik untuk Bisnis Anda</p></div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==================== DATABASE PRODUK ====================
with st.sidebar:
    st.markdown("## 📦 **Database Produk**")
    
    if is_premium_user():
        # Premium: bisa simpan banyak produk
        if "products" not in st.session_state:
            st.session_state.products = []
        products = st.session_state.products
        
        with st.expander("➕ Tambah/Edit Produk"):
            nama_produk = st.text_input("Nama Produk", placeholder="Contoh: Kaos Oversize")
            harga_jual_input = st.number_input("Harga Jual (Rp)", min_value=1000, value=100000, step=5000)
            modal_input = st.number_input("Modal / HPP (Rp)", min_value=500, value=60000, step=5000)
            admin_input = st.slider("Admin Marketplace (%)", 5, 30, 20, 1)
            
            if st.button("💾 Simpan Produk", use_container_width=True):
                if nama_produk:
                    admin_nom = harga_jual_input * (admin_input / 100)
                    laba = harga_jual_input - modal_input - admin_nom
                    roas_bep_produk = harga_jual_input / laba if laba > 0 else 999
                    existing = [p for p in products if p["nama"] == nama_produk]
                    if existing:
                        for i, p in enumerate(products):
                            if p["nama"] == nama_produk:
                                products[i] = {"nama": nama_produk, "harga_jual": harga_jual_input, "modal": modal_input, "admin_persen": admin_input, "laba_kotor": laba, "roas_bep": roas_bep_produk}
                                break
                    else:
                        products.append({"nama": nama_produk, "harga_jual": harga_jual_input, "modal": modal_input, "admin_persen": admin_input, "laba_kotor": laba, "roas_bep": roas_bep_produk})
                    st.session_state.products = products
                    st.success(f"✅ {nama_produk} disimpan!")
                    st.rerun()
        
        if products:
            st.markdown("### 📋 Pilih Produk")
            product_names = [p["nama"] for p in products]
            selected_product = st.selectbox("Pilih produk", ["-- Pilih Produk --"] + product_names)
            
            if selected_product != "-- Pilih Produk --":
                prod = [p for p in products if p["nama"] == selected_product][0]
                harga_jual = prod["harga_jual"]
                modal = prod["modal"]
                admin_persen = prod["admin_persen"]
                laba_kotor = prod["laba_kotor"]
                roas_bep = prod["roas_bep"]
                st.markdown(f"""
                <div style="background: #f0f0ff; padding: 0.6rem; border-radius: 0.6rem; margin-top: 0.3rem;">
                    <small><strong>📊 {selected_product}</strong><br>
                    Harga: Rp{harga_jual:,.0f}<br>
                    Laba: Rp{laba_kotor:,.0f}<br>
                    <strong>ROAS BEP = {roas_bep:.1f}x</strong></small>
                </div>
                """, unsafe_allow_html=True)
                if st.button("🗑️ Hapus Produk", use_container_width=True):
                    st.session_state.products = [p for p in products if p["nama"] != selected_product]
                    st.rerun()
            else:
                harga_jual = st.number_input("💰 Harga Jual (Rp)", min_value=1000, value=100000, step=5000, key="manual_harga")
                modal = st.number_input("🏭 Modal / HPP (Rp)", min_value=500, value=60000, step=5000, key="manual_modal")
                admin_persen = st.slider("🏪 Admin Marketplace (%)", 5, 30, 20, 1, key="manual_admin")
                admin_nominal = harga_jual * (admin_persen / 100)
                laba_kotor = harga_jual - modal - admin_nominal
                roas_bep = harga_jual / laba_kotor if laba_kotor > 0 else 999
                st.markdown(f"<div style='background:#f0f0ff;padding:0.6rem;border-radius:0.6rem;'><small><strong>ROAS BEP = {roas_bep:.1f}x</strong><br>Laba: Rp{laba_kotor:,.0f}</small></div>", unsafe_allow_html=True)
        else:
            harga_jual = st.number_input("💰 Harga Jual (Rp)", min_value=1000, value=100000, step=5000)
            modal = st.number_input("🏭 Modal / HPP (Rp)", min_value=500, value=60000, step=5000)
            admin_persen = st.slider("🏪 Admin Marketplace (%)", 5, 30, 20, 1)
            admin_nominal = harga_jual * (admin_persen / 100)
            laba_kotor = harga_jual - modal - admin_nominal
            roas_bep = harga_jual / laba_kotor if laba_kotor > 0 else 999
            st.markdown(f"<div style='background:#f0f0ff;padding:0.6rem;border-radius:0.6rem;'><small><strong>ROAS BEP = {roas_bep:.1f}x</strong><br>Laba: Rp{laba_kotor:,.0f}</small></div>", unsafe_allow_html=True)
            st.info("💡 Premium: Simpan produk agar tidak input ulang!")
    else:
        # Demo: hanya bisa input manual, tidak bisa simpan
        st.info("🎁 **Mode Demo** - Silakan input manual")
        st.markdown(f'<div class="demo-limit-warning">⚠️ Demo terbatas {MAX_DEMO_ANALYSIS}x analisis & {MAX_DEMO_GENERATOR}x generate</div>', unsafe_allow_html=True)
        harga_jual = st.number_input("💰 Harga Jual (Rp)", min_value=1000, value=100000, step=5000)
        modal = st.number_input("🏭 Modal / HPP (Rp)", min_value=500, value=60000, step=5000)
        admin_persen = st.slider("🏪 Admin Marketplace (%)", 5, 30, 20, 1)
        admin_nominal = harga_jual * (admin_persen / 100)
        laba_kotor = harga_jual - modal - admin_nominal
        roas_bep = harga_jual / laba_kotor if laba_kotor > 0 else 999
        st.markdown(f"<div style='background:#f0f0ff;padding:0.6rem;border-radius:0.6rem;'><small><strong>ROAS BEP = {roas_bep:.1f}x</strong><br>Laba: Rp{laba_kotor:,.0f}</small></div>", unsafe_allow_html=True)
        st.caption("💎 Beli premium untuk simpan produk!")

# ==================== INPUT DATA IKLAN ====================
st.subheader("📝 **Input Data Iklan Hari Ini**")

# Cek limit analisis demo
if st.session_state.get("demo_mode", False) and not can_do_demo_analysis():
    st.warning(f"⚠️ **Demo terbatas maksimal {MAX_DEMO_ANALYSIS} kali analisis.** Beli premium untuk akses unlimited!")
    
    wa_button = f'''
    <a href="{WA_LINK}" target="_blank">
        <button style="background: linear-gradient(135deg, #25D366 0%, #128C7E 100%); color: white; border: none; padding: 0.6rem; border-radius: 0.5rem; font-weight: bold; width: 100%; cursor: pointer;">
            💬 Beli Premium Rp147rb via WhatsApp
        </button>
    </a>
    '''
    st.markdown(wa_button, unsafe_allow_html=True)
    st.stop()

col1, col2 = st.columns(2)

with col1:
    impressions = st.number_input("👁️ Pengunjung (Impressions)", min_value=0, value=10000, step=1000)
    clicks = st.number_input("🖱️ Klik (Clicks)", min_value=0, value=300, step=50)
    budget_set = st.number_input("💵 Budget Setting (Rp/hari)", min_value=0, value=100000, step=10000)

with col2:
    budget_spent = st.number_input("💸 Budget Terserap (Rp/hari)", min_value=0, value=90000, step=5000)
    target_roas = st.number_input("🎯 Target ROAS Setting", min_value=1.0, value=6.0, step=0.5)
    sales = st.number_input("💰 Omset (Rp)", min_value=0, value=600000, step=50000)
    orders = st.number_input("📦 Jumlah Order", min_value=0, value=6, step=1)
    platform = st.selectbox("📱 Platform", ["Shopee", "TikTok"])

analyze_clicked = st.button("🔍 Analisis Iklan", use_container_width=True)

if analyze_clicked:
    if st.session_state.get("demo_mode", False):
        increment_demo_analysis()
    
    # Hitung metrik
    if clicks > 0 and impressions > 0:
        ctr = (clicks / impressions * 100)
        cpc = budget_spent / clicks
        roas_aktual = sales / budget_spent if budget_spent > 0 else 0
        budget_terserap_persen = (budget_spent / budget_set * 100) if budget_set > 0 else 0
        profit_estimasi = (laba_kotor * orders) - budget_spent if orders > 0 else -budget_spent
        status_profit = "UNTUNG" if profit_estimasi > 0 else "RUGI"
    else:
        ctr = 0
        cpc = 0
        roas_aktual = 0
        budget_terserap_persen = 0
        profit_estimasi = -budget_spent
        status_profit = "RUGI"

    def format_rp(angka):
        if angka >= 1000000:
            return f"Rp{angka/1000000:.1f}JT"
        elif angka >= 1000:
            return f"Rp{angka/1000:.0f}RB"
        return f"Rp{angka:,.0f}"

    # Metric Cards
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"<div class='metric-card'><h3>📈 CTR</h3><h2>{ctr:.1f}%</h2><p>{'✅ Bagus' if ctr >= 2 else '⚠️ Perlu perbaikan'}</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-card'><h3>💰 ROAS Aktual</h3><h2>{roas_aktual:.1f}x</h2><p>BEP: {roas_bep:.1f}x</p></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='metric-card'><h3>💸 Budget Terserap</h3><h2>{budget_terserap_persen:.0f}%</h2><p>Dari {format_rp(budget_set)}</p></div>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<div class='metric-card'><h3>💎 Estimasi Profit</h3><h2>{format_rp(profit_estimasi)}</h2><p>{status_profit}</p></div>", unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.subheader("🩺 **Diagnosis & Kesimpulan**")

    # Diagnosis Tabel
    st.markdown("""
    <div style="background: white; border-radius: 0.8rem; border: 1px solid #e5e7eb; overflow: hidden;">
        <div style="background: #f9fafb; padding: 0.5rem 0.8rem; border-bottom: 1px solid #e5e7eb;"><b>📋 Diagnostik Performa Iklan</b></div>
    """, unsafe_allow_html=True)

    if ctr >= 2:
        st.markdown(f"<div style='display: flex; padding: 0.4rem 0.8rem; border-bottom: 1px solid #f0f0f0;'><div style='width: 35%; font-weight: 500;'>📊 CTR</div><div style='width: 65%;'>{ctr:.1f}% <span class='badge-success'>✅ BAGUS</span><br><small>CTR di atas 2%, visual menarik</small></div></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='display: flex; padding: 0.4rem 0.8rem; border-bottom: 1px solid #f0f0f0;'><div style='width: 35%; font-weight: 500;'>📊 CTR</div><div style='width: 65%;'>{ctr:.1f}% <span class='badge-danger'>⚠️ RENDAH</span><br><small>CTR di bawah 2%, perlu ganti visual</small></div></div>", unsafe_allow_html=True)

    if roas_aktual >= roas_bep:
        st.markdown(f"<div style='display: flex; padding: 0.4rem 0.8rem; border-bottom: 1px solid #f0f0f0;'><div style='width: 35%; font-weight: 500;'>💰 ROAS</div><div style='width: 65%;'>{roas_aktual:.1f}x <span class='badge-success'>✅ PROFIT</span><br><small>ROAS > BEP, iklan untung</small></div></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='display: flex; padding: 0.4rem 0.8rem; border-bottom: 1px solid #f0f0f0;'><div style='width: 35%; font-weight: 500;'>💰 ROAS</div><div style='width: 65%;'>{roas_aktual:.1f}x <span class='badge-danger'>🔴 RUGI</span><br><small>ROAS < BEP, iklan boncos</small></div></div>", unsafe_allow_html=True)

    if budget_terserap_persen >= 90:
        st.markdown(f"<div style='display: flex; padding: 0.4rem 0.8rem; border-bottom: 1px solid #f0f0f0;'><div style='width: 35%; font-weight: 500;'>⏳ Budget Terserap</div><div style='width: 65%;'>{budget_terserap_persen:.0f}% <span class='badge-success'>✅ HABIS</span><br><small>Sistem bekerja optimal</small></div></div>", unsafe_allow_html=True)
    elif budget_terserap_persen >= 50:
        st.markdown(f"<div style='display: flex; padding: 0.4rem 0.8rem; border-bottom: 1px solid #f0f0f0;'><div style='width: 35%; font-weight: 500;'>⏳ Budget Terserap</div><div style='width: 65%;'>{budget_terserap_persen:.0f}% <span class='badge-warning'>🟡 KURANG</span><br><small>Target ROAS terlalu ketat</small></div></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='display: flex; padding: 0.4rem 0.8rem; border-bottom: 1px solid #f0f0f0;'><div style='width: 35%; font-weight: 500;'>⏳ Budget Terserap</div><div style='width: 65%;'>{budget_terserap_persen:.0f}% <span class='badge-danger'>🔴 SEDIKIT</span><br><small>Target ROAS terlalu tinggi</small></div></div>", unsafe_allow_html=True)

    if clicks > 50 and orders == 0:
        st.markdown(f"<div style='display: flex; padding: 0.4rem 0.8rem; border-bottom: 1px solid #f0f0f0;'><div style='width: 35%; font-weight: 500;'>🛒 Konversi</div><div style='width: 65%;'>{orders} order dari {clicks} klik <span class='badge-danger'>🔴 MASALAH</span><br><small>Klik banyak tapi 0 order → masalah produk</small></div></div>", unsafe_allow_html=True)
    elif orders > 0:
        cvr = orders / clicks * 100 if clicks > 0 else 0
        if cvr >= 2:
            st.markdown(f"<div style='display: flex; padding: 0.4rem 0.8rem; border-bottom: 1px solid #f0f0f0;'><div style='width: 35%; font-weight: 500;'>🛒 Konversi</div><div style='width: 65%;'>{orders} order dari {clicks} klik <span class='badge-success'>✅ BAGUS</span><br><small>CVR {cvr:.1f}% normal</small></div></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='display: flex; padding: 0.4rem 0.8rem; border-bottom: 1px solid #f0f0f0;'><div style='width: 35%; font-weight: 500;'>🛒 Konversi</div><div style='width: 65%;'>{orders} order dari {clicks} klik <span class='badge-warning'>🟡 RENDAH</span><br><small>CVR {cvr:.1f}% < 2%</small></div></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='display: flex; padding: 0.4rem 0.8rem; border-bottom: 1px solid #f0f0f0;'><div style='width: 35%; font-weight: 500;'>🛒 Konversi</div><div style='width: 65%;'>{orders} order dari {clicks} klik <span class='badge-info'>⏸️ TIDAK ADA</span><br><small>Belum ada order, evaluasi produk</small></div></div>", unsafe_allow_html=True)

    if cpc <= 3000:
        st.markdown(f"<div style='display: flex; padding: 0.4rem 0.8rem;'><div style='width: 35%; font-weight: 500;'>🖱️ CPC</div><div style='width: 65%;'>{format_rp(cpc)} <span class='badge-success'>✅ NORMAL</span><br><small>Biaya per klik efisien</small></div></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='display: flex; padding: 0.4rem 0.8rem;'><div style='width: 35%; font-weight: 500;'>🖱️ CPC</div><div style='width: 65%;'>{format_rp(cpc)} <span class='badge-warning'>⚠️ MAHAL</span><br><small>Perlu perbaiki relevansi</small></div></div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Rekomendasi
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.subheader("🎯 **Kesimpulan & Rekomendasi**")

    rekomendasi_budget = budget_set
    tindakan = ""
    prioritas = ""
    warna = ""

    if roas_aktual < roas_bep and roas_aktual > 0:
        tindakan = f"🔺 Naikkan target ROAS menjadi {roas_bep + 0.5:.1f} - {roas_bep + 1:.1f}"
        rekomendasi_budget = budget_set * 0.5
        prioritas = "🔴 PRIORITAS 1 - URGENT"
        warna = "danger"
    elif budget_terserap_persen < 70 and roas_aktual >= roas_bep:
        tindakan = f"🔻 Turunkan target ROAS 0.5 poin menjadi {target_roas - 0.5:.1f}"
        rekomendasi_budget = budget_set
        prioritas = "🟡 PRIORITAS 2 - OPTIMASI"
        warna = "warning"
    elif budget_terserap_persen >= 85 and roas_aktual >= roas_bep:
        tindakan = f"🚀 Naikkan budget 30% menjadi {format_rp(budget_set * 1.3)}"
        rekomendasi_budget = budget_set * 1.3
        prioritas = "🟢 PRIORITAS 3 - SCALE"
        warna = "success"
    elif clicks > 50 and orders == 0:
        tindakan = "🛠️ Perbaiki produk (harga, review, deskripsi) - JANGAN ubah setting iklan"
        rekomendasi_budget = budget_set
        prioritas = "🔴 PRIORITAS 1 - URGENT"
        warna = "danger"
    elif ctr < 2 and clicks > 0:
        tindakan = "🎨 Ganti visual iklan (foto utama / video hook 3 detik pertama)"
        rekomendasi_budget = budget_set
        prioritas = "🟡 PRIORITAS 2 - OPTIMASI"
        warna = "warning"
    else:
        tindakan = "✅ Pertahankan setting saat ini, pantau 3-5 hari"
        rekomendasi_budget = budget_set
        prioritas = "🟢 PRIORITAS 3 - PANTAU"
        warna = "info"

    bg_color = {"danger":"#fee2e2", "warning":"#fef3c7", "success":"#d1fae5", "info":"#dbeafe"}.get(warna, "#f0f0ff")
    border_color = {"danger":"#dc2626", "warning":"#f59e0b", "success":"#10b981", "info":"#3b82f6"}.get(warna, "#667eea")
    st.markdown(f"""
    <div style="background: {bg_color}; border-radius: 0.8rem; padding: 0.8rem; border-left: 4px solid {border_color}; margin: 0.5rem 0;">
        <h4 style="margin: 0 0 0.3rem 0;">{prioritas}</h4>
        <p style="margin: 0;"><strong>📌 Tindakan:</strong> {tindakan}</p>
        <p style="margin: 0.3rem 0 0 0;"><strong>💰 Rekomendasi Budget:</strong> {format_rp(rekomendasi_budget)}</p>
    </div>
    """, unsafe_allow_html=True)

# ==================== GENERATOR SEO & DESKRIPSI ====================
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.subheader("✨ **Generator SEO & Deskripsi Produk**")
st.markdown("Bikin judul dan deskripsi produk yang menarik biar CTR naik!")

# Cek limit generator demo
if st.session_state.get("demo_mode", False) and not can_do_demo_generator():
    st.warning(f"⚠️ **Demo terbatas maksimal {MAX_DEMO_GENERATOR} kali generate.** Beli premium untuk akses unlimited!")
    
    wa_button = f'''
    <a href="{WA_LINK}" target="_blank">
        <button style="background: linear-gradient(135deg, #25D366 0%, #128C7E 100%); color: white; border: none; padding: 0.6rem; border-radius: 0.5rem; font-weight: bold; width: 100%; cursor: pointer;">
            💬 Beli Premium Rp147rb via WhatsApp
        </button>
    </a>
    '''
    st.markdown(wa_button, unsafe_allow_html=True)

tab_gen1, tab_gen2, tab_gen3 = st.tabs(["📝 SEO Title Generator", "📄 Deskripsi Produk", "🎬 Hook Video TikTok"])

# ==================== TAB 1: SEO TITLE GENERATOR ====================
with tab_gen1:
    st.markdown("### 🎯 **Buat Judul Produk yang Bikin Klik**")
    
    col_title1, col_title2 = st.columns(2)
    with col_title1:
        produk_name = st.text_input("Nama Produk", placeholder="Contoh: Kaos Oversize Pria", key="seo_produk")
    with col_title2:
        keyword = st.text_input("Kata Kunci Utama (opsional)", placeholder="Contoh: nyaman, adem, premium", key="seo_keyword")
    
    if st.button("✨ Generate Judul SEO", key="btn_seo"):
        if st.session_state.get("demo_mode", False):
            if not can_do_demo_generator():
                st.warning("⚠️ Limit generate demo habis!")
                st.stop()
            increment_demo_generator()
        
        if produk_name:
            judul_list = [
                f"🔥 {produk_name} - Kualitas Premium Harga Terjangkau!",
                f"💯 {produk_name} BEST SELLER - Udah Terjual 1000+",
                f"✨ WAJIB PUNYA! {produk_name} Bikin Penampilan Makin Kece",
                f"🎯 {produk_name} - Dijamin Nyaman Dipakai Seharian",
                f"💎 {produk_name} PREMIUM QUALITY - Limited Stock!",
                f"🛒 {produk_name} - 50% OFF Hari Ini! Buruan",
                f"⭐ {produk_name} - Review 4.9/5, Cobain Sendiri!",
                f"📦 {produk_name} - FREE ONGKIR Se-Indonesia!",
                f"🏆 {produk_name} - Rekomendasi #1 di TikTok",
                f"💝 {produk_name} - Kado Terbaik untuk Orang Tersayang"
            ]
            if keyword:
                judul_list = [f"{j} | {keyword}" for j in judul_list]
            
            st.markdown("### 📋 **Judul Siap Pakai (Copy-Paste):**")
            for i, judul in enumerate(judul_list, 1):
                st.markdown(f"""
                <div style="background: #f8f9ff; padding: 0.5rem 1rem; border-radius: 0.5rem; margin: 0.3rem 0; border-left: 3px solid #667eea;">
                    <code>{i}. {judul}</code>
                </div>
                """, unsafe_allow_html=True)
            st.info("💡 **Tips:** Pilih judul yang paling sesuai dengan target pasar Anda!")
        else:
            st.warning("⚠️ Masukkan nama produk terlebih dahulu!")

# ==================== TAB 2: DESKRIPSI PRODUK ====================
with tab_gen2:
    st.markdown("### 📄 **Buat Deskripsi Produk yang Meyakinkan**")
    
    col_desc1, col_desc2 = st.columns(2)
    with col_desc1:
        produk_desc = st.text_input("Nama Produk", placeholder="Contoh: Kaos Oversize Pria", key="desc_produk")
        manfaat = st.text_area("Manfaat Produk (pisahkan dengan koma)", placeholder="Contoh: adem, nyaman, tidak panas, bahan tebal", key="manfaat")
    with col_desc2:
        spesifikasi = st.text_area("Spesifikasi (opsional)", placeholder="Contoh: Bahan Cotton Combed 30s, Size S-XXL, Tersedia 5 warna", key="spesifikasi")
        target_pasar = st.selectbox("Target Pasar", ["Pria", "Wanita", "Unisex", "Remaja", "Dewasa"], key="target")
    
    if st.button("✨ Generate Deskripsi", key="btn_desc"):
        if st.session_state.get("demo_mode", False):
            if not can_do_demo_generator():
                st.warning("⚠️ Limit generate demo habis!")
                st.stop()
            increment_demo_generator()
        
        if produk_desc:
            manfaat_list = [m.strip() for m in manfaat.split(",")] if manfaat else ["premium", "nyaman"]
            deskripsi = f"""
**✨ {produk_desc} - Kualitas Premium Harga Terjangkau!**

🔥 **Kenapa Harus Pilih {produk_desc}?**

✅ **Bahan Berkualitas** - Menggunakan material terbaik yang {' & '.join(manfaat_list[:3])}
✅ **Desain Modern** - Cocok untuk berbagai acara, dari santai sampai formal
✅ **Size Lengkap** - Tersedia dari S sampai XXL, cocok untuk semua postur tubuh
✅ **Garansi 100%** - Jika tidak sesuai, uang kembali!

📏 **Detail Produk:**
{spesifikasi if spesifikasi else '- Bahan: Premium Quality\n- Size: S, M, L, XL, XXL\n- Warna: Hitam, Putih, Navy, Abu, Coklat'}

🎯 **Cocok Untuk:**
- Daily casual
- Hangout sama teman
- OOTD keren
- {target_pasar} modern

💬 **Testimoni Pembeli:**
⭐ "Bahannya enak banget, gak panas! Recomended!" - Andi
⭐ "Pengiriman cepat, kualitas oke. Bakal repeat order!" - Budi
⭐ "Sesuai ekspektasi, bakal beli lagi buat kado." - Citra

🛒 **ORDER SEKARANG JUGA!**
Klik tombol "Beli" atau chat admin untuk konsultasi size.

🔥 **Promo Terbatas!** Free ongkir + Diskon 10% untuk 50 pembeli pertama!

*Stok terbatas, jangan sampai kehabisan!*
"""
            st.markdown("### 📋 **Deskripsi Siap Pakai (Copy-Paste):**")
            st.code(deskripsi, language="markdown")
            st.info("💡 **Tips:** Sesuaikan dengan brand voice Anda! Jangan lupa tambahkan emoji yang relevan.")
        else:
            st.warning("⚠️ Masukkan nama produk terlebih dahulu!")

# ==================== TAB 3: HOOK VIDEO TIKTOK ====================
with tab_gen3:
    st.markdown("### 🎬 **Buat Hook Video TikTok (3 Detik Pertama)**")
    st.markdown("Hook yang menarik = CTR tinggi! Ini kunci sukses iklan TikTok.")
    
    produk_hook = st.text_input("Nama Produk", placeholder="Contoh: Kaos Oversize", key="hook_produk")
    hook_style = st.selectbox("Gaya Hook", ["Problem Solver", "Diskon/Promo", "Bukti Sosial", "Curiosity", "Emosional"], key="hook_style")
    
    if st.button("✨ Generate Hook Video", key="btn_hook"):
        if st.session_state.get("demo_mode", False):
            if not can_do_demo_generator():
                st.warning("⚠️ Limit generate demo habis!")
                st.stop()
            increment_demo_generator()
        
        if produk_hook:
            if hook_style == "Problem Solver":
                hook_list = [
                    f"😫 Capek cari {produk_hook} yang nyaman? STOP!",
                    f"❌ Jangan beli {produk_hook} sebelum lihat video ini!",
                    f"🤯 Rahasia {produk_hook} yang gak pernah kamu tahu!",
                    f"⚠️ 5 kesalahan fatal pas beli {produk_hook}!",
                    f"💡 Cara pilih {produk_hook} yang bikin kamu auto percaya diri!"
                ]
            elif hook_style == "Diskon/Promo":
                hook_list = [
                    f"🔥 DISKON 50% {produk_hook} cuma hari ini!",
                    f"🎉 FREE ONGKIR {produk_hook} se-Indonesia!",
                    f"💰 Harga {produk_hook} turun drastis! Buruan!",
                    f"🎁 Beli 1 gratis 1 untuk {produk_hook} terbatas!",
                    f"⚡ Stok {produk_hook} tinggal 10! Cepat checkout!"
                ]
            elif hook_style == "Bukti Sosial":
                hook_list = [
                    f"🏆 {produk_hook} best seller dengan 5000+ review!",
                    f"⭐ 4.9/5 rating untuk {produk_hook}! Cobain sendiri!",
                    f"📦 1000+ orang udah beli {produk_hook} minggu ini!",
                    f"💬 Viral! {produk_hook} lagi di mana-mana!",
                    f"👑 Rekomendasi #1 untuk {produk_hook} versi seleb TikTok!"
                ]
            elif hook_style == "Curiosity":
                hook_list = [
                    f"🤔 Kenapa semua orang pake {produk_hook}?",
                    f"😱 Gak nyangka {produk_hook} sekeren ini!",
                    f"🫣 Psst... rahasia {produk_hook} akhirnya kebongkar!",
                    f"❓ Apa yang terjadi kalau kamu pake {produk_hook}?",
                    f"👀 Wajib lihat! {produk_hook} versi terbaru!"
                ]
            else:
                hook_list = [
                    f"🥺 Aku menangis lihat {produk_hook} ini!",
                    f"😍 Cinta pertama sama {produk_hook}!",
                    f"💗 {produk_hook} yang bikin aku percaya diri!",
                    f"🤗 Pelukan terbaik dari {produk_hook}!",
                    f"✨ Hidup berubah setelah pake {produk_hook}!"
                ]
            
            st.markdown("### 🎥 **Hook Video Siap Pakai (3 Detik Pertama):**")
            for i, hook in enumerate(hook_list, 1):
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%); padding: 0.6rem 1rem; border-radius: 0.5rem; margin: 0.4rem 0;">
                    <code style="font-size: 1rem;">🎬 {i}. {hook}</code>
                </div>
                """, unsafe_allow_html=True)
            st.info("💡 **Tips Hook Video TikTok:** Gunakan teks besar & warna mencolok di 3 detik pertama + ekspresi wajah yang overacting!")
        else:
            st.warning("⚠️ Masukkan nama produk terlebih dahulu!")

# ==================== TIPS CEPAT ====================
with st.expander("💡 **Tips Cepat Baca Data Iklan**"):
    st.markdown("""
    | Kondisi | Arti | Solusi |
    |---------|------|--------|
    | CTR < 2% | Visual kurang menarik | Ganti foto/video hook |
    | Budget terserap <70% | Target ROAS terlalu ketat | Turunkan target ROAS 0.5 |
    | ROAS < BEP | Iklan rugi | Naikkan target ROAS |
    | Klik >50, order=0 | Produk tidak meyakinkan | Perbaiki harga/review/deskripsi |
    | Budget habis & ROAS > BEP | Performa bagus | Scale naikkan budget 30% |
    """)

# ==================== FOOTER ====================
st.markdown("---")
st.markdown(f"""
<div class="footer">
    <p>🩺 <strong>DOCTOR ADS SHOPEE & TIKTOK PREMIUM</strong> | Framework GMV Max</p>
    <p>© 2024 Arkidigital - Solusi Digital Marketing Terbaik untuk Bisnis Anda</p>
    {'<p>🎁 Mode Demo - Beli premium untuk akses penuh tanpa batasan!</p>' if st.session_state.get("demo_mode", False) else ''}
</div>
""", unsafe_allow_html=True)
