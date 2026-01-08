import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. إعداد الصفحة وتصميمها (Configuration & Design)
st.set_page_config(
    page_title="HSE AI Pro",
    page_icon="🛡️",
    layout="centered"
)

# 2. لمسة التصميم العصري (Custom CSS for HSE Look)
st.markdown("""
    <style>
    /* خلفية التطبيق */
    .stApp {
        background-color: #f8f9fa;
    }
    /* تصميم العنوان */
    h1 {
        color: #2c3e50;
        text-align: center;
        border-bottom: 3px solid #ffc107;
        padding-bottom: 10px;
    }
    /* تصميم الأزرار (لون السلامة - Safety Yellow) */
    .stButton>button {
        background-color: #ffc107;
        color: #000000;
        font-weight: bold;
        border-radius: 8px;
        border: 2px solid #e0a800;
        width: 100%;
        padding: 10px;
    }
    .stButton>button:hover {
        background-color: #e0a800;
        color: white;
    }
    /* إطارات الرسائل */
    .report-box {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 5px solid #28a745;
    }
    </style>
""", unsafe_allow_html=True)

# 3. القائمة الجانبية للإعدادات (Sidebar)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3597/3597088.png", width=100)
    st.header("⚙️ إعدادات النظام")
    
    # إدخال الساروت
    api_key = st.text_input("🔑 API Key (Google Gemini)", type="password")
    
    st.divider()
    
    # اختيار اللغة
    language = st.selectbox(
        "🌐 لغة التقرير / Report Language",
        ["العربية", "Français", "English"]
    )
    
    st.info("💡 هذا النظام يعتمد على معايير ISO 45001 لتحليل المخاطر.")
    st.caption("Version 2.0 Pro")

# 4. واجهة التطبيق الرئيسية
st.title("🛡️ HSE SMART INSPECTOR")
st.markdown("<h5 style='text-align: center; color: gray;'>نظام كشف المخاطر بالذكاء الاصطناعي</h5>", unsafe_allow_html=True)
st.write("")

# التأكد من وجود المفتاح
if api_key:
    genai.configure(api_key=api_key)
    
    # اختيار طريقة رفع الصورة (TAB Design)
    tab1, tab2 = st.tabs(["📸 التقاط صورة (Camera)", "🖼️ رفع من الملفات (Upload)"])
    
    image_input = None
    
    with tab1:
        cam_img = st.camera_input("وجه الكاميرا نحو منطقة الخطر")
        if cam_img: image_input = cam_img
            
    with tab2:
        up_img = st.file_uploader("اختر صورة من الجهاز", type=['jpg', 'png', 'jpeg'])
        if up_img: image_input = up_img

    # 5. منطق التحليل
    if image_input:
        # عرض الصورة بشكل أنيق
        img = Image.open(image_input)
        st.divider()
        st.image(img, caption="📍 الموقع قيد التحليل", use_container_width=True)
        
        # زر التحليل
        analyze_btn = st.button("🚀 بدء التحليل الشامل (Analyze Hazards)")
        
        if analyze_btn:
            with st.spinner("🔄 جاري معالجة البيانات ومطابقة معايير ISO 45001..."):
                try:
                    # الموديل
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    # --- THE PROMPT (النص الاحترافي اللي طلبتي) ---
                    base_prompt = """
                    You are an expert HSE Inspector with deep knowledge of ISO 45001 standards. 
                    Analyze the provided image of a workplace or industrial site. 
                    Identify all safety hazards, unsafe acts, and lack of PPE. 
                    For each issue, provide: 
                    1. The Hazard Description. 
                    2. The Potential Risk. 
                    3. The Corrective Action according to safety regulations. 
                    Keep the response professional, concise, and structured.
                    """
                    
                    # إضافة تعليمة اللغة
                    final_prompt = f"{base_prompt}\n\nIMPORTANT: Please provide the final output STRICTLY in {language} language."
                    
                    # الحصول على النتيجة
                    response = model.generate_content([final_prompt, img])
                    
                    # عرض النتيجة بتصميم جميل
                    st.success("✅ تم التحليل بنجاح!")
                    st.markdown(f"""
                    <div class="report-box">
                        <h3>📋 تقرير التفتيش / Inspection Report</h3>
                        {response.text}
                    </div>
                    """, unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"❌ حدث خطأ: {e}")
else:
    # رسالة ترحيبية في حالة عدم إدخال المفتاح
    st.warning("⚠️ المرجو إدخال مفتاح API في القائمة الجانبية للبدء.")
    st.markdown("""
    ### كيف يعمل النظام؟
    1. أدخل مفتاح **Google API**.
    2. التقط صورة للورش أو المعدات.
    3. احصل على تقرير فوري بالمخاطر وحلولها.
    """)
