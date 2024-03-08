from django.db import models

# Create your models here.


class Header(models.Model):
    sessionUID = models.DecimalField(max_digits=22, decimal_places=0, unique=False) #header_data[5]
    sessionTime = models.FloatField()                                               #header_data[6]
    
    def __str__(self):
        return f"{self.sessionUID}-{self.sessionTime}"


class CarMotion(models.Model):
    header = models.ForeignKey(Header, on_delete=models.CASCADE)
    gForceLateral = models.FloatField()
    gForceLongitudinal = models.FloatField()
    gForceVertical = models.FloatField()
    yaw = models.FloatField()
    pitch = models.FloatField()
    roll = models.FloatField()
    
    def __str__(self):
        return f"{self.header}-{self.gForceLateral}-{self.gForceLongitudinal}-{self.gForceVertical}-{self.yaw}-{self.pitch}-{self.roll}"


class Lap(models.Model):
    header = models.ForeignKey(Header, on_delete=models.CASCADE)
    lastLapTimeInMS = models.PositiveIntegerField()     #0
    currentLapTimeInMS = models.PositiveIntegerField()  #1
    sector1TimeInMS = models.PositiveSmallIntegerField()#2
    sector2TimeInMS = models.PositiveSmallIntegerField()#3
    lapDistance = models.FloatField()                   #4
    totalDistance = models.FloatField()                 #5


class CarSetup(models.Model):
    header = models.OneToOneField(Header, on_delete=models.CASCADE)
    frontWing = models.PositiveSmallIntegerField()                  #0
    rearWing = models.PositiveSmallIntegerField()                   #1
    onThrottle = models.PositiveSmallIntegerField()                 #2
    offThrottle = models.PositiveSmallIntegerField()                #3
    frontCamber = models.FloatField()
    rearCamber = models.FloatField()
    frontToe = models.FloatField()
    rearToe = models.FloatField()
    frontSuspension = models.PositiveSmallIntegerField()
    rearSuspension = models.PositiveSmallIntegerField()
    frontAntiRollBar = models.PositiveSmallIntegerField()
    rearAntiRollBar = models.PositiveSmallIntegerField()
    frontSuspensionHeight = models.PositiveSmallIntegerField()
    rearSuspensionHeight = models.PositiveSmallIntegerField()
    brakePressure = models.PositiveSmallIntegerField()
    brakeBias = models.PositiveSmallIntegerField()
    rearLeftTyrePressure = models.FloatField()
    rearRightTyrePressure = models.FloatField()
    frontLeftTyrePressure = models.FloatField()
    frontRightTyrePressure = models.FloatField()
    ballast = models.PositiveSmallIntegerField()
    fuelLoad = models.FloatField()

class Participant(models.Model):
    aiControlled = models.BooleanField()
    driverId = models.PositiveSmallIntegerField(default=9999)
    teamId = models.PositiveSmallIntegerField()

class CarTelemetry(models.Model):
    header = models.ForeignKey(Header, on_delete=models.CASCADE)
    driverId = models.ForeignKey(Participant, on_delete=models.CASCADE)
    speed = models.PositiveSmallIntegerField()
    throttle = models.FloatField()
    steer = models.FloatField()
    brake = models.FloatField()
    clutch = models.PositiveSmallIntegerField()
    gear = models.SmallIntegerField()
    engineRPM = models.PositiveSmallIntegerField()
    drs = models.PositiveSmallIntegerField()
    revLightsPercent = models.PositiveSmallIntegerField()
    revLightsBitValue = models.PositiveSmallIntegerField()
    brakesTemperatureRR = models.PositiveSmallIntegerField()
    brakesTemperatureRL = models.PositiveSmallIntegerField()
    brakesTemperatureFL = models.PositiveSmallIntegerField()
    brakesTemperatureFR = models.PositiveSmallIntegerField()
    tyresSurfaceTemperatureRR = models.PositiveSmallIntegerField()
    tyresSurfaceTemperatureRL = models.PositiveSmallIntegerField()
    tyresSurfaceTemperatureFL = models.PositiveSmallIntegerField()
    tyresSurfaceTemperatureFR = models.PositiveSmallIntegerField()
    tyresInnerTemperatureRR = models.PositiveSmallIntegerField()
    tyresInnerTemperatureRL = models.PositiveSmallIntegerField()
    tyresInnerTemperatureFL = models.PositiveSmallIntegerField()
    tyresInnerTemperatureFR = models.PositiveSmallIntegerField()
    engineTemperature = models.PositiveSmallIntegerField()
    tyresPressureRR = models.FloatField()
    tyresPressureRL = models.FloatField()
    tyresPressureFL = models.FloatField()
    tyresPressureFR = models.FloatField()
    surfaceTypeRR = models.PositiveSmallIntegerField()
    surfaceTypeRL = models.PositiveSmallIntegerField()
    surfaceTypeFL = models.PositiveSmallIntegerField()
    surfaceTypeFR = models.PositiveSmallIntegerField()
