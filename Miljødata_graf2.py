import json
import pandas as pd
import matplotlib.pyplot as plt

# Les inn JSON-filen
with open("miljødata.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Ekstraher tidspunkter og værparametere
times = []
temps = []
wind_speeds = []
precipitations = []

for entry in data["properties"]["timeseries"]:
    times.append(entry["time"])
    
    details = entry["data"]["instant"]["details"]
    temps.append(details.get("air_temperature", None))
    wind_speeds.append(details.get("wind_speed", None))
    precipitations.append(entry["data"].get("next_1_hours", {}).get("details", {}).get("precipitation_amount", 0))

# Opprett DataFrame
df = pd.DataFrame({
    "Time": pd.to_datetime(times),
    "Temperature (°C)": temps,
    "Wind Speed (m/s)": wind_speeds,
    "Precipitation (mm)": precipitations
})

# Sorter etter tid
df = df.sort_values("Time")

# Opprett figur med 3 separate grafer
fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(10, 12), sharex=True)

# Temperatur-plot
axes[0].plot(df["Time"], df["Temperature (°C)"], marker="o", linestyle="-", color="b")
axes[0].set_ylabel("Temperatur (°C)")
axes[0].set_title("Temperaturutvikling i Trondheim")
axes[0].grid()

# Vindhastighet-plot
axes[1].plot(df["Time"], df["Wind Speed (m/s)"], marker="s", linestyle="--", color="g")
axes[1].set_ylabel("Vindhastighet (m/s)")
axes[1].set_title("Vindhastighet i Trondheim")
axes[1].grid()

# Nedbør-plot
axes[2].plot(df["Time"], df["Precipitation (mm)"], marker="^", linestyle=":", color="c")
axes[2].set_ylabel("Nedbør (mm)")
axes[2].set_title("Nedbør i Trondheim")
axes[2].set_xlabel("Tid")
axes[2].grid()

# Rotér x-aksen for bedre lesbarhet
plt.xticks(rotation=45)

# Juster mellomrom mellom plott
plt.tight_layout()

# Vis grafer
plt.show()

# Skriv ut første 10 rader for å vise data
print(df.head(10))
