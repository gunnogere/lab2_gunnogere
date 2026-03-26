# Lab 2 - Joshua Mulongo
# j.mulongo@alustudent.com
# March 26th, 2026

import csv

# --- QUEST 1: THE DATA AUDITOR (Data Cleaning) ---
def process_and_audit_data(input_file="twitter_dataset.csv"):
    """
    This function handles the 'Data Detective' work:
    1. Loads the file.
    2. Checks for missing information.
    3. Separates good data from bad data (write into separate files)
    """
    raw_tweets = []
    
    # I used 'try-except' block to catch any errors
    # and prevent the program from crashing if the file is missing
    try:
        # 'utf-8' encoding ensures we can read special characters and emojis
        # these are common in tweets
        # Columns in the sheet are Tweet_ID,Username,Text,Retweets,Likes,Timestamp
        with open(input_file, "r", encoding="utf-8") as file:
            # DictReader allows access to data by column name (e.g., tweet['Text']) which is friendler to indexes e.g [0]
            reader = csv.DictReader(file)
            fieldnames = reader.fieldnames # These are the column headers (Tweet_ID, Username, etc.)
            for row in reader:
                raw_tweets.append(row) # Add each row (as a dictionary) to the list
    except FileNotFoundError:
        print(f"Error: {input_file} not found. Please check the file path.")
        return []
    
    # Variables to track our audit results
    total_rows = len(raw_tweets)
    # This dictionary creates a counter for every column, starting at 0
    missing_counts = {col: 0 for col in fieldnames}
    
    clean_list = []                # List for tweets that pass the audit
    data_with_missing_column = []  # List for tweets we decide to ignore

    # Loop through every tweet  loaded from the file
    for tweet in raw_tweets:
        this_tweet_is_unusable = False # The assumption is that the tweet is good/usable unless we find a problem
        
        # Look at every column in the specific row
        for key in fieldnames:
            val = str(tweet.get(key, "")).strip() #.strip() removes accidental spaces at the start/end
            # Check if the cell is empty 
            if val == "":
                missing_counts[key] += 1 # Increment by 1 to the 'missing' count for this column
                # Rule: If the 'Text' of the tweet is missing, we can't use it at all
                if key == "Text":
                    this_tweet_is_unusable = True

        # Sort the tweet into the 'Clean' or 'Unclean' bucket
        if this_tweet_is_unusable:
            data_with_missing_column.append(tweet)
        else:
            # Requirement: If Likes or Retweets are missing/invalid, set their value to integer= 0
            # .isdigit() checks if the string is a valid number before we convert it
            likes_val = str(tweet.get("Likes", "")).strip()
            tweet["Likes"] = int(likes_val) if likes_val.isdigit() else 0
            
            retweets_val = str(tweet.get("Retweets", "")).strip()
            tweet["Retweets"] = int(retweets_val) if retweets_val.isdigit() else 0
            
            clean_list.append(tweet)

    # Export our results into two separate CSV files
    # These two files will be the result of the data audit check and can be inspected offline
    save_to_csv("twitter_dataset_cleandata.csv", clean_list, fieldnames)
    save_to_csv("twitter_dataset_notcleanrows.csv", data_with_missing_column, fieldnames)

    # PRINTING THE AUDIT REPORT
    print("\n" )
    print("DATA QUALITY CHECK")
    print("*"*40)
    for col, count in missing_counts.items():
        # .ljust(12) keeps the column names aligned in the console
        # We draw a small bar for a visual chart
        bar = "█" * (count if count < 20 else 20) 
        print(f"{col.ljust(12)} | {bar} ({count} missing)")
    
    # Calculate the percentage of data we ignored
    ignored_percent = (len(data_with_missing_column) / total_rows) * 100 if total_rows > 0 else 0
    print(f"\n- Summary: {total_rows} total rows processed.")
    print(f"- Ignored (had empty columns): {len(data_with_missing_column)} ({ignored_percent:.2f}%)")
    print(f"- Kept (all cells had data):    {len(clean_list)}  ({100-ignored_percent:.2f}%)")
    print("*"*40)
    
    return clean_list

def save_to_csv(filename, data, fieldnames):
    """A helper function to write data into a CSV file."""
    with open(filename, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader() # Writes the column names at the top
        writer.writerows(data) # Writes all the tweet dictionaries as rows

# --- QUEST 2: THE VIRAL POST  ---
def find_most_liked(tweets):
    """Finds the tweet with the highest number of likes without using max()."""
    if not tweets: return 
    
    # We start with -1 as a baseline because any real tweet will have 0 or more likes
    highest_likes = -1
    viral_tweet = None

    # Standard 'Linear Search' for a maximum value
    for tweet in tweets:
        # If this tweet's likes are higher than current record
        if tweet["Likes"] > highest_likes:
            # ...update the record to this new value
            highest_likes = tweet["Likes"]
            viral_tweet = tweet

    print("\nQUEST 2: MOST VIRAL POST")
    print(f"Username: {viral_tweet['Username']}")
    print(f"Likes:    {viral_tweet['Likes']}")
    print(f"Text:     {viral_tweet['Text']}")

# --- QUEST 3: ALGORITHM BUILDER (Selection Sort) ---
def sort_and_print_top_10(tweets):
    """Orders tweets from most likes to fewest."""
    n = len(tweets)
    
    # We use Selection Sort: find the biggest, move it to the front, repeat
    for i in range(n):
        max_index = i # Assume the current position 'i' is the biggest
        for j in range(i + 1, n):
            # If we find something even bigger later in the list...
            if tweets[j]["Likes"] > tweets[max_index]["Likes"]:
                max_index = j #mark its position
        
        # Swap the biggest one found with the one at position 'i'
        tweets[i], tweets[max_index] = tweets[max_index], tweets[i]

    print("\nQUEST 3: TOP 10 RANKING")
    # Using enumerate(..., 1) to print a numbered list starting at 1
    # [:10] is a 'slice' looks for the first 10 items
    for i, t in enumerate(tweets[:10], 1):
        print(f"{i}. @{t['Username']} ({t['Likes']} likes)")

# --- QUEST 4: CONTENT FILTER (Search) ---
def search_tweets(tweets):
    """Builds a new list of tweets that contain a specific word."""
    query = input("\nEnter keyword to search the Tweet .CSV file data: ").lower()
    matches = [] # declares an empty array since before we start the search we have zero matches

    for tweet in tweets:
        # .lower() makes the search 'case-insensitive' (e.g., 'Python' matches 'python')
        if query in tweet["Text"].lower():
            # append() adds the matching tweet to our new list
            matches.append(tweet) 

    # len(matches) tells the user how many we found
    print(f"\nFound {len(matches)} matches for '{query}':")
    for m in matches:
        print(f"- {m['Username']} ({m['Likes']} likes): {m['Text']}")
        print("_"*40)


# --- Call the functions above
if __name__ == "__main__":
    # 1. Clean the data first
    clean_data = process_and_audit_data()
    
    # If the file was found and cleaned, proceed to the Quests
    if clean_data:
        find_most_liked(clean_data)
        sort_and_print_top_10(clean_data)
        search_tweets(clean_data)