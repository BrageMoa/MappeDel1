import unittest
import json
import os
import pandas as pd
import requests

class TestWeatherData(unittest.TestCase):

    def setUp(self):
        # Vi setter opp testmiljøet ved å hente data og lagre det som JSON.
        self.url = "https://api.met.no/weatherapi/locationforecast/2.0/compact"
        self.params = {"lat": 63.42, "lon": 10.39}  
        self.headers = {"User-Agent": "Trø-IT Miljødataanalyse v1.0"}  
        self.filename = "test_miljødata.json"

        try:
            response = requests.get(self.url, params=self.params, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except requests.exceptions.RequestException as e:
            self.fail(f"API-forespørsel feilet: {e}")

    def test_json_file_exists(self):
        # Så tester vi om JSON-filen ble lagret.
        self.assertTrue(os.path.exists(self.filename), "JSON-filen ble ikke opprettet")

    def test_json_readable(self):
        # Her tester vi om JSON-filen kan leses uten feil.
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertIsInstance(data, dict, "JSON-data er ikke et dictionary")
        except Exception as e:
            self.fail(f"Feil ved lesing av JSON-fil: {e}")

    def test_dataframe_columns(self):
        # Tester om DataFrame inneholder forventede kolonner.
        with open(self.filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        times, temps, wind_speeds, precipitations = [], [], [], []

        for entry in data["properties"]["timeseries"]:
            times.append(entry["time"])
            details = entry["data"]["instant"]["details"]
            temps.append(details.get("air_temperature", None))
            wind_speeds.append(details.get("wind_speed", None))
            precipitations.append(entry["data"].get("next_1_hours", {}).get("details", {}).get("precipitation_amount", 0))

        df = pd.DataFrame({
            "Time": pd.to_datetime(times),
            "Temperature (°C)": temps,
            "Wind Speed (m/s)": wind_speeds,
            "Precipitation (mm)": precipitations
        })

        expected_columns = ["Time", "Temperature (°C)", "Wind Speed (m/s)", "Precipitation (mm)"]
        self.assertListEqual(list(df.columns), expected_columns, "DataFrame har ikke riktige kolonner")

    def tearDown(self):
        # Til slutt rydder vi opp etter testene ved å slette JSON-filen.
        if os.path.exists(self.filename):
            os.remove(self.filename)

if __name__ == "_main_":
    unittest.main()