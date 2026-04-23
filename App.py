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
    initial_sidebar_state="collapsed"
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

    .stNumberInput input, .stTextInput input, .stSelectbox div {
        background: rgba(0,0,0,0.7) !important; 
        border: 1px solid rgba(255,255,255,0.5) !important; 
        border-radius: 12px !important; 
        color: #FFFFFF !important;
    }
    </style>
    """, unsafe_allow_html=True)

apply_premium_style()

# ==================== 2. SESSION & LOCK SYSTEM ====================
if "authenticated" not in st.session_state: st.session_state["authenticated"] = False
if "demo_mode" not in st.session_state: st.session_state["demo_mode"] = False
if "demo_start_time" not in st.session_state: st.session_state["demo_start_time"] = None
if "demo_analysis_count" not in st.session_state: st.session_state["demo_analysis_count"] = 0
if "products" not in st.session_state: st.session_state["products"] = []
if "analysis_done" not in st.session_state: st.session_state["analysis_done"] = False
if "last_ctr" not in st.session_state: st.session_state["last_ctr"] = 0
if "last_roas" not in st.session_state: st.session_state["last_roas"] = 0
if "last_roas_bep" not in st.session_state: st.session_state["last_roas_bep"] = 0
if "last_s_rate" not in st.session_state: st.session_state["last_s_rate"] = 0
if "last_clicks" not in st.session_state: st.session_state["last_clicks"] = 0
if "last_orders" not in st.session_state: st.session_state["last_orders"] = 0
if "last_profit" not in st.session_state: st.session_state["last_profit"] = 0
if "last_budget_set" not in st.session_state: st.session_state["last_budget_set"] = 0
if "last_target_roas" not in st.session_state: st.session_state["last_target_roas"] = 0
if "last_budget_spent" not in st.session_state: st.session_state["last_budget_spent"] = 0

ADMIN_USERNAME = "arkidigital"
ADMIN_PASSWORD = "Arkidigital2026"
CHECKOUT_LINK = "https://muhammad-masruri.myscalev.com/checkout-pageku"

# ==================== API KEY CONFIGURATION ====================
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")

def call_gemini_api(prompt):
    """Panggil Gemini API via HTTP"""
    if not GEMINI_API_KEY:
        return None
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    try:
        response = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=30)
        if response.status_code == 200:
            result = response.json()
            return result["candidates"][0]["content"]["parts"][0]["text"]
        return None
    except Exception as e:
        return None

def format_rp(angka):
    if angka >= 1_000_000: return f"Rp{angka/1_000_000:.1f}JT"
    if angka >= 1000: return f"Rp{angka/1000:.0f}RB"
    return f"Rp{angka:,.0f}"

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

# ==================== FUNGSI REKOMENDASI (1-5) ====================
def generate_rekomendasi(roas_aktual, roas_bep, s_rate, clicks, orders, budget_set, target_roas, budget_spent, ctr):
    """Menghasilkan rekomendasi berdasarkan aturan 1-5"""
    rekom_tindakan = ""
    rekom_roas = target_roas
    rekom_budget = budget_set
    prioritas = ""
    warna = "info"
    
    # ATURAN 1: KLIK BANYAK, BUDGET HABIS, ORDER 0 → STOP IKLAN
    if clicks > 50 and s_rate >= 80 and orders == 0:
        prioritas = "🔴 PRIORITAS 1 - URGENT (Stop Iklan)"
        warna = "danger"
        rekom_budget = budget_set * 0.5
        rekom_tindakan = f"""🚨 **HENTIKAN IKLAN SEGERA!**

📊 Data: {clicks} klik, budget terserap {s_rate:.0f}%, tapi 0 order.

**Penyebab:** Produk belum layak iklan.

**Yang harus dilakukan:**
1. Cek harga produk — bandingkan dengan kompetitor
2. Tambah review & rating (target 10-20 review positif)
3. Perbaiki deskripsi — fokus ke MANFAAT
4. Pastikan stok aman

**Setelah produk siap, restart iklan dengan budget kecil (Rp50-100rb/hari).**"""
    
    # ATURAN 2: SIAP SCALE
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

⏰ **Tunggu 3 hari** tanpa perubahan apapun.

📌 Evaluasi setelah 3 hari:
- Jika ROAS tetap stabil → bisa scale lagi 30%
- Jika ROAS turun drastis → turunkan budget ke semula"""
    
    # ATURAN 3: ROAS PROFIT, BUDGET BELUM HABIS
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

