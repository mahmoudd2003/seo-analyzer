
import re
import yaml
from typing import Dict, List

def load_filler_rules(path: str) -> Dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def detect_fillers(text: str, rules: Dict) -> (List[str], List[str]):
    text_norm = re.sub(r"\s+", " ", text or "").strip()
    found = []
    suggestions = []
    for entry in rules.get("filler_phrases", []):
        pattern = entry.get("pattern")
        repls = entry.get("replacements", [])
        if not pattern:
            continue
        for m in re.finditer(pattern, text_norm):
            span = m.group(0)
            found.append(span)
            if repls:
                suggestions.append(repls[0])
    return list(dict.fromkeys(found)), suggestions[:3]
