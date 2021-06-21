from time import sleep
import pygame

from Assets import Assets
from Display import Display, DISPLAY_MODE
from Inputs import Input
from Logger import Logger
from ModeTransitions import ModeMapper, Commands
from ModeTransitions import TricorderMode, OperationMode
from Records import Records
from SensorArray import SensorArray


def build_tricorder():
    logger = Logger("Tricorder")
    assets = Assets()
    display = Display(logger, assets)
    sensor_array = SensorArray()
    mode_mapper = ModeMapper(logger)
    tricorder = Tricorder(logger, display, sensor_array, mode_mapper)
    tricorder._inputs = Input(logger)
    tricorder._records = Records(assets)
    return tricorder


class Tricorder:
    def __init__(self, logger: Logger, display: Display, sensor_array: SensorArray, mode_mapper: ModeMapper):
        self.logger = logger
        self.mode = TricorderMode.LAPTOP

        self._display = display
        self._sensor_array = sensor_array
        self._mode_mapper = mode_mapper

        self._inputs = None
        self._outputs = None
        self._records = None
        self._restart()
        self._set_mode()

    def _set_mode(self):
        if DISPLAY_MODE == "TFT":
            self.mode = TricorderMode.RASP_PI_SENSORS

    def update_sensors(self):
        sensor_bank = self._sensor_array.get_sensor_bank(self._mode_mapper.current_op_mode)
        for sensor_type in sensor_bank:
            sensor = sensor_bank[sensor_type]
            sensor.update_value()

    def update_display(self):
        disp_mode = self._mode_mapper.current_disp_mode
        sensor_mode = self._mode_mapper.current_op_mode
        if sensor_mode == OperationMode.RECORDS:
            current_record = self._records.get_current_record()
            self._display.update(disp_mode, current_record)
        elif sensor_mode == OperationMode.INIT:
            self._display.update(disp_mode, [])
        else:
            sensor_bank = self._sensor_array.get_sensor_bank(self._mode_mapper.current_op_mode)
            self._display.update(disp_mode, sensor_bank)

    def process_inputs(self, event):
        if self._inputs is not None:
            key = self._inputs.get_inputs(event)
            self._switch_display_modes(key)

    def refresh(self):
        self._display.tick_display()
        if self._mode_mapper.current_op_mode == OperationMode.INIT:
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
        for i in range(2):
            sleep(1)
