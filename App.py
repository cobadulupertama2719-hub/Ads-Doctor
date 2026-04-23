import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import hashlib
import time

# ==================== BACA API KEY DARI SECRETS ====================
try:
    if "GEMINI_API_KEY" in st.secrets:
        GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
        AI_AVAILABLE = True
    else:
        GEMINI_API_KEY = None
        AI_AVAILABLE = False
        st.warning("⚠️ API Key Gemini tidak ditemukan di Secrets. Fitur AI akan menggunakan template statis.")
except Exception as e:
    GEMINI_API_KEY = None
    AI_AVAILABLE = False
    st.warning(f"⚠️ Secrets tidak terbaca: {e}. Pastikan API Key sudah disimpan di dashboard Streamlit.")

# ==================== INISIALISASI GEMINI ====================
if AI_AVAILABLE:
    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        st.success("✅ AI Gemini aktif! Generator akan menghasilkan konten AI.")
    except ImportError:
        AI_AVAILABLE = False
        st.warning("⚠️ Library Google Generative AI belum terinstall. Jalankan: pip install google-generativeai")
    except Exception as e:
        AI_AVAILABLE = False
        st.warning(f"⚠️ Gagal inisialisasi Gemini: {e}")
else:
    st.warning("⚠️ AI tidak tersedia. Generator akan menggunakan template statis.")
    
# ==================== FUNGSI AI GENERATOR ====================
def generate_with_ai(mode, jenis, produk, extra_info=""):
    """Generate konten dengan Gemini AI, fallback ke template jika error"""
    if not AI_READY:
        return generate_template_fallback(mode, jenis, produk)
    
    prompt_templates = {
        "shopee_title": f"""Buatkan 5 judul produk untuk '{produk}' di Shopee.
Rules: 
- Gunakan bahasa Indonesia yang menarik
- Tambahkan emoji yang relevan (🔥, ✨, 💯, 🛒)
- Fokus pada MANFAAT produk
- Panjang judul maksimal 60 karakter
- Tambahkan kata kunci: kualitas premium, best seller, harga terjangkau {extra_info}
- Output format: satu judul per baris, tidak perlu nomor""",

        "shopee_desc": f"""Buatkan deskripsi produk untuk '{produk}' di Shopee.
Rules:
- Gunakan bahasa Indonesia yang persuasif
- Format: gunakan emoji sebagai bullet points (✅, 📏, 🎯, 💬)
- Sertakan: bahan berkualitas, size lengkap, garansi
- Panjang: 150-200 kata
- Tambahkan ajakan beli di akhir
- Informasi tambahan: {extra_info}""",

        "shopee_hook": f"""Buatkan 5 hook video untuk produk '{produk}' di Shopee.
Rules:
- Hook adalah kalimat pembuka 3-5 detik pertama video
- Fokus pada promo, diskon, atau manfaat produk
- Gunakan emoji dan huruf besar untuk kata kunci
- Contoh gaya: "🔥 DISKON 50%!", "📦 FREE ONGKIR!"
- Output: satu hook per baris""",

        "tiktok_title": f"""Buatkan 5 judul VIRAL untuk produk '{produk}' di TikTok.
Rules:
- Gunakan bahasa Indonesia yang emosional dan engaging
- Wajib ada emoji (😭, 🤯, 🫣, 💗, 🔥, ⚡)
- Gunakan kata: VIRAL, WAJIB PUNYA, AUTO, STOP, RAHASIA
- Fokus pada pain point customer dan solusi {extra_info}
- Output: satu judul per baris""",

        "tiktok_desc": f"""Buatkan deskripsi storytelling untuk produk '{produk}' di TikTok.
Rules:
- Gaya: curhat/personal (aku/dulu/sekarang)
- Ceritakan transformasi setelah pakai produk
- Gunakan emoji, huruf kapital untuk penekanan
- Sertakan ajakan beli dan hashtag #viral #fyp
- Informasi tambahan: {extra_info}""",

        "tiktok_hook": f"""Buatkan 5 hook VIRAL untuk video TikTok produk '{produk}'.
Rules:
- Hook 3 detik pertama yang bikin orang BERHENTI SCROLL
- Gunakan gaya: problem solver, diskon, bukti sosial, curiosity, emosional
- Contoh: "😫 Capek cari {produk} yang nyaman? STOP!"
- Output: satu hook per baris"""
    }
    
    key = f"{mode}_{jenis}"
    prompt = prompt_templates.get(key, "")
    
    if not prompt:
        return generate_template_fallback(mode, jenis, produk)
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.warning(f"AI Error: {e}. Menggunakan template.")
        return generate_template_fallback(mode, jenis, produk)

def generate_template_fallback(mode, jenis, produk):
    """Template statis jika AI tidak tersedia"""
    if mode == "shopee" and jenis == "title":
        return f"🔥 {produk} - Kualitas Premium\n💯 {produk} BEST SELLER\n✨ WAJIB PUNYA! {produk}\n🎯 {produk} Dijamin Nyaman\n💎 {produk} PREMIUM QUALITY"
    elif mode == "shopee" and jenis == "desc":
        return f"✨ {produk} - Kualitas Premium Harga Terjangkau!\n\n✅ Bahan Berkualitas\n✅ Desain Modern\n✅ Size Lengkap\n✅ Garansi 100%\n\n🔥 Promo Terbatas! Order sekarang."
    elif mode == "shopee" and jenis == "hook":
        return f"🛍️ {produk} - Kualitas Premium!\n📦 {produk} - FREE ONGKIR!\n⭐ {produk} - Rating 4.9/5!"
    elif mode == "tiktok" and jenis == "title":
        return f"😭 STOP! Jangan beli {produk}!\n🔥 VIRAL! {produk} yang lagi hype!\n💯 WAJIB PUNYA! {produk} auto percaya diri!"
    elif mode == "tiktok" and jenis == "desc":
        return f"Dulu aku selalu... TAPI setelah pake {produk}, semuanya berubah! 😭\n✨ Bahan premium\n✅ Desain kekinian\n🔥 PROMO TERBATAS! #viral #fyp"
    else:
        return f"😫 Capek cari {produk}? STOP!\n🔥 DISKON 50% {produk}!\n🏆 {produk} best seller!"

