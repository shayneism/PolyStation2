import numpy as np

class BufferManager:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.color_buffer = np.zeros((height, width, 3), dtype=np.uint8)
        self.z_buffer = np.full((height, width), float('inf'))

    def clear_buffers(self):
        self.color_buffer.fill(0)
        self.z_buffer.fill(float('inf'))

    def update_pixel(self, x, y, z, color):
        if 0 <= x < self.width and 0 <= y < self.height:
            if z < self.z_buffer[y, x]:
                self.color_buffer[y, x] = color
                self.z_buffer[y, x] = z

    def get_color_buffer(self):
        return self.color_buffer

class ColorPalette:
    @staticmethod
    def get_color(r, g, b):
        return np.array([r, g, b], dtype=np.uint8)

    @staticmethod
    def interpolate_color(color1, color2, t):
        return (1 - t) * color1 + t * color2