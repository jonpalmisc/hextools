import struct


def parseInt(bytes, maxSize, signed=True, endian="little"):
    return int.from_bytes(bytes[:maxSize], byteorder=endian, signed=signed)


def parseFloat(bytes):
    try:
        fmt = "d" if len(bytes) > 4 else "f"
        return struct.unpack(fmt, bytes)[0]
    except:
        return 0
