from rest_framework import serializers

class HealthPredictionSerializer(serializers.Serializer):
    coffee_cups_per_day = serializers.FloatField()
    caffeine_mg = serializers.FloatField()
    age = serializers.IntegerField()
    body_weight_kg = serializers.FloatField()
    exercise_minutes = serializers.FloatField()
    water_intake_liters = serializers.FloatField()
    sleep_hours = serializers.FloatField()
    stress_level = serializers.FloatField(read_only=True)  # predicted value
