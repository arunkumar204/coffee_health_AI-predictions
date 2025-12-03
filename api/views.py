from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import HealthPredictionSerializer
import joblib
import os
import pandas as pd

# Load model, scaler, and features
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # api folder
MODEL_PATH = os.path.join(BASE_DIR, '../ml_model/saved_model/model.pkl')
SCALER_PATH = os.path.join(BASE_DIR, '../ml_model/saved_model/scaler.pkl')
FEATURES_PATH = os.path.join(BASE_DIR, '../ml_model/saved_model/features.pkl')

# Ensure files exist
for path in [MODEL_PATH, SCALER_PATH, FEATURES_PATH]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}. Run train_model.py first.")

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
features = joblib.load(FEATURES_PATH)

class HealthPredictionViewSet(APIView):
    def post(self, request):
        serializer = HealthPredictionSerializer(data=request.data)
        if serializer.is_valid():
            # Convert input to DataFrame
            input_df = pd.DataFrame([serializer.validated_data])
            # Keep only the features used in training
            input_df = input_df[features]
            # Scale
            input_scaled = scaler.transform(input_df)
            # Predict
            prediction = model.predict(input_scaled)[0]
            return Response({'stress_level': float(prediction)}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
