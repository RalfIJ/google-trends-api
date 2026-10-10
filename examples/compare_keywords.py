"""Compare any number of keywords on one Google Trends scale.

The Google Trends website compares at most 8 keywords at a time (5 in classic Explore). This example puts
10 programming languages on one shared 0-100 scale and prints each one's share of search.

    pip install apify-client
    export APIFY_TOKEN=your-token        # Windows: set APIFY_TOKEN=your-token
    python examples/compare_keywords.py
"""

import csv
import os

from apify_client import ApifyClient

KEYWORDS = ["python", "javascript", "java", "c++", "c#", "go", "rust", "kotlin", "swift", "typescript"]

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("ralfij/google-trends-scraper").call(
    run_input={
        "keywords": KEYWORDS,
        "comparison": "shared",  # one scale for all keywords
        "timeRange": "today 5-y",
        "geo": "",  # worldwide
        "category": 31,  # Programming, so "go" and "swift" mean the languages
    }
)
rows = list(client.dataset(run.default_dataset_id).iterate_items())
rows.sort(key=lambda row: row["shareOfSearch"] or 0, reverse=True)

print(f"{'keyword':<12} {'share %':>8} {'average':>8}  trend")
for row in rows:
    change = row["trendChangePercent"]
    change_text = f"{change:+.1f}%" if change is not None else "n/a"
    print(f"{row['keyword']:<12} {row['shareOfSearch']:>8} {row['averageInterest']:>8}  {row['trend']} ({change_text})")

with open("compare_keywords.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["keyword", "share_of_search", "average_interest", "trend", "trend_change_percent", "peak_date"])
    for row in rows:
        writer.writerow([row["keyword"], row["shareOfSearch"], row["averageInterest"], row["trend"], row["trendChangePercent"], row["peakDate"]])
print("\nSaved compare_keywords.csv")
