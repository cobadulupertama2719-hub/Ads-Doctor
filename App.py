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
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 1rem;
        color: white;
        text-align: center;
    }
    .warning-card {
        background: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .danger-card {
        background: #fee2e2;
        border-left: 4px solid #ef4444;
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

# Header
st.markdown("""
<div class="main-header">
    <h1>🩺 Ads Doctor - TikTok Ads</h1>
    <p>Upload CSV TikTok Ads → Analisis Otomatis + Rekomendasi Perbaikan</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/tiktok.png", width=60)
    st.markdown("## ⚙️ Pengaturan")
    
    bep = st.number_input("🎯 ROAS BEP (target minimal)", value=5.0, step=0.5,
                          help="Contoh: 5 artinya setiap Rp1 iklan harus hasilkan Rp5 penjualan")
    ctr_threshold = st.slider("📊 Minimal CTR (%)", 0.5, 5.0, 2.0, 0.5)
    
    st.markdown("---")
    st.caption("📌 Khusus untuk export TikTok Ads")

# Upload file
uploaded = st.file_uploader("📂 Upload CSV dari TikTok Ads", type=["csv"])

if uploaded:
    with st.spinner("🔍 Menganalisis data TikTok..."):
        df = pd.read_csv(uploaded)
        
        # ==================== MAPPING KOLOM TIKTOK ====================
        # Mapping kolom Indonesia ke nama standar
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
        
        # Bersihkan data (konversi ke angka)
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
        
        # Filter data valid (impressions > 0)
        df_valid = df[df['impressions'] > 0].copy()
        
        if len(df_valid) == 0:
            st.warning("⚠️ Tidak ada data dengan impressions > 0")
            st.stop()
        
        # ==================== FUNGSI ANALISIS ====================
        def analisis(row):
            rekomendasi = []
            prioritas = 4
            masalah = []
            detail = []
            
            # 1. CTR Analysis
            if row['CTR'] < ctr_threshold:
                rekomendasi.append(f"🔴 Ganti visual video/hook (CTR {row['CTR']}% < {ctr_threshold}%)")
                masalah.append("CTR Rendah")
                detail.append(f"Impresi: {row['impressions']:,.0f} | Klik: {row['clicks']:.0f}")
                prioritas = 1
            
            # 2. ROAS Analysis
            if pd.notna(row['ROAS']) and row['ROAS'] < row['BEP']:
                rugi = (row['BEP'] - row['ROAS']) * row['spend']
                rekomendasi.append(f"🟠 ROAS {row['ROAS']} < BEP {row['BEP']} (Rugi Rp{rugi:,.0f})")
                masalah.append("ROAS Rendah")
                prioritas = min(prioritas, 2)
            elif pd.notna(row['ROAS']) and row['ROAS'] >= row['BEP'] * 1.5:
                rekomendasi.append(f"🏆 ROAS {row['ROAS']} > 1.5x BEP (Excellent!)")
                masalah.append("Performa Bagus")
                prioritas = min(prioritas, 3)
            
            # 3. Orders Analysis (Klik ada tapi order 0)
            if 'orders' in df.columns:
                if row['clicks'] > 30 and row['orders'] == 0:
                    rekomendasi.append(f"🟠 {row['clicks']:.0f} klik tapi 0 order → Cek produk (harga/review/deskripsi)")
                    masalah.append("Konversi 0%")
                    prioritas = min(prioritas, 1)
                elif row['orders'] > 0 and pd.notna(row['CVR']) and row['CVR'] < 2:
                    rekomendasi.append(f"🟡 CVR {row['CVR']}% < 2% → Optimasi landing page")
                    masalah.append("CVR Rendah")
                    prioritas = min(prioritas, 2)
            
            # 4. CPC Analysis
            if pd.notna(row['CPC']) and row['CPC'] > 3000:
                rekomendasi.append(f"💰 CPC Rp{row['CPC']:,.0f} > Rp3.000 → Perbaiki relevansi audience")
                masalah.append("CPC Mahal")
                prioritas = min(prioritas, 3)
            
            # 5. Distribution Analysis (Impresi kecil tapi ROAS tinggi)
            if row['impressions'] < 5000 and pd.notna(row['ROAS']) and row['ROAS'] > row['BEP'] * 1.5:
                rekomendasi.append("🟡 ROAS tinggi tapi jangkauan sempit → Longgarkan target ROAS, naikkan budget 20-30%")
                masalah.append("Distribusi Sempit")
                prioritas = min(prioritas, 2)
            
            # 6. Iklan tidak terserap
            if row['impressions'] < 1000 and row['spend'] < 50000:
                rekomendasi.append("🎯 Iklan tidak terserap → Turunkan target ROAS atau ganti kreatif")
                masalah.append("Tidak Terserap")
                prioritas = min(prioritas, 2)
            
            # 7. Performa Sehat
            if row['CTR'] >= ctr_threshold and pd.notna(row['ROAS']) and row['ROAS'] >= row['BEP']:
                if 'orders' in df.columns and row['orders'] > 0:
                    rekomendasi.append("✅ Performa sehat → Scale naikkan budget 30%, pantau 7 hari")
                    if prioritas == 4:
                        prioritas = 3
            
            if not rekomendasi:
                rekomendasi.append("⚠️ Data tidak cukup untuk analisis")
                masalah.append("Data Tidak Cukup")
            
            return {
                'rekomendasi': " | ".join(rekomendasi[:2]),
                'prioritas': prioritas,
                'masalah': masalah[0] if masalah else "Normal",
                'detail': " | ".join(detail[:2])
            }
        
        # Terapkan analisis
        hasil = df_valid.apply(analisis, axis=1)
        df_valid['rekomendasi'] = [x['rekomendasi'] for x in hasil]
        df_valid['prioritas'] = [x['prioritas'] for x in hasil]
        df_valid['masalah'] = [x['masalah'] for x in hasil]
        df_valid['detail'] = [x['detail'] for x in hasil]
        
        # ==================== METRIC CARDS ====================
        st.subheader("📊 Ringkasan Kinerja TikTok Ads")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            avg_ctr = df_valid['CTR'].mean()
            st.metric("Rata-rata CTR", f"{avg_ctr:.1f}%",
                     delta="✅ Bagus" if avg_ctr >= ctr_threshold else "⚠️ Perlu perbaikan")
        
        with col2:
            avg_roas = df_valid['ROAS'].mean()
            st.metric("Rata-rata ROAS", f"{avg_roas:.1f}x",
                     delta=f"Target: {bep}x")
        
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
        tab1, tab2, tab3 = st.tabs(["📋 Tabel Detail", "🎯 Prioritas Aksi", "📈 Insight"])
        
        with tab1:
            st.markdown("### 📋 Data Iklan + Rekomendasi")
            
            kolom_tampil = []
            if 'campaign' in df_valid.columns:
                kolom_tampil.append('campaign')
            if 'video_title' in df_valid.columns:
                kolom_tampil.append('video_title')
            kolom_tampil.extend(['CTR', 'ROAS', 'CPC', 'masalah', 'prioritas', 'rekomendasi'])
            
            kolom_tampil = [k for k in kolom_tampil if k in df_valid.columns]
            
            st.dataframe(df_valid[kolom_tampil], use_container_width=True, height=400)
        
        with tab2:
            st.markdown("### 🎯 Prioritas Tindakan (Urgent → Normal)")
            
            darurat = df_valid[df_valid['prioritas'] == 1]
            penting = df_valid[df_valid['prioritas'] == 2]
            normal = df_valid[df_valid['prioritas'] >= 3]
            
            if len(darurat) > 0:
                st.markdown("#### 🔴 PRIORITAS 1 - TINDAKAN SEGERA")
                for _, row in darurat.iterrows():
                    nama = row.get('campaign', row.get('video_title', 'Iklan'))
                    if len(nama) > 50:
                        nama = nama[:47] + "..."
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
                    if len(nama) > 50:
                        nama = nama[:47] + "..."
                    st.markdown(f"""
                    <div class="warning-card">
                        <b>📊 {nama}</b><br>
                        {row['rekomendasi']}
                    </div>
                    """, unsafe_allow_html=True)
            
            if len(normal) > 0:
                st.markdown("#### 🟢 PRIORITAS 3 - PANTAU & SCALE")
                for _, row in normal.iterrows():
                    nama = row.get('campaign', row.get('video_title', 'Iklan'))
                    if len(nama) > 60:
                        nama = nama[:57] + "..."
                    st.write(f"- **{nama}**: {row['rekomendasi']}")
        
        with tab3:
            st.markdown("### 💡 Insight TikTok Ads")
            
            # Insight 1: Best Video
            if 'video_title' in df_valid.columns and 'ROAS' in df_valid.columns:
                best_idx = df_valid['ROAS'].idxmax()
                best_video = df_valid.loc[best_idx, 'video_title'] if pd.notna(df_valid.loc[best_idx, 'video_title']) else "Tidak ada judul"
                best_roas = df_valid.loc[best_idx, 'ROAS']
                st.success(f"🏆 **Video Terbaik:** ROAS {best_roas:.1f}x\n\n{best_video[:100]}")
            
            # Insight 2: CTR Issue
            ctr_issue = len(df_valid[df_valid['CTR'] < ctr_threshold])
            if ctr_issue > 0:
                st.warning(f"📸 **{ctr_issue} video** memiliki CTR di bawah {ctr_threshold}%. Ganti hook video dalam 5 detik pertama.")
            
            # Insight 3: ROAS Issue
            roas_issue = len(df_valid[pd.notna(df_valid['ROAS']) & (df_valid['ROAS'] < bep)])
            if roas_issue > 0:
                st.warning(f"💰 **{roas_issue} iklan** rugi (ROAS < BEP). Naikkan target ROAS 0.5-1 poin.")
            
            # Insight 4: Conversion Issue
            if 'orders' in df_valid.columns:
                no_order = len(df_valid[(df_valid['clicks'] > 30) & (df_valid['orders'] == 0)])
                if no_order > 0:
                    st.warning(f"🛒 **{no_order} iklan** punya klik tapi 0 order. Cek harga, review, dan deskripsi produk.")
            
            # Insight 5: Best CTR
            best_ctr_idx = df_valid['CTR'].idxmax()
            best_ctr = df_valid.loc[best_ctr_idx, 'CTR']
            st.info(f"🎬 **CTR Tertinggi:** {best_ctr:.1f}% — analisis video ini untuk dijadikan benchmark.")
        
        # ==================== DOWNLOAD ====================
        st.markdown("---")
        csv = df_valid.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Hasil Analisis (CSV)",
            data=csv,
            file_name=f"tiktok_ads_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv"
        )

else:
    # Tampilan awal
    st.info("👈 **Upload CSV dari TikTok Ads** untuk memulai analisis")
    
    with st.expander("📖 Format CSV yang diterima (export TikTok Ads)"):
        st.markdown("""
        **Kolom yang diperlukan:**
        - `Nama kampanye` atau `campaign`
        - `Impresi iklan produk` atau `impressions`
        - `Jumlah klik iklan produk` atau `clicks`
        - `Biaya` atau `spend`
        - `Pendapatan kotor` atau `sales`
        
        **Opsional (lebih akurat):**
        - `Pesanan SKU` atau `orders`
        - `Judul video` atau `video_title`
        """)
        
        # Contoh data dari file Mas
        contoh = pd.DataFrame({
            'Nama kampanye': ['Sak Mlakune', 'GMV Max Best Sales Product'],
            'Impresi iklan produk': [9951, 20752],
            'Jumlah klik iklan produk': [236, 489],
            'Biaya': [125747, 354765],
            'Pendapatan kotor': [2121627, 1660079],
            'Pesanan SKU': [32, 25]
        })
        st.dataframe(contoh, use_container_width=True)

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>🩺 Ads Doctor | Khusus TikTok Ads | Framework GMV Max</p>", 
    unsafe_allow_html=True
)
