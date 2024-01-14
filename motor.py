# GPIO-Bibliothek laden
import json
import RPi.GPIO as GPIO
import time
import numpy as np


class Motor_control:
    def __init__(self):
        self.vertecies = np.zeros((self.max_hands, 21, 3))
        self._vertecies = np.zeros((self.max_hands, 21, 3))
        # BCM-Nummerierung verwenden
        GPIO.setmode(GPIO.BCM)

        # GPIO 17 (Pin 11) als Ausgang setzen
        GPIO.setup(24, GPIO.OUT)
        GPIO.setup(23, GPIO.OUT)

        # GPIO 17 (Pin 11) auf HIGH setzen

        # GPIO 17 (Pin 11) auf LOW setzen
        GPIO.output(23, False)

        while 1:
            GPIO.output(24, False)
            time.sleep(1)
            GPIO.output(24, True)
            time.sleep(1)

        # Benutzte GPIOs freigeben
        GPIO.cleanup()


    def move(self):
        print(self.vertecies)



    def update(self, message):
        self.data = json.loads(message)
        if (self.data["landmarks"] == []):
            return

        handcount = min(, len(self.data["landmarks"]))

        for n in range(handcount):
          for i in range(len(self.data["landmarks"][n])):
              for j in range(3):
                  key = 'x' if j == 0 else 'y' if j == 1 else 'z'
                  self.vertecies[n][i][j] = self.data["landmarks"][n][i][key]


