import random
import time
import math
from VRAM import VRAM, eDRAM

class PS2GPU:
    def __init__(self):
        self.vram = VRAM(4)  # 4MB of VRAM
        self.edram = eDRAM(4)  # 4KB of eDRAM
        self.temperature = 35  # Initial temperature in Celsius
        self.ambient_temperature = 25  # Ambient room temperature
        self.fan_speed = 20  # Fan speed as a percentage
        self.stress = 0  # Stress level as a percentage
        self.clock_speed = 147.456  # Clock speed in MHz (constant for PS2)
        self.fill_rate = 2.4  # Fill rate in gigapixels/second
        self.polygon_rate = 66  # Polygon rate in millions/second
        self.current_resolution = (640, 240)  # Default to 480i
        self.current_fps = 60  # Default to 60 fps
        self.last_operation = "idle"
        self.operation_start_time = time.time()
        self.heat_accumulation = 0
        self.cooling_efficiency = 0.8  # 80% cooling efficiency
        self.tmus = 8  # Texture Mapping Units
        self.rops = 16  # Render Output Units
        self.pony_synth_boost = 1.05  # 5% performance boost

        # Resolution options (width, height, interlaced)
        self.resolution_options = [
            (640, 240, True),   # 480i
            (640, 480, False),  # 480p (rare, but supported)
            (320, 240, True),   # 240i
        ]

    def update(self, dt):
        current_time = time.time()
        operation_duration = current_time - self.operation_start_time

        # Simulate different GPU operations
        if operation_duration > random.uniform(0.5, 3.0):
            self.last_operation = random.choice(["idle", "rendering", "texture_mapping", "particle_effects", "complex_scene"])
            self.operation_start_time = current_time

        # Update stress based on the current operation and resolution
        base_stress = {
            "idle": random.uniform(5, 15),
            "rendering": random.uniform(30, 50),
            "texture_mapping": random.uniform(40, 60),
            "particle_effects": random.uniform(50, 70),
            "complex_scene": random.uniform(60, 80)
        }[self.last_operation]

        # Adjust stress based on resolution
        resolution_factor = (self.current_resolution[0] * self.current_resolution[1]) / (640 * 240)
        self.stress = min(100, base_stress * resolution_factor)

        # Apply Pony Synth Performance Chip boost
        self.stress /= self.pony_synth_boost

        # Update heat accumulation
        heat_generation = self.stress * 0.1  # Heat generated per second
        self.heat_accumulation += heat_generation * dt

        # Update temperature based on heat accumulation and cooling
        cooling_amount = self.fan_speed * self.cooling_efficiency * 0.1 * dt
        self.heat_accumulation = max(0, self.heat_accumulation - cooling_amount)
        self.temperature = self.ambient_temperature + self.heat_accumulation

        # Adjust fan speed based on temperature
        if self.temperature < 45:
            self.fan_speed = max(20, self.fan_speed - 1)
        elif 45 <= self.temperature < 60:
            self.fan_speed = min(50, self.fan_speed + 1)
        elif 60 <= self.temperature < 70:
            self.fan_speed = min(75, self.fan_speed + 2)
        else:
            self.fan_speed = min(100, self.fan_speed + 3)

        # Simulate VRAM and eDRAM usage based on the current operation
        vram_usage = {
            "idle": random.uniform(10, 20),
            "rendering": random.uniform(30, 50),
            "texture_mapping": random.uniform(40, 60),
            "particle_effects": random.uniform(50, 70),
            "complex_scene": random.uniform(60, 80)
        }[self.last_operation]

        edram_usage = {
            "idle": random.uniform(5, 15),
            "rendering": random.uniform(20, 40),
            "texture_mapping": random.uniform(30, 50),
            "particle_effects": random.uniform(40, 60),
            "complex_scene": random.uniform(50, 70)
        }[self.last_operation]

        self.vram.set_usage(vram_usage)
        self.edram.set_usage(edram_usage)

        # Simulate fill rate and polygon rate variations
        stress_factor = 0.5 + (self.stress / 200)  # 0.5 to 1.0
        self.fill_rate = 2.4 * stress_factor * self.pony_synth_boost
        self.polygon_rate = 66 * stress_factor * self.pony_synth_boost

        # Adjust FPS based on stress and resolution
        max_fps = 60 if self.current_resolution[1] == 240 else 30
        self.current_fps = max(15, min(max_fps, int(60 * (1 - self.stress / 200) * self.pony_synth_boost)))

    def set_resolution(self, width, height, interlaced):
        if (width, height, interlaced) in self.resolution_options:
            self.current_resolution = (width, height)
            return True
        return False

    def get_info(self):
        return {
            "Temp": f"{self.temperature:.1f}°C",
            "Fan": f"{self.fan_speed:.0f}%",
            "Stress": f"{self.stress:.0f}%",
            "Clock": f"{self.clock_speed:.3f}MHz",
            "VRAM": f"{self.vram.get_usage_percentage():.1f}%",
            "eDRAM": f"{self.edram.get_usage_percentage():.1f}%",
            "Fill": f"{self.fill_rate:.2f}GP/s",
            "Poly": f"{self.polygon_rate:.1f}M/s",
            "Res": f"{self.current_resolution[0]}x{self.current_resolution[1]}{'i' if self.current_resolution[1] == 240 else 'p'}",
            "FPS": f"{self.current_fps}",
            "Op": f"{self.last_operation}",
            "TMUs": f"{self.tmus}",
            "ROPs": f"{self.rops}",
            "Pony": f"{(self.pony_synth_boost - 1) * 100:.0f}% boost"
        }