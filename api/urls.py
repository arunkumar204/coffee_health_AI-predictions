from django.urls import path
from .views import HealthPredictionViewSet

urlpatterns = [
    path('predictions/', HealthPredictionViewSet.as_view(), name='health-prediction'),
    path('predictions/predict/', HealthPredictionViewSet.as_view(), name='health-predict'),
]
