"""Google Trends without any library: the two JSON endpoints behind trends.google.com.

Fine for a handful of keywords. At scale Google answers with "429 Too Many Requests"
per IP, and it compares at most 5 keywords per request. See the other examples for
the hosted version that handles both.

    pip install requests
    python examples/raw_endpoints.py
"""

import json
from datetime import datetime, timezone

import requests


def google_json(text):
    return json.loads(text[text.index("{"):])  # answers start with a ")]}'" guard line


s = requests.Session()
s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36"
s.get("https://trends.google.com/trends/explore?geo=US")  # sets the NID cookie, even when it answers 429

req = {"comparisonItem": [{"keyword": "matcha", "geo": "US", "time": "today 12-m"}], "category": 0, "property": ""}
r = s.get("https://trends.google.com/trends/api/explore", params={"hl": "en-US", "tz": 0, "req": json.dumps(req)})
widgets = google_json(r.text)["widgets"]

timeseries = next(w for w in widgets if w["id"] == "TIMESERIES")
r = s.get(
    "https://trends.google.com/trends/api/widgetdata/multiline",
    params={"hl": "en-US", "tz": 0, "req": json.dumps(timeseries["request"]), "token": timeseries["token"]},
)
for point in google_json(r.text)["default"]["timelineData"][-3:]:
    day = datetime.fromtimestamp(int(point["time"]), tz=timezone.utc).date()
    print(day, point["value"][0])
