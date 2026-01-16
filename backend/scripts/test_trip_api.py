"""Quick test for Trip Planner API via requests."""
import requests
import json

response = requests.post(
    "http://localhost:8000/api/trip-planner/start",
    json={
        "origin": "LHR",
        "destination": "CDG", 
        "start_date": "2026-04-20",
        "end_date": "2026-04-25",
        "travelers": 2
    },
    timeout=120
)

print("Status:", response.status_code)
print("Response:")
print(json.dumps(response.json(), indent=2))
