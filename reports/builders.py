
import pandas as pd
from reports.schemas import UNIFIED_COLUMNS_AR

def build_unified_report(rows):
    df = pd.DataFrame(rows, columns=UNIFIED_COLUMNS_AR)
    return df

def build_sub_report(name: str, rows, columns):
    return pd.DataFrame(rows, columns=columns)
