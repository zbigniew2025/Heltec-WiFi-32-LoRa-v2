import time
import random
from machine import Pin, SoftI2C
import ssd1306

WIDTH = 128
HEIGHT = 64
NUM_SNOWFLAKES = 50

OLED_RESET_PIN = 16

i2c = SoftI2C(scl=Pin(15), sda=Pin(4))
oled_reset = Pin(OLED_RESET_PIN, Pin.OUT)
oled_reset.value(0)
time.sleep_ms(50)
oled_reset.value(1)
oled = ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)

snowflakes = []
for _ in range(NUM_SNOWFLAKES):
    x = random.randint(0, WIDTH - 1)
    y = random.randint(0, HEIGHT - 1)
    speed = random.randint(1, 3)
    snowflakes.append([x, y, speed])

while True:
    oled.fill(0)
    for snowflake in snowflakes:
        x, y, speed = snowflake
        oled.pixel(x, y, 1)
        y += speed
        if y >= HEIGHT:
            y = 0
            x = random.randint(0, WIDTH - 1)
            speed = random.randint(1, 3)
        snowflake[0] = x
        snowflake[1] = y
        snowflake[2] = speed
    oled.show()
    time.sleep_ms(50)