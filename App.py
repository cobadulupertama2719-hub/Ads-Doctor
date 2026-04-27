
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
    """Menghasilkan rekomendasi berdasarkan aturan 1-5 + analisa tambahan"""
    rekom_tindakan = ""
    rekom_roas = target_roas
    rekom_budget = budget_set
    prioritas = ""
    warna = "info"
    analisa_tambahan = ""
    
    # Hitung metrik tambahan
    cvr = (orders / clicks * 100) if clicks > 0 else 0
    profit_margin = (roas_aktual - roas_bep) / roas_bep * 100 if roas_bep > 0 else 0
    sisa_budget = budget_set - budget_spent if budget_set > budget_spent else 0
    
    # ========== PRIORITAS 1-5 (LENGKAP) ==========
    
    # PRIORITAS 1: URGENT STOP IKLAN
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
    
    # PRIORITAS 4: SIAP SCALE
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

⏰ **Tunggu 3 hari** tanpa perubahan apapun untuk melihat hasil scale."""
    
    # PRIORITAS 2: OPTIMASI BUDGET (Turunkan 1 poin, tunggu 3-7 hari)
    elif roas_aktual >= roas_bep and s_rate < 85:
        prioritas = "🟡 PRIORITAS 2 - OPTIMASI"
        warna = "warning"
        rekom_roas = target_roas - 1
        rekom_tindakan = f"""⚡ **OPTIMASI BUDGET**

✅ ROAS {roas_aktual:.1f}x ≥ BEP {roas_bep:.1f}x (untung)
📊 Budget terserap {s_rate:.0f}% (masih ada sisa Rp{sisa_budget:,.0f})

**Agar budget habis dan order maksimal:**
✅ Turunkan target ROAS **1 poin** menjadi **{rekom_roas:.1f}x**
✅ **JANGAN UBAH BUDGET** (tetap {format_rp(budget_set)})

⏰ **Tunggu 3-7 hari** dengan setting baru ini, evaluasi lagi setelah 3-7 hari."""
    
    # PRIORITAS 3: IKLAN RUGI (Dua skenario)
    elif roas_aktual < roas_bep and roas_aktual > 0:
        # Cek apakah budget cepat habis (s_rate >= 80)
        if s_rate >= 80:
            prioritas = "🔴 PRIORITAS 3A - IKLAN RUGI (Budget Cepat Habis)"
            warna = "danger"
            rekom_roas = target_roas + 1
            rekom_budget = budget_set
            rekom_tindakan = f"""💸 **IKLAN RUGI - BUDGET CEPAT HABIS!**

📉 ROAS {roas_aktual:.1f}x < BEP {roas_bep:.1f}x
💰 Budget terserap {s_rate:.0f}% (cepat habis)

**Penyebab:** Target ROAS terlalu rendah → sistem terlalu agresif, traffic kurang berkualitas.

**Solusi:**
✅ Naikkan target ROAS **1 poin** menjadi **{rekom_roas:.1f}x**
✅ **PERTAHANKAN** budget tetap {format_rp(budget_set)}

⏰ **Tunggu 3 hari**, jika masih cepat habis dan rugi → naikkan lagi 1 poin.

Target: Agar budget habis dalam 1 hari dengan ROAS ≥ BEP"""
        else:
            prioritas = "🔴 PRIORITAS 3B - IKLAN RUGI (Umum)"
            warna = "danger"
            rekom_roas = roas_bep + 0.5
            rekom_budget = budget_set * 0.7
            rekom_tindakan = f"""💸 **IKLAN RUGI!**

📉 ROAS {roas_aktual:.1f}x < BEP {roas_bep:.1f}x

**Solusi:**
✅ Naikkan target ROAS **0.5 poin** menjadi **{rekom_roas:.1f}x**
🔻 Turunkan budget **30%** menjadi {format_rp(rekom_budget)} untuk mengurangi kerugian

⏰ **Tunggu 3 hari** lalu evaluasi ulang."""
    
    # PRIORITAS 5: PERFORMA SEHAT (Default)
    elif roas_aktual >= roas_bep:
        prioritas = "🟢 PRIORITAS 5 - PANTAU"
        rekom_tindakan = f"""✅ **PERFORMA SEHAT**

