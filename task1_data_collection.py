# ============================================================
# TrendPulse - Task 1: Data Collection
# ============================================================

import requests
import time
import json
import os
from datetime import datetime

BASE_URL = "https://hacker-news.firebaseio.com/v0"
TOP_STORIES_URL = f"{BASE_URL}/topstories.json"

# Identify our program when making requests
headers = {
    "User-Agent": "TrendPulse/1.0"
}

# Keywords used to classify stories into categories
category_keywords = {
    "technology": [
        "AI", "software", "tech", "code", "computer",
        "data", "cloud", "API", "GPU", "LLM"
    ],
    "worldnews": [
        "war", "government", "country", "president",
        "election", "climate", "attack", "global"
    ],
    "sports": [
        "NFL", "NBA", "FIFA", "sport", "game",
        "team", "player", "league", "championship"
    ],
    "science": [
        "research", "study", "space", "physics",
        "biology", "discovery", "NASA", "genome"
    ],
    "entertainment": [
        "movie", "film", "music", "Netflix", "game",
        "book", "show", "award", "streaming"
    ]
}


# Find the category that matches a story title
def get_category(title):
    title_lower = title.lower()

    for category, keywords in category_keywords.items():
        for keyword in keywords:
            if keyword.lower() in title_lower:
                return category

    return None


print("Fetching top Hacker News stories...")

# Fetch the top 500 story IDs
try:
    response = requests.get(
        TOP_STORIES_URL,
        headers=headers,
        timeout=10
    )

    response.raise_for_status()
    story_ids = response.json()[:500]

    print(f"Successfully fetched {len(story_ids)} story IDs.")

except requests.RequestException as error:
    print(f"Failed to fetch top stories: {error}")
    story_ids = []


# Store collected stories
collected_stories = []

# Keep track of how many stories were collected per category
category_counts = {
    "technology": 0,
    "worldnews": 0,
    "sports": 0,
    "science": 0,
    "entertainment": 0
}


# Collect up to 25 stories for each category
for category in category_keywords:

    print(f"\nCollecting {category} stories...")

    for story_id in story_ids:

        # Stop when this category reaches 25 stories
        if category_counts[category] >= 25:
            break

        try:
            item_url = f"{BASE_URL}/item/{story_id}.json"

            response = requests.get(
                item_url,
                headers=headers,
                timeout=10
            )

            if response.status_code != 200:
                print(
                    f"Failed to fetch story {story_id}. "
                    f"Status: {response.status_code}"
                )
                continue

            story = response.json()

        except requests.RequestException as error:
            print(f"Request failed for story {story_id}: {error}")
            continue

        # Ignore empty results and non-story items
        if not story or story.get("type") != "story":
            continue

        title = story.get("title", "")

        # Ignore stories without a title
        if not title:
            continue

        # Determine the category from the title
        detected_category = get_category(title)

        if detected_category != category:
            continue

        # Store the required story information
        story_record = {
            "post_id": story.get("id"),
            "title": title,
            "category": category,
            "score": story.get("score", 0),
            "num_comments": story.get("descendants", 0),
            "author": story.get("by", "unknown"),
            "collected_at": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }

        collected_stories.append(story_record)
        category_counts[category] += 1

        print(
            f"{category}: "
            f"{category_counts[category]}/25"
        )

    print(
        f"Finished {category}: "
        f"{category_counts[category]} stories"
    )

    # Pause between categories to avoid sending requests too quickly
    time.sleep(2)


# Create the data folder if it does not exist
os.makedirs("data", exist_ok=True)

# Create today's JSON filename
today = datetime.now().strftime("%Y%m%d")
filename = f"data/trends_{today}.json"


# Save all collected stories as JSON
with open(filename, "w", encoding="utf-8") as file:
    json.dump(
        collected_stories,
        file,
        indent=4,
        ensure_ascii=False
    )


# Display the final collection results
print("\n" + "=" * 50)
print("TREND PULSE - COLLECTION COMPLETE")
print("=" * 50)

print("\nStories per category:")

for category, count in category_counts.items():
    print(f"{category}: {count}")

print(f"\nTotal stories collected: {len(collected_stories)}")
print(f"JSON file saved to: {filename}")

print("=" * 50)
