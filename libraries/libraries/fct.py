import pandas as pd

def process(value):
        if pd.isna(value) or value == "N/A":
            return ""
        return str(value).replace(" ", "").replace(".", "").replace(",", "").lower()