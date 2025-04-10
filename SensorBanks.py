from Indicator import Indicator, Indicator3D
from Sensor import TempSensor, Temp2Sensor, PressureSensor, HumiditySensor
from Sensor import AltitudeSensor, AccelerationSensor, MagnetometerSensor, ProximitySensor
from Sensor import ColorSensor, SoundSensor

from Displays.IDisplay import RED, RED_ORANGE, SF_YELLOW, WHITE, ORANGE
from ModeTransitions import OperationMode as OpMode


def power_down_sensors():
    try:
        import RPi.GPIO as GPIO
        GPIO.cleanup()
    except:
        pass


#
#  This is really an indicator array, rather than a sensor array
#  but I want to be consistent with terminology from the ST universe.
#
class SensorArray:
    def __init__(self, name):
        self.name = name
        self.sensors = []

    def add_sensor(self, indicator: Indicator):
        self.sensors.append(indicator)
        return self


class SensorBanks:
    def __init__(self):
        self.__sensor_array = {
            OpMode.ENVIRONMENTAL: SensorArray("E1")
                .add_sensor(Indicator("T", TempSensor()).set_x_pos(55).set_color(RED))
                .add_sensor(Indicator("HPA", PressureSensor()).set_x_pos(159).set_color(SF_YELLOW))
                .add_sensor(Indicator("%RH", HumiditySensor()).set_x_pos(262).set_color(WHITE)),

            OpMode.ENVIRONMENTAL2: SensorArray("E2")
                .add_sensor(Indicator("T", TempSensor()).set_color(RED))
                .add_sensor(Indicator("T", Temp2Sensor()).set_color(RED_ORANGE))
                .add_sensor(Indicator("HPA", PressureSensor()).set_color(SF_YELLOW))
                .add_sensor(Indicator("%RH", HumiditySensor()).set_color(WHITE))
                .add_sensor(Indicator("ALT", AltitudeSensor()).set_color(ORANGE)),

            OpMode.POSITIONAL: SensorArray("P1")
                .add_sensor(Indicator3D("ACC", AccelerationSensor()).set_color(RED))
                .add_sensor(Indicator3D("MAG", MagnetometerSensor()).set_color(SF_YELLOW)),

            OpMode.POSITIONAL2: SensorArray("P2")
                .add_sensor(Indicator3D("ACC", AccelerationSensor()).set_color(RED))
                .add_sensor(Indicator3D("MAG", MagnetometerSensor()).set_color(SF_YELLOW))
                .add_sensor(Indicator("PROX", ProximitySensor()).set_color(WHITE)),

            OpMode.AUDIO_VISUAL: SensorArray("AV")
                .add_sensor(Indicator("RGB", ColorSensor()).set_color(RED))
                .add_sensor(Indicator("dB", SoundSensor()).set_color(RED))
        }

    def get_sensor_array(self, sensor_mode: OpMode) -> SensorArray:
        if sensor_mode in self.__sensor_array:
            sensor_bank = self.__sensor_array[sensor_mode]
        else:
            sensor_bank = SensorArray('empty')
        return sensor_bank
