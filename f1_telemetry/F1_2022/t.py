from f1_22_telemetry.listener import TelemetryListener

listener = TelemetryListener(port=20777, host='localhost')
packet = listener.get()
