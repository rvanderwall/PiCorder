from abc import ABC, abstractmethod
from math import sin, cos
import time


class Sensor(ABC):
    def __init__(self, min_val: float, max_val: float):
        self.min = min_val
        self.max = max_val

    @abstractmethod
    def get_sensor_value(self):
        pass


#
#  The min and max are already rendered in the background image
#
class TempSensor(Sensor):
    def __init__(self):
        super().__init__(min_val=-40.0, max_val=120.0)

    def get_sensor_value(self):
        ts = time.time() * 10
        return 30.0 + 5 * sin(ts / 10)


class PressureSensor(Sensor):
    def __init__(self):
        super().__init__(min_val=280, max_val=1280)

    def get_sensor_value(self):
        ts = time.time() * 10
        return 980.0 + 50 * cos(ts / 20)


class HumiditySensor(Sensor):
    def __init__(self):
        super().__init__(min_val=0.00, max_val=1.00)

    def get_sensor_value(self):
        return .45


class AltitudeSensor(Sensor):
    def __init__(self):
        super().__init__(min_val=-100, max_val=5000)

    def get_sensor_value(self):
        ts = time.time() * 10
        return 1000.0 + 500 * cos(ts / 23)


class ProximitySensor(Sensor):
    def __init__(self):
        super().__init__(min_val=0, max_val=5000)

    def get_sensor_value(self):
        return 123


class AccelerationSensor(Sensor):
    def __init__(self):
        super().__init__(min_val=-5.0, max_val=5.0)

    def get_sensor_value(self):
        return 1.0
#        return (1.0, 0.0, 0.0)


class MagnetometerSensor(Sensor):
    def __init__(self):
        super().__init__(min_val=-5.0, max_val=5.0)

    def get_sensor_value(self):
        return 0.5
#        return (0.5, 0.5, 0.0)


class ColorSensor(Sensor):
    def __init__(self):
        super().__init__(min_val=0, max_val=255)

    def get_sensor_value(self):
        return 200
#        return (200, 100, 50)


class SoundSensor(Sensor):
    def __init__(self):
        super().__init__(min_val=0, max_val=150)

    def get_sensor_value(self):
        return 95