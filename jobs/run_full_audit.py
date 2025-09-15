
from pathlib import Path
from typing import List, Dict, Tuple
import pandas as pd

from collectors.html_fetcher import fetch, extract_basic_fields
from processors.filler_detector import load_filler_rules, detect_fillers
from processors.trust_compliance import load_trust_rules, evaluate_trust
from processors.text_features import sentence_stats, text_html_ratio
from reports.builders import build_unified_report

def run_full_audit(urls: List[str], profile: str, enable_flags: Dict, output_dir: Path) -> Tuple[pd.DataFrame, Dict[str, pd.DataFrame]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    filler_rules = load_filler_rules("configs/filler_rules.yaml")
    trust_rules  = load_trust_rules("configs/trust_compliance.yaml")

    rows = []
    sub_reports: Dict[str, pd.DataFrame] = {}

    content_rows, trust_rows = [], []

    for url in urls:
        # --- Fetch HTML ---
        try:
            status, html = fetch(url, timeout=25)
        except Exception:
            status, html = 0, ""

        # --- Extract basic fields ---
        fields = extract_basic_fields(html) if html else {
            "h1": "", "title": "", "text": "", "text_len": 0, "html_len": 0,
            "imgs_no_alt": 0, "pub_date": "", "mod_date": ""
        }

        # --- Text stats ---
        stats = sentence_stats(fields["text"])  # word_count / avg_sent_len
        ratio = text_html_ratio(fields["text_len"], fields["html_len"])

        # --- Filler detector ---
        fillers, suggestions = ([], [])
        if enable_flags.get("filler_detector", True):
            fillers, suggestions = detect_fillers(fields["text"], filler_rules)

        # --- Trust & Compliance (stub; replace later with real DOM/JSON-LD parsing) ---
        trust_score, missing, tips = (0, [], [])
        if enable_flags.get("trust_compliance", True):
            trust_score, missing, tips = evaluate_trust(
                {
                    "author_box": False,
                    "contact": False,
                    "about": False,
                    "sources_count": 0,
                    "privacy": False,
                    "terms": False,
                },
                trust_rules
            )

        # --- Build unified row EXACTLY matching UNIFIED_COLUMNS_AR (34 columns) ---
        row = [
            url,                                     # URL
            ("200" if status == 200 else str(status)),  # حالة_الفهرسة
            fields["h1"],                          # العنوان_H1
            "",                                    # نية_البحث (placeholder)
            stats.get("word_count", 0),            # عدد_الكلمات
            ratio,                                   # نسبة_النص_إلى_HTML
            0.0,                                     # نسبة_الإعلانات_إلى_النص (placeholder)
            0,                                       # مفيدة_Helpful_درجة (placeholder)
            0,                                       # E_E_A_T_درجة (placeholder)
            "",                                    # YMYL_أعلام (placeholder)
            trust_score,                             # ثقة_Trust_درجة
            ";".join(missing),                     # امتثال_Compliance_مفقود
            "متوسط",                               # سبام_مخاطر (placeholder)
            "لا",                                   # باب_دواروِي (placeholder)
            "",                                    # مكرر_مجموعة (placeholder)
            "",                                    # كثافة_الكلمات_الرئيسية (placeholder)
            "",                                    # كلمات_رئيسية_مستهدفة (placeholder)
            "",                                    # تداخل_داخلي (placeholder)
            0,                                       # روابط_داخلية_مكسورة (placeholder)
            "لا",                                   # صفحة_يتيمة (placeholder)
            0.0,                                     # PageRank_داخلي (placeholder)
            "",                                    # LCP
            "",                                    # CLS
            "",                                    # INP
            fields["imgs_no_alt"],                 # صور_بدون_alt
            0,                                       # فيديو_Schema (placeholder)
            fields["pub_date"],                    # تاريخ_النشر
            fields["mod_date"],                    # تاريخ_التحديث
            50,                                      # حداثة_الصفحة_درجة (placeholder)
            "؛".join(fillers),                     # الجمل_الحشوية
            "؛".join(suggestions),                 # بدائل_مقترحة
            50,                                      # إشارات_التفاعل_درجة (placeholder)
            "أضف author bio + 2 مصادر + FAQ",      # توصيات_تحريرية_مختصرة
            "أعد صياغة المقدمة بإضافة تجربة مباشرة ومصادر",  # خطة_إجراء
        ]
        rows.append(row)

        # --- Sub reports ---
        content_rows.append([
            url, fields["h1"], stats.get("word_count", 0), ratio,
            fields["imgs_no_alt"], "؛".join(fillers), "؛".join(suggestions)
        ])
        trust_rows.append([url, trust_score, ";".join(missing), "؛".join(tips)])

    # Build DataFrames
    df_unified = build_unified_report(rows)
    sub_reports["content_quality"] = pd.DataFrame(content_rows, columns=[
        "URL","H1","عدد_الكلمات","نسبة_النص_إلى_HTML","صور_بدون_alt","الجمل_الحشوية","بدائل_مقترحة"
    ])
    sub_reports["trust_compliance"] = pd.DataFrame(trust_rows, columns=[
        "URL","ثقة_Trust_درجة","امتثال_مفقود","توصيات"
    ])

    # Save to disk
    df_unified.to_csv(output_dir / "unified_report_ar.csv", index=False, encoding="utf-8")
    for name, df in sub_reports.items():
        df.to_csv(output_dir / f"{name}.csv", index=False, encoding="utf-8")
    return df_unified, sub_reports
