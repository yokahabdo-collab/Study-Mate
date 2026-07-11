import streamlit as st
import google.generativeai as genai

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Study Mate", page_icon="📚", layout="wide")

# ضعي مفتاحك الحقيقي هنا بين علامتي التنصيص
genai.configure(api_key="ضعي_مفتاحك_هنا") 

if 'page' not in st.session_state:
    st.session_state.page = "الرئيسية"

def go_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# الدالة المسرعة للحفاظ على النظام
@st.cache_data(show_spinner=False)
def get_ai_response(prompt_text, user_input):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(f"{prompt_text} {user_input}")
    return response.text

# ---------------- الصفحة الرئيسية ----------------
if st.session_state.page == "الرئيسية":
    st.markdown("<h1 style='color: black;'>Study Mate 🎓</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: black; font-size: 20px;'>شريكك الأذكى في المذاكرة، بنساعدك تذاكر بذكاء... مش بمجهود أكتر.</p>", unsafe_allow_html=True)
    st.write("---")
    st.subheader("كيف تحب أن تذاكر اليوم؟ اختر الطريقة التي تناسبك: 📚")
    st.write("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("📝 **تلخيص ذكي**")
        if st.button("دخول التلخيص"): go_to("تلخيص")
        st.warning("🧠 **خرائط ذهنية**")
        if st.button("دخول الخرائط"): go_to("خرائط")
    with col2:
        st.success("📖 **وصف المنهج**")
        if st.button("دخول الوصف"): go_to("وصف")
        st.error("🎥 **شرح بالفيديو**")
        if st.button("دخول الفيديوهات"): go_to("فيديو")
    with col3:
        st.info("❓ **حل الأسئلة**")
        if st.button("دخول الاختبارات"): go_to("أسئلة")

# ---------------- الصفحات الفرعية ----------------
else:
    st.title(f"صفحة: {st.session_state.page}")
    
    # استخدام Form لضمان السرعة ومنع إعادة التحميل المزعج
    with st.form(key='analysis_form'):
        uploaded_file = st.file_uploader("ارفعي ملف المذاكرة (PDF أو صورة):", type=['pdf', 'jpg', 'png'])
        text_input = st.text_area("أو اكتبي النص مباشرة هنا:")
        submit_button = st.form_submit_button(label='ابدأ التحليل 🚀')
    
    if submit_button:
        prompts = {
            "تلخيص": "لخص النص التالي بأسلوب ممتاز ومقسم لنقاط:",
            "خرائط": "حول النص التالي لخريطة ذهنية بصرية تستخدم شخصيات كرتونية (مثل سبونج بوب أو توم وجيري) أو ممثلين كوميديين لتوصيل المعلومة بشكل مضحك ومبتكر، استخدم صيغة Mermaid.js:",
            "وصف": "اشرح النص التالي بأسلوب مبسط جداً كأنه قصة مشوقة:",
            "فيديو": "ابحث عن رابط فيديو تعليمي على يوتيوب يشرح الموضوع التالي، واكتب وصفاً قصيراً له:",
            "أسئلة": "حل السؤال التالي واشرح الخطوات بأسلوب مشجع ومضحك:"
        }
        
        prompt_text = prompts.get(st.session_state.page, "لخص هذا:")
        
        with st.spinner('جاري التحليل بطريقة ممتعة...'):
            response_text = get_ai_response(prompt_text, text_input)
            
            # عرض النتيجة
            if st.session_state.page == "فيديو":
                st.success("إليك الفيديو المقترح:")
                st.write(response_text)
                if "http" in response_text:
                    link = [s for s in response_text.split() if "http" in s][0]
                    st.video(link)
            elif st.session_state.page == "خرائط":
                st.success("إليك الخريطة الذهنية:")
                st.markdown(f"```mermaid\n{response_text.replace('```mermaid', '').replace('```', '')}\n```")
            else:
                st.success("إليك النتيجة:")
                st.write(response_text)
        
    if st.button("⬅️ العودة للرئيسية"): go_to("الرئيسية")