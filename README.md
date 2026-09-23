# Who's Really Responsible for Climate Change?

AIPI 510 – Module Project 1: Data Storytelling (Ben Dushnitzky)

## Overview

If you ask "who is the biggest polluter?", most people say China. That's true if you only
look at one year. But when you look at CO2 **per person**, over **history**, and include
the emissions from **goods countries buy from other countries**, the picture changes a lot.

This project uses public CO2 data to compare those different ways of measuring
responsibility. The story is written up as a blog post in [`blog_post.md`](blog_post.md).

**Audience:** general readers (students, voters, news readers) who hear about climate
negotiations and want to understand why countries argue about "who should pay."

## Links

- **Blog post:** https://byline.blog/@bendushnitzky/china-is-the-worlds-biggest-polluter-so-why-do-other-countries-say-the-us-should-pay
- **Presentation slides:** https://claude.ai/artifact/V35T6rZ3wgD95mAzT3byVx

## Dataset

- **Source:** Our World in Data, *CO2 and Greenhouse Gas Emissions* dataset
- **Link:** https://github.com/owid/co2-data
- **Citation:** Our World in Data. *CO2 and Greenhouse Gas Emissions* dataset. https://github.com/owid/co2-data (accessed September 2026). Most of the CO2 numbers come from the Global Carbon Project's *Global Carbon Budget*.
- **License:** CC BY 4.0
- **Size:** ~50,000 rows (country × year, 1750–2024), 79 columns

Main columns I use: `co2` (million tonnes per year), `co2_per_capita`, `cumulative_co2`,
`consumption_co2` (emissions from what a country *buys*, including imports),
`population`, and the share-of-world columns.

## Project structure

```
co2-data-story/
├── data/
│   ├── raw/owid-co2-data.csv          # original download
│   └── clean/                         # created by the scripts
├── figures/                           # charts created by eda.py
├── src/
│   ├── download_data.py               # 1. download raw data
│   ├── clean_data.py                  # 2. clean + split countries / income groups
│   ├── features.py                    # 3. feature engineering
│   └── eda.py                         # 4. EDA printouts + charts
├── blog_post.md                       # public-facing blog post
└── presentation_outline.md            # outline for the 8-minute presentation
```

## How to reproduce

From the top folder of the repo:

```bash
pip install -r requirements.txt
python src/download_data.py    # downloads data/raw/owid-co2-data.csv
python src/clean_data.py       # writes data/clean/co2_countries.csv and co2_income_groups.csv
python src/features.py         # writes data/clean/co2_features_2023.csv and income_groups_2023.csv
python src/eda.py              # prints summary tables and saves charts to figures/
```

Note: OWID updates the dataset about once a year, so a fresh download may give slightly
different numbers. The raw file I used (downloaded September 2026) is included in `data/raw/`.

## Preprocessing

- Kept only the columns I need and years from 1850 onward
- Separated real countries (have a 3-letter ISO code) from regions and groups like
  "World" or "High-income countries" so countries aren't double counted
- Dropped country-years with no CO2 value
- Used 2023 as the main year because it is the latest year that has consumption-based data

## Engineered features

| Feature | Formula | What it tells us |
|---|---|---|
| `share_population` | country population / world population | How big a country is |
| `fair_share_ratio` | share of historical CO2 / share of population | Above 1 = emitted more than its "fair share" for its size |
| `trade_gap_pct` | (consumption CO2 − production CO2) / production CO2 | Positive = country "imports" emissions through goods |
| `times_world_avg` | CO2 per person / world CO2 per person | How a typical person compares to the world average |

## Key findings

1. China emits the most CO2 today (32% of the world in 2023), about 2.5x the US.
2. Per person, the average American emits 14.3 tonnes. That's about 3x the world average and 1.7x the average in China.
3. Over history the US has emitted 23.7% of all CO2, the most of any country.
4. High-income countries have 18% of the world's people but emitted 63% of all historical CO2.
   Low-income countries have 9% of people and emitted less than 1%.
5. Rich countries "import" emissions: the UK's consumption footprint is 58% higher than
   what it produces at home, while China, India and South Africa make goods for others.

## Limitations

- Country totals hide inequality **inside** countries (rich vs. poor households).
- Consumption-based numbers are estimates from trade models and only exist for ~120 countries.
- Older data (especially pre-1950) is less reliable.
- Only CO2 from fossil fuels and industry is included, not land use (deforestation) or methane.
- Borders change over time (e.g. the USSR), and historical emissions are assigned to today's countries.
