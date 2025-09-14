
# SEO System (Streamlit + Arabic Reports)

## تشغيل محلي
```bash
python -m venv .venv
source .venv/bin/activate  # على ويندوز: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## ماذا يقدّم الإصدار الأول؟
- واجهة Streamlit عربية مع صفحات:
  - مصادر الروابط (Sitemap/ملف)
  - الإعدادات (تحرير YAML للقواعد)
  - تشغيل الفحص (Full/Profile + Flags)
  - التقرير الموحّد بالعربية + تقارير فرعية
- وحدة **الجمل الحشوية + البدائل** (قابلة للتوسيع).
- طبقة **Trust & Compliance** (قابلة للتوسيع).
- تقارير CSV بالعربية تحفظ في `storage/outputs/`.

> ملاحظة: هذا إصدار مبدئي (Scaffold). استبدل المنطق الاختباري في `jobs/run_full_audit.py` بمنطق التحليل الحقيقي تدريجيًا.
