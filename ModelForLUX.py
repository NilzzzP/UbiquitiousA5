import pandas as pd
#from sklearn.neighbors import KNeighborsRegressor
#from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error
import csv

ValidISOValues = [100, 200, 400, 800, 1600, 3200, 6400]
ValidShutterSpeedValues_String = ["1/1000", "1/500", "1/250", "1/125", "1/60", "1/30", "1/15"]
ValidApertureValues = [2, 2.8, 4, 5.6, 8, 11, 16]
ValidShutterSpeedValues_Decimal = [1/1000, 1/500, 1/250, 1/125, 1/60, 1/30, 1/15]

def round_to_nearest(PredictedValue, ValueList):
    return min(ValueList, key=lambda x: abs(x-PredictedValue))

def decimal_to_fraction(value):
    index = ValidShutterSpeedValues_Decimal.index(value)
    return ValidShutterSpeedValues_String[index]

def fractionToFloat(fraction):
    if '/' in fraction:
        numerator, denominator = fraction.split('/')
        return float(numerator) / float(denominator)
    return float(fraction)


parsedData = []

TextFile = 'Light Sensor Sample Data.txt'
with open(TextFile, 'r') as file:
    
    for line in file :
        parts = line.split(']')

        if len(parts) == 2:
            settings = parts[0]
            lux = parts[1]

            settings = settings.replace('[','')
            settingsList = settings.split(',')

            ISO = float(settingsList[0].strip())
            ShutterSpeed = fractionToFloat(settingsList[1].strip())
            Aperture = float(settingsList[2].strip())

            lux = lux.replace('Light Level:','').replace('lux', '')
            lux = float(lux.strip())

            parsedData.append({
                'lux': lux, 
                'ISO': ISO,
                'ShutterSpeed' : ShutterSpeed,
                'Aperture' : Aperture
            })

df = pd.DataFrame(parsedData)
print("Parsed Data: ")
print(df.head())
print(f"Loaded {len(df)} rows from {TextFile}.")
df = df.drop_duplicates()
print(f"After removing duplicates: {len(df)} rows")

input = df[['lux']]
output = df[['ISO','ShutterSpeed','Aperture']]

input_train, input_test, output_train, output_test = train_test_split(input, output, test_size=0.2, random_state=42)

#knnModel = KNeighborsRegressor(n_neighbors=7)
#treeModel = DecisionTreeRegressor(max_depth = 3, random_state = 42)
forestModel = RandomForestRegressor(n_estimators=150,
                                    max_depth=6,
                                    random_state=42,
                                    min_samples_split=10)

forestModel.fit(input_train, output_train)
print("model trained!")
TestingScore = forestModel.score(input_test, output_test)
TrainingScore = forestModel.score(input_train, output_train)
print(f"model testing accuracy = {TestingScore * 100:.2f}%")
print(f"model training accuracy = {TrainingScore * 100:.2f}%")

test_lux = 200

new_reading = pd.DataFrame({'lux':[test_lux]})

prediction = forestModel.predict(new_reading)

RAWISO = prediction[0][0]
RAWShutterSpeed = prediction[0][1]
RAWAperture = prediction[0][2]

roundedISO = round_to_nearest(RAWISO, ValidISOValues)
roundedShutterSpeed = round_to_nearest(RAWShutterSpeed, ValidShutterSpeedValues_Decimal)
roundedAperture = round_to_nearest(RAWAperture, ValidApertureValues)

roundedShutterSpeed = decimal_to_fraction(roundedShutterSpeed)


print(f"For {test_lux} Lux, settings are: ")
print(f"ISO: {roundedISO}")
print(f"Aperture: {roundedAperture}")
print(f"Shutter Speed: {roundedShutterSpeed}")

# Displaying statistics in graphs

newPrediction = forestModel.predict(input_test)

predictedISO = newPrediction[:,0]
ActualISO = output_test['ISO'].values
LUXValues = input_test['lux'].values

residuals = ActualISO - predictedISO

mae = mean_absolute_error(ActualISO, predictedISO)
rmse = np.sqrt(mean_squared_error(ActualISO, predictedISO))

print("ISO error stats: ")
print(f"Mean Absolute Error: {mae:.1f} ISO points")
print(f"Root Mean Squared Error: {rmse:.1} ISO Points")

# fig, (ax1, ax2) = plt.subplots(1,2,figsize=(14,5))
# ax1.scatter(LUXValues, residuals, color='blue', alpha=0.6, edgecolor = 'black')
# ax1.axhline(y=0, color='red', linestyle='--', linewidth=2)
# ax1.set_title('Residual Plot (errors)')
# ax1.set_xlabel('LUX')
# ax1.set_ylabel('Error (Actual ISO - Predicted ISO)')
# ax1.grid(True, linestyle=':', alpha=0.7)

# ax2.hist(residuals, bins=15, color='orange', edgecolor='black', alpha=0.7)
# ax2.axvline(x=0, color='red', linestyle='--', linewidth=2)
# ax2.set_title('Error Distribution')
# ax2.set_xlabel('Size of error')
# ax2.set_ylabel('Frequency')
# ax2.grid(True, linestyle=':', alpha=0.7)

# plt.tight_layout()
# plt.show()

output_filename = 'LUXSettings.csv'

with open(output_filename,'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['lux','ISO','ShutterSpeed','Aperture'])

    for lux_value in range (1, 2001):
        Reading = pd.DataFrame({'lux': [lux_value]})
        prediction = forestModel.predict(Reading)

        RAWISO = prediction[0][0]
        RAWShutterSpeed = prediction[0][1]
        RAWAperture = prediction[0][2]

        FinalISO = round_to_nearest(RAWISO, ValidISOValues)
        FinalShutterSpeed_Decimal = round_to_nearest(RAWShutterSpeed, ValidShutterSpeedValues_Decimal)
        FinalShutterSpeed_String = decimal_to_fraction(FinalShutterSpeed_Decimal)
        FinalAperture = round_to_nearest(RAWAperture, ValidApertureValues)

        writer.writerow([lux_value, FinalISO, FinalShutterSpeed_String, FinalAperture])
print(f"Success! Wrote exactly 2000 individual rows to {output_filename}.")