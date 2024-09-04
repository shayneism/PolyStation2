import numpy as np

class VRAM:
    def __init__(self, size_mb=4):
        self.size = size_mb * 1024 * 1024  # Convert MB to bytes
        self.memory = np.zeros(self.size, dtype=np.uint8)
        self.usage = 0
        self.access_time = 0.000000015  # 15 nanoseconds access time

    def write(self, address, data):
        if address + len(data) > self.size:
            raise ValueError("Write operation exceeds VRAM size")
        self.memory[address:address+len(data)] = data
        self.update_usage()

    def read(self, address, length):
        if address + length > self.size:
            raise ValueError("Read operation exceeds VRAM size")
        return self.memory[address:address+length]

    def clear(self):
        self.memory.fill(0)
        self.update_usage()

    def update_usage(self):
        self.usage = np.count_nonzero(self.memory) / self.size * 100

    def set_usage(self, percentage):
        self.usage = percentage
        filled_bytes = int(self.size * percentage / 100)
        self.memory[:filled_bytes] = 1
        self.memory[filled_bytes:] = 0

    def get_usage_percentage(self):
        return self.usage

    def get_bandwidth(self):
        return self.size / self.access_time  # Bytes per second

class eDRAM:
    def __init__(self, size_kb=4):
        self.size = size_kb * 1024  # Convert KB to bytes
        self.memory = np.zeros(self.size, dtype=np.uint8)
        self.usage = 0
        self.access_time = 0.000000001  # 1 nanosecond access time

    def write(self, address, data):
        if address + len(data) > self.size:
            raise ValueError("Write operation exceeds eDRAM size")
        self.memory[address:address+len(data)] = data
        self.update_usage()

    def read(self, address, length):
        if address + length > self.size:
            raise ValueError("Read operation exceeds eDRAM size")
        return self.memory[address:address+length]

    def clear(self):
        self.memory.fill(0)
        self.update_usage()

    def update_usage(self):
        self.usage = np.count_nonzero(self.memory) / self.size * 100

    def get_usage_percentage(self):
        return self.usage

    def get_bandwidth(self):
        return self.size / self.access_time  # Bytes per second