⏰ **Tunggu 3 hari** tanpa perubahan apapun.

📌 Evaluasi setelah 3 hari:
- Jika budget sudah habis → siap scale
- Jika masih belum habis → turunkan ROAS lagi 0.5 poin"""
    
    # ATURAN 4: IKLAN RUGI
    elif roas_aktual < roas_bep and roas_aktual > 0:
        prioritas = "🔴 PRIORITAS 3 - IKLAN RUGI"
        warna = "danger"
        rekom_roas = roas_bep + 0.5
        rekom_budget = budget_set * 0.7
        rugi = (roas_bep - roas_aktual) * budget_spent
        rekom_tindakan = f"""💸 **IKLAN RUGI!**

📉 ROAS {roas_aktual:.1f}x < BEP {roas_bep:.1f}x
💰 Estimasi kerugian: {format_rp(rugi)} dari {format_rp(budget_spent)} yang terpakai

**Penyebab:** Target ROAS terlalu rendah atau produk kurang meyakinkan.

**Solusi:**
✅ Naikkan target ROAS **0.5 poin** menjadi **{rekom_roas:.1f}x**
🔻 Turunkan budget **30%** menjadi {format_rp(rekom_budget)} untuk mengurangi kerugian

**Atau jika produk belum layak:**
- Berhenti iklan sementara, perbaiki produk (harga, review, deskripsi)"""
    
    # ATURAN 5: PERFORMA SEHAT
    elif roas_aktual >= roas_bep:
        prioritas = "🟢 PRIORITAS 5 - PANTAU"
        rekom_tindakan = f"""✅ **PERFORMA SEHAT**

📈 ROAS {roas_aktual:.1f}x ≥ BEP {roas_bep:.1f}x
💰 Budget terserap {s_rate:.0f}%

**Rekomendasi:**
✅ Pertahankan setting saat ini
⏰ Pantau selama **3-5 hari** tanpa perubahan

📌 Jika konsisten (ROAS tetap di atas BEP dan budget habis), siap scale dengan menaikkan budget 30% (jangan sentuh ROAS)."""
    
    # TAMBAHAN: CTR RENDAH
    if ctr < 2 and clicks > 0 and "Stop Iklan" not in rekom_tindakan:
        rekom_tindakan += f"""

---
📸 **MASALAH CTR RENDAH!**

CTR {ctr:.1f}% < 2% → Iklan kurang menarik.

