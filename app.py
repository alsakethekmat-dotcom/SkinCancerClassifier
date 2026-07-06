import streamlit as st
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image
import cv2
import os

# =========================================================
# 1. إعدادات الصفحة والتصميم البصري العصري (Modern UI)
# =========================================================
st.set_page_config(
    page_title="نظام الفحص الذكي - اكتشف مبكراً",
    page_icon="🔬", 
    layout="wide", 
    initial_sidebar_state="collapsed" # إخفاء القائمة الجانبية تماماً لمظهر عصري
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

# كود CSS المطور لحل مشاكل الأبعاد والجمود والضغط تماماً
st.markdown("""
    <style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800&display=swap');

/* الخط والاتجاه العام */
* {
    font-family: 'Tajawal', sans-serif !important;
}

html, body, [data-testid="stAppViewContainer"], [data-testid="stMarkdownContainer"], 
.stMarkdown, label, p, h1, h2, h3, h4, h5, h6, .stCheckbox, .stAlert {
    direction: rtl !important;
    text-align: right !important;
}

body {
    background: #f4f7f6 !important;
}

/* العناوين الأساسية المدمجة لعدم إحداث سكرول */
.title-text {
    font-size: 2.2rem;
    font-weight: 800;
    background: -webkit-linear-gradient(45deg,#0284c7,#0ea5e9);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center !important;
    margin-bottom: 2px;
}

.subtitle-text {
    color: #475569;
    font-size: 1.1rem;
    font-weight: 600;
    text-align: center !important;
    margin-bottom: 20px;
}

/* حجم خطوط النصوص والاستبيان */
p, label, li, span, .stMarkdown, .stCaption {
    font-size: 17px !important;
    line-height: 1.7;
}

.stCheckbox {
    background: white;
    padding: 12px 18px;
    border-radius: 12px;
    border: 1px solid #edf2f7;
    box-shadow: 0 4px 10px rgba(0,0,0,.03);
    margin-bottom: 8px;
}

/* 1. الأزرار الأساسية الكبيرة (تم حصرها في كلاس مخصص لكي لا تخرب بقية الأزرار) */
.main-btn .stButton>button {
    width: 100% !important;
    background: linear-gradient(90deg,#0284c7,#0ea5e9) !important;
    color: white !important;
    font-size: 20px !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 50px !important;
    padding: 12px !important;
    transition: .3s !important;
    box-shadow: 0 5px 15px rgba(2,132,199,.35) !important;
}

.main-btn .stButton>button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 20px rgba(2,132,199,.45) !important;
}

/* 2. زر العودة للرئيسية (أنيق، صغير، وفي الزاوية المقابلة دون تمطيط) */
.nav-btn .stButton>button {
    width: auto !important;
    background: white !important;
    color: #0284c7 !important;
    border: 1px solid #0ea5e9 !important;
    font-size: 14px !important;
    font-weight: 700 !important;
    padding: 6px 16px !important;
    border-radius: 8px !important;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05) !important;
    transition: 0.2s;
}
.nav-btn .stButton>button:hover {
    background: #f0f9ff !important;
    color: #0284c7 !important;
    border-color: #0284c7 !important;
}

/* تنسيق صندوق رفع الملفات الاحترافي والمعرب */
.stFileUploader {
    direction: rtl !important;
    text-align: right !important;
}

.stFileUploader section {
    border: 3px dashed #0ea5e9 !important;
    border-radius: 20px !important;
    background-color: #f0f9ff !important;
    padding: 35px 20px !important;
    transition: all 0.3s ease-in-out !important;
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
    font-size: 17px !important;
    font-weight: 700 !important;
    color: #0369a1 !important;
    text-align: center !important;
    margin-bottom: 15px !important;
}

.stFileUploader button {
    background: linear-gradient(90deg, #0ea5e9, #0284c7) !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 20px 50px !important;
    cursor: pointer !important;
    box-shadow: 0 4px 12px rgba(14, 165, 233, 0.25) !important;
    transition: all 0.3s !important;
    position: relative !important;
    display: block !important;
    margin: 0 auto !important;
    color: transparent !important;
    font-size: 0px !important;
}

.stFileUploader button::after {
    content: "اختيار صورة من الجهاز 📂" !important;
    color: white !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    position: absolute !important;
    left: 50% !important;
    top: 50% !important;
    transform: translate(-50%, -50%) !important;
    white-space: nowrap !important;
}

/* بطاقة فريق العمل المدمجة جداً لمنع السكرول */
.team-container {
    background: white;
    padding: 15px 20px;
    border-radius: 15px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.03);
    border-right: 5px solid #0284c7;
}
.team-title {
    color: #0284c7;
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 8px;
}
.team-text {
    font-size: 15px !important;
    margin-bottom: 4px !important;
    line-height: 1.5 !important;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 2. تحميل نموذج الذكاء الاصطناعي في الخلفية
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


# =========================================================
# 3. الإطار العلوي الثابت المتعاكس (Header) - يظهر خارج الرئيسية
# =========================================================
if st.session_state.page != 'home':
    # تقسيم متوازن: زر العودة في أقصى اليسار، العنوان في الوسط، واللوغو في أقصى اليمين بدون انضغاط
    header_btn, header_title, header_logo = st.columns([1.5, 4, 1.5])
    with header_logo:
        st.image("logo.jpeg", width=85) # حجم ثابت ومحمي تماماً من الضغط والتشويه
    with header_title:
        st.markdown("<h3 style='color:#0284c7; margin-top:18px; text-align:right;'>نظام الفحص الأولي الذكي</h3>", unsafe_allow_html=True)
    with header_btn:
        st.markdown('<div class="nav-btn" style="margin-top:18px; text-align:left;">', unsafe_allow_html=True)
        if st.button("🏠 العودة للرئيسية", key="nav_to_home_logo"):
            go_home()
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<hr style='margin-top:5px; margin-bottom:20px;'>", unsafe_allow_html=True)


# =========================================================
# 4. منطق عرض الصفحات المتتابعة
# =========================================================

# ----------------- [صفحة 1: الصفحة الرئيسية المدمجة] -----------------
if st.session_state.page == 'home':
    # عرض اللوغو في الأعلى بحجم مدمج وأنيق
    c1, c2, c3 = st.columns([2, 0.8, 2])
    with c2:
        st.image("logo.jpeg", width=120)
    
    st.markdown('<div class="title-text">نظام الفحص الأولي لسرطان الجلد</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle-text">مشروع ابتكاري: اكتشف مبكراً… لتنقذ حياة 🛡️</div>', unsafe_allow_html=True)
    
    # التوزيع الأفقي الذكي لملء الشاشة ومنع السكرول
    col_info, col_team = st.columns([1.2, 1], gap="medium")
    
    with col_info:
        st.markdown("<h4 style='color:#0284c7; margin-top:0;'>🔬 عن النظام</h4>", unsafe_allow_html=True)
        st.info("نظام تقني ذكي يجمع بين دقة خوارزميات الذكاء الاصطناعي والمؤشرات السريرية المعتمدة عالمياً لدعم الكشف المبكر عن آفات الجلد وشاماته بكل خصوصية وسهولة وبأعلى درجات الأمان الطبي.")
    
    with col_team:
        st.markdown("""
        <div class="team-container">
            <div class="team-title">👥 بطاقة تعريفية</div>
            <p class="team-text"><b>👩‍💻 الطالبات:</b> سما، رنيم، جود， فرح، نورسين</p>
            <p class="team-text"><b>👩‍🏫 الإشراف:</b> المعلمة أماني أبو رمان</p>
            <p class="team-text"><b>🏫 المدرسة:</b> حكمت الساكت الأساسية</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="main-btn">', unsafe_allow_html=True)
    if st.button("🚀 ابـدء الـتـحـقـق والـفـحـص الآن"):
        st.session_state.page = 'survey'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------- [صفحة 2: استبيان ABCDE السريري] -----------------
elif st.session_state.page == 'survey':
    st.markdown("## 📋 الخطوة الأولى: التقييم السريري (ABCDE)")
    st.write("الرجاء الإجابة على الأسئلة التالية بناءً على ملاحظتك البصرية للشامة الحالية:")
    
    a = st.checkbox("A - عدم التماثل: هل شكل الشامة غير متماثل (إذا قسمتها من المنتصف لا يتطابق النصفان)؟")
    b = st.checkbox("B - الحدود: هل أطراف الشامة الخارجية متعرجة، خشنة، أو غير منتظمة؟")
    c = st.checkbox("C - اللون: هل تحتوي الشامة على تدرجات ألوان مختلفة (بني، أسود، أحمر، رمادي)؟")
    d = st.checkbox("D - القطر: هل يزيد القطر الإجمالي لحجم الشامة عن 6 ملم؟")
    e = st.checkbox("E - التطور: هل لاحظت تغيراً مفاجئاً في حجمها، أو بدأت تسبب حكة ونزيف؟")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="main-btn">', unsafe_allow_html=True)
    if st.button("حفظ الإجابات والانتقال لرفع الصورة ➡️"):
        st.session_state.abcde_score = sum([a, b, c, d, e])
        st.session_state.page = 'upload'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------- [صفحة 3: رفع الصورة وتحليلها] -----------------
elif st.session_state.page == 'upload':
    st.markdown("## 📸 الخطوة الثانية: الفحص الرقمي (الذكاء الاصطناعي)")
    st.write("الرجاء رفع صورة قريبة جداً وواضحة للشامة المستهدفة:")
    
    if not model_loaded:
        st.error("🚨 خطأ تقني: لم يتم تحميل ملف ذكاء اصطناعي صالح كـ 'best_skin_cancer_model.keras'.")
    
    uploaded_file = st.file_uploader("ارفع الصورة هنا", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        st.session_state.user_image = Image.open(uploaded_file)
        
        # تنسيق عرض الصورة بشكل منظم في المنتصف
        img_c1, img_c2, img_c3 = st.columns([1, 1, 1])
        with img_c2:
            st.image(st.session_state.user_image, caption="الصورة المرفوعة جاهزة للفحص", width=250)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="main-btn">', unsafe_allow_html=True)
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
                        st.error(f"حدث خطأ برمي أثناء التحليل الفني: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

# ----------------- [صفحة 4: التقرير الطبي والنتيجة النهائية] -----------------
elif st.session_state.page == 'result':
    st.markdown("## 📊 التقرير الطبي المشترك والنتيجة النهائية")
    
    abcde_score = st.session_state.abcde_score
    melanoma_probability = st.session_state.prediction * 100
    benign_probability = 100 - melanoma_probability
    
    # خوارزمية تحديد النتيجة الطبية المشتركة
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
    st.markdown('<div class="main-btn">', unsafe_allow_html=True)
    if st.button("🔄 إجراء فحص جديد لمريض آخر"):
        go_home()
    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# 5. تذييل الصفحة الثابت (Footer)
# =========================================================
st.markdown("<br><br>", unsafe_allow_html=True)
st.caption("🚨 إخلاء مسؤولية قانوني وطبي: هذا التطبيق هو مخرج لمشروع ابتكاري مدرسي، مخصص ومطور لغايات التوعية المجتمعية والتعليمية والفحص الذاتي الأولي فقط، ولا يمثل بأي حال من الأحوال تشخيصاً طبياً نهائياً يعوضك عن زيارة الطبيب المختص.")
