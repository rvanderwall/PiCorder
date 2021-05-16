from enum import Enum, unique
from Inputs import BUTTON_A, BUTTON_B, BUTTON_C


@unique
class TricorderMode(Enum):
    LAPTOP = 0
    RASP_PI_DEMO = 1
    RASP_PI_SENSORS = 2


@unique
class OperationMode(Enum):
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


@unique
class Commands(Enum):
    NOOP = 0
    RESET = 1
    RECORD = 2
    NEXT = 3


display_mode_map = {
    OperationMode.INIT: [DisplayMode.SPLASH],
    OperationMode.ENVIRONMENTAL: [DisplayMode.SLIDER, DisplayMode.GRAPH],
    OperationMode.ENVIRONMENTAL2: [DisplayMode.TEXT, DisplayMode.GRAPH],
    OperationMode.POSITIONAL: [DisplayMode.TEXT, DisplayMode.THREE_D],
    OperationMode.AUDIO_VISUAL: [DisplayMode.TEXT],
    OperationMode.RECORDS: [DisplayMode.TEXT, DisplayMode.VIDEO]
}


command_map = {
    OperationMode.INIT: Commands.RESET,
    OperationMode.ENVIRONMENTAL: Commands.RESET,
    OperationMode.ENVIRONMENTAL2: Commands.RESET,
    OperationMode.POSITIONAL: Commands.RESET,
    OperationMode.AUDIO_VISUAL: Commands.RECORD,
    OperationMode.RECORDS: Commands.NEXT
}


class ModeMapper:
    def __init__(self):
        self.current_op_mode = OperationMode.INIT
        self.current_disp_mode_idx = 0
        self._set_disp_mode()

    def enter_mode(self, mode: OperationMode):
        self.current_op_mode = mode
        self.current_disp_mode_idx = 0
        self._set_disp_mode()

    def switch_mode(self, button) -> Commands:
        if button is None:
            return Commands.NOOP

        if button == BUTTON_C:
            command = command_map[self.current_op_mode]
            return command

        # controller needs to take us out of init
        if self.current_op_mode == OperationMode.INIT:
            return Commands.NOOP

        if button == BUTTON_A:
            # Bump Sensor Mode
            cur_val = self.current_op_mode.value
            if cur_val >= OperationMode.RECORDS.value:
                self.current_op_mode = OperationMode.ENVIRONMENTAL
            else:
                self.current_op_mode = OperationMode(cur_val + 1)
            self.enter_mode(self.current_op_mode)

        elif button == BUTTON_B:
            # Bump Display mode
            disp_modes = display_mode_map[self.current_op_mode]
            self.current_disp_mode_idx += 1
            if self.current_disp_mode_idx >= len(disp_modes):
                self.current_disp_mode_idx = 0
            self._set_disp_mode()

        return Commands.NOOP

    def show_mode(self):
        print(f"Current mode: {self.current_op_mode}:{self.current_disp_mode}")

    def _set_disp_mode(self):
        disp_modes = display_mode_map[self.current_op_mode]
        self.current_disp_mode = disp_modes[self.current_disp_mode_idx]
