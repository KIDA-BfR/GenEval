import pandas as pd
from pathlib import Path

# Load the excel file containing two files to tables to compare, tables should
# contain the same columns

def dataframe_impl(path_truth, path_compared):
    # Testing for CARC
    file_truth_path = path_truth
    file_compared_path = path_compared

    filename_truth = Path(file_truth_path).stem
    filename_compared = Path(file_compared_path).stem

    # Load files
    table_truth = pd.read_excel(file_truth_path)
    table_compared = pd.read_excel(file_compared_path)
    
    return table_truth, table_compared
