# Strip any leading or trailing whitespace from all column names
# Sorting the data to normalize the comparison
# Adding a glossary for the user to add some equivalent terms
def sort_data(table_truth, table_compared):
    table_truth.columns = table_truth.columns.str.strip()
    table_truth = table_truth.sort_values(by=table_truth.columns[0]).reset_index(drop=True)

    table_compared.columns = table_compared.columns.str.strip()
    table_compared = table_compared.sort_values(by=table_compared.columns[0]).reset_index(drop=True)

    # Creating a glossary to specify if different terms have the same meaning
    glossary = {
        "String": {
            "DFGE" : "DeFeEeGe"
        },
    }
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