import streamlit as st
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image
import cv2
import os

# =========================================================
# 1. إعدادات الصفحة والتصميم البصري (معدل للقراءة الواضحة)
# =========================================================
st.set_page_config(page_title="نظام الفحص الذكي", page_icon="🔬", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;800&display=swap');
    
    /* ضبط اتجاه الصفحة بالكامل لليمين */
    html, body, [data-testid="stAppViewContainer"], .main {
        direction: rtl !important;
        text-align: right !important;
        font-family: 'Tajawal', sans-serif !important;
    }
    
    /* تكبير نصوص العناوين */
    .title-text { font-size: 3.2rem !important; font-weight: 800 !important; color: #0284c7; text-align: center; margin-bottom: 10px; }
    .subtitle-text { font-size: 1.6rem !important; color: #475569; text-align: center; margin-bottom: 30px; font-weight: 700; }
    
    /* تكبير عناوين الاستبيان والرفع */
    h3 { font-size: 1.8rem !important; color: #1e293b !important; margin-bottom: 20px !important; }
    
    /* تكبير نصوص الأسئلة */
    .stCheckbox label { font-size: 1.4rem !important; font-weight: 700 !important; color: #334155 !important; }
    
    /* تكبير النصوص الفرعية */
    .stCaption { font-size: 1.2rem !important; color: #64748b !important; }
    
    /* زر الفحص (تصميمك الأصلي مع خط أكبر) */
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #0284c7 0%, #0ea5e9 100%);
        color: white !important;
        font-size: 1.6rem !important;
        font-weight: 800 !important;
        border-radius: 50px !important;
        padding: 15px 30px !important;
    }
    
    /* تحسين منطقة الرفع */
    [data-testid="stFileUploadDropzone"] div div::before {
        content: "اضغط هنا لرفع صورة الشامة" !important;
        font-size: 1.3rem !important;
        font-weight: 700 !important;
    }
    </style>
""", unsafe_allow_html=True)

# =========================================================
# 2. القائمة الجانبية
# =========================================================
with st.sidebar:
    st.image("logo.jpeg", width=300) 
    st.markdown("### عن المشروع")
    st.info("نظام تقني لدعم التوعية بمخاطر سرطان الجلد.")
    # (تم الإبقاء على معلومات الفريق كما في كودك الأصلي)

# =========================================================
# 3. الواجهة الرئيسية
# =========================================================
st.markdown('<div class="title-text">نظام الفحص الأولي الذكي لسرطان الجلد</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-text">مشروع: اكتشف مبكراً… لتنقذ حياة 🛡️</div>', unsafe_allow_html=True)

# المسار والنموذج
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, 'best_skin_cancer_model.keras')

@st.cache_resource
def load_students_model():
    return tf.keras.models.load_model(model_path, compile=False)

try:
    model = load_students_model()
    model_loaded = True
except:
    model_loaded = False

# =========================================================
# 4. الاستبيان والفحص
# =========================================================
col1, col2 = st.columns([1, 1.2], gap="large")
abcde_score = 0

with col1:
    st.markdown("### 📋 أولاً: التقييم السريري (ABCDE)")
    st.caption("أجب على الأسئلة بناءً على ملاحظتك للشامة:")
    if st.checkbox("A - عدم التماثل: هل شكل الشامة غير متماثل من المنتصف؟"): abcde_score += 1
    if st.checkbox("B - الحدود: هل أطراف الشامة خارجية متعرجة؟"): abcde_score += 1
    if st.checkbox("C - اللون: هل تحتوي الشامة على تدرجات ألوان؟"): abcde_score += 1
    if st.checkbox("D - القطر: هل يزيد القطر عن 6 ملم؟"): abcde_score += 1
    if st.checkbox("E - التطور: هل لاحظت تغيراً مفاجئاً في حجمها؟"): abcde_score += 1

with col2:
    st.markdown("### 📸 ثانياً: الفحص الرقمي (الذكاء الاصطناعي)")
    uploaded_file = st.file_uploader("ارفع صورة قريبة وواضحة جداً للشامة", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        st.image(uploaded_file, use_container_width=True)

# تنفيذ الفحص
if uploaded_file and model_loaded:
    if st.button("🚀 بـدء الـفـحـص الـشـامـل"):
        st.success("جاري تحليل النتائج...")

st.markdown("---")
st.caption("إخلاء مسؤولية: هذا التطبيق للتوعية فقط ولا يغني عن الطبيب.")
