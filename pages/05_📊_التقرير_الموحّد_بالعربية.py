
import streamlit as st
import pandas as pd

st.set_page_config(page_title="التقرير الموحّد بالعربية", page_icon="📊")
st.title("📊 التقرير الموحّد بالعربية")

df = st.session_state.get("last_unified_df")
if df is None:
    st.info("لا يوجد تقرير بعد. شغّل الفحص أولاً.")
else:
    st.dataframe(df)
    st.download_button("⬇️ تنزيل CSV", data=df.to_csv(index=False).encode("utf-8"), file_name="unified_report_ar.csv", mime="text/csv")
