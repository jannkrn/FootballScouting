import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()


#Config
api_key = os.getenv("API_FOOTBALL_KEY")
url = "https://v3.football.api-sports.io/players"
headers = {"x-apisports-key": api_key}
output_path = "data/bronze/bundesliga/season_2024/players.json"

os.makedirs(
    os.path.dirname(output_path),
    exist_ok=True
)


#78 -> Bundesliga
page = 1
bundesliga_players_24 = []
success = True

while True:

    params = {"league": 78, "season": 2024, "page":page}

    response = requests.get(
    url,
    headers=headers,
    params=params
    )

    response.raise_for_status()

    data = response.json()

    if data["errors"]:
        print(data["errors"])
        success = False
        break

    bundesliga_players_24.extend(data["response"])

    print(f"Seite {page} geladen.")

    if page >= data["paging"]["total"]:
        break 

    page += 1 

print(f"Spieleranzahl= {len(bundesliga_players_24)}")

if success == True:
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(
            bundesliga_players_24,
            f,
            ensure_ascii=False,
            indent=4
        ) 
#print("JSON geladen")