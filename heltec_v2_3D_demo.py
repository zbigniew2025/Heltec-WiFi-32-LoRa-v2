import time
import math
import machine
import ssd1306

# Konfiguracja I2C (używamy SoftI2C)
i2c = machine.SoftI2C(scl=machine.Pin(15), sda=machine.Pin(4))

# Adres I2C ekranu OLED (domyślnie 0x3C)
oled_address = 0x3C

# Konfiguracja pinu resetu OLED
reset_pin = machine.Pin(16, machine.Pin.OUT)

# Sekwencja resetowania OLED
reset_pin.value(0)
time.sleep_ms(100)
reset_pin.value(1)
time.sleep_ms(100)

# Konfiguracja OLED (128x64 pikseli)
oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=oled_address)

# Definicja wierzchołków sześcianu
vertices = [
    (-0.5, -0.5, -0.5),
    (0.5, -0.5, -0.5),
    (0.5, 0.5, -0.5),
    (-0.5, 0.5, -0.5),
    (-0.5, -0.5, 0.5),
    (0.5, -0.5, 0.5),
    (0.5, 0.5, 0.5),
    (-0.5, 0.5, 0.5),
]

# Definicja krawędzi sześcianu
edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7),
]

# Funkcja do obracania punktu
def rotate_point(point, angle_x, angle_y, angle_z):
    x, y, z = point
    sin_x, cos_x = math.sin(angle_x), math.cos(angle_x)
    sin_y, cos_y = math.sin(angle_y), math.cos(angle_y)
    sin_z, cos_z = math.sin(angle_z), math.cos(angle_z)

    new_y = y * cos_x - z * sin_x
    new_z = y * sin_x + z * cos_x
    new_x = x * cos_y + new_z * sin_y
    new_z = -x * sin_y + new_z * cos_y
    new_x_final = new_x * cos_z - new_y * sin_z
    new_y_final = new_x * sin_z + new_y * cos_z

    return new_x_final, new_y_final, new_z

# Funkcja do rysowania linii
def draw_line(x1, y1, x2, y2, color):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    while True:
        oled.pixel(x1, y1, color)
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy

# Funkcja do rysowania sześcianu
def draw_cube(angle_x, angle_y, angle_z):
    rotated_vertices = []
    for vertex in vertices:
        rotated_vertices.append(rotate_point(vertex, angle_x, angle_y, angle_z))

    for edge in edges:
        v1, v2 = rotated_vertices[edge[0]], rotated_vertices[edge[1]]
        x1, y1, z1 = v1
        x2, y2, z2 = v2

        # Rzutowanie perspektywiczne
        scale = 5
        if z1 != 0:
            x1 = int(x1 * scale / (z1 + 3) * 15 + 64)
            y1 = int(y1 * scale / (z1 + 3) * 15 + 32)
        if z2 != 0:
            x2 = int(x2 * scale / (z2 + 3) * 15 + 64)
            y2 = int(y2 * scale / (z2 + 3) * 15 + 32)

        draw_line(x1, y1, x2, y2, 1)

# Tekst do scrollowania
scroll_text = "Hello! This is Heltec LoRa WiFi 32 v2 demo in 3D!"
scroll_offset = 0

# Główna pętla
angle_x, angle_y, angle_z = 0, 0, 0
while True:
    oled.fill(0)
    draw_cube(angle_x, angle_y, angle_z)

    # Scrollowanie tekstu
    for i in range(len(scroll_text)):
        char_x = (i * 8) - scroll_offset
        if char_x >= -8 and char_x < 128:
            oled.text(scroll_text[i], char_x, 56, 1)

    oled.show()

    angle_x += 0.05
    angle_y += 0.03
    angle_z += 0.02
    scroll_offset += 1
    if scroll_offset > len(scroll_text) * 8:
        scroll_offset = 0

    time.sleep(0.05)