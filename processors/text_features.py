
import re
from typing import Dict

def sentence_stats(text: str) -> Dict[str, float]:
    sents = re.split(r"[.!؟\n]+", text or "")
    sents = [s.strip() for s in sents if s.strip()]
    if not sents:
        return {"sent_count": 0, "avg_sent_len": 0.0, "word_count": 0}
    words = sum(len(s.split()) for s in sents)
    return {
        "sent_count": len(sents),
        "avg_sent_len": round(words / max(1,len(sents)), 2),
        "word_count": words
    }

def text_html_ratio(text_len: int, html_len: int) -> float:
    if html_len <= 0:
        return 0.0
    return round(text_len / html_len, 3)
