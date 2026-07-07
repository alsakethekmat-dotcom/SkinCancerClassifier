import streamlit as st
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image
import cv2
import os
import base64

# =========================================================
# 1. إعدادات الصفحة والتصميم البصري الفاخر (Premium UI)
# =========================================================
st.set_page_config(
    page_title="نظام الفحص الذكي - اكتشف مبكراً",
    page_icon="🔬", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# إدارة الصفحات والحالة عبر الـ Session State
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'abcde_score' not in st.session_state:
    st.session_state.abcde_score = 0
if 'prediction' not in st.session_state:
    st.session_state.prediction = None
if 'user_image' not in st.session_state:
    st.session_state.user_image = None

# دالة إعادة ضبط التطبيق للعودة للرئيسية
def go_home():
    st.session_state.page = 'home'
    st.session_state.abcde_score = 0
    st.session_state.prediction = None
    st.session_state.user_image = None
    st.rerun()

# كود الـ CSS الشامل
st.markdown("""
    <style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght=500;700;800&display=swap');

/* ضبط الخطوط والاتجاهات الشاملة للمنصة */
* {
    font-family: 'Tajawal', sans-serif !important;
}

html, body, [data-testid="stAppViewContainer"], [data-testid="stMarkdownContainer"], 
.stMarkdown, label, p, h1, h2, h3, h4, h5, h6, .stCheckbox, .stAlert {
    direction: rtl !important;
    text-align: right !important;
}

body {
    background: #f4f7f9 !important; 
}

/* التخلص الكامل من الفراغات الميتة غير المستغلة */
[data-testid="stAppViewBlockContainer"] {
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
    max-width: 1250px !important;
}

/* تكبير وتغميق خطوط المحتوى العام */
p, li, span, .stMarkdown {
    font-size: 21px !important;
    color: #1e293b !important;
    line-height: 1.8 !important;
    font-weight: 500 !important;
}

/* تصميم حاوية الهوية البصرية الممركزة */
.brand-flex-container {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 30px !important;
    width: 100% !important;
    margin-bottom: 35px !important;
    flex-wrap: wrap !important;
}

.brand-logo-img {
    width: 180px !important;
    height: auto !important;
    border-radius: 20px !important;
    box-shadow: 0 10px 25px rgba(26, 74, 117, 0.15) !important;
}

.brand-text-block {
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
}

.main-title {
    font-size: 3.2rem !important;
    font-weight: 800 !important;
    color: #1a4a75 !important;
    margin: 0 !important;
    padding: 0 !important;
    line-height: 1.2 !important;
}

.main-subtitle {
    color: #1c8c7c !important; 
    font-size: 1.6rem !important;
    font-weight: 800 !important;
    margin-top: 12px !important;
    margin-bottom: 0 !important;
}

/* تصميم البطاقات العصرية والمحتوى */
.custom-card {
    background: white !important;
    padding: 30px !important;
    border-radius: 20px !important;
    box-shadow: 0 10px 30px rgba(26, 74, 117, 0.06) !important;
    border: 1px solid #e2e8f0 !important;
}
.info-card { border-right: 6px solid #1c8c7c !important; } 
.team-card { border-right: 6px solid #1a4a75 !important; } 

.card-title {
    font-size: 24px !important;
    font-weight: 800 !important;
    color: #1a4a75 !important;
    margin-bottom: 15px !important;
}

.card-body-text {
    font-size: 19px !important;
    color: #334155 !important;
    line-height: 1.8 !important;
}

/* تكبير خطوط خيارات الاستبيان */
.stCheckbox label p {
    font-size: 21px !important;
    color: #0f172a !important;
    font-weight: 700 !important;
}
.stCheckbox {
    background: white; padding: 18px 22px; border-radius: 12px;
    border: 1px solid #cbd5e1; margin-bottom: 12px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.03);
}

/* =====================================================
   🎯 هندسة الأزرار (ألوان الشعار حصرياً)
   ===================================================== */

/* 1. زر البداية الرئيسي (لون الشعار الأزرق الداكن) */
div[data-testid="element-container"]:has(.hero-btn-marker) + div[data-testid="element-container"] div[data-testid="stButton"] button {
    background-color: #1a4a75 !important; /* أزرق داكن */
    color: white !important;
    font-size: 25px !important;
    font-weight: 800 !important;
    padding: 18px 0px !important;
    width: 100% !important;
    border-radius: 50px !important;
    border: none !important;
    box-shadow: 0 10px 25px rgba(26, 74, 117, 0.3) !important;
    transition: all 0.3s ease-in-out !important;
}

/* تأثير تمرير الماوس لزر البداية (يتحول للون الشعار الأخضر المزرق) */
div[data-testid="element-container"]:has(.hero-btn-marker) + div[data-testid="element-container"] div[data-testid="stButton"] button:hover {
    background-color: #1c8c7c !important; /* أخضر مزرق */
    transform: translateY(-4px) !important;
    box-shadow: 0 15px 35px rgba(28, 140, 124, 0.4) !important;
}

/* 2. أزرار الانتقال بين الصفحات (لون الشعار الأخضر المزرق) */
div[data-testid="element-container"]:has(.next-btn-marker) + div[data-testid="element-container"] div[data-testid="stButton"] button {
    width: 100% !important;
    background-color: #1c8c7c !important; /* أخضر مزرق */
    color: white !important;
    font-size: 22px !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 50px !important;
    padding: 15px !important;
    box-shadow: 0 8px 20px rgba(28, 140, 124, 0.25) !important;
    transition: all 0.3s ease-in-out !important;
}

/* تأثير تمرير الماوس لأزرار الانتقال (تتحول للأزرق الداكن) */
div[data-testid="element-container"]:has(.next-btn-marker) + div[data-testid="element-container"] div[data-testid="stButton"] button:hover {
    background-color: #1a4a75 !important; /* أزرق داكن */
    box-shadow: 0 12px 25px rgba(26, 74, 117, 0.3) !important;
}

/* 3. زر العودة للرئيسية في الإطار العلوي (مفرغ بإطار أزرق داكن) */
div[data-testid="element-container"]:has(.nav-btn-marker) + div[data-testid="element-container"] div[data-testid="stButton"] button {
    width: auto !important;
    background-color: white !important;
    color: #1a4a75 !important;
    border: 2px solid #1a4a75 !important; /* أزرق داكن */
    font-size: 16px !important;
    font-weight: 700 !important;
    padding: 6px 20px !important;
    border-radius: 8px !important;
}

div[data-testid="element-container"]:has(.nav-btn-marker) + div[data-testid="element-container"] div[data-testid="stButton"] button:hover {
    background-color: #1a4a75 !important;
    color: white !important;
}

/* =====================================================
   🛠️ صندوق رفع الملفات (بألوان الشعار)
   ===================================================== */
.stFileUploader section {
    border: 3px dashed #1c8c7c !important; /* أخضر مزرق */
    border-radius: 20px !important;
    background-color: #f0f7f6 !important;
    padding: 35px 20px !important;
}

.stFileUploader section text,
.stFileUploader section span,
.stFileUploader section small,
.stFileUploader section div div {
    display: none !important;
}

.stFileUploader section::before {
    content: "📷 اسحب صورة الشامة هنا أو اضغط على الزر بالأسفل" !important;
    display: block !important;
    font-size: 18px !important;
    font-weight: 700 !important;
    color: #1a4a75 !important; /* أزرق داكن */
    text-align: center !important;
    margin-bottom: 15px !important;
}

.stFileUploader button {
    background-color: #1a4a75 !important; /* أزرق داكن */
    border: none !important;
    border-radius: 12px !important;
    padding: 20px 50px !important;
    cursor: pointer !important;
    color: transparent !important;
    font-size: 0px !important;
    margin: 0 auto !important;
    display: block !important;
    position: relative !important;
}

.stFileUploader button:hover {
    background-color: #1c8c7c !important; /* أخضر مزرق عند التمرير */
}

.stFileUploader button::after {
    content: "اختيار صورة من الجهاز 📂" !important;
    color: white !important;
    font-size: 16px !important;
    font-weight: 700 !important;
    position: absolute !important;
    left: 50% !important;
    top: 50% !important;
    transform: translate(-50%, -50%) !important;
    white-space: nowrap !important;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 2. تحميل نموذج الذكاء الاصطناعي ودوال الفحص الخلفية
# =========================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_name = 'best_skin_cancer_model.keras' 
model_path = os.path.join(BASE_DIR, model_name)

@st.cache_resource
def load_students_model():
    try:
        original_input_layer_init = tf.keras.layers.InputLayer.__init__
        def patched_input_layer_init(self, *args, **kwargs):
            if 'batch_shape' in kwargs:
                kwargs['batch_input_shape'] = kwargs.pop('batch_shape')
            original_input_layer_init(self, *args, **kwargs)
        tf.keras.layers.InputLayer.__init__ = patched_input_layer_init
    except Exception:
        pass
    return tf.keras.models.load_model(model_path, compile=False)

try:
    model = load_students_model()
    model_loaded = True if model is not None else False
except Exception as e:
    model_loaded = False

def is_valid_skin_image(pil_img):
    opencv_img = np.array(pil_img)
    if len(opencv_img.shape) == 3 and opencv_img.shape[2] == 3:
        opencv_img = cv2.cvtColor(opencv_img, cv2.COLOR_RGB2BGR)
        hsv_img = cv2.cvtColor(opencv_img, cv2.COLOR_BGR2HSV)
        lower_skin_1, upper_skin_1 = np.array([0, 30, 60], dtype=np.uint8), np.array([20, 255, 255], dtype=np.uint8)
        lower_skin_2, upper_skin_2 = np.array([170, 30, 60], dtype=np.uint8), np.array([180, 255, 255], dtype=np.uint8)
        mask1 = cv2.inRange(hsv_img, lower_skin_1, upper_skin_1)
        mask2 = cv2.inRange(hsv_img, lower_skin_2, upper_skin_2)
        combined_mask = cv2.bitwise_or(mask1, mask2)
        return (np.sum(combined_mask > 0) / combined_mask.size) * 100 > 25.0
    return False

def get_base64_encoded_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception:
        return ""


# =========================================================
# 3. الإطار العلوي الثابت المتعاكس (Header) - الصفحات الداخلية
# =========================================================
if st.session_state.page != 'home':
    header_btn, header_title, header_logo = st.columns([1.5, 4, 1.2])
    with header_logo:
        st.image("logo.jpeg", width=115) 
    with header_title:
        st.markdown("<h2 style='color:#1a4a75; margin-top:25px; text-align:right; font-weight:800;'>نظام الفحص الأولي الذكي</h2>", unsafe_allow_html=True)
    with header_btn:
        st.markdown('<div style="margin-top:28px; text-align:left;">', unsafe_allow_html=True)
        st.markdown('<div class="nav-btn-marker"></div>', unsafe_allow_html=True)
        if st.button("🏠 العودة للرئيسية", key="nav_to_home_logo"):
            go_home()
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<hr style='margin-top:10px; margin-bottom:30px; border-color: #cbd5e1;'>", unsafe_allow_html=True)


# =========================================================
# 4. منطق عرض وتنسيق الصفحات المتتابعة
# =========================================================

# ----------------- [صفحة 1: الصفحة الرئيسية] -----------------
if st.session_state.page == 'home':
    
    logo_b64 = get_base64_encoded_image(os.path.join(BASE_DIR, "logo.jpeg"))
    
    if logo_b64:
        st.markdown(f"""
        <div class="brand-flex-container">
            <img src="data:image/jpeg;base64,{logo_b64}" class="brand-logo-img" />
            <div class="brand-text-block">
                <h1 class="main-title">نظام الفحص الأولي لسرطان الجلد</h1>
                <p class="main-subtitle">مشروع ابتكاري متميز: اكتشف مبكراً… لتنقذ حياة 🛡️</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<h1 class="main-title" style="text-align:center;">نظام الفحص الأولي لسرطان الجلد</h1>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_info, col_team = st.columns([1.1, 0.9])
    
    with col_info:
        st.markdown("""
        <div class="custom-card info-card">
            <div class="card-title">🔬 عن النظام الذكي</div>
            <div class="card-body-text">
                نظام تقني متطور يدمج بين دقة خوارزميات الذكاء الاصطناعي العميقة والمؤشرات السريرية المعتمدة عالمياً لدعم الكشف المبكر عن آفات الجلد وشاماته بكل خصوصية وسهولة وبأعلى درجات الأمان الطبي المتكامل.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_team:
        st.markdown("""
        <div class="custom-card team-card">
            <div class="card-title">👥 بطاقة تعريفية بالمشروع</div>
            <div class="card-body-text">
                <ul>
                    <li><b>👩‍💻 الطالبات المبتكرات:</b> سما، رنيم، جود، فرح، نورسين</li>
                    <li><b>👩‍🏫 الإشراف المتميز:</b> المعلمة أماني أبو رمان</li>
                    <li><b>🏫 صرح المدرسة:</b> حكمت الساكت الأساسية</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    _, btn_center_col, _ = st.columns([1, 1.6, 1])
    with btn_center_col:
        st.markdown('<div class="hero-btn-marker"></div>', unsafe_allow_html=True)
        if st.button("🚀 ابـدء الـتـحـقـق والـفـحـص الآن", key="main_start_trigger"):
            st.session_state.page = 'survey'
            st.rerun()

# ----------------- [صفحة 2: استبيان ABCDE السريري] -----------------
elif st.session_state.page == 'survey':
    st.markdown("<h2 style='color:#1a4a75; font-weight:800;'>📋 الخطوة الأولى: التقييم السريري (ABCDE)</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:20px; color:#475569;'>الرجاء الإجابة على الأسئلة التالية بناءً على ملاحظتك البصرية للشامة الحالية:</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    a = st.checkbox("A - عدم التماثل: هل شكل الشامة غير متماثل (إذا قسمتها من المنتصف لا يتطابق النصفان)؟")
    b = st.checkbox("B - الحدود: هل أطراف الشامة الخارجية متعرجة، خشنة، أو غير منتظمة؟")
    c = st.checkbox("C - اللون: هل تحتوي الشامة على تدرجات ألوان مختلفة (بني، أسود، أحمر، رمادي)؟")
    d = st.checkbox("D - القطر: هل يزيد القطر الإجمالي لحجم الشامة عن 6 ملم؟")
    e = st.checkbox("E - التطور: هل لاحظت تغيراً مفاجئاً في حجمها، أو بدأت تسبب حكة ونزيف؟")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="next-btn-marker"></div>', unsafe_allow_html=True)
    if st.button("حفظ الإجابات والانتقال لرفع الصورة ⬅️"):
        st.session_state.abcde_score = sum([a, b, c, d, e])
        st.session_state.page = 'upload'
        st.rerun()

# ----------------- [صفحة 3: رفع الصورة وتحليلها] -----------------
elif st.session_state.page == 'upload':
    st.markdown("<h2 style='color:#1a4a75; font-weight:800;'>📸 الخطوة الثانية: الفحص الرقمي (الذكاء الاصطناعي)</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:20px; color:#475569;'>الرجاء رفع صورة قريبة جداً وواضحة للشامة المستهدفة:</p>", unsafe_allow_html=True)
    
    if not model_loaded:
        st.error("🚨 خطأ تقني: لم يتم تحميل ملف ذكاء اصطناعي صالح كـ 'best_skin_cancer_model.keras'.")
    
    uploaded_file = st.file_uploader("ارفع الصورة هنا", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        st.session_state.user_image = Image.open(uploaded_file)
        
        img_c1, img_c2, img_c3 = st.columns([1, 1, 1])
        with img_c2:
            st.image(st.session_state.user_image, caption="الصورة المرفوعة جاهزة للفحص", width=250)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="next-btn-marker"></div>', unsafe_allow_html=True)
        if st.button("🚀 بـدء الـفـحـص الـشـامـل وإظهار التقرير"):
            if not is_valid_skin_image(st.session_state.user_image):
                st.error("❌ تم إيقاف الفحص: لم يتعرف النظام على نسيج جلد بشري. يرجى إلغاء الصورة والتقاط صورة مقربة للشامة فقط.")
            else:
                with st.spinner("🤖 جاري معالجة الصورة وتحليلها عبر النموذج الذكي..."):
                    try:
                        img_resized = st.session_state.user_image.resize((224, 224))
                        img_array = image.img_to_array(img_resized)
                        img_array = tf.keras.applications.efficientnet.preprocess_input(img_array)
                        img_array = np.expand_dims(img_array, axis=0)
                        
                        prediction = model.predict(img_array)[0][0]
                        st.session_state.prediction = float(prediction)
                        st.session_state.page = 'result'
                        st.rerun()
                    except Exception as e:
                        st.error(f"حدث خطأ برمجي أثناء التحليل الفني: {e}")

# ----------------- [صفحة 4: التقرير الطبي والنتيجة النهائية] -----------------
elif st.session_state.page == 'result':
    st.markdown("<h2 style='color:#1a4a75; font-weight:800;'>📊 التقرير الطبي المشترك والنتيجة النهائية</h2>", unsafe_allow_html=True)
    
    abcde_score = st.session_state.abcde_score
    melanoma_probability = st.session_state.prediction * 100
    benign_probability = 100 - melanoma_probability
    
    if melanoma_probability >= 70 or (melanoma_probability >= 40 and abcde_score >= 3):
        st.error(f"⚠️ مستوى الخطورة المحتملة: مرتفع")
        st.write(f"**نسبة الاشتباه المبني على الذكاء الاصطناعي:** {melanoma_probability:.1f}%")
        st.write(f"**علامات الخطر السريرية المرصودة:** {abcde_score} من أصل 5 علامات.")
        st.info("💡 التوجيه الطبي: يُنصح بشدة وبشكل عاجل بحجز موعد لدى طبيب استشاري أمراض جلدية لإجراء فحص مجهري دقيق.")
        
    elif 30 <= melanoma_probability < 70 or (melanoma_probability < 40 and abcde_score >= 2):
        st.warning(f"🟡 مستوى الخطورة المحتملة: متوسط (بحاجة لمتابعة)")
        st.write(f"**نسبة الاشتباه المبني على الذكاء الاصطناعي:** {melanoma_probability:.1f}%")
        st.write(f"**علامات الخطر السريرية المرصودة:** {abcde_score} من أصل 5 علامات.")
        st.info("💡 التوجيه الطبي: يفضل مراقبة الشامة بانتظام (مرة كل شهر) وملاحظة أي تطور، واستشارة الطبيب في حال استمرار التغير.")
        
    else:
        st.success(f"✅ مستوى الخطورة المحتملة: منخفض (مؤشرات مطمئنة جداً)")
        st.write(f"**نسبة سلامة الأنسجة (حميدة):** {benign_probability:.1f}%")
        st.write(f"**علامات الخطر السريرية المرصودة:** {abcde_score} من أصل 5.")
        st.info("💡 التوجيه الطبي: المؤشرات تبدو طبيعية ومطمئنة ولا تدعو للقلق. حافظ على فحص نفسك دورياً.")
        
    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.markdown('<div class="next-btn-marker"></div>', unsafe_allow_html=True)
    if st.button("🔄 إجراء فحص جديد لمريض آخر"):
        go_home()

# =========================================================
# 5. تذييل الصفحة الثابت (Footer)
# =========================================================
st.markdown("<br><br>", unsafe_allow_html=True)
st.caption("🚨 إخلاء مسؤولية قانوني وطبي: هذا التطبيق هو مخرج لمشروع ابتكاري مدرسي، مخصص ومطور لغايات التوعية المجتمعية والتعليمية والفحص الذاتي الأولي فقط، ولا يمثل بأي حال من الأحوال تشخيصاً طبياً نهائياً يعوضك عن زيارة الطبيب المختص.")
