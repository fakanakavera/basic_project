from django.db import models

# Create your models here.


class Header(models.Model):
    packetFormat = models.PositiveSmallIntegerField(default=0)
    gameMajorVersion = models.PositiveSmallIntegerField(default=0)
    gameMinorVersion = models.PositiveSmallIntegerField(default=0)
    packetVersion = models.PositiveSmallIntegerField(default=0)
    packetId = models.PositiveSmallIntegerField(default=0)
    sessionUID = models.DecimalField(max_digits=22, decimal_places=0, unique=False)
    sessionTime = models.FloatField(default=0.0)
    frameIdentifier = models.PositiveIntegerField(default=0)
    playerCarIndex = models.PositiveSmallIntegerField(default=0)
    secondaryPlayerCarIndex = models.PositiveSmallIntegerField(default=0)
    
    def __str__(self):
        return f"{self.sessionUID}-{self.sessionTime}"


class Participant(models.Model):
    header = models.ForeignKey(Header, on_delete=models.CASCADE)
    aiControlled = models.BooleanField()
    driverId = models.PositiveSmallIntegerField(default=9999)
    networkId = models.PositiveSmallIntegerField(default=0)
    teamId = models.PositiveSmallIntegerField(default=0)
    myTeam = models.BooleanField()
    raceNumber = models.PositiveSmallIntegerField(default=0)
    nationality = models.PositiveSmallIntegerField(default=0)
    name = models.CharField(max_length=100)
    yourTelemetry = models.BooleanField()

class CarMotion(models.Model):
    header = models.ForeignKey(Header, on_delete=models.CASCADE)
    driverId = models.ForeignKey(Participant, on_delete=models.CASCADE)
    worldPositionX = models.FloatField(default=0.0)
    worldPositionY = models.FloatField(default=0.0)
    worldPositionZ = models.FloatField(default=0.0)
    worldVelocityX = models.FloatField(default=0.0)
    worldVelocityY = models.FloatField(default=0.0)
    worldVelocityZ = models.FloatField(default=0.0)
    worldForwardDirX = models.SmallIntegerField(default=0, null=True)
    worldForwardDirY = models.SmallIntegerField(default=0, null=True)
    worldForwardDirZ = models.SmallIntegerField(default=0, null=True)
    worldRightDirX = models.SmallIntegerField(default=0, null=True)
    worldRightDirY = models.SmallIntegerField(default=0, null=True)
    worldRightDirZ = models.SmallIntegerField(default=0, null=True)
    gForceLateral = models.FloatField(default=0.0)
    gForceLongitudinal = models.FloatField(default=0.0)
    gForceVertical = models.FloatField(default=0.0)
    yaw = models.FloatField(default=0.0)
    pitch = models.FloatField(default=0.0)
    roll = models.FloatField(default=0.0)

    
    def __str__(self):
        return f"{self.header}-{self.gForceLateral}-{self.gForceLongitudinal}-{self.gForceVertical}-{self.yaw}-{self.pitch}-{self.roll}"

