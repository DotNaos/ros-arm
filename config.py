import configparser

class Config:
    def __init__(self, config_file):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.motor_pins = [
            {"pulse": self.config.getint("MOTOR_0", "pulse_pin"), "direction": self.config.getint("MOTOR_0", "direction_pin")},
            {"pulse": self.config.getint("MOTOR_1", "pulse_pin"), "direction": self.config.getint("MOTOR_1", "direction_pin")},
            {"pulse": self.config.getint("MOTOR_2", "pulse_pin"), "direction": self.config.getint("MOTOR_2", "direction_pin")},
            {"pulse": self.config.getint("MOTOR_3", "pulse_pin"), "direction": self.config.getint("MOTOR_3", "direction_pin")},
            {"pulse": self.config.getint("MOTOR_4", "pulse_pin"), "direction": self.config.getint("MOTOR_4", "direction_pin")}
        ]
