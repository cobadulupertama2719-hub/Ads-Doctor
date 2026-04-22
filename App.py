import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
import base64
from datetime import datetime

# ==================== KONFIGURASI HALAMAN ====================
st.set_page_config(
    page_title="Ads Doctor Pro",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
    /* Font & Background */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Card styling */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 1rem;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .warning-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 1rem;
        color: white;
    }
    
    .success-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1rem;
        border-radius: 1rem;
        color: white;
    }
    
    /* Custom button */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    /* Dataframe styling */
    .dataframe {
        border-radius: 0.5rem;
        overflow: hidden;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

# ==================== SESSION STATE ====================
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False
if 'analysis_done' not in st.session_state:
    st.session_state.analysis_done = False

# ==================== SIDEBAR ====================
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/advertising.png", width=60)
    st.title("⚙️ Pengaturan")
    
    # Dark mode toggle
    st.session_state.dark_mode = st.toggle("🌙 Dark Mode", value=st.session_state.dark_mode)
    
    st.markdown("---")
    
    # Input BEP
    st.subheader("🎯 Target Bisnis")
    bep_default = st.number_input(
        "ROAS BEP (minimal agar tidak rugi)", 
        value=5.0, 
        step=0.5,
        help="Hitung: Harga Jual ÷ (Harga Jual - HPP - Admin - Target Profit)"
    )
    
    st.markdown("---")
    
    # Threshold settings
    st.subheader("📊 Threshold")
    ctr_threshold = st.slider("Minimal CTR (%)", 0.5, 5.0, 2.0, 0.5)
    cpc_threshold = st.number_input("Maksimal CPC (Rp)", 1000, 10000, 3000, 500)
    
    st.markdown("---")
    
    # Help section
    with st.expander("❓ Cara Baca Hasil"):
        st.markdown("""
        - 🔴 **Prioritas 1**: Tindakan segera (stop atau ganti visual)
        - 🟠 **Prioritas 2**: Optimasi dalam 1-2 hari
        - 🟡 **Prioritas 3**: Scale / pantau
        - ✅ **Sehat**: Lanjutkan strategi
        
        **Rumus Cepat:**
        - CTR < 2% → Ganti visual
        - ROAS < BEP → Rugi, naikkan target ROAS
        - Klik ada, order 0 → Cek produk
        """)

# ==================== MAIN HEADER ====================
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.markdown("# 🩺 **Ads Doctor Pro**")
    st.markdown("##### *Analisis Iklan TikTok & Shopee → Langsung Dapat Rekomendasi*")
    st.markdown("---")

# ==================== UPLOAD SECTION ====================
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
        kolom_mapping = {
            'impressions': ['impressions', 'tayang', 'impresi', 'impression'],
            'clicks': ['clicks', 'klik', 'click'],
            'spend': ['spend', 'biaya', 'cost', 'pengeluaran', 'amount_spent'],
            'sales': ['sales', 'omset', 'revenue', 'penjualan', 'conversion_value'],
            'orders': ['orders', 'order', 'pesanan', 'konversi', 'purchase']
        }
        
        for target, possibilities in kolom_mapping.items():
            for col in df.columns:
                if col.lower() in [p.lower() for p in possibilities]:
                    df.rename(columns={col: target}, inplace=True)
                    break
        
        # Cek kolom wajib
        kolom_wajib = ['impressions', 'clicks', 'spend', 'sales']
        missing = [k for k in kolom_wajib if k not in df.columns]
        
        if missing:
            st.error(f"❌ CSV tidak memiliki kolom: {missing}")
            st.info(f"Kolom yang tersedia: {list(df.columns)}")
            st.stop()
        
        # Hitung metrik
        df['CTR'] = (df['clicks'] / df['impressions'] * 100).round(2)
        df['ROAS'] = (df['sales'] / df['spend']).round(2)
        df['CPC'] = (df['spend'] / df['clicks']).round(0)
        df['CPA'] = (df['spend'] / df['orders'].replace(0, np.nan)).round(0)
        df['BEP'] = bep_default
        
        # ==================== FUNGSI ANALISIS ====================
        def analisis_lengkap(row):
            rekomendasi = []
            prioritas = 4
            masalah = []
            
            # Rule 1: CTR rendah
            if row['CTR'] < ctr_threshold:
                rekomendasi.append(f"🔴 **Ganti visual & hook** (CTR {row['CTR']}% < {ctr_threshold}%)")
                masalah.append("CTR rendah")
                prioritas = min(prioritas, 1)
            
            # Rule 2: ROAS di bawah BEP
            if row['ROAS'] < row['BEP']:
                selisih = row['BEP'] - row['ROAS']
                rekomendasi.append(f"🟠 **ROAS {row['ROAS']} di bawah BEP {row['BEP']}** (rugi Rp{row['spend'] * selisih:,.0f}) → Naikkan target ROAS")
                masalah.append("ROAS rendah")
                prioritas = min(prioritas, 2)
            
            # Rule 3: Klik banyak tapi order 0
            if row['clicks'] > 30 and row.get('orders', 0) == 0:
                rekomendasi.append("🟠 **Klik banyak ({:.0f}) tapi order 0** → Cek harga, review, deskripsi produk".format(row['clicks']))
                masalah.append("Konversi 0")
                prioritas = min(prioritas, 1)
            
            # Rule 4: CPC mahal
            if row['CPC'] > cpc_threshold:
                rekomendasi.append(f"💰 **CPC Rp{row['CPC']:,.0f} > Rp{cpc_threshold:,.0f}** → Perbaiki relevansi audience")
                masalah.append("CPC mahal")
                prioritas = min(prioritas, 3)
            
            # Rule 5: Iklan tidak terserap
            if row['impressions'] < 1000 and row['spend'] < 50000:
                rekomendasi.append("🎯 **Iklan tidak terserap** → Turunkan target ROAS 1 poin")
                masalah.append("Tidak terserap")
                prioritas = min(prioritas, 2)
            
            # Rule 6: Jangkauan sempit
            if row['impressions'] < 5000 and row['ROAS'] > row['BEP'] * 1.5:
                rekomendasi.append("🟡 **ROAS tinggi tapi jangkauan sempit** → Longgarkan target ROAS, naikkan budget 20%")
                masalah.append("Distribusi sempit")
                prioritas = min(prioritas, 2)
            
            # Rule 7: Performa sehat
            if row['CTR'] >= ctr_threshold and row['ROAS'] >= row['BEP'] and row.get('orders', 0) > 0:
                rekomendasi.append("✅ **Performa sehat** → Scale naikkan budget 30%, pantau 7 hari")
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
        hasil = df.apply(lambda row: analisis_lengkap(row), axis=1)
        df['rekomendasi'] = [x['rekomendasi'] for x in hasil]
        df['prioritas'] = [x['prioritas'] for x in hasil]
        df['masalah'] = [x['masalah'] for x in hasil]
        
        st.session_state.analysis_done = True
        st.session_state.df = df
        
        st.success("✅ Analisis selesai!")

# ==================== TAMPILAN HASIL ====================
if st.session_state.analysis_done and 'df' in st.session_state:
    df = st.session_state.df
    
    # ==================== METRIC CARDS ====================
    st.subheader("📊 **Ringkasan Kinerja**")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        avg_ctr = df['CTR'].mean()
        st.metric("Rata-rata CTR", f"{avg_ctr:.1f}%", 
                  delta="✅ Bagus" if avg_ctr >= ctr_threshold else "⚠️ Perlu perbaikan")
    
    with col2:
        avg_roas = df['ROAS'].mean()
        st.metric("Rata-rata ROAS", f"{avg_roas:.1f}x",
                  delta=f"Target: {bep_default}x")
    
    with col3:
        total_spend = df['spend'].sum()
        st.metric("Total Belanja Iklan", f"Rp{total_spend:,.0f}")
    
    with col4:
        total_sales = df['sales'].sum()
        st.metric("Total Omset", f"Rp{total_sales:,.0f}")
    
    with col5:
        iklan_bermasalah = len(df[df['prioritas'] <= 2])
        st.metric("Iklan Bermasalah", f"{iklan_bermasalah} / {len(df)}",
                  delta="⚠️ Perlu aksi" if iklan_bermasalah > 0 else "✅ Semua sehat")
    
    st.markdown("---")
    
    # ==================== GRAFIK ====================
    tab1, tab2, tab3 = st.tabs(["📈 Visualisasi", "📋 Tabel Detail", "🎯 Prioritas Aksi"])
    
    with tab1:
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            # Bar chart CTR vs Threshold
            fig_ctr = go.Figure()
            fig_ctr.add_trace(go.Bar(
                x=df.index[:10] if len(df) > 10 else df.index,
                y=df['CTR'][:10] if len(df) > 10 else df['CTR'],
                name='CTR (%)',
                marker_color=['red' if x < ctr_threshold else 'green' for x in df['CTR'][:10] if len(df) > 10 else df['CTR']]
            ))
            fig_ctr.add_hline(y=ctr_threshold, line_dash="dash", line_color="orange", 
                              annotation_text=f"Threshold: {ctr_threshold}%")
            fig_ctr.update_layout(title="Top 10 Campaign - CTR", height=400)
            st.plotly_chart(fig_ctr, use_container_width=True)
        
        with col_chart2:
            # Bar chart ROAS vs BEP
            fig_roas = go.Figure()
            fig_roas.add_trace(go.Bar(
                x=df.index[:10] if len(df) > 10 else df.index,
                y=df['ROAS'][:10] if len(df) > 10 else df['ROAS'],
                name='ROAS',
                marker_color=['red' if x < bep_default else 'green' for x in df['ROAS'][:10] if len(df) > 10 else df['ROAS']]
            ))
            fig_roas.add_hline(y=bep_default, line_dash="dash", line_color="orange",
                               annotation_text=f"BEP: {bep_default}x")
            fig_roas.update_layout(title="Top 10 Campaign - ROAS", height=400)
            st.plotly_chart(fig_roas, use_container_width=True)
        
        # Scatter plot CTR vs ROAS
        fig_scatter = px.scatter(
            df, x='CTR', y='ROAS', 
            color='prioritas',
            color_continuous_scale=['red', 'orange', 'yellow', 'green'],
            hover_data=['campaign' if 'campaign' in df.columns else df.index],
            title="Peta Posisi Iklan (CTR vs ROAS)"
        )
        fig_scatter.add_vline(x=ctr_threshold, line_dash="dash", line_color="red")
        fig_scatter.add_hline(y=bep_default, line_dash="dash", line_color="red")
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    with tab2:
        # Tabel lengkap
        kolom_tampil = []
        if 'campaign' in df.columns:
            kolom_tampil.append('campaign')
        kolom_tampil.extend(['CTR', 'ROAS', 'CPC', 'prioritas', 'masalah', 'rekomendasi'])
        
        st.dataframe(
            df[kolom_tampil], 
            use_container_width=True,
            column_config={
                "CTR": st.column_config.NumberColumn("CTR (%)", format="%.2f"),
                "ROAS": st.column_config.NumberColumn("ROAS", format="%.2f"),
                "CPC": st.column_config.NumberColumn("CPC (Rp)", format="Rp%.0f"),
                "prioritas": st.column_config.NumberColumn("Prioritas"),
            }
        )
    
    with tab3:
        # Prioritas aksi
        st.subheader("🎯 **Rekomendasi Tindakan Hari Ini**")
        
        darurat = df[df['prioritas'] == 1]
        penting = df[df['prioritas'] == 2]
        optimasi = df[df['prioritas'] == 3]
        sehat = df[df['prioritas'] == 4]
        
        if len(darurat) > 0:
            with st.container():
                st.markdown("### 🔴 **TINDAKAN SEGERA (Prioritas 1)**")
                for idx, row in darurat.iterrows():
                    nama = row.get('campaign', f'Iklan {idx+1}')
                    with st.expander(f"⚠️ {nama} - {row['masalah']}"):
                        st.write(f"**Rekomendasi:** {row['rekomendasi']}")
                        st.write(f"**Data:** CTR {row['CTR']}% | ROAS {row['ROAS']}x | Spend Rp{row['spend']:,.0f}")
        
        if len(penting) > 0:
            with st.container():
                st.markdown("### 🟠 **OPTIMASI (Prioritas 2)**")
                for idx, row in penting.iterrows():
                    nama = row.get('campaign', f'Iklan {idx+1}')
                    with st.expander(f"📊 {nama} - {row['masalah']}"):
                        st.write(f"**Rekomendasi:** {row['rekomendasi']}")
                        st.write(f"**Data:** CTR {row['CTR']}% | ROAS {row['ROAS']}x")
        
        if len(optimasi) > 0:
            with st.container():
                st.markdown("### 🟡 **PANTAU & SCALE (Prioritas 3)**")
                for idx, row in optimasi.iterrows():
                    nama = row.get('campaign', f'Iklan {idx+1}')
                    st.write(f"- **{nama}**: {row['rekomendasi']}")
        
        if len(sehat) > 0:
            st.success(f"✅ {len(sehat)} iklan dalam kondisi sehat")
    
    # ==================== EXPORT ====================
    st.markdown("---")
    col_export1, col_export2, col_export3 = st.columns([1, 1, 2])
    
    with col_export1:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"ads_doctor_report_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    with col_export2:
        if st.button("🔄 Analisis Ulang"):
            st.session_state.analysis_done = False
            st.rerun()
    
    with col_export3:
        st.caption("💡 Tips: Export hasil untuk dokumentasi atau konsultasi tim")

else:
    st.info("👈 **Upload file CSV** di sidebar atau tombol di atas untuk memulai analisis")
    
    # Contoh format CSV
    with st.expander("📖 **Lihat contoh format CSV yang diterima**"):
        st.markdown("""
        Kolom minimal yang diperlukan:
        - `impressions` / `tayang` / `impresi`
        - `clicks` / `klik`
        - `spend` / `biaya` / `cost`
        - `sales` / `omset` / `revenue`
        
        **Opsional (lebih akurat):**
        - `orders` / `order` / `pesanan`
        - `campaign` / `nama_iklan`
        """)
        
        # Contoh data
        contoh_data = pd.DataFrame({
            'campaign': ['Campaign A', 'Campaign B'],
            'impressions': [10000, 8000],
            'clicks': [300, 120],
            'spend': [90000, 80000],
            'sales': [600000, 300000],
            'orders': [6, 2]
        })
        st.dataframe(contoh_data)

# ==================== FOOTER ====================
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>🩺 Ads Doctor Pro | Berdasarkan Framework GMV Max</p>", 
    unsafe_allow_html=True
)
