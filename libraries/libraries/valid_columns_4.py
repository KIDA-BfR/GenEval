import json
import pandas as pd
from collections import defaultdict
from libraries.valid_class_3 import NumericColumnProcessor, StringColumnProcessor, StringNoisyColumnProcessor, List_of_Numbers_ColumnProcessor, Ordered_List_of_Numbers_ColumnProcessor, List_of_Strings_ColumnProcessor

# Have the choice of 2 functions 
# The first one is better-suited for smaller tables
# You input a .txt file (the attribution argument) in which you already made the choice of which processing method 
# for each column by writing a list. The list is only the abbreviation of the processing method, reminded when 
# you run the function, in the same order as the columns, coma-separated and put into square bracket at beginning and end.
# Time-consuming but best if you already know you don't want the default values.

# The second one is better-suited for bigger tables
# The code automatically choose a processing method for each column, depending on the type of content inside
# There are default choices, but you can modify it and choose a more suitable processing method via the JSON file 
# that you get in the end. Run it in the next function to apply the modifications, after manually editing the JSON file.

def manual_process_for_columns_attribution(table_truth, attribution_txt_file_path):
    # Choosing the processing method for each column
    print("What type of processing for each column ?")
    print("Write a txt file via choosing from this table: ")
    print("Processing methods ")
    print("-"*19)
    print("num - NumericColumnProcessor()")
    print("words - StringColumnProcessor()")
    print("words_not_exact - StringNoisyColumnProcessor()")
    print("list_num - List_of_Numbers_ColumnProcessor()")
    print("ordered_list_num - Ordered_List_of_Numbers_ColumnProcessor()")
    print("list_words - List_of_Strings_ColumnProcessor()")

    # Extract column names from the table
    columns_list = table_truth.columns.str.strip().tolist()
    print(columns_list)

    # Read the list from the .txt file
    with open(attribution_txt_file_path, 'r') as file:
        file_content = file.read()
        process_list = [value.strip() for value in file_content.split(',')]

    # Check if both lists are the same length
    if len(columns_list) != len(process_list):
        return "Error: The number of columns and the number of processing methods do not match."

    # Check if values from the attribution.txt file are in the accepted values list
    process_values = ['num', 'words', 'words_not_exact', 'list_num', 'ordered_list_num', 'list_words']
    for value in process_list:
        if value not in process_values:
            return "Invalid choice of processing method. Check the spelling."
        
    # Mapping from accepted text values to processing method class names
    processing_mapping = {
        'num': NumericColumnProcessor,
        'words': StringColumnProcessor,
        'words_not_exact': StringNoisyColumnProcessor,
        'list_num': List_of_Numbers_ColumnProcessor,
        'ordered_list_num': Ordered_List_of_Numbers_ColumnProcessor,
        'list_words': List_of_Strings_ColumnProcessor
    }
    # Replace text values with actual processing method class names
    real_process_list = [processing_mapping[value].__name__ for value in process_list]
    print(real_process_list)

    # Create a dictionary combining the two lists
    processors = dict(zip(columns_list, real_process_list))
    return "The manual attribution was taken into account."


def automatic_process_for_columns_attribution(table_truth):
    # Sample data types and assign processing methods
    processors = {}
    sample_size = 5
    columns = table_truth.columns
    for column in columns:
        sample = table_truth[column].dropna().sample(min(sample_size, len(table_truth[column])), replace=True)
        types_in_column = set()

        for item in sample:
            if isinstance(item, list):
                if len(item) > 0:
                    # Check the type of the first element in the list
                    first_element_type = type(item[0])
                    if all(isinstance(x, (int, float)) for x in item):
                        types_in_column.add(list[int])
                    elif all(isinstance(x, str) for x in item):
                        types_in_column.add(list[str])
                    else:
                        types_in_column.add(list)
                else:
                    types_in_column.add(list)
            else:
                types_in_column.add(type(item))

        if any(typ in (int, float) for typ in types_in_column):
            processors[column] = NumericColumnProcessor()
        elif any(typ is str for typ in types_in_column):
            processors[column] = StringColumnProcessor()
        # elif any(typ is bool for typ in types_in_column):
        #     processors[column] = BooleanProcessor()
        # elif any(typ is pd.Timestamp for typ in types_in_column):
        #     processors[column] = DateTimeProcessor()
        elif any(typ is list[int] for typ in types_in_column):
            processors[column] = List_of_Numbers_ColumnProcessor()
        elif any(typ is list[str] for typ in types_in_column):
            processors[column] = List_of_Strings_ColumnProcessor()

    # Save processors to a JSON file
    processors_dict = {col: str(processor) for col, processor in processors.items()}
    with open('attribution.json', 'w') as json_file:
        json.dump(processors_dict, json_file, indent=4)  
    return "The JSON file holding the attribution has been saved on your end."


def modify_attribution(attribution):
    global processors
    with open(attribution, 'r') as json_file:
        processors = json.load(json_file)
    return processors, "The attribution has been edited."
