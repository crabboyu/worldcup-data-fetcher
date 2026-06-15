import json
import requests
from datetime import datetime

# FIFA World Cup 2026 data endpoint
API_URL = "https://worldcup-api.herokuapp.com"

def fetch_world_cup_data():
    """Fetch World Cup matches data from public API"""
    try:
        # Fetch all matches
        response = requests.get(f"{API_URL}/matches", timeout=10)
        response.raise_for_status()
        
        matches = response.json()
        
        # Parse and format the data
        data = {
            "updated_at": datetime.now().isoformat(),
            "matches": matches,
            "total_matches": len(matches)
        }
        
        return data
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching World Cup data: {e}")
        return None

def save_data(data, filename="data.json"):
    """Save data to JSON file"""
    if data:
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Data successfully saved to {filename}")
            return True
        except IOError as e:
            print(f"Error saving data to {filename}: {e}")
            return False
    return False

if __name__ == "__main__":
    print("Fetching World Cup 2026 data...")
    data = fetch_world_cup_data()
    
    if data:
        save_data(data)
        print("✓ World Cup data fetch completed successfully")
    else:
        print("✗ Failed to fetch World Cup data")
