
from typing import List
import pandas as pd

def load_urls_from_file(path: str) -> List[str]:
    if path.lower().endswith(".txt"):
        with open(path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    df = pd.read_csv(path)
    col = "URL" if "URL" in df.columns else df.columns[0]
    return df[col].dropna().astype(str).tolist()
