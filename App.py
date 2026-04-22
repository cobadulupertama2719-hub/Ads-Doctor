import streamlit as st
import numpy as np
from datetime import datetime

st.set_page_config(page_title="Ads Doctor Premium", page_icon="🩺", layout="wide")

# ==================== CUSTOM CSS PREMIUM ====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    
    .premium-card {
        background: white;
        padding: 1.25rem;
        border-radius: 1rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin: 1rem 0;
        transition: transform 0.2s;
    }
    
    .premium-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.12);
    }
    
    .metric-premium {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 0.75rem;
        color: white;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    
    .metric-premium h3 {
        font-size: 0.85rem;
        opacity: 0.9;
        margin-bottom: 0.5rem;
    }
    
    .metric-premium h2 {
        font-size: 1.75rem;
        font-weight: 700;
        margin: 0;
    }
    
    .danger-card {
        background: linear-gradient(135deg, #f5a5a5 0%, #f5576c 100%);
        color: white;
        padding: 1.25rem;
        border-radius: 1rem;
        margin: 1rem 0;
    }
    
    .warning-card {
        background: linear-gradient(135deg, #f9d976 0%, #f39f86 100%);
        color: #333;
        padding: 1.25rem;
        border-radius: 1rem;
        margin: 1rem 0;
    }
    
    .success-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 1.25rem;
        border-radius: 1rem;
        margin: 1rem 0;
    }
    
    .info-card {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        color: #333;
        padding: 1.25rem;
        border-radius: 1rem;
        margin: 1rem 0;
    }
    
    .badge {
        background: rgba(255,255,255,0.2);
        padding: 0.25rem 0.75rem;
        border-radius: 2rem;
        font-size: 0.75rem;
        display: inline-block;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    hr {
        margin: 1.5rem 0;
    }
    
    .divider {
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2, #667eea);
        border-radius: 2px;
        margin: 1.5rem 0;
    }
    
    .footer {
        text-align: center;
        color: #888;
        font-size: 0.8rem;
        padding: 2rem 0 1rem 0;
    }
    
    /* Rupiah formatting */
    .rupiah {
        font-family: monospace;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ==================== HEADER ====================
st.markdown("""
<div class="main-header">
    <h1>🩺 Ads Doctor Premium</h1>
    <p>Analisa Iklan TikTok & Shopee → Rekomendasi Perbaikan + Perhitungan Profit</p>
    <span class="badge">PREMIUM V3.0</span>
</div>
""", unsafe_allow_html=True)

# ==================== SIDEBAR ====================
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/advertising.png", width=70)
    st.markdown("## ⚙️ **Data Produk**")
    
    # Input harga produk
    st.markdown("### 📦 Hitung ROAS BEP")
    harga_jual = st.number_input("💰 Harga Jual Produk (Rp)", min_value=1000, value=100000, step=5000)
    modal = st.number_input("🏭 Modal / HPP (Rp)", min_value=500, value=60000, step=5000)
    
    # Admin marketplace (default 20%)
    admin_persen = st.slider("🏪 Admin Marketplace (%)", 5, 30, 20, 1)
    
    # Hitung ROAS BEP otomatis
    admin_nominal = harga_jual * (admin_persen / 100)
    laba_kotor = harga_jual - modal - admin_nominal
    roas_bep = harga_jual / laba_kotor if laba_kotor > 0 else 999
    
    st.markdown("---")
    st.markdown(f"""
    <div style="background: #f0f0f0; padding: 0.75rem; border-radius: 0.5rem;">
        <small>📊 <strong>Perhitungan:</strong><br>
        Harga Jual: Rp{harga_jual:,.0f}<br>
        Modal: Rp{modal:,.0f}<br>
        Admin {admin_persen}%: Rp{admin_nominal:,.0f}<br>
        <strong>Laba Kotor: Rp{laba_kotor:,.0f}</strong><br>
        <strong>🎯 ROAS BEP = {roas_bep:.1f}x</strong>
        </small>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.caption("💡 **Rumus ROAS BEP:**")
    st.caption(f"Harga Jual ÷ Laba Kotor = {harga_jual:,} ÷ {laba_kotor:,} = {roas_bep:.1f}x")
    st.caption("Artinya: Setiap Rp1 iklan harus menghasilkan minimal Rp{roas_bep:.1f} penjualan agar tidak rugi")

# ==================== FORM INPUT PREMIUM ====================
st.subheader("📝 **Input Data Iklan Hari Ini**")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📊 **Data Performa**")
    impressions = st.number_input("👁️ Pengunjung (Impressions)", min_value=0, value=10000, step=1000, help="Berapa kali iklan ditampilkan")
    clicks = st.number_input("🖱️ Klik (Clicks)", min_value=0, value=300, step=50, help="Berapa kali iklan diklik")
    
    st.markdown("### 💰 **Data Anggaran**")
    budget_set = st.number_input("💵 Anggaran Setting (Rp/hari)", min_value=0, value=100000, step=10000, help="Budget yang Anda pasang")
    budget_spent = st.number_input("💸 Anggaran Terserap (Rp/hari)", min_value=0, value=90000, step=5000, help="Budget yang terpakai hari ini")

with col2:
    st.markdown("### 🎯 **Target & Hasil**")
    target_roas = st.number_input("🎯 Target ROAS yang Disetting", min_value=1.0, value=6.0, step=0.5, help="Target yang Anda pasang di iklan")
    
    st.markdown("### 🛒 **Data Penjualan**")
    sales = st.number_input("💰 Omset / Pendapatan (Rp)", min_value=0, value=600000, step=50000, help="Total penjualan dari iklan")
    orders = st.number_input("📦 Jumlah Order / Pesanan", min_value=0, value=6, step=1, help="Total pesanan dari iklan")

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
else:
    ctr = 0
    cpc = 0
    roas_aktual = 0
    cpa = 0
    budget_terserap_persen = 0
    profit_estimasi = -budget_spent
    status_profit = "RUGI"

# Format Rupiah
def format_rp(angka):
    return f"Rp{angka:,.0f}".replace(",", ".")

# ==================== METRIC CARDS PREMIUM ====================
st.markdown("---")
st.subheader("📊 **Dashboard Performa**")

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    warna_ctr = "✅" if ctr >= 2 else "⚠️"
    st.markdown(f"""
    <div class="metric-premium">
        <h3>📈 CTR</h3>
        <h2>{ctr:.2f}%</h2>
        <small>{warna_ctr} {'Bagus' if ctr >= 2 else 'Perlu Perbaikan'}</small>
    </div>
    """, unsafe_allow_html=True)

with col2:
    warna_roas = "🟢" if roas_aktual >= roas_bep else "🔴"
    st.markdown(f"""
    <div class="metric-premium">
        <h3>💰 ROAS</h3>
        <h2>{roas_aktual:.2f}x</h2>
        <small>{warna_roas} BEP: {roas_bep:.1f}x | Target: {target_roas:.1f}x</small>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-premium">
        <h3>🖱️ CPC</h3>
        <h2>{format_rp(cpc)}</h2>
        <small>{'✅ Normal' if cpc <= 3000 else '⚠️ Mahal'}</small>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-premium">
        <h3>📦 CPA</h3>
        <h2>{format_rp(cpa)}</h2>
        <small>Biaya per Order</small>
    </div>
    """, unsafe_allow_html=True)

with col5:
    warna_profit = "🟢" if profit_estimasi > 0 else "🔴"
    st.markdown(f"""
    <div class="metric-premium">
        <h3>💎 Estimasi Profit</h3>
        <h2>{format_rp(profit_estimasi)}</h2>
        <small>{warna_profit} {status_profit}</small>
    </div>
    """, unsafe_allow_html=True)

with col6:
    warna_budget = "🟢" if budget_terserap_persen > 80 else "🟡" if budget_terserap_persen > 50 else "🔴"
    st.markdown(f"""
    <div class="metric-premium">
        <h3>⏳ Serapan Budget</h3>
        <h2>{budget_terserap_persen:.0f}%</h2>
        <small>{warna_budget} dari {format_rp(budget_set)}</small>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ==================== DIAGNOSIS PREMIUM ====================
st.subheader("🩺 **Diagnosis & Rekomendasi**")

masalah_list = []
solusi_list = []
prioritas_list = []

# ========== DIAGNOSIS 1: MASALAH CTR ==========
if ctr < 2:
    masalah_list.append("🔴 **CTR Rendah**")
    solusi_list.append(f"""
    **Masalah:** CTR {ctr:.2f}% di bawah standar (2%)
    
    **Akar Masalah:** 
    - Foto utama / thumbnail kurang menarik
    - Hook video 3 detik pertama tidak menggugah
    - Penawaran tidak jelas
    
    **✅ Solusi:**
    1. **Ganti visual iklan** — buat 3 variasi baru
    2. **Test hook berbeda:** diskon (50%), bukti sosial (terjual 1000+), masalah (celana kekecilan)
    3. **Pastikan produk terlihat jelas** di frame pertama
    """)
    prioritas_list.append("URGENT")

# ========== DIAGNOSIS 2: MASALAH BUDGET TERSERAP ==========
if budget_terserap_persen < 50:
    masalah_list.append("🔴 **Anggaran Tidak Terserap**")
    solusi_list.append(f"""
    **Masalah:** Hanya {budget_terserap_persen:.0f}% budget yang terpakai
    
    **Akar Masalah:**
    - Target ROAS terlalu ketat ({target_roas}x)
    - Sistem tidak bisa membelanjakan budget
    
    **✅ Solusi:**
    - **Turunkan target ROAS 0.5 - 1 poin**
    - Contoh: dari {target_roas} → {target_roas - 1:.1f} atau {target_roas - 0.5:.1f}
    - Setelah turun, **tunggu 3 hari** jangan diubah-ubah
    """)
    prioritas_list.append("URGENT")
elif budget_terserap_persen < 80:
    masalah_list.append("🟡 **Anggaran Kurang Optimal**")
    solusi_list.append(f"""
    **Masalah:** Budget terserap {budget_terserap_persen:.0f}% (belum habis)
    
    **✅ Solusi:**
    - **Turunkan target ROAS 0.5 poin** untuk melonggarkan
    - Atau **naikkan budget 20-30%** jika ROAS masih sehat
    """)
    prioritas_list.append("OPTIMASI")

# ========== DIAGNOSIS 3: MASALAH ROAS ==========
if roas_aktual < roas_bep and roas_aktual > 0:
    rugi = (roas_bep - roas_aktual) * budget_spent
    masalah_list.append("🔴 **ROAS di Bawah BEP (BONCOS!)**")
    solusi_list.append(f"""
    **Masalah:** ROAS {roas_aktual:.1f}x < BEP {roas_bep:.1f}x
    **Estimasi Kerugian:** {format_rp(rugi)}
    
    **Akar Masalah:**
    - Target ROAS terlalu rendah
    - Produk tidak meyakinkan (harga/review/deskripsi)
    
    **✅ Solusi (pilih salah satu):**
    | Opsi | Tindakan | Kapan |
    |------|----------|-------|
    | A | **Naikkan target ROAS** ke {roas_bep + 0.5:.1f} - {roas_bep + 1:.1f} | Sekarang |
    | B | **Turunkan budget 50%** (jadi {format_rp(budget_set * 0.5)}) | Sekarang |
    | C | **Stop iklan** sementara, perbaiki produk dulu | Hari ini |
    
    **⚠️ Prioritas utama:** Perbaiki konversi landing page
    """)
    prioritas_list.append("URGENT")
elif roas_aktual >= roas_bep and roas_aktual < target_roas:
    masalah_list.append("🟡 **ROAS di Bawah Target**")
    solusi_list.append(f"""
    **Masalah:** ROAS {roas_aktual:.1f}x < Target {target_roas}x (tapi masih di atas BEP ✅)
    
    **✅ Solusi:**
    - **Turunkan target ROAS ke {roas_aktual + 0.5:.1f}** agar iklan lebih longgar
    - Atau **biarkan 3-5 hari**, sistem bisa stabil sendiri
    - **Jangan naikkan budget** sampai ROAS stabil
    """)
    prioritas_list.append("OPTIMASI")
elif roas_aktual > target_roas * 1.5 and roas_aktual > 0:
    masalah_list.append("🏆 **ROAS SANGAT TINGGI! Siap Scale**")
    solusi_list.append(f"""
    **Masalah:** ROAS {roas_aktual:.1f}x > {target_roas * 1.5:.0f}x (luar biasa!)
    
    **✅ Solusi SCALE:**
    - **Naikkan budget 30-50%** → dari {format_rp(budget_set)} menjadi {format_rp(budget_set * 1.4)}
    - Target ROAS bisa **dipertahankan atau naikkan sedikit**
    - **Pastikan stok produk AMAN** sebelum scale
    
    **🚀 Rekomendasi target ROAS baru:** {target_roas + 0.5:.1f} - {target_roas + 1:.1f}
    """)
    prioritas_list.append("SCALE")

# ========== DIAGNOSIS 4: MASALAH KONVERSI ==========
if clicks > 50 and orders == 0:
    masalah_list.append("🔴 **Klik Banyak Tapi 0 Order!**")
    solusi_list.append(f"""
    **Masalah:** {clicks:.0f} klik tapi 0 pesanan
    
    **Akar Masalah (99% produk):**
    1. Harga tidak bersaing dengan kompetitor
    2. Review & rating masih sedikit/tidak ada
    3. Deskripsi produk lemah (cuma spesifikasi)
    
    **✅ Solusi (perbaiki produk, BUKAN iklan):**
    | Prioritas | Tindakan |
    |-----------|----------|
    | 1 | **Cek harga kompetitor** — turunkan jika terlalu mahal |
    | 2 | **Tambah review** — minta teman/tester |
    | 3 | **Perbaiki deskripsi** — fokus ke MANFAAT |
    | 4 | **Tambahkan video** — tunjukkan produk asli |
    
    **⚠️ JANGAN ubah setting ROAS dulu!** Masalahnya di produk.
    """)
    prioritas_list.append("URGENT")
elif clicks > 50 and orders > 0:
    cvr = orders / clicks * 100
    if cvr < 2:
        masalah_list.append("🟡 **CVR Rendah**")
        solusi_list.append(f"""
        **Masalah:** CVR {cvr:.1f}% < 2% standar
        
        **✅ Solusi Optimasi Landing Page:**
        - Perbaiki foto produk (tampilkan dari berbagai sudut)
        - Tambahkan promo/bundling (beli 2 gratis ongkir)
        - Pasang testimoni pembeli di deskripsi
        - Pastikan harga kompetitif
        """)
        prioritas_list.append("OPTIMASI")

# ========== DIAGNOSIS 5: MASALAH CPC ==========
if cpc > 3000 and clicks > 0:
    masalah_list.append("💰 **CPC Mahal**")
    solusi_list.append(f"""
    **Masalah:** CPC {format_rp(cpc)} > Rp3.000
    
    **✅ Solusi:**
    - **Turunkan target ROAS 0.5-1 poin** untuk memperluas audience
    - **Ganti kreatif iklan** agar lebih relevan
    - **Perluas target audiens** (jangan terlalu sempit)
    """)
    if "URGENT" not in prioritas_list:
        prioritas_list.append("OPTIMASI")

# ========== DIAGNOSIS 6: JANGKAUAN SEMPIT ==========
if impressions < 5000 and roas_aktual > roas_bep * 1.5 and roas_aktual > 0:
    masalah_list.append("🟡 **ROAS Tinggi Tapi Jangkauan Sempit**")
    solusi_list.append(f"""
    **Masalah:** Hanya {impressions:,.0f} tayangan, ROAS {roas_aktual:.1f}x tinggi
    
    **✅ Solusi Ekspansi:**
    - **Longgarkan target ROAS** turunkan 0.5-1 poin
    - **Naikkan budget 20-30%** → dari {format_rp(budget_set)} menjadi {format_rp(budget_set * 1.25)}
    - Biarkan 3-5 hari, pantau apakah jangkauan membesar
    """)
    if "SCALE" not in prioritas_list:
        prioritas_list.append("OPTIMASI")

# ========== DIAGNOSIS 7: PERFORM SEHAT ==========
if (ctr >= 2 and roas_aktual >= roas_bep and orders > 0 and 
    "🔴" not in str(masalah_list) and "URGENT" not in prioritas_list):
    masalah_list.append("✅ **Performa Sehat & Stabil**")
    solusi_list.append(f"""
    **Masalah:** Semua metrik dalam kondisi baik ✅
    
    **✅ Rekomendasi:**
    - **Scale naikkan budget 30%** → dari {format_rp(budget_set)} menjadi {format_rp(budget_set * 1.3)}
    - Pantau selama 7 hari
    - Jangan sering mengubah setting
    
    **📈 Target scaling berikutnya:** 
    - Jika ROAS tetap stabil → naikkan budget lagi 20-30%
    - Jika ROAS turun → turunkan budget ke semula
    """)
    prioritas_list.append("SCALE")

# ==================== TAMPILKAN HASIL ====================
if len(masalah_list) > 0:
    for i in range(len(masalah_list)):
        if "🔴" in masalah_list[i]:
            st.markdown(f"""
            <div class="danger-card">
                <h3>🚨 {masalah_list[i]}</h3>
                <hr style="background: rgba(255,255,255,0.3);">
                {solusi_list[i]}
                <hr style="background: rgba(255,255,255,0.3);">
                <p><strong>🎯 PRIORITAS:</strong> {prioritas_list[i] if i < len(prioritas_list) else 'Segera'} ⚡</p>
            </div>
            """, unsafe_allow_html=True)
        elif "🏆" in masalah_list[i] or "✅" in masalah_list[i]:
            st.markdown(f"""
            <div class="success-card">
                <h3>🎉 {masalah_list[i]}</h3>
                <hr style="background: rgba(255,255,255,0.3);">
                {solusi_list[i]}
            </div>
            """, unsafe_allow_html=True)
        elif "🟡" in masalah_list[i]:
            st.markdown(f"""
            <div class="warning-card">
                <h3>⚠️ {masalah_list[i]}</h3>
                <hr style="background: rgba(0,0,0,0.1);">
                {solusi_list[i]}
                <hr style="background: rgba(0,0,0,0.1);">
                <p><strong>🎯 PRIORITAS:</strong> {prioritas_list[i] if i < len(prioritas_list) else 'Normal'}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="info-card">
                <h3>ℹ️ {masalah_list[i]}</h3>
                {solusi_list[i]}
            </div>
            """, unsafe_allow_html=True)

# ==================== RINGKASAN ACTION PLAN ====================
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.subheader("📋 **Ringkasan Action Plan**")

col_action1, col_action2 = st.columns(2)

with col_action1:
    st.markdown("### 🎯 **Target ROAS**")
    if budget_terserap_persen < 50:
        st.success(f"🔻 **Turunkan** menjadi: {target_roas - 1:.1f} - {target_roas - 0.5:.1f}")
    elif roas_aktual < roas_bep:
        st.success(f"🔺 **Naikkan** menjadi: {roas_bep + 0.5:.1f} - {roas_bep + 1:.1f}")
    elif roas_aktual > target_roas * 1.5:
        st.success(f"✅ **Pertahankan atau naikkan** ke: {target_roas + 0.5:.1f}")
    else:
        st.info(f"⏸️ **Pertahankan** di: {target_roas:.1f}")

with col_action2:
    st.markdown("### 💰 **Budget Harian**")
    if roas_aktual > target_roas * 1.5:
        st.success(f"🚀 **Naikkan** menjadi: {format_rp(budget_set * 1.4)}")
    elif budget_terserap_persen < 50:
        st.warning(f"🔻 **Turunkan sementara** atau longgarkan ROAS")
    elif roas_aktual < roas_bep:
        st.warning(f"🔻 **Turunkan 50%** menjadi: {format_rp(budget_set * 0.5)}")
    else:
        st.info(f"⏸️ **Pertahankan** di: {format_rp(budget_set)}")

# ==================== TABEL RINGKASAN DATA ====================
with st.expander("📋 **Lihat Detail Perhitungan**"):
    st.markdown("""
    | Metrik | Nilai | Keterangan |
    |--------|-------|-------------|
    | CTR | {}% | {} |
    | ROAS Aktual | {}x | BEP: {}x |
    | Target ROAS Setting | {}x | {} |
    | CPC | {} | {} |
    | CPA | {} | Biaya per order |
    | Budget Setting | {} | Per hari |
    | Budget Terserap | {} ({}%) | {} |
    | Omset | {} | Dari iklan |
    | Order | {} pesanan | {} |
    | Estimasi Profit | {} | {} |
    """.format(
        f"{ctr:.2f}", "✅ Bagus" if ctr >= 2 else "⚠️ Perlu perbaikan",
        f"{roas_aktual:.2f}", f"{roas_bep:.1f}",
        f"{target_roas:.1f}", "✅ On track" if roas_aktual >= target_roas else "⚠️ Di bawah target",
        format_rp(cpc), "✅ Normal" if cpc <= 3000 else "⚠️ Mahal",
        format_rp(cpa),
        format_rp(budget_set),
        format_rp(budget_spent), f"{budget_terserap_persen:.0f}", "✅ Habis" if budget_terserap_persen > 80 else "⚠️ Kurang",
        format_rp(sales),
        f"{orders}", "✅ Ada order" if orders > 0 else "⚠️ Tidak ada order",
        format_rp(profit_estimasi), status_profit
    ), unsafe_allow_html=True)

# ==================== PANDUAN LENGKAP ====================
with st.expander("📖 **Panduan Lengkap Interpretasi Data**"):
    st.markdown("""
    ### 🎯 Cara Membaca Data Iklan
    
    | Masalah | Ciri-ciri | Solusi |
    |---------|-----------|--------|
    | **CTR Rendah** | CTR < 2% | Ganti visual (foto/video hook 3 detik) |
    | **Anggaran Tidak Habis** | Terserap <50% | Turunkan target ROAS 0.5-1 poin |
    | **ROAS di Bawah BEP** | ROAS < BEP | Naikkan target ROAS atau stop iklan |
    | **Klik banyak, order 0** | Clicks >50, orders=0 | Perbaiki produk (harga/review/deskripsi) |
    | **ROAS tinggi, jangkauan kecil** | ROAS > BEP×1.5, impressions<5000 | Longgarkan ROAS, naikkan budget |
    | **Performa sehat** | CTR>2%, ROAS>BEP, orders>0 | Scale naikkan budget 30% |
    
    ### 🔥 Rumus Cepat (WAJIB DIINGAT)
    
    - **CTR < 2%** → Masalah visual (ganti kreatif)
    - **Klik ada, order 0** → Masalah produk (bukan iklan)
    - **ROAS < BEP** → Rugi (naikkan target ROAS atau stop)
    - **Budget gak habis** → ROAS terlalu ketat (turunkan)
    - **ROAS > BEP × 1.5** → Siap scale (naikkan budget)
    
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
    
    **Artinya:** Setiap Rp1 iklan harus menghasilkan Rp5 penjualan agar tidak rugi.
    """)

# ==================== FOOTER ====================
st.markdown("---")
st.markdown(f"""
<div class="footer">
    <p>🩺 <strong>Ads Doctor Premium v3.0</strong> | Framework GMV Max Shopee & TikTok</p>
    <p>📅 Analisis terakhir: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
</div>
""", unsafe_allow_html=True)
