
import streamlit as st
import pandas as pd

st.set_page_config(page_title="تقارير فرعية", page_icon="🧩")
st.title("🧩 التقارير الفرعية")

sub_reports = st.session_state.get("last_sub_reports", {})
if not sub_reports:
    st.info("لا توجد تقارير فرعية بعد. شغّل الفحص أولاً.")
else:
    tabs = st.tabs(list(sub_reports.keys()))
    for tab, key in zip(tabs, sub_reports.keys()):
        with tab:
            df = sub_reports[key]
            st.dataframe(df)
            st.download_button("⬇️ تنزيل CSV", data=df.to_csv(index=False).encode("utf-8"), file_name=f"{key}.csv", mime="text/csv")
