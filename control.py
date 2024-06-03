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

        self.angle = 0
        self.len_arms = [108, 150, 174, 36] # Base-First, First-Second, Second-Third, Third-Fourth



    # Setup GPIO pins based on the configuration
    def setup_gpio(self):
        GPIO.setmode(GPIO.BCM)
        for motor in self.config.motor_pins:
            GPIO.setup(motor["pulse"], GPIO.OUT)
            GPIO.setup(motor["direction"], GPIO.OUT)
            # LOW ACTIVE, NEED to be HIGH to start
            GPIO.output(motor["pulse"], GPIO.HIGH)
            GPIO.output(motor["direction"], GPIO.HIGH)




    # Function to control a specific motor
    def move(self, motor_index, direction, distance=0, angle=0):

        motor = self.config.motor_pins[4]
        steps = 40


        for _ in range(steps):
            GPIO.output(motor["pulse"], GPIO.LOW)
            time.sleep(0.01)
            GPIO.output(motor["pulse"], GPIO.HIGH)

        # FOr testing

        # time.sleep(3)
        # GPIO.output(motor["pulse"], GPIO.HIGH)

        if 1 == 1:
            return
        def run_motor():
            if 0 <= motor_index < len(self.config.motor_pins):
                motor = self.config.motor_pins[motor_index]
                GPIO.output(motor["direction"], GPIO.HIGH if direction == "forward" else GPIO.LOW)

                pwm = GPIO.PWM(motor["pulse"], 500)  # Create a PWM instance on the pulse pin with a frequency of 500Hz
                pwm.start(50)  # Start the PWM signal with a duty cycle of 50%

                # Calculate the number of steps based on the distance and microsteps configuration
                if angle==0:
                    steps = distance * self.config.getint(f"MOTOR_{motor_index}", "steps")
                elif distance == 0:
                    steps = angle * self.config.getint(f"MOTOR_{motor_index}", "steps") / 360

                for _ in range(steps):
                    # Toggle the pulse pin to move the motor
                    GPIO.output(motor["pulse"], GPIO.HIGH)
                    time.sleep(0.001)  # Adjust this delay to control the speed of the motor
                    GPIO.output(motor["pulse"], GPIO.LOW)
                    time.sleep(0.001)

                pwm.stop()  # Stop the PWM signal
            else:
                raise ValueError("Invalid motor index")

        # Start the motor control operation in a separate thread
        motor_thread = threading.Thread(target=run_motor)
        motor_thread.start()


    def update(self, landmarks):
        joint = landmarks[0][0]
        # Clamp to a range of 0-1, and invert the axis
        x = 1 - max(0, min(1, joint["x"]))
        y = 1 - max(0, min(1, joint["y"]))
        z = 1 - max(0, min(1, joint["z"]))

        # Calculate the distance moved in each axis
        dx = x - self.x
        dy = y - self.y
        dz = z - self.z



        # TODO: Currently only the base moves, via x and y position of hand, add z movement of hand with motors 1 and 2
        # If distance is greater than a threshold, update the position
        if abs(dx) > 0.03 or abs(dy) > 0.03:

            # print({"dx": dx, "dy": dy})
            # Calculate angle and direction to move
            direction = "forward"


            center = 0.5

            new_angle = math.atan2(x - center, y) * 180 / math.pi

            d_angle = new_angle - self.angle
            print({"angle": new_angle, "Moved": d_angle})

            self.x = x
            self.y = y
            self.angle = new_angle

            self.move(0, direction, angle=d_angle)



        # print(joint)

