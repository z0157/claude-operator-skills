---
name: govcon-scout
description: Research U.S. federal contract spending and opportunities with free government APIs. Use when the user asks what the government buys, who wins contracts, realistic contract sizes in a category, or wants to find bid opportunities — USAspending (no key) for awarded contracts, SAM.gov (free key) for open solicitations.
---

# GovCon Scout

Answer "what does the government actually buy, from whom, for how much?" with
real award data — and find live bid opportunities. Two APIs cover it:

| API | Auth | What it gives you |
|---|---|---|
| **USAspending.gov** | None | Every awarded federal contract (historical fact) |
| **SAM.gov opportunities** | Free personal key | Open solicitations you can bid on now |

## USAspending: awarded contracts (no key, start here)

POST JSON to `https://api.usaspending.gov/api/v2/search/spending_by_award/`:

```python
import json, urllib.request

def post(url, body):
    req = urllib.request.Request(url, data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"})
    return json.load(urllib.request.urlopen(req, timeout=60))

res = post("https://api.usaspending.gov/api/v2/search/spending_by_award/", {
  "filters": {
    "award_type_codes": ["A", "B", "C", "D"],          # contract awards
    "naics_codes": ["561730"],                          # landscaping
    "time_period": [{"start_date": "2025-10-01", "end_date": "2026-06-30"}],
    "award_amounts": [{"lower_bound": 10000, "upper_bound": 150000}],
  },
  "fields": ["Award ID", "Recipient Name", "Award Amount", "Awarding Agency",
             "Awarding Sub Agency", "Place of Performance State Code", "Description",
             "Period of Performance Start Date", "Period of Performance Current End Date"],
  "sort": "Award Amount", "order": "desc", "limit": 25, "page": 1})
```

Count without fetching rows: same filters to
`/api/v2/search/spending_by_award_count/` → `results.contracts`.

### Analysis patterns that answer real questions
- **"Is there volume in this niche?"** → award count by NAICS in the $10K-150K
  band (the realistic small-business range). Janitorial 561720 and landscaping
  561730 run 1,400-1,900 awards per fiscal year in that band.
- **"What does a typical win look like?"** → sample descriptions + amounts.
  Watch for "BASE YEAR"/"OPTION YEAR" language — a $90K award may be year 1 of 5.
- **"Who's winning near me?"** → filter `place_of_performance_locations`, read
  Recipient Names; small LLCs winning repeatedly = the competitive tier.
- Top-line totals mislead: a $48B Dept of Energy lab contract sits in the same
  NAICS as $10K mowing jobs. Always band by award_amounts.

### Useful starter NAICS (services anyone can enter)
561720 janitorial · 561730 landscaping/snow · 238320 painting ·
562112 hazardous waste · 561621 security systems · 561210 facilities support

## SAM.gov: open opportunities (free key required)

`GET https://api.sam.gov/opportunities/v2/search` with:
`api_key`, `postedFrom`/`postedTo` (MM/dd/yyyy, both required), `limit`,
`ptype=o` (solicitations), `ncode` (NAICS), optional `typeOfSetAside`
(`SBA`, `8A`, `WOSB`...) and `state`.

- **DEMO_KEY does not work** — it 404s. A real personal key is free:
  SAM.gov → sign in → Account Details → Request API Key.
- Response `opportunitiesData[]`: `title`, `fullParentPathName` (agency),
  `responseDeadLine`, `typeOfSetAside`, `placeOfPerformance`, `uiLink`
  (direct link to the solicitation with attached SOW/PWS documents).
- Sort client-side by `responseDeadLine` for a bid calendar.

## Honest-analysis guardrails (include these in any report)
- Awarded ≠ available: USAspending shows history; only SAM.gov lists live bids.
- FAR 52.219-14 limits pass-through subcontracting on small-biz set-asides
  (prime must self-perform ≥50% of services labor) — flag this whenever the
  user's plan is "win it and sub it all out."
- Payment is Net-30 after invoicing (Prompt Payment Act) — cash-flow gap is real.
- Bands, not averages: award distributions are heavy-tailed; medians and
  percentile bands are the honest summary.
