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
ADMIN_USERNAME = "Arkidigital"
ADMIN_PASSWORD = "Arkidigital2026"

# LINK CHECKOUT PAGE
CHECKOUT_LINK = "https://muhammad-masruri.myscalev.com/checkout-pageku"

DEMO_DURATION_MINUTES = 5
MAX_DEMO_ANALYSIS = 2
MAX_DEMO_GENERATOR = 2

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
        st.markdown(f'<a href="{CHECKOUT_LINK}" target="_blank"><button style="background:#25D366; color:white; padding:10px; border-radius:30px; border:none; width:100%;">💎 Beli Premium</button></a>', unsafe_allow_html=True)
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

# ==================== LOGIN + DEMO ====================
def login_or_demo():
    st.markdown("""
    <div style="text-align:center; padding:2rem;">
        <h1>🩺 DOCTOR ADS PREMIUM</h1>
        <p>Analisa Iklan TikTok & Shopee → Rekomendasi Perbaikan Instan</p>
        <p style="color:#00E5A0;">Hanya Rp147rb (sekali bayar) + Konsultasi GRATIS!</p>
    </div>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        with st.form("login"):
            st.markdown("### 🔐 Login Premium")
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.form_submit_button("🔓 Login"):
                if u == ADMIN_USERNAME and p == ADMIN_PASSWORD:
                    st.session_state["authenticated"] = True
                    st.session_state["demo_mode"] = False
                    st.rerun()
                else:
                    st.error("Salah!")
    with col2:
        st.markdown("### 🎁 Coba Demo 5 Menit")
        st.markdown(f"✅ Maks {MAX_DEMO_ANALYSIS} analisis, {MAX_DEMO_GENERATOR} generate\n✅ 1x per 24 jam")
        if st.button("🚀 Mulai Demo Gratis"):
            start_demo()
    st.markdown(f'<a href="{CHECKOUT_LINK}" target="_blank" style="display:block; background:#25D366; color:white; text-align:center; padding:12px; border-radius:40px; text-decoration:none; margin-top:20px;">💎 Beli Premium Sekarang</a>', unsafe_allow_html=True)
    return False

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
    login_or_demo()
    st.stop()

if is_demo_expired():
    st.warning("⏰ Demo habis! Beli premium untuk akses penuh.")
    st.markdown(f'<a href="{CHECKOUT_LINK}" target="_blank" style="display:block; background:#00E5A0; color:#1a1a2e; text-align:center; padding:12px; border-radius:40px; text-decoration:none;">💎 Beli Premium Rp147rb</a>', unsafe_allow_html=True)
    st.stop()

# ==================== SIDEBAR ====================
with st.sidebar:
    if is_premium():
        st.markdown("### 🩺 **Premium Member**")
    else:
        rem = get_demo_remaining()
        st.markdown(f"### 🎁 Demo Mode: {rem//60}:{rem%60:02d} sisa")
        st.markdown(f"Analisis: {st.session_state.get('demo_analysis_count',0)}/{MAX_DEMO_ANALYSIS} | Generate: {st.session_state.get('demo_generator_count',0)}/{MAX_DEMO_GENERATOR}")
    
    st.markdown("## 📦 **Database Produk**")
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
                roas_bep = hj / laba if laba > 0 else 999
                save_product({"nama": nama, "harga_jual": hj, "modal": modal, "admin_persen": admin, "laba_kotor": laba, "roas_bep": roas_bep})
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
        st.info("🎁 Mode Demo: input manual")
        harga_jual = st.number_input("Harga Jual", min_value=1000, value=100000, step=5000, key="hj_demo")
        modal = st.number_input("Modal", min_value=500, value=60000, step=5000, key="modal_demo")
        admin_persen = st.slider("Admin %", 5, 30, 20, key="admin_demo")
        admin_nom = harga_jual * admin_persen/100
        laba_kotor = harga_jual - modal - admin_nom
        roas_bep = harga_jual / laba_kotor if laba_kotor > 0 else 999
        st.caption("💎 Beli premium untuk simpan produk")
    
    # ==================== HITUNG ROAS BEP (KALKULATOR) ====================
    st.markdown("---")
    st.markdown("## 🎯 **Hitung ROAS BEP**")
    
    with st.expander("📊 Kalkulator ROAS BEP", expanded=True):
        col_bep1, col_bep2 = st.columns(2)
        with col_bep1:
            hj_bep = st.number_input("💰 Harga Jual (Rp)", min_value=1000, value=100000, step=5000, key="bep_hj")
            modal_bep = st.number_input("🏭 Modal / HPP (Rp)", min_value=500, value=60000, step=5000, key="bep_modal")
        with col_bep2:
            admin_bep = st.slider("🏪 Admin Marketplace (%)", 5, 30, 20, key="bep_admin")
            target_profit_bep = st.number_input("🎯 Target Profit (Rp)", min_value=0, value=0, step=5000, key="bep_profit")
        
        admin_nom_bep = hj_bep * admin_bep / 100
        laba_kotor_bep = hj_bep - modal_bep - admin_nom_bep - target_profit_bep
        roas_bep_hasil = hj_bep / laba_kotor_bep if laba_kotor_bep > 0 else 999
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); padding: 1rem; border-radius: 1rem; margin-top: 0.5rem;">
            <p style="color: #888; margin: 0; font-size: 0.7rem;">📊 HASIL PERHITUNGAN</p>
            <p style="color: white; margin: 0.2rem 0;">Harga Jual: <strong style="color: #00E5A0;">Rp{hj_bep:,.0f}</strong></p>
            <p style="color: white; margin: 0.2rem 0;">Modal: Rp{modal_bep:,.0f}</p>
            <p style="color: white; margin: 0.2rem 0;">Admin {admin_bep}%: Rp{admin_nom_bep:,.0f}</p>
            <p style="color: white; margin: 0.2rem 0;">Target Profit: Rp{target_profit_bep:,.0f}</p>
            <hr style="margin: 0.5rem 0; border-color: #333;">
            <p style="color: white; margin: 0.2rem 0;"><strong>💎 Laba Kotor: Rp{laba_kotor_bep:,.0f}</strong></p>
            <p style="color: #00E5A0; margin: 0.2rem 0; font-size: 1.2rem; font-weight: bold;">🎯 ROAS BEP = {roas_bep_hasil:.1f}x</p>
            <p style="color: #888; margin: 0.3rem 0 0 0; font-size: 0.65rem;">Artinya: Setiap Rp1 iklan harus menghasilkan minimal Rp{roas_bep_hasil:.1f} penjualan agar tidak rugi.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with st.expander("📋 **Cek Kelayakan Produk**"):
        pernah = st.radio("Produk pernah laku?", ["Ya","Tidak"], horizontal=True, key="pernah_laku")
        if pernah == "Tidak":
            st.error("❌ Jangan iklan dulu!")
        else:
            terjual = st.number_input("Terjual/bulan", 0, 100000, 500, key="terjual")
            if terjual < 1000:
                st.warning("⚠️ Kurang kuat, tes kecil dulu.")
            harga_komp = st.number_input("Harga kompetitor", min_value=1000, value=90000, step=5000, key="harga_komp")
            if harga_jual > harga_komp * 1.2:
                st.warning("⚠️ Harga terlalu tinggi.")
            if laba_kotor <= 0:
                st.error("❌ Margin habis, ganti produk.")
            elif laba_kotor < 5000:
                st.warning("⚠️ Margin tipis, rawan boncos.")
            else:
                st.success("✅ Produk layak iklan!")

# ==================== DASHBOARD UTAMA ====================
st.markdown("""
<div style="background: linear-gradient(135deg, #5B2C8F, #4a1d7a); padding: 1rem; border-radius: 1rem; color: white; margin-bottom: 1rem;">
    <h1 style="margin:0">🩺 DOCTOR ADS PREMIUM</h1>
    <p>Analisa Iklan TikTok & Shopee → Rekomendasi Perbaikan Instan</p>
</div>
""", unsafe_allow_html=True)

# ==================== INPUT DATA IKLAN ====================
st.markdown("### 📝 Input Data Iklan")

if not is_premium() and not can_do_demo_analysis():
    st.warning(f"⚠️ Demo terbatas {MAX_DEMO_ANALYSIS}x analisis. Beli premium untuk unlimited!")
    st.markdown(f'<a href="{CHECKOUT_LINK}" target="_blank" style="display:block; background:#00E5A0; color:#1a1a2e; text-align:center; padding:12px; border-radius:40px; text-decoration:none;">💎 Beli Premium</a>', unsafe_allow_html=True)
    st.stop()

colA, colB = st.columns(2)
with colA:
    impressions = st.number_input("👁️ Impressions", min_value=0, value=10000, step=1000, key="impressions")
    clicks = st.number_input("🖱️ Clicks", min_value=0, value=300, step=50, key="clicks")
    budget_set = st.number_input("💵 Budget Setting (Rp)", min_value=0, value=100000, step=10000, key="budget_set")
with colB:
    budget_spent = st.number_input("💸 Budget Terserap (Rp)", min_value=0, value=90000, step=5000, key="budget_spent")
    target_roas = st.number_input("🎯 Target ROAS", min_value=1.0, value=6.0, step=0.5, key="target_roas")
    sales = st.number_input("💰 Omset (Rp)", min_value=0, value=600000, step=50000, key="sales")
    orders = st.number_input("📦 Jumlah Order", min_value=0, value=6, step=1, key="orders")
    platform = st.selectbox("📱 Platform", ["Shopee", "TikTok"], key="platform")

analize = st.button("🔍 Analisis Iklan", use_container_width=True, key="analize_btn")

# ==================== ANALISIS & REKOMENDASI ====================
if analize:
    if not is_premium():
        inc_demo_analysis()
    
    # Hitung metrik
    if clicks > 0 and impressions > 0:
        ctr = (clicks / impressions * 100)
        cpc = budget_spent / clicks if clicks > 0 else 0
        roas_aktual = sales / budget_spent if budget_spent > 0 else 0
        budget_terserap_persen = (budget_spent / budget_set * 100) if budget_set > 0 else 0
        profit_estimasi = (laba_kotor * orders) - budget_spent if orders > 0 else -budget_spent
    else:
        ctr = 0
        cpc = 0
        roas_aktual = 0
        budget_terserap_persen = 0
        profit_estimasi = -budget_spent
    
    def format_rp(angka):
        if angka >= 1_000_000:
            return f"Rp{angka/1_000_000:.1f}JT"
        elif angka >= 1000:
            return f"Rp{angka/1000:.0f}RB"
        return f"Rp{angka:,.0f}"
    
    # Metric cards
    st.markdown("### 📊 Dashboard Performa")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown(f"<div style='background:#1a1a2e; padding:1rem; border-radius:1rem; border-left:4px solid #00E5A0;'><p style='color:#888; margin:0'>Total Belanja</p><h2 style='color:white; margin:0'>{format_rp(budget_spent)}</h2></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div style='background:#1a1a2e; padding:1rem; border-radius:1rem; border-left:4px solid #00E5A0;'><p style='color:#888; margin:0'>Total Omset</p><h2 style='color:white; margin:0'>{format_rp(sales)}</h2></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div style='background:#1a1a2e; padding:1rem; border-radius:1rem; border-left:4px solid #00E5A0;'><p style='color:#888; margin:0'>ROAS Aktual</p><h2 style='color:white; margin:0'>{roas_aktual:.1f}x</h2></div>", unsafe_allow_html=True)
    with col4:
        warna_profit = "#00E5A0" if profit_estimasi > 0 else "#ff6b6b"
        st.markdown(f"<div style='background:#1a1a2e; padding:1rem; border-radius:1rem; border-left:4px solid #00E5A0;'><p style='color:#888; margin:0'>Estimasi Profit</p><h2 style='color:{warna_profit}; margin:0'>{format_rp(profit_estimasi)}</h2></div>", unsafe_allow_html=True)
    with col5:
        status_bep = "✅ Aman" if roas_aktual >= roas_bep else "⚠️ Rugi"
        st.markdown(f"<div style='background:#1a1a2e; padding:1rem; border-radius:1rem; border-left:4px solid #00E5A0;'><p style='color:#888; margin:0'>ROAS BEP</p><h2 style='color:white; margin:0'>{roas_bep:.1f}x</h2><p style='color:#888; margin:0; font-size:0.7rem;'>{status_bep}</p></div>", unsafe_allow_html=True)
    
    # Rekomendasi
    st.markdown("---")
    st.subheader("🎯 **Kesimpulan & Rekomendasi**")
    
    rekomendasi_tindakan = ""
    rekomendasi_roas = target_roas
    rekomendasi_budget = budget_set
    prioritas = ""
    warna = "info"
    
    # ATURAN 1: KLIK BANYAK, BUDGET HABIS, ORDER 0 → STOP IKLAN
    if clicks > 50 and budget_terserap_persen >= 80 and orders == 0:
        rekomendasi_tindakan = f"""
        🔴 **PRIORITAS 1 - HENTIKAN IKLAN SEGERA!**  
        📊 Data: {clicks} klik, budget terserap {budget_terserap_persen:.0f}%, tapi 0 order.  
        **Penyebab:** Produk belum layak iklan.  
        **Yang harus dilakukan:**  
        1. Cek harga produk — apakah lebih murah atau setara kompetitor?  
        2. Tambah review & rating (minimal 10-20 review positif)  
        3. Perbaiki deskripsi — fokus ke MANFAAT  
        4. Pastikan stok aman dan produk dibutuhkan pasar  
        **Setelah produk siap, restart iklan dengan budget kecil (Rp50-100rb/hari).**
        """
        prioritas = "🔴 PRIORITAS 1 - URGENT (Stop Iklan)"
        warna = "danger"
    
    # ATURAN 2: SIAP SCALE
    elif budget_terserap_persen >= 85 and roas_aktual >= roas_bep * 1.2:
        new_budget = budget_set * 1.3
        rekomendasi_tindakan = f"""
        🟢 **PRIORITAS 4 - SIAP SCALE**  
        ROAS {roas_aktual:.1f}x > BEP {roas_bep:.1f}x (untung)  
        Budget terserap {budget_terserap_persen:.0f}% (hampir habis)  
        ✅ Naikkan **BUDGET 30%** menjadi Rp{new_budget:,.0f}  
        ✅ **PERTAHANKAN** target ROAS di {target_roas:.1f}x  
        ⏰ Tunggu **3 hari** tanpa perubahan apapun.
        """
        rekomendasi_budget = new_budget
        prioritas = "🟢 PRIORITAS 4 - SCALE (Naik Budget 30%)"
        warna = "success"
    
    # ATURAN 3: ROAS PROFIT, BUDGET BELUM HABIS
    elif roas_aktual >= roas_bep and budget_terserap_persen < 85:
        new_target = target_roas - 0.5
        rekomendasi_tindakan = f"""
        🟡 **PRIORITAS 2 - OPTIMASI**  
        ROAS {roas_aktual:.1f}x ≥ BEP {roas_bep:.1f}x (untung)  
        Budget terserap {budget_terserap_persen:.0
