import json
import pandas as pd
import os

input_path = "data/bronze/bundesliga/season_2024/players.json"

with open(input_path, "r", encoding="utf-8") as f:
    players = json.load(f)

print(type(players))
print(len(players))
#print(players[0])


all_players = []
for player in players:
    silver_player = {
        "player_id": player["player"]["id"],
        "name": player["player"]["name"],
        "age": player["player"]["age"],
        "nationality":player["player"]["nationality"],
        "team":player["statistics"][0]["team"]["name"],
        "position":player["statistics"][0]["games"]["position"],
        "appearances": player["statistics"][0]["games"]["appearences"],
        "lineups": player["statistics"][0]["games"]["lineups"],
        "minutes": player["statistics"][0]["games"]["minutes"],
        "rating": player["statistics"][0]["games"]["rating"],

        "shots_total": player["statistics"][0]["shots"]["total"],
        "shots_on": player["statistics"][0]["shots"]["on"],

        "goals": player["statistics"][0]["goals"]["total"],
        "assists": player["statistics"][0]["goals"]["assists"],

        "passes_total": player["statistics"][0]["passes"]["total"],
        "key_passes": player["statistics"][0]["passes"]["key"],
        "pass_accuracy": player["statistics"][0]["passes"]["accuracy"],

        "tackles": player["statistics"][0]["tackles"]["total"],
        "blocks": player["statistics"][0]["tackles"]["blocks"],
        "interceptions": player["statistics"][0]["tackles"]["interceptions"],

        "duels_total": player["statistics"][0]["duels"]["total"],
        "duels_won": player["statistics"][0]["duels"]["won"],

        "dribbles_attempts": player["statistics"][0]["dribbles"]["attempts"],
        "dribbles_success": player["statistics"][0]["dribbles"]["success"],

        "fouls_drawn": player["statistics"][0]["fouls"]["drawn"],
        "fouls_committed": player["statistics"][0]["fouls"]["committed"],

        "yellow_cards": player["statistics"][0]["cards"]["yellow"],
        "red_cards": player["statistics"][0]["cards"]["red"]
    }
    
    all_players.append(silver_player)

df = pd.DataFrame(all_players)

output_path = "data/silver/bundesliga/season_2024/players.parquet"

os.makedirs(
    os.path.dirname(output_path),
    exist_ok=True
)

df.to_parquet(
    output_path,
    index=False
)

print(f"Silver gespeichert: {output_path}")