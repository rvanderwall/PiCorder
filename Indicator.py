from Sensor import Sensor


class Indicator:
    def __init__(self, name: str, sensor: Sensor):
        self.label = name
        self.min = sensor.min
        self.max = sensor.max
        self.reader = sensor.get_sensor_value

        # Rendering attributes for text
        self.text_width = 65
        self.info_txt = sensor.info

        # Rendering attributes to determine Y position
        # The Y position will be the same for slider and graph
        self.cur_val = 0        # Actual reading
        self.cur_scaled = 0     # Scaled and translated for display

        self.graph_offset = 15
        self.graph_top = 3
        self.graph_bottom = 200
        delta = self.max - self.min
        self.scale = (self.graph_bottom - self.graph_top) / delta

        # Attributes for slider rendering
        self.x_position = 0

        # Attributes for graph rendering
        self.color = None
        self.num_points = 290

        self.history = []
        self._init_history(delta)

    def _init_history(self, delta):
        mid = self._scale(delta / 2)
        for _ in range(self.num_points):
            self.history.append(mid)    # Fill history with mid-point data

    # Sets the slider X position
    def set_x_pos(self, pos):
        self.x_position = pos
        return self

    # Sets the slider X position
    def set_text_width(self, width):
        self.text_width = width
        return self

    # Sets the color for the graph
    def set_color(self, color):
        self.color = color
        return self

    def update_value(self):
        val = self.reader()
        self.cur_val = val
        self.cur_scaled = self._scale(val)
        self.history.append(self.cur_scaled)
        self.history.pop(0)

    def get_position(self):
        return self.x_position, self.cur_scaled

    def get_history(self):
        data = []
        for x in range(len(self.history)):
            data.append((x+self.graph_offset, self.history[x]))
        return data

    def _scale(self, val):
        t = self.graph_bottom - self.scale * (val - self.min)
        return int(t)


class Indicator3D(Indicator):
    def __init__(self, name: str, sensor: Sensor):
        super().__init__(name, sensor)

    def _init_history(self, delta):
        mid_val = (delta / 2, delta / 2, delta / 2)
        mid = self._scale(mid_val)
        for _ in range(self.num_points):
            self.history.append(mid)    # Fill history with mid-point data

    def _scale(self, val):
        x, y, z = val
        t_x = self.graph_bottom - self.scale * (x - self.min)
        t_y = self.graph_bottom - self.scale * (y - self.min)
        t_z = self.graph_bottom - self.scale * (z - self.min)
        return t_x, t_y, t_z

    def get_position(self):
        pass
