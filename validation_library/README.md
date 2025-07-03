# Validation of an LLM-performed Extraction Library
---

This library compares a ground truth table to an extraction table and evaluates the accuracy of the extraction.

---

## Main goal
---
The idea behind the creation of such library is to be able to validate the data extraction performance of an LLM - or any other data extraction tool.
For now, six different data types can be analysed. They are listed under **Type of extracted data**.
More processing methods can/ will be added.

You need first at least one PDF file containing all the relevant data.
Then you will produce a ground truth table - in which you read and copied the PDF file content of interest.
The you will produce an extracted "compared" table - by an LLM or another tool - for which you asked to extract the same content as in your ground truth table.

This library is relevant if a bigger LLM extraction project is undertaken. You can apply this library to a sample of PDF files, from which you would have previously extracted the data - by hand and via the use of an LLM.

---

## Type of extracted data
---
- Strings, Approximate strings, Lists of strings
- Numbers, Lists of numbers, Ordered lists of numbers

---

## Functions - Application to a basic use case

You can find the use case tables under the folder `content`
- `truth_table.xlsx`
- `compared_table.xlsx`

---

### 1. `reading_tables()`
This function allows to load the data tables.

python
from libraries. import reading_tables

table_truth, table_compared = reading_tables("file_path/truth_table.xlsx", "file_path/compared_table.xlsx)

### 2. `sort_data()`

### 3. classes

| Name of the class | Manual attribution | Data type | Description |
|-------------------|--------------------|-------------|-----------|
| `NumericColumnProcessor` | num | int, float | ?
| `StringColumnProcessor` | words | str | ? 
| `StringNoisyColumnProcessor` | words_not_exact | str | ? 
| `List_of_Numbers_ColumnProcessor` | list_num | int, float | ? 
| `Ordered_List_of_Numbers_ColumnProcessor` | ordered_list_num | int, float | ? 
| `List_of_Strings_ColumnProcessor` | list_words | str | ?

### 4.1. `manual_process_for_columns_attribution()`
### 4.2. `automatic_process_for_columns_attribution()`
### 4.3. `modify_attribution()`

### 5. `comparison_init()`

### 6. `results()`

---

# Installation

