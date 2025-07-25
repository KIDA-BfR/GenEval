# Strip any leading or trailing whitespace from all column names
# Sorting the data to normalize the comparison
# Adding a glossary for the user to add some equivalent terms
def sort_data(table_truth, table_compared, glossary=None):
    # Default glossary if none provided
    if glossary is None:
        glossary = {}
    
    # Read the spreadsheets
    table1 = table_truth
    table2 = table_compared

    # Using col names of table1 for table 2; Attention: make sure order is the same!
    table2.columns = table1.columns

    # Strip any leading or trailing whitespace from all column names
    table1.columns = table1.columns.str.strip()
    table2.columns = table2.columns.str.strip()


    # Applying the glossary to a specific column
    tables = [("truth", table_truth), ("compared", table_compared)]
    for name, df in tables:
        missing_columns = []
        applied_columns = []

        for column, replacements in glossary.items():
            if column in df.columns:
                df[column] = df[column].replace(replacements)
                applied_columns.append(column)
            else:
                missing_columns.append(column)

    # Reporting the glossaries application results
        if missing_columns:
            print(f"Table {name}: The following glossary columns were not found in the DataFrame: {missing_columns}")
        if applied_columns:
            print(f"Table {name}: Glossary was applied to {applied_columns}")
            
    return table_truth, table_compared