import streamlit as st
import numpy as np
from datetime import datetime

st.set_page_config(page_title="Ads Doctor Premium - TikTok & Shopee", page_icon="🩺", layout="wide")

# ==================== CUSTOM CSS PREMIUM ====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem 2rem;
        border-radius: 1.5rem;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 20px 35px -10px rgba(0,0,0,0.2);
    }
    
    .logo-container {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .logo-text h1 {
        font-size: 1.8rem;
        margin: 0;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    
    .logo-text p {
        margin: 0;
        opacity: 0.9;
        font-size: 0.85rem;
    }
    
    .premium-card {
        background: white;
        padding: 1.25rem;
        border-radius: 1rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin: 1rem 0;
        transition: all 0.3s ease;
        border: 1px solid rgba(0,0,0,0.05);
    }
    
    .premium-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 28px rgba(0,0,0,0.12);
    }
    
    .metric-premium {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 1rem;
        color: white;
        text-align: center;
        box-shadow: 0 8px 20px rgba(102,126,234,0.3);
    }
    
    .metric-premium h3 {
        font-size: 0.75rem;
        opacity: 0.85;
        margin-bottom: 0.5rem;
        letter-spacing: 0.5px;
    }
    
    .metric-premium h2 {
        font-size: 1.6rem;
        font-weight: 800;
        margin: 0;
    }
    
    .metric-premium p {
        font-size: 0.7rem;
        margin-top: 0.5rem;
        opacity: 0.8;
    }
    
    .danger-card {
        background: linear-gradient(135deg, #f5a5a5 0%, #f5576c 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 1rem;
        margin: 1rem 0;
        box-shadow: 0 8px 20px rgba(245,87,108,0.3);
    }
    
    .warning-card {
        background: linear-gradient(135deg, #f9d976 0%, #f39f86 100%);
        color: #2d2d2d;
        padding: 1.5rem;
        border-radius: 1rem;
        margin: 1rem 0;
        box-shadow: 0 8px 20px rgba(243,159,134,0.3);
    }
    
    .success-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 1rem;
        margin: 1rem 0;
        box-shadow: 0 8px 20px rgba(79,172,254,0.3);
    }
    
    .info-card {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        color: #2d2d2d;
        padding: 1.5rem;
        border-radius: 1rem;
        margin: 1rem 0;
    }
    
    .case-card {
        background: #f8f9ff;
        border-left: 4px solid #667eea;
        padding: 1rem;
        border-radius: 0.75rem;
        margin: 0.5rem 0;
    }
    
    .badge {
        background: rgba(255,255,255,0.2);
        padding: 0.25rem 0.75rem;
        border-radius: 2rem;
        font-size: 0.7rem;
        font-weight: 600;
        display: inline-block;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 0.75rem;
        padding: 0.7rem 1.5rem;
        font-weight: 700;
        width: 100%;
        transition: all 0.3s ease;
        font-size: 0.9rem;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(102,126,234,0.4);
    }
    
    .divider {
        height: 3px;
        background: linear-gradient(90deg, #667eea, #764ba2, #667eea);
        border-radius: 3px;
        margin: 1.5rem 0;
    }
    
    .footer {
        text-align: center;
        color: #888;
        font-size: 0.75rem;
        padding: 2rem 0 1rem 0;
        border-top: 1px solid #eee;
        margin-top: 2rem;
    }
    
    .rupiah {
        font-weight: 700;
        font-family: monospace;
    }
    
    hr {
        margin: 1rem 0;
        opacity: 0.3;
    }
    
    /* Input styling */
    .stNumberInput > div > div > input {
        font-size: 1rem;
        font-weight: 500;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background-color: #f8f9ff;
        padding: 0.5rem;
        border-radius: 1rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 0.75rem;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ==================== HEADER DENGAN LOGO ====================
st.markdown("""
<div class="main-header">
    <div class="logo-container">
        <div style="background: white; border-radius: 1rem; padding: 0.5rem 1rem;">
            <span style="font-size: 2rem;">🩺</span>
        </div>
        <div class="logo-text">
            <h1>Arkidigital</h1>
            <p>Solusi Digital Marketing Terbaik untuk Bisnis Anda</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==================== SIDEBAR - HITUNG ROAS BEP ====================
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/advertising.png", width=70)
    st.markdown("## 🎯 **Hitung ROAS BEP**")
    
    st.markdown("### 📦 Data Produk")
    harga_jual = st.number_input("💰 Harga Jual (Rp)", min_value=1000, value=100000, step=5000)
    modal = st.number_input("🏭 Modal / HPP (Rp)", min_value=500, value=60000, step=5000)
    admin_persen = st.slider("🏪 Admin Marketplace (%)", 5, 30, 20, 1)
    
    # Hitung ROAS BEP
    admin_nominal = harga_jual * (admin_persen / 100)
    laba_kotor = harga_jual - modal - admin_nominal
    roas_bep = harga_jual / laba_kotor if laba_kotor > 0 else 999
    
    st.markdown("---")
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #f0f0ff 0%, #e8e8ff 100%); padding: 1rem; border-radius: 1rem;">
        <small><strong>📊 Perhitungan ROAS BEP:</strong></small><br>
        <small>Harga Jual: <strong>Rp{harga_jual:,.0f}</strong></small><br>
        <small>Modal: <strong>Rp{modal:,.0f}</strong></small><br>
        <small>Admin {admin_persen}%: <strong>Rp{admin_nominal:,.0f}</strong></small><br>
        <small>Laba Kotor: <strong>Rp{laba_kotor:,.0f}</strong></small><br>
        <hr style="margin: 0.5rem 0;">
        <strong>🎯 ROAS BEP = {roas_bep:.1f}x</strong><br>
        <small style="color: #666;">Artinya: Setiap Rp1 iklan → minimal Rp{roas_bep:.1f} omset</small>
    </div>
    """, unsafe_allow_html=True)
    
    # Catatan khusus TikTok
    st.markdown("---")
    st.markdown("""
    <div style="background: #fff3cd; padding: 0.75rem; border-radius: 0.75rem;">
        <small>📱 <strong>Khusus TikTok:</strong><br>
        Set target ROAS <strong>+2 poin</strong> dari BEP<br>
        Contoh: BEP 4 → Target ROAS 6</small>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.caption("💡 **Rumus:** Harga Jual ÷ Laba Kotor")

# ==================== FORM INPUT PREMIUM ====================
st.subheader("📝 **Input Data Iklan**")
st.markdown("Isi data iklan Anda untuk mendapatkan analisis lengkap")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📊 **Data Performa**")
    impressions = st.number_input("👁️ Pengunjung (Impressions)", min_value=0, value=10000, step=1000)
    clicks = st.number_input("🖱️ Klik (Clicks)", min_value=0, value=300, step=50)
    
    st.markdown("### 💰 **Data Anggaran**")
    budget_set = st.number_input("💵 Anggaran Setting (Rp/hari)", min_value=0, value=100000, step=10000)
    budget_spent = st.number_input("💸 Anggaran Terserap (Rp/hari)", min_value=0, value=90000, step=5000)

with col2:
    st.markdown("### 🎯 **Target & Hasil**")
    target_roas = st.number_input("🎯 Target ROAS yang Disetting", min_value=1.0, value=6.0, step=0.5)
    
    st.markdown("### 🛒 **Data Penjualan**")
    sales = st.number_input("💰 Omset / Pendapatan (Rp)", min_value=0, value=600000, step=50000)
    orders = st.number_input("📦 Jumlah Order / Pesanan", min_value=0, value=6, step=1)
    
    # Platform
    platform = st.selectbox("📱 Platform Iklan", ["Shopee", "TikTok"])

# ==================== HITUNG METRIK ====================
if clicks > 0 and impressions > 0:
    ctr = (clicks / impressions * 100)
    cpc = budget_spent / clicks if clicks > 0 else 0
    roas_aktual = sales / budget_spent if budget_spent > 0 else 0
    cpa = budget_spent / orders if orders > 0 else 0
    budget_terserap_persen = (budget_spent / budget_set * 100) if budget_set > 0 else 0
    
    # Hitung profit/loss
    if orders > 0:
        profit_estimasi = (laba_kotor * orders) - budget_spent
        status_profit = "UNTUNG" if profit_estimasi > 0 else "RUGI"
    else:
        profit_estimasi = -budget_spent
        status_profit = "RUGI"
    
    # Rekomendasi target ROAS untuk TikTok
    target_rekomendasi_tiktok = roas_bep + 2
else:
    ctr = 0
    cpc = 0
    roas_aktual = 0
    cpa = 0
    budget_terserap_persen = 0
    profit_estimasi = -budget_spent
    status_profit = "RUGI"
    target_rekomendasi_tiktok = roas_bep + 2

# Format Rupiah
def format_rp(angka):
    if angka >= 1000000000:
        return f"Rp{angka/1000000000:.1f}M"
    elif angka >= 1000000:
        return f"Rp{angka/1000000:.1f}JT"
    elif angka >= 1000:
        return f"Rp{angka/1000:.0f}RB"
    return f"Rp{angka:,.0f}"

def format_rp_full(angka):
    return f"Rp{angka:,.0f}".replace(",", ".")

# ==================== METRIC CARDS PREMIUM ====================
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.subheader("📊 **Dashboard Performa**")

col1, col2, col3, col4 = st.columns(4)

with col1:
    warna_ctr = "✅" if ctr >= 2 else "⚠️"
    st.markdown(f"""
    <div class="metric-premium">
        <h3>📈 CTR (Click Through Rate)</h3>
        <h2>{ctr:.2f}%</h2>
        <p>{warna_ctr} {'Bagus ≥2%' if ctr >= 2 else 'Perlu Perbaikan <2%'}</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    warna_roas = "🟢" if roas_aktual >= roas_bep else "🔴"
    st.markdown(f"""
    <div class="metric-premium">
        <h3>💰 ROAS Aktual</h3>
        <h2>{roas_aktual:.2f}x</h2>
        <p>{warna_roas} BEP: {roas_bep:.1f}x | Target: {target_roas:.1f}x</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-premium">
        <h3>🖱️ CPC (Biaya per Klik)</h3>
        <h2>{format_rp(cpc)}</h2>
        <p>{'✅ Normal ≤Rp3RB' if cpc <= 3000 else '⚠️ Mahal >Rp3RB'}</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    warna_profit = "🟢" if profit_estimasi > 0 else "🔴"
    st.markdown(f"""
    <div class="metric-premium">
        <h3>💎 Estimasi Profit</h3>
        <h2>{format_rp(profit_estimasi)}</h2>
        <p>{warna_profit} {status_profit}</p>
    </div>
    """, unsafe_allow_html=True)

col5, col6, col7, col8 = st.columns(4)

with col5:
    st.markdown(f"""
    <div class="metric-premium">
        <h3>📦 CPA (Biaya per Order)</h3>
        <h2>{format_rp(cpa)}</h2>
        <p>Target aman: {format_rp(laba_kotor)}</p>
    </div>
    """, unsafe_allow_html=True)

with col6:
    st.markdown(f"""
    <div class="metric-premium">
        <h3>🛒 Omset</h3>
        <h2>{format_rp(sales)}</h2>
        <p>Dari {orders} order</p>
    </div>
    """, unsafe_allow_html=True)

with col7:
    warna_budget = "🟢" if budget_terserap_persen > 80 else "🟡" if budget_terserap_persen > 50 else "🔴"
    st.markdown(f"""
    <div class="metric-premium">
        <h3>⏳ Serapan Budget</h3>
        <h2>{budget_terserap_persen:.0f}%</h2>
        <p>{warna_budget} dari {format_rp(budget_set)}</p>
    </div>
    """, unsafe_allow_html=True)

with col8:
    st.markdown(f"""
    <div class="metric-premium">
        <h3>🎯 ROAS BEP</h3>
        <h2>{roas_bep:.1f}x</h2>
        <p>{'🟢' if roas_aktual >= roas_bep else '🔴'} Minimal aman</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ==================== DIAGNOSIS & REKOMENDASI ====================
st.subheader("🩺 **Diagnosis & Rekomendasi**")

# ========== STUDI KASUS 1: IKLAN SEHAT ==========
if ctr >= 2 and roas_aktual >= roas_bep and orders > 0 and clicks > 50:
    st.markdown(f"""
    <div class="success-card">
        <h3>✅ STUDI KASUS 1 — IKLAN NORMAL (SEHAT)</h3>
        <hr style="background: rgba(255,255,255,0.3);">
        <p><strong>📊 DATA:</strong><br>
        Impresi: {impressions:,.0f} | CTR: {ctr:.1f}% → {clicks:.0f} klik<br>
        Conversion rate: {(orders/clicks*100):.1f}% → {orders} order<br>
        Anggaran: {format_rp_full(budget_set)} | Terserap: {format_rp_full(budget_spent)}<br>
        Omset: {format_rp_full(sales)} | ROAS: {roas_aktual:.1f}x</p>
        
        <p><strong>🔍 ANALISA:</strong><br>
        ✅ ROAS ({roas_aktual:.1f}x) > BEP ({roas_bep:.1f}x) → UNTUNG<br>
        ✅ CTR bagus ({ctr:.1f}%) → produk menarik<br>
        ✅ CVR {(orders/clicks*100):.1f}% → normal</p>
        
        <p><strong>🎯 KEPUTUSAN:</strong><br>
        👉 LANJUT & SIAP SCALE — Naikkan budget 30%</p>
    </div>
    """, unsafe_allow_html=True)

# ========== STUDI KASUS 2: KLIK ADA, ORDER 0 ==========
elif clicks > 30 and orders == 0:
    st.markdown(f"""
    <div class="danger-card">
        <h3>🚨 STUDI KASUS 2 — KLIK ADA, TAPI 0 ORDER</h3>
        <hr style="background: rgba(255,255,255,0.3);">
        <p><strong>📊 DATA:</strong><br>
        Impresi: {impressions:,.0f}<br>
        CTR: {ctr:.1f}% → {clicks:.0f} klik<br>
        Order: 0<br>
        Biaya terserap: {format_rp_full(budget_spent)}<br>
        ROAS: 0</p>
        
        <p><strong>🔍 ANALISA:</strong><br>
        ✅ CTR bagus ({ctr:.1f}%) → iklan menarik<br>
        ❌ Tapi 0 order → MASALAH PRODUK</p>
        
        <p><strong>🎯 KEPUTUSAN:</strong><br>
        👉 Perbaiki fondasi produk:<br>
        • Cek harga kompetitor (mungkin terlalu mahal)<br>
        • Tambah review & rating<br>
        • Perbaiki deskripsi (fokus ke manfaat)<br>
        • Tambah video produk<br>
        <strong>⚠️ Klik tinggi ≠ pasti laku!</strong></p>
    </div>
    """, unsafe_allow_html=True)

# ========== STUDI KASUS 3: CTR RENDAH ==========
elif ctr < 2 and clicks > 0:
    st.markdown(f"""
    <div class="warning-card">
        <h3>⚠️ STUDI KASUS 3 — CTR RENDAH</h3>
        <hr style="background: rgba(0,0,0,0.1);">
        <p><strong>📊 DATA:</strong><br>
        Impresi: {impressions:,.0f}<br>
        CTR: {ctr:.1f}% → {clicks:.0f} klik<br>
        Order: {orders}<br>
        Omset: {format_rp_full(sales)}<br>
        ROAS: {roas_aktual:.1f}x</p>
        
        <p><strong>🔍 ANALISA:</strong><br>
        ❌ CTR rendah ({ctr:.1f}% < 2%) → iklan mahal<br>
        {'❌ ROAS < BEP → rugi' if roas_aktual < roas_bep else '✅ ROAS masih aman'}</p>
        
        <p><strong>🎯 KEPUTUSAN:</strong><br>
        👉 Perbaiki foto utama & deskripsi, tambah ulasan<br>
        <strong>💡 Masalah ada di klik, bukan produk</strong></p>
    </div>
    """, unsafe_allow_html=True)

# ========== STUDI KASUS 4: ROAS DI BAWAH BEP ==========
elif roas_aktual < roas_bep and roas_aktual > 0 and orders > 0:
    st.markdown(f"""
    <div class="danger-card">
        <h3>🚨 STUDI KASUS 4 — ROAS DI BAWAH BEP (BONCOS!)</h3>
        <hr style="background: rgba(255,255,255,0.3);">
        <p><strong>📊 DATA:</strong><br>
        Order: {orders}<br>
        Omset: {format_rp_full(sales)}<br>
        Biaya: {format_rp_full(budget_spent)}<br>
        ROAS: {roas_aktual:.1f}x | BEP: {roas_bep:.1f}x</p>
        
        <p><strong>🔍 ANALISA:</strong><br>
        ❌ ROAS ({roas_aktual:.1f}x) < BEP ({roas_bep:.1f}x)<br>
        👉 RUGI (Boncos diam-diam)</p>
        
        <p><strong>🎯 SOLUSI:</strong><br>
        👉 Naikkan target ROAS ke {roas_bep + 0.5:.1f} - {roas_bep + 1:.1f}<br>
        <strong>💡 Jangan lihat order, lihat profit!</strong></p>
    </div>
    """, unsafe_allow_html=True)

# ========== STUDI KASUS 5: IKLAN GAK SPEND ==========
elif budget_terserap_persen < 30 and budget_spent > 0:
    st.markdown(f"""
    <div class="warning-card">
        <h3>⚠️ STUDI KASUS 5 — IKLAN GAK SPEND</h3>
        <hr style="background: rgba(0,0,0,0.1);">
        <p><strong>📊 DATA:</strong><br>
        Budget: {format_rp_full(budget_set)}<br>
        Terpakai: {format_rp_full(budget_spent)} ({budget_terserap_persen:.0f}%)<br>
        Target ROAS setting: {target_roas}x</p>
        
        <p><strong>🔍 ANALISA:</strong><br>
        ❌ Target ROAS ({target_roas}x) terlalu tinggi → sistem ketat</p>
        
        <p><strong>🎯 SOLUSI:</strong><br>
        👉 Turunkan target ROAS ke {target_roas - 1:.1f}<br>
        <strong>💡 Bukan kurang budget, tapi terlalu selektif!</strong></p>
    </div>
    """, unsafe_allow_html=True)

# ========== STUDI KASUS 6: ORDER ADA, PROFIT TIPIS ==========
elif roas_aktual > roas_bep and roas_aktual < roas_bep * 1.2 and orders > 0:
    st.markdown(f"""
    <div class="warning-card">
        <h3>⚠️ STUDI KASUS 6 — ORDER ADA, PROFIT TIPIS</h3>
        <hr style="background: rgba(0,0,0,0.1);">
        <p><strong>📊 DATA:</strong><br>
        Order: {orders}<br>
        Omset: {format_rp_full(sales)}<br>
        Biaya: {format_rp_full(budget_spent)}<br>
        ROAS: {roas_aktual:.1f}x (BEP: {roas_bep:.1f}x)</p>
        
        <p><strong>🔍 ANALISA:</strong><br>
        ✅ ROAS sedikit di atas BEP → untung tipis<br>
        ⚠️ Untung tipis = rawan turun</p>
        
        <p><strong>🎯 SOLUSI:</strong><br>
        👉 Naikkan target ROAS ke {roas_bep + 1:.1f}<br>
        <strong>💡 Amankan profit sebelum scale!</strong></p>
    </div>
    """, unsafe_allow_html=True)

# ========== STUDI KASUS 7: SCALE BERHASIL ==========
elif roas_aktual >= roas_bep * 1.5 and roas_aktual > 0 and orders > 0:
    st.markdown(f"""
    <div class="success-card">
        <h3>🏆 STUDI KASUS 7 — SIAP SCALE!</h3>
        <hr style="background: rgba(255,255,255,0.3);">
        <p><strong>📊 DATA:</strong><br>
        ROAS: {roas_aktual:.1f}x | Stabil<br>
        Budget saat ini: {format_rp_full(budget_set)}</p>
        
        <p><strong>🔍 ANALISA:</strong><br>
        🏆 ROAS {roas_aktual:.1f}x > {roas_bep * 1.5:.0f}x (1.5x BEP)<br>
        ✅ Performa sangat bagus, siap scale</p>
        
        <p><strong>🎯 KEPUTUSAN:</strong><br>
        👉 Naikkan budget menjadi {format_rp_full(budget_set * 1.3)}<br>
        👉 Target ROAS bisa dipertahankan atau naikkan ke {target_roas + 0.5:.1f}<br>
        <strong>🚀 LANJUT SCALE UP SAMPAI SETERUSNYA</strong></p>
    </div>
    """, unsafe_allow_html=True)

# ========== STUDI KASUS 8: SCALE GAGAL (deteksi dari data) ==========
elif budget_set > 100000 and roas_aktual < roas_bep and orders > 0:
    st.markdown(f"""
    <div class="danger-card">
        <h3>🚨 STUDI KASUS 8 — SCALE GAGAL</h3>
        <hr style="background: rgba(255,255,255,0.3);">
        <p><strong>📊 DATA:</strong><br>
        Budget: {format_rp_full(budget_set)}<br>
        ROAS turun: {roas_aktual:.1f}x (target BEP: {roas_bep:.1f}x)</p>
        
        <p><strong>🔍 ANALISA:</strong><br>
        ❌ Terlalu agresif scale</p>
        
        <p><strong>🎯 SOLUSI:</strong><br>
        👉 Kembalikan ke setting awal (budget lebih kecil)<br>
        <strong>💡 Scale bertahap: naikkan ROAS dulu, baru budget!</strong></p>
    </div>
    """, unsafe_allow_html=True)

# ========== STUDI KASUS 9: IKLAN DROP ==========
else:
    st.markdown(f"""
    <div class="info-card">
        <h3>📉 STUDI KASUS 9 — CEK KONSISTENSI</h3>
        <hr style="background: rgba(0,0,0,0.1);">
        <p><strong>📊 DATA SAAT INI:</strong><br>
        CTR: {ctr:.1f}% | ROAS: {roas_aktual:.1f}x | Order: {orders}</p>
        
        <p><strong>🔍 ANALISA:</strong><br>
        {'✅ Data masih normal, pantau 3-5 hari' if roas_aktual >= roas_bep else '⚠️ ROAS di bawah BEP, perlu evaluasi'}</p>
        
        <p><strong>🎯 REKOMENDASI:</strong><br>
        👉 {'Jangan panik, tunggu 2-3 hari, bisa jadi sistem recalibrate' if roas_aktual >= roas_bep else 'Evaluasi setting ROAS atau perbaiki produk'}<br>
        <strong>💡 Iklan naik turun itu normal!</strong></p>
    </div>
    """, unsafe_allow_html=True)

# ==================== REKOMENDASI SETTING ====================
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.subheader("🎯 **Rekomendasi Setting Ulang**")

col_rec1, col_rec2, col_rec3 = st.columns(3)

with col_rec1:
    st.markdown("### 🎯 Target ROAS")
    if platform == "TikTok":
        st.success(f"""
        **Khusus TikTok:**\n
        BEP: {roas_bep:.1f}x\n
        👉 Setting awal: **{roas_bep + 2:.1f}x**\n
        (Naikkan 2 poin dari BEP)
        """)
    elif budget_terserap_persen < 50:
        st.success(f"🔻 **Turunkan** menjadi: {target_roas - 1:.1f} - {target_roas - 0.5:.1f}")
    elif roas_aktual < roas_bep:
        st.success(f"🔺 **Naikkan** menjadi: {roas_bep + 0.5:.1f} - {roas_bep + 1:.1f}")
    elif roas_aktual > roas_bep * 1.5:
        st.success(f"✅ **Pertahankan atau naikkan** ke: {target_roas + 0.5:.1f}")
    else:
        st.info(f"⏸️ **Pertahankan** di: {target_roas:.1f}")

with col_rec2:
    st.markdown("### 💰 Budget Harian")
    if roas_aktual > roas_bep * 1.5:
        st.success(f"🚀 **Naikkan** menjadi: {format_rp_full(budget_set * 1.4)}")
    elif budget_terserap_persen < 50:
        st.warning(f"🔻 **Turunkan sementara** atau longgarkan ROAS")
    elif roas_aktual < roas_bep:
        st.warning(f"🔻 **Turunkan 50%** menjadi: {format_rp_full(budget_set * 0.5)}")
    else:
        st.info(f"⏸️ **Pertahankan** di: {format_rp_full(budget_set)}")

with col_rec3:
    st.markdown("### 📋 Prioritas")
    if roas_aktual < roas_bep and orders == 0:
        st.error("🔴 **URGENT** - Perbaiki produk")
    elif ctr < 2:
        st.warning("🟡 **OPTIMASI** - Ganti visual")
    elif roas_aktual > roas_bep * 1.5:
        st.success("🚀 **SCALE** - Naikkan budget")
    else:
        st.info("🟢 **PANTAU** - Evaluasi 3-5 hari")

# ==================== TIKTOK KHUSUS ====================
if platform == "TikTok":
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.subheader("📱 **Khusus TikTok Ads**")
    st.markdown(f"""
    <div class="info-card">
        <h3>🎯 Strategi Setting ROAS untuk TikTok</h3>
        <p><strong>Rumus:</strong> Target ROAS Awal = ROAS BEP + 2 poin</p>
        <p>Contoh: ROAS BEP = {roas_bep:.1f}x → Setting target ROAS = <strong>{roas_bep + 2:.1f}x</strong></p>
        <p><strong>Kenapa?</strong> TikTok punya algoritma berbeda, perlu ruang napas lebih.</p>
        <p><strong>Evaluasi:</strong> Jalankan 3-5 hari, lihat data aktual, baru adjust.</p>
    </div>
    """, unsafe_allow_html=True)

# ==================== RINGKASAN TABEL ====================
with st.expander("📋 **Lihat Detail Perhitungan Lengkap**"):
    st.markdown(f"""
    | Metrik | Nilai | Status |
    |--------|-------|--------|
    | CTR | {ctr:.2f}% | {'✅ Bagus (≥2%)' if ctr >= 2 else '⚠️ Perlu perbaikan (<2%)'} |
    | ROAS Aktual | {roas_aktual:.2f}x | {'✅ UNTUNG' if roas_aktual >= roas_bep else '🔴 RUGI'} |
    | ROAS BEP | {roas_bep:.1f}x | Minimal aman |
    | Target ROAS Setting | {target_roas:.1f}x | {'✅ On track' if roas_aktual >= target_roas else '⚠️ Di bawah target'} |
    | CPC | {format_rp_full(cpc)} | {'✅ Normal (≤Rp3RB)' if cpc <= 3000 else '⚠️ Mahal (>Rp3RB)'} |
    | CPA | {format_rp_full(cpa)} | Target aman: {format_rp_full(laba_kotor)} |
    | Budget Setting | {format_rp_full(budget_set)} | Per hari |
    | Budget Terserap | {format_rp_full(budget_spent)} ({budget_terserap_persen:.0f}%) | {'✅ Habis' if budget_terserap_persen > 80 else '⚠️ Kurang'} |
    | Omset | {format_rp_full(sales)} | Dari iklan |
    | Order | {orders} pesanan | {'✅ Ada order' if orders > 0 else '⚠️ Tidak ada order'} |
    | Laba Kotor per Produk | {format_rp_full(laba_kotor)} | Harga Jual - Modal - Admin |
    | Estimasi Profit | {format_rp_full(profit_estimasi)} | {status_profit} |
    """)

# ==================== PANDUAN LENGKAP ====================
with st.expander("📖 **Panduan Lengkap 10 Studi Kasus**"):
    st.markdown("""
    ### 🎯 Ringkasan 10 Studi Kasus GMV Max
    
    | Kasus | Masalah | Ciri-ciri | Solusi |
    |-------|---------|-----------|--------|
    | 1 | Iklan Sehat | ROAS > BEP, CTR > 2% | Scale naikkan budget 30% |
    | 2 | Klik ada, order 0 | Clicks >50, orders=0 | Perbaiki produk (harga/review) |
    | 3 | CTR Rendah | CTR < 2% | Ganti visual (foto/video hook) |
    | 4 | ROAS di bawah BEP | ROAS < BEP | Naikkan target ROAS |
    | 5 | Iklan gak spend | Budget terserap <30% | Turunkan target ROAS |
    | 6 | Profit tipis | ROAS = BEP + sedikit | Naikkan target ROAS |
    | 7 | Scale berhasil | ROAS stabil, order naik | Lanjut scale bertahap |
    | 8 | Scale gagal | Budget naik, ROAS turun drastis | Kembali ke setting awal |
    | 9 | Iklan drop | ROAS turun 1-3 hari | Tunggu 2-3 hari, jangan panik |
    | 10 | Produk salah | CTR <2%, ROAS <3 terus | Ganti produk |
    
    ### 🔥 Rumus Cepat (WAJIB DIINGAT)
    
    - **CTR < 2%** → Masalah visual (ganti kreatif)
    - **Klik ada, order 0** → Masalah produk (bukan iklan!)
    - **ROAS < BEP** → Rugi (naikkan target ROAS atau stop)
    - **Budget gak habis** → ROAS terlalu ketat (turunkan)
    - **ROAS > BEP × 1.5** → Siap scale (naikkan budget 30%)
    
    ### 💰 Cara Hitung ROAS BEP (Sudah Otomatis di Aplikasi)
    
    ```
    Rumus: ROAS BEP = Harga Jual ÷ (Harga Jual - Modal - Admin)
    
    Contoh:
    Harga Jual = Rp100.000
    Modal = Rp60.000
    Admin 20% = Rp20.000
    Laba Kotor = Rp20.000
    
    ROAS BEP = 100.000 ÷ 20.000 = 5x
    ```
    
    **Artinya:** Setiap Rp1 iklan harus menghasilkan minimal Rp5 penjualan agar tidak rugi.
    
    ### 📱 Khusus TikTok
    
    Setting target ROAS awal = ROAS BEP + 2 poin
    Contoh: BEP 5 → Setting target ROAS 7
    """)

# ==================== FOOTER ====================
st.markdown("---")
st.markdown(f"""
<div class="footer">
    <p>🩺 <strong>Ads Doctor Premium</strong> | Framework GMV Max Shopee & TikTok</p>
    <p>📅 Analisis: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} | Platform: {platform}</p>
    <p style="font-size: 0.7rem;">© 2024 Arkidigital - Solusi Digital Marketing Terbaik untuk Bisnis Anda</p>
</div>
""", unsafe_allow_html=True)
