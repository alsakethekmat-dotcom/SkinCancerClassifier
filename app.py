import streamlit as st
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image
import cv2
import os

# =========================================================
# 1. إعدادات الصفحة والتصميم البصري العصري
# =========================================================
st.set_page_config(
    page_title="نظام الفحص الذكي - اكتشف مبكراً",
    page_icon="🔬", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800&display=swap');
    * { font-family: 'Tajawal', sans-serif !important; }
    html, body, [data-testid="stAppViewContainer"], .main { direction: rtl !important; text-align: right !important; background-color: #f4f7f6 !important; }
    [data-testid="stSidebar"] { background-color: #ffffff !important; border-left: 1px solid #e0e0e0; direction: rtl !important; text-align: right !important; }
    .title-text { font-size: 2.8rem; font-weight: 800; background: -webkit-linear-gradient(45deg, #0284c7, #0ea5e9); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; margin-bottom: 5px; }
    .subtitle-text { color: #475569; font-size: 1.2rem; text-align: center; margin-bottom: 40px; font-weight: 500; }
    .stCheckbox { background: #ffffff; padding: 15px 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.04); margin-bottom: 12px; border: 1px solid #f1f5f9; }
    .stButton > button { width: 100%; background: linear-gradient(90deg, #0284c7 0%, #0ea5e9 100%); color: white !important; font-size: 1.4rem !important; font-weight: 700 !important; border-radius: 50px !important; padding: 12px 24px !important; border: none !important; box-shadow: 0 4px 15px rgba(2, 132, 199, 0.4) !important; }
    .team-card { background: #f8fafc; padding: 20px; border-radius: 15px; border-right: 4px solid #0284c7; margin-top: 20px; text-align: right; }
    .team-title { color: #0284c7; font-weight: 700; margin-bottom: 10px; font-size: 1.1rem; }
    .team-names { color: #334155; font-size: 1rem; line-height: 1.8; font-weight: 500;}
    [data-testid="stFileUploadDropzone"] div div::before { content: "اسحب وأفلت الصورة هنا أو اضغط للاستعراض"; display: block; font-family: 'Tajawal', sans-serif; color: #475569; font-weight: 600; font-size: 1.1rem; }
    [data-testid="stFileUploadDropzone"] div div span, [data-testid="stFileUploadDropzone"] div div small { display: none !important; }
    </style>
""", unsafe_allow_html=True)

# =========================================================
# 2. القائمة الجانبية
# =========================================================
with st.sidebar:
    # أيقونة مجهر طبية
    st.image("https://cdn-icons-png.flaticon.com/512/3304/3304567.png", width=100)
    st.markdown("### عن المشروع")
    st.info("نظام تقني يجمع بين دقة الذكاء الاصطناعي والمؤشرات السريرية لدعم التوعية الصحية.")
    st.markdown("""
    <div class="team-card">
        <div class="team-title">👩‍💻 الطالبات المبدعات</div>
        <div class="team-names">• سما • رنيم • جود • فرح • نورسين</div>
        <hr style="margin: 10px 0;">
        <div class="team-title">👩‍🏫 إشراف المعلمة</div>
        <div class="team-names">أماني أبو رمان</div>
        <hr style="margin: 10px 0;">
        <div class="team-title">🏫 المدرسة</div>
        <div class="team-names">مدرسة حكمت الساكت الأساسية</div>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# 3. الواجهة الرئيسية
# =========================================================
st.markdown('<div class="title-text">نظام الفحص الأولي الذكي لسرطان الجلد</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-text">مشروع: اكتشف مبكراً… لتنقذ حياة 🛡️</div>', unsafe_allow_html=True)

model_path = 'best_skin_cancer_model.keras'
@st.cache_resource
def load_model():
    return tf.keras.models.load_model(model_path, compile=False)

try:
    model = load_model()
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
    if st.checkbox("A - عدم التماثل: هل شكل الشامة غير متماثل؟"): abcde_score += 1
    if st.checkbox("B - الحدود: هل أطراف الشامة غير منتظمة؟"): abcde_score += 1
    if st.checkbox("C - اللون: هل تحتوي الشامة على تدرجات ألوان؟"): abcde_score += 1
    if st.checkbox("D - القطر: هل يزيد القطر عن 6 ملم؟"): abcde_score += 1
    if st.checkbox("E - التطور: هل لاحظت تغيراً مفاجئاً في حجمها؟"): abcde_score += 1

with col2:
    st.markdown("### 📸 ثانياً: الفحص الرقمي")
    uploaded_file = st.file_uploader("ارفع صورة الشامة", type=["jpg", "png"])
    if uploaded_file:
        st.image(uploaded_file, use_container_width=True)

if uploaded_file and model_loaded:
    if st.button("🚀 بـدء الـفـحـص الـشـامـل"):
        st.write("جاري تحليل النتائج...")
        # يتم دمج abcde_score مع نتيجة الذكاء الاصطناعي هنا كما في كودك السابق

st.markdown("---")
st.caption("🚨 إخلاء مسؤولية: هذا التطبيق مخصص لغايات التوعية والفحص الذاتي الأولي فقط.")
هل يعمل الآن بشكل صحيح بعد استبدال الكود بهذا الإ
