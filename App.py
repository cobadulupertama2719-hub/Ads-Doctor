import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ==================== KONFIGURASI ====================
st.set_page_config(
    page_title="Ads Doctor - Analisa Iklan TikTok & Shopee",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 1rem;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Metric card */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 1rem;
        color: white;
        text-align: center;
    }
    
    /* Button */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        font-weight: 600;
        width: 100%;
    }
    
    /* Warning card */
    .warning-card {
        background: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    
    /* Success card */
    .success-card {
        background: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ==================== HEADER ====================
st.markdown("""
<div class="main-header">
    <h1>🩺 Ads Doctor Pro</h1>
    <p>Analisa Iklan TikTok & Shopee → Langsung Dapat Rekomendasi Perbaikan</p>
</div>
""", unsafe_allow_html=True)

# ==================== SIDEBAR ====================
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/advertising.png", width=60)
    st.markdown("## ⚙️ Pengaturan")
    
    # Input BEP
    bep = st.number_input(
        "🎯 ROAS BEP (target minimal)", 
        value=5.0, 
        step=0.5,
        help="Hitung: Harga Jual ÷ (Harga Jual - HPP - Admin - Target Profit)"
    )
    
    st.markdown("---")
    
    # Threshold
    ctr_threshold = st.slider("📊 Minimal CTR (%)", 0.5, 5.0, 2.0, 0.5)
    cpc_threshold = st.number_input("💰 Maksimal CPC (Rp)", 1000, 10000, 3000, 500)
    
    st.markdown("---")
    
    # Informasi
    with st.expander("📖 Panduan Cepat"):
        st.markdown("""
        **Rumus Cepat:**
        - CTR < 2% → Ganti visual
        - ROAS < BEP → Rugi, naikkan target ROAS
        - Klik ada, order 0 → Cek produk
        - CPC > Rp3.000 → Perbaiki relevansi
        
        **Prioritas:**
        - 🔴 Darurat → stop / ganti visual
        - 🟠 Optimasi → 1-2 hari
        - 🟡 Scale → pantau 3-7 hari
        - ✅ Sehat → lanjutkan
        """)
    
    st.caption(f"📅 Last update: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

# ==================== MAIN CONTENT ====================
uploaded_file = st.file_uploader(
    "📂 **Upload file CSV** dari TikTok Ads atau Shopee Ads", 
    type=["csv"],
    help="Export data iklan dari dashboard TikTok/Shopee dalam format CSV"
)

if uploaded_file is not None:
    with st.spinner("🔄 Sedang menganalisis data..."):
        # Baca CSV
        df = pd.read_csv(uploaded_file)
        
        # Normalisasi kolom
        for col in df.columns:
            col_lower = col.lower()
            if 'impression' in col_lower or 'tayang' in col_lower or 'impresi' in col_lower:
                df.rename(columns={col: 'impressions'}, inplace=True)
            if 'click' in col_lower or 'klik' in col_lower:
                df.rename(columns={col: 'clicks'}, inplace=True)
            if 'spend' in col_lower or 'biaya' in col_lower or 'cost' in col_lower:
                df.rename(columns={col: 'spend'}, inplace=True)
            if 'sales' in col_lower or 'omset' in col_lower or 'revenue' in col_lower or 'penjualan' in col_lower:
                df.rename(columns={col: 'sales'}, inplace=True)
            if 'order' in col_lower or 'pesanan' in col_lower or 'purchase' in col_lower:
                df.rename(columns={col: 'orders'}, inplace=True)
        
        # Cek kolom wajib
        required = ['impressions', 'clicks', 'spend', 'sales']
        missing = [r for r in required if r not in df.columns]
        
        if missing:
            st.error(f"❌ Kolom tidak ditemukan: {missing}")
            st.info(f"Kolom yang tersedia: {list(df.columns)}")
            st.stop()
        
        # Hitung metrik
        df['CTR'] = (df['clicks'] / df['impressions'] * 100).round(2)
        df['ROAS'] = (df['sales'] / df['spend']).round(2)
        df['CPC'] = (df['spend'] / df['clicks']).round(0)
        
        if 'orders' in df.columns:
            df['CPA'] = (df['spend'] / df['orders'].replace(0, np.nan)).round(0)
        
        df['BEP'] = bep
        
        # Fungsi analisis
        def analisis(row):
            rekomendasi = []
            prioritas = 4
            masalah = []
            
            # CTR rendah
            if row['CTR'] < ctr_threshold:
                rekomendasi.append(f"🔴 Ganti visual & hook (CTR {row['CTR']}% < {ctr_threshold}%)")
                masalah.append("CTR rendah")
                prioritas = 1
            
            # ROAS di bawah BEP
            if row['ROAS'] < row['BEP']:
                rekomendasi.append(f"🟠 ROAS {row['ROAS']} < BEP {row['BEP']} → Naikkan target ROAS")
                masalah.append("ROAS rendah")
                prioritas = min(prioritas, 2)
            
            # Klik ada, order 0
            if row['clicks'] > 30 and 'orders' in df.columns:
                if row.get('orders', 0) == 0:
                    rekomendasi.append("🟠 Klik banyak ({:.0f}) tapi order 0 → Cek produk".format(row['clicks']))
                    masalah.append("Konversi 0")
                    prioritas = min(prioritas, 1)
            
            # CPC mahal
            if row['CPC'] > cpc_threshold:
                rekomendasi.append(f"💰 CPC Rp{row['CPC']:,.0f} > Rp{cpc_threshold:,.0f} → Perbaiki relevansi")
                masalah.append("CPC mahal")
                prioritas = min(prioritas, 3)
            
            # Iklan tidak terserap
            if row['impressions'] < 1000 and row['spend'] < 50000:
                rekomendasi.append("🎯 Iklan tidak terserap → Turunkan target ROAS")
                masalah.append("Tidak terserap")
                prioritas = min(prioritas, 2)
            
            # Jangkauan sempit
            if row['impressions'] < 5000 and row['ROAS'] > row['BEP'] * 1.5:
                rekomendasi.append("🟡 ROAS tinggi tapi jangkauan sempit → Longgarkan ROAS, naikkan budget")
                masalah.append("Distribusi sempit")
                prioritas = min(prioritas, 2)
            
            # Performa sehat
            if row['CTR'] >= ctr_threshold and row['ROAS'] >= row['BEP']:
                if 'orders' in df.columns and row.get('orders', 0) > 0:
                    rekomendasi.append("✅ Performa sehat → Scale naikkan budget 30%")
                    masalah.append("Sehat")
                    prioritas = min(prioritas, 3)
            
            if not rekomendasi:
                rekomendasi.append("⚠️ Data tidak cukup untuk analisis otomatis")
                masalah.append("Data tidak cukup")
            
            return {
                'rekomendasi': " | ".join(rekomendasi),
                'prioritas': prioritas,
                'masalah': ", ".join(masalah)
            }
        
        # Terapkan analisis
        hasil = df.apply(analisis, axis=1)
        df['rekomendasi'] = [x['rekomendasi'] for x in hasil]
        df['prioritas'] = [x['prioritas'] for x in hasil]
        df['masalah'] = [x['masalah'] for x in hasil]
        
        st.success(f"✅ {len(df)} iklan berhasil dianalisis")
        
        # ==================== METRIC CARDS ====================
        st.markdown("## 📊 Ringkasan Kinerja")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            avg_ctr = df['CTR'].mean()
            st.metric("Rata-rata CTR", f"{avg_ctr:.1f}%", 
                     delta="✅ Bagus" if avg_ctr >= ctr_threshold else "⚠️ Perlu perbaikan")
        
        with col2:
            avg_roas = df['ROAS'].mean()
            st.metric("Rata-rata ROAS", f"{avg_roas:.1f}x",
                     delta=f"Target: {bep}x")
        
        with col3:
            total_spend = df['spend'].sum()
            st.metric("Total Belanja Iklan", f"Rp{total_spend:,.0f}")
        
        with col4:
            total_sales = df['sales'].sum()
            st.metric("Total Omset", f"Rp{total_sales:,.0f}")
        
        with col5:
            bermasalah = len(df[df['prioritas'] <= 2])
            st.metric("Iklan Bermasalah", f"{bermasalah} / {len(df)}",
                     delta="⚠️ Perlu aksi" if bermasalah > 0 else "✅ Sehat")
        
        st.markdown("---")
        
        # ==================== TAB ====================
        tab1, tab2, tab3 = st.tabs(["📋 Tabel Detail", "🎯 Prioritas Aksi", "📈 Visualisasi"])
        
        with tab1:
            # Tabel lengkap
            kolom_tampil = []
            if 'campaign' in df.columns:
                kolom_tampil.append('campaign')
            kolom_tampil.extend(['CTR', 'ROAS', 'CPC', 'prioritas', 'masalah', 'rekomendasi'])
            
            st.dataframe(df[kolom_tampil], use_container_width=True)
        
        with tab2:
            # Prioritas aksi
            darurat = df[df['prioritas'] == 1]
            penting = df[df['prioritas'] == 2]
            optimasi = df[df['prioritas'] == 3]
            
            if len(darurat) > 0:
                st.markdown("### 🔴 TINDAKAN SEGERA")
                for _, row in darurat.iterrows():
                    nama = row.get('campaign', 'Iklan')
                    st.markdown(f"""
                    <div class="warning-card">
                        <b>⚠️ {nama}</b><br>
                        {row['rekomendasi']}<br>
                        <small>CTR: {row['CTR']}% | ROAS: {row['ROAS']}x | Spend: Rp{row['spend']:,.0f}</small>
                    </div>
                    """, unsafe_allow_html=True)
            
            if len(penting) > 0:
                st.markdown("### 🟠 PERLU OPTIMASI")
                for _, row in penting.iterrows():
                    nama = row.get('campaign', 'Iklan')
                    st.markdown(f"""
                    <div class="warning-card">
                        <b>📊 {nama}</b><br>
                        {row['rekomendasi']}
                    </div>
                    """, unsafe_allow_html=True)
            
            if len(optimasi) > 0:
                st.markdown("### 🟡 PANTAU & SCALE")
                for _, row in optimasi.iterrows():
                    nama = row.get('campaign', 'Iklan')
                    st.write(f"- **{nama}**: {row['rekomendasi']}")
        
        with tab3:
            # Grafik
            col_chart1, col_chart2 = st.columns(2)
            
            with col_chart1:
                fig_ctr = px.bar(
                    df.head(10), 
                    x=df.head(10).index, 
                    y='CTR',
                    title='Top 10 - CTR (%)',
                    color='CTR',
                    color_continuous_scale=['red', 'yellow', 'green']
                )
                fig_ctr.add_hline(y=ctr_threshold, line_dash="dash", line_color="orange")
                st.plotly_chart(fig_ctr, use_container_width=True)
            
            with col_chart2:
                fig_roas = px.bar(
                    df.head(10),
                    x=df.head(10).index,
                    y='ROAS',
                    title='Top 10 - ROAS',
                    color='ROAS',
                    color_continuous_scale=['red', 'yellow', 'green']
                )
                fig_roas.add_hline(y=bep, line_dash="dash", line_color="orange")
                st.plotly_chart(fig_roas, use_container_width=True)
            
            # Scatter plot
            fig_scatter = px.scatter(
                df, x='CTR', y='ROAS',
                color='prioritas',
                color_continuous_scale=['red', 'orange', 'yellow', 'green'],
                hover_data=['campaign'] if 'campaign' in df.columns else None,
                title='Peta Posisi Iklan'
            )
            fig_scatter.add_vline(x=ctr_threshold, line_dash="dash", line_color="red")
            fig_scatter.add_hline(y=bep, line_dash="dash", line_color="red")
            st.plotly_chart(fig_scatter, use_container_width=True)
        
        # ==================== DOWNLOAD ====================
        st.markdown("---")
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Hasil Analisis (CSV)",
            data=csv,
            file_name=f"ads_doctor_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv"
        )

else:
    # Tampilan awal sebelum upload
    st.info("👈 **Upload file CSV** untuk memulai analisis")
    
    with st.expander("📖 Lihat contoh format CSV yang diterima"):
        st.markdown("""
        **Kolom minimal yang diperlukan:**
        - `impressions` / tayang / impresi
        - `clicks` / klik
        - `spend` / biaya / cost
        - `sales` / omset / revenue
        
        **Contoh data:**
        """)
        contoh = pd.DataFrame({
            'campaign': ['Campaign A', 'Campaign B'],
            'impressions': [10000, 8000],
            'clicks': [300, 120],
            'spend': [90000, 80000],
            'sales': [600000, 300000],
            'orders': [6, 2]
        })
        st.dataframe(contoh)

# ==================== FOOTER ====================
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>🩺 Ads Doctor Pro | Berdasarkan Framework GMV Max Shopee & TikTok</p>", 
    unsafe_allow_html=True
                         )
