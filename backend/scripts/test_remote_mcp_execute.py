import httpx
import json

# Test executing a flight search via remote MCP
print("--- Testing Search_Flights execution via Google Flights2 ---")

# First, let's get the tool schema to understand required params
r_form = httpx.get('http://127.0.0.1:8000/api/mcp/tools/rapidapi-google-flights2/Search_Flights/form', timeout=60)
print(f"Form schema status: {r_form.status_code}")
if r_form.status_code == 200:
    form = r_form.json()
    print(f"Tool: {form['toolName']}")
    print("Fields:")
    for f in form['fields']:
        req = "*" if f['required'] else ""
        print(f"  - {f['name']}{req}: {f['type']}")

# Execute the search
print("\n--- Executing flight search ---")
search_args = {
    "departure_id": "LHR",
    "arrival_id": "JFK",
    "outbound_date": "2026-04-20"
}

r_exec = httpx.post(
    'http://127.0.0.1:8000/api/mcp/tools/rapidapi-google-flights2/Search_Flights/execute',
    json=search_args,
    timeout=90
)
print(f"Execution status: {r_exec.status_code}")
result = r_exec.json()
print(f"Success: {result.get('success')}")
if result.get('result'):
    for item in result['result'][:1]:
        text = item.get('text', '')
        # Parse as JSON if possible
        try:
            import json
            data = json.loads(text)
            if 'data' in data:
                flights = data['data']
                if isinstance(flights, dict) and 'itineraries' in flights:
                    itin = flights['itineraries']
                    if 'topFlights' in itin:
                        for f in itin['topFlights'][:3]:
                            print(f"  Flight: ${f.get('price')} | {f.get('departure_time')} -> {f.get('arrival_time')}")
                elif isinstance(flights, list):
                    for f in flights[:3]:
                        print(f"  Flight: ${f.get('price')} | {f.get('departure_time')} -> {f.get('arrival_time')}")
            else:
                print(f"Response: {text[:300]}")
        except:
            print(f"Raw: {text[:300]}")
else:
    print(f"Error or empty result")
