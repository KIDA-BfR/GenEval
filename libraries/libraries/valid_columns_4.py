import json
import pandas as pd
from collections import defaultdict
from libraries.valid_class_3 import NumericColumnProcessor, StringColumnProcessor, StringNoisyColumnProcessor, List_of_Numbers_ColumnProcessor, Ordered_List_of_Numbers_ColumnProcessor, List_of_Strings_ColumnProcessor

# Have the choice of 2 functions 
# The first one is better-suited for smaller tables
# You input a .txt file (the attribution argument) in which you already made the choice of which processing method 
# for each column by writing a list. The list is only the abbreviation of the processing method, in the same order
# as the columns go, and coma-separated.
# Time-consuming but best if you already know you don't want the default values.

# The second one is better-suited for bigger tables
# The code automatically choose a processing method for each column, depending on the type of content inside
# There are default choices, but you can modify it and choose a more suitable processing method via the JSON file 
# that you get in the end. Run it in the next function to apply the modifications, after manually editing the JSON file.

def manual_process_for_columns_attribution(table_truth, attribution):
    # Defining how many columns
    table_truth.columns = table_truth.columns.str.strip()
    nb_columns = len(table_truth.columns)

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

    


def automatic_process_for_columns_attribution(table_truth):
    # Sample data types and assign processing methods
    processors = {}
    sample_size = 5
    columns = table_truth.columns
    for column in columns:
        sample = table_truth[column].dropna().sample(min(sample_size, len(table_truth[column])))
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


def modify_attribution(attribution):
    global processors
    with open('attribution.json', 'r') as json_file:
        processors = json.load(json_file)
    print("The attribution has been edited.") 
