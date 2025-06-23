# Strip any leading or trailing whitespace from all column names
# Sorting the data to normalize the comparison
def sort_data(table_truth, table_compared):
    table_truth.columns = table_truth.columns.str.strip()
    table_truth = table_truth.sort_values(by=table_truth.columns[0]).reset_index(drop=True)

    table_compared.columns = table_compared.columns.str.strip()
    table_compared = table_compared.sort_values(by=table_compared.columns[0]).reset_index(drop=True)
