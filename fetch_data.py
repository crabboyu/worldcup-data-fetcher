import json
import requests
from datetime import datetime, timezone, timedelta

def get_hk_time():
    return datetime.now(timezone(timedelta(hours=8)))

def fetch_espn_scoreboard():
    # ESPN 2026 世界杯赛事实时数据接口 (基于已知公开端点)
    url = "https://site.api.espn.com/apis/site/v2/sports/soccer/fifa.worldcup/scoreboard"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        return data
    except Exception as e:
        print(f"Error fetching ESPN data: {e}")
        return None

def parse_matches(espn_data):
    matches = []
    if not espn_data or 'events' not in espn_data:
        return matches
    for event in espn_data.get('events', []):
        try:
            competitions = event.get('competitions', [])
            if not competitions:
                continue
            comp = competitions[0]
            competitors = comp.get('competitors', [])
            if len(competitors) < 2:
                continue
            home = competitors[0].get('team', {}).get('displayName', 'Unknown')
            away = competitors[1].get('team', {}).get('displayName', 'Unknown')
            home_score = competitors[0].get('score')
            away_score = competitors[1].get('score')
            status = event.get('status', {}).get('type', {}).get('description', 'Unknown')
            venue = comp.get('venue', {}).get('fullName', 'Unknown')
            date = event.get('date', 'Unknown')
            matches.append({
                "home_team": home,
                "away_team": away,
                "home_score": home_score,
                "away_score": away_score,
                "status": status,
                "venue": venue,
                "date": date
            })
        except Exception as e:
            print(f"Parse error for event: {e}")
            continue
    return matches

def main():
    print("Fetching World Cup data from ESPN...")
    espn_data = fetch_espn_scoreboard()
    if espn_data is None:
        print("Failed to fetch data, using empty dataset.")
        matches = []
    else:
        matches = parse_matches(espn_data)
        print(f"Found {len(matches)} matches")
    
    output = {
        "last_updated": get_hk_time().strftime("%Y-%m-%d %H:%M:%S"),
        "matches": matches,
        "source": "ESPN (via site.api.espn.com)"
    }
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print("data.json saved.")

if __name__ == "__main__":
    main()
          fi
