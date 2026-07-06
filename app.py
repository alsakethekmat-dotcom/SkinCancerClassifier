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
    initial_sidebar_state="expanded"
)

# كود CSS المطور بالكامل لتغيير شكل صندوق الرفع وجعله تفاعلياً وعربياً 100%
st.markdown("""
    <style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800&display=swap');

/* =======================================================
   1. الخط والاتجاه العام الآمن
======================================================= */
* {
    font-family: 'Tajawal', sans-serif !important;
}

html, body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"], 
[data-testid="stMarkdownContainer"], .stMarkdown, label, p, h1, h2, h3, h4, h5, h6, 
.stCheckbox, .stAlert {
    direction: rtl !important;
    text-align: right !important;
}

body {
    background: #f4f7f6 !important;
}

/* =======================================================
   2. القائمة الجانبية
======================================================= */
[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-left: 1px solid #e5e7eb;
}

/* =======================================================
   3. العناوين الأساسية
======================================================= */
.title-text {
    font-size: 2.8rem;
    font-weight: 800;
    background: -webkit-linear-gradient(45deg,#0284c7,#0ea5e9);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center !important;
    margin-bottom: 8px;
}

.subtitle-text {
    color: #475569;
    font-size: 1.25rem;
    font-weight: 600;
    text-align: center !important;
    margin-bottom: 35px;
}

/* =======================================================
   4. حجم الخط العام للاستبيان
======================================================= */
p, label, li, span, .stMarkdown, .stCaption {
    font-size: 18px !important;
    line-height: 1.9;
}

h1, h2, h3 {
    font-weight: 700 !important;
}

.stCheckbox {
    background: white;
    padding: 16px 20px;
    border-radius: 14px;
    border: 1px solid #edf2f7;
    box-shadow: 0 4px 10px rgba(0,0,0,.05);
    margin-bottom: 12px;
}

.stCheckbox label {
    font-size: 18px !important;
    font-weight: 500;
}

/* =======================================================
   5. زر بدء الفحص (الأساسي اللامع)
======================================================= */
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

/* =======================================================
   6. التنسيق الثوري والجديد لصندوق رفع الصورة (مكسور الجمود)
======================================================= */
[data-testid="stFileUploader"] {
    direction: rtl !important;
}

/* إعادة تصميم الحاوية الكبيرة بالكامل */
[data-testid="stFileUploadDropzone"] {
    border: 3px dashed #0ea5e9 !important;
    border-radius: 20px !important;
    background: #f0f9ff !important; /* خلفية زرقاء ناعمة مريحة */
    padding: 45px 20px !important;
    transition: all 0.3s ease-in-out;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 15px !important;
}

[data-testid="stFileUploadDropzone"]:hover {
    background: #e0f2fe !important; /* تفتيح الخلفية عند اللمس */
    border-color: #0284c7 !important;
    transform: translateY(-2px);
}

/* إخفاء كل الهياكل والنصوص الإنجليزية المتداخلة نهائياً */
[data-testid="stFileUploadDropzone"] section,
[data-testid="stFileUploadDropzone"] div span,
[data-testid="stFileUploadDropzone"] div small {
    display: none !important;
}

/* حقن النص التوجيهي العربي بخط عريض وجميل */
[data-testid="stFileUploadDropzone"]::before {
    content: "📷 اسحب صورة الشامة هنا أو اضغط على الزر بالأسفل";
    display: block !important;
    font-size: 19px !important;
    font-weight: 700 !important;
    color: #0369a1 !important;
    text-align: center !important;
    margin-bottom: 5px;
}

/* تحويل الزر الداخلي "الجامد" إلى زر عصري وملون وملفت للنظر */
[data-testid="stFileUploadDropzone"] button {
    font-size: 0px !important; /* تصفير الكلمة المشوهة بالكامل */
    background: linear-gradient(90deg, #0ea5e9, #0284c7) !important; /* تلوين الزر */
    color: transparent !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 25px 80px !important; /* تكبير حجم الزر */
    cursor: pointer !important;
    box-shadow: 0 4px 12px rgba(14, 165, 233, 0.25) !important;
    transition: all 0.3s !important;
    position: relative !important;
    display: inline-block !important;
}

[data-testid="stFileUploadDropzone"] button:hover {
    background: linear-gradient(90deg, #0284c7, #0369a1) !important;
    box-shadow: 0 6px 15px rgba(2, 132, 199, 0.4) !important;
    transform: scale(1.03);
}

/* كتابة النص العربي المختار والنظيف فوق الزر الجديد */
[data-testid="stFileUploadDropzone"] button::after {
    content: "اختيار صورة من الجهاز 📂";
    color: white !important; /* خط أبيض واضح */
    font-size: 16px !important;
    font-weight: 700 !important;
    position: absolute !important;
    left: 50% !important;
    top: 50% !important;
    transform: translate(-50%, -50%) !important;
    white-space: nowrap !important;
}

/* =======================================================
   7. بطاقات الفريق
======================================================= */
.team-card {
    background: #f8fafc;
    padding: 20px;
    border-radius: 15px;
    border-right: 4px solid #0284c7;
}

.team-title {
    color: #0284c7;
    font-size: 20px;
    font-weight: 700;
}

.team-names {
    color: #334155;
    font-size: 18px;
    line-height: 2;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 2. القائمة الجانبية (فريق العمل والمدرسة)
# =========================================================
with st.sidebar:
    st.image("logo.jpeg", width=500) 
    st.markdown("### عن المشروع")
    st.info("نظام تقني يجمع بين دقة الذكاء الاصطناعي والمؤشرات السريرية لدعم الكشف المبكر عن سرطان الجلد.")
    
    st.markdown("""
    <div class="team-card">
        <div class="team-title">👩‍💻 الطالبات المبدعات</div>
        <div class="team-names">
            • سما <br>
            • رنيم <br>
            • جود <br>
            • فرح <br>
            • نورسين
        </div>
        <hr style="margin: 10px 0;">
        <div class="team-title">👩‍🏫 إشراف المعلمة</div>
        <div class="team-names">أماني أبو رمان</div>
        <hr style="margin: 10px 0;">
        <div class="team-title">🏫 المدرسة</div>
        <div class="team-names"> حكمت الساكت الأساسية </div>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# 3. الواجهة الرئيسية
# =========================================================
st.markdown('<div class="title-text">نظام الفحص الأولي لسرطان الجلد</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-text">مشروع: اكتشف مبكراً… لتنقذ حياة 🛡️</div>', unsafe_allow_html=True)

# تحديد المسار المطلق والملف
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
    st.error(f"🚨تنبيه: لم يتم تحميل ملف النموذج. تفاصيل الخطأ التقني: {e}")
    model_loaded = False

# =========================================================
# 4. الفلتر الذكي الصارم لفحص أنسجة الجلد (HSV المطور)
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
        total_pixels = combined_mask.size
        skin_percentage = (skin_pixels / total_pixels) * 100
        
        return skin_percentage > 25.0
    return False

# =========================================================
# 5. تقسيم الشاشة إلى عمودين
# =========================================================
col1, col2 = st.columns([1, 1.2], gap="large")

abcde_score = 0
uploaded_file = None

# العمود الأول: الاستبيان
with col1:
    st.markdown("### 📋 أولاً: التقييم السريري (ABCDE)")
    st.caption("أجب على الأسئلة بناءً على ملاحظتك للشامة:")
    
    if st.checkbox("A - عدم التماثل: هل شكل الشامة غير متماثل من المنتصف؟"): abcde_score += 1
    if st.checkbox("B - الحدود: هل أطراف الشامة خارجية متعرجة أو غير منتظمة؟"): abcde_score += 1
    if st.checkbox("C - اللون: هل تحتوي الشامة على تدرجات ألوان (بني، أسود، أحمر)؟"): abcde_score += 1
    if st.checkbox("D - القطر: هل يزيد القطر الإجمالي لحجم الشامة عن 6 ملم؟"): abcde_score += 1
    if st.checkbox("E - التطور: هل لاحظت تغيراً مفاجئاً في حجمها أو بدأت تنزف؟"): abcde_score += 1

# العمود الثاني: رفع الصورة
with col2:
    st.markdown("### 📸 ثانياً: الفحص الرقمي (الذكاء الاصطناعي)")
    uploaded_file = st.file_uploader("ارفع صورة قريبة وواضحة جداً للشامة", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        user_image = Image.open(uploaded_file)
        st.image(user_image, caption="الصورة الجاهزة للفحص", use_container_width=True)

# =========================================================
# 6. زر الفحص ومعالجة النتائج
# =========================================================
if uploaded_file is not None and model_loaded:
    if st.button("🚀 بـدء الـفـحـص الـشـامـل"):
        
        if not is_valid_skin_image(user_image):
            st.error("❌ تم إيقاف الفحص: النظام لم يتعرف على أنسجة جلد بشري في الصورة المرفوعة. يرجى التأكد من رفع صورة واضحة ومقربة للشامة على الجلد (لا تقم برفع صور لأشياء أخرى).")
            st.stop()
            
        with st.spinner("🤖 جاري تحليل الأنسجة وربط البيانات السريرية..."):
            try:
                img_resized = user_image.resize((224, 224))
                img_array = image.img_to_array(img_resized)
                img_array = tf.keras.applications.efficientnet.preprocess_input(img_array)
                img_array = np.expand_dims(img_array, axis=0)
                
                prediction = model.predict(img_array)[0][0]
                melanoma_probability = prediction * 100
                benign_probability = 100 - melanoma_probability
                
                st.markdown("---")
                st.markdown("### 📊 التقرير الطبي المشترك:")
                
                if melanoma_probability >= 70 or (melanoma_probability >= 40 and abcde_score >= 3):
                    st.error(f"⚠️ مستوى الخطورة المحتملة: مرتفع")
                    st.write(f"**نسبة الاشتباه (بالذكاء الاصطناعي):** {melanoma_probability:.1f}%")
                    st.write(f"**علامات الخطر السريرية التي لاحظتها:** {abcde_score} من 5")
                    st.info("💡التوجيه: يُنصح بشدة بحجز موعد لدى طبيب الجلدية المختص لإجراء فحص سريري دقيق.")
                    
                elif 30 <= melanoma_probability < 70 or (melanoma_probability < 40 and abcde_score >= 2):
                    st.warning(f"🟡 مستوى الخطورة المحتملة: متوسط")
                    st.write(f"**نسبة الاشتباه (بالذكاء الاصطناعي):** {melanoma_probability:.1f}%")
                    st.write(f"**علامات الخطر السريرية التي لاحظتها:** {abcde_score} من 5")
                    st.info("💡 التوجيه: يُفضل مراقبة الشامة بشكل دوري وإعادة الفحص في حال حدوث أي تغيرات.")
                    
                else:
                    st.success(f"✅ مستوى الخطورة المحتملة: منخفض (مؤشرات مطمئنة)")
                    st.write(f"**نسبة السلامة (بالذكاء الاصطناعي):** {benign_probability:.1f}%")
                    st.info("💡 التوجيه: لا توجد علامات قلق ظاهرة حالياً. حافظ على فحص الجلد ذاتياً بانتظام.")
                    
            except Exception as e:
                st.error(f"حدث خطأ غير متوقع أثناء معالجة الصورة: {e}")

st.markdown("---")
st.caption("🚨 إخلاء مسؤولية: هذا التطبيق هو مخرج لمشروع علمي ابتكاري ، مخصص لغايات التوعية والفحص الذاتي الأولي فقط، ولا يعتبر بديلاً عن التشخيص الطبي الاحترافي.")
