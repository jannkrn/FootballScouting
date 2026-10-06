from pathlib import Path

import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler


gold_dir = Path("data/gold/bundesliga/season_2024")
input_path = gold_dir / "players_features.parquet"
output_path = gold_dir / "similar_players.parquet"
features_path = gold_dir / "player_features_for_similarity.parquet"

features = [
    "goals_per_90",
    "assists_per_90",
    "shots_per_90",
    "key_passes_per_90",
    "tackles_per_90",
    "interceptions_per_90",
    "duels_won_per_90",
    "dribbles_success_per_90",
]


df = pd.read_parquet(input_path)
df = df.dropna(subset=["name"]).copy()

df[features] = df[features].fillna(0)

feature_table = pd.DataFrame({"feature": features})
feature_table.to_parquet(features_path, index=False)

X = df[features]
X_scaled = StandardScaler().fit_transform(X)

neighbors = min(len(df), 6)
model = NearestNeighbors(n_neighbors=neighbors, metric="cosine")
model.fit(X_scaled)

cosine_distances, indices = model.kneighbors(X_scaled)

result_rows = []
for player_index, target_player in enumerate(df["name"]):
    similar_indices = indices[player_index][1:neighbors]
    similarity_scores = (1 - cosine_distances[player_index][1:neighbors]) * 100
    similar_names = df.iloc[similar_indices]["name"].tolist()

    for rank, (similar_player, similarity) in enumerate(
        zip(similar_names, similarity_scores), start=1
    ):
        result_rows.append(
            {
                "target_player": target_player,
                "similar_player": similar_player,
                "rank": rank,
                "similarity_percentage": similarity,
            }
        )

result = pd.DataFrame(result_rows, columns=[
    "target_player",
    "similar_player",
    "rank",
    "similarity_percentage",
])
output_path.parent.mkdir(parents=True, exist_ok=True)
result.to_parquet(output_path, index=False)

print(f"Ähnliche Spieler gespeichert: {output_path}")
print(result.head(10))