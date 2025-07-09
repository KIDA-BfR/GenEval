import pandas as pd
from pathlib import Path
from IPython.display import display

# Load the excel file containing two files to tables to compare, tables should
# contain the same columns

def reading_tables(path_truth, path_compared, display_tables = False):
    # Load files
    table_truth = pd.read_excel(path_truth)
    table_compared = pd.read_excel(path_compared)

    # Display loaded tables if display_tables is True
    if display_tables:
        with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.width', None, 'display.max_colwidth', None):
            display(table_truth)
            display(table_compared)
    
    print("Tables are loaded") 
    return table_truth, table_compared
