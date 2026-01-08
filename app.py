import streamlit as st
import google.generativeai as genai
from PIL import Image

# إعداد الصفحة
st.set_page_config(page_title="HSE AI Inspector", page_icon="👷‍♂️")

# العنوان (عربي / فرنسي)
st.title("👷‍♂️ AI Safety Inspector")
st.markdown("**مفتش السلامة الذكي / Inspecteur HSE Intelligent**")

# 1. إعدادات اللغة (Language Settings)
language = st.selectbox(
    "اختر لغة التقرير / Choisissez la langue du rapport :",
    ["العربية", "Français", "English", "Español", "Deutsch", "中文 (Chinese)", "Русский (Russian)"]
)

# 2. بلاصة الساروت
api_key = st.text_input("Enter Google API Key:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    
    # 3. الكاميرا
    camera_image = st.camera_input("التقط صورة / Prenez une photo")

    if camera_image:
        img = Image.open(camera_image)
        
        # زر التحليل
        analyze_btn = st.button("🔍 تحليل المخاطر / Analyser les risques")
        
        if analyze_btn:
            with st.spinner("جاري التحليل... / Analyse en cours..."):
                try:
                    # استدعاء الموديل
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    # الأمر الذكي (Dynamic Prompt)
                    prompt = f"""
                    Role: You are an expert HSE Safety Officer specializing in ISO 45001 standards.
                    Task: Analyze the provided image of a workplace/industrial site.
                    Language: Provide the full report STRICTLY in {language}.
                    
                    Structure of the Report:
                    1. **General Observation** (وصف عام).
                    2. **Identified Hazards** (المخاطر المرصودة) - List specific hazards (unsafe acts/conditions).
                    3. **Risk Level** (مستوى الخطورة) - (Low/Medium/High/Critical).
                    4. **ISO 45001 Violations** (مخالفات المعايير).
                    5. **Corrective Actions** (الإجراءات التصحيحية) - Concrete technical steps to fix the issues.
                    
                    Tone: Professional, Technical, and Directive.
                    """
                    
                    # الحصول على النتيجة
                    response = model.generate_content([prompt, img])
                    
                    # عرض النتيجة
                    st.markdown(f"### 📋 Report in {language}")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"Error: {e}")
else:
    st.warning("المرجو إدخال مفتاح API للبدء / Veuillez entrer la clé API pour commencer.")
