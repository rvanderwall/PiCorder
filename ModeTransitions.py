from enum import Enum, unique
from Inputs import BUTTON_A, BUTTON_B, BUTTON_C


@unique
class TricorderMode(Enum):
    LAPTOP = 0
    RASP_PI_DEMO = 1
    RASP_PI_SENSORS = 2


@unique
class SensorMode(Enum):
    INIT = -1
    ENVIRONMENTAL = 0
    ENVIRONMENTAL2 = 1
    POSITIONAL = 2
    AUDIO_VISUAL = 3
    RECORDS = 4

@unique
class DisplayMode(Enum):
    SPLASH = 0
    SLIDER = 1
    GRAPH = 2
    TEXT = 3
    THREE_D = 4
    VIDEO = 5


display_mode_map = {
    SensorMode.INIT: [DisplayMode.SPLASH],
    SensorMode.ENVIRONMENTAL : [DisplayMode.SLIDER, DisplayMode.GRAPH],
    SensorMode.ENVIRONMENTAL2: [DisplayMode.TEXT, DisplayMode.GRAPH],
    SensorMode.POSITIONAL: [DisplayMode.TEXT, DisplayMode.THREE_D],
    SensorMode.AUDIO_VISUAL: [DisplayMode.TEXT],
    SensorMode.RECORDS: [DisplayMode.TEXT, DisplayMode.VIDEO]
}


class ModeMapper:
    def __init__(self):
        self.current_sensor_mode = SensorMode.INIT
        self.current_disp_mode_idx = 0
        self._set_disp_mode()

    def enter_mode(self, mode: SensorMode):
        self.current_sensor_mode = mode
        self.current_disp_mode_idx = 0
        self._set_disp_mode()

    def switch_mode(self, button):
        if button is None:
            return

        if button == BUTTON_C:
            self.enter_mode(SensorMode.INIT)
            return

        # controller needs to take us out of init
        if self.current_sensor_mode == SensorMode.INIT:
            return

        if button == BUTTON_A:
            # Bump Sensor Mode
            cur_val = self.current_sensor_mode.value
            if cur_val >= SensorMode.RECORDS.value:
                self.current_sensor_mode = SensorMode.ENVIRONMENTAL
            else:
                self.current_sensor_mode = SensorMode(cur_val + 1)
            self.enter_mode(self.current_sensor_mode)

        elif button == BUTTON_B:
            # Bump Display mode
            disp_modes = display_mode_map[self.current_sensor_mode]
            self.current_disp_mode_idx += 1
            if self.current_disp_mode_idx >= len(disp_modes):
                self.current_disp_mode_idx = 0
            self._set_disp_mode()

    def show_mode(self):
        print(f"Current mode: {self.current_sensor_mode}:{self.current_disp_mode}")

    def _set_disp_mode(self):
        disp_modes = display_mode_map[self.current_sensor_mode]
        self.current_disp_mode = disp_modes[self.current_disp_mode_idx]