class PacketSession(models.Model):
    header = models.ForeignKey(Header, on_delete=models.CASCADE)
    weather = models.IntegerField(default=0)
    trackTemperature = models.IntegerField(default=0)
    airTemperature = models.IntegerField(default=0)
    totalLaps = models.IntegerField(default=0)
    trackLength = models.IntegerField(default=0)
    sessionType = models.IntegerField(default=0)
    trackId = models.IntegerField(default=0)
    formula = models.IntegerField(default=0)
    sessionTimeLeft = models.IntegerField(default=0)
    sessionDuration = models.IntegerField(default=0)
    pitSpeedLimit = models.IntegerField(default=0)
    gamePaused = models.IntegerField(default=0)
    isSpectating = models.IntegerField(default=0)
    spectatorCarIndex = models.IntegerField(default=0)
    sliProNativeSupport = models.IntegerField(default=0)
    numMarshalZones = models.IntegerField(default=0)
    zoneStart = models.FloatField(default=0.0)
    zoneFlag = models.IntegerField(default=0)
    safetyCarStatus = models.IntegerField(default=0)
    networkGame = models.IntegerField(default=0)
    numWeatherForecastSamples = models.IntegerField(default=0)
    timeOffset = models.IntegerField(default=0)
    trackTemperatureChange = models.IntegerField(default=0)
    airTemperatureChange = models.IntegerField(default=0)
    rainPercentage = models.IntegerField(default=0)
    forecastAccuracy = models.IntegerField(default=0)
    aiDifficulty = models.IntegerField(default=0)
    seasonLinkIdentifier = models.PositiveBigIntegerField(default=0)
    weekendLinkIdentifier = models.PositiveBigIntegerField(default=0)
    sessionLinkIdentifier = models.PositiveIntegerField(default=0)
    pitStopWindowIdealLap = models.IntegerField(default=0)
    pitStopWindowLatestLap = models.IntegerField(default=0)
    pitStopRejoinPosition = models.IntegerField(default=0)
    steeringAssist = models.IntegerField(default=0)
    brakingAssist = models.IntegerField(default=0)
    gearboxAssist = models.IntegerField(default=0)
    pitAssist = models.IntegerField(default=0)
    pitReleaseAssist = models.IntegerField(default=0)
    ERSAssist = models.IntegerField(default=0)
    DRSAssist = models.IntegerField(default=0)
    dynamicRacingLine = models.IntegerField(default=0)
    dynamicRacingLineType = models.IntegerField(default=0)
    gameMode = models.IntegerField(default=0)
    ruleSet = models.IntegerField(default=0)
    timeOfDay = models.PositiveBigIntegerField(default=0)
    sessionLength = models.IntegerField(default=0)
    
class Lap(models.Model):
    header = models.ForeignKey(Header, on_delete=models.CASCADE)
    driverId = models.ForeignKey(Participant, on_delete=models.CASCADE)
    lastLapTimeInMS = models.PositiveIntegerField(default=0)                     #0
    currentLapTimeInMS = models.PositiveIntegerField(default=0)                  #1
    sector1TimeInMS = models.PositiveIntegerField(default=0)                     #2
    sector2TimeInMS = models.PositiveIntegerField(default=0)                     #3
    lapDistance = models.FloatField(default=0.0)                                   #4
    totalDistance = models.FloatField(default=0.0)                                 #5
    safetyCarDelta = models.FloatField(default=0.0)                                #6
    carPosition = models.PositiveSmallIntegerField(default=0)                    #7
    currentLapNum = models.PositiveSmallIntegerField(default=0)                  #8
    pitStatus = models.PositiveSmallIntegerField(default=0)                      #9
    numPitStops = models.PositiveSmallIntegerField(default=0)                    #10
    sector = models.PositiveSmallIntegerField(default=0)                         #11
    currentLapInvalid = models.PositiveSmallIntegerField(default=0)              #12
    penalties = models.PositiveSmallIntegerField(default=0)                      #13
    warnings = models.PositiveSmallIntegerField(default=0)                       #14
    numUnservedDriveThroughPens = models.PositiveSmallIntegerField(default=0)    #15
    numUnservedStopGoPens = models.PositiveSmallIntegerField(default=0)          #16
    gridPosition = models.PositiveSmallIntegerField(default=0)                   #17
    driverStatus = models.PositiveSmallIntegerField(default=0)                   #18
    resultStatus = models.PositiveSmallIntegerField(default=0)                   #19
    pitLaneTimerActive = models.PositiveSmallIntegerField(default=0)             #20
    pitLaneTimeInLaneInMS = models.PositiveIntegerField(default=0)               #21
    pitStopTimerInMS = models.PositiveIntegerField(default=0)                    #22
    pitStopShouldServePen = models.PositiveSmallIntegerField(default=0)          #23



