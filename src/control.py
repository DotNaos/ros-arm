import RPi.GPIO as GPIO
import asyncio
from src.config import Config

config = Config('config.cfg')

# Setup GPIO pins based on the configuration
def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    for motor in config.motor_pins:
        GPIO.setup(motor["pulse"], GPIO.OUT)
        GPIO.setup(motor["direction"], GPIO.OUT)

# Function to control a specific motor
async def control_motor(motor_index, direction, duration):
    if 0 <= motor_index < len(config.motor_pins):
        motor = config.motor_pins[motor_index]
        GPIO.output(motor["direction"], direction)
        GPIO.output(motor["pulse"], GPIO.HIGH)
        await asyncio.sleep(duration)
        GPIO.output(motor["pulse"], GPIO.LOW)
    else:
        raise ValueError("Invalid motor index")

# Initialize the GPIO setup
setup_gpio()