# ==================== FUNGSI AI SUMMARY (Kesimpulan Otomatis) ====================
def generate_ai_summary(ctr, roas_aktual, roas_bep, budget_terserap_persen, clicks, orders, platform):
    """AI generate summary dari data analisis"""
    if not AI_READY:
        return None
    
    prompt = f"""
Anda adalah pakar iklan TikTok & Shopee. Berdasarkan data berikut, buatkan KESIMPULAN SINGKAT (maks 100 kata) + REKOMENDASI.

Data:
- CTR: {ctr:.1f}% (target minimal 2%)
- ROAS Aktual: {roas_aktual:.1f}x
- ROAS BEP: {roas_bep:.1f}x
- Budget terserap: {budget_terserap_persen:.0f}%
- Klik: {clicks}
- Order: {orders}
- Platform: {platform}

Buatkan analisis:
1. Apa masalah utamanya?
2. Apa yang harus dilakukan?
3. Prioritas tindakan (1-5)

Gunakan bahasa Indonesia yang profesional tapi mudah dipahami seller pemula.
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except:
        return None

# ==================== FUNGSI AI VISUAL RECOMMENDATION ====================
def generate_visual_recommendation(produk, ctr):
    """AI rekomendasi visual untuk CTR rendah"""
    if not AI_READY or ctr >= 2:
        return None
    
    prompt = f"""
Anda adalah desainer kreatif untuk iklan TikTok & Shopee.

Produk: {produk}
CTR saat ini: {ctr:.1f}% (di bawah standar 2%)

Buatkan rekomendasi perbaikan visual:
1. Saran warna background
2. Saran font dan tata letak
3. Saran hook untuk video (3 detik pertama)
4. Contoh teks yang bisa ditempel di video/foto

Output dalam bahasa Indonesia, format poin-poin, maksimal 150 kata.
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except:
        return None

