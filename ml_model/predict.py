import pandas as pd
import numpy as np
import joblib
import os

# ------------------------
# Absolute paths based on script location
# ------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # ml_model folder
MODEL_PATH = os.path.join(BASE_DIR, 'saved_model', 'model.pkl')
SCALER_PATH = os.path.join(BASE_DIR, 'saved_model', 'scaler.pkl')
FEATURES_PATH = os.path.join(BASE_DIR, 'saved_model', 'features.pkl')

# Check if files exist
for path in [MODEL_PATH, SCALER_PATH, FEATURES_PATH]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}. Make sure train_model.py has been run.")

# Load model, scaler, and features
model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
features = joblib.load(FEATURES_PATH)

# ------------------------
# Helper functions
# ------------------------
def preprocess_input(input_df):
    """Ensure input has all required features, extra columns are ignored, missing columns filled with 0."""
    input_df = input_df.reindex(columns=features, fill_value=0)
    return scaler.transform(input_df)

def predict_stress(input_data):
    """
    Predict stress level.

    input_data: dict or pandas DataFrame
    """
    if isinstance(input_data, dict):
        df = pd.DataFrame([input_data])
    elif isinstance(input_data, pd.DataFrame):
        df = input_data.copy()
    else:
        raise ValueError("Input must be a dictionary or a pandas DataFrame.")

    X_scaled = preprocess_input(df)
    predictions = model.predict(X_scaled)
    return predictions

def predict_from_csv(csv_path, output_path=None):
    """Predict stress levels for all rows in a CSV file."""
    df = pd.read_csv(csv_path)
    predictions = predict_stress(df)
    df['predicted_stress_level'] = predictions

    if output_path:
        df.to_csv(output_path, index=False)
        print(f"Predictions saved to {output_path}")

    return df

# ------------------------
# Example usage
# ------------------------
if __name__ == "__main__":
    # Single input example
    single_input = {
        'coffee_cups_per_day': 3,
        'caffeine_mg': 200,
        'age': 30,
        'body_weight_kg': 70,
        'exercise_minutes': 40,
        'water_intake_liters': 2,
        'sleep_hours': 7
    }
    pred = predict_stress(single_input)
    print(f"Predicted Stress Level (single input): {pred[0]:.2f}")

    # Batch CSV example
    csv_input = os.path.join(BASE_DIR, '../data/coffee_health_dataset.csv')  # adjust if needed
    output_csv = os.path.join(BASE_DIR, '../data/coffee_health_predictions.csv')
    df_with_pred = predict_from_csv(csv_input, output_csv)
