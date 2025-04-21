import unittest
import json
import os
import pandas as pd
import requests
import numpy as np

class TestWeatherData(unittest.TestCase):

    def setUp(self):
        # Setter opp testmiljøet ved å hente data fra MET API og lagre som JSON.
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
        # Tester om JSON-filen ble lagret korrekt.
        self.assertTrue(os.path.exists(self.filename), "JSON-filen ble ikke opprettet")

    def test_json_readable(self):
        # Tester om JSON-filen kan leses uten feil.
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

    def test_temperature_statistics(self):
        # Tester beregning av gjennomsnitt, median og standardavvik for temperatur
        sample_temps = [5, 10, 15]
        mean = np.mean(sample_temps)
        median = np.median(sample_temps)
        std = np.std(sample_temps)

        self.assertAlmostEqual(mean, 10.0, places=2, msg="Feil i gjennomsnittsberegning")
        self.assertEqual(median, 10.0, "Feil i medianberegning")
        self.assertAlmostEqual(std, 4.08, places=2, msg="Feil i standardavviksberegning")

    def test_timeseries_not_empty(self):
        # Tester at timeseriedata faktisk inneholder data
        with open(self.filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        timeseries = data["properties"]["timeseries"]
        self.assertGreater(len(timeseries), 0, "Timeseriedata er tom")

    def tearDown(self):
        # Rydder opp etter testene ved å slette JSON-filen.
        if os.path.exists(self.filename):
            os.remove(self.filename)

if __name__ == "__main__":
    unittest.main()
