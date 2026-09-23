# Step 3: Feature engineering
# I focus on 2023 because it's the latest year with consumption-based data.

import pandas as pd

YEAR = 2023

countries = pd.read_csv("data/clean/co2_countries.csv")
groups = pd.read_csv("data/clean/co2_income_groups.csv")

world = groups[(groups["country"] == "World") & (groups["year"] == YEAR)].iloc[0]

df = countries[countries["year"] == YEAR].copy()

# Feature 1: share of the world's population
df["share_population"] = df["population"] / world["population"] * 100

# Feature 2: "fair share ratio" = share of historical CO2 / share of population
# 1 means a country emitted exactly its "fair share" for its size.
# 5 means it emitted 5x more than its share of people.
df["fair_share_ratio"] = df["share_global_cumulative_co2"] / df["share_population"]

# Feature 3: trade gap = how much more (or less) CO2 a country's consumption
# causes compared to what it produces at home, in percent.
# Positive = the country "imports" emissions (goods made elsewhere).
df["trade_gap_pct"] = (df["consumption_co2"] - df["co2"]) / df["co2"] * 100

# Feature 4: how many times the world average per-person emissions
df["times_world_avg"] = df["co2_per_capita"] / world["co2_per_capita"]

df.to_csv("data/clean/co2_features_2023.csv", index=False)
print("Saved data/clean/co2_features_2023.csv with", len(df), "countries")

# Same population vs history comparison for the income groups
g = groups[(groups["year"] == YEAR) & (groups["country"] != "World")].copy()
g["share_population"] = g["population"] / world["population"] * 100
g["fair_share_ratio"] = g["share_global_cumulative_co2"] / g["share_population"]
g.to_csv("data/clean/income_groups_2023.csv", index=False)

print(g[["country", "share_population", "share_global_co2",
         "share_global_cumulative_co2", "fair_share_ratio"]].round(1))
