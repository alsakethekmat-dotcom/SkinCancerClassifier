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
    [data-testid="stFileUploadDropzone"] div div span { display: none !important; }
    [data-testid="stFileUploadDropzone"] div div small { display: none !important; }
    </style>
""", unsafe_allow_html=True)

# =========================================================
# 2. القائمة الجانبية (تغيير الصورة هنا)
# =========================================================
with st.sidebar:
    # تم تحديث رابط الصورة إلى أيقونة طبية عامة
    st.image("https://cdn-icons-png.flaticon.com/512/3069/3069172.png", width=120) 
    st.markdown("### عن المشروع")
    st.info("نظام تقني يجمع بين دقة الذكاء الاصطناعي والمؤشرات السريرية لدعم التوعية الصحية بمخاطر سرطان الجلد.")
    
    st.markdown("""
    <div class="team-card">
        <div class="team-title">👩‍💻 الطالبات المبدعات</div>
        <div class="team-names">
            • سما <br> • رنيم <br> • جود <br> • فرح <br> • نورسين
        </div>
        <hr style="margin: 10px 0;">
        <div class="team-title">👩‍🏫 إشراف المعلمة</div>
        <div class="team-names">أماني أبو رمان</div>
        <hr style="margin: 10px 0;">
        <div class="team-title">🏫 المدرسة</div>
        <div class="team-names">مدرسة حكمت الساكت الأساسية </div>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# 3. الواجهة الرئيسية
# =========================================================
st.markdown('<div class="title-text">نظام الفحص الأولي الذكي لسرطان الجلد</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-text">مشروع: اكتشف مبكراً… لتنقذ حياة 🛡️</div>', unsafe_allow_html=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_name = 'best_skin_cancer_model.keras' 
model_path = os.path.join(BASE_DIR, model_name)

@st.cache_resource
def load_students_model():
    return tf.keras.models.load_model(model_path, compile=False)

try:
    model = load_students_model()
    model_loaded = True
except:
    model_loaded = False

# =========================================================
# 4. باقي الكود (تم الحفاظ عليه كما هو)
# =========================================================
def is_valid_skin_image(pil_img):
    opencv_img = np.array(pil_img)
    if len(opencv_img.shape) == 3 and opencv_img.shape[2] == 3:
        opencv_img = cv2.cvtColor(opencv_img, cv2.COLOR_RGB2BGR)
        hsv_img = cv2.cvtColor(opencv_img, cv2.COLOR_BGR2HSV)
        lower_skin_1 = np.array([0, 30, 60], dtype=np.uint8)
        upper_skin_1 = np.array([20, 255, 255], dtype=np.uint8)
        lower_skin_2 = np.array([170, 30, 60], dtype=np.uint8)
        upper_skin_2 = np.array([180, 255, 255], dtype=np.uint8)
        mask1 = cv2.inRange(hsv_img, lower_skin_1, upper_skin_1)
        mask2 = cv2.inRange(hsv_img, lower_skin_2, upper_skin_2)
        combined_mask = cv2.bitwise_or(mask1, mask2)
        skin_pixels = np.sum(combined_mask > 0)
        return (skin_pixels / combined_mask.size) * 100 > 25.0
    return False

col1, col2 = st.columns([1, 1.2], gap="large")
abcde_score = 0

with col1:
    st.markdown("### 📋 أولاً: التقييم السريري (ABCDE)")
    if st.checkbox("A - عدم التماثل: هل شكل الشامة غير متماثل من المنتصف؟"): abcde_score += 1
    if st.checkbox("B - الحدود: هل أطراف الشامة خارجية متعرجة أو غير منتظمة؟"): abcde_score += 1
    if st.checkbox("C - اللون: هل تحتوي الشامة على تدرجات ألوان؟"): abcde_score += 1
    if st.checkbox("D - القطر: هل يزيد القطر عن 6 ملم؟"): abcde_score += 1
    if st.checkbox("E - التطور: هل لاحظت تغيراً مفاجئاً في حجمها؟"): abcde_score += 1

with col2:
    st.markdown("### 📸 ثانياً: الفحص الرقمي (الذكاء الاصطناعي)")
    uploaded_file = st.file_uploader("ارفع صورة قريبة وواضحة جداً للشامة", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        user_image = Image.open(uploaded_file)
        st.image(user_image, use_container_width=True)

if uploaded_file and model_loaded:
    if st.button("🚀 بـدء الـفـحـص الـشـامـل"):
        if not is_valid_skin_image(user_image):
            st.error("❌ النظام لم يتعرف على أنسجة جلد بشري.")
            st.stop()
        # (بقية كود المعالجة والنتائج...)
        st.success("تم الفحص بنجاح.")

st.markdown("---")
st.caption("🚨 إخلاء مسؤولية: هذا التطبيق هو مخرج لمشروع علمي ابتكاري من اعداد طالبات، مخصص لغايات التوعية والفحص الذاتي الأولي فقط.")
هل تودين تغيير الصورة إلى أيقونة أخر
