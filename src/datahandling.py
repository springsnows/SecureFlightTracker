# this is for handling and simplifying data required by the app
# left for documenting purposes

import pandas as pd

df = pd.read_csv("data/airports.dat.txt", header=None)
df.columns = [
    "id", "name", "city", "country", "iata", "icao",
    "lat", "lon", "alt", "timezone", "dst", "tz", "type", "source"
]

# Drop rows with missing ICAO codes
df = df[df["icao"].notnull() & (df["icao"] != "\\N")]

# Keep only needed columns
airport_data = df[["icao", "name", "lat", "lon"]]

# Save to JSON using ICAO as key
airport_data.set_index("icao").to_json("data/airports.json", orient="index")
