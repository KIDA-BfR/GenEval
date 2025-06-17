import pandas as pd
from pathlib import Path

# Load the excel file containing two files to tables to compare, tables should
# contain the same columns

def dataframe_impl():
    # Testing for CARC
    file_truth_path = '/content/CARC_Truth.xlsx'
    file_compared_path = '/content/CARC_LLM.xlsx'

    filename_truth = Path(file_truth_path).stem
    filename_compared = Path(file_compared_path).stem

    # Load files
    table_truth = pd.read_excel(file_truth_path)
    table_compared = pd.read_excel(file_compared_path)
    