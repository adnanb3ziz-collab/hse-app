import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. إعداد الصفحة
st.set_page_config(page_title="HSE AI Pro", page_icon="🛡️", layout="centered")

# 2. الستايل (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    h1 { color: #2c3e50; text-align: center; border-bottom: 3px solid #ffc107; padding-bottom: 10px; }
    .stButton>button { background-color: #ffc107; color: #000000; font-weight: bold; width: 100%; padding: 10px; border: 2px solid #e0a800; border-radius: 8px; }
    .report-box { background-color: white; padding: 20px; border-radius: 10px; border-left: 5px solid #28a745; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    </style>
""", unsafe_allow_html=True)

# 3. القائمة الجانبية (Sidebar)
with st.sidebar:
    st.header("⚙️ الإعدادات")
    api_key = st.text_input("🔑 API Key", type="password")
    st.divider()
    language = st.selectbox("🌐 اللغة", ["العربية", "Français", "English"])
    st.info("System: Gemini Pro Vision (Stable)")

# 4. الواجهة الرئيسية
st.title("🛡️ HSE SMART INSPECTOR")
st.markdown("<h5 style='text-align: center; color: gray;'>نظام كشف المخاطر بالذكاء الاصطناعي</h5>", unsafe_allow_html=True)

if api_key:
    genai.configure(api_key=api_key)
    
    # رفع الصور
    tab1, tab2 = st.tabs(["📸 الكاميرا", "🖼️ ملف"])
    image_input = None
    
    with tab1:
        cam = st.camera_input("التقط صورة")
        if cam: image_input = cam
    with tab2:
        up = st.file_uploader("حمل صورة", type=['jpg','png','jpeg'])
        if up: image_input = up

    if image_input:
        img = Image.open(image_input)
        st.image(img, caption="الصورة قيد التحليل", use_container_width=True)
        
        if st.button("🚀 تحليل المخاطر (Analyze)"):
            with st.spinner("جاري التحليل... (Gemini Pro Vision)"):
                try:
                    # الحل الجذري: استخدام الموديل المستقر
                    model = genai.GenerativeModel('gemini-pro-vision')
                    
                    prompt = f"""
                    Role: Expert HSE Inspector (ISO 45001).
                    Task: Analyze this image for safety hazards and unsafe acts.
                    Output Language: {language}.
                    
                    Format:
                    1. Hazard Description.
                    2. Risk Level.
                    3. Corrective Actions.
                    
                    Be professional and concise.
                    """
                    
                    response = model.generate_content([prompt, img])
                    
                    st.markdown(f"""
                    <div class="report-box">
                        <h3>📋 التقرير ({language})</h3>
                        {response.text}
                    </div>
                    """, unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"Error: {e}")
else:
    st.warning("⚠️ أدخل مفتاح API في القائمة الجانبية للبدء.")
