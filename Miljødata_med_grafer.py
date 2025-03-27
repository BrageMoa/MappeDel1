import requests
import json
import pandas as pd
import matplotlib.pyplot as plt

# API-forespørsel
url = "https://api.met.no/weatherapi/locationforecast/2.0/compact"
headers = {"User-Agent": "Trø-IT Miljødataanalyse v1.0 (contact@example.com)"}

# Brukerdrevet koordinatinntasting
try:
    lat = float(input("Skriv inn breddegrad: "))
    lon = float(input("Skriv inn lengdegrad: "))
except ValueError:
    print("Ugyldige koordinater! Bruk desimaltall.")
    exit()

params = {"lat": lat, "lon": lon}

try:
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    data = response.json()

    with open("miljødata.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

except requests.exceptions.HTTPError as e:
    print(f"HTTP-feil: {e.response.status_code} - {e.response.reason}")
    exit()
except requests.exceptions.ConnectionError:
    print("Tilkoblingsfeil! Sjekk nettverket ditt.")
    exit()
except requests.exceptions.Timeout:
    print("Forespørselen tok for lang tid!")
    exit()
except requests.exceptions.RequestException as e:
    print(f"API-forespørsel feilet: {e}")
    exit()

# Les og behandle JSON-filen
try:
    with open("miljødata.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    if "properties" in data and "timeseries" in data["properties"]:
        timeseries = data["properties"]["timeseries"]
    else:
        print("Feil: Timeseries-data mangler!")
        exit()

    # Ekstraher tidspunkter og værparametere
    times, temps, wind_speeds, precipitations = [], [], [], []
    for entry in timeseries:
        times.append(entry["time"])
        details = entry["data"]["instant"]["details"]
        temps.append(details.get("air_temperature", float('nan')))
        wind_speeds.append(details.get("wind_speed", float('nan')))
        precip = entry["data"].get("next_1_hours", {}).get("details", {}).get("precipitation_amount")
        precipitations.append(float('nan') if precip is None else precip)

    # Opprett DataFrame
    df = pd.DataFrame({
        "Time": pd.to_datetime(times),
        "Temperature (°C)": temps,
        "Wind Speed (m/s)": wind_speeds,
        "Precipitation (mm)": precipitations
    }).sort_values("Time")

    # Plotting
    fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(10, 12), sharex=True)
    axes[0].plot(df["Time"], df["Temperature (°C)"], marker="o", linestyle="-", color="b", label="Temperatur")
    axes[1].plot(df["Time"], df["Wind Speed (m/s)"], marker="s", linestyle="--", color="g", label="Vindhastighet")
    axes[2].plot(df["Time"], df["Precipitation (mm)"], marker="^", linestyle=":", color="c", label="Nedbør")
    
    for ax in axes:
        ax.legend()
        ax.grid()
    
    axes[0].set_ylabel("Temperatur (°C)")
    axes[1].set_ylabel("Vindhastighet (m/s)")
    axes[2].set_ylabel("Nedbør (mm)")
    axes[2].set_xlabel("Tid")
    axes[2].xaxis.set_major_locator(plt.MaxNLocator(nbins=6))
    fig.autofmt_xdate()
    plt.tight_layout()
    plt.savefig("miljødata_plot.png", dpi=300)
    plt.show()

    # Vis første 10 rader
    print(df.head(10))

except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Feil ved lesing av JSON-fil: {e}")
