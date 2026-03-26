import csv

# --- QUEST 1: THE DATA AUDITOR (Data Cleaning) ---
def process_and_audit_data(input_file="twitter_dataset.csv"):
    """
    Loads the CSV, audits for missing fields, and splits data into 
    'Clean' and 'Unclean' files for professional record-keeping.
    """
    raw_tweets = []
    
    # Standard file loading with UTF-8 encoding to handle emojis
    try:
        with open(input_file, "r", encoding="utf-8") as file:
            # DictReader treats the first row as keys for easier access
            reader = csv.DictReader(file)
            fieldnames = reader.fieldnames
            for row in reader:
                raw_tweets.append(row)
    except FileNotFoundError:
        print(f"Error: {input_file} not found. Please check the file path.")
        return []

    # Initialize counters for the Data Audit report
    total_rows = len(raw_tweets)
    missing_counts = {col: 0 for col in fieldnames}
    
    clean_list = []
    garbage_list = []

    for tweet in raw_tweets:
        is_unusable = False
        
        # Iterate through columns to find empty or 'None' values
        for key in fieldnames:
            val = str(tweet.get(key, "")).strip()
            if val == "" or val.lower() == "none":
                missing_counts[key] += 1
                # Requirement: If 'Text' is missing, ignore/remove the row
                if key == "Text":
                    is_unusable = True

        if is_unusable:
            # Row is added to the "Unclean" list for export
            garbage_list.append(tweet)
        else:
            # Requirement: Fix Likes/Retweets if missing by defaulting to 0
            # Data Types: Convert strings to integers for mathematical comparison
            l_val = str(tweet.get("Likes", "")).strip()
            tweet["Likes"] = int(l_val) if l_val.isdigit() else 0
            
            r_val = str(tweet.get("Retweets", "")).strip()
            tweet["Retweets"] = int(r_val) if r_val.isdigit() else 0
            
            # Add valid data to the 'Clean' list
            clean_list.append(tweet)

    # Save cleaned results to disk (overwrites each execution)
    save_to_csv("twitter_dataset_cleandata.csv", clean_list, fieldnames)
    save_to_csv("twitter_dataset_notcleanrows.csv", garbage_list, fieldnames)

    # VISUAL AUDIT REPORT
    print("\n" + "="*40)
    print("📊 DATA QUALITY AUDIT")
    print("="*40)
    for col, count in missing_counts.items():
        # Create a text-based bar chart using the '█' character
        bar = "█" * (count if count < 20 else 20)
        print(f"{col.ljust(12)} | {bar} ({count} missing)")
    
    # Summary using len() to check list sizes as per requirements
    ignored_pct = (len(garbage_list) / total_rows) * 100 if total_rows > 0 else 0
    print(f"\nSummary: {total_rows} total rows processed.")
    print(f"- Ignored: {len(garbage_list)} ({ignored_pct:.2f}%)")
    print(f"- Kept:    {len(clean_list)}")
    print("="*40)
    
    return clean_list

def save_to_csv(filename, data, fieldnames):
    """Helper function to write lists of dictionaries to CSV files."""
    with open(filename, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

# --- QUEST 2: THE VIRAL POST (Manual Maximum) ---
def find_most_liked(tweets):
    """Finds the highest Likes using a logical loop (No max() allowed)."""
    if not tweets: return
    
    # Start with a baseline for comparison
    highest_likes = -1
    viral_tweet = None

    for tweet in tweets:
        # Comparison logic: update if current tweet has more likes
        if tweet["Likes"] > highest_likes:
            highest_likes = tweet["Likes"]
            viral_tweet = tweet

    print("\n🔥 QUEST 2: MOST VIRAL POST")
    print(f"Username: {viral_tweet['Username']}")
    print(f"Likes:    {viral_tweet['Likes']}")
    print(f"Text:     {viral_tweet['Text']}")

# --- QUEST 3: ALGORITHM BUILDER (Selection Sort) ---
def sort_and_print_top_10(tweets):
    """Sorts tweets by Likes DESC using Selection Sort (No .sort() allowed)."""
    n = len(tweets)
    
    # Standard Selection Sort algorithm
    for i in range(n):
        max_idx = i
        for j in range(i + 1, n):
            # Compare current index with the rest of the list
            if tweets[j]["Likes"] > tweets[max_idx]["Likes"]:
                max_idx = j
        
        # Swap the found maximum element with the first element
        tweets[i], tweets[max_idx] = tweets[max_idx], tweets[i]

    print("\n🏆 QUEST 3: TOP 10 RANKING")
    # Slicing the list to only show the top 10 results
    for i, t in enumerate(tweets[:10], 1):
        print(f"{i}. @{t['Username']} ({t['Likes']} likes)")

# --- QUEST 4: CONTENT FILTER (Search) ---
def search_tweets(tweets):
    """Extracts matching tweets into a new list based on user input."""
    query = input("\nEnter keyword to search: ").lower()
    matches = []

    for tweet in tweets:
        # Check if query exists within the Text field
        if query in tweet["Text"].lower():
            matches.append(tweet) # Using .append() as per instructions

    # Display count using len() and the results
    print(f"\nFound {len(matches)} matches for '{query}':")
    for m in matches:
        print(f"- {m['Username']} ({m['Likes']} likes): {m['Text']}")

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    # Execute the cleaning pipeline first
    clean_data = process_and_audit_data()
    
    if clean_data:
        find_most_liked(clean_data)
        sort_and_print_top_10(clean_data)
        search_tweets(clean_data)