from abc import ABC, abstractmethod
from math import sin, cos
import time
from Logger import Logger

try:
    import board
    import adafruit_sht31d
    import Adafruit_GPIO.SPI as SPI
    import Adafruit_SSD1306 as SSD
    SENSOR_MODE = "Operational"
    lg = Logger("Startup")
    lg.info("Entering operational sensor mode")
except:
    SENSOR_MODE = "Emulation"
    lg = Logger("Startup")
    lg.info("Entering sensor emulation mode")


class Sensor(ABC):
    def __init__(self, min_val: float, max_val: float):
        self.min = min_val
        self.max = max_val

    def get_sensor_value(self):
        if SENSOR_MODE == "Operational":
            return self.get_real_sensor_value()
        else:
            return self.get_emulation_sensor_value()

    @abstractmethod
    def get_emulation_sensor_value(self):
        pass

    @abstractmethod
    def get_real_sensor_value(self):
        pass


#
#  The min and max are already rendered in the background image
#
class TempSensor(Sensor):
    def __init__(self):
        super().__init__(min_val=-40.0, max_val=120.0)

    def get_emulation_sensor_value(self):
       ts = time.time() * 10
       return 30.0 + 5 * sin(ts / 10)

    def get_real_sensor_value(self):
        sensor = get_sensor()
        c = sensor.temperature
        return c


class PressureSensor(Sensor):
    def __init__(self):
        super().__init__(min_val=280, max_val=1280)

    def get_emulation_sensor_value(self):
        ts = time.time() * 10
        return 980.0 + 50 * cos(ts / 20)

    def get_real_sensor_value(self):
        return 0.00


class HumiditySensor(Sensor):
    def __init__(self):
        super().__init__(min_val=0.00, max_val=100)

    def get_emulation_sensor_value(self):
        return 45

    def get_real_sensor_value(self):
        sensor = get_sensor()
        h = sensor.relative_humidity
        return h


class AltitudeSensor(Sensor):
    def __init__(self):
        super().__init__(min_val=-100, max_val=5000)

    def get_emulation_sensor_value(self):
        ts = time.time() * 10
        return 1000.0 + 500 * cos(ts / 23)

    def get_real_sensor_value(self):
        return 0.0


class ProximitySensor(Sensor):
    def __init__(self):
        super().__init__(min_val=0, max_val=5000)

    def get_emulation_sensor_value(self):
        return 123

    def get_real_sensor_value(self):
        return 0.0


class AccelerationSensor(Sensor):
    def __init__(self):
        super().__init__(min_val=-5.0, max_val=5.0)

    def get_emulation_sensor_value(self):
        # return (1.0, 0.0, 0.0)
        return 1.0

    def get_real_sensor_value(self):
        return 0.0


class MagnetometerSensor(Sensor):
    def __init__(self):
        super().__init__(min_val=-5.0, max_val=5.0)

    def get_emulation_sensor_value(self):
        # return (0.5, 0.5, 0.0)
        return 0.5

    def get_real_sensor_value(self):
        return 0.0


class ColorSensor(Sensor):
    def __init__(self):
        super().__init__(min_val=0, max_val=255)

    def get_emulation_sensor_value(self):
        # return (200, 100, 50)
        return 200

    def get_real_sensor_value(self):
        return 0.0


class SoundSensor(Sensor):
    def __init__(self):
        super().__init__(min_val=0, max_val=150)

    def get_emulation_sensor_value(self):
        return 95

    def get_real_sensor_value(self):
        return 0.0


def get_sensor():
    i2c = board.I2C()
    sensor = adafruit_sht31d.SHT31D(i2c)
    return sensor

