
# ============================================================
# TrendPulse - Task 4: Visualizations
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
import os

# Load the analysed data created in Task 3
input_file = "data/trends_analysed.csv"
df = pd.read_csv(input_file)

# Create the outputs folder if it does not already exist
os.makedirs("outputs", exist_ok=True)

print(f"Loaded data: {df.shape}")

# ============================================================
# Chart 1: Top 10 Stories by Score
# ============================================================

# Select the 10 stories with the highest scores
top_10 = df.nlargest(10, "score").copy()

# Shorten titles longer than 50 characters
top_10["short_title"] = top_10["title"].apply(
    lambda title: title[:50] + "..." if len(title) > 50 else title
)

# Create horizontal bar chart
plt.figure(figsize=(10, 6))
plt.barh(top_10["short_title"], top_10["score"])

plt.title("Top 10 Stories by Score")
plt.xlabel("Score")
plt.ylabel("Story Title")

# Put highest-scoring story at the top
plt.gca().invert_yaxis()

plt.tight_layout()

# Save before showing
plt.savefig("outputs/chart1_top_stories.png")
plt.show()

print("Chart 1 saved successfully.")

# ============================================================
# Chart 2: Stories per Category
# ============================================================

# Count stories in each category
category_counts = df["category"].value_counts()

# Create bar chart with different colours
plt.figure(figsize=(9, 6))

plt.bar(
    category_counts.index,
    category_counts.values,
    color=[
        "steelblue",
        "orange",
        "green",
        "red",
        "purple"
    ]
)

plt.title("Stories per Category")
plt.xlabel("Category")
plt.ylabel("Number of Stories")

plt.tight_layout()

# Save before showing
plt.savefig("outputs/chart2_categories.png")
plt.show()

print("Chart 2 saved successfully.")

# ============================================================
# Chart 3: Score vs Comments
# ============================================================

# Separate popular and non-popular stories
popular = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

plt.figure(figsize=(10, 6))

# Popular stories
plt.scatter(
    popular["score"],
    popular["num_comments"],
    color="blue",
    label="Popular"
)

# Non-popular stories
plt.scatter(
    not_popular["score"],
    not_popular["num_comments"],
    color="orange",
    label="Not Popular"
)

plt.title("Score vs Comments")
plt.xlabel("Score")
plt.ylabel("Number of Comments")
plt.legend()

plt.tight_layout()

# Save before showing
plt.savefig("outputs/chart3_scatter.png")
plt.show()

print("Chart 3 saved successfully.")

# ============================================================
# Bonus: TrendPulse Dashboard
# ============================================================

fig, axes = plt.subplots(1, 3, figsize=(20, 7))

# ------------------------------------------------------------
# Dashboard Chart 1
# ------------------------------------------------------------

axes[0].barh(
    top_10["short_title"],
    top_10["score"]
)

axes[0].set_title("Top 10 Stories by Score")
axes[0].set_xlabel("Score")
axes[0].set_ylabel("Story Title")
axes[0].invert_yaxis()

# ------------------------------------------------------------
# Dashboard Chart 2
# ------------------------------------------------------------

axes[1].bar(
    category_counts.index,
    category_counts.values,
    color=[
        "steelblue",
        "orange",
        "green",
        "red",
        "purple"
    ]
)

axes[1].set_title("Stories per Category")
axes[1].set_xlabel("Category")
axes[1].set_ylabel("Number of Stories")

# ------------------------------------------------------------
# Dashboard Chart 3
# ------------------------------------------------------------

axes[2].scatter(
    popular["score"],
    popular["num_comments"],
    color="blue",
    label="Popular"
)

axes[2].scatter(
    not_popular["score"],
    not_popular["num_comments"],
    color="orange",
    label="Not Popular"
)

axes[2].set_title("Score vs Comments")
axes[2].set_xlabel("Score")
axes[2].set_ylabel("Number of Comments")
axes[2].legend()

# Overall dashboard title
fig.suptitle("TrendPulse Dashboard", fontsize=16)

plt.tight_layout()

# Save dashboard before showing
plt.savefig("outputs/dashboard.png")
plt.show()

print("Dashboard saved successfully.")

print("\nAll Task 4 visualizations completed successfully.")
