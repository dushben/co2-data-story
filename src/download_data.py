# Step 1: Download the raw CO2 dataset from Our World in Data's GitHub

import os
import requests

url = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"
out_path = "data/raw/owid-co2-data.csv"

os.makedirs("data/raw", exist_ok=True)

response = requests.get(url)
print("Status code:", response.status_code)

with open(out_path, "wb") as f:
    f.write(response.content)

print("Saved raw data to", out_path)
