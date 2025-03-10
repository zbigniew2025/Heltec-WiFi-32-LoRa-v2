import machine
import ssd1306
import time

# Konfiguracja I2C (używamy SoftI2C)
i2c = machine.SoftI2C(scl=machine.Pin(15), sda=machine.Pin(4))

# Adres I2C ekranu OLED (domyślnie 0x3C)
oled_address = 0x3C

# Konfiguracja pinu resetu OLED
reset_pin = machine.Pin(16, machine.Pin.OUT)

# Sekwencja resetowania OLED
reset_pin.value(0) # Ustawienie pinu resetu na niski stan
time.sleep_ms(100) # Krótkie opóźnienie
reset_pin.value(1) # Ustawienie pinu resetu na wysoki stan
time.sleep_ms(100) # Krótkie opóźnienie

# Konfiguracja OLED (128x64 pikseli)
oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=oled_address)

# Pętla wyświetlania tekstu
while True:
    oled.fill(0) # Czyszczenie ekranu przed wyświetleniem nowego tekstu
    oled.text("Witaj swiecie!", 0, 0)
    oled.text("MicroPython", 0, 10)
    oled.show()
    time.sleep_ms(100) # Krótkie opóźnienie