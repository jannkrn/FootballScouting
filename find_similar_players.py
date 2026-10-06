from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
import pandas as pd

gold_path = "data/gold/bundesliga/season_2024/players_features.parquet"

df = pd.read_parquet(gold_path)


attackers = df[df["position"] == "Attacker"].copy()

features = [
    "goals_per_90",
    "assists_per_90",
    "shots_per_90",
    "key_passes_per_90",
    "tackles_per_90",
    "interceptions_per_90",
    "duels_won_per_90",
    "dribbles_success_per_90"
]

X = attackers[features]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X) #z = (x - Mittelwert) / Standardabweichung



#print(attackers[["name"] + features])
#print(X_scaled)

model = NearestNeighbors(n_neighbors=5, metric="euclidean") #euklidischer Distanz

model.fit(X_scaled)

target_name = "H. Kane"


attackers_reset = attackers.reset_index(drop=True)

target_position = attackers_reset[
    attackers_reset["name"] == target_name
].index[0]


distances, indices = model.kneighbors(
    [X_scaled[target_position]]
)

for distance, idx in zip(distances[0], indices[0]):
    print(
        attackers_reset.iloc[idx]["name"],
        distance
    )