from f1_22_telemetry.listener import TelemetryListener

listener = TelemetryListener(port=20777, host='localhost')
packet = listener.get()

# TRUNCATE TABLE f1_telemetry_carmotion, f1_telemetry_carsetup, f1_telemetry_cartelemetry, f1_telemetry_header, f1_telemetry_lap, f1_telemetry_log, f1_te
# lemetry_packetsession, f1_telemetry_participant RESTART IDENTITY;