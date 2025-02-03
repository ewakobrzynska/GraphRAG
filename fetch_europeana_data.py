import requests
import json

EUROPEANA_API_KEY = "oqualongl"
BASE_URL = "https://api.europeana.eu/record/v2/search.json"

def fetch_europeana_data(query, rows=10):
    params = {
        "wskey": EUROPEANA_API_KEY,
        "query": query,
        "rows": rows,
        "profile": "rich",
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    return data.get("items", [])

data = fetch_europeana_data("ancient vase")
with open("europeana_data.json", "w") as f:
    json.dump(data, f, indent=2)
