import threading
import time
import RPi.GPIO as GPIO
from config import Config





class Control:
    def __init__(self):
        self.config = Config('config.cfg')
        self.setup_gpio()

    def loop(self):
        print("running")

    # Setup GPIO pins based on the configuration
    def setup_gpio(self):
        try:
            GPIO.setmode(GPIO.BCM)
            for motor in self.config.motor_pins:
                GPIO.setup(motor["pulse"], GPIO.OUT)
                GPIO.setup(motor["direction"], GPIO.OUT)
        except:
            GPIO.cleanup()

# Function to control a specific motor
def move(self, motor_index, direction, distance):
    def run_motor():
        if 0 <= motor_index < len(self.config.motor_pins):
            motor = self.config.motor_pins[motor_index]
            GPIO.output(motor["direction"], GPIO.HIGH if direction == "forward" else GPIO.LOW)

            pwm = GPIO.PWM(motor["pulse"], 500)  # Create a PWM instance on the pulse pin with a frequency of 500Hz
            pwm.start(50)  # Start the PWM signal with a duty cycle of 50%

            # Calculate the number of steps based on the distance and microsteps configuration
            steps = distance * self.config.getint(f"MOTOR_{motor_index}", "steps")

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
        print(landmarks)

