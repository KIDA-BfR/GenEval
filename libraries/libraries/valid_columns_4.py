
from libraries.libraries.valid_class_3 import NumericColumnProcessor, StringColumnProcessor, StringNoisyColumnProcessor, List_of_Numbers_ColumnProcessor, Ordered_List_of_Numbers_ColumnProcessor, List_of_Strings_ColumnProcessor

#prb 1: 


def define_columns():
#méthode 2: choix de la classe pr chaque colonne
    # try :
    #     for i in range(1,len('table')+1):
    #         c_i = [read ième column name]
    #         print("'c_i' is your column {i}")
    #         print("How would you process it ?")
    #         #besoin de trouver un moyen de répertorier ttes les class de valid_class_3.py sans les énumérer manuellement
    #         print("Choose among: ...")
            
    #         process = input()
    #         print("You chose {process}")

    # except ValueError:
    #     print("Choose a valid processing method.")

#méthode 1: choix de la colonne pr chaque classe

#méthode 2: autre approche
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

    liste_attribution = []
    for i in range (len('table')):
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

    processors = {

        "column 1: " : liste_attribution[0],
        "column 2: " : liste_attribution[1],


        "column n: " : liste_attribution[n],
    }






