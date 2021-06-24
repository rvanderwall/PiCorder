from time import sleep
import pygame

from Assets import Assets
from Display import Display, TFT_ALLOWED
from Logger import Logger
from ModeTransitions import ModeMapper, Commands
from ModeTransitions import TricorderMode, OperationMode
from Records import Records
from SensorArray import SensorArray


def build_tricorder(hw_mode):
    logger = Logger("Tricorder")
    assets = Assets()
    mode_mapper = ModeMapper(logger)
    mode = Tricorder.get_mode(hw_mode, TFT_ALLOWED)
    display = Display(logger, assets, tft_mode=mode.TFT)
    sensor_array = SensorArray()
    tricorder = Tricorder(logger, display, sensor_array, mode_mapper, mode)
    tricorder._records = Records(assets)
    return tricorder


class Tricorder:
    def __init__(self, logger: Logger, display: Display, sensor_array: SensorArray,
                 mode_mapper: ModeMapper, mode: TricorderMode):
        self.logger = logger

        self._display = display
        self._sensor_array = sensor_array
        self._mode_mapper = mode_mapper

        self._outputs = None
        self._records = None

        self.mode = mode

    @staticmethod
    def get_mode(hw_mode, tft_allowed):
        mode = TricorderMode()
        if hw_mode & 1:
            mode.TFT = True
        elif hw_mode & 2:
            mode.Demo = True

        if not tft_allowed:
            mode.TFT = False

        return mode

    def update_sensors(self):
        sensor_bank = self._sensor_array.get_sensor_bank(self._operating_mode())
        for sensor_type in sensor_bank:
            sensor = sensor_bank[sensor_type]
            sensor.update_value()

    def update_display(self):
        disp_mode = self._display_mode()
        sensor_mode = self._operating_mode()
        if sensor_mode == OperationMode.RECORDS:
            current_record = self._records.get_current_record()
            self._display.update(disp_mode, current_record)
        elif sensor_mode == OperationMode.INIT:
            self._display.update(disp_mode, [])
        else:
            sensor_bank = self._sensor_array.get_sensor_bank(self._operating_mode())
            self._display.update(disp_mode, sensor_bank)

    def process_button_press(self, button_press):
        if button_press is not None:
            self._switch_display_modes(button_press)

    def refresh(self):
        self._display.tick_display()
        if self._operating_mode() == OperationMode.INIT:
            self._restart()

    def _switch_display_modes(self, button):
        command = self._mode_mapper.switch_mode(button)
        self._mode_mapper.show_mode()
        self._process_command(command)

    def _process_command(self, command: Commands):
        if command == Commands.RESET:
            self._mode_mapper.enter_mode(OperationMode.INIT)
        elif command == Commands.RECORD:
            self.logger.error("Cannot record yet")
        elif command == Commands.NEXT:
            self._records.next_record()
        elif command == Commands.TERMINATE:
            pass
        else:
            pass

    def _restart(self):
        self.update_display()
        pygame.event.get()      # Release control back to event loop to update display
        self._mode_mapper.enter_mode(OperationMode.ENVIRONMENTAL)
        self._init_sensors()

    @staticmethod
    def _init_sensors():
        # Just give time for them to warm up
        sleep(2)

    def _operating_mode(self):
        return self._mode_mapper.current_op_mode

    def _display_mode(self):
        return self._mode_mapper.current_disp_mode