📈 ROAS {roas_aktual:.1f}x ≥ BEP {roas_bep:.1f}x
💰 Budget terserap {s_rate:.0f}%

**Rekomendasi:**
✅ Pertahankan setting saat ini
⏰ Pantau selama **3-5 hari** tanpa perubahan"""
    
    else:
        prioritas = "ℹ️ PERLU DATA LEBIH LENGKAP"
        warna = "info"
        rekom_tindakan = f"""📊 **Data Belum Cukup**

Mohon isi data performa iklan dengan lengkap:
- Pastikan Impressions > 0
- Pastikan Budget Spent > 0
- Pastikan Budget Setting > 0

Setelah data lengkap, klik RUN ANALYTICS lagi."""
    
    # ========== ANALISA TAMBAHAN (TIDAK MENGUBAH PRIORITAS) ==========
    
    # Analisa 1: CTR bagus (>3%) & CVR = 0
    if ctr > 3 and cvr == 0 and orders == 0:
        analisa_tambahan += f"""
---
📊 **ANALISA STUDI KASUS: Klik Tinggi, Order Nol**

🔍 Data: CTR {ctr:.1f}% (>3% bagus) tapi {clicks} klik tidak menghasilkan order.

💡 **Apa yang terjadi?**
Klik tinggi = iklan MENARIK
Tapi gak ada yang beli = PRODUK BERMASALAH

👉 Kemungkinan penyebab:
• Harga kalah bersaing dengan kompetitor
• Belum dapat kepercayaan pembeli (minim review/rating)
• Deskripsi produk lemah (tidak menjelaskan manfaat)

🎯 **Solusi:**
✅ Perbaiki fondasi produk sebelum lanjut iklan
✅ Bandingkan harga dengan kompetitor
✅ Kumpulkan 10-20 review positif
✅ Perkuat deskripsi (fokus ke MANFAAT, bukan fitur)"""
    
    # Analisa 2: CTR rendah (<2%) & ROAS < BEP
    elif ctr < 2 and roas_aktual < roas_bep and roas_aktual > 0:
        analisa_tambahan += f"""
---
📊 **ANALISA STUDI KASUS: CTR Rendah, Iklan Mahal**

🔍 Data: CTR {ctr:.1f}% (<2%) dan ROAS {roas_aktual:.1f}x < BEP {roas_bep:.1f}x

💡 **Apa yang terjadi?**
CTR rendah = iklan tidak menarik perhatian
Iklan mahal = biaya per klik tinggi
ROAS rugi = biaya tidak sebanding hasil

👉 Masalah ada di **IKLAN**, bukan produk

🎯 **Solusi:**
✅ Ganti visual (foto utama / video hook 3 detik pertama)
✅ Perbaiki hook dengan pertanyaan provokatif atau solusi masalah
✅ Tambahkan CTA yang kuat (buruan, terbatas, diskon)
✅ Buat 3-5 variasi kreatif baru untuk A/B testing"""
    
    # Analisa 3: ROAS sedikit di atas BEP (untung tipis, margin <20%)
    elif profit_margin > 0 and profit_margin < 20 and roas_aktual > 0 and "SIAP SCALE" not in prioritas:
        analisa_tambahan += f"""
---
📊 **ANALISA STUDI KASUS: Untung Tipis, Rawan Turun**

🔍 Data: ROAS {roas_aktual:.1f}x hanya {profit_margin:.0f}% di atas BEP {roas_bep:.1f}x

💡 **Apa yang terjadi?**
🟡 Profit tipis = rawan berubah jadi rugi
📉 Jika kompetitor naik atau biaya iklan naik, bisa boncos diam-diam

🎯 **Solusi:**
✅ Naikkan target ROAS **0.5-1 poin** untuk buffer
✅ Pantau lebih ketat (setiap 2 hari, bukan 5 hari)
✅ Cari cara efisiensi biaya (perbaiki CTR/CVR)"""
    
    # Analisa 4: Budget tidak habis (<50%) karena ROAS terlalu tinggi
    elif s_rate < 50 and target_roas > roas_bep + 1 and roas_aktual > 0:
        analisa_tambahan += f"""
---
📊 **ANALISA STUDI KASUS: Budget Tidak Habis**

