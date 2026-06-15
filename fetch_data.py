import json
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta

def get_hk_time():
    return datetime.now(timezone(timedelta(hours=8)))

def fetch_espn_scoreboard():
    url = "https://site.api.espn.com/apis/site/v2/sports/soccer/fifa.worldcup/scoreboard"
    headers = {"User-Agent": "Mozilla/5.0"}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            data = response.read().decode('utf-8')
            return json.loads(data)
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def parse_matches(data):
    matches = []
    if not data or 'events' not in data:
        return matches
    for event in data.get('events', []):
        try:
            comp = event.get('competitions', [{}])[0]
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
            print(f"Parse error: {e}")
    return matches

def main():
    print("Fetching World Cup data from ESPN...")
    raw = fetch_espn_scoreboard()
    matches = parse_matches(raw) if raw else []
    print(f"Found {len(matches)} matches")
    output = {
        "last_updated": get_hk_time().strftime("%Y-%m-%d %H:%M:%S"),
        "matches": matches,
        "source": "ESPN (urllib)"
    }
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print("data.json saved")

if __name__ == "__main__":
    main()
