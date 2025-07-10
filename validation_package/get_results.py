import pandas as pd
import os
from IPython.display import display 

def results(table_truth, table_compared, comparison_results, confusion_matrices, display_results = False):
    combined_output = pd.DataFrame()
    columns = table_truth.columns

    # Combine outputs and comparisons
    for column in columns:
        combined_output[f'{column}_truth'] = table_truth[column]
        combined_output[f'{column}_compared'] = table_compared[column]
        combined_output[f'{column}_comparison'] = comparison_results[column]

    # Calculate accuracy for each column in the confusion matrices
    for column, matrix in confusion_matrices.items():
        C = matrix["Correct"]
        FP = matrix["False Positive"]
        FN = matrix["False Negative"]
        N = matrix["Incorrect"]

        accuracy = C / (C + FP + FN + N) if (C + FP + FN + N) > 0 else 0

        # Store only the accuracy in the matrix
        matrix.update({
            "Accuracy": accuracy
        })

    # Fill confusion matrix
    overall_metrics = {"Correct": 0, "Incorrect": 0, "False Positive": 0, "False Negative": 0}

    # Sum all the confusion matrix values to get overall metrics
    for column, matrix in confusion_matrices.items():
        if column == "Overall":
            continue  # Skip if already calculated
        overall_metrics["Correct"] += matrix["Correct"]
        overall_metrics["Incorrect"] += matrix["Incorrect"]
        overall_metrics["False Positive"] += matrix["False Positive"]
        overall_metrics["False Negative"] += matrix["False Negative"]

    # Calculate the overall accuracy
    C = overall_metrics["Correct"] # Can be further splitted to True Positive, True Negative as well
    # omitted for the current applications.
    FP = overall_metrics["False Positive"]
    FN = overall_metrics["False Negative"]
    N = overall_metrics["Incorrect"]

    overall_accuracy = C / (C + FP + FN + N) if (C + FP + FN + N) > 0 else 0

    # Store the overall metrics in the matrix
    overall_metrics.update({"Accuracy": overall_accuracy})
    confusion_matrices["Overall"] = overall_metrics

    # Convert confusion matrices to DataFrame
    confusion_matrices_df = pd.DataFrame(confusion_matrices).T

    # Reset index to make the index a column
    confusion_matrices_df.reset_index(inplace=True)
    confusion_matrices_df.rename(columns={'index': 'Column'}, inplace=True)

    # Display results if display_results is True
    if display_results:
        with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.width', None, 'display.max_colwidth', None):
            display(combined_output)
            display(confusion_matrices_df)

    # Saving results in an .xlsx file
    notebook_dir = os.getcwd()
    comparison_results_file_path = os.path.join(notebook_dir, 'comparison.results.xlsx')
    combined_output.to_excel(comparison_results_file_path, index = False)
    confusion_matrices_file_path = os.path.join(notebook_dir, 'confusion_matrices.xlsx')
    confusion_matrices_df.to_excel(confusion_matrices_file_path, index = False)

    print(f"results are saved to {comparison_results_file_path}.")
    return combined_output, confusion_matrices_df