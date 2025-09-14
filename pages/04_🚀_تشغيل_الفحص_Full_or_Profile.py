
import streamlit as st
import pandas as pd
from pathlib import Path
import yaml
from jobs.run_full_audit import run_full_audit

st.set_page_config(page_title="تشغيل الفحص", page_icon="🚀")
st.title("🚀 تشغيل الفحص")

urls = st.session_state.get("input_urls", [])
st.caption(f"عدد الروابط المحفوظة في الجلسة: {len(urls)}")
profile = st.selectbox("اختر Profile", ["full", "content_only", "tech_only", "spam_only", "trust_only", "competitive"], index=0)
enable_filler = st.checkbox("تفعيل وحدة الجمل الحشوية", True)
enable_trust = st.checkbox("تفعيل Trust & Compliance", True)
enable_internal = st.checkbox("تفعيل الروابط الداخلية (تجريبي)", False)

if st.button("ابدأ الفحص الآن"):
    if not urls:
        st.warning("لا توجد روابط في الجلسة. عد لصفحة مصادر الروابط أولاً.")
    else:
        with st.spinner("جاري تشغيل الفحص، يرجى الانتظار..."):
            df_unified, sub_reports = run_full_audit(
                urls=urls,
                profile=profile,
                enable_flags={
                    "filler_detector": enable_filler,
                    "trust_compliance": enable_trust,
                    "internal_links": enable_internal,
                },
                output_dir=Path("storage/outputs")
            )
        st.success("تم الانتهاء! انتقل إلى صفحة التقرير الموحّد لعرض النتائج.")
        st.session_state["last_unified_df"] = df_unified
        st.session_state["last_sub_reports"] = sub_reports
