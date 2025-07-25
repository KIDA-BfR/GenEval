# Validation of an LLM-performed Extraction Library
---

This library compares a ground truth table to an extraction table and evaluates the accuracy of the extraction.

---

## Main goal
---
The idea behind the creation of such library is to be able to validate the data extraction performance of an LLM - or any other data extraction tool.
For now, nine different data types can be analysed. They are listed under **As an input**.
More processing methods can/ will be added.

To use this library, you will produce a ground truth table - in which you read and copied at least one PDF file content of interest.
Then you will produce an extracted "compared" table - by an LLM or another tool - for which you asked to extract the same content as in your ground truth table.

This library is relevant if a bigger LLM extraction project is undertaken. You can apply this library to a sample of PDF files, from which you would have previously extracted the data - by hand and via the use of an LLM.

---

## An an input:
---
You input 2 files, containing the following type of data:
- Strings, Approximate strings, Lists of strings, Sentences
- Numbers, Lists of numbers, Ordered lists of numbers

---

## Functions - Application to a basic use case

You can find the use case tables under the folder `use_case_content`
- `truth_table.xlsx`
- `compared_table.xlsx`

There is also the file 
- `attribution.json` useful to test the function `manual_process_for_columns_attribution`
---

### 1. `reading_tables()`
This function allows to load the data tables.
Change the path way to your actual one to load files.
You can display the tables by setting `display_tables` to `True`.

```python
from validation_package.load import reading_tables

table_truth, table_compared = reading_tables("your_file_path/truth_table.xlsx", "your_file_path/compared_table.xlsx", display_tables = True)
```

### 2. `sort_data()`
This function normalize the data and allows you to edit a glossary in the function's arguments. 
Useful to indicate the code that some non-identical items should be treated as identical.

```python
from validation_package.sort_and_glossary import sort_data

sort_data(table_truth, table_compared, gloassry = None)
```

### 3. classes
Here are the current different processing methods you can find to validate your data.
Each processing method is stored under a class.

| Name of the class | Manual attribution | Data type | Description |
|-------------------|--------------------|-------------|-----------|
| `StringColumnProcessor` | words | str | Compares string columns by normalizing them & comparing using sequence matching
| `StringNoisyColumnProcessor` | words_not_exact | str | Like `StringColumnProcessor` but with lower similarity threshold
| `NumericColumnProcessor` | num | int, float | Compares numeric values
| `BooleanListColumnProcessor` | choice | int, float, str | Accepts boolean operators in truth file and checks comparison file accordingly
| `KeywordListColumnProcessor` | keyword | str | Takes truth file as keywords and only looks for keywords in extraction
| `ListColumnProcessor` | list_num | int, float | Compares lists with numeric values
| `OrderedListColumnProcessor` | list_num_order | int, float | Compares lists with numeric values and take order into account
| `List_of_Strings_ColumnProcessor` | list_words | str | Compares lists with string values
| `LLMColumnProcessor` | sentence | int, float | Lets an LLM prompt-based compare the 2 files

**Warning** : You need an **API key** to use the `LLMColumnProcessor`.
You will be asked to input it when running the columns attribution part

### 4. columns attribution
This part includes 3 functions, of which 2 main, and you should choose the best-suited one for your case.
In this example we are using both to demonstrate, but they have the same goal. The 3rd one is linked with the 2nd one.

#### 4.1. `manual_process_for_columns_attribution()`
This function is better-suited for smaller tables. 
You input a .txt file (the attribution argument) in which you already made the choice of which processing method for each column by writing a list. The list is only the abbreviation of the processing method (cf ***3. classes***), reminded when you run the function, in the same order as the columns and coma-separated.
Time-consuming but best if you already know you don't want the default values.
Change the path way to your actual one to load attribution file.

``` python
from validation_package.columns_attribution import manual_process_for_columns_attribution

attribution_file = "your_file_path/manual_attribution_ex.txt"
processors = manual_process_for_columns_attribution(table_truth, attribution_file)
print(processors)
```

#### 4.2. `automatic_process_for_columns_attribution()`
The second one is better-suited for bigger tables. 
The code automatically choose a processing method for each column, depending on the type of content inside.
There are default choices, but you can modify it and choose a more suitable processing method via the JSON file that you get in the end. 
Run it in the next function to apply the modifications, after manually editing the JSON file.

``` python
from validation_package.columns_attribution import automatic_process_for_columns_attribution

processors = automatic_process_for_columns_attribution(table_truth)
print(processors)
```

#### 4.3. `modify_attribution()`
As mentioned previously, run the modified JSON file to update the dictionary containing the processing method for each column.
Change the path way to your actual one to load new attribution file.

``` python
from validation_package.columns_attribution import modify_attribution

modified_attribution_file = "your_file_path/modified_attribution_file.json"
new_processors = modify_attribution(modified_attribution_file)
print(new_processors)
```

### 5. `comparison_init()`
This function initialises the confusion matrix and the comparison results.

``` python
from validation_package.comparison import comparison_init

comparison_results, confusion_matrices = comparison_init(table_truth, table_compared, processors)
```

### 6. `results()`
Finally this function provides an .xlsx file with the comparison results.
You can display the tables by setting `display_results` to `True`.

``` python 
from validation_package.get_results import results

combined_output, confusion_matrices_df = results(table_truth, table_compared, comparison_results, confusion_matrices, display_results=True)
``` 

---

## Output:
---
You get 2 files saved on your end: a confusion matrice and a table compararison side by side of each row of each column.

---

## Installation

