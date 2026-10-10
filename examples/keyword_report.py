"""A quick trend report for a few keywords, each on its own 0-100 scale.

For every keyword it prints the trend direction, the peak, the busiest month and the
fastest rising related searches, then saves everything to keyword_report.json.

    pip install apify-client
    export APIFY_TOKEN=your-token        # Windows: set APIFY_TOKEN=your-token
    python examples/keyword_report.py
"""

import json
import os

from apify_client import ApifyClient

KEYWORDS = ["coffee", "tea", "matcha"]

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("ralfij/google-trends-scraper").call(
    run_input={
        "keywords": KEYWORDS,
        "comparison": "separate",  # each keyword on its own scale
        "timeRange": "today 12-m",
        "geo": "US",
    }
)
rows = list(client.dataset(run.default_dataset_id).iterate_items())

for row in rows:
    change = row["trendChangePercent"]
    print(f"\n{row['keyword']} ({row['location']}, {row['timeRange']})")
    print(f"  trend:         {row['trend']}" + (f" ({change:+.1f}%)" if change is not None else ""))
    print(f"  peak:          {row['peakInterest']} on {row['peakDate']}")
    print(f"  busiest month: {row['busiestMonth'] or 'n/a'}")
    top_regions = ", ".join(region["name"] for region in row["interestByRegion"][:3])
    print(f"  top regions:   {top_regions or 'n/a'}")
    rising = [f"{q['query']} ({q['change']})" for q in row["relatedQueriesRising"][:5]]
    print(f"  rising:        {'; '.join(rising) or 'n/a'}")

with open("keyword_report.json", "w", encoding="utf-8") as f:
    json.dump(rows, f, indent=2, ensure_ascii=False)
print("\nSaved keyword_report.json")
