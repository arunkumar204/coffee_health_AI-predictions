import pandas as pd
import numpy as np

np.random.seed(42)

data = {
    'coffee_cups_per_day': np.random.uniform(0, 10, 10000),
    'caffeine_mg': np.random.uniform(0, 1000, 10000),
    'age': np.random.randint(18, 80, 10000),
    'body_weight_kg': np.random.uniform(50, 120, 10000),
    'exercise_minutes': np.random.uniform(0, 300, 10000),
    'water_intake_liters': np.random.uniform(0, 5, 10000),
    'sleep_hours': np.random.uniform(4, 12, 10000),
    'stress_level': np.random.uniform(1, 10, 10000),
    'heart_rate': np.random.uniform(60, 120, 10000),
    'sleep_quality': np.random.uniform(1, 10, 10000),
}

df = pd.DataFrame(data)

# Create relationships between features
df['caffeine_per_kg'] = df['caffeine_mg'] / df['body_weight_kg']
df['stress_level'] = df['stress_level'] + (df['coffee_cups_per_day'] * 0.5)
df['sleep_quality'] = 10 - (df['stress_level'] * 0.3) - (df['caffeine_mg'] / 100)
df['heart_rate'] = 60 + (df['coffee_cups_per_day'] * 5) + (df['stress_level'] * 2)

# Clip values to valid ranges
df['stress_level'] = df['stress_level'].clip(1, 10)
df['sleep_quality'] = df['sleep_quality'].clip(1, 10)
df['heart_rate'] = df['heart_rate'].clip(60, 150)

df.to_csv('coffee_health_dataset.csv', index=False)
print("Dataset generated successfully!")