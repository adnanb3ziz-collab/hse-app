import streamlit as st
import google.generativeai as genai
from PIL import Image

# إعداد الصفحة
st.set_page_config(page_title="HSE Pro", page_icon="🛡️")

# التصميم
st.markdown("""
    <style>
    .stApp {background-color: #f8f9fa;}
    .stButton>button {background-color: #ffc107; color: black; width: 100%; border-radius: 10px;}
    </style>
""", unsafe_allow_html=True)

# القائمة الجانبية
with st.sidebar:
    st.header("⚙️ الإعدادات")
    api_key = st.text_input("🔑 API Key", type="password")
    language = st.selectbox("🌐 اللغة", ["العربية", "Français", "English"])

# الواجهة
st.title("🛡️ HSE SMART INSPECTOR")

if not api_key:
    st.warning("⚠️ أدخل المفتاح (API Key) في القائمة الجانبية.")
    st.stop()

genai.configure(api_key=api_key)

# رفع الصور
tab1, tab2 = st.tabs(["📸 كاميرا", "🖼️ ملف"])
image_input = None

with tab1:
    cam = st.camera_input("صور هنا")
    if cam: image_input = cam
with tab2:
    up = st.file_uploader("حمل صورة", type=['jpg','png','jpeg'])
    if up: image_input = up

if image_input:
    img = Image.open(image_input)
    st.image(img, caption="جاري التحليل...", use_container_width=True)
    
    if st.button("🚀 تحليل المخاطر"):
        with st.spinner("انتظر قليلاً..."):
            try:
                # استخدام الموديل الأحدث والمجاني
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"""
                Act as an HSE Expert (ISO 45001). Analyze the image for hazards.
                Output in {language}.
                Format: Hazard, Risk, Action.
                """
                response = model.generate_content([prompt, img])
                st.success("تم التحليل!")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"Error: {e}")
                
