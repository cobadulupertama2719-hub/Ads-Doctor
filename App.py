import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import hashlib
import requests
import json

# ==================== 1. ELITE UI CONFIGURATION ====================
def apply_premium_style():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700;800&display=swap');
    
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; color: #F8FAFC; }
    .stApp { background: radial-gradient(circle at 2% 2%, #1e1b4b 0%, #020617 100%); }

    /* Luxury Glassmorphism Card */
    .premium-card {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 30px;
        margin-bottom: 25px;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5);
    }
    
    .gold-header {
        background: linear-gradient(135deg, #FFD700 0%, #B8860B 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }

    /* Premium Button */
    .stButton>button {
        background: linear-gradient(135deg, #00E5A0 0%, #00a878 100%);
        color: #020617 !important; font-weight: 800; border: none; border-radius: 15px;
        padding: 18px; transition: all 0.3s ease; text-transform: uppercase; letter-spacing: 1.5px;
    }
    .stButton>button:hover { transform: translateY(-3px); box-shadow: 0 15px 35px rgba(0, 229, 160, 0.4); }

    /* Custom Inputs */
    .stNumberInput input, .stTextInput input, .stSelectbox div {
        background: rgba(0,0,0,0.4) !important; border-radius: 12px !important; color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ==================== 2. CORE LOGIC & SECURITY ====================
for key, val in {
    "authenticated": False, "demo_mode": False, "demo_start_time": None,
    "demo_analysis_count": 0, "demo_generator_count": 0, "products": []
}.items():
    if key not in st.session_state: st.session_state[key] = val

ADMIN_USERNAME = "arkidigital"
ADMIN_PASSWORD = "Arkidigital2026"
[span_3](start_span)CHECKOUT_LINK = "https://muhammad-masruri.myscalev.com/checkout-pageku"[span_3](end_span)
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")

def call_gemini(prompt):
    if not GEMINI_API_KEY: return None
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    try:
        r = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=15)
        return r.json()["candidates"][0]["content"]["parts"][0]["text"]
    except: return None

def format_rp(angka):
    if angka >= 1_000_000: return f"Rp{angka/1_000_000:.1f}JT"
    if angka >= 1000: return f"Rp{angka/1000:.0f}RB"
    [span_4](start_span)return f"Rp{angka:,.0f}"[span_4](end_span)

# ==================== 3. LOGIN INTERFACE ====================
def show_login():
    apply_premium_style()
    st.markdown('<div style="text-align:center; padding-top:80px;">', unsafe_allow_html=True)
    st.markdown('<h1 class="gold-header" style="font-size:3.5rem;">🩺 DOCTOR ADS ELITE</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#94A3B8; font-size:1.2rem;">Predictive Ad Analytics & AI Strategy Lab</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="large")
    with col1:
        with st.form("login"):
            st.markdown("### 🔐 Member Access")
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.form_submit_button("UNLOCK DASHBOARD"):
                if u == ADMIN_USERNAME and p == ADMIN_PASSWORD:
                    [span_5](start_span)st.session_state.authenticated = True; st.rerun()[span_5](end_span)
                else: st.error("Wrong Password!")
    with col2:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown("### 🎁 Trial Access")
        st.write("Coba analisis AI kami selama 5 menit secara gratis.")
        if st.button("START FREE TRIAL"):
            [span_6](start_span)st.session_state.demo_mode = True; st.session_state.demo_start_time = datetime.now(); st.rerun()[span_6](end_span)
        st.markdown('</div>', unsafe_allow_html=True)

# ==================== 4. MAIN ELITE DASHBOARD ====================
def main():
    st.set_page_config(page_title="Doctor Ads Elite", page_icon="🩺", layout="wide")
    apply_premium_style()

    if not st.session_state.authenticated and not st.session_state.demo_mode:
        show_login(); st.stop()

    if st.session_state.demo_mode:
        elapsed = (datetime.now() - st.session_state.demo_start_time).total_seconds()
        [span_7](start_span)[span_8](start_span)if elapsed > 300: st.warning("Trial Expired!"); st.stop()[span_7](end_span)[span_8](end_span)

    # --- TOP SECTION: FINANCIAL AUDIT ---
    [span_9](start_span)st.markdown('<h1 class="gold-header">🩺 DASHBOARD UTAMA</h1>', unsafe_allow_html=True)[span_9](end_span)
    
    c_f1, c_f2 = st.columns([2, 1])
    with c_f1:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        [span_10](start_span)st.markdown("### 🎯 Elite ROAS BEP Calculator")[span_10](end_span)
        col_b1, col_b2, col_b3 = st.columns(3)
        hj = col_b1.number_input("Harga Jual (Rp)", value=150000, step=5000)
        modal = col_b2.number_input("Modal / HPP (Rp)", value=75000, step=5000)
        admin_p = col_b3.slider("Admin %", 5, 30, 20)
        [span_11](start_span)target_p = st.number_input("Target Profit (Rp)", value=0)[span_11](end_span)
        
        laba = hj - modal - (hj * admin_p/100) - target_p
        roas_bep = hj / laba if laba > 0 else 999
        [span_12](start_span)st.markdown(f'<h2 style="color:#00E5A0; text-align:center;">TARGET ROAS BEP: {roas_bep:.1f}x</h2>', unsafe_allow_html=True)[span_12](end_span)
        st.markdown('</div>', unsafe_allow_html=True)

    with c_f2:
        st.markdown('<div class="premium-card" style="height:100%;">', unsafe_allow_html=True)
        [span_13](start_span)st.markdown("### 📋 Kelayakan Produk")[span_13](end_span)
        [span_14](start_span)pernah = st.radio("Pernah Laku?", ["Ya", "Tidak"], horizontal=True)[span_14](end_span)
        [span_15](start_span)if pernah == "Tidak": st.error("❌ Jangan iklan dulu!")[span_15](end_span)
        else:
            [span_16](start_span)h_komp = st.number_input("Harga Kompetitor", value=140000)[span_16](end_span)
            [span_17](start_span)if hj > h_komp * 1.2: st.warning("⚠️ Harga terlalu tinggi.")[span_17](end_span)
            [span_18](start_span)elif laba < 5000: st.error("❌ Margin terlalu tipis.")[span_18](end_span)
            [span_19](start_span)else: st.success("✅ Layak Iklan!")[span_19](end_span)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- MAIN SECTION: AD PERFORMANCE ---
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    [span_20](start_span)[span_21](start_span)st.markdown("### 📊 Performance Analytics")[span_20](end_span)[span_21](end_span)
    c_p1, c_p2, c_p3 = st.columns(3)
    [span_22](start_span)imp = c_p1.number_input("👁️ Impressions", value=20000)[span_22](end_span)
    [span_23](start_span)clk = c_p1.number_input("🖱️ Clicks", value=600)[span_23](end_span)
    [span_24](start_span)spent = c_p2.number_input("💸 Spent (Rp)", value=150000)[span_24](end_span)
    [span_25](start_span)rev = c_p2.number_input("💰 Omset (Rp)", value=900000)[span_25](end_span)
    [span_26](start_span)ords = c_p3.number_input("📦 Orders", value=8)[span_26](end_span)
    [span_27](start_span)b_set = c_p3.number_input("💵 Budget Set", value=200000)[span_27](end_span)
    
    [span_28](start_span)if st.button("RUN DEEP ANALYTICS", use_container_width=True):[span_28](end_span)
        [span_29](start_span)ctr = (clk/imp*100) if imp > 0 else 0[span_29](end_span)
        [span_30](start_span)roas = (rev/spent) if spent > 0 else 0[span_30](end_span)
        [span_31](start_span)s_rate = (spent/b_set*100) if b_set > 0 else 0[span_31](end_span)
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("CTR", f"{ctr:.2f}%")
        m2.metric("ROAS Aktual", f"{roas:.2f}x")
        [span_32](start_span)m3.metric("Status BEP", "UNSAFE" if roas < roas_bep else "SAFE")[span_32](end_span)
        [span_33](start_span)m4.metric("Est. Profit", format_rp(laba * ords - spent))[span_33](end_span)

        # REKOMENDASI ASLI
        st.markdown("---")
        if clk > 50 and s_rate >= 80 and ords == 0:
            [span_34](start_span)st.error(f"🔴 PRIORITAS 1: STOP IKLAN! Klik {clk}, Budget {s_rate:.0f}%, 0 Order.")[span_34](end_span)
        elif s_rate >= 85 and roas >= roas_bep * 1.2:
            [span_35](start_span)st.success(f"🟢 PRIORITAS 4: SCALE UP! Naikkan budget ke {format_rp(b_set*1.3)}.")[span_35](end_span)
        elif roas >= roas_bep and s_rate < 85:
            [span_36](start_span)st.warning("🟡 PRIORITAS 2: OPTIMASI. Turunkan Target ROAS 0.5 poin.")[span_36](end_span)
        
        [span_37](start_span)if ctr < 2: st.info(f"📸 CTR RENDAH ({ctr:.1f}%). Ganti Visual Produk!")[span_37](end_span)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- AI COPYWRITING LAB ---
    st.markdown("### ✨ AI Creative Lab")
    p_name = st.text_input("🏷️ Product Name", placeholder="Masukkan Nama Produk...")
    [span_38](start_span)tabs = st.tabs(["🛍️ Shopee SEO", "🎥 TikTok Story", "🎬 Hooks", "#️⃣ Hashtags"])[span_38](end_span)
    
    with tabs[0]:
        if st.button("Generate Elite Shopee Title"):
            res = call_gemini(f"Buat 5 Judul Shopee Premium SEO untuk {p_name}")
            [span_39](start_span)st.code(res if res else f"🔥 {p_name} Best Seller", language="text")[span_39](end_span)
    
    with tabs[1]:
        if st.button("Generate TikTok Viral Story"):
            res = call_gemini(f"Buat copy TikTok storytelling emosional untuk {p_name}")
            [span_40](start_span)st.code(res if res else "Dulu aku...", language="markdown")[span_40](end_span)

    [span_41](start_span)st.markdown('<div style="text-align:center; padding:50px; color:#64748B;">© 2026 Arkidigital Premier</div>', unsafe_allow_html=True)[span_41](end_span)

if __name__ == "__main__": main()