# ==================== FUNGSI AI SCALE PREDICTION ====================
def generate_scale_prediction(roas_aktual, budget_set, roas_bep):
    """AI prediksi performa jika scale"""
    if not AI_READY or roas_aktual < roas_bep:
        return None
    
    new_budget = budget_set * 1.3
    prompt = f"""
Anda adalah pakar iklan. Prediksi performa jika naikkan budget 30%.

Data saat ini:
- ROAS: {roas_aktual:.1f}x
- Budget: Rp{budget_set:,.0f}/hari
- ROAS BEP: {roas_bep:.1f}x

Jika naikkan budget menjadi Rp{new_budget:,.0f}/hari:
1. Prediksi ROAS setelah scale (estimasi)
2. Estimasi profit tambahan per hari
3. Level resiko (Rendah/Sedang/Tinggi)
4. Tips agar scale berhasil

Output singkat, maksimal 100 kata.
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except:
        return None

# ==================== INISIALISASI SESSION STATE ====================
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "demo_mode" not in st.session_state:
    st.session_state["demo_mode"] = False
if "demo_start_time" not in st.session_state:
    st.session_state["demo_start_time"] = None
if "demo_analysis_count" not in st.session_state:
    st.session_state["demo_analysis_count"] = 0
if "demo_generator_count" not in st.session_state:
    st.session_state["demo_generator_count"] = 0
if "products" not in st.session_state:
    st.session_state["products"] = []
if "demo_history" not in st.session_state:
    st.session_state["demo_history"] = {}

# ==================== KONFIGURASI ====================
ADMIN_USERNAME = "arkidigital"
ADMIN_PASSWORD = "Arkidigital2026"
CHECKOUT_LINK = "https://muhammad-masruri.myscalev.com/checkout-pageku"
DEMO_DURATION_MINUTES = 5
MAX_DEMO_ANALYSIS = 2
MAX_DEMO_GENERATOR = 2

# ==================== CUSTOM CSS PREMIUM ====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0A0A1A 0%, #0F0F2A 50%, #0A0A1A 100%);
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 24px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        transition: all 0.3s cubic-bezier(0.2, 0, 0, 1);
    }
    
    .glass-card:hover {
        transform: translateY(-4px);
        border-color: rgba(255, 255, 255, 0.15);
        box-shadow: 0 20px 35px -15px rgba(0, 0, 0, 0.5);
    }
    
    .metric-premium {
        background: rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 20px;
        padding: 1rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-premium:hover {
        transform: translateY(-3px);
        border-color: rgba(255, 255, 255, 0.2);
        background: rgba(255, 255, 255, 0.07);
    }
    
    .metric-premium h3 {
        font-size: 0.7rem;
        font-weight: 500;
        letter-spacing: 1px;
        text-transform: uppercase;
        color: #94A3B8;
        margin-bottom: 0.5rem;
    }
    
    .metric-premium h2 {
        font-size: 1.6rem;
        font-weight: 700;
        color: #FFFFFF;
        margin: 0;
    }
    
    .btn-primary {
        background: #FFFFFF;
        color: #0A0A1A;
        padding: 12px 24px;
        border-radius: 40px;
        text-align: center;
        font-weight: 700;
        font-size: 1rem;
        text-decoration: none;
        display: inline-block;
        transition: all 0.3s ease;
        border: none;
        cursor: pointer;
        width: 100%;
        box-shadow: 0 4px 15px rgba(255, 255, 255, 0.1);
    }
    
    .btn-primary:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(255, 255, 255, 0.2);
        background: #F8FAFC;
    }
    
    .btn-secondary {
        background: rgba(255, 255, 255, 0.05);
        color: #FFFFFF;
        padding: 12px 24px;
        border-radius: 40px;
        text-align: center;
        font-weight: 600;
        font-size: 0.9rem;
        text-decoration: none;
        display: inline-block;
        transition: all 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.15);
        width: 100%;
    }
    
    .btn-secondary:hover {
        background: rgba(255, 255, 255, 0.1);
        border-color: rgba(255, 255, 255, 0.3);
        transform: translateY(-2px);
    }
    
    .premium-header {
        background: linear-gradient(135deg, rgba(10, 10, 26, 0.8) 0%, rgba(15, 15, 42, 0.6) 100%);
        backdrop-filter: blur(10px);
        border-radius: 28px;
        padding: 1.2rem 2rem;
        margin-bottom: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 10px 30px -15px rgba(0, 0, 0, 0.3);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #05050F 0%, #0A0A1A 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    .badge-chip {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 40px;
        padding: 4px 12px;
        font-size: 0.7rem;
        font-weight: 500;
        display: inline-block;
        color: #CBD5E1;
    }
    
    .premium-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        margin: 1.5rem 0;
    }
    
    .ai-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2px 8px;
        border-radius: 20px;
        font-size: 0.6rem;
        font-weight: 600;
        display: inline-block;
        margin-left: 8px;
    }
    
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeInUp 0.5s ease-out;
    }
    
    .premium-footer {
        text-align: center;
        padding: 1.5rem;
        margin-top: 2rem;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        color: #64748B;
        font-size: 0.75rem;
    }
    
    .stTextInput > div > div > input, 
    .stNumberInput > div > div > input,
    .stTextArea > div > textarea {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 14px !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# ==================== FUNGSI DEMO ====================
def get_device_fingerprint():
    user_agent = st.context.headers.get('User-Agent', 'unknown')
    ip = st.context.headers.get('X-Forwarded-For', 'unknown')
    return hashlib.md5(f"{user_agent}_{ip}".encode()).hexdigest()

def load_demo_history():
    return st.session_state.demo_history

def can_start_demo(fingerprint):
    history = load_demo_history()
    now = datetime.now()
    if fingerprint not in history:
        history[fingerprint] = {"attempts": []}
    history[fingerprint]["attempts"] = [t for t in history[fingerprint]["attempts"] if now - datetime.fromisoformat(t) < timedelta(hours=24)]
    return len(history[fingerprint]["attempts"]) < 1

def record_demo_start(fingerprint):
    history = load_demo_history()
    if fingerprint not in history:
        history[fingerprint] = {"attempts": []}
    history[fingerprint]["attempts"].append(datetime.now().isoformat())
    st.session_state.demo_history = history

def start_demo():
    fingerprint = get_device_fingerprint()
    if not can_start_demo(fingerprint):
        st.error("⚠️ Demo hanya 1x per 24 jam!")
        st.markdown(f'<a href="{CHECKOUT_LINK}" target="_blank" class="btn-primary" style="display:block;">💎 Beli Premium</a>', unsafe_allow_html=True)
        return False
    record_demo_start(fingerprint)
    st.session_state["demo_mode"] = True
    st.session_state["demo_start_time"] = datetime.now()
    st.session_state["demo_analysis_count"] = 0
    st.session_state["demo_generator_count"] = 0
    st.session_state["authenticated"] = False
    st.rerun()
    return True

def is_demo_expired():
    if not st.session_state.get("demo_mode", False):
        return False
    start = st.session_state.get("demo_start_time")
    if start is None:
        return True
    if datetime.now() - start > timedelta(minutes=DEMO_DURATION_MINUTES):
        st.session_state["demo_mode"] = False
        return True
    return False

def get_demo_remaining():
    if not st.session_state.get("demo_mode", False):
        return 0
    elapsed = (datetime.now() - st.session_state["demo_start_time"]).total_seconds()
    return max(0, DEMO_DURATION_MINUTES * 60 - int(elapsed))

def can_do_demo_analysis():
    return st.session_state.get("demo_analysis_count", 0) < MAX_DEMO_ANALYSIS

def can_do_demo_generator():
    return st.session_state.get("demo_generator_count", 0) < MAX_DEMO_GENERATOR

def inc_demo_analysis():
    if st.session_state.get("demo_mode", False):
        st.session_state["demo_analysis_count"] = st.session_state.get("demo_analysis_count", 0) + 1

def inc_demo_generator():
    if st.session_state.get("demo_mode", False):
        st.session_state["demo_generator_count"] = st.session_state.get("demo_generator_count", 0) + 1

def is_premium():
    return st.session_state.get("authenticated", False)

# ==================== DATABASE PRODUK ====================
def load_products():
    return st.session_state.products

def save_product(p):
    products = load_products()
    for i, prod in enumerate(products):
        if prod["nama"] == p["nama"]:
            products[i] = p
            st.session_state.products = products
            return
    products.append(p)
    st.session_state.products = products

def delete_product(nama):
    products = load_products()
    st.session_state.products = [p for p in products if p["nama"] != nama]

# ==================== LOGIN + DEMO ====================
def login_or_demo():
    st.markdown("""
    <div style="text-align:center; padding:3rem 1rem;" class="fade-in">
        <div style="background: rgba(255,255,255,0.03); border-radius: 60px; width: 80px; height: 80px; display: flex; align-items: center; justify-content: center; margin: 0 auto 1.5rem auto; border: 1px solid rgba(255,255,255,0.1);">
            <span style="font-size: 40px;">🩺</span>
        </div>
        <h1 style="font-size: 2.2rem; font-weight: 800; background: linear-gradient(135deg, #FFFFFF 0%, #94A3B8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.5rem;">DOCTOR ADS PREMIUM</h1>
        <p style="color: #94A3B8; margin-bottom: 1rem;">Analisa Iklan TikTok & Shopee → Rekomendasi Perbaikan Instan</p>
        <div class="badge-chip" style="margin-bottom: 2rem;">✨ Hanya Rp147rb (sekali bayar) + Konsultasi GRATIS!</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        with st.form("login"):
            st.markdown("### 🔐 **Login Premium**")
            u = st.text_input("Username", placeholder="Masukkan username")
            p = st.text_input("Password", type="password", placeholder="Masukkan password")
            if st.form_submit_button("🔓 Login", use_container_width=True):
                if u == ADMIN_USERNAME and p == ADMIN_PASSWORD:
                    st.session_state["authenticated"] = True
                    st.session_state["demo_mode"] = False
                    st.rerun()
                else:
                    st.error("❌ Username atau password salah!")
    
    with col2:
        st.markdown("### 🎁 **Coba Demo 5 Menit**")
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.03); border-radius: 16px; padding: 1rem; margin-bottom: 1rem;">
            <small>✅ Maks {MAX_DEMO_ANALYSIS} analisis<br>
            ✅ Maks {MAX_DEMO_GENERATOR} generate<br>
            ✅ 1x per 24 jam</small>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚀 Mulai Demo Gratis", use_container_width=True):
            start_demo()
    
    st.markdown(f"""
    <div class="premium-divider"></div>
    <a href="{CHECKOUT_LINK}" target="_blank" class="btn-primary" style="display:block; text-align:center;">💎 Beli Premium Sekarang</a>
    """, unsafe_allow_html=True)
    return False

