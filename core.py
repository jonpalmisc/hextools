def parseInt(bytes, maxSize, signed=True, endian="little"):
    return int.from_bytes(bytes[:maxSize], byteorder=endian, signed=signed)
