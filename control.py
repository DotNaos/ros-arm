import threading
import time
import RPi.GPIO as GPIO
import math
from config import Config


class Control:
    def __init__(self):
        self.config = Config('config.cfg')
        self.setup_gpio()

        self.x = 0.5
        self.y = 0.5
        self.z = 0.5

        self.d_angle = 0

        self.angle = 0

        # USED FOR Z AXis
        # self.len_arms = [108, 150, 174, 36] # Base-First, First-Second, Second-Third, Third-Fourth


    def loop(self):
        while 1:
            # print(self.angle)

            if 1 == 0:
                continue
            # threading.Event().wait(0.1)
            if self.d_angle != 0:
                # TODO: HIER KANN MAN ZUM TESTEN DEN MOTOR ÄNDERN
                motor = self.config.motor_pins[0]
                # Set direction
                GPIO.output(motor["direction"], GPIO.HIGH if self.d_angle > 0 else GPIO.LOW)

                # Calculate steps, and get absolute value
                steps = abs(math.floor(self.d_angle / 1.8))

                self.steps(motor["pulse"], steps)

                self.d_angle = 0

    # Setup GPIO pins based on the configuration
    def setup_gpio(self):
        GPIO.setmode(GPIO.BCM)
        for motor in self.config.motor_pins:
            GPIO.setup(motor["pulse"], GPIO.OUT)
            GPIO.setup(motor["direction"], GPIO.OUT)
            # LOW ACTIVE, NEED to be HIGH to start
            GPIO.output(motor["pulse"], GPIO.HIGH)
            GPIO.output(motor["direction"], GPIO.HIGH)


    def steps(self, pin, count):
        for i in range(count):
            GPIO.output(pin, GPIO.LOW)
            time.sleep(0.01)
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(0.01)

    def update(self, landmarks):
        joint = landmarks[0][0]
        # Clamp to a range of 0-1, and invert the axis
        x = 1 - max(0, min(1, joint["x"]))
        y = 1 - max(0, min(1, joint["y"]))
        # z = 1 - max(0, min(1, joint["z"]))

        # Calculate the distance moved in each axis
        # dx = x - self.x
        # dy = y - self.y
        # dz = z - self.z


        # TODO: Currently only the base moves, via x and y position of hand, add z movement of hand with motors 1 and 2
        # If distance is greater than a threshold, update the position
        # if abs(dx) > 0.03 or abs(dy) > 0.03:

        # print({"dx": dx, "dy": dy})
        # Calculate angle and direction to move


        center = 0.5

        new_angle = math.atan2(x - center, y) * 180 / math.pi

        self.d_angle = new_angle - self.angle
        # print({"angle": new_angle, "Moved": d_angle})

        self.x = x
        self.y = y
        self.angle = new_angle





        # print(joint)

