
import streamlit as st

st.set_page_config(page_title="SEO System 🇦🇪", page_icon="📈", layout="wide")

st.markdown('<link rel="stylesheet" href="assets/styles.css">', unsafe_allow_html=True)

st.title("🚀 نظام تدقيق الـSEO المتكامل")
st.write(
    "استخدم التبويبات على اليسار: ابدأ من **مصادر الروابط** ثم **الإعدادات** ثم **تشغيل الفحص** لعرض **التقرير الموحّد بالعربية**."
)
st.info("نصيحة: يمكنك إدخال رابط sitemap.xml أو رفع ملف يحتوي على الروابط المطلوب فحصها.")

st.markdown("---")
st.subheader("ما الذي يقدمه هذا النظام؟")
st.markdown(
    """
- تقرير موحّد بالعربية يجمع (Helpful/E-E-A-T/YMYL/Trust/Spam/Tech/Media/Internal Links/Freshness).
- تقارير فرعية لكل وحدة فحص.
- وحدة **كشف الجمل الحشوية** مع **بدائل ذكية** جاهزة بالعربية.
- طبقة **Trust & Compliance** لقياس الثقة والامتثال.
- **إشارات التفاعل** (Usefulness Proxy) عند توافر GA4/GSC.
    """
)
