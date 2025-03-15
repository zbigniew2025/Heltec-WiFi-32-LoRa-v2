import network
import socket
import machine
import ssd1306
import time

# Konfiguracja Wi-Fi
ssid = "WIFI NAME"
password = "password"
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Konfiguracja I2C i OLED
i2c = machine.SoftI2C(scl=machine.Pin(15), sda=machine.Pin(4))
oled_address = 0x3C
reset_pin = machine.Pin(16, machine.Pin.OUT)
reset_pin.value(0)
time.sleep_ms(100)
reset_pin.value(1)
time.sleep_ms(100)

try:
    oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=oled_address)
    print("Wyświetlacz OLED zainicjalizowany")
except OSError as e:
    print("Błąd inicjalizacji wyświetlacza OLED: {}".format(e))
    oled = None

oled.fill(0)
oled.text("Laczenie z WiFi...", 0, 0)
oled.show()

wlan.connect(ssid, password)

# Czekaj na połączenie Wi-Fi
while not wlan.isconnected():
    print("Oczekiwanie na połączenie Wi-Fi...")
    time.sleep(1)

print("Połączono z Wi-Fi")

oled.fill(0)
oled.text("Polaczono z WiFi", 0, 0)
oled.text("Laczenie z IRC...", 0, 8)
oled.show()

# Konfiguracja IRC
server = "IRC.server.addres.net"
port = 6667
nickname = "yournick"
channel = "#channel0190"

def wrap_text(text, max_chars_per_line):
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        if len(current_line + word) <= max_chars_per_line:
            current_line += word + " "
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    lines.append(current_line.strip())
    return lines

def connect_to_irc():
    try:
        s = socket.socket()
        addr = socket.getaddrinfo(server, port)[0][-1]
        s.connect(addr)
        print("Połączono z serwerem IRC")
        s.send("NICK {}\r\n".format(nickname).encode())
        s.send("USER {} 0 * :{}\r\n".format(nickname, nickname).encode())
        s.send("JOIN {}\r\n".format(channel).encode())
        print("Zalogowano i dołączono do kanału")
        return s
    except OSError as e:
        print("Błąd połączenia z serwerem IRC: {}".format(e))
        return None

s = connect_to_irc()

messages = []
last_ping = time.ticks_ms()
scroll_offset = 0
scroll_time = 0
prg_button = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)

if s and oled:
    while True:
        try:
            # Wysyłanie PING co 60 sekund
            if time.ticks_diff(time.ticks_ms(), last_ping) > 60000:
                s.send("PING :keepalive\r\n".encode())
                last_ping = time.ticks_ms()
                print("Wysłano PING")

            data = s.recv(1024)
            if data:
                message = data.decode()
                print("Odebrano: {}".format(message.strip()))
                if "PING" in message:
                    pong_message = message.replace("PING", "PONG")
                    s.send(pong_message.encode())
                    print("Wysłano PONG")
                elif "PRIVMSG #c-64 :" in message:
                    parts = message.split(":", 2)
                    if len(parts) == 3:
                        nick = parts[1].split("!")[0]
                        text = parts[2].split("PRIVMSG #c-64 :")[-1].strip()
                        messages.append("{}: {}".format(nick, text))
                        if len(messages) > 8:
                            messages.pop(0)

            # Obsługa przycisku PRG
            if prg_button.value() == 0:
                scroll_offset = max(0, scroll_offset + 1)
                scroll_time = time.ticks_ms()
                while prg_button.value() == 0:
                    time.sleep_ms(10)

            # Automatyczne przewijanie do bieżącej linii
            if time.ticks_diff(time.ticks_ms(), scroll_time) > 6000:
                scroll_offset = 0

            oled.fill(0)
            line_count = 0
            for msg in messages:
                lines = wrap_text(msg, 128 // 8)
                for line in lines:
                    if line_count >= scroll_offset and line_count < scroll_offset + 8:
                        oled.text(line, 0, (line_count - scroll_offset) * 8)
                    line_count += 1
            oled.show()

            time.sleep(0.1)
        except OSError as e:
            print("Błąd odbierania wiadomości: {}".format(e))
            s.close()
            s = connect_to_irc()
            if not s:
                time.sleep(5)