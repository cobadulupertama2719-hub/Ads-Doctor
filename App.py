import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(page_title="Ads Doctor", page_icon="🩺", layout="wide")

# Header
st.title("🩺 Ads Doctor")
st.markdown("##### *Upload CSV Iklan TikTok/Shopee → Dapat Rekomendasi Perbaikan*")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.markdown("## ⚙️ Pengaturan")
    bep = st.number_input("🎯 ROAS BEP (target minimal)", value=5.0, step=0.5)
    ctr_threshold = st.slider("📊 Minimal CTR (%)", 0.5, 5.0, 2.0, 0.5)
    st.markdown("---")
    st.caption("📌 Framework GMV Max Shopee & TikTok")

# Upload file
uploaded = st.file_uploader("📂 Upload CSV dari TikTok/Shopee Ads", type=["csv"])

if uploaded:
    with st.spinner("🔍 Menganalisis..."):
        df = pd.read_csv(uploaded)
        
        # Cari kolom yang diperlukan
        for col in df.columns:
            col_lower = col.lower()
            if 'impression' in col_lower or 'tayang' in col_lower:
                df.rename(columns={col: 'impressions'}, inplace=True)
            if 'click' in col_lower or 'klik' in col_lower:
                df.rename(columns={col: 'clicks'}, inplace=True)
            if 'spend' in col_lower or 'biaya' in col_lower or 'cost' in col_lower:
                df.rename(columns={col: 'spend'}, inplace=True)
            if 'sales' in col_lower or 'omset' in col_lower or 'revenue' in col_lower:
                df.rename(columns={col: 'sales'}, inplace=True)
        
        # Hitung metrik
        df['CTR'] = (df['clicks'] / df['impressions'] * 100).round(2)
        df['ROAS'] = (df['sales'] / df['spend']).round(2)
        df['BEP'] = bep
        
        # Analisis
        def rekomendasi(row):
            if row['CTR'] < ctr_threshold:
                return f"🔴 Ganti visual & hook (CTR {row['CTR']}% < {ctr_threshold}%)"
            elif row['ROAS'] < row['BEP']:
                return f"🟠 ROAS {row['ROAS']} < BEP {row['BEP']} → Naikkan target ROAS"
            elif row['ROAS'] >= row['BEP']:
                return "✅ Performa sehat → Scale naikkan budget 30%"
            else:
                return "⚠️ Cek manual"
        
        df['rekomendasi'] = df.apply(rekomendasi, axis=1)
        
        # Tampilkan hasil
        st.success(f"✅ {len(df)} iklan dianalisis")
        
        # Metric
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Rata-rata CTR", f"{df['CTR'].mean():.1f}%")
        with col2:
            st.metric("Rata-rata ROAS", f"{df['ROAS'].mean():.1f}x")
        with col3:
            st.metric("Total Spend", f"Rp{df['spend'].sum():,.0f}")
        with col4:
            st.metric("Total Sales", f"Rp{df['sales'].sum():,.0f}")
        
        # Tabel
        st.subheader("📊 Hasil Analisis")
        tampil = []
        if 'campaign' in df.columns:
            tampil.append('campaign')
        tampil.extend(['CTR', 'ROAS', 'rekomendasi'])
        st.dataframe(df[tampil], use_container_width=True)
        
        # Prioritas
        st.subheader("🎯 Prioritas Tindakan")
        masalah = df[df['rekomendasi'].str.contains("🔴|🟠")]
        if len(masalah) > 0:
            st.warning(f"⚠️ {len(masalah)} iklan perlu tindakan")
            for _, row in masalah.iterrows():
                nama = row.get('campaign', 'Iklan')
                st.write(f"- **{nama}**: {row['rekomendasi']}")
        else:
            st.success("✅ Semua iklan dalam kondisi sehat")
        
        # Download
        st.download_button("📥 Download CSV", df.to_csv(index=False), "hasil_analisa.csv")

else:
    st.info("👈 Upload file CSV untuk memulai")
    
    with st.expander("📖 Contoh format CSV"):
        st.dataframe(pd.DataFrame({
            'campaign': ['Sepatu A', 'Jaket B'],
            'impressions': [10000, 8000],
            'clicks': [300, 120],
            'spend': [90000, 80000],
            'sales': [600000, 300000]
        }))

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>🩺 Ads Doctor | Framework GMV Max</p>", unsafe_allow_html=True)
