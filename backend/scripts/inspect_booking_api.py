import httpx
import json
import os

# Base URL for backend MCP proxy
BASE_URL = 'http://127.0.0.1:8000/api/mcp/tools/rapidapi-booking'

def get_tool_schema(tool_name):
    print(f"\n--- Fetching schema for {tool_name} ---")
    try:
        resp = httpx.get(f"{BASE_URL}/{tool_name}/form", timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            print(f"Tool: {data['toolName']}")
            print("Fields:")
            for field in data['fields']:
                req = "*" if field['required'] else ""
                print(f"  - {field['name']}{req} ({field['type']}): {field.get('description', 'No desc')}")
            return data
        else:
            print(f"Error fetching schema: {resp.status_code} - {resp.text}")
            return None
    except Exception as e:
        print(f"Exception: {e}")
        return None

def test_booking_flight_search():
    tool_name = "Search_flights"
    schema = get_tool_schema(tool_name)
    
    if not schema:
        return

    print(f"\n--- Executing {tool_name} ---")
    
    # Try with AIRPORT.CODE format which is common for Booking.com flight APIs
    args = {
        "fromId": "LHR.AIRPORT", 
        "toId": "JFK.AIRPORT",
        "departDate": "2026-04-20",
        "adults": 1,
        "cabinClass": "ECONOMY",
        "currency_code": "USD",
        "locale": "en-US"
    }
    
    try:
        r_exec = httpx.post(
            f"{BASE_URL}/{tool_name}/execute",
            json=args,
            timeout=90
        )
        print(f"Status: {r_exec.status_code}")
        if r_exec.status_code == 200:
            result = r_exec.json()
            # print(json.dumps(result, indent=2)[:500])
            if result.get('success'):
                res_text = result['result'][0]['text']
                print(f"Result text preview: {res_text[:500]}")
            else:
                 print(f"Failed: {result}")
        else:
            print(f"Error: {r_exec.text}")
    except Exception as e:
        print(f"Exec Exception: {e}")

if __name__ == "__main__":
    test_booking_flight_search()
