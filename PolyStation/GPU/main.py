import pygame
import numpy as np
import time
from PS2GPU import PS2GPU
from bufferupdateandcolors import BufferManager, ColorPalette

# Initialize Pygame
pygame.init()

# Set up display (start with 480i resolution)
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("PS2 GPU Simulation")

# Initialize GPU and buffer manager
gpu = PS2GPU()
buffer_manager = BufferManager(width, height)

# Cube vertices
vertices = np.array([
    [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
    [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]
])

# Cube edges
edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]

def rotate_cube(vertices, angle_x, angle_y, angle_z):
    rotation_x = np.array([
        [1, 0, 0],
        [0, np.cos(angle_x), -np.sin(angle_x)],
        [0, np.sin(angle_x), np.cos(angle_x)]
    ])
    rotation_y = np.array([
        [np.cos(angle_y), 0, np.sin(angle_y)],
        [0, 1, 0],
        [-np.sin(angle_y), 0, np.cos(angle_y)]
    ])
    rotation_z = np.array([
        [np.cos(angle_z), -np.sin(angle_z), 0],
        [np.sin(angle_z), np.cos(angle_z), 0],
        [0, 0, 1]
    ])
    return np.dot(vertices, rotation_x).dot(rotation_y).dot(rotation_z)

def project_3d_to_2d(vertices, width, height):
    return [(int(v[0] * 100 + width / 2), int(v[1] * 100 + height / 2)) for v in vertices]

def draw_gpu_info(screen, gpu_info, font):
    y_offset = 10
    for key, value in gpu_info.items():
        text = f"{key}: {value}"
        text_surface = font.render(text, True, (255, 255, 255))
        screen.blit(text_surface, (10, y_offset))
        y_offset += 20

angle_x, angle_y, angle_z = 0, 0, 0

clock = pygame.time.Clock()
running = True

last_update_time = time.time()
font = pygame.font.Font(None, 24)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                gpu.set_resolution(640, 240, True)  # 480i
            elif event.key == pygame.K_2:
                gpu.set_resolution(640, 480, False)  # 480p
            elif event.key == pygame.K_3:
                gpu.set_resolution(320, 240, True)  # 240i

    current_time = time.time()
    dt = current_time - last_update_time
    last_update_time = current_time

    # Clear the screen
    screen.fill((0, 0, 0))
    buffer_manager.clear_buffers()

    # Update GPU simulation
    gpu.update(dt)

    # Rotate and project cube
    rotated_vertices = rotate_cube(vertices, angle_x, angle_y, angle_z)
    projected_vertices = project_3d_to_2d(rotated_vertices, width, height)

    # Draw cube edges
    for edge in edges:
        start = projected_vertices[edge[0]]
        end = projected_vertices[edge[1]]
        color = ColorPalette.get_color(0, 255, 0)  # Green color for edges
        pygame.draw.line(screen, color, start, end, 2)

    # Draw GPU info
    gpu_info = gpu.get_info()
    draw_gpu_info(screen, gpu_info, font)

    pygame.display.flip()

    # Update rotation angles
    angle_x += 0.01
    angle_y += 0.02
    angle_z += 0.03

    # Limit FPS to match GPU's current FPS
    clock.tick(gpu.current_fps)

pygame.quit()