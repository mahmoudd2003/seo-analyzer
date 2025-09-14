
import streamlit as st
import yaml
from pathlib import Path

st.set_page_config(page_title="الإعدادات وملفات YAML", page_icon="⚙️")
st.title("⚙️ الإعدادات وملفات YAML")

CONFIG_DIR = Path("configs")

def edit_yaml(name: str):
    path = CONFIG_DIR / name
    st.subheader(name)
    default_text = path.read_text(encoding="utf-8") if path.exists() else ""
    txt = st.text_area(f"تحرير {name}", value=default_text, height=300)
    if st.button(f"حفظ {name}"):
        path.write_text(txt, encoding="utf-8")
        st.success(f"تم حفظ {name}")

for f in ["filler_rules.yaml", "trust_compliance.yaml", "scoring.yaml", "profiles.yaml", "site.yaml"]:
    edit_yaml(f)
