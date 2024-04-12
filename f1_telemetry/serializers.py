from rest_framework import serializers
from .models import Header, CarMotion, Lap, CarSetup, Participant, CarTelemetry, PacketSession, Log

class HeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Header
        fields = '__all__'

class CarMotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarMotion
        fields = '__all__'

class LapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lap
        fields = '__all__'

class CarSetupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarSetup
        fields = '__all__'

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = '__all__'

class CarTelemetrySerializer(serializers.ModelSerializer):
    class Meta:
        model = CarTelemetry
        fields = '__all__'

class PacketSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PacketSession
        fields = '__all__'

class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = '__all__'
