
def define_columns():
    processors = {
        # common columns
        "Authors": StringColumnProcessor(),
        "Publication Year": NumericColumnProcessor(),
        "Study Identification": StringColumnProcessor(),
        "Data Owner": StringNoisyColumnProcessor(),
        "Study Type": StringColumnProcessor(),
        "Batchlot": List_of_Strings_ColumnProcessor(), # For Muta one can use NumericColumnProcessor()
        "Purity [%]": List_of_Numbers_ColumnProcessor(), # For Muta one can use NumericColumnProcessor()

        # columns specific for CARC study
        "Duration (months)": NumericColumnProcessor(),
        "Route": StringColumnProcessor(), # dif
        "Dietary doses (ppm)": Ordered_List_of_Numbers_ColumnProcessor(),
        "Achieved doses in males (mg/kg)": Ordered_List_of_Numbers_ColumnProcessor(),
        "Achieved doses in females (mg/kg)": Ordered_List_of_Numbers_ColumnProcessor(),
        "NO(A)EL": NumericColumnProcessor(),
        "LO(A)EL": NumericColumnProcessor(),

        # columns specific for Muta study
        "S.typhimurium strain (TA)": List_of_Numbers_ColumnProcessor(),
        "E.coli strain": List_of_Strings_ColumnProcessor(),
        "Dose Range (preincubation) [µg/plate] (min,max)": Ordered_List_of_Numbers_ColumnProcessor(),
        "Dose Range (plate-incorporation) [µg/plate] (min,max)": Ordered_List_of_Numbers_ColumnProcessor(),
        "Known Impurities [percentage value, name]": List_of_Strings_ColumnProcessor(),
        "Metabolic Activation (plate-incorporation)": StringColumnProcessor(),
        "Metabolic Activation (preincubation)": StringColumnProcessor(),
        "Results": StringColumnProcessor(),
        "Status": StringColumnProcessor(),
    }