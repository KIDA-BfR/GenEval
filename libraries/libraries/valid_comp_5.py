import pandas as pd

def comparison_storage(table_truth, table_compared, processors):
    # Create an empty DataFrame to store the comparison results
    columns = table_truth.columns
    comparison_results = pd.DataFrame(columns=columns)

    # Initialize confusion matrices
    confusion_matrices = {col: {"Correct": 0, "Incorrect": 0, "False Positive": 0, "False Negative": 0} for col in columns}

    # Process and compare the data
    for column in columns:
        processor = processors[column]
        processed_table1 = table_truth[column].apply(processor.process)
        processed_table2 = table_compared[column].apply(processor.process)
        comparison_results[column] = [
            processor.compare(val1, val2) for val1, val2 in zip(processed_table1, processed_table2)
        ]

        # Update confusion matrices
        for result in comparison_results[column]:
            confusion_matrices[column][result] += 1
    return comparison_results, confusion_matrices