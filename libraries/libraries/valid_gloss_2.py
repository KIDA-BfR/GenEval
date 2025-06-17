# Specifying the glossary/picklist
# For this particular Study type was transformed to match OECD guidelines
# Different variations of Data owner are used  as well

# Glossary for Muta and CARC
glossary = {
    "Study Type": {
        "Bacterial Reverse Mutation Test (Ames Test)": "Ames Test", # Muta glossary

         # CARC glossary
        "OECD 453": "Combined chronic toxicity/ carcinogenicity",
        "OECD 451": "Carcinogenicity",
        "OECD 452": "Chronic toxicity",
        "US-EPA 83-5": "Combined chronic toxicity/ carcinogenicity"
    },
    "Data Owner": {
        "Arysta": "Arysta Life Sciences",
        "Helm": "HAG",
        "Helm AG": "HAG",
        "Albaugh":"Albaugh Europe Sàrl"
    },
}

# Strip any leading or trailing whitespace from all column names
# Sorting the data to normalize the comparison
def sort_data():
    table_truth.columns = table_truth.columns.str.strip()
    table_truth = table_truth.sort_values(by=table_truth.columns[0]).reset_index(drop=True)

    table_compared.columns = table_compared.columns.str.strip()
    table_compared = table_compared.sort_values(by=table_compared.columns[0]).reset_index(drop=True)

    # Applying the glossary to a specific column ""
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