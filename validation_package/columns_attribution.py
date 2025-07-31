import json
import pandas as pd
from collections import defaultdict
from validation_package.classes import (
    StringColumnProcessor, StringNoisyColumnProcessor, NumericColumnProcessor,
    BooleanListColumnProcessor, KeywordListColumnProcessor, 
    ListColumnProcessor, OrderedListColumnProcessor, List_of_Strings_ColumnProcessor,
    LLMColumnProcessor
)

# Have the choice of 2 functions :
# The first one is better-suited for smaller tables.
# You input a .txt file (the attribution argument) in which you already made the choice of which processing method 
# for each column by writing a list. The list is only the abbreviation of the processing method, reminded when 
# you run the function, in the same order as the columns and coma-separated.
# Time-consuming but best if you already know you don't want the default values.

# The second one is better-suited for bigger tables.
# The code automatically choose a processing method for each column, depending on the type of content inside.
# There are default choices, but you can modify it and choose a more suitable processing method via the JSON file 
# that you get in the end. Run it in the next function to apply the modifications, after manually editing the JSON file.

def manual_process_for_columns_attribution(table_truth, attribution_txt_file_path, ignore_column_txt_file_path):
    # Choosing the processing method for each column
    print("What type of processing for each column ?")
    print("Write a txt file via choosing from this table: ")
    print("Processing methods ")
    print("-"*19)
    print("words - StringColumnProcessor()")
    print("words_not_exact - StringNoisyColumnProcessor()")
    print("num - NumericColumnProcessor()")
    print("choice - BooleanListColumnProcessor()")
    print("keyword - KeywordListColumnProcessor()")
    print("list_num - ListColumnProcessor()")
    print("list_num_order - OrderedListColumnProcessor()")
    print("list_words - List_of_Strings_ColumnProcessor()")
    print("sentence - LLMColumnProcessor()")

    # Extract column names from the table
    columns_list = table_truth.columns.str.strip().tolist()
    print(columns_list)

    # Read the list of columns to ignore from the ignore text file
    with open(ignore_column_txt_file_path, 'r') as ignore_file:
        ignore_content = ignore_file.read()
        ignore_columns = [col.strip() for col in ignore_content.split(',')]

    # Filter out the columns to ignore
    columns_to_process = [col for col in columns_list if col not in ignore_columns]

    # Read the list from the .txt file
    with open(attribution_txt_file_path, 'r') as file:
        file_content = file.read()
        process_list = [value.strip() for value in file_content.split(',')]

    # Check if both lists are the same length
    if len(columns_to_process) != len(process_list):
        return "Error: The number of columns and the number of processing methods do not match."

    # Check if values from the attribution.txt file are in the accepted values list
    process_values = ['words', 'words_not_exact', 'num', 'choice', 'keyword', 'list_num', 'list_num_order', 'list_words', 'sentence']
    for value in process_list:
        if value not in process_values:
            return "Invalid choice of processing method. Check the spelling."
        
    # Mapping from accepted text values to processing method class names
    processing_mapping = {
        'words': StringColumnProcessor,
        'words_not_exact': StringNoisyColumnProcessor,
        'num': NumericColumnProcessor,
        'choice': BooleanListColumnProcessor,
        'keyword': KeywordListColumnProcessor,
        'list_num': ListColumnProcessor,
        'list_num_order': OrderedListColumnProcessor,
        'list_words': List_of_Strings_ColumnProcessor,
        'sentence': LLMColumnProcessor
    }
    # Replace text values with actual processing method class names
    real_process_list = [processing_mapping[value]() for value in process_list]
    print(real_process_list)

    # Create a dictionary combining the columns to process and their processors
    processors = dict(zip(columns_to_process, real_process_list))

    # Print the columns that have been ignored
    for col in ignore_columns:
        print(f"Column '{col}' has been ignored for the validation.")

    print("The manual attribution was taken into account.")
    return processors 


def automatic_process_for_columns_attribution(table_truth):
    # Sample data types and assign processing methods
    processors = {}
    sample_size = 5
    columns = table_truth.columns
    for column in columns:
        sample = table_truth[column].dropna().sample(min(sample_size, len(table_truth[column])), replace=True)
        types_in_column = set()

        for item in sample:
            # Check if the item is a string that can be split into multiple parts
            if isinstance(item, str) and ',' in item:
                # Split the string by commas and strip whitespace
                parts = [part.strip() for part in item.split(',')]

                # Determine the type of each part
                part_types = set()
                for part in parts:
                    if part.isdigit():
                        part_types.add(int)
                    elif part.replace('.', '', 1).isdigit():  # Check for float
                        part_types.add(float)
                    else:
                        part_types.add(str)

                # Determine the overall type of the list
                if part_types: # Check if not empty
                    if len(part_types) == 1:
                        part_type = part_types.pop()
                        if part_type in (int, float):
                            types_in_column.add(list[int])
                        elif part_type is str:
                            types_in_column.add(list[str])
                    else:
                        types_in_column.add(list)
            else:
                types_in_column.add(type(item))

        # Assign processor based on detected types
        if any(typ in (int, float) for typ in types_in_column):
            processors[column] = NumericColumnProcessor()
        elif any(typ is str for typ in types_in_column):
            processors[column] = StringColumnProcessor()
        elif any(typ is bool for typ in types_in_column):
             processors[column] = BooleanListColumnProcessor()
        elif any(typ is list[int] for typ in types_in_column):
            processors[column] = ListColumnProcessor()
        elif any(typ is list[str] for typ in types_in_column):
            processors[column] = List_of_Strings_ColumnProcessor()
        else:
            processors[column] = StringColumnProcessor()

    # Save processors to a JSON file
    processors_dict = {col: str(processor) for col, processor in processors.items()}
    with open('attribution.json', 'w') as json_file:
        json.dump(processors_dict, json_file, indent=4)  
    return "The JSON file holding the attribution has been saved on your end."


def modify_attribution(attribution):
    global processors
    with open(attribution, 'r') as json_file:
        processors = json.load(json_file)
    for key, value in processors.items():
        print(f"{key} : {value}")
    return "The attribution has been edited."
