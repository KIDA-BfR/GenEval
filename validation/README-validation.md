# ColumnProcessor Class Hierarchy and Logic
---

## 1. Abstract Base: `ColumnProcessor`
- **`process(value)`** and **`compare(val1, val2)`** are declared.  
- Every concrete subclass must override both methods.

---

## 2. `NumericColumnProcessor`
### `process(value)`
1. **Missing or non-applicable**  
   - Returns `""` if `value` is `NaN`, `"N/A"` or an empty string.  
2. **Numeric conversion & rounding**  
   - Tries `float(value)` and rounds to **2 decimal places**.  
   - If conversion fails, logs an error and returns the original (unrounded) value.

### `compare(val1, val2)`
1. **Presence checks**  
   - `""` vs non-`""` → **False Positive** or **False Negative**  
   - both `""` → **Correct**  
2. **Exact numeric match**  
   - If the two (rounded) floats are equal → **Correct**, else → **Incorrect**

---

## 3. `StringColumnProcessor`
Wraps the `NumericColumnProcessor` to try numeric fallback.

### `process(value)`
1. **Missing or N/A** → `""`  
2. **Cleanup**  
   - Trim, lowercase, strip `%` and bracket characters, remove all whitespace.  
3. **Numeric fallback**  
   - Attempt `float(cleaned_string)`.  
   - If success, return the result of the numeric processor on that float.  
   - Otherwise, return the cleaned string.

### `compare(val1, val2)`
1. **Presence checks** (same as numeric)  
2. **Numeric-style compare**  
   - Tries `NumericColumnProcessor.compare(val1, val2)`  
3. **String similarity**  
   - If numeric compare isn’t possible, computes `SequenceMatcher.ratio()`.  
   - Only perfect matches (`ratio == 1`) count as **Correct**, else **Incorrect**.

---

## 4. `StringNoisyColumnProcessor`
- Inherits all of `StringColumnProcessor.process`.  
- **`compare`** uses **fuzzy** matching on strings:  
  - Same presence checks as above.  
  - Computes `SequenceMatcher.ratio()`.  
  - Returns **Correct** if similarity **> 0.75**, else **Incorrect**.

---

## 5. `List_of_Numbers_ColumnProcessor`
### `process(value)`
1. **Missing or N/A** → `""`  
2. **Single number**  
   - If `value` can be cast directly to `float`, returns `[float(value)]`.  
3. **Extract multiple numbers**  
   - Uses regex `\d+(?:\.\d+)?` to pull out all integer/decimal substrings.  
   - Converts each to `float` and returns the list.

### `compare(truth_list, comparison_list)`
1. Convert both lists to **sets**.  
2. Compute:  
   - **Missing elements** = items in truth but not in comparison.  
   - **Extra elements** = items in comparison but not in truth.  
3. Decide:  
   - Both missing & extra → **Incorrect**  
   - Only extra → **False Positive**  
   - Only missing → **False Negative**  
   - Neither → **Correct**

---

## 6. `Ordered_List_of_Numbers_ColumnProcessor`
- Inherits `process` from `List_of_Numbers_ColumnProcessor`.  
- **`compare`** tweaks the above logic:  
  1. Same extra/missing checks for FP/FN.  
  2. If both lists have the same elements but differ in order → **Incorrect**.  
  3. Exact same content _and_ order → **Correct**.

---

## 7. `List_of_Strings_ColumnProcessor`
### `__init__`
- Creates its own `StringColumnProcessor` for per-item cleaning/comparison.

### `process(value)`
1. **Missing or N/A** → `""`  
2. **Split** on commas or semicolons.  
3. **Clean each piece** via `StringColumnProcessor.process`, returning a list of cleaned strings.

### `compare`
- Inherits the **set-based** comparison from `List_of_Numbers_ColumnProcessor`, but applied to the processed string list.

---

### Overall Architecture
1. **Preprocessing** (`process`):  
   Normalize raw cell values into a consistent Python type (empty string, float, string, or a list of them).  
2. **Comparison** (`compare`):  
   Use presence checks first (empty vs non-empty), then type-specific logic:
   - Exact equality for strict numeric/string cases.  
   - Fuzzy/string-distance for noisy text.  
   - Set or ordered comparisons for lists.

This layered design allows the user to plug in new column types (e.g. dates, booleans) by subclassing `ColumnProcessor`, implementing `process` and `compare`, and benefiting from the same high-level workflow.
