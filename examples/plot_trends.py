"""Plot interest over time for several keywords on one shared scale.

    pip install apify-client matplotlib
    export APIFY_TOKEN=your-token        # Windows: set APIFY_TOKEN=your-token
    python examples/plot_trends.py
"""

import os
from datetime import date

import matplotlib.pyplot as plt
from apify_client import ApifyClient

KEYWORDS = ["ChatGPT", "Gemini", "Claude", "Copilot", "Perplexity", "DeepSeek"]

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("ralfij/google-trends-scraper").call(
    run_input={"keywords": KEYWORDS, "comparison": "shared", "timeRange": "today 12-m", "geo": ""}
)
rows = client.dataset(run.default_dataset_id).iterate_items()

fig, ax = plt.subplots(figsize=(10, 5))
for row in rows:
    points = [p for p in row["interestOverTime"] if not p["partial"] and p["value"] is not None]
    dates = [date.fromisoformat(p["date"][:10]) for p in points]
    ax.plot(dates, [p["value"] for p in points], label=f"{row['keyword']} ({row['shareOfSearch']}%)")

ax.set_title("Google Trends, past 12 months, worldwide (one shared scale)")
ax.set_ylabel("Search interest")
ax.legend()
fig.tight_layout()
fig.savefig("trends.png", dpi=150)
print("Saved trends.png")
