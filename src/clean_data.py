# Step 2: Clean the raw data
# - split real countries from regions/income groups
# - keep only the columns I use
# - keep years from 1850 on (data before that is very sparse)

import pandas as pd

df = pd.read_csv("data/raw/owid-co2-data.csv")
print("Raw shape:", df.shape)

columns = ["country", "year", "iso_code", "population", "gdp",
           "co2", "co2_per_capita", "consumption_co2", "consumption_co2_per_capita",
           "cumulative_co2", "share_global_co2", "share_global_cumulative_co2"]
df = df[columns]
df = df[df["year"] >= 1850]

# Real countries have a 3-letter ISO code. Regions and groups like "World"
# or "High-income countries" have no code (a few use OWID_ codes).
is_country = df["iso_code"].notna() & ~df["iso_code"].str.startswith("OWID", na=False)
countries = df[is_country].copy()

# Keep the World row and the four World Bank income groups
groups_to_keep = ["World", "High-income countries", "Upper-middle-income countries",
                  "Lower-middle-income countries", "Low-income countries"]
groups = df[df["country"].isin(groups_to_keep)].copy()

# Check for missing values in the columns I care about most
print("\nMissing values (countries):")
print(countries[["population", "co2", "consumption_co2"]].isna().sum())

# Drop country-years with no CO2 number at all - nothing to analyze there
countries = countries.dropna(subset=["co2"])

print("\nCountries:", countries["country"].nunique())
print("Years:", countries["year"].min(), "-", countries["year"].max())

countries.to_csv("data/clean/co2_countries.csv", index=False)
groups.to_csv("data/clean/co2_income_groups.csv", index=False)
print("\nSaved cleaned files to data/clean/")
