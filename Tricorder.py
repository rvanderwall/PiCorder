from time import sleep
import os
import sys
import pygame

from Assets import Assets
from Display import Display, TFT_ALLOWED
from Logger import Logger
from ModeTransitions import ModeMapper, Commands, config_menu
from ModeTransitions import TricorderMode, OperationMode
from Output import LEDS
from Records import Records
from SensorBanks import SensorBanks, power_down_sensors


def build_tricorder(hw_mode):
    logger = Logger("Tricorder")
    assets = Assets()
    mode_mapper = ModeMapper(logger)
    mode = Tricorder.get_mode(hw_mode, TFT_ALLOWED)
    display = Display(logger, assets, tft_mode=mode.TFT)
    sensor_array = SensorBanks()
    tricorder = Tricorder(logger, display, sensor_array, mode_mapper, mode)
    tricorder._records = Records(assets)
    tricorder._leds = LEDS(logger)
    return tricorder, tricorder._leds


class Tricorder:
    def __init__(self, logger: Logger, display: Display, sensor_banks: SensorBanks,
                 mode_mapper: ModeMapper, mode: TricorderMode):
        self.logger = logger

        self._display = display
        self._sensor_banks = sensor_banks
        self._mode_mapper = mode_mapper

        self._outputs = None
        self._records = None
        self._leds = None

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
        # Update ALL sensors with history, not just the ones we are looking at
        for mode in [OperationMode.ENVIRONMENTAL, OperationMode.ENVIRONMENTAL2, self._operating_mode()]:
            sensor_array = self._sensor_banks.get_sensor_array(mode)
            for indicator in sensor_array.sensors:
                indicator.update_value()

    def update_display(self):
        disp_mode = self._display_mode()
        operating_mode = self._operating_mode()
        if operating_mode == OperationMode.RECORDS:
            current_record = self._records.get_current_record()
            self._display.update(disp_mode, current_record)
        elif operating_mode == OperationMode.INIT:
            self._display.update(disp_mode, [])
        elif operating_mode == OperationMode.CONFIGURE:
            self._display.update(disp_mode, config_menu)
        else:
            sensor_array = self._sensor_banks.get_sensor_array(operating_mode)
            self._display.update(disp_mode, sensor_array)

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
            pass    # Handled in outer event loop
        elif command == Commands.POWERDOWN:
            self.logger.info("POWERING DOWN NOW!!!!")
            self._leds.power_down()
            power_down_sensors()
            self._display.powerdown()
            os.system("sudo shutdown -h now")
            os.system("sudo poweroff")
            sys.exit(0)
        else:
            pass

    def _restart(self):
        self.update_display()
        pygame.event.get()      # Release control back to event loop to update display
        self._mode_mapper.enter_mode(OperationMode.ENVIRONMENTAL)
        self._init_sensors()

    def _init_sensors(self):
        # Just give time for them to warm up
        self._blink_red()

    def _operating_mode(self):
        return self._mode_mapper.get_op_mode()

    def _display_mode(self):
        return self._mode_mapper.get_disp_mode()

    def _blink_red(self):
        assert isinstance(self._leds, LEDS)
        self._leds.turn_on_blue_led()
        self._leds.turn_on_yellow_led()
        self._leds.turn_on_red_led()
        for i in range(4):
            sleep(0.2)
            self._leds.turn_off_red_led()
            sleep(0.2)
            self._leds.turn_on_red_led()

        self._leds.turn_off_blue_led()
        self._leds.turn_off_yellow_led()
