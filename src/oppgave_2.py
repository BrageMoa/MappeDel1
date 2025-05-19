import requests
import json

url = "https://api.met.no/weatherapi/locationforecast/2.0/compact"
params = {"lat": 63.42, "lon": 10.39}  # Koordinater for Trondheim
headers = {"User-Agent": "Trø-IT Miljødataanalyse v1.0"}

try:
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()  # Kaster en feil hvis statuskode er 4xx eller 5xx
    data = response.json()

    with open("data/miljodata.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

except requests.exceptions.RequestException as e:
    print(f"API-forespørsel feilet: {e}")
    data = None

if data:
    try:
        with open("data/miljodata.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        print(json.dumps(data, indent=4))  # Formaterer JSON-data pent

        temps = [entry["data"]["instant"]["details"]["air_temperature"]
                 for entry in data["properties"]["timeseries"]]

        print(temps[:10])  # Viser de 10 første temperaturverdiene

    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Feil ved lesing av JSON-fil: {e}")

