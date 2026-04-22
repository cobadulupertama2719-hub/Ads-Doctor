import streamlit as st
import numpy as np

st.set_page_config(page_title="Ads Doctor - Manual Input", page_icon="🩺", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .result-card {
        background: white;
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    .danger {
        background: #fee2e2;
        border-left: 4px solid #ef4444;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .warning {
        background: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .success {
        background: #d1fae5;
        border-left: 4px solid #10b981;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .info {
        background: #dbeafe;
        border-left: 4px solid #3b82f6;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .metric-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 0.75rem;
        color: white;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🩺 Ads Doctor - Manual Input</h1>
    <p>Isi data iklan Anda → Langsung Dapat Rekomendasi & Solusi</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/advertising.png", width=60)
    st.markdown("## ⚙️ Target Bisnis")
    bep_roas = st.number_input("🎯 ROAS BEP (target minimal)", value=5.0, step=0.5,
                                help="Contoh: 5 artinya setiap Rp1 iklan harus hasilkan Rp5 penjualan")
    st.markdown("---")
    st.caption("💡 Tips: ROAS BEP = Harga Jual ÷ (Harga Jual - HPP - Admin)")

# ==================== FORM INPUT ====================
st.subheader("📝 Input Data Iklan Hari Ini")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📊 Data Performa Iklan")
    impressions = st.number_input("👁️ Pengunjung (Impressions)", min_value=0, value=10000, step=1000)
    clicks = st.number_input("🖱️ Klik (Clicks)", min_value=0, value=300, step=50)
    
    st.markdown("### 💰 Data Anggaran")
    budget_set = st.number_input("💰 Anggaran yang disetting (Budget per hari)", min_value=0, value=100000, step=10000)
    budget_spent = st.number_input("💸 Anggaran yang terserap hari ini", min_value=0, value=90000, step=5000)

with col2:
    st.markdown("### 🎯 Target ROAS")
    target_roas = st.number_input("🎯 ROAS / ROI yang disetting", min_value=0.0, value=6.0, step=0.5,
                                   help="Target ROAS yang Anda pasang di iklan")
    
    st.markdown("### 📈 Data Penjualan")
    sales = st.number_input("🛒 Omset (Pendapatan kotor)", min_value=0, value=600000, step=50000)
    orders = st.number_input("📦 Jumlah Order (Pesanan)", min_value=0, value=6, step=1)

# ==================== HITUNG METRIK ====================
if clicks > 0 and impressions > 0:
    ctr = (clicks / impressions * 100)
    cpc = budget_spent / clicks if clicks > 0 else 0
    roas_aktual = sales / budget_spent if budget_spent > 0 else 0
    cpa = budget_spent / orders if orders > 0 else 0
    budget_terserap_persen = (budget_spent / budget_set * 100) if budget_set > 0 else 0
else:
    ctr = 0
    cpc = 0
    roas_aktual = 0
    cpa = 0
    budget_terserap_persen = 0

# ==================== METRIC CARDS ====================
st.markdown("---")
st.subheader("📊 Ringkasan Metrik")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class="metric-box">
        <h4>CTR</h4>
        <h2>{ctr:.2f}%</h2>
        <small>{'✅ Bagus' if ctr >= 2 else '⚠️ Rendah'}</small>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-box">
        <h4>ROAS Aktual</h4>
        <h2>{roas_aktual:.2f}x</h2>
        <small>Target: {target_roas}x | BEP: {bep_roas}x</small>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-box">
        <h4>CPC</h4>
        <h2>Rp{cpc:,.0f}</h2>
        <small>{'✅ Normal' if cpc <= 3000 else '⚠️ Mahal'}</small>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-box">
        <h4>CPA</h4>
        <h2>Rp{cpa:,.0f}</h2>
        <small>Biaya per order</small>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="metric-box">
        <h4>Anggaran Terserap</h4>
        <h2>{budget_terserap_persen:.0f}%</h2>
        <small>Dari Rp{budget_set:,.0f}</small>
    </div>
    """, unsafe_allow_html=True)

# ==================== DIAGNOSIS & REKOMENDASI ====================
st.markdown("---")
st.subheader("🩺 Diagnosis & Rekomendasi")

masalah = []
solusi = []
prioritas = []

# ========== DIAGNOSIS 1: MASALAH CTR ==========
if ctr < 2:
    masalah.append("🔴 **CTR Rendah** (kurang dari 2%)")
    solusi.append("""
    **Solusi:** Ganti visual iklan (foto utama / video hook dalam 3-5 detik pertama)
    - Buat 3 variasi kreatif baru dengan angle berbeda (diskon, masalah, bukti sosial)
    - Pastikan produk terlihat jelas dan menarik
    - Tambahkan teks promo yang menggugah (contoh: "Diskon 50%", "Stok Terbatas")
    """)
    prioritas.append("URGENT - Lakukan dalam 24 jam")
elif ctr < 3:
    masalah.append("🟡 **CTR Cukup** (2-3%)")
    solusi.append("""
    **Solusi:** CTR masih wajar, tapi bisa ditingkatkan
    - Test A/B dengan 1-2 kreatif baru
    - Optimasi hook video di 3 detik pertama
    """)
    prioritas.append("Optimasi - Lakukan dalam 3 hari")
else:
    masalah.append("✅ **CTR Bagus** (diatas 3%)")
    solusi.append("**Solusi:** Visual sudah menarik, fokus ke aspek lain")
    prioritas.append("Pertahankan")

# ========== DIAGNOSIS 2: MASALAH ANGGARAN TERSERAP ==========
if budget_terserap_persen < 50:
    masalah.append("🔴 **Anggaran Tidak Terserap** (kurang dari 50%)")
    solusi.append("""
    **Solusi:** Target ROAS terlalu ketat, sistem tidak bisa membelanjakan budget
    - **Turunkan target ROAS 0.5 - 1 poin**
    - Contoh: dari ROAS 6 → turunkan ke 5 atau 5.5
    - Setelah turun, tunggu 3 hari jangan diubah-ubah
    """)
    prioritas.append("URGENT - Lakukan sekarang")
elif budget_terserap_persen < 80:
    masalah.append("🟡 **Anggaran Kurang Optimal** (50-80%)")
    solusi.append("""
    **Solusi:** Anggaran belum habis, coba longgarkan target ROAS sedikit
    - **Turunkan target ROAS 0.5 poin**
    - Atau naikkan budget 20-30% jika ROAS masih sehat
    """)
    prioritas.append("Optimasi - Lakukan dalam 1-2 hari")

# ========== DIAGNOSIS 3: MASALAH ROAS ==========
if roas_aktual < bep_roas and roas_aktual > 0:
    rugi = (bep_roas - roas_aktual) * budget_spent
    masalah.append(f"🔴 **ROAS {roas_aktual:.1f}x di bawah BEP {bep_roas}x** (Rugi Rp{rugi:,.0f})")
    solusi.append(f"""
    **Solusi:** Iklan sedang rugi, harus segera ditangani
    - **Opsi 1:** Naikkan target ROAS menjadi {bep_roas + 0.5:.1f} - {bep_roas + 1:.1f}
    - **Opsi 2:** Stop iklan sementara, perbaiki produk dulu
    - **Opsi 3:** Turunkan budget 50% untuk mengurangi kerugian
    
    **Prioritas utama:** Perbaiki konversi di landing page (review, harga, deskripsi)
    """)
    prioritas.append("URGENT - Evaluasi hari ini")
elif roas_aktual < target_roas and roas_aktual >= bep_roas:
    masalah.append(f"🟡 **ROAS {roas_aktual:.1f}x di bawah target {target_roas}x**")
    solusi.append(f"""
    **Solusi:** ROAS masih aman (di atas BEP), tapi belum mencapai target
    - **Turunkan target ROAS ke {roas_aktual + 0.5:.1f}** agar iklan lebih longgar
    - Atau biarkan 3-5 hari, sistem bisa stabil sendiri
    - Jangan naikkan budget dulu sampai ROAS stabil
    """)
    prioritas.append("Pantau - Evaluasi 3 hari lagi")
elif roas_aktual > target_roas * 1.5:
    masalah.append(f"🏆 **ROAS {roas_aktual:.1f}x sangat tinggi!** (>{target_roas * 1.5:.0f}x)")
    solusi.append(f"""
    **Solusi:** Performa sangat bagus, waktunya SCALE
    - **Naikkan budget 30-50%** (misal dari Rp{budget_set:,.0f} ke Rp{budget_set * 1.3:,.0f})
    - Target ROAS bisa dipertahankan atau naikkan sedikit
    - Pastikan stok produk aman sebelum scale
    """)
    prioritas.append("Scale - Lakukan segera")

# ========== DIAGNOSIS 4: MASALAH KONVERSI (Klik ada, order sedikit) ==========
if clicks > 50 and orders == 0:
    masalah.append("🔴 **Klik banyak ({clicks}) tapi 0 order**")
    solusi.append("""
    **Solusi:** Produk tidak meyakinkan pembeli, fokus perbaiki:
    1. **Cek harga kompetitor** - apakah terlalu mahal?
    2. **Tambah review & rating** - minimal 10-20 review positif
    3. **Perbaiki deskripsi** - fokus ke manfaat, bukan spesifikasi
    4. **Tambahkan video produk** - tunjukkan produk asli
    
    **Jangan ubah setting ROAS dulu**, karena masalahnya di produk, bukan iklan
    """)
    prioritas.append("URGENT - Perbaiki produk dulu")
elif clicks > 50 and orders > 0:
    cvr = orders / clicks * 100
    if cvr < 2:
        masalah.append(f"🟡 **CVR {cvr:.1f}% rendah** (kurang dari 2%)")
        solusi.append("""
        **Solusi:** Konversi rendah, optimasi landing page:
        - Perbaiki foto produk (tampilkan dari berbagai sudut)
        - Tambahkan promo/bundling (beli 2 gratis ongkir)
        - Pasang testimoni pembeli di deskripsi
        - Pastikan harga kompetitif dengan kompetitor
        """)
        prioritas.append("Optimasi - Lakukan dalam 3 hari")

# ========== DIAGNOSIS 5: MASALAH CPC ==========
if cpc > 3000 and clicks > 0:
    masalah.append(f"💰 **CPC Rp{cpc:,.0f} terlalu mahal** (>Rp3.000)")
    solusi.append("""
    **Solusi:** Biaya per klik mahal, perbaiki relevansi:
    - Perluas target audiens (jangan terlalu sempit)
    - Ganti kreatif iklan agar lebih relevan
    - Turunkan target ROAS 0.5-1 poin
    """)
    prioritas.append("Optimasi - Lakukan dalam 1-2 hari")

# ========== DIAGNOSIS 6: JANGKAUAN SEMPIT ==========
if impressions < 5000 and roas_aktual > bep_roas * 1.5 and roas_aktual > 0:
    masalah.append("🟡 **ROAS tinggi tapi jangkauan sempit** (<5000 tayangan)")
    solusi.append("""
    **Solusi:** Iklan terlalu selektif, perlu ekspansi:
    - **Longgarkan target ROAS** turunkan 0.5-1 poin
    - **Naikkan budget 20-30%**
    - Biarkan 3-5 hari, pantau apakah jangkauan membesar
    """)
    prioritas.append("Optimasi - Lakukan dalam 1-2 hari")

# ========== TAMPILKAN HASIL ==========
if len(masalah) > 0:
    for i in range(len(masalah)):
        if "🔴" in masalah[i]:
            st.markdown(f"""
            <div class="danger">
                <h4>{masalah[i]}</h4>
                {solusi[i]}
                <hr>
                <b>🎯 Prioritas:</b> {prioritas[i] if i < len(prioritas) else 'Segera'}
            </div>
            """, unsafe_allow_html=True)
        elif "🟡" in masalah[i]:
            st.markdown(f"""
            <div class="warning">
                <h4>{masalah[i]}</h4>
                {solusi[i]}
                <hr>
                <b>🎯 Prioritas:</b> {prioritas[i] if i < len(prioritas) else 'Normal'}
            </div>
            """, unsafe_allow_html=True)
        elif "🏆" in masalah[i]:
            st.markdown(f"""
            <div class="success">
                <h4>{masalah[i]}</h4>
                {solusi[i]}
                <hr>
                <b>🎯 Prioritas:</b> Scale!
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="info">
                <h4>{masalah[i]}</h4>
                {solusi[i]}
            </div>
            """, unsafe_allow_html=True)

# ========== RINGKASAN ACTION PLAN ==========
st.markdown("---")
st.subheader("📋 Ringkasan Action Plan")

st.markdown("""
| Prioritas | Tindakan | Deadline |
|-----------|----------|----------|
| 🔴 URGENT | Ganti visual / turunkan ROAS / stop iklan | Hari ini |
| 🟡 OPTIMASI | Perbaiki produk / landing page | 1-3 hari |
| 🟢 PANTAU | Scale bertahap / pantau stabilitas | 3-7 hari |
""")

# ========== REKOMENDASI ANGKA ==========
st.markdown("---")
st.subheader("🎯 Rekomendasi Setting Ulang")

col_rek1, col_rek2 = st.columns(2)

with col_rek1:
    st.markdown("### 🎯 Target ROAS")
    if budget_terserap_persen < 50:
        st.success(f"**Turunkan target ROAS menjadi:** {target_roas - 1:.1f} - {target_roas - 0.5:.1f}")
    elif roas_aktual < bep_roas:
        st.success(f"**Naikkan target ROAS menjadi:** {bep_roas + 0.5:.1f} - {bep_roas + 1:.1f}")
    elif roas_aktual > target_roas * 1.5:
        st.success(f"**Pertahankan target ROAS di:** {target_roas:.1f} (bisa naikkan sedikit)")
    else:
        st.info(f"**Pertahankan target ROAS di:** {target_roas:.1f}")

with col_rek2:
    st.markdown("### 💰 Budget Harian")
    if roas_aktual > target_roas * 1.5:
        st.success(f"**Naikkan budget menjadi:** Rp{budget_set * 1.3:,.0f} - Rp{budget_set * 1.5:,.0f}")
    elif budget_terserap_persen < 50:
        st.warning(f"**Turunkan budget sementara** atau longgarkan ROAS dulu")
    elif roas_aktual < bep_roas:
        st.warning(f"**Turunkan budget 50%** (Rp{budget_set * 0.5:,.0f}) sampai ROAS membaik")
    else:
        st.info(f"**Pertahankan budget di:** Rp{budget_set:,.0f}")

# ==================== PANDUAN LENGKAP ====================
with st.expander("📖 Panduan Lengkap Interpretasi Data"):
    st.markdown("""
    ### 🎯 Cara Membaca Data Iklan
    
    | Masalah | Ciri-ciri | Solusi |
    |---------|-----------|--------|
    | **CTR Rendah** | CTR < 2% | Ganti visual (foto/video hook) |
    | **Anggaran Tidak Habis** | Terserap <50% | Turunkan target ROAS 0.5-1 poin |
    | **ROAS di Bawah BEP** | ROAS < BEP | Naikkan target ROAS atau stop |
    | **Klik banyak, order 0** | Clicks >50, orders=0 | Perbaiki produk (harga/review) |
    | **ROAS tinggi, jangkauan kecil** | ROAS > BEP×1.5, impressions<5000 | Longgarkan ROAS, naikkan budget |
    | **Performa sehat** | CTR>2%, ROAS>BEP | Scale naikkan budget 30% |
    
    ### 🔥 Rumus Cepat yang Wajib Diingat
    
    - **CTR < 2%** → Masalah visual (ganti kreatif)
    - **Klik ada, order 0** → Masalah produk (harga/review/deskripsi)
    - **ROAS < BEP** → Rugi (naikkan target ROAS atau stop)
    - **Budget gak habis** → ROAS terlalu ketat (turunkan)
    """)

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>🩺 Ads Doctor | Framework GMV Max Shopee & TikTok</p>", unsafe_allow_html=True)