**Solusi:** Ganti visual (foto utama / video hook 3 detik pertama). Buat 3 variasi kreatif baru."""
    
    return rekom_tindakan, rekom_budget, rekom_roas, prioritas, warna

# ==================== 3. ACCESS CONTROL ====================
demo_expired = False
if st.session_state.demo_mode and st.session_state.demo_start_time:
    elapsed = (datetime.now() - st.session_state.demo_start_time).total_seconds()
    if elapsed > 300 or st.session_state.demo_analysis_count >= 2:
        demo_expired = True

if (not st.session_state.authenticated and not st.session_state.demo_mode) or demo_expired:
    st.markdown('<div style="text-align:center; padding-top:50px;">', unsafe_allow_html=True)
    if demo_expired:
        st.markdown('<h1 class="gold-header">⏰ TRIAL SELESAI</h1>', unsafe_allow_html=True)
        st.markdown('<h3>Akses demo habis. Upgrade sekarang untuk kontrol penuh tanpa batas!</h3>', unsafe_allow_html=True)
    else:
        st.markdown('<h1 class="gold-header" style="font-size:4.5rem;">🩺 DOCTOR ADS</h1>', unsafe_allow_html=True)
    
    st.markdown(f'<a href="{CHECKOUT_LINK}" target="_blank" class="cta-upgrade">💎 UNLOCK PREMIUM SEKARANG - RP147RB</a>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        with st.form("login"):
            st.markdown("### 🔐 Member Login")
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.form_submit_button("MASUK DASHBOARD"):
                if u == ADMIN_USERNAME and p == ADMIN_PASSWORD:
                    st.session_state.authenticated = True
                    st.session_state.demo_mode = False
                    st.rerun()
                else: st.error("Login Gagal!")
    with c2:
        if not demo_expired:
            st.markdown('<div class="premium-card"><h3>🎁 Demo Mode</h3>', unsafe_allow_html=True)
            st.write("Coba 5 menit atau 2x analisis secara gratis.")
            if st.button("MULAI TRIAL"):
                st.session_state.demo_mode = True
                st.session_state.demo_start_time = datetime.now()
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ==================== 4. MAIN ELITE DASHBOARD ====================
st.markdown('<h1 class="gold-header">🩺 ADVERTISING COMMAND CENTER</h1>', unsafe_allow_html=True)

# --- SIDEBAR DATABASE PRODUK ---
with st.sidebar:
    st.markdown("### 📦 **Produk Database**")
    if st.session_state.authenticated:
        products = st.session_state.products
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
        if products:
            pilih_produk = st.selectbox("Pilih Produk", ["-- Pilih --"] + [p["nama"] for p in products], key="pilih_produk_sidebar")
            if pilih_produk != "-- Pilih --":
                prod = next(p for p in products if p["nama"] == pilih_produk)
                st.info(f"ROAS BEP: {prod['roas_bep']:.1f}x | Laba: Rp{prod['laba_kotor']:,.0f}")
                if st.button("🗑️ Hapus Produk", key="hapus_produk_sidebar"):
                    delete_product(pilih_produk)
                    st.rerun()
    
    st.markdown("---")
    st.markdown(f'<a href="{CHECKOUT_LINK}" target="_blank" style="display:block; text-align:center; background:#00E5A0; color:#020617; padding:10px; border-radius:40px; text-decoration:none; font-weight:bold;">💎 Upgrade Premium</a>', unsafe_allow_html=True)

# --- FINANSIAL AUDIT ---
col_calc, col_audit = st.columns([2, 1])
with col_calc:
    st.markdown('<div class="premium-card"><h3>🎯 ROAS BEP Calculator</h3>', unsafe_allow_html=True)
    cb1, cb2, cb3 = st.columns(3)
    hj = cb1.number_input("Harga Jual (Rp)", value=150000, key="hj_main")
    modal = cb2.number_input("Modal (Rp)", value=75000, key="modal_main")
    admin_p = cb3.slider("Admin Platform %", 5, 30, 20, key="admin_main")
    target_p = st.number_input("Target Profit (Rp)", value=0, key="target_main")
    
    laba_kotor_p = hj - modal - (hj * admin_p / 100)
    laba_setelah_p = laba_kotor_p - target_p
    roas_bep_p = hj / laba_setelah_p if laba_setelah_p > 0 else 999
    
    st.markdown(f'<div style="text-align:center;"><h1 style="color:#00E5A0; font-size:4rem; margin:0;">{roas_bep_p:.2f}x</h1><p style="color:#888;">TARGET ROAS BEP ANDA</p></div>', unsafe_allow_html=True)
    
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
        h_komp = st.number_input("Harga Kompetitor", value=140000, key="harga_komp_main")
        if hj > h_komp * 1.2: 
            st.warning("⚠️ Harga terlalu mahal. Turunkan atau tambah value produk.")
        elif laba_kotor_p < 5000: 
            st.error("❌ Margin terlalu tipis. Cari produk lain atau naikkan harga.")
        else:
            st.success("✅ Produk layak beriklan!")
            if laba_kotor_p > 20000:
                st.balloons()
    st.markdown('</div>', unsafe_allow_html=True)

# --- ANALISIS IKLAN ---
st.markdown('<div class="premium-card"><h3>📊 Ad Performance Matrix</h3>', unsafe_allow_html=True)
ip1, ip2, ip3 = st.columns(3)
impressions = ip1.number_input("👁️ Impressions", value=20000, key="imp_main")
clicks = ip1.number_input("🖱️ Clicks", value=600, key="clicks_main")
budget_spent = ip2.number_input("💸 Spent (Rp)", value=150000, key="spent_main")
sales = ip2.number_input("💰 Revenue (Rp)", value=900000, key="sales_main")
orders = ip3.number_input("📦 Orders", value=8, key="orders_main")
budget_set = ip3.number_input("Budget Setting", value=200000, key="budget_set_main")
target_roas_p = st.number_input("🎯 Target ROAS", value=6.0, key="target_roas_main")

# Tombol Analisis
if st.button("RUN DEEP ANALYTICS", use_container_width=True, key="run_analytics"):
    # Update session state
    if st.session_state.demo_mode:
        st.session_state.demo_analysis_count += 1
    
    # Hitung metrik
    ctr_p = (clicks/impressions*100) if impressions > 0 else 0
    roas_akt_p = (sales/budget_spent) if budget_spent > 0 else 0
    s_rate_p = (budget_spent/budget_set*100) if budget_set > 0 else 0
    profit_est_p = (laba_kotor_p * orders) - budget_spent if orders > 0 else -budget_spent
    cpc_p = budget_spent/clicks if clicks > 0 else 0
    
    # Simpan ke session state untuk ditampilkan
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
    
    # Metric Cards
    m1, m2, m3, m4 = st.columns(4)
    m1.markdown(f'<div class="premium-card"><h5>📈 CTR</h5><h2 style="color:white;">{ctr_p:.2f}%</h2><p style="color:#888;">{"✅ Normal" if ctr_p >= 2 else "⚠️ Rendah"}</p></div>', unsafe_allow_html=True)
    m2.markdown(f'<div class="premium-card"><h5>💰 ROAS</h5><h2 style="color:#00E5A0;">{roas_akt_p:.2f}x</h2><p style="color:#888;">{"🟢 Profit" if roas_akt_p >= roas_bep_p else "🔴 Rugi"}</p></div>', unsafe_allow_html=True)
    m3.markdown(f'<div class="premium-card"><h5>💎 PROFIT</h5><h2 style="color:{"#00E5A0" if profit_est_p > 0 else "#ff6b6b"};">{format_rp(profit_est_p)}</h2><p style="color:#888;">{"Untung" if profit_est_p > 0 else "Rugi"}</p></div>', unsafe_allow_html=True)
    m4.markdown(f'<div class="premium-card"><h5>🎯 BEP</h5><h2 style="color:white;">{roas_bep_p:.2f}x</h2><p style="color:#888;">{"✅ Aman" if roas_akt_p >= roas_bep_p else "⚠️ Dibawah"}</p></div>', unsafe_allow_html=True)
    
    # ==================== AI SUMMARY ====================
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
            if ai_summary:
                st.markdown(f'<div class="premium-card"><h3>🤖 AI Insight</h3><p style="font-size:1.1rem;">{ai_summary}</p></div>', unsafe_allow_html=True)
    
    # ==================== REKOMENDASI 1-5 (WAJIB MUNCUL) ====================
    st.markdown("### 🎯 Rekomendasi Strategis")
    
    rekom_tindakan, rekom_budget, rekom_roas, prioritas, warna = generate_rekomendasi(
        roas_akt_p, roas_bep_p, s_rate_p, clicks, orders, 
        budget_set, target_roas_p, budget_spent, ctr_p
    )
    
    bg_c = {"danger":"#fee2e2", "warning":"#fef3c7", "success":"#d1fae5", "info":"#dbeafe"}.get(warna, "#f0f0ff")
    br_c = {"danger":"#dc2626", "warning":"#f59e0b", "success":"#10b981", "info":"#3b82f6"}.get(warna, "#667eea")
    
    st.markdown(f"""
    <div style="background:{bg_c}; border-radius:1rem; padding:2rem; border-left:10px solid {br_c}; margin:1rem 0; color: #1a1a1a;">
        <h3 style="margin:0 0 0.5rem 0; font-weight: 800;">{prioritas}</h3>
        <p style="font-size:1.15rem; line-height:1.6;">{rekom_tindakan.replace(chr(10), '<br>')}</p>
        <hr style="border:0.5px solid {br_c}; opacity:0.3;">
        <p><strong>💰 Budget Rekomendasi:</strong> {format_rp(rekom_budget)} | <strong>🎯 Target ROAS:</strong> {rekom_roas:.1f}x</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ==================== PREDIKSI SCALE (Jika kondisi terpenuhi) ====================
