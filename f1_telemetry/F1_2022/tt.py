def format_dict_for_log(d):
    """Formats a dictionary into a string for logging purposes."""
    return ', '.join(f'{key}: {value} --> {type}' for key, value, type in d)
header_data = []
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

print(format_dict_for_log(header_data))

#make a for loop for a dictionary