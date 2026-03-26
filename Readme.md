# README.md

## Project Overview
This application is designed to clean, analyze, and sort Twitter data from a CSV dataset. It fulfills the requirements for the BSE Year 1 Individual Coding Lab, focusing on manual algorithmic implementation, data integrity, and shell-based analysis.

## How the Custom Sorting Algorithm Works
The script implements a **Selection Sort** algorithm to organize tweets by their like counts in descending order. It works by iteratively searching the unsorted portion of the list for the tweet with the highest number of likes and swapping it into its correct position at the front of the collection.

---

## Python Application (data-detective.py)
The Python script processes `twitter_dataset.csv` through four specific "Quests":

### 1. Data Auditor (Cleaning)
- **Logic**: Iterates through the dataset to identify missing values using `DictReader`.
- **Handling**: Rows missing the **Text** field are ignored to maintain analysis quality. Rows missing **Likes** or **Retweets** are replaced with `0`.
- **Output**: Generates `twitter_dataset_cleandata.csv` and `twitter_dataset_notcleanrows.csv`.

### 2. Viral Post (Manual Max)
- **Logic**: Performs a linear search to find the maximum value in the "Likes" column.
- **Constraint**: Implemented using a manual comparison loop to avoid the restricted `max()` function.

### 3. Algorithm Builder (Custom Sort)
- **Logic**: Uses the **Selection Sort** algorithm.
- **Process**: Orders the list from highest to lowest likes and slices the results to show the top 10.

### 4. Content Filter (Search)
- **Logic**: Extracts any tweet containing a user-defined keyword into a new list.
- **Implementation**: Uses `.append()` for list building and `len()` to report the total match count.

---

## Shell Script (feed-analyzer.sh)
The Bash script provides a terminal pipeline to identify the most active users in the dataset.

- **Commands Used**: 
  - `cut -d',' -f2`: Extracts the username column.
  - `tail -n +2`: Skips the CSV header.
  - `sort | uniq -c`: Groups and counts occurrences per user.
  - `sort -rn | head -5`: Displays the Top 5 most active accounts.

---

## Technical Details
- **Language**: Python 3.x, Bash.
- **Data Types**: CSV strings are explicitly converted to `int()` for accurate numerical comparisons (e.g., ensuring "100" > "90").
- **Documentation**: Meaningful comments are included throughout the source code for clarity.

## How to Run
1. Place `twitter_dataset.csv` in the same directory as the scripts.
2. **Python**: Run `python data-detective.py`
3. **Bash**: Run `bash feed-analyzer.sh` (ensure the script has execution permissions: `chmod +x feed-analyzer.sh`).