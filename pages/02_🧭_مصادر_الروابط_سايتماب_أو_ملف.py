
import streamlit as st
import pandas as pd
from pathlib import Path
from urllib.parse import urlparse
from collectors.sitemap_crawler import extract_urls_from_sitemap

st.set_page_config(page_title="مصادر الروابط", page_icon="🧭")

st.title("🧭 مصادر الروابط: Sitemap أو ملف")
mode = st.radio("اختر طريقة الإدخال:", ["Sitemap URL", "رفع ملف روابط (TXT/CSV)"], horizontal=True)
urls = []

if mode == "Sitemap URL":
    sitemap_url = st.text_input("ضع رابط sitemap.xml", placeholder="https://example.com/sitemap.xml")
    if st.button("جلب الروابط من السايت ماب"):
        if sitemap_url.strip():
            with st.spinner("جارِ جلب الروابط من السايت ماب..."):
                try:
                    urls = extract_urls_from_sitemap(sitemap_url.strip(), respect_robots=False)
                    st.success(f"تم استخراج {len(urls)} رابطًا.")
                except Exception as e:
                    st.error(f"فشل الجلب: {e}")
        else:
            st.warning("الرجاء إدخال رابط صحيح.")
else:
    up = st.file_uploader("ارفع ملف TXT (رابط في كل سطر) أو CSV يحوي عمود URL", type=["txt","csv"])
    if up is not None:
        try:
            if up.name.lower().endswith(".txt"):
                urls = [line.strip() for line in up.getvalue().decode("utf-8", "ignore").splitlines() if line.strip()]
            else:
                df = pd.read_csv(up)
                col = "URL" if "URL" in df.columns else df.columns[0]
                urls = df[col].dropna().astype(str).tolist()
            st.success(f"تم تحميل {len(urls)} رابطًا.")
        except Exception as e:
            st.error(f"فشل قراءة الملف: {e}")

if urls:
    st.dataframe(pd.DataFrame({"URL": urls}).head(50))
    if st.button("حفظ الروابط للجلسة"):
        st.session_state["input_urls"] = urls
        st.success("تم حفظ الروابط في الجلسة. يمكنك الانتقال إلى صفحة تشغيل الفحص.")
