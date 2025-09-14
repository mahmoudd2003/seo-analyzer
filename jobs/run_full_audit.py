
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
    # Load configs
    filler_rules = load_filler_rules("configs/filler_rules.yaml")
    trust_rules  = load_trust_rules("configs/trust_compliance.yaml")

    rows = []
    sub_reports = {"content_quality": None, "trust_compliance": None}
    content_rows, trust_rows = [], []

    for url in urls:
        try:
            status, html = fetch(url, timeout=25)
        except Exception as e:
            status, html = 0, ""
        fields = extract_basic_fields(html) if html else {
            "h1": "", "title": "", "text": "", "text_len": 0, "html_len": 0, "imgs_no_alt": 0, "pub_date": "", "mod_date": ""
        }
        # Content stats
        stats = sentence_stats(fields["text"])
        ratio = text_html_ratio(fields["text_len"], fields["html_len"])

        fillers, suggestions = ([], [])
        if enable_flags.get("filler_detector", True):
            fillers, suggestions = detect_fillers(fields["text"], filler_rules)

        # Trust stub (replace with DOM/JSON-LD parsing later)
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

        row = [
            url, ("200" if status==200 else str(status)), fields["h1"], "", stats["word_count"], ratio,
            0.0, 0, 0, "",
            trust_score, ";".join(missing), "متوسط", "لا", "",
            "", "", "", 0,
            "لا", 0.0, "", "",  fields["imgs_no_alt"], 0,
            fields["pub_date"], fields["mod_date"], 50, "؛".join(fillers), "؛".join(suggestions),
            50, "أضف author bio + 2 مصادر + FAQ", "أعد صياغة المقدمة بإضافة تجربة مباشرة ومصادر"
        ]
        rows.append(row)
        content_rows.append([url, fields["h1"], stats["word_count"], ratio, fields["imgs_no_alt"], "؛".join(fillers), "؛".join(suggestions)])
        trust_rows.append([url, trust_score, ";".join(missing), "؛".join(tips)])

    df_unified = build_unified_report(rows)
    sub_reports["content_quality"] = pd.DataFrame(content_rows, columns=[
        "URL","H1","عدد_الكلمات","نسبة_النص_إلى_HTML","صور_بدون_alt","الجمل_الحشوية","بدائل_مقترحة"
    ])
    sub_reports["trust_compliance"] = pd.DataFrame(trust_rows, columns=["URL","ثقة_Trust_درجة","امتثال_مفقود","توصيات"])

    # Save
    df_unified.to_csv(output_dir / "unified_report_ar.csv", index=False, encoding="utf-8")
    for name, df in sub_reports.items():
        if df is not None:
            df.to_csv(output_dir / f"{name}.csv", index=False, encoding="utf-8")
    return df_unified, sub_reports
