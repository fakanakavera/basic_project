data_types = {
    'int8': {'size': 1, 'format': 'b'},  # Signed 8-bit integer
    'uint8': {'size': 1, 'format': 'B'},  # Unsigned 8-bit integer
    'int16': {'size': 2, 'format': 'h'},  # Signed 16-bit integer
    'uint16': {'size': 2, 'format': 'H'},  # Unsigned 16-bit integer
    'int32': {'size': 4, 'format': 'i'},  # Signed 32-bit integer
    'uint32': {'size': 4, 'format': 'I'},  # Unsigned 32-bit integer
    'f': {'size': 4, 'format': 'f'},  # 32-bit floating point
    'int64': {'size': 8, 'format': 'q'},  # Signed 64-bit integer
    'uint64': {'size': 8, 'format': 'Q'},  # Unsigned 64-bit integer
    'char': {'size': 48, 'format': '48s'},  # Character
}


packet_types = {
    0: {'name': 'Motion', 'size': 1464},
    1: {'name': 'Session', 'size': 632},
    2: {'name': 'Lap Data', 'size': 972},
    3: {'name': 'Event', 'size': 40},
    4: {'name': 'Participants', 'size': 1257},
    5: {'name': 'Car Setups', 'size': 1102},
    6: {'name': 'Car Telemetry', 'size': 1347},
    7: {'name': 'Car Status', 'size': 1058},
    8: {'name': 'Final Classification', 'size': 1015},
    9: {'name': 'Lobby Info', 'size': 1191},
    10: {'name': 'Car Damage', 'size': 948},
    11: {'name': 'Session History', 'size': 1155},
}

track_ids = {
    0: 'Melbourne',
    1: 'Paul Ricard',
    2: 'Shanghai',
    3: 'Sakhir (Bahrain)',
    4: 'Catalunya',
    5: 'Monaco',
    6: 'Montreal',
    7: 'Silverstone',
    8: 'Hockenheim',
    9: 'Hungaroring',
    10: 'Spa',
    11: 'Monza',
    12: 'Singapore',
    13: 'Suzuka',
    14: 'Abu Dhabi',
    15: 'Texas',
    16: 'Brazil',
    17: 'Austria',
    18: 'Sochi',
    19: 'Mexico',
    20: 'Baku (Azerbaijan)',
    21: 'Sakhir Short',
    22: 'Silverstone Short',
    23: 'Texas Short',
    24: 'Suzuka Short',
    25: 'Hanoi',
    26: 'Zandvoort',
    27: 'Imola',
    28: 'Portimão',
    29: 'Jeddah',
    30: 'Miami'

}
