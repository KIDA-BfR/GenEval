import pandas as pd
import re
from difflib import SequenceMatcher
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from openpyxl import load_workbook

class ColumnProcessor:
    def process(self, value):
        raise NotImplementedError("Subclasses should implement this!")

    def compare(self, val1, val2):
        raise NotImplementedError("Subclasses should implement this!")
       

class StringColumnNoisyProcessor(ColumnProcessor):
    def process(self, value):
        if pd.isna(value) or value == "N/A":
            return ""
        return str(value).replace(" ", "").replace(".", "").replace(",", "").lower()

    def compare(self, val1, val2):
        if val1 == "" and val2 != "":
            return "False Positive"
        elif val1 != "" and val2 == "":
            return "False Negative"
        similarity = SequenceMatcher(None, val1, val2).ratio()
        return "Correct" if similarity > 0.75 else "Incorrect"

    def highlight_differences(self, val1, val2):
        matcher = SequenceMatcher(None, val1, val2)
        highlighted_val2 = []
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'equal':
                highlighted_val2.append(val2[j1:j2])
            elif tag == 'replace' or tag == 'delete' or tag == 'insert':
                highlighted_val2.append(f"[{val2[j1:j2]}]")
        return ''.join(highlighted_val2)