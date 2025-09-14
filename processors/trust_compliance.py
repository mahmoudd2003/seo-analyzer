
import yaml
from typing import Dict, List

def load_trust_rules(path: str) -> Dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def evaluate_trust(sample_fields: Dict, rules: Dict) -> (int, List[str], List[str]):
    # Stub: evaluate presence of keys (in real system, parse DOM/json-ld)
    missing = []
    tips = []
    score = 0
    # Publisher identity
    pub = rules.get("publisher_identity", {})
    if pub.get("author_box") == "required" and not sample_fields.get("author_box"):
        missing.append("author_box")
        tips.append("أضف صندوق المؤلف مع نبذة واضحة.")
    else:
        score += 10
    if pub.get("contact_page") == "required" and not sample_fields.get("contact"):
        missing.append("contact_page")
        tips.append("أضف صفحة تواصل وأدرجها في الفوتر.")
    else:
        score += 10
    if pub.get("about_page") == "required" and not sample_fields.get("about"):
        missing.append("about_page")
        tips.append("أضف صفحة من نحن مع فريق التحرير.")
    else:
        score += 10
    # Citations
    cit = rules.get("citations", {})
    min_src = cit.get("min_sources_per_article", 2)
    if sample_fields.get("sources_count", 0) >= min_src:
        score += 10
    else:
        missing.append("sources")
        tips.append(f"أضف على الأقل {min_src} مصادر موثوقة.")
    # Policies
    pol = rules.get("policies", {})
    if pol.get("privacy_policy") == "required" and not sample_fields.get("privacy"):
        missing.append("privacy_policy")
        tips.append("أضف سياسة خصوصية واضحة.")
    else:
        score += 10
    if pol.get("terms_of_use") == "required" and not sample_fields.get("terms"):
        missing.append("terms_of_use")
        tips.append("أضف اتفاقية استخدام.")
    else:
        score += 10

    # Normalize to 0-100 (simple stub)
    score = min(100, score * 2)
    return score, missing, tips
