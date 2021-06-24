from abc import ABC, abstractmethod
from math import sin, cos
import time
from Logger import Logger


try:
    import board
    import adafruit_sht31d
    import adafruit_bmp280
    import adafruit_lsm303_accel
    import adafruit_lis2mdl
    SENSOR_MODE = "Operational"
except Exception as ex:
    SENSOR_MODE = "Emulation"

lg = Logger("Startup")
lg.info(f"Entering sensor {SENSOR_MODE} mode")


class Sensor(ABC):
    def __init__(self, min_val: float, max_val: float):
        self.min = min_val
        self.max = max_val
        self.info = ""

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
        self.info = "Temperature degrees C"

    def get_emulation_sensor_value(self):
        ts = time.time() * 10
        return 30.0 + 5 * sin(ts / 10)

    def get_real_sensor_value(self):
        sht_sensor = get_sht_sensor()
        t1 = sht_sensor.temperature
        return t1


#
#  Temp from BMP sensor can be used as double check on T1
#
class Temp2Sensor(Sensor):
    def __init__(self):
        super().__init__(min_val=-40.0, max_val=120.0)
        self.info = "Alt temp sensor"

    def get_emulation_sensor_value(self):
        ts = time.time() * 10
        return 30.0 + 5 * sin(ts / 12)

    def get_real_sensor_value(self):
        bmp_sensor = get_bmp_sensor()
        t2 = bmp_sensor.temperature
        return t2


#
#  The min and max are already rendered in the background image
#
class HumiditySensor(Sensor):
    def __init__(self):
        super().__init__(min_val=0.00, max_val=100)
        self.info = "Relative Humidity"

    def get_emulation_sensor_value(self):
        return 45

    def get_real_sensor_value(self):
        sensor = get_sht_sensor()
        h = sensor.relative_humidity
        return h


#
#  The min and max are already rendered in the background image
#
class PressureSensor(Sensor):
    def __init__(self):
        super().__init__(min_val=280, max_val=1280)
        self.info = "Pressure mm Hg"

    def get_emulation_sensor_value(self):
        ts = time.time() * 10
        return 980.0 + 50 * cos(ts / 20)

    def get_real_sensor_value(self):
        sensor = get_bmp_sensor()
        p = sensor.pressure
        return p


#
#  For this to be accurate, the sea_level_pressure must be set.
#
class AltitudeSensor(Sensor):
    def __init__(self):
        super().__init__(min_val=-100, max_val=5000)
        self.info = "Altitude in meters"

    def get_emulation_sensor_value(self):
        ts = time.time() * 10
        return 1000.0 + 500 * cos(ts / 23)

    def get_real_sensor_value(self):
        sensor = get_bmp_sensor()
        a = sensor.altitude
        return a


#
#  3D Sensor - Up to 10G (9.8 X 10 ~ 100
#
class AccelerationSensor(Sensor):
    def __init__(self):
        super().__init__(min_val=-100.0, max_val=100.0)
        self.info = "Acceleration m/sec^2"

    def get_emulation_sensor_value(self):
        # return (1.0, 0.0, 0.0)
        return 9.8, 50.0, -75.5

    def get_real_sensor_value(self):
        sensor = get_lsm_sensors()
        accel = sensor.acceleration
        return accel


#
#  3D Sensor - Not sure of the max/min
#
class MagnetometerSensor(Sensor):
    def __init__(self):
        super().__init__(min_val=-5.0, max_val=5.0)
        self.info = "Magnetic flux in mT"

    def get_emulation_sensor_value(self):
        return 125.0, -100.0, 500.0

    def get_real_sensor_value(self):
        sensor = get_lis_sensor()
        m = sensor.magnetic
        return m


class ProximitySensor(Sensor):
    def __init__(self):
        super().__init__(min_val=0, max_val=5000)

    def get_emulation_sensor_value(self):
        return 123

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


def get_sht_sensor():
    # temperature, relative_humidity
    i2c = board.I2C()
    sensor = adafruit_sht31d.SHT31D(i2c)
    return sensor


def get_bmp_sensor():
    # temperature, pressure, altitude
    i2c = board.I2C()
    sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
    sensor.sea_level_pressure = 1013.25
    return sensor


def get_lsm_sensors():
    # acceleration
    i2c = board.I2C()
    accel = adafruit_lsm303_accel.LSM303_Accel(i2c)
    return accel


def get_lis_sensor():
    # magnetic
    i2c = board.I2C()
    mag = adafruit_lis2mdl.LIS2MDL(i2c)
    return mag
