import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(page_title="Ads Doctor - TikTok Ads", page_icon="🩺", layout="wide")

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
    .danger-card {
        background: #fee2e2;
        border-left: 4px solid #ef4444;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .warning-card {
        background: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .success-card {
        background: #d1fae5;
        border-left: 4px solid #10b981;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>🩺 Ads Doctor - TikTok Ads</h1>
    <p>Upload file Excel dari TikTok Ads → Analisis Otomatis + Rekomendasi Perbaikan</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/tiktok.png", width=60)
    st.markdown("## ⚙️ Pengaturan")
    bep = st.number_input("🎯 ROAS BEP (target minimal)", value=5.0, step=0.5)
    ctr_threshold = st.slider("📊 Minimal CTR (%)", 0.5, 5.0, 2.0, 0.5)
    st.markdown("---")
    st.caption("📌 Support file Excel (.xlsx) dari TikTok Ads")

# Upload file
uploaded = st.file_uploader("📂 Upload file Excel dari TikTok Ads", type=["xlsx", "csv"])

if uploaded:
    with st.spinner("🔍 Menganalisis data TikTok..."):
        # Baca file
        if uploaded.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded, sheet_name=0)
        else:
            df = pd.read_csv(uploaded)
        
        # ==================== MAPPING KOLOM TIKTOK (SESUAI FILE MAS) ====================
        # Mapping dari kolom asli TikTok ke nama standar
        mapping_kolom = {
            'Nama kampanye': 'campaign',
            'Biaya': 'spend',
            'Pesanan SKU': 'orders',
            'Pendapatan kotor': 'sales',
            'Impresi iklan produk': 'impressions',
            'Jumlah klik iklan produk': 'clicks',
            'Tingkat klik iklan produk': 'ctr_raw',
            'Rasio konversi iklan': 'cvr_raw',
            'ROI': 'roi',
            'Biaya per pesanan': 'cpa',
            'Jenis materi iklan': 'ad_type',
            'Judul video': 'video_title',
            'Akun TikTok': 'tiktok_account'
        }
        
        for old_name, new_name in mapping_kolom.items():
            if old_name in df.columns:
                df.rename(columns={old_name: new_name}, inplace=True)
        
        # Cek kolom wajib
        required = ['impressions', 'clicks', 'spend', 'sales']
        missing = [r for r in required if r not in df.columns]
        
        if missing:
            st.error(f"❌ Kolom tidak ditemukan: {missing}")
            st.info(f"Kolom yang tersedia: {list(df.columns)}")
            st.stop()
        
        # Konversi ke numeric
        for col in ['impressions', 'clicks', 'spend', 'sales', 'orders']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        # Filter data valid
        df_valid = df[df['impressions'] > 0].copy()
        
        if len(df_valid) == 0:
            st.warning("⚠️ Tidak ada data dengan impressions > 0")
            st.stop()
        
        # Hitung metrik
        df_valid['CTR'] = (df_valid['clicks'] / df_valid['impressions'] * 100).round(2)
        df_valid['ROAS'] = (df_valid['sales'] / df_valid['spend'].replace(0, np.nan)).round(2)
        df_valid['CPC'] = (df_valid['spend'] / df_valid['clicks'].replace(0, np.nan)).round(0)
        
        if 'orders' in df_valid.columns:
            df_valid['CVR'] = (df_valid['orders'] / df_valid['clicks'].replace(0, np.nan) * 100).round(2)
        
        df_valid['BEP'] = bep
        
        # ==================== FUNGSI ANALISIS ====================
        def analisis(row):
            rekomendasi = []
            prioritas = 4
            masalah = []
            
            # CTR rendah
            if row['CTR'] < ctr_threshold:
                rekomendasi.append(f"🔴 Ganti visual/hook (CTR {row['CTR']}% < {ctr_threshold}%)")
                masalah.append("CTR Rendah")
                prioritas = 1
            
            # ROAS di bawah BEP
            if pd.notna(row['ROAS']) and row['ROAS'] < row['BEP']:
                rekomendasi.append(f"🟠 ROAS {row['ROAS']} < BEP {row['BEP']} → Naikkan target ROAS")
                masalah.append("ROAS Rendah")
                prioritas = min(prioritas, 2)
            elif pd.notna(row['ROAS']) and row['ROAS'] >= row['BEP'] * 1.5:
                rekomendasi.append(f"🏆 ROAS {row['ROAS']} > 1.5x BEP (Excellent!)")
                masalah.append("Performa Bagus")
                prioritas = min(prioritas, 3)
            
            # Klik banyak tapi order 0
            if 'orders' in df_valid.columns:
                if row['clicks'] > 30 and row['orders'] == 0:
                    rekomendasi.append(f"🟠 {row['clicks']:.0f} klik tapi 0 order → Cek produk")
                    masalah.append("Konversi 0%")
                    prioritas = min(prioritas, 1)
            
            # Iklan tidak terserap
            if row['impressions'] < 1000 and row['spend'] < 50000:
                rekomendasi.append("🎯 Iklan tidak terserap → Turunkan target ROAS")
                masalah.append("Tidak Terserap")
                prioritas = min(prioritas, 2)
            
            # Jangkauan sempit
            if row['impressions'] < 5000 and pd.notna(row['ROAS']) and row['ROAS'] > row['BEP'] * 1.5:
                rekomendasi.append("🟡 ROAS tinggi tapi jangkauan sempit → Longgarkan target ROAS")
                masalah.append("Distribusi Sempit")
                prioritas = min(prioritas, 2)
            
            # Performa sehat
            if row['CTR'] >= ctr_threshold and pd.notna(row['ROAS']) and row['ROAS'] >= row['BEP']:
                if 'orders' in df_valid.columns and row['orders'] > 0:
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
        st.subheader("📊 Ringkasan Kinerja TikTok Ads")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            avg_ctr = df_valid['CTR'].mean()
            st.metric("Rata-rata CTR", f"{avg_ctr:.1f}%")
        
        with col2:
            avg_roas = df_valid['ROAS'].mean()
            st.metric("Rata-rata ROAS", f"{avg_roas:.1f}x")
        
        with col3:
            total_spend = df_valid['spend'].sum()
            st.metric("Total Spend", f"Rp{total_spend:,.0f}")
        
        with col4:
            total_sales = df_valid['sales'].sum()
            st.metric("Total Omset", f"Rp{total_sales:,.0f}")
        
        with col5:
            if 'orders' in df_valid.columns:
                total_orders = df_valid['orders'].sum()
                st.metric("Total Order", f"{total_orders:,.0f}")
            else:
                st.metric("Total Iklan", f"{len(df_valid)}")
        
        st.markdown("---")
        
        # ==================== TAB ====================
        tab1, tab2 = st.tabs(["📋 Tabel Detail", "🎯 Prioritas Aksi"])
        
        with tab1:
            kolom_tampil = []
            if 'campaign' in df_valid.columns:
                kolom_tampil.append('campaign')
            if 'video_title' in df_valid.columns:
                kolom_tampil.append('video_title')
            kolom_tampil.extend(['CTR', 'ROAS', 'CPC', 'masalah', 'prioritas', 'rekomendasi'])
            
            kolom_tampil = [k for k in kolom_tampil if k in df_valid.columns]
            st.dataframe(df_valid[kolom_tampil], use_container_width=True, height=400)
        
        with tab2:
            darurat = df_valid[df_valid['prioritas'] == 1]
            penting = df_valid[df_valid['prioritas'] == 2]
            
            if len(darurat) > 0:
                st.markdown("#### 🔴 PRIORITAS 1 - TINDAKAN SEGERA")
                for _, row in darurat.iterrows():
                    nama = row.get('campaign', row.get('video_title', 'Iklan'))
                    if len(str(nama)) > 50:
                        nama = str(nama)[:47] + "..."
                    st.markdown(f"""
                    <div class="danger-card">
                        <b>⚠️ {nama}</b><br>
                        {row['rekomendasi']}<br>
                        <small>CTR: {row['CTR']}% | ROAS: {row['ROAS']:.1f}x | Spend: Rp{row['spend']:,.0f}</small>
                    </div>
                    """, unsafe_allow_html=True)
            
            if len(penting) > 0:
                st.markdown("#### 🟠 PRIORITAS 2 - OPTIMASI (1-3 Hari)")
                for _, row in penting.iterrows():
                    nama = row.get('campaign', row.get('video_title', 'Iklan'))
                    if len(str(nama)) > 50:
                        nama = str(nama)[:47] + "..."
                    st.markdown(f"""
                    <div class="warning-card">
                        <b>📊 {nama}</b><br>
                        {row['rekomendasi']}
                    </div>
                    """, unsafe_allow_html=True)
        
        # ==================== DOWNLOAD ====================
        csv = df_valid.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Hasil Analisis (CSV)",
            data=csv,
            file_name=f"tiktok_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv"
        )

else:
    st.info("👈 **Upload file Excel dari TikTok Ads**")
    
    with st.expander("📖 Format kolom yang didukung"):
        st.markdown("""
        **Kolom yang akan terbaca otomatis:**
        - `Nama kampanye` → Nama iklan
        - `Biaya` → Spend iklan
        - `Pendapatan kotor` → Omset
        - `Impresi iklan produk` → Tayangan
        - `Jumlah klik iklan produk` → Klik
        - `Pesanan SKU` → Jumlah order
        - `Judul video` → Judul video
        - `Jenis materi iklan` → Kartu produk / Video
        
        **Cara export dari TikTok Ads:**
        1. Buka TikTok Ads Manager
        2. Pilih tab **Laporan** → **Laporan Kustom**
        3. Pilih kolom di atas
        4. Export sebagai **Excel (.xlsx)**
        5. Upload ke sini
        """)

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>🩺 Ads Doctor | Khusus TikTok Ads | Framework GMV Max</p>", unsafe_allow_html=True)