if st.session_state.analysis_done and st.session_state.last_roas >= st.session_state.last_roas_bep * 1.2:
    st.markdown('<div class="premium-card"><h3>📈 Prediksi Scale</h3>', unsafe_allow_html=True)
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

# ==================== PREDIKSI 7 HARI ====================
if st.session_state.analysis_done and st.session_state.last_roas > 0:
    st.markdown('<div class="premium-card"><h3>📊 Prediksi 7 Hari ke Depan</h3>', unsafe_allow_html=True)
    
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

# ==================== REKOMENDASI BUDGET BESOK ====================
if st.session_state.analysis_done and st.session_state.last_roas > 0:
    st.markdown('<div class="premium-card"><h3>💰 Rekomendasi Budget Besok</h3>', unsafe_allow_html=True)
    
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

# ==================== TANYA JAWAB AI ====================
st.markdown('<div class="premium-card"><h3>💬 Tanya AI (Konsultasi Iklan)</h3>', unsafe_allow_html=True)
user_question = st.text_input("Pertanyaan kamu:", placeholder="Contoh: ROAS saya turun drastis, harus gimana?", key="chatbot_question")
if st.button("🤖 Tanya AI", use_container_width=True, key="ask_ai"):
    if user_question:
        with st.spinner("AI sedang berpikir..."):
            prompt = f"""Anda adalah pakar iklan TikTok & Shopee. Jawab pertanyaan seller pemula ini dengan singkat (maks 100 kata) dan mudah dipahami.

Pertanyaan: {user_question}

Jawab dengan bahasa Indonesia yang ramah, profesional, dan berikan solusi praktis.
"""
            answer = call_gemini_api(prompt)
            if answer:
                st.info(f"💡 {answer}")
            else:
                st.warning("Maaf, AI sedang sibuk. Coba lagi nanti.")
    else:
        st.warning("Masukkan pertanyaan dulu.")
