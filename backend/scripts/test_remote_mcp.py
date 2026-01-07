import httpx

# Test Google Flights2 tools
print("--- Google Flights2 Tools ---")
r = httpx.get('http://127.0.0.1:8000/api/mcp/tools/rapidapi-google-flights2', timeout=60)
data = r.json()
print(f"Tool count: {data['count']}")
for t in data['tools']:
    print(f"  - {t['name']}: {t.get('description', '')[:50]}...")

print("\n--- Booking.com Tools (searching for flights) ---")
r2 = httpx.get('http://127.0.0.1:8000/api/mcp/tools/rapidapi-booking', timeout=90)
data2 = r2.json()
print(f"Total count: {data2['count']}")
flight_tools = [t for t in data2['tools'] if 'flight' in t['name'].lower()]
print(f"Flight-related tools: {len(flight_tools)}")
for t in flight_tools:
    print(f"  - {t['name']}")
