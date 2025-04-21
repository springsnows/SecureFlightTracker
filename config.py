import pandas as pd

df = pd.read_csv("data/airports.dat.txt", header=None)
df.columns = [
    "id", "name", "city", "country", "iata", "icao",
    "lat", "lon", "alt", "timezone", "dst", "tz", "type", "source"
]

# Drop rows with missing IATA codes
df = df[df["iata"].notnull() & (df["iata"] != "\\N")]

# Keep only needed columns
airport_data = df[["iata", "name", "lat", "lon"]]

airport_data.set_index("iata").to_json("data/airports.json", orient="index")
