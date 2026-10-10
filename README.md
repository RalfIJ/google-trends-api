# Google Trends API for Python (a pytrends alternative)

Get Google Trends data into Python: interest over time, interest by region, top and rising related searches, and simple trend metrics. You can also **compare more than 5 keywords on one scale**, which the Google Trends website doesn't allow.

[pytrends](https://github.com/GeneralMills/pytrends) was archived in April 2025 and often fails with `429 Too Many Requests`. Google announced an official Trends API in July 2025, but it is an alpha with limited, application-based access. These examples use a hosted scraper instead, the [Google Trends Scraper](https://apify.com/ralfij/google-trends-scraper) on Apify, which deals with Google's session cookies and rate limits for you.

**Tutorial:** [Google Trends in Python without pytrends, and how to compare more than 5 keywords](docs/google-trends-python-without-pytrends.md). It covers the two endpoints behind the website, the trick for linking comparisons, and what the data looks like.

![Google searches for programming languages over 5 years](docs/programming-languages-5y.png)

*Example output: search interest in the Programming category fell 40-68% for most languages between 2021 and 2026. Made with `examples/compare_keywords.py` and matplotlib.*

## Quick start

1. Create a free [Apify account](https://console.apify.com/sign-up). The free plan includes $5 of credit every month, which covers about 2,500 keywords. No credit card needed.
2. Copy your API token from **Settings > API & Integrations** in Apify Console.
3. Run an example:

```bash
pip install -r requirements.txt
export APIFY_TOKEN=your-token        # Windows: set APIFY_TOKEN=your-token
python examples/compare_keywords.py
```

```
keyword       share %  average  trend
java             29.4     63.7  falling (-48.8%)
c++              23.8     51.6  stable (-7.1%)
python           15.8     34.3  falling (-43.7%)
...
```

## Examples

| File | What it does |
|---|---|
| [`examples/compare_keywords.py`](examples/compare_keywords.py) | Compares 10 keywords on one shared scale, prints share of search and trend, and saves a CSV |
| [`examples/keyword_report.py`](examples/keyword_report.py) | Trend, peak, busiest month, top regions and rising searches per keyword |
| [`examples/plot_trends.py`](examples/plot_trends.py) | Plots interest over time for several keywords with matplotlib |
| [`examples/raw_endpoints.py`](examples/raw_endpoints.py) | The two JSON endpoints behind trends.google.com, with no library at all. Good for a few keywords. |

[`sample-output/programming-languages-5y.csv`](sample-output/programming-languages-5y.csv) shows the CSV from `compare_keywords.py`.

## What you get per keyword

- `interestOverTime`: the full time series (0-100), with the unfinished last week or day marked `partial`
- `interestByRegion`: countries, states or regions where the keyword is most popular
- `relatedQueriesTop` and `relatedQueriesRising`, including breakouts
- `averageInterest`, `latestInterest`, `peakInterest`, `peakDate`
- `trend` (rising, falling or stable) and `trendChangePercent`: the last quarter of the period against the first quarter
- `busiestMonth` for periods of about a year or longer
- `shareOfSearch` when you compare keywords on one shared scale

## How comparing more than 5 keywords works

Google compares at most 5 keywords per request and scales each request so its highest point is 100. To compare more, the scraper:

1. requests the keywords in groups of 5;
2. compares the most searched keyword of each group (the group "leader") with the other leaders, 5 at a time with one leader of overlap, so any number of groups can be chained;
3. rescales every group through its leader, then rescales everything so the highest point overall is 100.

Google rounds to whole numbers, so a tiny keyword next to a huge one can still show as 0. Compare keywords of a similar size for the best precision.

## Notes

- I built the Google Trends Scraper used in these examples, so keep that in mind. `raw_endpoints.py` shows how to do it yourself.
- Pricing is per keyword with no subscription; see the [actor page](https://apify.com/ralfij/google-trends-scraper). More ready-made searches are on its [example tasks](https://apify.com/ralfij/google-trends-scraper/examples/ai-chatbots-compared).
- Not affiliated with, endorsed by or sponsored by Google. Google Trends is a trademark of Google LLC.

## License

MIT
