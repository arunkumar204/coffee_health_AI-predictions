import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os

# ------------------------
# Load dataset
# ------------------------
df = pd.read_csv('../data/coffee_health_dataset.csv')  # adjust path if needed

# ------------------------
# Handle missing values
# ------------------------
# Numeric columns → fill with mean
numeric_cols = df.select_dtypes(include=['number']).columns
df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

# Non-numeric columns → fill with mode
non_numeric_cols = df.select_dtypes(exclude=['number']).columns
for col in non_numeric_cols:
    df[col].fillna(df[col].mode()[0], inplace=True)

# ------------------------
# Feature selection
# ------------------------
features = ['coffee_cups_per_day', 'caffeine_mg', 'age', 'body_weight_kg',
            'exercise_minutes', 'water_intake_liters', 'sleep_hours']
target = 'stress_level'

X = df[features]
y = df[target]

# ------------------------
# Split data
# ------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ------------------------
# Scale features
# ------------------------
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ------------------------
# Train model
# ------------------------
model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10)
model.fit(X_train_scaled, y_train)

# ------------------------
# Evaluate
# ------------------------
y_pred = model.predict(X_test_scaled)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print(f"Model RMSE: {rmse:.4f}")
print(f"Model R² Score: {r2:.4f}")

# ------------------------
# Save model, scaler, and features
# ------------------------
os.makedirs('saved_model', exist_ok=True)
joblib.dump(model, 'saved_model/model.pkl')
joblib.dump(scaler, 'saved_model/scaler.pkl')
joblib.dump(features, 'saved_model/features.pkl')

print("Model, scaler, and features saved in 'saved_model/' folder!")
