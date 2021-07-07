from enum import Enum, unique
from Inputs import BUTTON_A, BUTTON_B, BUTTON_C, BUTTON_QUIT
from Logger import Logger


class TricorderMode:
    def __init__(self):
        self.TFT = False
        self.Demo = False


@unique
class OperationMode(Enum):
    INIT = -1
    ENVIRONMENTAL = 0
    ENVIRONMENTAL2 = 1
    POSITIONAL = 2
    POSITIONAL2 = 3
    AUDIO_VISUAL = 4
    RECORDS = 5
    CONFIGURE = 6
    EXIT = 7


@unique
class DisplayMode(Enum):
    SPLASH = 0
    SLIDER = 1
    GRAPH = 2
    TEXT = 3
    THREE_D = 4
    VIDEO = 5
    MENU = 6


@unique
class Commands(Enum):
    NOOP = 0
    RESET = 1
    RECORD = 2
    NEXT = 3
    CONFIGURE = 4
    TERMINATE = 5
    POWERDOWN = 6


config_menu = [
    "A: Resume",
    "B: Reset",
    "C: Power Down"
]

display_mode_map = {
    OperationMode.INIT: [DisplayMode.SPLASH],
    OperationMode.ENVIRONMENTAL: [DisplayMode.SLIDER, DisplayMode.GRAPH],
    OperationMode.ENVIRONMENTAL2: [DisplayMode.TEXT, DisplayMode.GRAPH],
    OperationMode.POSITIONAL: [DisplayMode.TEXT, DisplayMode.THREE_D],
    OperationMode.POSITIONAL2: [DisplayMode.TEXT, DisplayMode.GRAPH],
    OperationMode.AUDIO_VISUAL: [DisplayMode.TEXT],
    OperationMode.RECORDS: [DisplayMode.TEXT, DisplayMode.VIDEO],
    OperationMode.CONFIGURE: [DisplayMode.MENU]
}


command_map = {
    OperationMode.INIT: Commands.RESET,
    OperationMode.ENVIRONMENTAL: Commands.CONFIGURE,
    OperationMode.ENVIRONMENTAL2: Commands.CONFIGURE,
    OperationMode.POSITIONAL: Commands.CONFIGURE,
    OperationMode.AUDIO_VISUAL: Commands.RECORD,
    OperationMode.RECORDS: Commands.NEXT
}


class ModeMapper:
    def __init__(self, logger: Logger):
        self._lgr = logger
        self._current_op_mode = OperationMode.INIT
        self._current_disp_mode_idx = 0

        self._prev_op_mode = None
        self._prev_disp_mode_idx = None

    def enter_mode(self, mode: OperationMode):
        self._prev_op_mode = self._current_op_mode
        self._prev_disp_mode_idx = self._current_disp_mode_idx
        self._current_op_mode = mode
        self._current_disp_mode_idx = 0

    def switch_mode(self, button) -> Commands:
        # controller needs to take us out of init
        if self._current_op_mode == OperationMode.INIT:
            return Commands.NOOP

        if self._current_op_mode == OperationMode.CONFIGURE:
            return self._process_menu(button)

        if button is None:
            return Commands.NOOP

        if button == BUTTON_A:
            self._bump_op_mode()

        elif button == BUTTON_B:
            self._bump_disp_mode()

        elif button == BUTTON_C:
            command = command_map[self._current_op_mode]
            if command == Commands.CONFIGURE:
                self.enter_mode(OperationMode.CONFIGURE)
            return command

        elif button == BUTTON_QUIT:
            return Commands.TERMINATE

        return Commands.NOOP

    def show_mode(self):
        self._lgr.info(f"Current mode: {self._current_op_mode}:{self.get_disp_mode()}")

    def get_op_mode(self):
        return self._current_op_mode

    def get_disp_mode(self):
        disp_modes = display_mode_map[self._current_op_mode]
        return disp_modes[self._current_disp_mode_idx]

    def _bump_op_mode(self):
        # Move to the next operation mode
        self._prev_op_mode = self._current_op_mode
        self._prev_disp_mode_idx = self._current_disp_mode_idx
        cur_val = self._current_op_mode
        if cur_val == OperationMode.ENVIRONMENTAL:
            self._current_op_mode = OperationMode.ENVIRONMENTAL2
        elif cur_val == OperationMode.ENVIRONMENTAL2:
            self._current_op_mode = OperationMode.POSITIONAL
        elif cur_val == OperationMode.POSITIONAL:
            self._current_op_mode = OperationMode.RECORDS
        elif cur_val == OperationMode.RECORDS:
            self._current_op_mode = OperationMode.ENVIRONMENTAL

        self.enter_mode(self._current_op_mode)

    def _bump_disp_mode(self):
        # Move to the next display mode within this operation mode
        disp_modes = display_mode_map[self._current_op_mode]
        self._current_disp_mode_idx += 1
        if self._current_disp_mode_idx >= len(disp_modes):
            self._current_disp_mode_idx = 0

    def _process_menu(self, button):
        if button == BUTTON_A:
            self._current_op_mode = self._prev_op_mode
            self._current_disp_mode_idx = self._prev_disp_mode_idx
            return Commands.NOOP
        elif button == BUTTON_B:
            return Commands.RESET
        elif button == BUTTON_C:
            return Commands.POWERDOWN
        return Commands.NOOP