🔍 Data: Budget terserap hanya {s_rate:.0f}% dari {format_rp(budget_set)}
Target ROAS: {target_roas:.1f}x (terlalu tinggi)

💡 **Apa yang terjadi?**
ROAS terlalu tinggi → sistem terlalu selektif
Sistem cuma cari pembeli yang "paling pasti beli" 
Akibatnya: traffic sedikit, budget tidak habis

🎯 **Solusi:**
✅ Turunkan target ROAS **0.5-1 poin**
✅ Ini bukan masalah kurang budget, tapi terlalu selektif
⏰ Setelah turun, tunggu 3 hari → budget akan terserap lebih banyak"""
    
    # Tambahan saran CTR rendah jika belum tercover
    if ctr < 2 and clicks > 0 and "Stop Iklan" not in rekom_tindakan and "CTR rendah" not in analisa_tambahan and "belum layak" not in rekom_tindakan:
        if analisa_tambahan:
            analisa_tambahan += f"\n\n📸 **Tambahan:** CTR {ctr:.1f}% < 2% → Ganti visual iklan (foto utama / video hook)."
        else:
            analisa_tambahan += f"""
---
📸 **MASALAH CTR RENDAH!**

CTR {ctr:.1f}% < 2% → Iklan kurang menarik.

**Solusi:** Ganti visual (foto utama / video hook 3 detik pertama). Buat 3 variasi kreatif baru."""
    
    # Gabungkan rekomendasi utama dengan analisa tambahan
    if analisa_tambahan:
        rekom_tindakan += analisa_tambahan
    
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
            <p style="font-size:1rem; line-height:1.6;">{rekom_tindakan}</p>
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

# ==================== HALAMAN GMV MAX (TIDAK DIUBAH) ====================
def render_gmvmax():
    st.markdown('<div class="premium-card"><h3 style="color:#FFD700;">🚀 GMV MAX - Panduan Strategi Iklan untuk Pemula</h3>', unsafe_allow_html=True)
    st.markdown('<p style="color:#94A3B8;">Panduan lengkap memahami algoritma GMV Max TikTok & Shopee</p>', unsafe_allow_html=True)
    
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
    
    with st.expander("🧠 2. LOGIKA INTI ALGORITMA (CTR, CVR, CPA)", expanded=False):
        st.markdown("""
        **Cara AI mikir:** "Dari semua orang yang lihat iklan ini, siapa yang paling mungkin beli dengan biaya murah?"
        
        **Algoritma pakai 3 sinyal utama:**
        
        | Sinyal | Fungsi |
        |--------|--------|
        | **CTR** | "Apakah orang tertarik?" → Tinggi = disebar luas / Rendah = dipersempit |
        | **CVR** | "Apakah orang beli?" → Klik tinggi tapi gak beli = produk lemah |
        | **CPA** | "Berapa biaya dapetin 1 order?" → **INI YANG PALING PENTING** |
        
        > 🔥 **Rumus dalam kepala algoritma:** Profit ≈ Revenue – Cost
        """)
    
    with st.expander("🎯 3. PERAN ROAS DI DALAM ALGORITMA", expanded=False):
        st.markdown("""
        **Banyak orang salah kaprah!** ROAS itu bukan target profit, tapi **constraint (batasan sistem)**.
        
        | Setting ROAS | Perilaku Algoritma |
        |--------------|-------------------|
        | **Tinggi** | Cari buyer yang "paling pasti beli" → traffic kecil tapi mahal |
        | **Rendah** | Lebih agresif → traffic luas tapi risk tinggi |
        
        > 🔥 **Kesimpulan:** ROAS = filter kualitas traffic
        """)
    
    with st.expander("💸 4. HUBUNGAN ROAS vs BUDGET", expanded=False):
        st.markdown("""
        | Setting | Respon Algoritma |
        |---------|------------------|
        | ROAS tinggi | selektif |
        | ROAS rendah | eksplorasi |
        | Budget besar | butuh audience luas |
        | Budget kecil | distribusi terbatas |
        
        > 🔥 **Insight:** Budget besar + ROAS tinggi = sistem "bingung" (gak bisa spend)
        """)
    
    with st.expander("🔄 5. LEARNING PHASE", expanded=False):
        st.markdown("""
        **Syarat stabil sistem:**
        - Conversion cukup (±30–50)
        - Tidak sering diubah
        - Budget cukup untuk sampling
        
        **❌ Jangan ganggu:** Edit ROAS, ganti budget drastis, pause terlalu cepat → Model reset!
        """)
    
    with st.expander("🧪 6. OPTIMISASI OTOMATIS", expanded=False):
        st.markdown("""
        Setelah learning, sistem masuk fase **EXPLOIT MODE**:
        - Fokus ke audience paling profitable
        - Naikkan distribusi ke segmen itu
        - Kurangi yang tidak perform
        
        > 🔥 **Ini yang disebut:** "Scaling otomatis oleh AI"
        """)
    
    with st.expander("📉 7. KENAPA IKLAN BISA DROP?", expanded=False):
        st.markdown("""
        | Penyebab | Penjelasan |
        |----------|------------|
        | Audience fatigue | Jenuh |
        | Kompetitor naik | Auction lebih mahal |
        | Data berubah | Buyer behavior berubah |
        """)
    
    with st.expander("🧠 8. HUBUNGAN PRODUK DENGAN ALGORITMA", expanded=False):
        st.markdown("""
        Algoritma **TIDAK bisa menyelamatkan produk jelek**.
        
        > 🔥 **Jadi:** Produk = bahan bakar, Algoritma = mesin. Kalau bahan bakar jelek → mesin gak jalan
        """)
    
    with st.expander("🎯 9. FLOW KERJA ALGORITMA", expanded=False):
        st.markdown("""
        1. Iklan jalan
        2. Sistem tes audience
        3. Ukur CTR → tertarik?
        4. Ukur CVR → beli?
        5. Hitung CPA
        6. Bandingkan dengan target ROAS
        7. Kalau cocok → scale / Kalau tidak → stop
        """)
    
    with st.expander("🔥 10. RUMUS BESAR GMV MAX", expanded=False):
        st.markdown("""
        ```
        Profit = (CTR × CVR × AOV) – CPA
        ```
        > **Sistem menyederhanakan:** "Apakah ROAS tercapai?"
        """)
    
    with st.expander("⚠️ 11. KESALAHAN YANG SERING TERJADI", expanded=False):
        st.markdown("""
        | ❌ Kesalahan | ✅ Yang Benar |
        |--------------|---------------|
        | Terlalu sering edit | Biarkan belajar (3-5 hari) |
        | Fokus ROAS tinggi dari awal | Mulai dengan ROAS sedang |
        | Budget terlalu kecil | Pastikan cukup untuk sampling |
        | Produk belum valid | Validasi produk dulu |
        """)
    
    with st.expander("🔥 12. KESIMPULAN BESAR", expanded=False):
        st.markdown("""
        **3 kontrol utama kamu:**
        - **ROAS** → arahkan kualitas
        - **Budget** → atur volume
        - **Produk & konten** → tentukan hasil
        """)
    
    st.markdown("""
    <div class="gmv-quote">
    💡 <strong>Inti Satu Kalimat:</strong><br>
    GMV Max adalah sistem distribusi traffic berbasis probabilitas pembelian yang dikontrol oleh constraint ROAS dan diberi makan oleh data CTR & CVR.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== HALAMAN GENERATOR (TIDAK DIUBAH) ====================
