import network
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
reset_pin.value(0)
time.sleep_ms(100)
reset_pin.value(1)
time.sleep_ms(100)

# Konfiguracja OLED (128x64 pikseli)
oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=oled_address)

# Konfiguracja WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

def scan_and_display():
    networks = wlan.scan()
    oled.fill(0)
    if networks:
        for i, net in enumerate(networks):
            ssid = net[0].decode('utf-8')
            oled.text(ssid, 0, i * 10)
            if i >= 6: # Maksymalnie 7 sieci na ekranie
                break
    else:
        oled.text("No WiFi found", 0, 0)
    oled.show()

# Początkowe skanowanie i wyświetlanie
scan_and_display()

# Pętla główna z regularnym skanowaniem
while True:
    time.sleep(30)  # Opóźnienie 30 sekund
    scan_and_display()