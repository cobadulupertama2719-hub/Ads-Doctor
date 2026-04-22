import streamlit as st
import hashlib
import hmac
from datetime import datetime

# ==================== KONFIGURASI AKSES ====================
# Ganti password ini dengan yang Mas mau!
ADMIN_USERNAME = "arkidigital"
ADMIN_PASSWORD = "GMVMAX"  # Ganti dengan password Mas sendiri

# Fungsi verifikasi password
def check_password():
    """Mengembalikan True jika user sudah login"""
    
    def login_form():
        with st.form("Login"):
            st.markdown("""
            <div style="text-align: center; padding: 2rem;">
                <h1>🩺 Ads Doctor Premium</h1>
                <p>Silakan login untuk mengakses aplikasi</p>
            </div>
            """, unsafe_allow_html=True)
            
            username = st.text_input("📧 Username", placeholder="Masukkan username")
            password = st.text_input("🔒 Password", type="password", placeholder="Masukkan password")
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                submitted = st.form_submit_button("🔓 Login", use_container_width=True)
            
            if submitted:
                if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                    st.session_state["authenticated"] = True
                    st.rerun()
                else:
                    st.error("❌ Username atau password salah!")
    
    # Cek session state
    if st.session_state.get("authenticated", False):
        return True
    
    # Tampilkan form login
    login_form()
    return False