def render_generator():
    st.markdown("<h2 class='gold-header'>✨ Elite Copywriter Lab</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#94A3B8; margin-bottom:20px;'>Copywriting profesional ala ahli advertising 10 tahun</p>", unsafe_allow_html=True)
    
    # SEO TITLE
    with st.container():
        st.markdown('<div class="generator-card">', unsafe_allow_html=True)
        st.markdown("### 📝 SEO Title")
        p_name = st.text_input("🏷️ Nama Produk", placeholder="Contoh: Kaos Oversize Premium", key="seo_name")
        if st.button("✨ Generate SEO Title", key="gen_seo", use_container_width=True):
            with st.spinner("🧠 AI copywriter sedang merancang judul..."):
                if p_name:
                    prompt = f"""Buat 5 judul produk untuk '{p_name}' dengan formula: [Nama] + [Kategori] + [Atribut] + [Manfaat]. 
Tambahkan emoji di awal. Maksimal 70 karakter. Output 5 judul satu per baris."""
                    res = call_gemini_api(prompt)
                    if res:
                        st.code(res, language="text")
                    else:
                        st.code(f"🔥 {p_name} | Fashion | Premium Quality | Best Seller", language="text")
                else:
                    st.warning("Masukkan nama produk.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # DESKRIPSI
    with st.container():
        st.markdown('<div class="generator-card">', unsafe_allow_html=True)
        st.markdown("### 📄 Deskripsi Produk")
        p_name_desc = st.text_input("🏷️ Nama Produk", placeholder="Contoh: Kaos Oversize Premium", key="desc_name")
        manfaat = st.text_area("Manfaat (pisahkan koma)", placeholder="Contoh: adem, nyaman, tidak panas", key="manfaat_desc")
        if st.button("✨ Generate Deskripsi", key="gen_desc", use_container_width=True):
            with st.spinner("🧠 AI copywriter sedang menulis deskripsi..."):
                if p_name_desc:
                    prompt = f"""Buat deskripsi produk untuk '{p_name_desc}'. Manfaat: {manfaat}. 
Gunakan hook di awal, bullet points, CTA kuat. Maksimal 300 karakter."""
                    res = call_gemini_api(prompt)
                    if res:
                        st.code(res, language="markdown")
                    else:
                        st.code(f"✨ {p_name_desc} - Kualitas Premium!\n✅ {manfaat if manfaat else 'Bahan premium'}", language="markdown")
                else:
                    st.warning("Masukkan nama produk.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # HOOK VIDEO
    with st.container():
        st.markdown('<div class="generator-card">', unsafe_allow_html=True)
        st.markdown("### 🎬 Hook Video")
        p_name_hook = st.text_input("🏷️ Nama Produk", placeholder="Contoh: Kaos Oversize Premium", key="hook_name")
        gaya = st.selectbox("Gaya Hook", ["Problem Solver", "Diskon", "Bukti Sosial", "Curiosity", "Emosional"], key="gaya_hook")
        if st.button("✨ Generate Hook Video", key="gen_hook", use_container_width=True):
            with st.spinner("🧠 AI creative director sedang membuat hook..."):
                if p_name_hook:
                    prompt = f"""Buat 5 hook 3 detik untuk produk '{p_name_hook}' gaya {gaya}. 
Maksimal 10 kata per hook. Output satu per baris."""
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
    
    # HASHTAG
    with st.container():
        st.markdown('<div class="generator-card">', unsafe_allow_html=True)
        st.markdown("### #️⃣ Hashtag Viral")
        p_name_hash = st.text_input("🏷️ Nama Produk", placeholder="Contoh: Kaos Oversize Premium", key="hash_name")
        niche_hash = st.selectbox("Niche", ["Fashion", "Kosmetik", "Makanan", "Elektronik", "Olahraga"], key="niche_hash")
        if st.button("✨ Generate Hashtag Viral", key="gen_hash", use_container_width=True):
            with st.spinner("🧠 AI trend analyst sedang meracik hashtag..."):
                if p_name_hash:
                    prompt = f"""Buat 20 hashtag untuk produk '{p_name_hash}', niche {niche_hash}.
Kombinasi trending, niche, broad, event. Output satu baris dipisah spasi."""
                    res = call_gemini_api(prompt)
                    if res:
                        st.code(res, language="text")
                    else:
                        st.code("#fyp #viral #rekomendasi #shopee #tiktokshop #promo #diskon", language="text")
                else:
                    st.warning("Masukkan nama produk.")
        st.markdown('</div>', unsafe_allow_html=True)

# ==================== HALAMAN DATABASE (TIDAK DIUBAH) ====================
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

# ==================== HALAMAN EXECUTIVE DASHBOARD (BARU) ====================
def render_executive():
    st.markdown('<div class="premium-card"><h3 style="color:#FFD700;">👑 EXECUTIVE DASHBOARD</h3>', unsafe_allow_html=True)
    st.markdown('<p style="color:#94A3B8;">Upload file CSV/Excel untuk analisis massal dan ringkasan eksekutif</p>', unsafe_allow_html=True)
    
    # Download template CSV
    template_df = pd.DataFrame({
        'nama_produk': ['Kaos Premium', 'Jaket Parka'],
        'harga_jual': [150000, 250000],
        'modal': [75000, 120000],
        'admin_persen': [20, 20],
        'impressions': [20000, 15000],
        'clicks': [600, 400],
        'budget_spent': [150000, 120000],
        'sales': [900000, 720000],
        'orders': [8, 6],
        'budget_set': [200000, 180000],
        'target_roas': [6.0, 5.0]
    })
    
    col_template, _ = st.columns([1, 2])
    with col_template:
        csv_template = template_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Template CSV",
            data=csv_template,
            file_name="template_analisis.csv",
            mime="text/csv"
        )
    
    st.markdown("---")
    
    # Upload file
    uploaded_file = st.file_uploader(
        "📁 Upload File CSV atau Excel",
        type=['csv', 'xlsx', 'xls'],
        help="Upload file dengan kolom: nama_produk, impressions, clicks, budget_spent, sales, orders, budget_set, target_roas"
    )
    
    if uploaded_file is not None:
        try:
            # Baca file
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.success(f"✅ File berhasil diupload! {len(df)} produk ditemukan.")
            
            # Preview data
            with st.expander("📋 Preview Data (5 baris pertama)", expanded=False):
                st.dataframe(df.head(), use_container_width=True)
            
            # Tombol analisis
            if st.button("⚡ ANALYZE ALL PRODUCTS", use_container_width=True):
                with st.spinner(f"📊 Menganalisis {len(df)} produk..."):
                    results = []
                    for _, row in df.iterrows():
                        result = analyze_batch_product(row)
                        if result:
                            results.append(result)
                    
                    st.session_state.executive_results = results
                    st.success(f"✅ Analisis selesai! {len(results)} produk berhasil dianalisis.")
                    st.rerun()
            
            # Tampilkan hasil jika ada
            if st.session_state.executive_results:
                results = st.session_state.executive_results
                
                # Kategorisasi produk
                scale_products = [r for r in results if "SIAP SCALE" in r['prioritas']]
                optimasi_products = [r for r in results if "OPTIMASI" in r['prioritas']]
                rugi_products = [r for r in results if "RUGI" in r['prioritas']]
                stop_products = [r for r in results if "STOP" in r['prioritas']]
                
                # ========== RINGKASAN EKSEKUTIF ==========
                st.markdown("---")
                st.markdown("### 📊 RINGKASAN EKSEKUTIF")
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.markdown(f"""
                    <div class="executive-stat">
                        <h3 style="margin:0; color:#00E5A0;">{len(scale_products)}</h3>
                        <p style="margin:0;">🚀 SIAP SCALE</p>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.markdown(f"""
                    <div class="executive-stat">
                        <h3 style="margin:0; color:#F59E0B;">{len(optimasi_products)}</h3>
                        <p style="margin:0;">⚡ OPTIMASI</p>
                    </div>
                    """, unsafe_allow_html=True)
                with col3:
                    st.markdown(f"""
                    <div class="executive-stat">
                        <h3 style="margin:0; color:#EF4444;">{len(rugi_products)}</h3>
                        <p style="margin:0;">🔴 RUGI</p>
                    </div>
                    """, unsafe_allow_html=True)
                with col4:
                    st.markdown(f"""
                    <div class="executive-stat">
                        <h3 style="margin:0; color:#EF4444;">{len(stop_products)}</h3>
                        <p style="margin:0;">🛑 STOP IKLAN</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # ========== TOP 3 SIAP SCALE ==========
                if scale_products:
                    st.markdown("### 🏆 TOP 3 PRODUK SIAP SCALE")
                    for i, prod in enumerate(scale_products[:3]):
                        profit_text = format_rp(prod['profit']) if prod['profit'] > 0 else format_rp(prod['profit'])
                        st.markdown(f"""
                        <div class="executive-card">
                            <strong>{i+1}. {prod['nama_produk']}</strong><br>
                            📈 ROAS: {prod['roas_aktual']:.1f}x ≥ BEP {prod['roas_bep']:.1f}x<br>
                            💰 Profit: {profit_text}<br>
                            💡 Rekomendasi: {prod['rekomendasi']}
                        </div>
                        """, unsafe_allow_html=True)
                
                # ========== PRIORITAS OPTIMASI ==========
                if optimasi_products:
                    st.markdown("### ⚠️ PRIORITAS OPTIMASI")
                    for prod in optimasi_products[:5]:
                        st.markdown(f"""
                        <div class="executive-card" style="border-left-color: #F59E0B;">
                            • <strong>{prod['nama_produk']}</strong><br>
                            ROAS {prod['roas_aktual']:.1f}x ≥ BEP {prod['roas_bep']:.1f}x | Budget terserap {prod['s_rate']:.0f}%<br>
                            💡 {prod['rekomendasi']}
                        </div>
                        """, unsafe_allow_html=True)
                
                # ========== URGENT STOP IKLAN ==========
                if stop_products:
                    st.markdown("### 🔴 URGENT STOP IKLAN")
                    for prod in stop_products:
                        st.markdown(f"""
                        <div class="executive-card" style="border-left-color: #EF4444;">
                            • <strong>{prod['nama_produk']}</strong><br>
                            {prod['clicks']:.0f} klik tapi {prod['orders']:.0f} order | Budget terserap {prod['s_rate']:.0f}%<br>
                            💡 {prod['rekomendasi']}
                        </div>
                        """, unsafe_allow_html=True)
                
                # ========== TOTAL POTENSI PROFIT ==========
                total_profit_scale = sum([p['profit'] for p in scale_products if p['profit'] > 0])
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #064e3b 0%, #0d9488 100%); border-radius: 20px; padding: 25px; text-align: center; margin: 20px 0;">
                    <h3 style="margin:0; color:#FFD700;">💰 TOTAL POTENSI PROFIT (jika scale semua)</h3>
                    <h1 style="font-size: 3rem; margin: 10px 0; color: #00E5A0;">{format_rp(total_profit_scale)} / HARI</h1>
                    <p style="margin:0;">Dari {len(scale_products)} produk yang siap scale</p>
                </div>
                """, unsafe_allow_html=True)
                
                # ========== TABEL DETAIL SEMUA PRODUK ==========
                st.markdown("### 📋 DETAIL SEMUA PRODUK")
                detail_df = pd.DataFrame([{
                    'Nama Produk': r['nama_produk'],
                    'CTR': f"{r['ctr']:.1f}%",
                    'ROAS': f"{r['roas_aktual']:.1f}x",
                    'BEP': f"{r['roas_bep']:.1f}x",
                    'Profit': format_rp(r['profit']),
                    'Rekomendasi': r['prioritas']
                } for r in results])
                st.dataframe(detail_df, use_container_width=True)
                
                # ========== EXPORT HASIL ==========
                export_df = pd.DataFrame([{
                    'nama_produk': r['nama_produk'],
                    'ctr_%': round(r['ctr'], 2),
                    'roas_aktual': round(r['roas_aktual'], 2),
                    'roas_bep': round(r['roas_bep'], 2),
                    'profit': r['profit'],
                    'rekomendasi_prioritas': r['prioritas'],
                    'rekomendasi_text': r['rekomendasi'],
                    'rekomendasi_budget': r['rekom_budget'],
                    'rekomendasi_target_roas': r['rekom_roas']
                } for r in results])
                
                csv_export = export_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Hasil Analisis (CSV)",
                    data=csv_export,
                    file_name=f"hasil_analisis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                
        except Exception as e:
            st.error(f"❌ Gagal membaca file: {e}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== RENDER PAGE ====================
if st.session_state.current_page == "dashboard":
    render_dashboard()
elif st.session_state.current_page == "gmvmax":
    render_gmvmax()
elif st.session_state.current_page == "generator":
    render_generator()
elif st.session_state.current_page == "database":
    render_database()
elif st.session_state.current_page == "executive":
    render_executive()

# ==================== FOOTER ====================
st.markdown("""
<div class="custom-footer">
    <p style="color: #94A3B8; font-size: 0.8rem;">
        Powered by <span style="color: #00E5A0; font-weight: bold;">Arkidigital</span> © 2025
    </p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🚪 LOGOUT", key="logout_footer", use_container_width=True):
        st.session_state.clear()
        st.rerun()
