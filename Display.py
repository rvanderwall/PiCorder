import pygame

from Assets import Assets
from ModeTransitions import DisplayMode
from Indicator import Indicator, Indicator3D
from Logger import Logger
from Records import Record

try:
    import digitalio
    from Displays.TFTDisplay import TFT_Display, FPS, HEIGHT
    DISPLAY_MODE = "TFT"
    lg = Logger("Startup")
    lg.info("Entering TFT display mode")
except Exception as ex:
    from Displays.PyGameDisplay import PyGameDisplay, FPS, HEIGHT
    DISPLAY_MODE = "WINDOW"
    lg = Logger("Startup")
    lg.info("Entering WINDOW display mode")


class Display:
    def __init__(self, assets: Assets):
        if DISPLAY_MODE == "TFT":
            assets.set_tft_mode()
            self._display = TFT_Display(assets.font)
        else:
            self._display = PyGameDisplay(assets.font)

        self._frame_rate = pygame.time.Clock()

        # Load assets
        self._scales = assets.scales
        self._grid = assets.grid
        self._slider_img = assets.slider_img
        self._logo = assets.logo
        self._lbl_vertical = False    # If labels are horizontal or vertical

    def clear(self):
        self._display.clear()

    def tick_display(self):
        self._frame_rate.tick(FPS)

    def update(self, mode, data_src):
        self.clear()
        if mode == DisplayMode.SPLASH:
            self._show_splash()
        elif isinstance(data_src, Record):
            self._update_records_disp(mode, data_src)
        else:
            self._update_sensor_disp(mode, data_src)

        # pygame.display.update()

    def _update_records_disp(self, mode, data_src):
        if mode == DisplayMode.VIDEO:
            self._display.render_image(data_src.image, (0, 0))
        elif mode == DisplayMode.TEXT:
            self._update_record_text(data_src.text)
        else:
            self._update_to_unknown(mode)

    def _update_sensor_disp(self, mode, sensor_array):
        if mode == DisplayMode.SLIDER:
            self._update_sliders(sensor_array)
        elif mode == DisplayMode.GRAPH:
            self._update_graphs(sensor_array)
        elif mode == DisplayMode.TEXT:
            self._update_sensor_text(sensor_array)
        else:
            self._update_to_unknown(mode)

    def _update_sliders(self, sensor_array):
        self._display.render_image(self._scales, (0, 0))
        for sensor_type in sensor_array:
            indicator = sensor_array[sensor_type]
            assert isinstance(indicator, Indicator)
            self._display.render_image(self._slider_img, indicator.get_position())

    def _update_record_text(self, str_text):
        hdr = "Record Bank matches:"
        self._display.render_text(hdr, (20, 20))
        self._display.render_text(str_text, (20, 50))

    def _update_sensor_text(self, sensor_array):
        lbl_idx = 0
        hdr = f"Sensor Bank [{len(sensor_array)} sensors]"
        self._display.render_text(hdr, (20, 20))

        self._lbl_vertical = True
        for sensor_type in sensor_array:
            indicator = sensor_array[sensor_type]
            if isinstance(indicator, Indicator3D):
                v = indicator.cur_val
                val_txt = f"[{v[0]:.2f}, {v[1]:.2f}, {v[2]:.2f}]"
                lbl = f"{indicator.label}: {val_txt}"
            else:
                assert isinstance(indicator, Indicator)
                lbl = f"{indicator.label} {indicator.cur_val:.2f} | {indicator.info_txt}"

            x_lbl_pos, y_lbl_pos = self._label_pos(lbl_idx)
            self._display.render_text(lbl, (x_lbl_pos, y_lbl_pos))
            lbl_idx += 1

    def _update_graphs(self, sensor_array):
        self._display.render_image(self._grid, (0, 0))
        lbl_idx = 0
        offset = 0
        self._lbl_vertical = False
        for sensor_type in sensor_array:
            indicator = sensor_array[sensor_type]
            assert isinstance(indicator, Indicator)
            self._display.render_lines(indicator.color, indicator.get_history())

            lbl = f"{indicator.label} {indicator.cur_val:.2f}"
            x_lbl_pos, y_lbl_pos = self._label_pos(lbl_idx, offset)
            self._display.render_text(lbl, (x_lbl_pos, y_lbl_pos))
            lbl_idx += 1
            offset += indicator.text_width

    def _label_pos(self, lbl_num, offset=None):
        if self._lbl_vertical:
            # Stack Vertically
            x_lbl_pos = 20
            y_lbl_pos = HEIGHT / 2
            y_lbl_pos += lbl_num * 20
        else:
            # Stack Horizontally
            if offset is None:
                x_lbl_pos = 20 + lbl_num * 65
            else:
                x_lbl_pos = 20 + offset
            y_lbl_pos = 206

        return x_lbl_pos, y_lbl_pos

    def _update_to_unknown(self, mode):
        self._display.render_text(f"Unknown mode: {mode}", (10, 180))

    def _show_splash(self):
        self.clear()
        logo_position = (90, 0)  #PyGame
        logo_position = (96, 50) #TFT
        self._display.render_image(self._logo, logo_position)
        txt_position = (10, 180)
        txt_position = (0, 0)
        self._display.render_text("StarFleet Tricorder TR-109", txt_position, size=33)

