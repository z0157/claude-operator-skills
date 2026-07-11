---
name: local-lead-finder
description: Find local businesses — especially ones with NO website — in any city, free, with no API keys. Use when the user wants local business leads, a prospect list for web/marketing services, or market research on a city's businesses. Uses OpenStreetMap (Nominatim + Overpass) with opportunity scoring and chain filtering.
---

# Local Lead Finder (OpenStreetMap, $0)

Build a scored list of real local businesses in any city — names, categories,
phones, addresses, coordinates, and whether they have a website — using only
free OpenStreetMap APIs. A "no website" flag on a real business with a phone
number is a warm lead for web design, SEO, lead-gen, and marketing services.

## The pipeline

**City name → bounding box → business dump → filter/score → ranked leads**

### 1. Geocode the city (Nominatim)

```python
import json, urllib.request, urllib.parse

UA = {"User-Agent": "LeadFinder/1.0 (contact: you@example.com)"}  # required!

def geocode(city):
    url = "https://nominatim.openstreetmap.org/search?" + urllib.parse.urlencode(
        {"q": city, "format": "json", "limit": 1, "addressdetails": 1})
    d = json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30))[0]
    bb = d["boundingbox"]   # [south, north, west, east]
    return {"south": float(bb[0]), "north": float(bb[1]),
            "west": float(bb[2]), "east": float(bb[3]),
            "city": d.get("address", {}).get("city") or city.split(",")[0],
            "state": d.get("address", {}).get("state", "")}
```

Nominatim requires a real User-Agent and ~1 req/sec. One call per city is fine.

### 2. Pull businesses (Overpass)

Query nodes AND ways (many shops are mapped as building outlines — use
`out center` to get coordinates for ways):

```python
def overpass(geo, limit=400):
    bbox = f"{geo['south']},{geo['west']},{geo['north']},{geo['east']}"
    q = f"""[out:json][timeout:90];(
      node["shop"]({bbox}); way["shop"]({bbox});
      node["craft"]({bbox}); way["craft"]({bbox});
      node["amenity"~"restaurant|fast_food|cafe|bar|pub|dentist|doctors|clinic|veterinary|car_repair|pharmacy"]({bbox});
      way["amenity"~"restaurant|fast_food|cafe|bar|dentist|clinic|car_repair"]({bbox});
      node["office"~"lawyer|accountant|estate_agent|insurance"]({bbox});
      node["leisure"~"fitness_centre|sports_centre"]({bbox});
    );out center tags {limit};"""
    req = urllib.request.Request("https://overpass-api.de/api/interpreter",
        data=urllib.parse.urlencode({"data": q}).encode(), headers=UA)
    return json.load(urllib.request.urlopen(req, timeout=120))
```

Useful tags per element: `name`, `phone`/`contact:phone`, `email`,
`website`/`contact:website`/`url`, `addr:housenumber`, `addr:street`,
`addr:city`, `addr:postcode`, plus `lat`/`lon` (or `center` for ways).

### 3. The money filter: no website

```python
website = tags.get("website") or tags.get("contact:website") or tags.get("url")
if website is None:   # <-- the lead
```

Real-world hit rates: a mid-size US city yields 150-350 no-website businesses
per pull. Expect ~40-60% to have phone numbers.

### 4. Filter chains (critical — don't skip)

OSM's missing-website tag false-positives hard on franchises (a Great Clips
has a corporate site even if its OSM node doesn't say so). Maintain a denylist
and skip matches:

```python
CHAINS = {"mcdonald","subway","starbucks","great clips","supercuts","walmart",
  "ace hardware","midas","jiffy lube","autozone","o'reilly","cvs","walgreens",
  "dollar general","7-eleven","planet fitness","h&r block","ups store",
  "state farm","verizon","t-mobile", ...}  # extend as you meet them

def is_chain(name): return any(c in name.lower() for c in CHAINS)
```

Report how many you filtered — silent filtering hides data-quality problems.

### 5. Score the opportunity

```python
def score(lead):
    s = 50.0
    if not lead["website"]: s += 45          # the core signal
    if lead.get("phone"):   s += 12          # reachable
    if lead.get("email"):   s += 6
    if lead.get("address"): s += 4
    # weight categories by willingness-to-pay for marketing services:
    s *= {"plumber":1.3,"electrician":1.3,"hvac":1.3,"contractor":1.25,
          "dentist":1.2,"auto":1.2,"salon":1.15,"restaurant":1.15}.get(lead["category"], 1.0)
    return round(s, 1)
```

Trades (plumber/HVAC/electrician) and dentists rank highest: high job value,
proven marketing spend. Sort descending; the top 20 are your call list.

## Persistence pattern

Store in SQLite with a `source_id` of `osm:{type}/{id}` as the dedupe key and a
`status` column (`new → contacted → replied → won/lost`) so repeated pulls
upsert instead of duplicating.

## Etiquette & limits
- Overpass is a shared free service: one query per city, cache results, don't hammer.
- Nominatim: 1 req/sec, identify yourself in User-Agent.
- OSM data is ODbL-licensed: fine to use for prospecting; attribute if you republish it.
- Data freshness varies by city — phones can be stale; verify before pitching.
