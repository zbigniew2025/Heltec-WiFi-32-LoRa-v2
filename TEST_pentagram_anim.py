import time
import math
from machine import Pin, SoftI2C
import ssd1306

WIDTH = 128
HEIGHT = 64
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2
RADIUS = 30

OLED_RESET_PIN = 16

i2c = SoftI2C(scl=Pin(15), sda=Pin(4))
oled_reset = Pin(OLED_RESET_PIN, Pin.OUT)
oled_reset.value(0)
time.sleep_ms(50)
oled_reset.value(1)
oled = ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)

def draw_pentagram(angle_offset):
    points = []
    for i in range(5):
        angle = math.pi * (2 * i / 5 - 1 / 2) + angle_offset
        x = int(CENTER_X + RADIUS * math.cos(angle))
        y = int(CENTER_Y + RADIUS * math.sin(angle))
        points.append((x, y))

    for i in range(5):
        x1, y1 = points[i]
        x2, y2 = points[(i + 2) % 5]
        dx = x2 - x1
        dy = y2 - y1
        steps = max(abs(dx), abs(dy))
        for j in range(steps + 1):
            x = int(x1 + dx * j / steps)
            y = int(y1 + dy * j / steps)
            oled.pixel(x, y, 1)

angle = 0
while True:
    oled.fill(0)
    draw_pentagram(angle)
    oled.show()
    angle += 0.1  # Prędkość obrotu (możesz dostosować)
    time.sleep_ms(50)  # Opóźnienie (możesz dostosować)