# ==================== CUSTOM CSS PREMIUM ====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.2rem 2rem;
        border-radius: 1rem;
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 25px -10px rgba(0,0,0,0.2);
    }
    
    .logo-container {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .logo-text h1 {
        font-size: 1.5rem;
        margin: 0;
        font-weight: 700;
    }
    
    .logo-text p {
        margin: 0;
        opacity: 0.85;
        font-size: 0.75rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0.8rem;
        border-radius: 0.8rem;
        color: white;
        text-align: center;
    }
    
    .metric-card h3 {
        font-size: 0.7rem;
        opacity: 0.85;
        margin-bottom: 0.3rem;
    }
    
    .metric-card h2 {
        font-size: 1.3rem;
        font-weight: 700;
        margin: 0;
    }
    
    .metric-card p {
        font-size: 0.65rem;
        margin-top: 0.3rem;
        opacity: 0.8;
    }
    
    .logout-btn {
        position: fixed;
        top: 1rem;
        right: 1rem;
        z-index: 999;
    }
    
    .divider {
        height: 2px;
        background: linear-gradient(90deg, #667eea, #764ba2, #667eea);
        border-radius: 2px;
        margin: 1.2rem 0;
    }
    
    .footer {
        text-align: center;
        color: #888;
        font-size: 0.7rem;
        padding: 1.5rem 0 0.5rem 0;
        border-top: 1px solid #eee;
        margin-top: 1.5rem;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        font-weight: 600;
        width: 100%;
    }
    
    .badge-success {
        background: #d1fae5;
        color: #059669;
        padding: 0.2rem 0.6rem;
        border-radius: 2rem;
        font-size: 0.7rem;
        font-weight: 600;
        display: inline-block;
    }
    
    .badge-danger {
        background: #fee2e2;
        color: #dc2626;
        padding: 0.2rem 0.6rem;
        border-radius: 2rem;
        font-size: 0.7rem;
        font-weight: 600;
        display: inline-block;
    }
    
    .badge-warning {
        background: #fef3c7;
        color: #d97706;
        padding: 0.2rem 0.6rem;
        border-radius: 2rem;
        font-size: 0.7rem;
        font-weight: 600;
        display: inline-block;
    }
    
    .badge-info {
        background: #dbeafe;
        color: #2563eb;
        padding: 0.2rem 0.6rem;
        border-radius: 2rem;
        font-size: 0.7rem;
        font-weight: 600;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# ==================== CEK AUTHENTIKASI ====================
if not check_password():
    st.stop()

# ==================== TAMPILAN UTAMA (SETELAH LOGIN) ====================

# Tombol Logout di pojok kanan
with st.container():
    col_logout1, col_logout2, col_logout3 = st.columns([6, 1, 1])
    with col_logout3:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state["authenticated"] = False
            st.rerun()

# Header
st.markdown("""
<div class="main-header">
    <div class="logo-container">
        <div style="background: white; border-radius: 0.8rem; padding: 0.3rem 0.8rem;">
            <span style="font-size: 1.5rem;">🩺</span>
        </div>
        <div class="logo-text">
            <h1>Arkidigital</h1>
            <p>Solusi Digital Marketing Terbaik untuk Bisnis Anda</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("## 🎯 **Hitung ROAS BEP**")
    
    harga_jual = st.number_input("💰 Harga Jual (Rp)", min_value=1000, value=100000, step=5000)
    modal = st.number_input("🏭 Modal / HPP (Rp)", min_value=500, value=60000, step=5000)
    admin_persen = st.slider("🏪 Admin Marketplace (%)", 5, 30, 20, 1)
    
    admin_nominal = harga_jual * (admin_persen / 100)
    laba_kotor = harga_jual - modal - admin_nominal
    roas_bep = harga_jual / laba_kotor if laba_kotor > 0 else 999
    
    st.markdown("---")
    st.markdown(f"""
    <div style="background: #f0f0ff; padding: 0.8rem; border-radius: 0.8rem;">
        <small><strong>📊 ROAS BEP = {roas_bep:.1f}x</strong></small><br>
        <small>Laba kotor: Rp{laba_kotor:,.0f}</small>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
    <div style="background: #fff3cd; padding: 0.6rem; border-radius: 0.6rem;">
        <small>📱 <strong>TikTok:</strong> Target awal = BEP + 2 poin</small>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.caption(f"👤 Login sebagai: **{ADMIN_USERNAME}**")

# ==================== INPUT DATA ====================
st.subheader("📝 **Input Data Iklan**")

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

# ==================== HITUNG METRIK ====================
if clicks > 0 and impressions > 0:
    ctr = (clicks / impressions * 100)
    cpc = budget_spent / clicks if clicks > 0 else 0
    roas_aktual = sales / budget_spent if budget_spent > 0 else 0
    cpa = budget_spent / orders if orders > 0 else 0
    budget_terserap_persen = (budget_spent / budget_set * 100) if budget_set > 0 else 0
    
    if orders > 0:
        profit_estimasi = (laba_kotor * orders) - budget_spent
        status_profit = "UNTUNG" if profit_estimasi > 0 else "RUGI"
    else:
        profit_estimasi = -budget_spent
        status_profit = "RUGI"
else:
    ctr = 0
    cpc = 0
    roas_aktual = 0
    cpa = 0
    budget_terserap_persen = 0
    profit_estimasi = -budget_spent
    status_profit = "RUGI"

def format_rp(angka):
    if angka >= 1000000:
        return f"Rp{angka/1000000:.1f}JT"
    elif angka >= 1000:
        return f"Rp{angka/1000:.0f}RB"
    return f"Rp{angka:,.0f}"

# ==================== METRIC CARDS ====================
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <h3>📈 CTR</h3>
        <h2>{ctr:.1f}%</h2>
        <p>{'✅ Bagus' if ctr >= 2 else '⚠️ Perlu perbaikan'}</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <h3>💰 ROAS Aktual</h3>
        <h2>{roas_aktual:.1f}x</h2>
        <p>BEP: {roas_bep:.1f}x</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <h3>💸 Budget Terserap</h3>
        <h2>{budget_terserap_persen:.0f}%</h2>
        <p>Dari {format_rp(budget_set)}</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <h3>💎 Profit Estimasi</h3>
        <h2>{format_rp(profit_estimasi)}</h2>
        <p>{status_profit}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ==================== DIAGNOSIS (TABEL SEDERHANA) ====================
st.subheader("🩺 **Diagnosis & Kesimpulan**")

# Tabel Diagnosis
st.markdown("""
<div style="background: white; border-radius: 1rem; border: 1px solid #e5e7eb; overflow: hidden;">
    <div style="background: #f9fafb; padding: 0.75rem 1rem; border-bottom: 1px solid #e5e7eb;">
        <b>📋 Diagnostik Performa Iklan</b>
    </div>
""", unsafe_allow_html=True)

# Baris 1: CTR
if ctr >= 2:
    ctr_status = '<span class="badge-success">✅ BAGUS</span>'
    ctr_ket = "CTR di atas 2%, visual menarik"
else:
    ctr_status = '<span class="badge-danger">⚠️ RENDAH</span>'
    ctr_ket = "CTR di bawah 2%, perlu ganti visual"

st.markdown(f"""
<div style="display: flex; padding: 0.6rem 1rem; border-bottom: 1px solid #f0f0f0;">
    <div style="width: 35%; font-weight: 500;">📊 CTR</div>
    <div style="width: 65%;">{ctr:.1f}% {ctr_status}<br><small style="color: #666;">{ctr_ket}</small></div>
</div>
""", unsafe_allow_html=True)

# Baris 2: ROAS
if roas_aktual >= roas_bep:
    roas_status = '<span class="badge-success">✅ PROFIT</span>'
    roas_ket = f"ROAS {roas_aktual:.1f}x > BEP {roas_bep:.1f}x, iklan untung"
else:
    roas_status = '<span class="badge-danger">🔴 RUGI</span>'
    roas_ket = f"ROAS {roas_aktual:.1f}x < BEP {roas_bep:.1f}x, iklan boncos"

st.markdown(f"""
<div style="display: flex; padding: 0.6rem 1rem; border-bottom: 1px solid #f0f0f0;">
    <div style="width: 35%; font-weight: 500;">💰 ROAS</div>
    <div style="width: 65%;">{roas_aktual:.1f}x {roas_status}<br><small style="color: #666;">{roas_ket}</small></div>
</div>
""", unsafe_allow_html=True)

# Baris 3: Budget Serapan
if budget_terserap_persen >= 90:
    budget_status = '<span class="badge-success">✅ HABIS</span>'
    budget_ket = f"Budget terserap {budget_terserap_persen:.0f}%, sistem bekerja optimal"
elif budget_terserap_persen >= 50:
    budget_status = '<span class="badge-warning">🟡 KURANG</span>'
    budget_ket = f"Budget hanya terserap {budget_terserap_persen:.0f}%, target ROAS terlalu ketat"
else:
    budget_status = '<span class="badge-danger">🔴 SEDIKIT</span>'
    budget_ket = f"Budget terserap {budget_terserap_persen:.0f}%, target ROAS terlalu tinggi"

st.markdown(f"""
<div style="display: flex; padding: 0.6rem 1rem; border-bottom: 1px solid #f0f0f0;">
    <div style="width: 35%; font-weight: 500;">⏳ Budget Terserap</div>
    <div style="width: 65%;">{budget_terserap_persen:.0f}% {budget_status}<br><small style="color: #666;">{budget_ket}</small></div>
</div>
""", unsafe_allow_html=True)

# Baris 4: Konversi
if clicks > 50 and orders == 0:
    konversi_status = '<span class="badge-danger">🔴 MASALAH</span>'
    konversi_ket = f"{clicks:.0f} klik tapi 0 order → masalah di produk (harga/review/deskripsi)"
elif orders > 0:
    cvr = (orders / clicks * 100) if clicks > 0 else 0
    if cvr >= 2:
        konversi_status = '<span class="badge-success">✅ BAGUS</span>'
        konversi_ket = f"CVR {cvr:.1f}% normal, produk meyakinkan"
    else:
        konversi_status = '<span class="badge-warning">🟡 RENDAH</span>'
        konversi_ket = f"CVR {cvr:.1f}% < 2%, perlu optimasi landing page"
else:
    konversi_status = '<span class="badge-info">⏸️ TIDAK ADA</span>'
    konversi_ket = "Belum ada order, evaluasi produk"

st.markdown(f"""
<div style="display: flex; padding: 0.6rem 1rem; border-bottom: 1px solid #f0f0f0;">
    <div style="width: 35%; font-weight: 500;">🛒 Konversi (Klik → Order)</div>
    <div style="width: 65%;">{orders} order dari {clicks} klik {konversi_status}<br><small style="color: #666;">{konversi_ket}</small></div>
</div>
""", unsafe_allow_html=True)

# Baris 5: CPC
if cpc <= 3000:
    cpc_status = '<span class="badge-success">✅ NORMAL</span>'
    cpc_ket = f"CPC {format_rp(cpc)} ≤ Rp3RB, efisien"
else:
    cpc_status = '<span class="badge-warning">⚠️ MAHAL</span>'
    cpc_ket = f"CPC {format_rp(cpc)} > Rp3RB, perlu perbaiki relevansi"

st.markdown(f"""
<div style="display: flex; padding: 0.6rem 1rem;">
    <div style="width: 35%; font-weight: 500;">🖱️ CPC</div>
    <div style="width: 65%;">{format_rp(cpc)} {cpc_status}<br><small style="color: #666;">{cpc_ket}</small></div>
</div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ==================== KESIMPULAN & REKOMENDASI ====================
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.subheader("🎯 **Kesimpulan & Rekomendasi**")

# LOGIKA REKOMENDASI
rekomendasi_budget = budget_set
tindakan = ""
prioritas = ""

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

if warna == "danger":
    st.markdown(f"""
    <div style="background: #fee2e2; border-radius: 1rem; padding: 1rem; border-left: 4px solid #dc2626;">
        <h4 style="margin: 0 0 0.5rem 0;">{prioritas}</h4>
        <p style="margin: 0;"><strong>📌 Tindakan:</strong> {tindakan}</p>
        <p style="margin: 0.5rem 0 0 0;"><strong>💰 Rekomendasi Budget:</strong> {format_rp(rekomendasi_budget)}</p>
    </div>
    """, unsafe_allow_html=True)
elif warna == "warning":
    st.markdown(f"""
    <div style="background: #fef3c7; border-radius: 1rem; padding: 1rem; border-left: 4px solid #f59e0b;">
        <h4 style="margin: 0 0 0.5rem 0;">{prioritas}</h4>
        <p style="margin: 0;"><strong>📌 Tindakan:</strong> {tindakan}</p>
        <p style="margin: 0.5rem 0 0 0;"><strong>💰 Rekomendasi Budget:</strong> {format_rp(rekomendasi_budget)}</p>
    </div>
    """, unsafe_allow_html=True)
elif warna == "success":
    st.markdown(f"""
    <div style="background: #d1fae5; border-radius: 1rem; padding: 1rem; border-left: 4px solid #10b981;">
        <h4 style="margin: 0 0 0.5rem 0;">{prioritas}</h4>
        <p style="margin: 0;"><strong>📌 Tindakan:</strong> {tindakan}</p>
        <p style="margin: 0.5rem 0 0 0;"><strong>💰 Rekomendasi Budget:</strong> {format_rp(rekomendasi_budget)}</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div style="background: #dbeafe; border-radius: 1rem; padding: 1rem; border-left: 4px solid #3b82f6;">
        <h4 style="margin: 0 0 0.5rem 0;">{prioritas}</h4>
        <p style="margin: 0;"><strong>📌 Tindakan:</strong> {tindakan}</p>
        <p style="margin: 0.5rem 0 0 0;"><strong>💰 Rekomendasi Budget:</strong> {format_rp(rekomendasi_budget)}</p>
    </div>
    """, unsafe_allow_html=True)

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
    <p>🩺 <strong>Ads Doctor Premium</strong> | Framework GMV Max | {platform}</p>
    <p>© 2024 Arkidigital - Solusi Digital Marketing Terbaik untuk Bisnis Anda</p>
</div>
""", unsafe_allow_html=True)
