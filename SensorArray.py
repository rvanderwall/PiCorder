from enum import Enum, unique
from Indicator import Indicator
from Sensor import TempSensor, PressureSensor, HumiditySensor
from Sensor import AltitudeSensor, AccelerationSensor, MagnetometerSensor, ProximitySensor
from Sensor import ColorSensor, SoundSensor

from Display import RED, SF_YELLOW, WHITE, ORANGE
from ModeTransitions import OperationMode


@unique
class SensorType(Enum):
    # Environmental sensors / Bank 0
    TEMP = 1
    PRESSURE = 2
    HUMIDITY = 3
    ALTITUDE = 4

    # Positional sensors / Bank 1
    ACCELEROMETER = 5
    MAGNETOMETER = 6
    PROXIMITY = 7

    # Light / Bank 2
    RGB_COLOR = 8
    SOUND = 9


#
#  This is really an indicator array, rather than a sensor array
#  but I want to be consistent with terminology from the ST universe.
#
class SensorArray:
    def __init__(self):
        self.__sensor_array = {
            OperationMode.ENVIRONMENTAL: {
                SensorType.TEMP: Indicator("T", TempSensor()).set_pos(55).set_color(RED),
                SensorType.PRESSURE: Indicator("HPA", PressureSensor()).set_pos(159).set_color(SF_YELLOW),
                SensorType.HUMIDITY: Indicator("%RH", HumiditySensor()).set_pos(262).set_color(WHITE)
            },
            OperationMode.ENVIRONMENTAL2: {
                SensorType.TEMP: Indicator("T", TempSensor()).set_color(RED),
                SensorType.PRESSURE: Indicator("HPA", PressureSensor()).set_color(SF_YELLOW),
                SensorType.HUMIDITY: Indicator("%RH", HumiditySensor()).set_color(WHITE),
                SensorType.ALTITUDE: Indicator("ALT", AltitudeSensor()).set_color(ORANGE)
            },
            OperationMode.POSITIONAL: {
                SensorType.ACCELEROMETER: Indicator("ACC", AccelerationSensor()).set_color(RED),
                SensorType.MAGNETOMETER: Indicator("MAG", MagnetometerSensor()).set_color(SF_YELLOW),
                SensorType.PROXIMITY: Indicator("PROX", ProximitySensor()).set_color(WHITE),
            },
            OperationMode.AUDIO_VISUAL: {
                SensorType.RGB_COLOR: Indicator("RGB", ColorSensor()).set_color(RED),
                SensorType.SOUND: Indicator("dB", SoundSensor()).set_color(RED),
            }
        }

    def get_sensor_bank(self, sensor_mode: OperationMode):
        if sensor_mode in self.__sensor_array:
            sensor_bank = self.__sensor_array[sensor_mode]
        else:
            sensor_bank = []
        return sensor_bank
