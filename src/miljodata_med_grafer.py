import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Her endrer vi stilen i grafene
sns.set_theme(style="darkgrid")

# Vi leser inn JSON-filen "miljodata.json" som inneholder dataene fra API-en
with open("data/miljodata.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Vi tar ut de tidspunktene og værparameterene fra JSON-fil dataene som vi øsnker å fremvise
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

# Vi lager en DataFrame
df = pd.DataFrame({
    "Time": pd.to_datetime(times),
    "Temperature (°C)": temps,
    "Wind Speed (m/s)": wind_speeds,
    "Precipitation (mm)": precipitations
})

df = df.sort_values("Time")

# Her setter vi opp en figur med 3 separate grafer
fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(12, 10), sharex=True)

# Dette er kun for å legge til fargevalg
colors = sns.color_palette("viridis", 3)

# Her setter vi opp temperatur-grafen
axes[0].plot(df["Time"], df["Temperature (°C)"], marker="o", linestyle="-", color=colors[0], linewidth=2)
axes[0].fill_between(df["Time"], df["Temperature (°C)"], alpha=0.2, color=colors[0])
axes[0].set_ylabel("Temperatur (°C)", fontsize=12)
axes[0].set_title("Temperaturutvikling i Trondheim", fontsize=14, fontweight="bold")
axes[0].grid(True, linestyle="--", alpha=0.6)

# Her setter vi opp vindhastighets-grafen
axes[1].plot(df["Time"], df["Wind Speed (m/s)"], marker="s", linestyle="--", color=colors[1], linewidth=2)
axes[1].fill_between(df["Time"], df["Wind Speed (m/s)"], alpha=0.2, color=colors[1])
axes[1].set_ylabel("Vindhastighet (m/s)", fontsize=12)
axes[1].set_title("Vindhastighet i Trondheim", fontsize=14, fontweight="bold")
axes[1].grid(True, linestyle="--", alpha=0.6)

# Her setter vi opp nedbørs-grafen
axes[2].plot(df["Time"], df["Precipitation (mm)"], marker="^", linestyle=":", color=colors[2], linewidth=2)
axes[2].fill_between(df["Time"], df["Precipitation (mm)"], alpha=0.2, color=colors[2])
axes[2].set_ylabel("Nedbør (mm)", fontsize=12)
axes[2].set_title("Nedbør i Trondheim", fontsize=14, fontweight="bold")
axes[2].set_xlabel("Tid", fontsize=12)
axes[2].grid(True, linestyle="--", alpha=0.6)

# Forbedre lesbarheten av datoene under x-aksen ved å endre oppstllingen
plt.xticks(rotation=30, ha="right", fontsize=10)

# Vi justerer mellomrom mellom plott
plt.tight_layout()

# Nå viser vi grafene
plt.show()
