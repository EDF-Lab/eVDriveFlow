"""
.. module:: custom_canvas
   :platform: Unix
   :synopsis: A module that allows plotting in an animation.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.animation import TimedAnimation
import numpy as np


class CustomCanvas(FigureCanvas, TimedAnimation):
    """This is the class that will plot the data and display it properly in 15118 DC use case.

    """
    def __init__(self, power_data, energy_data, limits, battery=None):
        """Basic constructor.

        :param power_data: The array-like containing power data.
        :param energy_data: The array-like containing energy data.
        :param limits: The couple containing the limits for the EV/EVSE.
        :param battery: The battery value. If not specified, it means the limits are for the EVSE. Else the limits are
        for the EV.
        """
        self.power_data = power_data
        self.energy_data = energy_data
        self.figure = plt.figure()
        self.nb_points = 500
        # Power ax settings
        self.power_ax = self.figure.add_subplot(211)
        self.power_ax.grid()
        # Energy ax settings
        self.energy_ax = self.figure.add_subplot(212)
        self.energy_ax.grid()

        limit_percentage = int(limits[0]*0.1)
        self.set_subplot(self.power_ax, "Power (W)", (limits[1] - limit_percentage, limits[0] + limit_percentage))
        self.set_subplot(self.energy_ax, "Energy (Wh)", (0, 100000))

        self.power_values, self.power_line = self.get_plot_data(self.power_ax)

        if battery is None:
            self.evmaximum_charge_power, self.evmaximum_charge_power_line = self.get_plot_data(
                self.power_ax, color="g", linestyle="dashed", label="EV maximum charge power")
            self.evmaximum_discharge_power, self.evmaximum_discharge_power_line = self.get_plot_data(
                self.power_ax, color="r", linestyle="dashed", label="EV maximum discharge power")
            self.evsemaximum_charge_power, self.evsemaximum_charge_power_line = self.get_plot_data(
                self.power_ax, value=limits[0], color="g", linestyle="dotted", label="EVSE maximum charge power")
            self.evsemaximum_discharge_power, self.evsemaximum_discharge_power_line = self.get_plot_data(
                self.power_ax, value=limits[1], color="r", linestyle="dotted", label="EVSE maximum discharge power")
            self.maximum_battery_capacity, self.maximum_battery_capacity_line = self.get_plot_data(
                self.energy_ax, color="black", label="Maximum battery capacity")
        else:
            self.evmaximum_charge_power, self.evmaximum_charge_power_line = self.get_plot_data(
                self.power_ax, value=limits[0], color="g", linestyle="dashed", label="EV maximum charge power")
            self.evmaximum_discharge_power, self.evmaximum_discharge_power_line = self.get_plot_data(
                self.power_ax, value=limits[1], color="r", linestyle="dashed", label="EV maximum discharge power")
            self.evsemaximum_charge_power, self.evsemaximum_charge_power_line = self.get_plot_data(
                self.power_ax, color="g", linestyle="dotted", label="EVSE maximum charge power")
            self.evsemaximum_discharge_power, self.evsemaximum_discharge_power_line = self.get_plot_data(
                self.power_ax, color="r", linestyle="dotted", label="EVSE maximum discharge power")
            self.maximum_battery_capacity, self.maximum_battery_capacity_line = self.get_plot_data(
                self.energy_ax, value=battery, color="black", label="Maximum battery capacity")
        self.power_ax.legend()

        self.energy_values, self.energy_line = self.get_plot_data(self.energy_ax)

        self.energy_ax.legend()
        FigureCanvas.__init__(self, self.figure)
        TimedAnimation.__init__(self, self.figure, interval=20, blit=True)

    def new_frame_seq(self):
        return iter(range(self.nb_points))

    def _init_draw(self):
        self._drawn_artists = [self.power_line, self.energy_line, self.evmaximum_charge_power_line,
                               self.evmaximum_discharge_power_line, self.evsemaximum_charge_power_line,
                               self.evsemaximum_discharge_power_line, self.maximum_battery_capacity_line]
        for line in self._drawn_artists:
            line.set_ydata([np.nan])

    def _draw_frame(self, framedata):
        self.shift_left(self.power_values, self.power_data, self.power_line)
        self.shift_left(self.energy_values, self.energy_data, self.energy_line)
        self.shift_left(self.evmaximum_charge_power, self.evmaximum_charge_power,
                        self.evmaximum_charge_power_line)
        self.shift_left(self.evmaximum_discharge_power, self.evmaximum_discharge_power,
                        self.evmaximum_discharge_power_line)
        self.shift_left(self.evsemaximum_charge_power, self.evsemaximum_charge_power,
                        self.evsemaximum_charge_power_line)
        self.shift_left(self.evsemaximum_discharge_power, self.evsemaximum_discharge_power,
                        self.evsemaximum_discharge_power_line)
        self.shift_left(self.maximum_battery_capacity, self.maximum_battery_capacity,
                        self.maximum_battery_capacity_line)
        for line in self._drawn_artists:
            line.set_animated(True)

    def set_subplot(self, ax, plot_name, limits):
        ax.set_ylabel(plot_name)
        ax.set_xlim(0, self.nb_points)
        ax.set_ylim(limits)
        ax.get_xaxis().set_visible(False)

    def get_plot_data(self, ax, value=np.nan, color="b", linestyle="-", label="Present value"):
        """Creates empty arrays needed for an initial drawing. We can customize it.

        :param ax: The ax to be used.
        :param value: The value used to fill the array.
        :param color: The line's color.
        :param linestyle: The line's style.
        :param label: The line's label.
        :return: np.array, Line2D -- the resulting array and its line.
        """
        values = np.full(shape=(self.nb_points,), fill_value=value)
        plot, = ax.plot(values, color=color, linestyle=linestyle, label=label)
        return values, plot

    def shift_left(self, plot_values, data, line) -> None:
        """Shifts array data to the left creating a moving window.

        :param plot_values: The array-like to be shifted.
        :param data: The data the array-like will get.
        :param line: The line that should be updated.
        :return:
        """
        plot_values[:-1] = plot_values[1:]  # shift values one place to the left
        plot_values[-1] = data[-1]
        line.set_ydata(plot_values)