st.markdown('</div>', unsafe_allow_html=True)

# ==================== GENERATOR ====================
st.markdown("<h2 class='gold-header'>✨ Elite Copywriter Lab</h2>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["📝 SEO Title", "📄 Deskripsi", "🎬 Hook Video", "#️⃣ Hashtag"])

with tab1:
    p_name = st.text_input("🏷️ Nama Produk", placeholder="Contoh: Kaos Oversize Premium", key="seo_name")
    if st.button("Generate Elite SEO Title", key="gen_seo"):
        with st.spinner("🧠 AI sedang merancang judul..."):
            if p_name:
                res = call_gemini_api(f"Buat 5 judul untuk '{p_name}' di Shopee. Judul menarik, ada emoji, fokus manfaat. Output per baris.")
                st.code(res if res else f"🔥 {p_name} - Kualitas Premium\n💯 {p_name} BEST SELLER", language="text")
            else:
                st.warning("Masukkan nama produk.")

with tab2:
    p_name_desc = st.text_input("🏷️ Nama Produk", placeholder="Contoh: Kaos Oversize Premium", key="desc_name")
    manfaat = st.text_area("Manfaat (pisahkan koma)", placeholder="Contoh: adem, nyaman, tidak panas", key="manfaat_desc")
    if st.button("Generate Elite Deskripsi", key="gen_desc"):
        with st.spinner("🧠 AI sedang menulis deskripsi..."):
            if p_name_desc:
                prompt = f"Buat deskripsi untuk '{p_name_desc}' di Shopee. Manfaat: {manfaat}. Gunakan emoji, ajakan beli."
                res = call_gemini_api(prompt)
                st.code(res if res else f"✨ {p_name_desc} - Kualitas Premium!\n✅ {manfaat if manfaat else 'Bahan premium'}", language="markdown")
            else:
                st.warning("Masukkan nama produk.")

with tab3:
    p_name_hook = st.text_input("🏷️ Nama Produk", placeholder="Contoh: Kaos Oversize Premium", key="hook_name")
    gaya = st.selectbox("Gaya Hook", ["Problem Solver", "Diskon", "Bukti Sosial", "Curiosity", "Emosional"], key="gaya_hook")
    if st.button("Generate Elite Hook", key="gen_hook"):
        with st.spinner("🧠 AI sedang membuat hook..."):
            if p_name_hook:
                prompt = f"Buat 5 hook untuk '{p_name_hook}' di TikTok. Gaya: {gaya}. Hook 3 detik pertama."
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

with tab4:
    p_name_hash = st.text_input("🏷️ Nama Produk", placeholder="Contoh: Kaos Oversize Premium", key="hash_name")
    niche_hash = st.selectbox("Niche", ["Fashion", "Kosmetik", "Makanan", "Elektronik", "Olahraga"], key="niche_hash")
    if st.button("Generate Hashtag Viral", key="gen_hash"):
        with st.spinner("🧠 AI sedang membuat hashtag..."):
            if p_name_hash:
                prompt = f"Buat 15 hashtag TikTok untuk '{p_name_hash}', niche {niche_hash}. Format: #fyp #viral #namaproduk"
                res = call_gemini_api(prompt)
                st.code(res if res else "#fyp #viral #rekomendasi #shopee #tiktokshop #promo #diskon", language="text")
            else:
                st.warning("Masukkan nama produk.")

# ==================== FOOTER ====================
st.markdown(f'<div style="text-align:center; padding:60px;"><a href="{CHECKOUT_LINK}" target="_blank" class="cta-upgrade">💎 UPGRADE PREMIUM - AKSES TANPA BATAS</a></div>', unsafe_allow_html=True)
