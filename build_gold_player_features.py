import pandas as pd

silver_path = "data/silver/bundesliga/season_2024/players.parquet"

df = pd.read_parquet(silver_path)

print("Shape:")
print(df.shape)

print("\nDatentypen:")
print(df.dtypes)

print("\nNULL-Werte:")
print(df.isna().sum())

print("\nDoppelte player_id:")
print(df["player_id"].duplicated().sum())

print("\nMin/Max Minuten:")
print(df["minutes"].min(), df["minutes"].max())

print("\nPositionen:")
print(df["position"].value_counts())


count_columns = [
    "shots_total",
    "shots_on",
    "goals",
    "assists",
    "passes_total",
    "key_passes",
    "tackles",
    "blocks",
    "interceptions",
    "duels_total",
    "duels_won",
    "dribbles_attempts",
    "dribbles_success",
    "fouls_drawn",
    "fouls_committed"
]

df[count_columns] = df[count_columns].fillna(0)

df["rating"] = pd.to_numeric(
    df["rating"],
    errors="coerce"
)



df["position"] = df["position"].replace({
    "Forward": "Attacker"
})

print(df["position"].value_counts())

df = df[df["minutes"]>= 500].copy()

df["goals_per_90"] = df["goals"]/df["minutes"] * 90

df["assists_per_90"] = (
    df["assists"] / df["minutes"] * 90
)

df["tackles_per_90"] = (
    df["tackles"] / df["minutes"] * 90
)

df["interceptions_per_90"] = (
    df["interceptions"] / df["minutes"] * 90
)

df["duels_won_per_90"] = (df["duels_won"] / df["minutes"] * 90)

df["dribbles_success_per_90"] = df["dribbles_success"] / df["minutes"] * 90

df["shots_per_90"] = df["shots_total"] / df["minutes"] * 90

df["key_passes_per_90"] = df["key_passes"] / df["minutes"] * 90

gold_path = "data/gold/bundesliga/season_2024/players_features.parquet"

import os

os.makedirs(
    os.path.dirname(gold_path),
    exist_ok=True
)

df.to_parquet(
    gold_path,
    index=False
)