# ==================== CEK AKSES ====================
if not is_premium() and not st.session_state.get("demo_mode", False):
    login_or_demo()
    st.stop()

if is_demo_expired():
    st.markdown("""
    <div style="background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.2); border-radius: 16px; padding: 1rem; margin-bottom: 1rem;">
        <p style="color: #F87171; margin: 0;">⏰ Demo habis! Beli premium untuk akses penuh.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f'<a href="{CHECKOUT_LINK}" target="_blank" class="btn-primary" style="display:block;">💎 Beli Premium Rp147rb</a>', unsafe_allow_html=True)
    st.stop()

# ==================== HEADER PREMIUM ====================
st.markdown(f"""
<div class="premium-header fade-in">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="background: rgba(255,255,255,0.05); border-radius: 16px; padding: 8px 14px;">
                <span style="font-size: 24px;">🩺</span>
            </div>
            <div>
                <h1 style="margin: 0; font-size: 1.3rem; font-weight: 700;">DOCTOR ADS PREMIUM</h1>
                <p style="margin: 0; font-size: 0.7rem; color: #94A3B8;">Analisa Iklan TikTok & Shopee</p>
            </div>
        </div>
        <div style="display: flex; align-items: center; gap: 12px;">
            <div class="badge-chip">{'🎁 DEMO MODE' if not is_premium() else '⭐ PREMIUM MEMBER'}</div>
            <div class="badge-chip">{datetime.now().strftime('%d %b %Y')}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0; border-bottom: 1px solid rgba(255,255,255,0.05); margin-bottom: 1rem;">
        <div style="background: rgba(255,255,255,0.05); border-radius: 20px; width: 50px; height: 50px; display: flex; align-items: center; justify-content: center; margin: 0 auto 0.8rem auto;">
            <span style="font-size: 28px;">🩺</span>
        </div>
        <h3 style="margin: 0; font-size: 0.9rem;">ARKIDIGITAL</h3>
        <p style="margin: 0; font-size: 0.6rem; color: #64748B;">Digital Marketing Solution</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not is_premium():
        rem = get_demo_remaining()
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.05); border-radius: 16px; padding: 0.8rem; margin-bottom: 1rem; text-align: center;">
            <p style="margin: 0; font-size: 0.7rem; color: #94A3B8;">⏱️ Demo Mode</p>
            <p style="margin: 0; font-size: 1.2rem; font-weight: 700;">{rem//60}:{rem%60:02d}</p>
            <p style="margin: 0; font-size: 0.6rem; color: #64748B;">Analisis: {st.session_state.get('demo_analysis_count',0)}/{MAX_DEMO_ANALYSIS} | Generate: {st.session_state.get('demo_generator_count',0)}/{MAX_DEMO_GENERATOR}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Menu sidebar
    st.markdown("### 📋 **Menu**")
    menu = st.radio("", ["📊 Dashboard", "📦 Database Produk", "🎯 Kalkulator BEP", "📋 Cek Produk"], label_visibility="collapsed")
    
    st.markdown("---")
    
    # Database Produk
    if menu == "📦 Database Produk" and is_premium():
        st.markdown("### 📦 **Database Produk**")
        products = load_products()
        with st.expander("➕ Tambah/Edit Produk"):
            nama = st.text_input("Nama Produk", key="nama_produk_input")
            hj = st.number_input("Harga Jual", min_value=1000, value=100000, step=5000, key="hj_input")
            modal = st.number_input("Modal", min_value=500, value=60000, step=5000, key="modal_input")
            admin = st.slider("Admin %", 5, 30, 20, key="admin_input")
            if st.button("💾 Simpan", key="simpan_produk") and nama:
                admin_nom = hj * admin/100
                laba = hj - modal - admin_nom
                roas_bep_prod = hj / laba if laba > 0 else 999
                save_product({"nama": nama, "harga_jual": hj, "modal": modal, "admin_persen": admin, "laba_kotor": laba, "roas_bep": roas_bep_prod})
                st.success("Tersimpan")
        if products:
            pilih = st.selectbox("Pilih produk", ["--"] + [p["nama"] for p in products], key="pilih_produk")
            if pilih != "--":
                prod = next(p for p in products if p["nama"] == pilih)
                harga_jual = prod["harga_jual"]
                modal = prod["modal"]
                admin_persen = prod["admin_persen"]
                laba_kotor = prod["laba_kotor"]
                roas_bep = prod["roas_bep"]
                st.info(f"ROAS BEP: {roas_bep:.1f}x | Laba: Rp{laba_kotor:,.0f}")
                if st.button("🗑️ Hapus", key="hapus_produk"):
                    delete_product(pilih)
                    st.rerun()
            else:
                harga_jual = st.number_input("Harga Jual", min_value=1000, value=100000, step=5000, key="manual_hj_sidebar")
                modal = st.number_input("Modal", min_value=500, value=60000, step=5000, key="manual_modal_sidebar")
                admin_persen = st.slider("Admin %", 5, 30, 20, key="manual_admin_sidebar")
                admin_nom = harga_jual * admin_persen/100
                laba_kotor = harga_jual - modal - admin_nom
                roas_bep = harga_jual / laba_kotor if laba_kotor > 0 else 999
        else:
            harga_jual = st.number_input("Harga Jual", min_value=1000, value=100000, step=5000, key="hj_default")
            modal = st.number_input("Modal", min_value=500, value=60000, step=5000, key="modal_default")
            admin_persen = st.slider("Admin %", 5, 30, 20, key="admin_default")
            admin_nom = harga_jual * admin_persen/100
            laba_kotor = harga_jual - modal - admin_nom
            roas_bep = harga_jual / laba_kotor if laba_kotor > 0 else 999
    
    elif menu == "📦 Database Produk" and not is_premium():
        st.info("🔒 Fitur Premium. Silakan beli premium untuk menyimpan produk.")
        harga_jual = st.number_input("Harga Jual", min_value=1000, value=100000, step=5000, key="hj_demo_sidebar")
        modal = st.number_input("Modal", min_value=500, value=60000, step=5000, key="modal_demo_sidebar")
        admin_persen = st.slider("Admin %", 5, 30, 20, key="admin_demo_sidebar")
        admin_nom = harga_jual * admin_persen/100
        laba_kotor = harga_jual - modal - admin_nom
        roas_bep = harga_jual / laba_kotor if laba_kotor > 0 else 999
    
    # Kalkulator BEP
    elif menu == "🎯 Kalkulator BEP":
        st.markdown("### 🎯 **Kalkulator ROAS BEP**")
        col_bep1, col_bep2 = st.columns(2)
        with col_bep1:
            hj_bep = st.number_input("💰 Harga Jual", min_value=1000, value=100000, step=5000, key="bep_hj")
            modal_bep = st.number_input("🏭 Modal", min_value=500, value=60000, step=5000, key="bep_modal")
        with col_bep2:
            admin_bep = st.slider("Admin %", 5, 30, 20, key="bep_admin")
            target_profit_bep = st.number_input("🎯 Target Profit", min_value=0, value=0, step=5000, key="bep_profit")
        
        admin_nom_bep = hj_bep * admin_bep / 100
        laba_kotor_bep = hj_bep - modal_bep - admin_nom_bep - target_profit_bep
        roas_bep_hasil = hj_bep / laba_kotor_bep if laba_kotor_bep > 0 else 999
        
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.04); border-radius: 16px; padding: 1rem; margin-top: 0.5rem;">
            <p style="color: #64748B; margin: 0;">📊 HASIL</p>
            <p style="font-size: 1.5rem; font-weight: 700;">ROAS BEP = {roas_bep_hasil:.1f}x</p>
            <p style="font-size: 0.7rem; color: #64748B;">Setiap Rp1 iklan harus menghasilkan minimal Rp{roas_bep_hasil:.1f} penjualan agar tidak rugi.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Cek Produk
    elif menu == "📋 Cek Produk":
        st.markdown("### 📋 **Cek Kelayakan Produk**")
        pernah = st.radio("Produk pernah laku?", ["Ya","Tidak"], horizontal=True, key="pernah_laku")
        if pernah == "Tidak":
            st.error("❌ Jangan iklan dulu!")
        else:
            terjual = st.number_input("Terjual/bulan", 0, 100000, 500, key="terjual")
            if terjual < 1000:
                st.warning("⚠️ Kurang kuat, tes kecil dulu.")
            harga_komp = st.number_input("Harga kompetitor", min_value=1000, value=90000, step=5000, key="harga_komp")
            if 'harga_jual' in locals() and harga_jual > harga_komp * 1.2:
                st.warning("⚠️ Harga terlalu tinggi.")
            if 'laba_kotor' in locals():
                if laba_kotor <= 0:
                    st.error("❌ Margin habis, ganti produk.")
                elif laba_kotor < 5000:
                    st.warning("⚠️ Margin tipis, rawan boncos.")
                else:
                    st.success("✅ Produk layak iklan!")
    
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center;">
        <a href="{CHECKOUT_LINK}" target="_blank" class="btn-primary" style="display:block; text-align:center; padding: 10px;">💎 Beli Premium</a>
        <p style="font-size: 0.6rem; color: #64748B; margin-top: 0.5rem;">© 2024 Arkidigital</p>
    </div>
    """, unsafe_allow_html=True)

# ==================== DASHBOARD UTAMA ====================
if menu == "📊 Dashboard":
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    
    # Input Data Iklan
    st.markdown("### 📝 **Input Data Iklan**")
    
    if not is_premium() and not can_do_demo_analysis():
        st.warning(f"⚠️ Demo terbatas {MAX_DEMO_ANALYSIS}x analisis. Beli premium untuk unlimited!")
        st.markdown(f'<a href="{CHECKOUT_LINK}" target="_blank" class="btn-primary" style="display:block;">💎 Beli Premium</a>', unsafe_allow_html=True)
        st.stop()
    
    colA, colB = st.columns(2)
    with colA:
        impressions = st.number_input("👁️ Impressions", min_value=0, value=10000, step=1000, key="impressions")
        clicks = st.number_input("🖱️ Clicks", min_value=0, value=300, step=50, key="clicks")
        budget_set = st.number_input("💵 Budget Setting (Rp)", min_value=0, value=100000, step=10000, key="budget_set")
        produk_name = st.text_input("🏷️ Nama Produk (untuk AI)", placeholder="Contoh: Kaos Oversize Pria", key="produk_name")
    with colB:
        budget_spent = st.number_input("💸 Budget Terserap (Rp)", min_value=0, value=90000, step=5000, key="budget_spent")
        target_roas = st.number_input("🎯 Target ROAS", min_value=1.0, value=6.0, step=0.5, key="target_roas")
        sales = st.number_input("💰 Omset (Rp)", min_value=0, value=600000, step=50000, key="sales")
        orders = st.number_input("📦 Jumlah Order", min_value=0, value=6, step=1, key="orders")
        platform = st.selectbox("📱 Platform", ["Shopee", "TikTok"], key="platform")
    
    analize = st.button("🔍 Analisis Iklan", use_container_width=True, key="analize_btn")
    
    if analize:
        if not is_premium():
            inc_demo_analysis()
        
        # Hitung metrik
        if clicks > 0 and impressions > 0:
            ctr = (clicks / impressions * 100)
            cpc = budget_spent / clicks if clicks > 0 else 0
            roas_aktual = sales / budget_spent if budget_spent > 0 else 0
            budget_terserap_persen = (budget_spent / budget_set * 100) if budget_set > 0 else 0
            profit_estimasi = (laba_kotor * orders) - budget_spent if orders > 0 else -budget_spent
        else:
            ctr = 0; cpc = 0; roas_aktual = 0; budget_terserap_persen = 0; profit_estimasi = -budget_spent
        
        def format_rp(angka):
            if angka >= 1_000_000:
                return f"Rp{angka/1_000_000:.1f}JT"
            elif angka >= 1000:
                return f"Rp{angka/1000:.0f}RB"
            return f"Rp{angka:,.0f}"
        
        # Metric Cards
        st.markdown("### 📊 **Dashboard Performa**")
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.markdown(f"""
            <div class="metric-premium">
                <h3>💰 TOTAL BELANJA</h3>
                <h2>{format_rp(budget_spent)}</h2>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-premium">
                <h3>🛒 TOTAL OMSET</h3>
                <h2>{format_rp(sales)}</h2>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="metric-premium">
                <h3>📈 ROAS AKTUAL</h3>
                <h2>{roas_aktual:.1f}x</h2>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            warna_profit = "#34D399" if profit_estimasi > 0 else "#F87171"
            st.markdown(f"""
            <div class="metric-premium">
                <h3>💎 ESTIMASI PROFIT</h3>
                <h2 style="color: {warna_profit};">{format_rp(profit_estimasi)}</h2>
            </div>
            """, unsafe_allow_html=True)
        with col5:
            status_bep = "✅ AMAN" if roas_aktual >= roas_bep else "⚠️ RUGI"
            st.markdown(f"""
            <div class="metric-premium">
                <h3>🎯 ROAS BEP</h3>
                <h2>{roas_bep:.1f}x</h2>
                <p style="font-size: 0.6rem; margin-top: 0.3rem;">{status_bep}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # ==================== AI SUMMARY ====================
        st.markdown("---")
        st.markdown("### 🤖 **AI Summary & Rekomendasi**")
        
        with st.spinner("AI sedang menganalisis data..."):
            ai_summary = generate_ai_summary(ctr, roas_aktual, roas_bep, budget_terserap_persen, clicks, orders, platform)
        
        if ai_summary:
            st.markdown(f"""
            <div style="background: rgba(102, 126, 234, 0.1); border-radius: 20px; padding: 1.2rem; border: 1px solid rgba(102, 126, 234, 0.2); margin-bottom: 1rem;">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 0.8rem;">
                    <span style="font-size: 20px;">🤖</span>
                    <span style="font-weight: 700; color: #A78BFA;">Gemini AI</span>
                    <span class="badge-chip" style="background: rgba(102,126,234,0.2);">Powered by Google</span>
                </div>
                <div style="color: #E2E8F0; line-height: 1.6;">
                    {ai_summary.replace(chr(10), '<br>')}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Fallback ke rule-based
            rekomendasi = ""
            prioritas = ""
            if roas_aktual < roas_bep:
                rekomendasi = f"ROAS {roas_aktual:.1f}x < BEP {roas_bep:.1f}x → IKLAN RUGI. Naikkan target ROAS."
                prioritas = "🔴 PRIORITAS 3"
            elif budget_terserap_persen < 80:
                rekomendasi = f"Budget terserap {budget_terserap_persen:.0f}% → Turunkan target ROAS."
                prioritas = "🟡 PRIORITAS 2"
            elif roas_aktual >= roas_bep and budget_terserap_persen >= 85:
                rekomendasi = f"Performa bagus! Siap scale naikkan budget 30%."
                prioritas = "🟢 PRIORITAS 4"
            else:
                rekomendasi = "Pertahankan setting, pantau 3-5 hari."
                prioritas = "🟢 PRIORITAS 5"
            
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.04); border-radius: 20px; padding: 1.2rem; margin-bottom: 1rem;">
                <p style="font-weight: 700;">{prioritas}</p>
                <p>{rekomendasi}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # ==================== AI VISUAL RECOMMENDATION (Jika CTR rendah) ====================
        if ctr < 2 and clicks > 0:
            st.markdown("### 🎨 **AI Rekomendasi Visual**")
            with st.spinner("AI sedang memberikan saran visual..."):
                visual_ai = generate_visual_recommendation(produk_name if produk_name else "produk ini", ctr)
            
            if visual_ai:
                st.markdown(f"""
                <div style="background: rgba(245, 158, 11, 0.1); border-radius: 20px; padding: 1.2rem; border: 1px solid rgba(245, 158, 11, 0.2);">
                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 0.8rem;">
                        <span style="font-size: 20px;">🎨</span>
                        <span style="font-weight: 700; color: #FBBF24;">Rekomendasi Visual AI</span>
                    </div>
                    <div style="color: #E2E8F0; line-height: 1.6;">
                        {visual_ai.replace(chr(10), '<br>')}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # ==================== AI SCALE PREDICTION ====================
        if roas_aktual >= roas_bep and budget_terserap_persen >= 85:
            st.markdown("### 📈 **AI Prediksi Scale**")
            with st.spinner("AI menghitung prediksi performa..."):
                scale_ai = generate_scale_prediction(roas_aktual, budget_set, roas_bep)
            
            if scale_ai:
                st.markdown(f"""
                <div style="background: rgba(52, 211, 153, 0.1); border-radius: 20px; padding: 1.2rem; border: 1px solid rgba(52, 211, 153, 0.2);">
                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 0.8rem;">
                        <span style="font-size: 20px;">📊</span>
                        <span style="font-weight: 700; color: #34D399;">Prediksi Scale AI</span>
                    </div>
                    <div style="color: #E2E8F0; line-height: 1.6;">
                        {scale_ai.replace(chr(10), '<br>')}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Rekomendasi Budget & ROAS
        rekomendasi_budget = budget_set
        rekomendasi_roas = target_roas
        
        if roas_aktual >= roas_bep * 1.2 and budget_terserap_persen >= 85:
            rekomendasi_budget = budget_set * 1.3
        elif roas_aktual >= roas_bep and budget_terserap_persen < 85:
            rekomendasi_roas = target_roas - 0.5
        elif roas_aktual < roas_bep and roas_aktual > 0:
            rekomendasi_roas = roas_bep + 0.5
        
        st.markdown(f"""
        <div class="premium-divider"></div>
        <div style="display: flex; justify-content: space-between; gap: 1rem; flex-wrap: wrap;">
            <div style="flex: 1;">
                <p style="color: #94A3B8; font-size: 0.7rem;">💰 REKOMENDASI BUDGET</p>
                <p style="font-size: 1.2rem; font-weight: 700;">{format_rp(rekomendasi_budget)}</p>
                <p style="font-size: 0.7rem; color: #64748B;">{'↑ Naik 30% dari budget awal' if rekomendasi_budget > budget_set else 'Pertahankan' if rekomendasi_budget == budget_set else '↓ Turunkan'}</p>
            </div>
            <div style="flex: 1;">
                <p style="color: #94A3B8; font-size: 0.7rem;">🎯 REKOMENDASI TARGET ROAS</p>
                <p style="font-size: 1.2rem; font-weight: 700;">{rekomendasi_roas:.1f}x</p>
                <p style="font-size: 0.7rem; color: #64748B;">{'↑ Naikkan' if rekomendasi_roas > target_roas else '↓ Turunkan' if rekomendasi_roas < target_roas else 'Pertahankan'}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== GENERATOR (Tetap ada di Dashboard) ====================
if menu == "📊 Dashboard":
    st.markdown("---")
    st.markdown("### ✨ **Generator Konten AI**")
    st.markdown(f"<span class='ai-badge'>🤖 Powered by Gemini AI</span>", unsafe_allow_html=True)
    
    def generator_access():
        if is_premium():
            return True
        if can_do_demo_generator():
            return True
        st.warning("⚠️ Demo hanya 2x generate. Beli premium untuk unlimited!")
        st.markdown(f'<a href="{CHECKOUT_LINK}" target="_blank" class="btn-primary" style="display:block;">💎 Beli Premium</a>', unsafe_allow_html=True)
        return False
    
    mode_gen = st.radio("Pilih Mode:", ["🛍️ Mode Shopee (SEO Panjang)", "🎥 Mode TikTok (Viral & Emosional)"], horizontal=True, key="mode_generator")
    
    tab1, tab2, tab3 = st.tabs(["📝 SEO Title", "📄 Deskripsi Produk", "🎬 Hook Video"])
    
    if mode_gen == "🛍️ Mode Shopee (SEO Panjang)":
        mode = "shopee"
        with tab1:
            prod_title = st.text_input("Nama Produk", key="seo_shopee")
            keyword = st.text_input("Kata Kunci Utama (opsional)", placeholder="Contoh: kaos adem, premium", key="kw_shopee")
            if st.button("✨ Generate Judul SEO (AI)", key="gen_seo_shopee"):
                if generator_access():
                    if not is_premium():
                        inc_demo_generator()
                    if prod_title:
                        with st.spinner("AI sedang menulis judul..."):
                            result = generate_with_ai(mode, "title", prod_title, keyword)
                            for line in result.strip().split('\n'):
                                if line.strip():
                                    st.markdown(f"- {line.strip()}")
                    else:
                        st.warning("Masukkan nama produk.")
        
        with tab2:
            prod_desc = st.text_input("Nama Produk", key="desc_shopee")
            manfaat = st.text_input("Manfaat Utama (opsional)", placeholder="Contoh: adem, nyaman, bahan tebal", key="manfaat_shopee")
            if st.button("✨ Generate Deskripsi (AI)", key="gen_desc_shopee"):
                if generator_access():
                    if not is_premium():
                        inc_demo_generator()
                    if prod_desc:
                        with st.spinner("AI sedang menulis deskripsi..."):
                            result = generate_with_ai(mode, "desc", prod_desc, manfaat)
                            st.code(result, language="markdown")
                    else:
                        st.warning("Masukkan nama produk.")
        
        with tab3:
            prod_hook = st.text_input("Nama Produk", key="hook_shopee")
            if st.button("✨ Generate Hook Video (AI)", key="gen_hook_shopee"):
                if generator_access():
                    if not is_premium():
                        inc_demo_generator()
                    if prod_hook:
                        with st.spinner("AI sedang membuat hook..."):
                            result = generate_with_ai(mode, "hook", prod_hook, "")
                            for line in result.strip().split('\n'):
                                if line.strip():
                                    st.markdown(f"- 🎬 {line.strip()}")
                    else:
                        st.warning("Masukkan nama produk.")
    
    else:
        mode = "tiktok"
        with tab1:
            prod_title = st.text_input("Nama Produk", key="seo_tiktok")
            pain = st.text_input("Pain Point Customer (opsional)", placeholder="Contoh: panas, kekecitan, mahal", key="pain_tiktok")
            if st.button("✨ Generate Judul Viral (AI)", key="gen_seo_tiktok"):
                if generator_access():
                    if not is_premium():
                        inc_demo_generator()
                    if prod_title:
                        with st.spinner("AI sedang menulis judul viral..."):
                            result = generate_with_ai(mode, "title", prod_title, pain)
                            for line in result.strip().split('\n'):
                                if line.strip():
                                    st.markdown(f"- 🎥 {line.strip()}")
                    else:
                        st.warning("Masukkan nama produk.")
        
        with tab2:
            prod_desc = st.text_input("Nama Produk", key="desc_tiktok")
            cerita = st.text_area("Cerita Singkat (opsional)", placeholder="Contoh: Dulu aku gak percaya diri...", key="cerita_tiktok")
            if st.button("✨ Generate Deskripsi Emosional (AI)", key="gen_desc_tiktok"):
                if generator_access():
                    if not is_premium():
                        inc_demo_generator()
                    if prod_desc:
                        with st.spinner("AI sedang menulis deskripsi..."):
                            result = generate_with_ai(mode, "desc", prod_desc, cerita)
                            st.code(result, language="markdown")
                    else:
                        st.warning("Masukkan nama produk.")
        
        with tab3:
            prod_hook = st.text_input("Nama Produk", key="hook_tiktok")
            style = st.selectbox("Gaya Hook", ["Problem Solver", "Diskon", "Bukti Sosial", "Curiosity"], key="style_tiktok")
            if st.button("✨ Generate Hook Viral (AI)", key="gen_hook_tiktok"):
                if generator_access():
                    if not is_premium():
                        inc_demo_generator()
                    if prod_hook:
                        with st.spinner("AI sedang membuat hook viral..."):
                            result = generate_with_ai(mode, "hook", prod_hook, style)
                            for line in result.strip().split('\n'):
                                if line.strip():
                                    st.markdown(f"- 🎬 {line.strip()}")
                    else:
                        st.warning("Masukkan nama produk.")
    
    # AI Status Indicator
    if AI_READY:
        st.markdown("""
        <div style="background: rgba(52, 211, 153, 0.1); border-radius: 12px; padding: 0.5rem; margin-top: 1rem; text-align: center;">
            <span style="font-size: 0.7rem; color: #34D399;">🤖 AI Powered by Google Gemini — Hasil lebih kreatif & variatif</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ AI tidak tersedia. Periksa API Key Gemini di Streamlit Secrets.")

# ==================== FOOTER ====================
st.markdown("""
<div class="premium-footer">
    <p>🩺 DOCTOR ADS SHOPEE & TIKTOK PREMIUM</p>
    <p>© 2024 Arkidigital - Solusi Digital Marketing Terbaik</p>
</div>
""", unsafe_allow_html=True)
