import time
import machine

# Konfiguracja pinu PWM
pwm_pin = machine.Pin(2)  # Wybierz dowolny pin GPIO
pwm = machine.PWM(pwm_pin)

# Definicja nut i ich częstotliwości (dostosowane do Axel F)
notes = {
    "F4": 349,
    "G4": 392,
    "A4": 440,
    "B4": 494,
    "C5": 523,
    "D5": 587,
    "E5": 659,
    "F5": 698,
}

# Definicja melodyjki Axel F (nuty i ich czasy trwania)
melody = [
    ("F4", 0.25), ("F4", 0.25), ("G4", 0.5), ("F4", 0.25), ("A4", 0.5),
    ("F4", 0.25), ("F4", 0.25), ("G4", 0.5), ("F4", 0.25), ("B4", 0.5),
    ("F4", 0.25), ("F4", 0.25), ("G4", 0.5), ("F4", 0.25), ("C5", 0.5),
    ("A4", 0.25), ("A4", 0.25), ("G4", 0.5), ("F4", 0.25), ("D5", 0.5),
]

# Funkcja do odtwarzania nuty
def play_note(note, duration):
    if note in notes:
        frequency = notes[note]
        pwm.freq(frequency)
        pwm.duty(512)  # 50% wypełnienia
        time.sleep(duration)
    pwm.duty(0)  # Wyłączenie sygnału

# Główna pętla
while True:
    for note, duration in melody:
        play_note(note, duration)
    time.sleep(1)  # Krótka pauza między powtórzeniami