class CarSetup(models.Model):
    header = models.ForeignKey(Header, on_delete=models.CASCADE)
    driverId = models.ForeignKey(Participant, on_delete=models.CASCADE)
    frontWing = models.PositiveSmallIntegerField(default=0)                  #0
    rearWing = models.PositiveSmallIntegerField(default=0)                   #1
    onThrottle = models.PositiveSmallIntegerField(default=0)                 #2
    offThrottle = models.PositiveSmallIntegerField(default=0)                #3
    frontCamber = models.FloatField(default=0.0)
    rearCamber = models.FloatField(default=0.0)
    frontToe = models.FloatField(default=0.0)
    rearToe = models.FloatField(default=0.0)
    frontSuspension = models.PositiveSmallIntegerField(default=0)
    rearSuspension = models.PositiveSmallIntegerField(default=0)
    frontAntiRollBar = models.PositiveSmallIntegerField(default=0)
    rearAntiRollBar = models.PositiveSmallIntegerField(default=0)
    frontSuspensionHeight = models.PositiveSmallIntegerField(default=0)
    rearSuspensionHeight = models.PositiveSmallIntegerField(default=0)
    brakePressure = models.PositiveSmallIntegerField(default=0)
    brakeBias = models.PositiveSmallIntegerField(default=0)
    rearLeftTyrePressure = models.FloatField(default=0.0)
    rearRightTyrePressure = models.FloatField(default=0.0)
    frontLeftTyrePressure = models.FloatField(default=0.0)
    frontRightTyrePressure = models.FloatField(default=0.0)
    ballast = models.PositiveSmallIntegerField(default=0)
    fuelLoad = models.FloatField(default=0.0)


class CarTelemetry(models.Model):
    header = models.ForeignKey(Header, on_delete=models.CASCADE)
    driverId = models.ForeignKey(Participant, on_delete=models.CASCADE)
    speed = models.PositiveSmallIntegerField(default=0)
    throttle = models.FloatField(default=0.0)
    steer = models.FloatField(default=0.0)
    brake = models.FloatField(default=0.0)
    clutch = models.PositiveSmallIntegerField(default=0)
    gear = models.SmallIntegerField(default=0)
    engineRPM = models.PositiveSmallIntegerField(default=0)
    drs = models.PositiveSmallIntegerField(default=0)
    revLightsPercent = models.PositiveSmallIntegerField(default=0)
    revLightsBitValue = models.PositiveSmallIntegerField(default=0)
    brakesTemperatureRR = models.PositiveSmallIntegerField(default=0)
    brakesTemperatureRL = models.PositiveSmallIntegerField(default=0)
    brakesTemperatureFL = models.PositiveSmallIntegerField(default=0)
    brakesTemperatureFR = models.PositiveSmallIntegerField(default=0)
    tyresSurfaceTemperatureRR = models.PositiveSmallIntegerField(default=0)
    tyresSurfaceTemperatureRL = models.PositiveSmallIntegerField(default=0)
    tyresSurfaceTemperatureFL = models.PositiveSmallIntegerField(default=0)
    tyresSurfaceTemperatureFR = models.PositiveSmallIntegerField(default=0)
    tyresInnerTemperatureRR = models.PositiveSmallIntegerField(default=0)
    tyresInnerTemperatureRL = models.PositiveSmallIntegerField(default=0)
    tyresInnerTemperatureFL = models.PositiveSmallIntegerField(default=0)
    tyresInnerTemperatureFR = models.PositiveSmallIntegerField(default=0)
    engineTemperature = models.PositiveSmallIntegerField(default=0)
    tyresPressureRR = models.FloatField(default=0.0)
    tyresPressureRL = models.FloatField(default=0.0)
    tyresPressureFL = models.FloatField(default=0.0)
    tyresPressureFR = models.FloatField(default=0.0)
    surfaceTypeRR = models.PositiveSmallIntegerField(default=0)
    surfaceTypeRL = models.PositiveSmallIntegerField(default=0)
    surfaceTypeFL = models.PositiveSmallIntegerField(default=0)
    surfaceTypeFR = models.PositiveSmallIntegerField(default=0)

class Log(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    event_type = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return f"{self.created_at} - {self.event_type}"
    
class session_type(models.Model):
    session_id = models.IntegerField(default=0)
    session_type = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.session_type}"