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


class ListColumnProcessor(ColumnProcessor):
    def process(self, value):
        # 1) Handle blanks/N/A as an empty list
        if pd.isna(value) or str(value).strip().upper() == "N/A":
            return []
        # 2) Split on commas into items
        raw = str(value)
        items = []
        for part in raw.split(','):
            # strip whitespace and surrounding punctuation, lowercase
            clean = part.strip().lower().strip(" .;:()[]{}\"'")
            if clean:
                items.append(clean)
        return items

    def compare(self, truth_list, comp_list):
        # 1) both empty → Correct
        if not truth_list and not comp_list:
            return "Correct"
        # 2) truth empty vs comp nonempty → FP
        if not truth_list and comp_list:
            return "False Positive"
        # 3) truth nonempty vs comp empty → FN
        if truth_list and not comp_list:
            return "False Negative"
        # 4) both nonempty → set logic
        truth_set = set(truth_list)
        comp_set  = set(comp_list)
        missing = truth_set - comp_set
        extra   = comp_set - truth_set

        if not missing and not extra:
            return "Correct"
        if extra and not missing:
            return "False Positive"
        if missing and not extra:
            return "False Negative"
        return "Incorrect"


class BooleanListColumnProcessor(ColumnProcessor):
    def process(self, value):
        # Normalize missing
        if pd.isna(value) or str(value).strip().upper() == "N/A":
            return []
        raw = str(value)
        # Split on standalone “OR”
        parts = re.split(r'\bOR\b', raw, flags=re.IGNORECASE)
        alternatives = []
        for part in parts:
            # Now split on commas into a list of strings
            items = [item.strip().lower() 
                     for item in part.split(',') 
                     if item.strip()]
            alternatives.append(items)
        # If only one alternative, just return that list
        if len(alternatives) == 1:
            return alternatives[0]
        # Otherwise, return list-of-alternative-lists
        return alternatives

    def compare(self, truth_list, comp_list):
        # Handle empty‐vs‐nonempty
        if not truth_list and comp_list:
            return "False Positive"
        if truth_list and not comp_list:
            return "False Negative"
        if not truth_list and not comp_list:
            return "Correct"

        # If truth_list is a list of alternatives
        if (isinstance(truth_list, list) and truth_list and
            isinstance(truth_list[0], list)):
            # Try each alternative in turn
            for alt in truth_list:
                result = self._compare_single(alt, comp_list)
                if result == "Correct":
                    return "Correct"
                # Otherwise keep track of FP/FN if they occur
                if result in ("False Positive", "False Negative"):
                    last_fp_fn = result
            return last_fp_fn if 'last_fp_fn' in locals() else "Incorrect"

        # Otherwise it's a single list -> compare directly
        return self._compare_single(truth_list, comp_list)

    def _compare_single(self, truth_items, comp_items):
        truth_set = set(truth_items)
        comp_set  = set(comp_items)
        missing = truth_set - comp_set
        extra   = comp_set - truth_set

        if not missing and not extra:
            return "Correct"
        if extra and not missing:
            return "False Positive"
        if missing and not extra:
            return "False Negative"
        return "Incorrect"


class KeywordListColumnProcessor(ColumnProcessor):
    def process(self, value):
        # Treat blanks/N/A as “no keywords”
        if pd.isna(value) or str(value).strip().upper() == "N/A":
            return []
        raw = str(value)
        # Split on commas into candidate keywords
        parts = [part.strip() for part in raw.split(",")]
        keywords = []
        for part in parts:
            # Remove everything except letters+digits, lowercase
            clean = re.sub(r'[^A-Za-z0-9]', '', part).lower()
            if clean:
                keywords.append(clean)
        return keywords

    def compare(self, truth_keywords, comp_keywords):
        # Edge cases: empty vs non-empty
        if not truth_keywords and comp_keywords:
            return "False Positive"
        if truth_keywords and not comp_keywords:
            return "False Negative"
        if not truth_keywords and not comp_keywords:
            return "Correct"

        # Check that every truth‐keyword appears in *some* comp string
        missing = [
            kw for kw in truth_keywords
            if not any(kw in comp for comp in comp_keywords)
        ]
        return "Correct" if not missing else "False Negative"


class OrderedListColumnProcessor(ListColumnProcessor):
    def compare(self, truth_list, comparison_list):
        if truth_list == "" and comparison_list != "":
            return "False Positive"
        elif truth_list != "" and comparison_list == "":
            return "False Negative"
        if not truth_list or not comparison_list:
            return "Incorrect"

        # Convert the lists to sets to compare their contents
        truth_set = set(truth_list)
        comparison_set = set(comparison_list)

        # Check for missing elements in the second list (False Negative)
        missing_elements = truth_set - comparison_set

        # Check for extra elements in the second list (False Positive)
        extra_elements = comparison_set - truth_set

        # If both missing and extra elements exist, treat it as Incorrect
        if missing_elements and extra_elements:
            return "Incorrect"

        # If there are only extra elements in the second list (False Positive)
        if extra_elements:
            return "False Positive"

        # If there are only missing elements in the second list (False Negative)
        if missing_elements:
            return "False Negative"

        # Check if the lists have the same elements but in the wrong order (Incorrect)
        if truth_list != comparison_list:
            return "Incorrect"

        # If both lists are exactly the same in content and order, return Correct
        return "Correct"


class NumericColumnProcessor(ColumnProcessor):
    def process(self,value):
        if pd.isna(value) or value == "N/A":
            return ""

        # Use regular expressions to find numeric parts in the string
        match = re.search(r"\d+(\.\d+)?", str(value))

        if match:
            # Convert the matched number to float and round to one decimal place
            number = round(float(match.group()), 1)

            # Return the number as a string with one decimal place
            return str(number)

        # Return empty string if no numeric part is found
        return ""

    def compare(self, val1, val2):
        if val1 == "" and val2 != "":
            return "False Positive"
        elif val1 != "" and val2 == "":
            return "False Negative"
        elif val1 == "" and val2 == "":
            return "Correct"
        elif val1 != "" and val2 != "":
       #similarity = SequenceMatcher(None, val1, val2).ratio() # can try other metrics later on
          num1=float(val1)
          num2=float(val2)
          if num1 == num2:
            return "Correct"
          else:
            return "Incorrect"