import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# Step 1: Load datasets
# Replace 'rainfall_data.csv' with actual dataset file path
# Assume columns: ['elevation', 'rainfall']
data = pd.read_csv('rainfall_data.csv')

# Step 2: Feature engineering
# Add orographic effect
data['orographic_effect'] = data['elevation'] * 0.002  # Simplified

# Define features (X) and target (y)
X = data[['elevation','orographic_effect']]
y = data['rainfall']

# Step 3: Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 4: Train Random Forest Model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Step 5: Evaluate Model
y_pred = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print(f"RMSE: {rmse}")
print(f"R^2 Score: {r2}")

# Step 6: Plot predictions
plt.scatter(y_test, y_pred, alpha=0.5)
plt.xlabel('Actual Rainfall')
plt.ylabel('Predicted Rainfall')
plt.title('Actual vs. Predicted Rainfall')
plt.show()

# Predict rainfall for new data
# Replace with future climate data or scenarios
new_data = pd.DataFrame({
    'elevation': [1500, 2000],  # Example elevations
    'orographic_effect': [1500 * 0.002, 2000 * 0.002]
})

future_rainfall = model.predict(new_data)
print("Predicted Rainfall:", future_rainfall)

