import streamlit as st
import google.generativeai as genai
import pandas as pd
import json
import time
import random
import requests
import requests
from bs4 import BeautifulSoup
import subprocess

def copy_to_clipboard(text):
    try:
        process = subprocess.Popen('pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
        process.communicate(text.encode('utf-8'))
        return True
    except Exception as e:
        print(f"Copy failed: {e}")
        return False

# --- Page Config ---
st.set_page_config(
    page_title="Meta Ads Copywriter AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS for Meta Ads Editor UI ---
st.markdown("""
<style>
    /* General Font */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');
    
    .stApp {
        font-family: 'Roboto', sans-serif;
    }

    /* Meta Editor Container */
    .meta-editor-container {
        background-color: white;
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #ddd;
    }

    /* Input Labels */
    .meta-label {
        font-size: 14px;
        font-weight: 600;
        color: #1c1e21;
        margin-bottom: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .meta-label-info {
        font-size: 12px;
        color: #606770;
        font-weight: normal;
        margin-left: 4px;
    }

    .meta-badge {
        background-color: #f0f2f5;
        color: #606770;
        font-size: 12px;
        padding: 2px 8px;
        border-radius: 12px;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
    }

    /* Customizing Streamlit Inputs to look like Meta */
    div[data-baseweb="input"] {
        border-radius: 6px;
        border: 1px solid #ced0d4;
        background-color: white;
    }
    
    div[data-baseweb="textarea"] {
        border-radius: 6px;
        border: 1px solid #ced0d4;
        background-color: white;
    }

    div[data-baseweb="input"]:focus-within, div[data-baseweb="textarea"]:focus-within {
        border-color: #1877f2;
        box-shadow: 0 0 0 2px rgba(24, 119, 242, 0.2);
    }

    /* "Tambahkan opsi" Button Style */
    .add-option-btn {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background-color: white;
        border: 1px solid #ced0d4;
        color: #1c1e21;
        font-weight: 600;
        font-size: 14px;
        padding: 8px 12px;
        border-radius: 6px;
        margin-top: 8px;
        margin-bottom: 16px;
        cursor: pointer;
        width: fit-content;
    }
    .add-option-btn:hover {
        background-color: #f0f2f5;
    }

    /* Optimization Section */
    .optimization-section {
        margin-top: 16px;
        margin-bottom: 16px;
    }
    .optimization-status {
        color: #1c1e21;
        font-size: 14px;
    }
    .optimization-link {
        color: #1877f2;
        font-weight: 600;
        text-decoration: none;
    }

    /* --- Facebook Ad Preview Styles --- */
    .ad-preview-card {
        background-color: white;
        border: 1px solid #dddfe2;
        border-radius: 8px;
        max-width: 500px;
        margin: 0 auto;
        font-family: Helvetica, Arial, sans-serif;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
        overflow: hidden;
    }

    .ad-header {
        padding: 12px 16px 0;
        display: flex;
        align-items: center;
        margin-bottom: 12px;
    }

    .ad-profile-pic {
        width: 40px;
        height: 40px;
        background-color: #ddd;
        border-radius: 50%;
        margin-right: 10px;
    }

    .ad-header-text {
        flex-grow: 1;
    }

    .ad-name {
        font-weight: 600;
        font-size: 15px;
        color: #050505;
        line-height: 1.2;
    }

    .ad-sponsored {
        font-size: 13px;
        color: #65676b;
        line-height: 1.2;
    }

    .ad-menu-dots {
        color: #606770;
        font-weight: bold;
        font-size: 20px;
        cursor: pointer;
    }

    .ad-primary-text {
        padding: 0 16px 12px;
        font-size: 15px;
        color: #050505;
        line-height: 1.4;
        white-space: pre-wrap; /* Preserve newlines */
    }

    .ad-image-placeholder {
        width: 100%;
        height: 300px;
        background-color: #f0f2f5;
        display: flex;
        align-items: center;
        justify-content: center;
        border-top: 1px solid #dddfe2;
        border-bottom: 1px solid #dddfe2;
    }

    .ad-footer {
        padding: 10px 16px;
        background-color: #f0f2f5;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .ad-footer-content {
        flex-grow: 1;
        margin-right: 10px;
    }

    .ad-footer-domain {
        font-size: 12px;
        color: #65676b;
        text-transform: uppercase;
        margin-bottom: 2px;
    }

    .ad-headline {
        font-weight: 600;
        font-size: 16px;
        color: #050505;
        line-height: 1.2;
        margin-bottom: 2px;
    }

    .ad-description {
        font-size: 14px;
        color: #65676b;
        line-height: 1.2;
        max-height: 40px;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .ad-cta-button {
        background-color: #e4e6eb;
        color: #050505;
        border: none;
        border-radius: 6px;
        padding: 8px 12px;
        font-weight: 600;
        font-size: 15px;
        cursor: pointer;
        white-space: nowrap;
    }

    .ad-social-actions {
        padding: 8px 16px;
        border-top: 1px solid #dddfe2;
        display: flex;
        justify-content: space-around;
        color: #65676b;
        font-weight: 600;
        font-size: 14px;
    }
    
    .ad-social-actions span {
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    
    .ad-social-actions span:hover {
        background-color: #f2f2f2;
        border-radius: 4px;
    }    border: none;
        white-space: nowrap;
    }
</style>
""", unsafe_allow_html=True)

# --- API Key Management ---
class APIKeyManager:
    def __init__(self, manual_key_input=None):
        self.keys = []
        if manual_key_input:
            # Split by comma or newline and strip whitespace
            raw_keys = manual_key_input.replace(",", "\n").split("\n")
            self.keys.extend([k.strip() for k in raw_keys if k.strip()])
        
        # Load from secrets
        try:
            for key, value in st.secrets.items():
                if "API_KEY" in key or "GOOGLE_API_KEY" in key:
                    # Handle multi-line secrets
                    if isinstance(value, str) and "\n" in value:
                        secret_keys = value.replace(",", "\n").split("\n")
                        for k in secret_keys:
                            clean_key = k.strip()
                            if clean_key and clean_key not in self.keys:
                                self.keys.append(clean_key)
                    # Handle single line secret
                    elif isinstance(value, str) and value.strip():
                        if value.strip() not in self.keys:
                            self.keys.append(value.strip())
        except FileNotFoundError:
            pass # No secrets file found
            
        self.current_key_index = 0

    def get_current_key(self):
        if not self.keys:
            return None
        return self.keys[self.current_key_index]

    def rotate_key(self):
        if not self.keys:
            return False
        self.current_key_index = (self.current_key_index + 1) % len(self.keys)
        return True

    def execute_with_retry(self, func, *args, **kwargs):
        attempts = 0
        max_attempts = len(self.keys) if self.keys else 1
        
        while attempts < max_attempts:
            current_key = self.get_current_key()
            if not current_key:
                st.error("❌ Tidak ada API Key yang ditemukan. Masukkan API Key di Sidebar.")
                return None

            try:
                genai.configure(api_key=current_key)
                return func(*args, **kwargs)
            except Exception as e:
                st.warning(f"⚠️ Error dengan Key {self.current_key_index + 1}: {e}")
                if "429" in str(e) or "quota" in str(e).lower() or "key" in str(e).lower():
                    if self.rotate_key():
                        st.info("🔄 Mencoba key berikutnya...")
                        attempts += 1
                        time.sleep(1)
                    else:
                        st.error("❌ Semua API Key gagal.")
                        return None
                else:
                     # If it's not a quota/key error, it might be a model error or something else, re-raise or stop
                    st.error(f"❌ Terjadi kesalahan tak terduga: {e}")
                    return None
        return None

# --- Helper Function: Fetch Landing Page ---
def get_landing_page_text(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
            
        text = soup.get_text(separator=' ')
        # Break into lines and remove leading/trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # Drop blank lines
        text = '\\n'.join(chunk for chunk in chunks if chunk)
        return text[:10000] # Limit text to avoid token limits
    except Exception as e:
        st.error(f"❌ Gagal mengambil konten landing page: {e}")
        return None

# --- Sidebar ---
with st.sidebar:
    st.title("⚙️ Konfigurasi")
    
    # Load saved keys
    saved_keys = ""
    try:
        with open("api_keys.txt", "r") as f:
            saved_keys = f.read()
    except FileNotFoundError:
        pass

    with st.expander("🔐 Kelola API Keys ", expanded=False):
        manual_api_key = st.text_area("Masukkan Google API Key (Bisa Banyak)", value=saved_keys, height=100, help="Masukkan satu per baris atau pisahkan dengan koma. Prioritas tertinggi. Jika kosong, akan menggunakan st.secrets.", placeholder="AIzaSy...\nAIzaSy...")
        
        if st.button("💾 Simpan API Key"):
            with open("api_keys.txt", "w") as f:
                f.write(manual_api_key)
            st.success("API Key berhasil disimpan!")
        
    language = st.selectbox("Bahasa Output", ["Indonesia Gaul", "Indonesia Formal", "Inggris", "Bahasa Sederhana (Curhat sama Teman)"])
    use_flash_only = st.checkbox("⚡ Mode Flash", value=False, help="Centang ini jika sering gagal/error. Akan memaksa menggunakan model Gemini Flash yang lebih stabil.")
    
    st.markdown("---")
    st.markdown("### 💡 Tips")
    st.info("Pastikan Link Landing Page valid dan dapat diakses publik.")

# --- Main Content ---
st.title("🚀 Meta Ads Copywriter AI")
st.markdown("Buat iklan Facebook/Instagram otomatis hanya dari Link Landing Page.")

with st.form("ad_input_form"):
    product_name = st.text_input("Nama Produk", placeholder="Contoh: SlimFit Tea")
    landing_page_url = st.text_input("Link Landing Page (WAJIB)", placeholder="https://websiteanda.com/promo")

    submitted = st.form_submit_button("✨ Generate Iklan Otomatis", type="primary")

# --- Logic ---
if submitted:
    if not landing_page_url:
        st.error("❌ Link Landing Page wajib diisi!")
    else:
        key_manager = APIKeyManager(manual_api_key)
        
        if not key_manager.keys:
             st.error("❌ Harap masukkan API Key di sidebar atau konfigurasi secrets.")
        else:
            with st.spinner("🕵️‍♂️ Sedang menganalisa Landing Page..."):
                landing_page_text = get_landing_page_text(landing_page_url)
            
            if landing_page_text:
                with st.spinner("🤖 Sedang meracik strategi & copy iklan..."):
                    
                    def get_prioritized_models():
                        if use_flash_only:
                            return ['models/gemini-1.5-flash', 'models/gemini-1.5-flash-latest', 'models/gemini-1.5-flash-001']

                        try:
                            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                            
                            # Define strict priority list (Stable models first)
                            target_models = [
                                'models/gemini-1.5-pro-latest',
                                'models/gemini-1.5-pro',
                                'models/gemini-1.5-pro-001',
                                'models/gemini-1.5-flash-latest',
                                'models/gemini-1.5-flash',
                                'models/gemini-1.5-flash-001',
                                'models/gemini-1.0-pro',
                                'models/gemini-pro'
                            ]
                            
                            # Find which target models are actually available for this key
                            valid_models = [m for m in target_models if m in available_models]
                            
                            # If no specific target found, fallback to any available gemini model (excluding experimental if possible, or just add them at the end)
                            if not valid_models:
                                valid_models = [m for m in available_models if 'gemini' in m]
                                
                            return valid_models
                        except Exception as e:
                            # Fallback if listing fails
                            return ['models/gemini-1.5-flash', 'models/gemini-pro']

                    def generate_content():
                        models_to_try = get_prioritized_models()
                        if not models_to_try:
                            models_to_try = ['models/gemini-1.5-flash', 'models/gemini-pro']
                            
                        last_exception = None
                        
                        for model_name in models_to_try:
                            try:
                                # st.write(f"Trying model: {model_name}") # Debug
                                model = genai.GenerativeModel(model_name)
                                
                                prompt = f"""
                                Bertindaklah sebagai Senior Copywriter spesialis Meta Ads (Facebook & Instagram).
                                
                                **INPUT DATA:**
                                Nama Produk: {product_name}
                                Link Landing Page: {landing_page_url}
                                Bahasa Output: {language}
                                
                                **KONTEN LANDING PAGE:**
                                {landing_page_text}
                                
                                **TUGASMU:**
                                1. **Analisa Konten:** Baca konten landing page di atas. Tentukan Target Audience terbaik, USP (Unique Selling Proposition) terkuat, dan Tone of Voice yang paling cocok untuk produk ini.
                                2. **Buat 3 Variasi Iklan:** Berdasarkan analisamu, buat 3 variasi iklan yang berbeda angle.
                                
                                **ATURAN COPYWRITING (WAJIB DIPATUHI):**
                                1. **Primary Text:** 3-4 paragraf pendek agar mudah dibaca di mobile. Gunakan emoji yang relevan. Hook kalimat pertama harus sangat kuat.
                                2. **CTA Wajib:** Di akhir Primary Text, WAJIB menyisipkan kalimat ajakan bertindak diikuti link landing page: {landing_page_url}
                                3. **Headline:** Judul iklan yang tebal (Bold), maksimal 5-7 kata. Harus clickbait tapi jujur.
                                4. **Description:** Info tambahan singkat untuk footer iklan (misal: "Gratis Ongkir" atau "Diskon Terbatas").
                                5. **Variasi Angle:**
                                   - Variasi 1: Fokus pada Masalah (Pain Point) yang ditemukan di landing page.
                                   - Variasi 2: Fokus pada Manfaat/Hasil (Benefit) utama produk.
                                   - Variasi 3: Fokus pada Penawaran Spesial/Urgency (jika ada di landing page) atau Social Proof.
                                
                                **FORMAT OUTPUT:**
                                Keluarkan HANYA JSON murni tanpa markdown (```json ... ```).
                                Strukturnya harus list of objects seperti ini:
                                [
                                    {{
                                        "angle": "Pain Point / Masalah",
                                        "analysis_summary": "Target: Wanita 25-35th, Masalah: Susah diet. USP: Herbal alami.",
                                        "primary_text": "Teks iklan lengkap...",
                                        "headline": "Judul Iklan",
                                        "description": "Deskripsi singkat"
                                    }},
                                    ...
                                ]
                                """
                                
                                response = model.generate_content(prompt)
                                return response.text
                                
                            except Exception as e:
                                last_exception = e
                                # If 429 (Quota) or 404 (Not Found), continue to next model
                                if "429" in str(e) or "quota" in str(e).lower() or "404" in str(e) or "not found" in str(e).lower():
                                    continue
                                else:
                                    # For other errors, we might also want to try next model just in case
                                    continue
                        
                        # If all models fail, raise the last exception to trigger key rotation
                        if last_exception:
                            raise last_exception
                        else:
                            raise Exception("No models available to generate content.")


                    result_text = key_manager.execute_with_retry(generate_content)
                    
                    if result_text:
                        try:
                            # Clean up potential markdown formatting
                            cleaned_text = result_text.replace("```json", "").replace("```", "").strip()
                            ad_variations = json.loads(cleaned_text)
                            
                            # Save to session state
                            st.session_state['ad_variations'] = ad_variations
                            st.session_state['product_name'] = product_name # Save product name for CSV filename
                            
                            st.success("✅ Analisa & Iklan berhasil dibuat!")
                            
                        except json.JSONDecodeError:
                            st.error("❌ Gagal memproses output dari AI. Coba lagi.")
                            with st.expander("Lihat Raw Output"):
                                st.code(result_text)
                        except Exception as e:
                            st.error(f"❌ Terjadi kesalahan: {e}")

# --- Display Results from Session State ---
if 'ad_variations' in st.session_state:
    ad_variations = st.session_state['ad_variations']
    product_name_saved = st.session_state.get('product_name', 'Produk') # Use saved name or default

    # --- Display Results with Meta UI ---
    tabs = st.tabs([f"Variasi {i+1}: {v['angle']}" for i, v in enumerate(ad_variations)])
    
    for i, tab in enumerate(tabs):
        ad = ad_variations[i]
        with tab:
            # Show Analysis Summary
            st.info(f"💡 **Analisa AI:** {ad.get('analysis_summary', 'Tidak ada ringkasan')}")
            
            col_editor, col_preview = st.columns([1.2, 1]) # Adjusted ratio
            
            # --- Left Column: Meta Editor UI ---
            with col_editor:
                # Teks Utama
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.markdown("""
                        <div class="meta-label">
                            <span>Teks utama <span class="meta-label-info">ℹ️</span></span>
                        </div>
                    """, unsafe_allow_html=True)
                with c2:
                    if st.button("📋 Copy", key=f"btn_pt_{i}"):
                        copy_to_clipboard(ad['primary_text'])
                        st.toast("Teks Utama disalin!", icon="✅")

                primary_text = st.text_area("Teks Utama", value=ad['primary_text'], height=150, key=f"pt_{i}", label_visibility="collapsed", placeholder="Beri tahu orang-orang tentang apa iklan Anda")
                
                # Judul
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.markdown("""
                        <div class="meta-label">
                            <span>Judul <span class="meta-label-info">ℹ️</span></span>
                        </div>
                    """, unsafe_allow_html=True)
                with c2:
                    if st.button("📋 Copy", key=f"btn_hl_{i}"):
                        copy_to_clipboard(ad['headline'])
                        st.toast("Judul disalin!", icon="✅")

                headline = st.text_input("Judul", value=ad['headline'], key=f"hl_{i}", label_visibility="collapsed", placeholder="Tulis judul yang singkat")
                
                # Deskripsi
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.markdown("""
                        <div class="meta-label">
                            <span>Deskripsi <span class="meta-label-info">ℹ️</span></span>
                        </div>
                    """, unsafe_allow_html=True)
                with c2:
                    if st.button("📋 Copy", key=f"btn_desc_{i}"):
                        copy_to_clipboard(ad['description'])
                        st.toast("Deskripsi disalin!", icon="✅")

                description = st.text_area("Deskripsi", value=ad['description'], height=68, key=f"desc_{i}", label_visibility="collapsed", placeholder="Masukkan detail tambahan")

                # Tombol Ajakan
                st.markdown("""
                    <div class="meta-label">
                        <span>Tombol ajakan <span class="meta-label-info">ℹ️</span></span>
                    </div>
                """, unsafe_allow_html=True)
                st.selectbox("Tombol", ["Selengkapnya", "Hubungi Kami", "Beli Sekarang", "Daftar"], key=f"cta_{i}", label_visibility="collapsed")

            # --- Right Column: Live Preview ---
            with col_preview:
                st.markdown("### Preview Iklan")
                
                # Meta Ad Preview Card
                st.markdown(f"""
                <div class="ad-preview-card">
                    <div class="ad-header">
                        <div class="ad-profile-pic"></div>
                        <div class="ad-header-text">
                            <div class="ad-name">Nama Halaman Anda</div>
                            <div class="ad-sponsored">Bersponsor <span style="font-size: 10px;">🌐</span></div>
                        </div>
                        <div class="ad-menu-dots">...</div>
                    </div>
                    <div class="ad-primary-text">
                        {primary_text.replace(chr(10), '<br>')}
                    </div>
                    <div class="ad-image-placeholder">
                        <div style="text-align: center; color: #65676b;">
                            <span style="font-size: 40px;">🖼️</span><br>
                            [Gambar/Video Iklan]
                        </div>
                    </div>
                    <div class="ad-footer">
                        <div class="ad-footer-content">
                            <div class="ad-footer-domain">WEBSITEANDA.COM</div>
                            <div class="ad-headline">{headline}</div>
                            <div class="ad-description">{description}</div>
                        </div>
                        <div class="ad-cta-button">Selengkapnya</div>
                    </div>
                    <div class="ad-social-actions">
                        <span>👍 Suka</span>
                        <span>💬 Komentar</span>
                        <span>↗️ Bagikan</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # --- CSV Download ---
    df = pd.DataFrame(ad_variations)
    csv = df.to_csv(index=False).encode('utf-8')
    
    st.download_button(
        label="📥 Download Semua Variasi (CSV)",
        data=csv,
        file_name=f"ad_copy_{product_name_saved.replace(' ', '_')}.csv",
        mime="text/csv",
    )
