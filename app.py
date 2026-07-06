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
    initial_sidebar_state="collapsed" # إخفاء القائمة الجانبية تماماً لمظهر أكثر اتساعاً وعصرية
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

# كود CSS الشامل لتنسيق الصفحات وصندوق الرفع والـ Header الثابت
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

/* العناوين الأساسية */
.title-text {
    font-size: 3rem;
    font-weight: 800;
    background: -webkit-linear-gradient(45deg,#0284c7,#0ea5e9);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center !important;
    margin-bottom: 8px;
}

.subtitle-text {
    color: #475569;
    font-size: 1.4rem;
    font-weight: 600;
    text-align: center !important;
    margin-bottom: 35px;
}

/* حجم خطوط النصوص والاستبيان */
p, label, li, span, .stMarkdown, .stCaption {
    font-size: 18px !important;
    line-height: 1.9;
}

.stCheckbox {
    background: white;
    padding: 16px 20px;
    border-radius: 14px;
    border: 1px solid #edf2f7;
    box-shadow: 0 4px 10px rgba(0,0,0,.05);
    margin-bottom: 12px;
}

/* الأزرار الكبيرة التفاعلية */
.stButton>button {
    width: 100%;
    background: linear-gradient(90deg,#0284c7,#0ea5e9);
    color: white !important;
    font-size: 22px !important;
    font-weight: 700;
    border: none;
    border-radius: 50px;
    padding: 14px;
    transition: .3s;
    box-shadow: 0 5px 15px rgba(2,132,199,.35);
}

.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(2,132,199,.45);
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
    padding: 40px 20px !important;
    transition: all 0.3s ease-on-out !important;
}

.stFileUploader section:hover {
    background-color: #e0f2fe !important;
    border-color: #0284c7 !important;
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
    color: #0369a1 !important;
    text-align: center !important;
    margin-bottom: 20px !important;
}

.stFileUploader button {
    background: linear-gradient(90deg, #0ea5e9, #0284c7) !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 22px 60px !important;
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
    font-size: 16px !important;
    font-weight: 700 !important;
    position: absolute !important;
    left: 50% !important;
    top: 50% !important;
    transform: translate(-50%, -50%) !important;
    white-space: nowrap !important;
}

/* بطاقة فريق العمل في الصفحة الرئيسية */
.team-container {
    background: white;
    padding: 30px;
    border-radius: 20px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.05);
    border-right: 6px solid #0284c7;
    margin-top: 25px;
}
.team-grid {
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 20px;
}
.team-section {
    flex: 1;
    min-width: 200px;
}
.team-title {
    color: #0284c7;
    font-size: 22px;
    font-weight: 700;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 2. تحميل نموذج الذكاء الاصطناعي (يتم مرة واحدة في الخلفية)
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

# دالة فلتر الأنسجة
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
# 3. الإطار العلوي الثابت للزاوية اليمنى (Header) - يظهر خارج الرئيسية
# =========================================================
if st.session_state.page != 'home':
    header_left, header_right = st.columns([5, 1])
    with header_right:
        # عرض اللوغو في أقصى اليمين وجعل أسفله زر مخفي أو واضح للعودة للرئيسية عند الضغط
        st.image("logo.jpeg", width=120)
        if st.button("🏠 العودة للرئيسية", key="nav_to_home_logo"):
            go_home()
    with header_left:
        st.markdown(f"<h3 style='color:#0284c7; margin-top:20px;'>نظام الفحص الأولي الذكي</h3>", unsafe_allow_html=True)
    st.markdown("<hr style='margin-top:0; margin-bottom:30px;'>", unsafe_allow_html=True)


# =========================================================
# 4. منطق عرض الصفحات (Page Routing)
# =========================================================

# ----------------- [صفحة 1: الصفحة الرئيسية] -----------------
if st.session_state.page == 'home':
    # هيدر الصفحة الرئيسية يتوسطه الشعار والعنوان
    center_col1, center_col2, center_col3 = st.columns([1, 2, 1])
    with center_col2:
        st.image("logo.jpeg", use_container_width=True)
    
    st.markdown('<div class="title-text">نظام الفحص الأولي لسرطان الجلد</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle-text">مشروع ابتكاري: اكتشف مبكراً… لتنقذ حياة 🛡️</div>', unsafe_allow_html=True)
    
    st.info("💡 عن النظام: نظام تقني ذكي يجمع بين دقة خوارزميات الذكاء الاصطناعي والمؤشرات السريرية المعتمدة عالمياً لدعم الكشف المبكر عن آفات الجلد وشاماته بكل خصوصية وسهولة.")
    
    # بطاقة فريق العمل والمعلومات الأساسية للمشروع
    st.markdown("""
    <div class="team-container">
        <div class="team-grid">
            <div class="team-section">
                <div class="team-title">👩‍💻 الطالبات المبدعات</div>
                <p>• سما &nbsp;&nbsp; • رنيم &nbsp;&nbsp; • جود &nbsp;&nbsp; • فرح &nbsp;&nbsp; • نورسين</p>
            </div>
            <div class="team-section">
                <div class="team-title">👩‍🏫 إشراف المعلمة</div>
                <p>أماني أبو رمان</p>
            </div>
            <div class="team-section">
                <div class="team-title">🏫 المدرسة</div>
                <p>حكمت الساكت الأساسية</p>
            </div>
        </div>
    </div>
    <br><br>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 ابـدء الـتـحـقـق والـفـحـص الآن"):
        st.session_state.page = 'survey'
        st.rerun()

# ----------------- [صفحة 2: استبيان ABCDE السريري] -----------------
elif st.session_state.page == 'survey':
    st.markdown("## 📋 الخطوة الأولى: التقييم السريري (ABCDE)")
    st.write("الرجاء الإجابة على الأسئلة التالية بكل دقة بناءً على ملاحظتك البصرية للشامة الحالية:")
    
    st.markdown("<br>", unsafe_allow_html=True)
    a = st.checkbox("A - عدم التماثل: هل شكل الشامة غير متماثل (إذا قسمتها من المنتصف لا يتطابق النصفان)؟")
    b = st.checkbox("B - الحدود: هل أطراف الشامة الخارجية متعرجة، خشنة، أو غير منتظمة؟")
    c = st.checkbox("C - اللون: هل تحتوي الشامة على تدرجات ألوان مختلفة (بني، أسود، أحمر، رمادي)؟")
    d = st.checkbox("D - القطر: هل يزيد القطر الإجمالي لحجم الشامة عن 6 ملم (أكبر من ممحاة قلم رصاص)؟")
    e = st.checkbox("E - التطور: هل لاحظت تغيراً مفاجئاً في حجمها، لونها، شكلها، أو بدأت تسبب حكة ونزيف؟")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("حفظ الإجابات والانتقال لرفع الصورة ➡️"):
        st.session_state.abcde_score = sum([a, b, c, d, e])
        st.session_state.page = 'upload'
        st.rerun()

# ----------------- [صفحة 3: رفع الصورة وتحليلها] -----------------
elif st.session_state.page == 'upload':
    st.markdown("## 📸 الخطوة الثانية: الفحص الرقمي (الذكاء الاصطناعي)")
    st.write("الرجاء رفع صورة قريبة جداً، واضحة، وفي إضاءة جيدة للشامة المستهدفة:")
    
    if not model_loaded:
        st.error("🚨 خطأ تقني: لم يتم تحميل ملف ذكاء اصطناعي صالح كـ 'best_skin_cancer_model.keras' في المجلد الرئيسي.")
    
    uploaded_file = st.file_uploader("ارفع الصورة هنا", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        st.session_state.user_image = Image.open(uploaded_file)
        st.image(st.session_state.user_image, caption="الصورة التي تم رفعها بنجاح", width=350)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("🚀 بـدء الـفـحـص الـشـامـل وإظهار التقرير"):
            # التحقق من فلتر الأنسجة
            if not is_valid_skin_image(st.session_state.user_image):
                st.error("❌ تم إيقاف الفحص: لم يتعرف النظام على نسيج جلد بشري في الصورة. يرجى التقاط صورة مقربة وواضحة للشامة فقط على البشرة.")
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

# ----------------- [صفحة 4: التقرير الطبي والنتيجة النهائية] -----------------
elif st.session_state.page == 'result':
    st.markdown("## 📊 التقرير الطبي المشترك والنتيجة النهائية")
    st.write("تم دمج نتائج التقييم السريري (ABCDE) مع الفحص الرقمي العميق للنموذج:")
    
    abcde_score = st.session_state.abcde_score
    melanoma_probability = st.session_state.prediction * 100
    benign_probability = 100 - melanoma_probability
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # خوارزمية تحديد النتيجة الطبية المشتركة
    if melanoma_probability >= 70 or (melanoma_probability >= 40 and abcde_score >= 3):
        st.error(f"⚠️ مستوى الخطورة المحتملة: مرتفع")
        st.write(f"**نسبة الاشتباه المبني على الذكاء الاصطناعي:** {melanoma_probability:.1f}%")
        st.write(f"**علامات الخطر السريرية المرصودة من قبلك:** {abcde_score} من أصل 5 علامات.")
        st.info("💡 التوجيه الطبي: يُنصح بشدة وبشكل عاجل بحجز موعد لدى طبيب استشاري أمراض جلدية لإجراء فحص مجهري (Dermoscopy) أو أخذ خزعة تأكيدية.")
        
    elif 30 <= melanoma_probability < 70 or (melanoma_probability < 40 and abcde_score >= 2):
        st.warning(f"🟡 مستوى الخطورة المحتملة: متوسط (بحاجة لمتابعة)")
        st.write(f"**نسبة الاشتباه المبني على الذكاء الاصطناعي:** {melanoma_probability:.1f}%")
        st.write(f"**علامات الخطر السريرية المرصودة من قبلك:** {abcde_score} من أصل 5 علامات.")
        st.info("💡 التوجيه الطبي: يفضل مراقبة الشامة بانتظام (مرة كل شهر) وملاحظة أي تطور في الحجم أو اللون، واستشارة الطبيب في حال استمرار التغير.")
        
    else:
        st.success(f"✅ مستوى الخطورة المحتملة: منخفض (مؤشرات مطمئنة جداً)")
        st.write(f"**نسبة سلامة الأنسجة (حميدة):** {benign_probability:.1f}%")
        st.write(f"**علامات الخطر السريرية المرصودة:** {abcde_score} من أصل 5.")
        st.info("💡 التوجيه الطبي: المؤشرات تبدو طبيعية ومطمئنة ولا تدعو للقلق البتة. حافظ على حماية جلدك من أشعة الشمس المباشرة وافحص نفسك دورياً.")
        
    st.markdown("<br><br><hr>", unsafe_allow_html=True)
    if st.button("🔄 إجراء فحص جديد لمريض آخر"):
        go_home()

# =========================================================
# 5. تذييل الصفحة الثابت (Footer)
# =========================================================
st.markdown("<br><br><br><br>", unsafe_allow_html=True)
st.caption("🚨 إخلاء مسؤولية قانوني وطبي: هذا التطبيق هو مخرج لمشروع ابتكاري مدرسي، مخصص ومطور لغايات التوعية المجتمعية والتعليمية والفحص الذاتي الأولي فقط، ولا يمثل بأي حال من الأحوال تشخيصاً طبياً نهائياً يعوضك عن زيارة الطبيب المختص.")
