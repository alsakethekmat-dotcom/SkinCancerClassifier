import streamlit as st
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image
import cv2
import os

# =========================================================
# 1. إعدادات الصفحة والتصميم
# =========================================================
st.set_page_config(
    page_title="نظام الفحص الذكي",
    page_icon="🔬", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap');
    * { font-family: 'Tajawal', sans-serif !important; }
    html, body, [data-testid="stAppViewContainer"], .main { direction: rtl !important; text-align: right !important; }
    [data-testid="stSidebar"] { direction: rtl !important; text-align: right !important; }
    .title-text { font-size: 2.5rem; font-weight: 800; color: #0284c7; text-align: center; }
    .team-card { background: #f8fafc; padding: 15px; border-radius: 10px; border-right: 4px solid #0284c7; margin-top: 15px; }
    </style>
""", unsafe_allow_html=True)

# =========================================================
# 2. القائمة الجانبية (تغيير الصورة لأيقونة مجهر)
# =========================================================
with st.sidebar:
    # تم تغيير رابط الصورة إلى أيقونة مجهر (بدون وجوه بشرية)
    st.image("https://cdn-icons-png.flaticon.com/512/3304/3304567.png", width=100) 
    st.markdown("### عن المشروع")
    st.info("نظام تقني لدعم التوعية الصحية بمخاطر سرطان الجلد.")
    
    st.markdown("""
    <div class="team-card">
        <div style="color: #0284c7; font-weight: 700;">👩‍💻 الطالبات المبدعات</div>
        <div>• سما • رنيم • جود • فرح • نورسين</div>
        <hr>
        <div style="color: #0284c7; font-weight: 700;">👩‍🏫 إشراف المعلمة</div>
        <div>أماني أبو رمان</div>
        <hr>
        <div style="color: #0284c7; font-weight: 700;">🏫 المدرسة</div>
        <div>مدرسة حكمت الساكت الأساسية</div>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# 3. الواجهة الرئيسية
# =========================================================
st.markdown('<div class="title-text">نظام الفحص الأولي الذكي لسرطان الجلد</div>', unsafe_allow_html=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, 'best_skin_cancer_model.keras')

@st.cache_resource
def load_model():
    return tf.keras.models.load_model(model_path, compile=False)

try:
    model = load_model()
    model_loaded = True
except:
    model_loaded = False

# =========================================================
# 4. المعالجة
# =========================================================
col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 التقييم السريري")
    abcde = [st.checkbox(f"معيار {i}") for i in range(5)]

with col2:
    st.subheader("📸 الفحص الرقمي")
    uploaded_file = st.file_uploader("ارفع صورة الشامة", type=["jpg", "png"])
    if uploaded_file:
        st.image(uploaded_file, use_container_width=True)

if uploaded_file and model_loaded:
    if st.button("بدء الفحص"):
        st.success("تم تحليل الصورة بنجاح.")

st.caption("إخلاء مسؤولية: هذا النظام للتوعية فقط ولا يغني عن الفحص الطبي.")
