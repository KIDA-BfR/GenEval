from libraries.valid_class_3 import NumericColumnProcessor, StringColumnProcessor, StringNoisyColumnProcessor, List_of_Numbers_ColumnProcessor, Ordered_List_of_Numbers_ColumnProcessor, List_of_Strings_ColumnProcessor

def define_columns(table_truth):
    
    #defining how many columns
    table_truth.columns = table_truth.columns.str.strip()
    nb_columns = len(table_truth.columns)

    #choosing processing method for each column
    liste_attribution = []
    for i in range (nb_columns):
        print("What type of processing ?")
        print("Choose from this table: ")
        print("Processing methods ")
        print("-"*19)
        print("1 - NumericColumnProcessor()")
        print("2 - StringColumnProcessor()")
        print("3 - StringNoisyColumnProcessor()")
        print("4 - List_of_Numbers_ColumnProcessor()")
        print("5 - Ordered_List_of_Numbers_ColumnProcessor()")
        print("6 - List_of_Strings_ColumnProcessor()")
        c = int(input("Choose a number between 1 to 6"))
        if c == 1:
            liste_attribution.append(NumericColumnProcessor())
        elif c == 2:
            liste_attribution.append(StringColumnProcessor())
        elif c == 3:
            liste_attribution.append(StringNoisyColumnProcessor())
        elif c == 4:
            liste_attribution.append(List_of_Numbers_ColumnProcessor())
        elif c == 5:
            liste_attribution.append(Ordered_List_of_Numbers_ColumnProcessor())
        elif c == 6:
            liste_attribution.append(List_of_Strings_ColumnProcessor())
        else:
            print("Invalid choice. Please select a number between 1 to 6.")

    #pairing each columns with processing methods
    processors = dict(zip(table_truth.columns,liste_attribution))
    return processors 
