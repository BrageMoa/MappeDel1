import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# Laster inn JSON-data
data = pd.read_json('data/miljodata.json')

# Trekker ut timeseriedata
timeseries = data.loc['timeseries', 'properties']
timeseries_df = pd.DataFrame(timeseries)

# Pakker ut måleverdier
data_values = pd.json_normalize(timeseries_df['data'])

# Kombinerer tidspunkter og måledata
full_data = pd.concat([timeseries_df['time'], data_values], axis=1)

# Gir kolonnene enkle navn
full_data.rename(columns={
    'instant.details.air_temperature': 'temperatur',
    'instant.details.relative_humidity': 'luftfuktighet'
}, inplace=True)

# Sjekker datasettet
print(full_data.head())

# Håndterer manglende verdier
full_data.dropna(subset=['temperatur', 'luftfuktighet'], inplace=True)

# Velger input og output for regresjon
X = full_data[['temperatur']]  # uavhengig variabel
y = full_data['luftfuktighet']  # avhengig variabel

# Deler opp i trenings- og testsett
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

# Lager prediksjoner
y_pred = model.predict(X_test)

print(f"Mean Squared Error (MSE): {mean_squared_error(y_test, y_pred):.2f}")
print(f"R-squared (R2 score): {r2_score(y_test, y_pred):.2f}")

# Scatterplot med regresjonslinje
plt.figure(figsize=(8, 6))
sns.scatterplot(x=X_test['temperatur'], y=y_test, label='Ekte data')
sns.lineplot(x=X_test['temperatur'], y=y_pred, color='red', label='Predikert')
plt.title('Scatterplot: Temperatur vs Luftfuktighet')
plt.xlabel('Temperatur (°C)')
plt.ylabel('Luftfuktighet (%)')
plt.legend()
plt.grid(True)
plt.show()

# Søylediagram Faktiske vs Predikerte verdier
plt.figure(figsize=(10, 6))
width = 0.4
indices = np.arange(len(y_test))
plt.bar(indices, y_test, width=width, label='Ekte')
plt.bar(indices + width, y_pred, width=width, label='Predikert')
plt.title('Sammenligning av Faktiske og Predikerte Luftfuktighet')
plt.xlabel('Indeks')
plt.ylabel('Luftfuktighet (%)')
plt.legend()
plt.show()

# Linjediagram over tid (hvis tid finnes)
full_data['time'] = pd.to_datetime(full_data['time'])
full_data.sort_values('time', inplace=True)

plt.figure(figsize=(12, 6))
plt.plot(full_data['time'], full_data['temperatur'], label='Temperatur')
plt.plot(full_data['time'], full_data['luftfuktighet'], label='Luftfuktighet')
plt.title('Temperatur og Luftfuktighet over Tid')
plt.xlabel('Tid')
plt.ylabel('Verdi')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Demonstrasjon: Manglende verdier-effekt
full_data_missing = full_data.copy()
full_data_missing.loc[::10, 'temperatur'] = np.nan

plt.figure(figsize=(12, 6))
plt.plot(full_data_missing['time'], full_data_missing['temperatur'], label='Temperatur med manglende verdier', color='orange')
plt.title('Temperatur med Simulerte Manglende Verdier')
plt.xlabel('Tid')
plt.ylabel('Temperatur (°C)')
plt.legend()
plt.grid(True)
plt.show()