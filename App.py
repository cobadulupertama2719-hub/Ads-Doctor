import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import hashlib
import json
import plotly.graph_objects as go

# ==================== KONFIGURASI ====================
ADMIN_USERNAME = "arkidigital"
ADMIN_PASSWORD = "Arkidigital2026"
WA_NUMBER = "6288228878258"
WA_LINK = f"https://wa.me/{WA_NUMBER}?text=Halo%20Arkidigital%2C%20saya%20mau%20beli%20Doctor%20Ads%20Premium%20Rp147rb"

DEMO_DURATION_MINUTES = 5
MAX_DEMO_ANALYSIS = 2
MAX_DEMO_GENERATOR = 2

# ==================== FUNGSI DEMO ====================
def get_device_fingerprint():
    user_agent = st.context.headers.get('User-Agent', 'unknown')
    ip = st.context.headers.get('X-Forwarded-For', 'unknown')
    return hashlib.md5(f"{user_agent}_{ip}".encode()).hexdigest()

def load_demo_history():
    if "demo_history" not in st.session_state:
        st.session_state.demo_history = {}
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
        st.error("⚠️ Anda sudah pernah mencoba demo! Demo hanya 1x per 24 jam.")
        st.markdown(f'<a href="{WA_LINK}" target="_blank"><button style="background:#25D366; color:white; padding:10px; border-radius:30px; border:none; width:100%;">💬 Beli Premium via WA</button></a>', unsafe_allow_html=True)
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
    st.markdown(f'<a href="{WA_LINK}" target="_blank" style="display:block; background:#25D366; color:white; text-align:center; padding:12px; border-radius:40px; text-decoration:none; margin-top:20px;">💬 Chat Admin via WhatsApp</a>', unsafe_allow_html=True)
    return False

# ==================== DATABASE PRODUK ====================
def load_products():
    if "products" not in st.session_state:
        st.session_state.products = []
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

# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
    * { margin:0; padding:0; box-sizing:border-box; }
    body { background: #5B2C8F; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto; }
    .main-header { background: linear-gradient(135deg, #5B2C8F, #4a1d7a); padding: 1rem; border-radius: 1rem; color: white; margin-bottom: 1rem; }
    .metric-card { background: #1a1a2e; padding: 1rem; border-radius: 1rem; border-left: 4px solid #00E5A0; }
    .btn-primary { background: #00E5A0; color: #1a1a2e; padding: 0.7rem; border-radius: 2rem; text-align: center; font-weight: bold; text-decoration: none; display: block; margin: 0.5rem 0; }
    .btn-secondary { background: rgba(255,255,255,0.1); color: white; padding: 0.7rem; border-radius: 2rem; text-align: center; text-decoration: none; display: block; margin: 0.5rem 0; }
    .premium-badge { background: #00E5A0; color: #1a1a2e; padding: 0.2rem 0.6rem; border-radius: 2rem; font-size: 0.7rem; }
    .demo-warning { background: #fef3c7; color: #d97706; padding: 0.5rem; border-radius: 0.5rem; margin-bottom: 1rem; }
</style>
""", unsafe_allow_html=True)

# ==================== PAGE CONFIG ====================
st.set_page_config(page_title="Doctor Ads Premium", page_icon="🩺", layout="wide")

# ==================== CEK AKSES ====================
if not is_premium() and not st.session_state.get("demo_mode", False):
    login_or_demo()
    st.stop()

if is_demo_expired():
    st.warning("⏰ Demo habis! Beli premium untuk akses penuh.")
    st.markdown(f'<a href="{WA_LINK}" target="_blank" class="btn-primary">💎 Beli Premium Rp147rb</a>', unsafe_allow_html=True)
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
            nama = st.text_input("Nama Produk")
            hj = st.number_input("Harga Jual", min_value=1000, value=100000, step=5000)
            modal = st.number_input("Modal", min_value=500, value=60000, step=5000)
            admin = st.slider("Admin %", 5, 30, 20)
            if st.button("💾 Simpan") and nama:
                admin_nom = hj * admin/100
                laba = hj - modal - admin_nom
                roas_bep = hj / laba if laba > 0 else 999
                save_product({"nama": nama, "harga_jual": hj, "modal": modal, "admin_persen": admin, "laba_kotor": laba, "roas_bep": roas_bep})
                st.success("Tersimpan")
        if products:
            pilih = st.selectbox("Pilih produk", ["--"] + [p["nama"] for p in products])
            if pilih != "--":
                prod = next(p for p in products if p["nama"] == pilih)
                harga_jual = prod["harga_jual"]
                modal = prod["modal"]
                admin_persen = prod["admin_persen"]
                laba_kotor = prod["laba_kotor"]
                roas_bep = prod["roas_bep"]
                st.info(f"ROAS BEP: {roas_bep:.1f}x | Laba: Rp{laba_kotor:,.0f}")
                if st.button("🗑️ Hapus"):
                    delete_product(pilih)
                    st.rerun()
            else:
                harga_jual = st.number_input("Harga Jual", min_value=1000, value=100000, step=5000, key="manual_hj")
                modal = st.number_input("Modal", min_value=500, value=60000, step=5000, key="manual_modal")
                admin_persen = st.slider("Admin %", 5, 30, 20, key="manual_admin")
                admin_nom = harga_jual * admin_persen/100
                laba_kotor = harga_jual - modal - admin_nom
                roas_bep = harga_jual / laba_kotor if laba_kotor > 0 else 999
        else:
            harga_jual = st.number_input("Harga Jual", min_value=1000, value=100000, step=5000)
            modal = st.number_input("Modal", min_value=500, value=60000, step=5000)
            admin_persen = st.slider("Admin %", 5, 30, 20)
            admin_nom = harga_jual * admin_persen/100
            laba_kotor = harga_jual - modal - admin_nom
            roas_bep = harga_jual / laba_kotor if laba_kotor > 0 else 999
    else:
        st.info("🎁 Mode Demo: input manual")
        harga_jual = st.number_input("Harga Jual", min_value=1000, value=100000, step=5000)
        modal = st.number_input("Modal", min_value=500, value=60000, step=5000)
        admin_persen = st.slider("Admin %", 5, 30, 20)
        admin_nom = harga_jual * admin_persen/100
        laba_kotor = harga_jual - modal - admin_nom
        roas_bep = harga_jual / laba_kotor if laba_kotor > 0 else 999
        st.caption("💎 Beli premium untuk simpan produk")
    
    # Cek kelayakan produk (flowchart)
    with st.expander("📋 **Cek Kelayakan Produk**"):
        pernah = st.radio("Produk pernah laku?", ["Ya","Tidak"], horizontal=True)
        if pernah == "Tidak":
            st.error("❌ Jangan iklan dulu! Risiko tinggi.")
        else:
            terjual = st.number_input("Terjual/bulan", 0, 100000, 500)
            if terjual < 1000:
                st.warning("⚠️ Kurang kuat, tes kecil dulu.")
            harga_komp = st.number_input("Harga kompetitor", min_value=1000, value=90000, step=5000)
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

# Metric cards (akan diisi setelah analisis)
st.markdown("### 📊 Dashboard Performa")
col1, col2, col3, col4 = st.columns(4)
for c in [col1, col2, col3, col4]:
    c.markdown("<div class='metric-card'><p style='color:#888; margin:0'>-</p><h2 style='color:white; margin:0'>0</h2></div>", unsafe_allow_html=True)

# ==================== INPUT DATA IKLAN ====================
st.markdown("---")
st.markdown("### 📝 Input Data Iklan")

# Cek limit analisis demo
if not is_premium() and not can_do_demo_analysis():
    st.warning(f"⚠️ Demo terbatas {MAX_DEMO_ANALYSIS}x analisis. Beli premium untuk unlimited!")
    st.markdown(f'<a href="{WA_LINK}" target="_blank" class="btn-primary">💎 Beli Premium</a>', unsafe_allow_html=True)
    st.stop()

colA, colB = st.columns(2)
with colA:
    impressions = st.number_input("👁️ Impressions", min_value=0, value=10000, step=1000)
    clicks = st.number_input("🖱️ Clicks", min_value=0, value=300, step=50)
    budget_set = st.number_input("💵 Budget Setting (Rp)", min_value=0, value=100000, step=10000)
with colB:
    budget_spent = st.number_input("💸 Budget Terserap (Rp)", min_value=0, value=90000, step=5000)
    target_roas = st.number_input("🎯 Target ROAS", min_value=1.0, value=6.0, step=0.5)
    sales = st.number_input("💰 Omset (Rp)", min_value=0, value=600000, step=50000)
    orders = st.number_input("📦 Jumlah Order", min_value=0, value=6, step=1)
    platform = st.selectbox("📱 Platform", ["Shopee", "TikTok"])

analize = st.button("🔍 Analisis Iklan", use_container_width=True)

# ==================== ANALISIS ====================
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
        status_profit = "UNTUNG" if profit_estimasi > 0 else "RUGI"
    else:
        ctr = 0; cpc = 0; roas_aktual = 0; budget_terserap_persen = 0; profit_estimasi = -budget_spent; status_profit = "RUGI"
    
    def format_rp(angka):
        if angka >= 1_000_000:
            return f"Rp{angka/1_000_000:.1f}JT"
        elif angka >= 1000:
            return f"Rp{angka/1000:.0f}RB"
        return f"Rp{angka:,.0f}"
    
    # Update metric cards dengan data real
    st.markdown("### 📊 Dashboard Performa")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"<div class='metric-card'><p style='color:#888; margin:0'>Total Belanja</p><h2 style='color:white; margin:0'>{format_rp(budget_spent)}</h2></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-card'><p style='color:#888; margin:0'>Total Omset</p><h2 style='color:white; margin:0'>{format_rp(sales)}</h2></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='metric-card'><p style='color:#888; margin:0'>ROAS Aktual</p><h2 style='color:white; margin:0'>{roas_aktual:.1f}x</h2></div>", unsafe_allow_html=True)
    with col4:
        warna_profit = "#00E5A0" if profit_estimasi > 0 else "#ff6b6b"
        st.markdown(f"<div class='metric-card'><p style='color:#888; margin:0'>Estimasi Profit</p><h2 style='color:{warna_profit}; margin:0'>{format_rp(profit_estimasi)}</h2></div>", unsafe_allow_html=True)
    
    # ==================== REKOMENDASI DECISION TREE ====================
    st.markdown("---")
    st.subheader("🎯 Kesimpulan & Rekomendasi")
    
    rekom_txt = ""
    rekom_roas = target_roas
    rekom_budget = budget_set
    prioritas = ""
    warna = "info"
    
    # Aturan 3: klik >50, budget terserap >80%, order=0 -> stop iklan
    if clicks > 50 and budget_terserap_persen >= 80 and orders == 0:
        rekom_txt = f"""
        🔴 **PRIORITAS 1 - HENTIKAN IKLAN!**  
        Data: {clicks} klik, budget terserap {budget_terserap_persen:.0f}%, 0 order.  
        **Produk belum layak iklan.**  
        **Langkah:**  
        1. Perbaiki produk (harga, review, deskripsi)  
        2. Setelah siap, restart iklan dengan budget kecil (Rp50-100rb)  
        **JANGAN lanjutkan iklan sebelum produk siap!**  
        """
        prioritas = "🔴 PRIORITAS 1 - URGENT (Stop Iklan)"
        warna = "danger"
    
    # Scale hanya naikkan budget, ROAS tetap
    elif budget_terserap_persen >= 85 and roas_aktual >= roas_bep * 1.2:
        new_budget = budget_set * 1.3
        rekom_txt = f"""
        🟢 **PRIORITAS 4 - SIAP SCALE**  
        ROAS {roas_aktual:.1f}x > BEP {roas_bep:.1f}x (untung)  
        Budget terserap {budget_terserap_persen:.0f}% (hampir habis)  
        ✅ Naikkan **BUDGET 30%** menjadi Rp{new_budget:,.0f}  
        ✅ **PERTAHANKAN** target ROAS di {target_roas:.1f}x  
        ⏰ Tunggu **3 hari** tanpa perubahan.  
        """
        rekom_budget = new_budget
        prioritas = "🟢 PRIORITAS 4 - SCALE (Naik Budget)"
        warna = "success"
    
    # ROAS profit, budget belum habis -> turunkan ROAS
    elif roas_aktual >= roas_bep and budget_terserap_persen < 85:
        new_target = target_roas - 0.5
        rekom_txt = f"""
        🟡 **PRIORITAS 2 - OPTIMASI (Turunkan ROAS)**  
        ROAS {roas_aktual:.1f}x ≥ BEP {roas_bep:.1f}x  
        Budget terserap {budget_terserap_persen:.0f}% (masih sisa)  
        ✅ Turunkan target ROAS **0.5 poin** menjadi {new_target:.1f}x  
        ✅ **JANGAN UBAH BUDGET** (Rp{budget_set:,.0f})  
        ⏰ Tunggu **3 hari** tanpa perubahan.  
        """
        rekom_roas = new_target
        prioritas = "🟡 PRIORITAS 2 - OPTIMASI (Turun ROAS)"
        warna = "warning"
    
    # Iklan rugi -> naikkan ROAS
    elif roas_aktual < roas_bep and roas_aktual > 0:
        new_target = roas_bep + 0.5
        rekom_txt = f"""
        🔴 **PRIORITAS 3 - IKLAN RUGI**  
        ROAS {roas_aktual:.1f}x < BEP {roas_bep:.1f}x  
        ✅ Naikkan target ROAS **0.5 poin** menjadi {new_target:.1f}x  
        ✅ **JANGAN UBAH BUDGET** (Rp{budget_set:,.0f})  
        ⏰ Tunggu **3 hari** tanpa perubahan.  
        Jika masih rugi, pertimbangkan stop iklan sementara.
        """
        rekom_roas = new_target
        prioritas = "🔴 PRIORITAS 3 - URGENT (Naik ROAS)"
        warna = "danger"
    
    # Performa sehat
    else:
        rekom_txt = f"""
        ✅ **PERFORMA SEHAT**  
        ROAS {roas_aktual:.1f}x ≥ BEP {roas_bep:.1f}x  
        Budget terserap {budget_terserap_persen:.0f}%  
        Pertahankan setting saat ini.  
        Pantau 3-5 hari. Jika konsisten dan budget habis, scale naikkan budget 30%.
        """
        prioritas = "🟢 PRIORITAS 5 - PANTAU"
        warna = "info"
    
    # Tambahan jika CTR rendah
    if ctr < 2 and clicks > 0 and "Stop Iklan" not in rekom_txt:
        rekom_txt += f"\n\n---\n📸 **CTR Rendah** ({ctr:.1f}% < 2%)\nSolusi: Ganti visual (foto/video hook). Buat 3 variasi kreatif baru."
    
    bg = {"danger":"#fee2e2", "warning":"#fef3c7", "success":"#d1fae5", "info":"#dbeafe"}.get(warna, "#f0f0ff")
    border = {"danger":"#dc2626", "warning":"#f59e0b", "success":"#10b981", "info":"#3b82f6"}.get(warna, "#667eea")
    st.markdown(f"""
    <div style="background:{bg}; border-radius:1rem; padding:1rem; border-left:5px solid {border}; margin:1rem 0;">
        <h4 style="margin:0 0 0.5rem 0;">{prioritas}</h4>
        <div style="color:#333;">{rekom_txt.replace(chr(10), '<br>')}</div>
        <hr>
        <p><strong>💰 Budget rekomendasi:</strong> {format_rp(rekom_budget)} &nbsp;|&nbsp; <strong>🎯 Target ROAS rekomendasi:</strong> {rekom_roas:.1f}x</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Grafik sederhana (placeholder)
    st.markdown("---")
    st.subheader("📈 Tren Performa (Line Chart)")
    st.info("Data akan muncul setelah beberapa kali analisis. Untuk demo, hanya preview.")
    # Simple line chart demo (opsional)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[1,2,3], y=[roas_aktual*0.8, roas_aktual, roas_aktual*1.1], mode='lines+markers', name='ROAS'))
    fig.update_layout(height=300, margin=dict(l=0,r=0,t=30,b=0), plot_bgcolor='#1a1a2e', paper_bgcolor='#1a1a2e', font_color='white')
    st.plotly_chart(fig, use_container_width=True)

# ==================== GENERATOR PREMIUM (dengan popup untuk demo) ====================
st.markdown("---")
st.subheader("✨ Generator SEO & Deskripsi Produk")
tab1, tab2, tab3 = st.tabs(["📝 SEO Title", "📄 Deskripsi", "🎬 Hook TikTok"])

# Fungsi untuk mengecek akses generator (premium atau demo belum mencapai limit)
def generator_access():
    if is_premium():
        return True
    if can_do_demo_generator():
        return True
    st.warning("⚠️ Demo hanya 2x generate. Beli premium untuk unlimited!")
    st.markdown(f'<a href="{WA_LINK}" target="_blank" class="btn-primary">💎 Beli Premium</a>', unsafe_allow_html=True)
    return False

with tab1:
    st.markdown("Buat judul produk yang menarik.")
    prod_title = st.text_input("Nama Produk", key="seo_title")
    if st.button("✨ Generate Judul SEO"):
        if generator_access():
            if not is_premium():
                inc_demo_generator()
            if prod_title:
                titles = [f"🔥 {prod_title} - Kualitas Premium!", f"💯 {prod_title} BEST SELLER!", f"✨ WAJIB PUNYA! {prod_title}", f"🎯 {prod_title} Dijamin Nyaman", f"💎 {prod_title} PREMIUM QUALITY"]
                for t in titles:
                    st.markdown(f"- {t}")
            else:
                st.warning("Masukkan nama produk.")

with tab2:
    st.markdown("Buat deskripsi produk yang meyakinkan.")
    prod_desc = st.text_input("Nama Produk", key="desc_prod")
    manfaat = st.text_area("Manfaat (pisahkan koma)")
    if st.button("✨ Generate Deskripsi"):
        if generator_access():
            if not is_premium():
                inc_demo_generator()
            if prod_desc:
                desc = f"✨ {prod_desc} - Kualitas Premium!\n✅ Bahan berkualitas\n✅ Desain modern\n✅ Size lengkap\n✅ Garansi 100%\n\n🔥 Promo terbatas! Order sekarang."
                st.code(desc, language="markdown")
            else:
                st.warning("Masukkan nama produk.")

with tab3:
    st.markdown("Buat hook video TikTok 3 detik pertama.")
    prod_hook = st.text_input("Nama Produk", key="hook_prod")
    style = st.selectbox("Gaya Hook", ["Problem Solver", "Diskon", "Bukti Sosial", "Curiosity"])
    if st.button("✨ Generate Hook"):
        if generator_access():
            if not is_premium():
                inc_demo_generator()
            if prod_hook:
                hooks = [f"😫 Capek cari {prod_hook}? STOP!", f"🔥 DISKON 50% {prod_hook}!", f"🏆 {prod_hook} best seller!", f"🤔 Kenapa semua pake {prod_hook}?"]
                for h in hooks:
                    st.markdown(f"- 🎬 {h}")
            else:
                st.warning("Masukkan nama produk.")

# ==================== FOOTER ====================
st.markdown("---")
st.markdown(f"""
<div style="text-align:center; font-size:12px; color:#888;">
    <p>🩺 DOCTOR ADS SHOPEE & TIKTOK PREMIUM</p>
    <p>© 2024 Arkidigital - Solusi Digital Marketing Terbaik</p>
</div>
""", unsafe_allow_html=True)
