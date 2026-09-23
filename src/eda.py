# Step 4: Exploratory data analysis + charts for the blog post
# Run from the top folder of the repo: python src/eda.py

import os
import pandas as pd
import matplotlib.pyplot as plt

os.makedirs("figures", exist_ok=True)

BLUE = "#2a78d6"
ORANGE = "#eb6834"
GRAY = "#52514e"

plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False
plt.rcParams["font.size"] = 11

countries = pd.read_csv("data/clean/co2_countries.csv")
df = pd.read_csv("data/clean/co2_features_2023.csv")
groups = pd.read_csv("data/clean/income_groups_2023.csv")

# Leave out tiny countries (< 1 million people) so the per-person rankings
# aren't dominated by very small countries and islands
big = df[df["population"] >= 1_000_000]


def save(name):
    plt.tight_layout()
    plt.savefig(f"figures/{name}.png", dpi=150)
    plt.close()
    print("Saved figures/" + name + ".png")


# ----- Quick look at the data -----
print("Countries in 2023:", len(df))
print("\nSummary of per-person CO2 (tonnes), countries with 1M+ people:")
print(big["co2_per_capita"].describe().round(2))


# ----- Chart 1: Biggest emitters today (total CO2 in 2023) -----
top = df.sort_values("co2", ascending=False).head(10)
print("\nTop 10 emitters in 2023 (share of world %):")
print(top[["country", "share_global_co2"]].round(1).to_string(index=False))

plt.figure(figsize=(8, 5))
plt.barh(top["country"][::-1], top["co2"][::-1] / 1000, color=BLUE)
plt.xlabel("Billion tonnes of CO2")
plt.title("Who emits the most CO2 today? (2023)")
save("1_top_emitters_2023")


# ----- Chart 2: Per person, the ranking looks very different -----
names = ["United States", "China", "India", "Germany", "Brazil", "Nigeria"]
per_person = df[df["country"].isin(names)].sort_values("co2_per_capita")
world_avg = per_person["co2_per_capita"].iloc[0] / per_person["times_world_avg"].iloc[0]
print("\nPer-person CO2 (tonnes):")
print(per_person[["country", "co2_per_capita", "times_world_avg"]].round(2).to_string(index=False))

plt.figure(figsize=(8, 5))
plt.barh(per_person["country"], per_person["co2_per_capita"], color=BLUE)
plt.axvline(world_avg, color=GRAY, linestyle="--", linewidth=1)
plt.text(world_avg + 0.2, 0, f"World average: {world_avg:.1f} t", color=GRAY)
plt.xlabel("Tonnes of CO2 per person")
plt.title("CO2 per person, 2023")
save("2_per_person_2023")


# ----- Chart 3: Historical (cumulative) emissions since 1750 -----
hist = df.sort_values("cumulative_co2", ascending=False).head(10)
print("\nTop 10 historical emitters (share of all CO2 ever, %):")
print(hist[["country", "share_global_cumulative_co2"]].round(1).to_string(index=False))

plt.figure(figsize=(8, 5))
plt.barh(hist["country"][::-1], hist["share_global_cumulative_co2"][::-1], color=BLUE)
plt.xlabel("% of all CO2 emitted since 1750")
plt.title("Who has emitted the most CO2 over history?")
save("3_historical_share")


# ----- Chart 4: US vs China over time -----
us = countries[countries["country"] == "United States"]
china = countries[countries["country"] == "China"]

plt.figure(figsize=(8, 5))
plt.plot(us["year"], us["cumulative_co2"] / 1000, color=BLUE, linewidth=2, label="United States")
plt.plot(china["year"], china["cumulative_co2"] / 1000, color=ORANGE, linewidth=2, label="China")
plt.ylabel("Billion tonnes of CO2 (running total)")
plt.title("Total CO2 emitted so far: the US still leads")
plt.legend(frameon=False)
save("4_us_vs_china_cumulative")


# ----- Chart 5: Income groups - share of people vs share of historical CO2 -----
order = ["High-income countries", "Upper-middle-income countries",
         "Lower-middle-income countries", "Low-income countries"]
groups = groups.set_index("country").loc[order]
labels = ["High", "Upper-middle", "Lower-middle", "Low"]
x = range(len(labels))

plt.figure(figsize=(8, 5))
plt.bar([i - 0.2 for i in x], groups["share_population"], width=0.38, color=BLUE, label="Share of world population")
plt.bar([i + 0.2 for i in x], groups["share_global_cumulative_co2"], width=0.38, color=ORANGE, label="Share of all CO2 ever emitted")
plt.xticks(list(x), labels)
plt.xlabel("Country income group")
plt.ylabel("Percent")
plt.title("Rich countries: 18% of people, 63% of historical CO2")
plt.legend(frameon=False)
save("5_income_groups")


# ----- Chart 6: Trade gap - emissions "imported" through goods -----
trade = big.dropna(subset=["trade_gap_pct"])
trade_names = ["United Kingdom", "France", "Germany", "United States", "Japan",
               "China", "India", "Russia", "South Africa"]
trade = trade[trade["country"].isin(trade_names)].sort_values("trade_gap_pct")
print("\nTrade gap (% more CO2 from consumption than production):")
print(trade[["country", "trade_gap_pct"]].round(1).to_string(index=False))

colors = [ORANGE if v > 0 else BLUE for v in trade["trade_gap_pct"]]
plt.figure(figsize=(8, 5))
plt.barh(trade["country"], trade["trade_gap_pct"], color=colors)
plt.axvline(0, color=GRAY, linewidth=1)
plt.xlabel("<-- exports emissions (makes goods for others)    |    imports emissions (buys goods made abroad) -->\n% difference between consumption and production CO2", fontsize=9)
plt.title("Does a country consume more CO2 than it produces? (2023)")
save("6_trade_gap")


# ----- Fair share ratio: who's furthest above/below their share -----
fair = big.dropna(subset=["fair_share_ratio"]).sort_values("fair_share_ratio", ascending=False)
print("\nHighest fair share ratio (historical CO2 share / population share):")
print(fair[["country", "fair_share_ratio"]].head(8).round(1).to_string(index=False))
print("\nFair share ratio for big countries:")
print(fair[fair["country"].isin(names)][["country", "fair_share_ratio"]].round(2).to_string(index=False))
