
# ============================================================
# TrendPulse - Task 3: Analysis with Pandas & NumPy
# ============================================================

import pandas as pd
import numpy as np
import os

# Load the cleaned CSV file from Task 2
input_file = "data/trends_clean.csv"
df = pd.read_csv(input_file)

print(f"Loaded data: {df.shape}")

# ------------------------------------------------------------
# 1. Load and Explore the Data
# ------------------------------------------------------------

print("\nFirst 5 rows:")
print(df.head())

# Calculate average score and average number of comments
average_score = df["score"].mean()
average_comments = df["num_comments"].mean()

print(f"\nAverage score   : {average_score:.2f}")
print(f"Average comments: {average_comments:.2f}")

# ------------------------------------------------------------
# 2. NumPy Analysis
# ------------------------------------------------------------

# Convert scores to a NumPy array
scores = df["score"].to_numpy()

# Calculate NumPy statistics
mean_score = np.mean(scores)
median_score = np.median(scores)
std_score = np.std(scores)
max_score = np.max(scores)
min_score = np.min(scores)

print("\n--- NumPy Stats ---")
print(f"Mean score   : {mean_score:.2f}")
print(f"Median score : {median_score:.2f}")
print(f"Std deviation: {std_score:.2f}")
print(f"Max score    : {max_score}")
print(f"Min score    : {min_score}")

# Find the category with the most stories
category_counts = df["category"].value_counts()

most_common_category = category_counts.idxmax()
most_common_count = category_counts.max()

print(
    f"\nMost stories in: "
    f"{most_common_category} ({most_common_count} stories)"
)

# Find the story with the most comments
most_commented = df.loc[df["num_comments"].idxmax()]

print(
    f'Most commented story: "{most_commented["title"]}" '
    f'— {most_commented["num_comments"]} comments'
)

# ------------------------------------------------------------
# 3. Create New Columns
# ------------------------------------------------------------

# Calculate engagement
# Formula: num_comments / (score + 1)
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# Create is_popular column
# True when the story score is above the average score
df["is_popular"] = df["score"] > average_score

print("\nNew columns added:")
print(df[["title", "score", "num_comments", "engagement", "is_popular"]].head())

# ------------------------------------------------------------
# 4. Save the Analysed Data
# ------------------------------------------------------------

# Make sure the data folder exists
os.makedirs("data", exist_ok=True)

output_file = "data/trends_analysed.csv"
df.to_csv(output_file, index=False)

print(f"\nSaved analysed data to {output_file}")
