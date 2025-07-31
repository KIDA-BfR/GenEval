import pandas as pd

def comparison_init(table_truth, table_compared, processors, ignore_columns=None):
    if ignore_columns is None:
        ignore_columns = []

    # Filter out the columns to ignore from both tables
    columns = [col for col in table_truth.columns if col not in ignore_columns]
    table_truth_filtered = table_truth[columns]
    table_compared_filtered = table_compared[columns]

    # Create an empty DataFrame to store the comparison results
    comparison_results = pd.DataFrame(columns=columns)

    # Initialize confusion matrices
    confusion_matrices = {col: {"Correct": 0, "Incorrect": 0, "False Positive": 0, "False Negative": 0} for col in columns}

    # Process and compare the data
    for column in columns:
        processor = processors[column]
        processed_table1 = table_truth_filtered[column].apply(processor.process)
        processed_table2 = table_compared_filtered[column].apply(processor.process)
        comparison_results[column] = [
            processor.compare(val1, val2) for val1, val2 in zip(processed_table1, processed_table2)
        ]

        # Update confusion matrices
        for result in comparison_results[column]:
            confusion_matrices[column][result] += 1
    return comparison_results, confusion_matrices