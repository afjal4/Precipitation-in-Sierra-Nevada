import numpy as np
import pandas as pd

df = pd.read_csv("rock_property_data.csv", usecols=range(0, 5))
df = df.dropna()

df = df[(df['LAT_nad27'] >= 36) & (df['LAT_nad27'] <= 38)]
df = df[(df['LONG_nad27'] >= -120) & (df['LONG_nad27'] <= -118)]


df = df[df['GD_kg_m3'] > df['DBD_kg_m3']]
df = df[df['SBD_kg_m3'] > df['DBD_kg_m3']] 

grain_density = df['GD_kg_m3'].to_numpy()
s_bulk_density = df['SBD_kg_m3'].to_numpy()
dry_bulk_density = df['DBD_kg_m3'].to_numpy()


denom = grain_density - dry_bulk_density
saturation = np.zeros(len(df))
porosity = np.zeros(len(df))
rate_of_detach = np.zeros(len(df))

for b in range(len(df)):
    if denom[b] > 0:
        saturation[b] = (s_bulk_density[b] - dry_bulk_density[b]) / denom[b]
        porosity[b] = (grain_density[b] - dry_bulk_density[b]) / grain_density[b]
        rate_of_detach[b] = saturation[b] * porosity[b] * 0.75

avg_porosity = np.nanmean(porosity)
avg_saturation = np.nanmean(saturation)
avg_rate_of_detach = np.nanmean(rate_of_detach)

print("Avg porosity: ", avg_porosity)
print("Avg saturation: ", avg_saturation)
print("Avg rate of detachability: ", avg_rate_of_detach)
print("Change in distance (per year) due to bombardment: ", avg_rate_of_detach/2.69)
