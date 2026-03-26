#!/bin/bash

# Name of the target CSV file
FILE="twitter_dataset.csv"

# Error handling: Check if the file exists before processing
if [ ! -f "$FILE" ]; then
    echo "Error: $FILE not found in current directory."
    exit 1
fi

echo "-----------------------------------"
echo "TOP 5 MOST ACTIVE USERS (BASH)"
echo "-----------------------------------"

# Pipeline Explanation:
# 1. cut -d',' -f2  : Extracts only the 2nd column (Username)
# 2. tail -n +2     : Removes the header row from the output
# 3. sort           : Groups duplicate usernames together for uniq
# 4. uniq -c        : Counts the consecutive identical lines (usernames)
# 5. sort -rn       : Sorts the counts numerically (-n) in reverse (-r)
# 6. head -5        : Displays only the top 5 results

cut -d',' -f2 "$FILE" | tail -n +2 | sort | uniq -c | sort -rn | head -5