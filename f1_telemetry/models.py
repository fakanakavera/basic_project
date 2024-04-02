from django.db import models

# Create your models here.


class Header(models.Model):
    packetFormat = models.PositiveSmallIntegerField()
    gameMajorVersion = models.PositiveSmallIntegerField()
    gameMinorVersion = models.PositiveSmallIntegerField()
    packetVersion = models.PositiveSmallIntegerField()
    packetId = models.PositiveSmallIntegerField()
    sessionUID = models.DecimalField(max_digits=22, decimal_places=0, unique=False)
    sessionTime = models.FloatField()
    frameIdentifier = models.PositiveIntegerField()
    playerCarIndex = models.PositiveSmallIntegerField()
    secondaryPlayerCarIndex = models.PositiveSmallIntegerField()
    
    def __str__(self):
        return f"{self.sessionUID}-{self.sessionTime}"


class CarMotion(models.Model):
    header = models.ForeignKey(Header, on_delete=models.CASCADE)
    worldPositionX = models.FloatField()
    worldPositionY = models.FloatField()
    worldPositionZ = models.FloatField()
    worldVelocityX = models.FloatField()
    worldVelocityY = models.FloatField()
    worldVelocityZ = models.FloatField()
    worldForwardDirX = models.PositiveSmallIntegerField(null=True)
    worldForwardDirY = models.PositiveSmallIntegerField(null=True)
    worldForwardDirZ = models.PositiveSmallIntegerField(null=True)
    worldRightDirX = models.PositiveSmallIntegerField(null=True)
    worldRightDirY = models.PositiveSmallIntegerField(null=True)
    worldRightDirZ = models.PositiveSmallIntegerField(null=True)
    gForceLateral = models.FloatField()
    gForceLongitudinal = models.FloatField()
    gForceVertical = models.FloatField()
    yaw = models.FloatField()
    pitch = models.FloatField()
    roll = models.FloatField()

    
    def __str__(self):
        return f"{self.header}-{self.gForceLateral}-{self.gForceLongitudinal}-{self.gForceVertical}-{self.yaw}-{self.pitch}-{self.roll}"

class PacketSession(models.Model):
    header = models.ForeignKey(Header, on_delete=models.CASCADE)
    m_weather = models.IntegerField()
    m_trackTemperature = models.IntegerField()
    m_airTemperature = models.IntegerField()
    m_totalLaps = models.IntegerField()
    m_trackLength = models.IntegerField()
    m_sessionType = models.IntegerField()
    m_trackId = models.IntegerField()
    m_formula = models.IntegerField()
    m_sessionTimeLeft = models.IntegerField()
    m_sessionDuration = models.IntegerField()
    m_pitSpeedLimit = models.IntegerField()
    m_gamePaused = models.IntegerField()
    m_isSpectating = models.IntegerField()
    m_spectatorCarIndex = models.IntegerField()
    m_sliProNativeSupport = models.IntegerField()
    m_numMarshalZones = models.IntegerField()
    m_zoneStart = models.FloatField()
    m_zoneFlag = models.IntegerField()
    m_safetyCarStatus = models.IntegerField()
    m_networkGame = models.IntegerField()
    m_numWeatherForecastSamples = models.IntegerField()
    m_timeOffset = models.IntegerField()
    m_trackTemperatureChange = models.IntegerField()
    m_airTemperatureChange = models.IntegerField()
    m_rainPercentage = models.IntegerField()
    m_forecastAccuracy = models.IntegerField()
    m_aiDifficulty = models.IntegerField()
    m_seasonLinkIdentifier = models.PositiveIntegerField()
    m_weekendLinkIdentifier = models.PositiveIntegerField()
    m_sessionLinkIdentifier = models.PositiveIntegerField()
    m_pitStopWindowIdealLap = models.IntegerField()
    m_pitStopWindowLatestLap = models.IntegerField()
    m_pitStopRejoinPosition = models.IntegerField()
    m_steeringAssist = models.IntegerField()
    m_brakingAssist = models.IntegerField()
    m_gearboxAssist = models.IntegerField()
    m_pitAssist = models.IntegerField()
    m_pitReleaseAssist = models.IntegerField()
    m_ERSAssist = models.IntegerField()
    m_DRSAssist = models.IntegerField()
    m_dynamicRacingLine = models.IntegerField()
    m_dynamicRacingLineType = models.IntegerField()
    m_gameMode = models.IntegerField()
    m_ruleSet = models.IntegerField()
    m_timeOfDay = models.PositiveIntegerField()
    m_sessionLength = models.IntegerField()
    
class Lap(models.Model):
    header = models.ForeignKey(Header, on_delete=models.CASCADE)
    lastLapTimeInMS = models.PositiveIntegerField()                     #0
    currentLapTimeInMS = models.PositiveIntegerField()                  #1
    sector1TimeInMS = models.PositiveIntegerField()                     #2
    sector2TimeInMS = models.PositiveIntegerField()                     #3
    lapDistance = models.FloatField()                                   #4
    totalDistance = models.FloatField()                                 #5
    safetyCarDelta = models.FloatField()                                #6
    carPosition = models.PositiveSmallIntegerField()                    #7
    currentLapNum = models.PositiveSmallIntegerField()                  #8
    pitStatus = models.PositiveSmallIntegerField()                      #9
    numPitStops = models.PositiveSmallIntegerField()                    #10
    sector = models.PositiveSmallIntegerField()                         #11
    currentLapInvalid = models.PositiveSmallIntegerField()              #12
    penalties = models.PositiveSmallIntegerField()                      #13
    warnings = models.PositiveSmallIntegerField()                       #14
    numUnservedDriveThroughPens = models.PositiveSmallIntegerField()    #15
    numUnservedStopGoPens = models.PositiveSmallIntegerField()          #16
    gridPosition = models.PositiveSmallIntegerField()                   #17
    driverStatus = models.PositiveSmallIntegerField()                   #18
    resultStatus = models.PositiveSmallIntegerField()                   #19
    pitLaneTimerActive = models.PositiveSmallIntegerField()             #20
    pitLaneTimeInLaneInMS = models.PositiveIntegerField()               #21
    pitStopTimerInMS = models.PositiveIntegerField()                    #22
    pitStopShouldServePen = models.PositiveSmallIntegerField()          #23



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
    header = models.ForeignKey(Header, on_delete=models.CASCADE)
    numActiveCars = models.PositiveSmallIntegerField()
    aiControlled = models.BooleanField()
    driverId = models.PositiveSmallIntegerField(default=9999)
    networkId = models.PositiveSmallIntegerField()
    teamId = models.PositiveSmallIntegerField()
    myTeam = models.BooleanField()
    raceNumber = models.PositiveSmallIntegerField()
    nationality = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=100)
    yourTelemetry = models.BooleanField()

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




class Log(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    event_type = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return f"{self.created_at} - {self.event_type}"