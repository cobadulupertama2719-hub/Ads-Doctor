import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(page_title="Ads Doctor - TikTok Ads", page_icon="🩺", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 1rem;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>🩺 Ads Doctor - TikTok Ads</h1>
    <p>Upload Excel/CSV TikTok Ads → Analisis Otomatis + Rekomendasi Perbaikan</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/tiktok.png", width=60)
    st.markdown("## ⚙️ Pengaturan")
    bep = st.number_input("🎯 ROAS BEP (target minimal)", value=5.0, step=0.5)
    ctr_threshold = st.slider("📊 Minimal CTR (%)", 0.5, 5.0, 2.0, 0.5)
    st.markdown("---")
    st.caption("📌 Support file Excel (.xlsx) dan CSV (.csv) dari TikTok Ads")

# Upload file - SUPPORT EXCEL & CSV
uploaded = st.file_uploader("📂 Upload file Excel (.xlsx) atau CSV (.csv) dari TikTok Ads", 
                            type=["csv", "xlsx"])

if uploaded:
    with st.spinner("🔍 Menganalisis data TikTok..."):
        # Baca file (otomatis detect Excel atau CSV)
        if uploaded.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded, sheet_name=0)  # baca sheet pertama
            st.success(f"✅ File Excel terbaca: {uploaded.name}")
        else:
            df = pd.read_csv(uploaded)
            st.success(f"✅ File CSV terbaca: {uploaded.name}")
        
        # Tampilkan preview
        with st.expander("📋 Preview data (10 baris pertama)"):
            st.dataframe(df.head(10), use_container_width=True)
        
        # ==================== MAPPING KOLOM TIKTOK ====================
        kolom_mapping = {
            'Nama kampanye': 'campaign',
            'ID Campaign': 'campaign_id',
            'Jenis materi iklan': 'ad_type',
            'Judul video': 'video_title',
            'Biaya': 'spend',
            'Pesanan SKU': 'orders',
            'Pendapatan kotor': 'sales',
            'Impresi iklan produk': 'impressions',
            'Jumlah klik iklan produk': 'clicks',
            'Tingkat klik iklan produk': 'ctr_raw',
            'Rasio konversi iklan': 'cvr_raw',
            'ROI': 'roi',
            'Biaya per pesanan': 'cpa',
            'Akun TikTok': 'tiktok_account'
        }
        
        for old_name, new_name in kolom_mapping.items():
            if old_name in df.columns:
                df.rename(columns={old_name: new_name}, inplace=True)
        
        # Cek kolom wajib
        required = ['impressions', 'clicks', 'spend', 'sales']
        missing = [r for r in required if r not in df.columns]
        
        if missing:
            st.error(f"❌ Kolom tidak ditemukan: {missing}")
            st.info(f"Kolom yang tersedia: {list(df.columns)}")
            st.stop()
        
        # Bersihkan data
        for col in ['spend', 'sales', 'impressions', 'clicks', 'orders']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        # Hitung metrik
        df['CTR'] = (df['clicks'] / df['impressions'] * 100).round(2)
        df['ROAS'] = (df['sales'] / df['spend'].replace(0, np.nan)).round(2)
        df['CPC'] = (df['spend'] / df['clicks'].replace(0, np.nan)).round(0)
        
        if 'orders' in df.columns:
            df['CVR'] = (df['orders'] / df['clicks'].replace(0, np.nan) * 100).round(2)
            df['CPA'] = (df['spend'] / df['orders'].replace(0, np.nan)).round(0)
        
        df['BEP'] = bep
        
        # Filter data valid
        df_valid = df[df['impressions'] > 0].copy()
        
        if len(df_valid) == 0:
            st.warning("⚠️ Tidak ada data dengan impressions > 0")
            st.stop()
        
        # ==================== FUNGSI ANALISIS ====================
        def analisis(row):
            rekomendasi = []
            prioritas = 4
            masalah = []
            
            if row['CTR'] < ctr_threshold:
                rekomendasi.append(f"🔴 Ganti visual/hook (CTR {row['CTR']}% < {ctr_threshold}%)")
                masalah.append("CTR Rendah")
                prioritas = 1
            
            if pd.notna(row['ROAS']) and row['ROAS'] < row['BEP']:
                rekomendasi.append(f"🟠 ROAS {row['ROAS']} < BEP {row['BEP']} → Naikkan target ROAS")
                masalah.append("ROAS Rendah")
                prioritas = min(prioritas, 2)
            elif pd.notna(row['ROAS']) and row['ROAS'] >= row['BEP'] * 1.5:
                rekomendasi.append(f"🏆 ROAS {row['ROAS']} > 1.5x BEP (Excellent!)")
                masalah.append("Performa Bagus")
                prioritas = min(prioritas, 3)
            
            if 'orders' in df.columns:
                if row['clicks'] > 30 and row['orders'] == 0:
                    rekomendasi.append(f"🟠 {row['clicks']:.0f} klik tapi 0 order → Cek produk")
                    masalah.append("Konversi 0%")
                    prioritas = min(prioritas, 1)
                elif row['orders'] > 0 and pd.notna(row['CVR']) and row['CVR'] < 2:
                    rekomendasi.append(f"🟡 CVR {row['CVR']}% < 2% → Optimasi landing page")
                    masalah.append("CVR Rendah")
                    prioritas = min(prioritas, 2)
            
            if row['impressions'] < 5000 and pd.notna(row['ROAS']) and row['ROAS'] > row['BEP'] * 1.5:
                rekomendasi.append("🟡 ROAS tinggi tapi jangkauan sempit → Longgarkan target ROAS")
                masalah.append("Distribusi Sempit")
                prioritas = min(prioritas, 2)
            
            if row['impressions'] < 1000 and row['spend'] < 50000:
                rekomendasi.append("🎯 Iklan tidak terserap → Turunkan target ROAS")
                masalah.append("Tidak Terserap")
                prioritas = min(prioritas, 2)
            
            if row['CTR'] >= ctr_threshold and pd.notna(row['ROAS']) and row['ROAS'] >= row['BEP']:
                if 'orders' in df.columns and row['orders'] > 0:
                    rekomendasi.append("✅ Performa sehat → Scale naikkan budget 30%")
                    if prioritas == 4:
                        prioritas = 3
            
            if not rekomendasi:
                rekomendasi.append("⚠️ Data tidak cukup")
                masalah.append("Data Tidak Cukup")
            
            return {
                'rekomendasi': " | ".join(rekomendasi[:2]),
                'prioritas': prioritas,
                'masalah': masalah[0] if masalah else "Normal"
            }
        
        hasil = df_valid.apply(analisis, axis=1)
        df_valid['rekomendasi'] = [x['rekomendasi'] for x in hasil]
        df_valid['prioritas'] = [x['prioritas'] for x in hasil]
        df_valid['masalah'] = [x['masalah'] for x in hasil]
        
        # ==================== METRIC CARDS ====================
        st.subheader("📊 Ringkasan Kinerja")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_ctr = df_valid['CTR'].mean()
            st.metric("Rata-rata CTR", f"{avg_ctr:.1f}%")
        
        with col2:
            avg_roas = df_valid['ROAS'].mean()
            st.metric("Rata-rata ROAS", f"{avg_roas:.1f}x")
        
        with col3:
            st.metric("Total Spend", f"Rp{df_valid['spend'].sum():,.0f}")
        
        with col4:
            st.metric("Total Omset", f"Rp{df_valid['sales'].sum():,.0f}")
        
        st.markdown("---")
        
        # ==================== TABEL HASIL ====================
        st.markdown("### 📋 Hasil Analisis")
        
        kolom_tampil = []
        if 'campaign' in df_valid.columns:
            kolom_tampil.append('campaign')
        if 'video_title' in df_valid.columns:
            kolom_tampil.append('video_title')
        kolom_tampil.extend(['CTR', 'ROAS', 'masalah', 'prioritas', 'rekomendasi'])
        kolom_tampil = [k for k in kolom_tampil if k in df_valid.columns]
        
        st.dataframe(df_valid[kolom_tampil], use_container_width=True, height=400)
        
        # ==================== PRIORITAS ====================
        st.markdown("### 🎯 Prioritas Tindakan")
        
        darurat = df_valid[df_valid['prioritas'] == 1]
        penting = df_valid[df_valid['prioritas'] == 2]
        
        if len(darurat) > 0:
            st.error(f"🔴 {len(darurat)} iklan perlu TINDAKAN SEGERA")
            for _, row in darurat.iterrows():
                nama = row.get('campaign', row.get('video_title', 'Iklan'))
                st.write(f"- **{nama[:50]}**: {row['rekomendasi']}")
        
        if len(penting) > 0:
            st.warning(f"🟠 {len(penting)} iklan perlu OPTIMASI")
            for _, row in penting.iterrows():
                nama = row.get('campaign', row.get('video_title', 'Iklan'))
                st.write(f"- **{nama[:50]}**: {row['rekomendasi']}")
        
        # ==================== DOWNLOAD ====================
        csv = df_valid.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Hasil Analisis (CSV)",
            data=csv,
            file_name=f"tiktok_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv"
        )

else:
    st.info("👈 **Upload file Excel (.xlsx) atau CSV (.csv) dari TikTok Ads**")
    
    with st.expander("📖 Cara Export dari TikTok Ads"):
        st.markdown("""
        1. Buka TikTok Ads Manager
        2. Pilih tab **Laporan** → **Laporan Kustom**
        3. Pilih kolom: 
           - Nama kampanye
           - Impresi iklan produk
           - Jumlah klik iklan produk
           - Biaya
           - Pendapatan kotor
           - Pesanan SKU (opsional)
        4. Export sebagai **Excel (.xlsx)** atau **CSV (.csv)**
        5. Upload file ke sini
        """)

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>🩺 Ads Doctor | Support Excel & CSV TikTok Ads</p>", unsafe_allow_html=True)
