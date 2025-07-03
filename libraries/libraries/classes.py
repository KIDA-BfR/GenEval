import pandas as pd 
import re
from difflib import SequenceMatcher

class ColumnProcessor: # Head class specifying the structure for subclasses
    def process(self, value): # Class-specific method for the preprocessing
        raise NotImplementedError("Subclasses should implement this!")

    def compare(self, val1, val2): # Class-specific method for the comparison
        raise NotImplementedError("Subclasses should implement this!")

class NumericColumnProcessor(ColumnProcessor):
    def process(self, value):
        if pd.isna(value) or value == "N/A" or value =="":
          # if an input is an empty string we directly return it
            return ""
        try:
            # Round the numeric value to the first digit after the comma
            value = round((float(value)), 2)
        except ValueError as e:
            print(f"Error converting val1 ('{value}') to float: {e}")
        return value

    def compare(self, val1, val2):
        if val1 == "" and val2 != "":
            return "False Positive"
        elif val1 != "" and val2 == "":
            return "False Negative"
        elif val1 == "" and val2 == "":
            return "Correct"
        if val1 == val2:
          return "Correct"
        else:
          return "Incorrect"


class StringColumnProcessor(ColumnProcessor):
    def __init__(self):
        self.numeric_processor = NumericColumnProcessor()

    def process(self, value):
        if pd.isna(value) or value == "N/A" or value == "":
            return ""
            # Preprocessing of a string
            # Remove brackets and percentage signs
            # Remove all whitespace characters
            # Lower the
        value_str = str(value).strip().lower()
        value_str = re.sub(r"[()\[\]{}%]", "", value_str)
        value_str = re.sub(r"\s", "", value_str)
        try:
            # Attempt to convert to float to check if it's numeric
            # If successful, delegate processing to NumericColumnProcessor
            result=self.numeric_processor.process(float(value_str))
            return result

        except  ValueError:  # if the conversion fails, then the provided string is not
        # a solid number, thus, we are  processing with a string pre-processing
            return value_str

    def compare(self, val1, val2):
        if val1 == "" and val2 != "":
            return "False Positive"
        elif val1 != "" and val2 == "":
            return "False Negative"
        elif val1 == "" and val2 == "":
            return "Correct"
        try:
            return self.numeric_processor.compare(val1, val2) # try to compare values
        except ValueError:
            # If the value comparison fails, then proceed with a string comparison
            similarity = SequenceMatcher(None, val1, val2).ratio()
            return "Correct" if similarity == 1 else "Incorrect"


class StringNoisyColumnProcessor(StringColumnProcessor): # inherits the same preprocessing as for strict strings
    def compare(self, val1, val2):
        if val1 == "" and val2 != "":
            return "False Positive"
        elif val1 != "" and val2 == "":
            return "False Negative"
        elif val1 == "" and val2 == "":
            return "Correct"
        similarity = SequenceMatcher(None, val1, val2).ratio()
        return "Correct" if similarity > 0.75 else "Incorrect"


class List_of_Numbers_ColumnProcessor(ColumnProcessor):
    def process(self, value):
        if pd.isna(value) or value == "N/A" or value == "":
            return ""
        try:
            # Attempt to convert the value directly to float
            return [float(value)]
        except (ValueError, TypeError):
            pass  # Not a standalone number; proceed to extract numbers

        try:
            # Extract integers and decimals, then convert to float
            # Splitting can be commas, semicolons, spaces, etc. the pre-processing
            # does not depend on it directly

            numbers = re.findall(r'\d+(?:\.\d+)?', value)
            extracted_list = [float(num) for num in numbers]
        except ValueError as e:
            print(f"Error converting val1 ('{value}') to the list of numbers: {e}")
        return extracted_list

    def compare(self, truth_list, comparison_list):
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
        if extra_elements and not missing_elements:
            return "False Positive"

        # If there are only missing elements in the second list (False Negative)
        if missing_elements and not extra_elements:
            return "False Negative"

        # If both sets are exactly the same (order is ignored), return Correct
        return "Correct"

class Ordered_List_of_Numbers_ColumnProcessor(List_of_Numbers_ColumnProcessor):
  # Here we inherit the pre-processing logic from List_of_Numbers_ColumnProcessor
    def compare(self, truth_list, comparison_list):
        truth_set = set(truth_list)
        comparison_set = set(comparison_list)

        missing_elements = truth_set - comparison_set
        extra_elements = comparison_set - truth_set

        # If there are only extra elements in the second list (False Positive)
        if extra_elements and not missing_elements:
            return "False Positive"

        # If there are only missing elements in the second list (False Negative)
        if missing_elements and not extra_elements:
            return "False Negative"

        # If the lists do not match exactly (including the order) the return incorrect
        if truth_list != comparison_list:
            return "Incorrect"

        # If both lists are exactly the same in content and order, return Correct
        return "Correct"


class List_of_Strings_ColumnProcessor(List_of_Numbers_ColumnProcessor):
    # Inherits compare from List_of_Numbers_ColumnProcessor
    # Uses instances of StringColumnProcessor
    def __init__(self):
        self.string_processor = StringColumnProcessor()

    def process(self, value):
        if pd.isna(value) or value == "N/A" or value =='':
            return ""
        try:
            raw_parts = re.split(r"[,;]+", str(value))
            # We apply the inherited process method to each string
            extracted_list = [self.string_processor.process(part) for part in raw_parts if part.strip()]
        except ValueError as e:
            print(f"Error converting input ('{value}') to the list of strings: {e}")
        return extracted_list
