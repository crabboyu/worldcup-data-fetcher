import json
import os
from datetime import datetime, timezone, timedelta
from sports_skills import football

# 获取香港时区（UTC+8）
def get_hk_time():
    return datetime.now(timezone(timedelta(hours=8)))

# 定义要抓取的数据列表
competitions = [
    ("世界盃 (FIFA World Cup)", "fifa-world-cup"),
    ("世界盃 - 小組賽 (FIFA World Cup - Group Stage)", "fifa-world-cup"),
    ("世界盃 - 淘汰賽 (FIFA World Cup - Knockout Stage)", "fifa-world-cup"),
]

matches_list = []
for league_name, comp_id in competitions:
    try:
        scoreboard = football.get_scoreboard(competition_id=comp_id)
        if scoreboard and "data" in scoreboard and "events" in scoreboard["data"]:
            for event in scoreboard["data"]["events"]:
                match_info = {
                    "league": league_name,
                    "date": event.get("date"),
                    "home_team": event["competitions"][0]["competitors"][0]["team"]["displayName"],
                    "away_team": event["competitions"][0]["competitors"][1]["team"]["displayName"],
                    "home_score": event["competitions"][0]["competitors"][0].get("score"),
                    "away_score": event["competitions"][0]["competitors"][1].get("score"),
                    "status": event["status"]["type"]["description"],
                    "venue": event["competitions"][0]["venue"]["fullName"]
                }
                matches_list.append(match_info)
        else:
            print(f"No matches found for {league_name}")
    except Exception as e:
        print(f"Error fetching {league_name}: {e}")

# 整合所有数据
data = {
    "last_updated": get_hk_time().strftime("%Y-%m-%d %H:%M:%S"),
    "matches": matches_list,
    "source": "ESPN via sports-skills"
}

# 写入 data.json 文件
with open("data.json", "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Data saved at {get_hk_time().strftime('%Y-%m-%d %H:%M:%S')} with {len(matches_list)} matches")
