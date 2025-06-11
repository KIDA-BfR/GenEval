import pandas as pd
from difflib import SequenceMatcher

class ColumnProcessor:
    def process(self, value):
        raise NotImplementedError("Subclasses should implement this!")

    def compare(self, val1, val2):
        raise NotImplementedError("Subclasses should implement this!")


class StringColumnProcessor(ColumnProcessor):
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
        return "Correct" if similarity == 1 else "Incorrect"