
returnData = []  # Create an empty array
header_data = []  # Create an empty array
CarMotionData = []  # Create an empty array
PacketSessionData = []  # Create an empty array
LapData = []  # Create an empty array
CarSetupData = []  # Create an empty array
CarTelemetryData = []  # Create an empty array
ParticipantsData = []  # Create an empty array
# Initialize data array -- BEGIN FUNCTION


def initArray():
    global header_data
    header_data.append(['m_packetFormat', 0, 'uint16'])
    header_data.append(['m_gameMajorVersion', 0, 'uint8'])
    header_data.append(['m_gameMinorVersion', 0, 'uint8'])
    header_data.append(['m_packetVersion', 0, 'uint8'])
    header_data.append(['m_packetId', 0, 'uint8'])
    header_data.append(['m_sessionUID', 0, 'uint64'])   # 5
    header_data.append(['m_sessionTime', 0, 'f'])       # 6
    header_data.append(['m_frameIdentifier', 0, 'uint32'])
    header_data.append(['m_playerCarIndex', 0, 'uint8'])
    header_data.append(['m_secondaryPlayerCarIndex', 0, 'uint8'])

    CarMotionData.append(['m_worldPositionX', 0, 'f'])
    CarMotionData.append(['m_worldPositionY', 0, 'f'])
    CarMotionData.append(['m_worldPositionZ', 0, 'f'])
    CarMotionData.append(['m_worldVelocityX', 0, 'f'])
    CarMotionData.append(['m_worldVelocityY', 0, 'f'])
    CarMotionData.append(['m_worldVelocityZ', 0, 'f'])
    CarMotionData.append(['m_worldForwardDirX', 0, 'int16'])
    CarMotionData.append(['m_worldForwardDirY', 0, 'int16'])
    CarMotionData.append(['m_worldForwardDirZ', 0, 'int16'])
    CarMotionData.append(['m_worldRightDirX', 0, 'int16'])
    CarMotionData.append(['m_worldRightDirY', 0, 'int16'])
    CarMotionData.append(['m_worldRightDirZ', 0, 'int16'])
    CarMotionData.append(['m_gForceLateral', 0, 'f'])       #12
    CarMotionData.append(['m_gForceLongitudinal', 0, 'f'])  #13
    CarMotionData.append(['m_gForceVertical', 0, 'f'])      #14
    CarMotionData.append(['m_yaw', 0, 'f'])                 #15
    CarMotionData.append(['m_pitch', 0, 'f'])               #16
    CarMotionData.append(['m_roll', 0, 'f'])                #17

    
    
    
    
    PacketSessionData.append(['m_weather', 0, 'uint8'])
    PacketSessionData.append(['m_trackTemperature', 0, 'int8'])
    PacketSessionData.append(['m_airTemperature', 0, 'int8'])
    PacketSessionData.append(['m_totalLaps', 0, 'uint8'])
    PacketSessionData.append(['m_trackLength', 0, 'uint16'])
    PacketSessionData.append(['m_sessionType', 0, 'uint8'])
    PacketSessionData.append(['m_trackId', 0, 'int8'])
    PacketSessionData.append(['m_formula', 0, 'uint8'])
    PacketSessionData.append(['m_sessionTimeLeft', 0, 'uint16'])
    PacketSessionData.append(['m_sessionDuration', 0, 'uint16'])
    PacketSessionData.append(['m_pitSpeedLimit', 0, 'uint8'])
    PacketSessionData.append(['m_gamePaused', 0, 'uint8'])
    PacketSessionData.append(['m_isSpectating', 0, 'uint8'])
    PacketSessionData.append(['m_spectatorCarIndex', 0, 'uint8'])
    PacketSessionData.append(['m_sliProNativeSupport', 0, 'uint8'])
    PacketSessionData.append(['m_numMarshalZones', 0, 'uint8'])
    PacketSessionData.append(['m_zoneStart', 0, 'f'])
    PacketSessionData.append(['m_zoneFlag', 0, 'int8'])
    PacketSessionData.append(['m_safetyCarStatus', 0, 'uint8'])
    PacketSessionData.append(['m_networkGame', 0, 'uint8'])
    PacketSessionData.append(['m_numWeatherForecastSamples', 0, 'uint8'])
    PacketSessionData.append(['m_sessionType', 0, 'uint8'])
    PacketSessionData.append(['m_timeOffset', 0, 'uint8'])
    PacketSessionData.append(['m_weather', 0, 'uint8'])
    PacketSessionData.append(['m_trackTemperature', 0, 'int8'])
    PacketSessionData.append(['m_trackTemperatureChange', 0, 'int8'])
    PacketSessionData.append(['m_airTemperature', 0, 'int8'])
    PacketSessionData.append(['m_airTemperatureChange', 0, 'int8'])
    PacketSessionData.append(['m_rainPercentage', 0, 'uint8'])
    PacketSessionData.append(['m_forecastAccuracy', 0, 'uint8'])
    PacketSessionData.append(['m_aiDifficulty', 0, 'uint8'])
    PacketSessionData.append(['m_seasonLinkIdentifier', 0, 'uint32'])
    PacketSessionData.append(['m_weekendLinkIdentifier', 0, 'uint32'])
    PacketSessionData.append(['m_sessionLinkIdentifier', 0, 'uint32'])
    PacketSessionData.append(['m_pitStopWindowIdealLap', 0, 'uint8'])
    PacketSessionData.append(['m_pitStopWindowLatestLap', 0, 'uint8'])
    PacketSessionData.append(['m_pitStopRejoinPosition', 0, 'uint8'])
    PacketSessionData.append(['m_steeringAssist', 0, 'uint8'])
    PacketSessionData.append(['m_brakingAssist', 0, 'uint8'])
    PacketSessionData.append(['m_gearboxAssist', 0, 'uint8'])
    PacketSessionData.append(['m_pitAssist', 0, 'uint8'])
    PacketSessionData.append(['m_pitReleaseAssist', 0, 'uint8'])
    PacketSessionData.append(['m_ERSAssist', 0, 'uint8'])
    PacketSessionData.append(['m_DRSAssist', 0, 'uint8'])
    PacketSessionData.append(['m_dynamicRacingLine', 0, 'uint8'])
    PacketSessionData.append(['m_dynamicRacingLineType', 0, 'uint8'])
    PacketSessionData.append(['m_gameMode', 0, 'uint8'])
    PacketSessionData.append(['m_ruleSet', 0, 'uint8'])
    PacketSessionData.append(['m_timeOfDay', 0, 'uint32'])
    PacketSessionData.append(['m_sessionLength', 0, 'uint8'])

    LapData.append(['m_lastLapTimeInMS', 0, 'uint32'])
    LapData.append(['m_currentLapTimeInMS', 0, 'uint32'])
    LapData.append(['m_sector1TimeInMS', 0, 'uint16'])
    LapData.append(['m_sector2TimeInMS', 0, 'uint16'])
    LapData.append(['m_lapDistance', 0, 'f'])
    LapData.append(['m_totalDistance', 0, 'f'])
    LapData.append(['m_safetyCarDelta', 0, 'f'])
    LapData.append(['m_carPosition', 0, 'uint8'])
    LapData.append(['m_currentLapNum', 0, 'uint8'])
    LapData.append(['m_pitStatus', 0, 'uint8'])
    LapData.append(['m_numPitStops', 0, 'uint8'])
    LapData.append(['m_sector', 0, 'uint8'])
    LapData.append(['m_currentLapInvalid', 0, 'uint8'])
    LapData.append(['m_penalties', 0, 'uint8'])
    LapData.append(['m_warnings', 0, 'uint8'])
    LapData.append(['m_numUnservedDriveThroughPens', 0, 'uint8'])
    LapData.append(['m_numUnservedStopGoPens', 0, 'uint8'])
    LapData.append(['m_gridPosition', 0, 'uint8'])
    LapData.append(['m_driverStatus', 0, 'uint8'])
    LapData.append(['m_resultStatus', 0, 'uint8'])
    LapData.append(['m_pitLaneTimerActive', 0, 'uint8'])
    LapData.append(['m_pitLaneTimeInLaneInMS', 0, 'uint16'])
    LapData.append(['m_pitStopTimerInMS', 0, 'uint16'])
    LapData.append(['m_pitStopShouldServePen', 0, 'uint8'])

    CarSetupData.append(['m_frontWing', 0, 'uint8'])
    CarSetupData.append(['m_rearWing', 0, 'uint8'])
    CarSetupData.append(['m_onThrottle', 0, 'uint8'])
    CarSetupData.append(['m_offThrottle', 0, 'uint8'])
    CarSetupData.append(['m_frontCamber', 0, 'f'])
    CarSetupData.append(['m_rearCamber', 0, 'f'])
    CarSetupData.append(['m_frontToe', 0, 'f'])
    CarSetupData.append(['m_rearToe', 0, 'f'])
    CarSetupData.append(['m_frontSuspension', 0, 'uint8'])
    CarSetupData.append(['m_rearSuspension', 0, 'uint8'])
    CarSetupData.append(['m_frontAntiRollBar', 0, 'uint8'])
    CarSetupData.append(['m_rearAntiRollBar', 0, 'uint8'])
    CarSetupData.append(['m_frontSuspensionHeight', 0, 'uint8'])
    CarSetupData.append(['m_rearSuspensionHeight', 0, 'uint8'])
    CarSetupData.append(['m_brakePressure', 0, 'uint8'])
    CarSetupData.append(['m_brakeBias', 0, 'uint8'])
    CarSetupData.append(['m_rearLeftTyrePressure', 0, 'f'])
    CarSetupData.append(['m_rearRightTyrePressure', 0, 'f'])
    CarSetupData.append(['m_frontLeftTyrePressure', 0, 'f'])
    CarSetupData.append(['m_frontRightTyrePressure', 0, 'f'])
    CarSetupData.append(['m_ballast', 0, 'uint8'])
    CarSetupData.append(['m_fuelLoad', 0, 'f'])

    CarTelemetryData.append(['m_speed', 0, 'uint16'])
    CarTelemetryData.append(['m_throttle', 0, 'f'])
    CarTelemetryData.append(['m_steer', 0, 'f'])
    CarTelemetryData.append(['m_brake', 0, 'f'])
    CarTelemetryData.append(['m_clutch', 0, 'uint8'])
    CarTelemetryData.append(['m_gear', 0, 'int8'])
    CarTelemetryData.append(['m_engineRPM', 0, 'uint16'])
    CarTelemetryData.append(['m_drs', 0, 'uint8'])
    CarTelemetryData.append(['m_revLightsPercent', 0, 'uint8'])
    CarTelemetryData.append(['m_revLightsBitValue', 0, 'uint16'])
    CarTelemetryData.append(['m_brakesTemperatureRR', 0, 'uint16'])
    CarTelemetryData.append(['m_brakesTemperatureRL', 0, 'uint16'])
    CarTelemetryData.append(['m_brakesTemperatureFL', 0, 'uint16'])
    CarTelemetryData.append(['m_brakesTemperatureFR', 0, 'uint16'])
    CarTelemetryData.append(['m_tyresSurfaceTemperatureRR', 0, 'uint8'])
    CarTelemetryData.append(['m_tyresSurfaceTemperatureRL', 0, 'uint8'])
    CarTelemetryData.append(['m_tyresSurfaceTemperatureFL', 0, 'uint8'])
    CarTelemetryData.append(['m_tyresSurfaceTemperatureFR', 0, 'uint8'])
    CarTelemetryData.append(['m_tyresInnerTemperatureRR', 0, 'uint8'])
    CarTelemetryData.append(['m_tyresInnerTemperatureRL', 0, 'uint8'])
    CarTelemetryData.append(['m_tyresInnerTemperatureFL', 0, 'uint8'])
    CarTelemetryData.append(['m_tyresInnerTemperatureFR', 0, 'uint8'])
    CarTelemetryData.append(['m_engineTemperature', 0, 'uint16'])
    CarTelemetryData.append(['m_tyresPressureRR', 0, 'f'])
    CarTelemetryData.append(['m_tyresPressureRL', 0, 'f'])
    CarTelemetryData.append(['m_tyresPressureFL', 0, 'f'])
    CarTelemetryData.append(['m_tyresPressureFR', 0, 'f'])
    CarTelemetryData.append(['m_surfaceTypeRR', 0, 'uint8'])
    CarTelemetryData.append(['m_surfaceTypeRL', 0, 'uint8'])
    CarTelemetryData.append(['m_surfaceTypeFL', 0, 'uint8'])
    CarTelemetryData.append(['m_surfaceTypeFR', 0, 'uint8'])

    ParticipantsData.append(['m_numActiveCars', 0, 'uint8'])
    ParticipantsData.append(['m_aiControlled', 0, 'uint8'])
    ParticipantsData.append(['m_driverId', 0, 'uint8'])
    ParticipantsData.append(['m_networkId', 0, 'uint8'])
    ParticipantsData.append(['m_teamId', 0, 'uint8'])
    ParticipantsData.append(['m_myTeam', 0, 'uint8'])
    ParticipantsData.append(['m_raceNumber', 0, 'uint8'])
    ParticipantsData.append(['m_nationality', 0, 'uint8'])
    ParticipantsData.append(['m_name', 0, 'char'])
    ParticipantsData.append(['m_yourTelemetry', 0, 'uint8'])


initArray()  # Execute the function
