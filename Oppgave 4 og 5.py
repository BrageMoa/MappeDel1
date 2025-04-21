import json
import matplotlib.pyplot as plt
import seaborn as sns 
from datetime import datetime
import numpy as np

# Laster inn værdata fra JSON-fil
with open('miljødata.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Henter ut timeserien
timeseries = data['properties']['timeseries']

# Lager lister for tid, temperatur og trykk
time_list = []
temperature_list = []
pressure_list = []

for entry in timeseries:
    time_str = entry['time']
    time = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
    details = entry['data']['instant']['details']

    temp = details.get('air_temperature')
    press = details.get('air_pressure_at_sea_level')

    if temp is not None and press is not None:
        time_list.append(time)
        temperature_list.append(temp)
        pressure_list.append(press)

# Beregner statistikk
temp_mean = np.mean(temperature_list)
temp_median = np.median(temperature_list)
temp_std = np.std(temperature_list)

press_mean = np.mean(pressure_list)
press_median = np.median(pressure_list)
press_std = np.std(pressure_list)

# Viser statistikk i eget vindu
stats_text = (
    " Temperatur:\n"
    f"  Gjennomsnitt: {temp_mean:.2f} °C\n"
    f"  Median:       {temp_median:.2f} °C\n"
    f"  Standardavvik:{temp_std:.2f} °C\n\n"
    "🔵 Lufttrykk:\n"
    f"  Gjennomsnitt: {press_mean:.2f} hPa\n"
    f"  Median:       {press_median:.2f} hPa\n"
    f"  Standardavvik:{press_std:.2f} hPa"
)

# Lager en figur kun for tekst
fig_stats = plt.figure(figsize=(6, 4))
plt.axis('off')  # Fjern akser
plt.text(0.01, 0.99, stats_text, ha='left', va='top', fontsize=12, family='monospace')
plt.title("Statistikk for temperatur og lufttrykk", fontsize=14)
plt.tight_layout()

# Lager grafen for temperatur og trykk (vanlig Matplotlib)
fig, ax1 = plt.subplots(figsize=(10, 6))

ax1.set_xlabel('Tid')
ax1.set_ylabel('Temperatur (°C)', color='tab:red')
ax1.plot(time_list, temperature_list, color='tab:red', label='Temperatur')
ax1.tick_params(axis='y', labelcolor='tab:red')

ax2 = ax1.twinx()
ax2.set_ylabel('Lufttrykk (hPa)', color='tab:blue')
ax2.plot(time_list, pressure_list, color='tab:blue', label='Lufttrykk')
ax2.tick_params(axis='y', labelcolor='tab:blue')

plt.title('Temperatur og lufttrykk over tid')
fig.autofmt_xdate()
plt.grid(True)
plt.tight_layout()

# Lager en separat figur for Seaborn-grafen
sns.set_theme(style="whitegrid")  # Pent tema
plt.figure(figsize=(10, 6))
sns.lineplot(x=time_list, y=temperature_list, color='crimson')
plt.title('Temperaturmålinger over tid (Seaborn)')
plt.xlabel('Tid')
plt.ylabel('Temperatur (°C)')
plt.xticks(rotation=45)
plt.tight_layout()

# Vis alle plottene
plt.show()
