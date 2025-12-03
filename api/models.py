from django.db import models

class HealthPrediction(models.Model):
    coffee_cups_per_day = models.FloatField()
    caffeine_mg = models.FloatField()
    age = models.IntegerField()
    body_weight_kg = models.FloatField()
    exercise_minutes = models.FloatField()
    water_intake_liters = models.FloatField()
    sleep_hours = models.FloatField()
    predicted_stress_level = models.CharField(max_length=100, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prediction {self.id} - Stress: {self.predicted_stress_level}"
