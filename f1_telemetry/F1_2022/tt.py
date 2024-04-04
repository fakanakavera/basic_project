def format_dict_for_log(d):
    """Formats a dictionary into a string for logging purposes."""
    return ', '.join(f'{key}: {value} --> {type}' for key, value, type in d)


d = [['m_packetFormat', 2022, 'uint16'], ['m_gameMajorVersion', 1, 'uint8'], ['m_gameMinorVersion', 19, 'uint8'], ['m_packetVersion', 1, 'uint8'], ['m_packetId', 3, 'uint8'], ['m_sessionUID', 17745228683760066244, 'uint64'], ['m_sessionTime', 2.743454933166504, 'f'], ['m_frameIdentifier', 57, 'uint32'], ['m_playerCarIndex', 0, 'uint8'], ['m_secondaryPlayerCarIndex', 255, 'uint8']]
print(format_dict_for_log(d))

#make a for loop for a dictionary