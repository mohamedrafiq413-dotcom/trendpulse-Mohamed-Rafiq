
# ============================================================
# TrendPulse - Task 2: Clean the Data & Save as CSV
# ============================================================

import pandas as pd
import os

# Load the JSON file collected in Task 1
input_file = "data/trends_20260928.json"
df = pd.read_json(input_file)

# Print the number of stories loaded
print(f"Loaded {len(df)} stories from {input_file}")

# Remove duplicate stories based on post_id
df = df.drop_duplicates(subset="post_id")
print(f"After removing duplicates: {len(df)}")

# Remove rows missing required values
df = df.dropna(subset=["post_id", "title", "score"])
print(f"After removing nulls: {len(df)}")

# Convert score and num_comments to integers
df["score"] = pd.to_numeric(
    df["score"], errors="coerce"
).fillna(0).astype(int)

df["num_comments"] = pd.to_numeric(
    df["num_comments"], errors="coerce"
).fillna(0).astype(int)

# Remove stories with a score below 5
df = df[df["score"] >= 5]
print(f"After removing low scores: {len(df)}")

# Remove extra whitespace from titles
df["title"] = df["title"].str.strip()

# Create the data folder if it does not exist
os.makedirs("data", exist_ok=True)

# Save the cleaned data as a CSV file
output_file = "data/trends_clean.csv"
df.to_csv(output_file, index=False)

print(f"Saved {len(df)} rows to {output_file}")

# Display the number of stories in each category
print("\nStories per category:")

category_summary = df["category"].value_counts()

for category, count in category_summary.items():
    print(f"  {category:<15} {count}")
