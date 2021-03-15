#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: N200 TPR V2
# Author: Matthew Nelson
# Copyright: 2016-2021
# Description: Implementation of a Software Defined Radiometer
# GNU Radio version: 3.8.2.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from PyQt5 import Qt
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import eng_notation
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from TPR import TPR  # grc-generated hier_block
from datetime import datetime
from gnuradio import analog
from gnuradio import blocks
from gnuradio import gr
from gnuradio.fft import window
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio.fft import logpwrfft
from gnuradio.qtgui import Range, RangeWidget

from gnuradio import qtgui

class N200_TPR_2(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "N200 TPR V2")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("N200 TPR V2")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "N200_TPR_2")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 1e6
        self.prefix = prefix = "tpr_"
        self.fftsize = fftsize = 8192
        self.GUI_samp_rate = GUI_samp_rate = int(5e6)
        self.text_samp_rate = text_samp_rate = 0
        self.text_deviceID = text_deviceID = 0
        self.text_USRP_Clock = text_USRP_Clock = 100e6
        self.text_Device_addr = text_Device_addr = 0
        self.subdev = subdev = "A:0"
        self.spec_data_fifo = spec_data_fifo = "spectrum_" + datetime.now().strftime("%Y.%m.%d.%H.%M.%S") + ".dat"
        self.spavg = spavg = 5
        self.scope_rate = scope_rate = 2
        self.samp_rate_0 = samp_rate_0 = int(GUI_samp_rate)
        self.recfile_tpr = recfile_tpr = prefix + datetime.now().strftime("%Y.%m.%d.%H.%M.%S") + ".dat"
        self.recfile_kelvin = recfile_kelvin = prefix+"kelvin" + datetime.now().strftime("%Y.%m.%d.%H.%M.%S") + ".dat"
        self.noise_amplitude = noise_amplitude = 1
        self.integ = integ = 2
        self.gain = gain = 15
        self.frequency = frequency = 1.4125e9
        self.freq = freq = 1.415e9
        self.file_rate = file_rate = 2.0
        self.fftrate = fftrate = int(samp_rate/fftsize)
        self.devid = devid = "addr=192.168.10.2"
        self.det_rate = det_rate = int(20.0)
        self.dc_gain = dc_gain = 1
        self.clock = clock = 100e6
        self.calib_2 = calib_2 = -342.774
        self.calib_1 = calib_1 = 4.0755e3

        ##################################################
        # Blocks
        ##################################################
        self._spavg_range = Range(1, 20, 1, 5, 200)
        self._spavg_win = RangeWidget(self._spavg_range, self.set_spavg, "Spectral Averaging", 'dial', float)
        self.top_grid_layout.addWidget(self._spavg_win)
        self._noise_amplitude_range = Range(0.01, 2, .01, 1, 200)
        self._noise_amplitude_win = RangeWidget(self._noise_amplitude_range, self.set_noise_amplitude, 'Noise Amplitutde', 'counter_slider', float)
        self.top_grid_layout.addWidget(self._noise_amplitude_win)
        # Create the options list
        self._dc_gain_options = (1, 10, 100, 1000, 10000, )
        # Create the labels list
        self._dc_gain_labels = ('1', '10', '100', '1000', '10000', )
        # Create the combo box
        # Create the radio buttons
        self._dc_gain_group_box = Qt.QGroupBox('DC Gain' + ": ")
        self._dc_gain_box = Qt.QHBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._dc_gain_button_group = variable_chooser_button_group()
        self._dc_gain_group_box.setLayout(self._dc_gain_box)
        for i, _label in enumerate(self._dc_gain_labels):
            radio_button = Qt.QRadioButton(_label)
            self._dc_gain_box.addWidget(radio_button)
            self._dc_gain_button_group.addButton(radio_button, i)
        self._dc_gain_callback = lambda i: Qt.QMetaObject.invokeMethod(self._dc_gain_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._dc_gain_options.index(i)))
        self._dc_gain_callback(self.dc_gain)
        self._dc_gain_button_group.buttonClicked[int].connect(
            lambda i: self.set_dc_gain(self._dc_gain_options[i]))
        self.top_grid_layout.addWidget(self._dc_gain_group_box)
        self._calib_2_tool_bar = Qt.QToolBar(self)
        self._calib_2_tool_bar.addWidget(Qt.QLabel('Calibration Point 2' + ": "))
        self._calib_2_line_edit = Qt.QLineEdit(str(self.calib_2))
        self._calib_2_tool_bar.addWidget(self._calib_2_line_edit)
        self._calib_2_line_edit.returnPressed.connect(
            lambda: self.set_calib_2(eng_notation.str_to_num(str(self._calib_2_line_edit.text()))))
        self.top_grid_layout.addWidget(self._calib_2_tool_bar)
        self._calib_1_tool_bar = Qt.QToolBar(self)
        self._calib_1_tool_bar.addWidget(Qt.QLabel('Calibration Point 1' + ": "))
        self._calib_1_line_edit = Qt.QLineEdit(str(self.calib_1))
        self._calib_1_tool_bar.addWidget(self._calib_1_line_edit)
        self._calib_1_line_edit.returnPressed.connect(
            lambda: self.set_calib_1(eng_notation.str_to_num(str(self._calib_1_line_edit.text()))))
        self.top_grid_layout.addWidget(self._calib_1_tool_bar)
        self._text_samp_rate_tool_bar = Qt.QToolBar(self)

        if None:
            self._text_samp_rate_formatter = None
        else:
            self._text_samp_rate_formatter = lambda x: str(x)

        self._text_samp_rate_tool_bar.addWidget(Qt.QLabel('Device Sample Rate' + ": "))
        self._text_samp_rate_label = Qt.QLabel(str(self._text_samp_rate_formatter(self.text_samp_rate)))
        self._text_samp_rate_tool_bar.addWidget(self._text_samp_rate_label)
        self.top_grid_layout.addWidget(self._text_samp_rate_tool_bar)
        self._text_deviceID_tool_bar = Qt.QToolBar(self)

        if None:
            self._text_deviceID_formatter = None
        else:
            self._text_deviceID_formatter = lambda x: str(x)

        self._text_deviceID_tool_bar.addWidget(Qt.QLabel('Device ID' + ": "))
        self._text_deviceID_label = Qt.QLabel(str(self._text_deviceID_formatter(self.text_deviceID)))
        self._text_deviceID_tool_bar.addWidget(self._text_deviceID_label)
        self.top_grid_layout.addWidget(self._text_deviceID_tool_bar)
        self._text_USRP_Clock_tool_bar = Qt.QToolBar(self)

        if None:
            self._text_USRP_Clock_formatter = None
        else:
            self._text_USRP_Clock_formatter = lambda x: eng_notation.num_to_str(x)

        self._text_USRP_Clock_tool_bar.addWidget(Qt.QLabel('USRP Clock' + ": "))
        self._text_USRP_Clock_label = Qt.QLabel(str(self._text_USRP_Clock_formatter(self.text_USRP_Clock)))
        self._text_USRP_Clock_tool_bar.addWidget(self._text_USRP_Clock_label)
        self.top_grid_layout.addWidget(self._text_USRP_Clock_tool_bar)
        self._text_Device_addr_tool_bar = Qt.QToolBar(self)

        if None:
            self._text_Device_addr_formatter = None
        else:
            self._text_Device_addr_formatter = lambda x: str(x)

        self._text_Device_addr_tool_bar.addWidget(Qt.QLabel('Device IP' + ": "))
        self._text_Device_addr_label = Qt.QLabel(str(self._text_Device_addr_formatter(self.text_Device_addr)))
        self._text_Device_addr_tool_bar.addWidget(self._text_Device_addr_label)
        self.top_grid_layout.addWidget(self._text_Device_addr_tool_bar)
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_waterfall_sink_x_0_win)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            1024, #size
            100000, #samp_rate
            'TPR Ticker Tape', #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.01)
        self.qtgui_time_sink_x_0.set_y_axis(0, 5)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(True)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(True)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Radiometer', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.qtgui_tab_widget_0 = Qt.QTabWidget()
        self.qtgui_tab_widget_0_widget_0 = Qt.QWidget()
        self.qtgui_tab_widget_0_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.qtgui_tab_widget_0_widget_0)
        self.qtgui_tab_widget_0_grid_layout_0 = Qt.QGridLayout()
        self.qtgui_tab_widget_0_layout_0.addLayout(self.qtgui_tab_widget_0_grid_layout_0)
        self.qtgui_tab_widget_0.addTab(self.qtgui_tab_widget_0_widget_0, 'All')
        self.qtgui_tab_widget_0_widget_1 = Qt.QWidget()
        self.qtgui_tab_widget_0_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.qtgui_tab_widget_0_widget_1)
        self.qtgui_tab_widget_0_grid_layout_1 = Qt.QGridLayout()
        self.qtgui_tab_widget_0_layout_1.addLayout(self.qtgui_tab_widget_0_grid_layout_1)
        self.qtgui_tab_widget_0.addTab(self.qtgui_tab_widget_0_widget_1, 'Radio Control')
        self.qtgui_tab_widget_0_widget_2 = Qt.QWidget()
        self.qtgui_tab_widget_0_layout_2 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.qtgui_tab_widget_0_widget_2)
        self.qtgui_tab_widget_0_grid_layout_2 = Qt.QGridLayout()
        self.qtgui_tab_widget_0_layout_2.addLayout(self.qtgui_tab_widget_0_grid_layout_2)
        self.qtgui_tab_widget_0.addTab(self.qtgui_tab_widget_0_widget_2, 'Radiometer')
        self.top_grid_layout.addWidget(self.qtgui_tab_widget_0)
        self.qtgui_number_sink_2 = qtgui.number_sink(
            gr.sizeof_float,
            .5,
            qtgui.NUM_GRAPH_HORIZ,
            1,
            None # parent
        )
        self.qtgui_number_sink_2.set_update_time(0.10)
        self.qtgui_number_sink_2.set_title('Calibrated Noise Temperature')

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['K', '', '', '', '',
            '', '', '', '', '']
        colors = [("blue", "red"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.qtgui_number_sink_2.set_min(i, 0)
            self.qtgui_number_sink_2.set_max(i, 300)
            self.qtgui_number_sink_2.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_2.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_2.set_label(i, labels[i])
            self.qtgui_number_sink_2.set_unit(i, units[i])
            self.qtgui_number_sink_2.set_factor(i, factor[i])

        self.qtgui_number_sink_2.enable_autoscale(False)
        self._qtgui_number_sink_2_win = sip.wrapinstance(self.qtgui_number_sink_2.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_number_sink_2_win)
        self.qtgui_number_sink_1 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1,
            None # parent
        )
        self.qtgui_number_sink_1.set_update_time(0.10)
        self.qtgui_number_sink_1.set_title("")

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.qtgui_number_sink_1.set_min(i, -1)
            self.qtgui_number_sink_1.set_max(i, 1)
            self.qtgui_number_sink_1.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_1.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_1.set_label(i, labels[i])
            self.qtgui_number_sink_1.set_unit(i, units[i])
            self.qtgui_number_sink_1.set_factor(i, factor[i])

        self.qtgui_number_sink_1.enable_autoscale(False)
        self._qtgui_number_sink_1_win = sip.wrapinstance(self.qtgui_number_sink_1.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_number_sink_1_win)
        self.qtgui_number_sink_0 = qtgui.number_sink(
            gr.sizeof_float,
            .5,
            qtgui.NUM_GRAPH_HORIZ,
            2,
            None # parent
        )
        self.qtgui_number_sink_0.set_update_time(0.10)
        self.qtgui_number_sink_0.set_title('TPR Value')

        labels = ['Raw', 'Calibrated', 'Peak detected', '', '',
            '', '', '', '', '']
        units = ['', 'K', '', '', '',
            '', '', '', '', '']
        colors = [("blue", "red"), ("blue", "red"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(2):
            self.qtgui_number_sink_0.set_min(i, -5)
            self.qtgui_number_sink_0.set_max(i, 10)
            self.qtgui_number_sink_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0.set_label(i, labels[i])
            self.qtgui_number_sink_0.set_unit(i, units[i])
            self.qtgui_number_sink_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0.enable_autoscale(False)
        self._qtgui_number_sink_0_win = sip.wrapinstance(self.qtgui_number_sink_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_number_sink_0_win)
        self.logpwrfft_x_0 = logpwrfft.logpwrfft_c(
            sample_rate=samp_rate,
            fft_size=fftsize,
            ref_scale=2,
            frame_rate=fftrate,
            avg_alpha=1.0/float(spavg*fftrate),
            average=True)
        self._gain_range = Range(0, 50, 1, 15, 200)
        self._gain_win = RangeWidget(self._gain_range, self.set_gain, 'RF Gain (dB)', 'counter_slider', float)
        self.top_grid_layout.addWidget(self._gain_win)
        self._freq_tool_bar = Qt.QToolBar(self)
        self._freq_tool_bar.addWidget(Qt.QLabel('Center Frequency' + ": "))
        self._freq_line_edit = Qt.QLineEdit(str(self.freq))
        self._freq_tool_bar.addWidget(self._freq_line_edit)
        self._freq_line_edit.returnPressed.connect(
            lambda: self.set_freq(eng_notation.str_to_num(str(self._freq_line_edit.text()))))
        self.top_grid_layout.addWidget(self._freq_tool_bar)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_peak_detector_xb_0 = blocks.peak_detector_fb(0.25, 0.40, 10, 0.001)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_ff(calib_1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(dc_gain)
        self.blocks_keep_one_in_n_3 = blocks.keep_one_in_n(gr.sizeof_float*fftsize, fftrate)
        self.blocks_keep_one_in_n_1 = blocks.keep_one_in_n(gr.sizeof_float*1, int(det_rate/file_rate))
        self.blocks_file_sink_5 = blocks.file_sink(gr.sizeof_float*fftsize, spec_data_fifo, False)
        self.blocks_file_sink_5.set_unbuffered(True)
        self.blocks_file_sink_4 = blocks.file_sink(gr.sizeof_float*1, recfile_tpr, False)
        self.blocks_file_sink_4.set_unbuffered(True)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_float*1, 'test.dat', False)
        self.blocks_file_sink_0.set_unbuffered(True)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.blocks_char_to_float_0 = blocks.char_to_float(1, 1)
        self.blocks_add_const_vxx_1 = blocks.add_const_ff(calib_2)
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, noise_amplitude, 0)
        self.TPR_0 = TPR(
            det_rate=det_rate,
            integ=integ,
            samp_rate=samp_rate,
        )
        # Create the options list
        self._GUI_samp_rate_options = (int(1e6), int(2e6), int(5e6), int(10e6), int(15e6), )
        # Create the labels list
        self._GUI_samp_rate_labels = ('1 MHz', '2 MHz', '5 MHz', '10 MHz', '15 MHz', )
        # Create the combo box
        # Create the radio buttons
        self._GUI_samp_rate_group_box = Qt.QGroupBox('GUI Sample Rate (BW)' + ": ")
        self._GUI_samp_rate_box = Qt.QHBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._GUI_samp_rate_button_group = variable_chooser_button_group()
        self._GUI_samp_rate_group_box.setLayout(self._GUI_samp_rate_box)
        for i, _label in enumerate(self._GUI_samp_rate_labels):
            radio_button = Qt.QRadioButton(_label)
            self._GUI_samp_rate_box.addWidget(radio_button)
            self._GUI_samp_rate_button_group.addButton(radio_button, i)
        self._GUI_samp_rate_callback = lambda i: Qt.QMetaObject.invokeMethod(self._GUI_samp_rate_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._GUI_samp_rate_options.index(i)))
        self._GUI_samp_rate_callback(self.GUI_samp_rate)
        self._GUI_samp_rate_button_group.buttonClicked[int].connect(
            lambda i: self.set_GUI_samp_rate(self._GUI_samp_rate_options[i]))
        self.top_grid_layout.addWidget(self._GUI_samp_rate_group_box)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.TPR_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_add_const_vxx_1, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_add_const_vxx_1, 0), (self.qtgui_number_sink_2, 0))
        self.connect((self.blocks_char_to_float_0, 0), (self.qtgui_number_sink_1, 0))
        self.connect((self.blocks_complex_to_real_0, 0), (self.blocks_peak_detector_xb_0, 0))
        self.connect((self.blocks_keep_one_in_n_1, 0), (self.blocks_file_sink_4, 0))
        self.connect((self.blocks_keep_one_in_n_1, 0), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.blocks_keep_one_in_n_1, 0), (self.qtgui_number_sink_0, 1))
        self.connect((self.blocks_keep_one_in_n_1, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_keep_one_in_n_3, 0), (self.blocks_file_sink_5, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_keep_one_in_n_1, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.qtgui_number_sink_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.blocks_add_const_vxx_1, 0))
        self.connect((self.blocks_peak_detector_xb_0, 0), (self.blocks_char_to_float_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.TPR_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.logpwrfft_x_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.qtgui_waterfall_sink_x_0, 0))
        self.connect((self.logpwrfft_x_0, 0), (self.blocks_keep_one_in_n_3, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "N200_TPR_2")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_fftrate(int(self.samp_rate/self.fftsize))
        self.TPR_0.set_samp_rate(self.samp_rate)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.logpwrfft_x_0.set_sample_rate(self.samp_rate)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(0, self.samp_rate)

    def get_prefix(self):
        return self.prefix

    def set_prefix(self, prefix):
        self.prefix = prefix
        self.set_recfile_kelvin(self.prefix+"kelvin" + datetime.now().strftime("%Y.%m.%d.%H.%M.%S") + ".dat")
        self.set_recfile_tpr(self.prefix + datetime.now().strftime("%Y.%m.%d.%H.%M.%S") + ".dat")

    def get_fftsize(self):
        return self.fftsize

    def set_fftsize(self, fftsize):
        self.fftsize = fftsize
        self.set_fftrate(int(self.samp_rate/self.fftsize))

    def get_GUI_samp_rate(self):
        return self.GUI_samp_rate

    def set_GUI_samp_rate(self, GUI_samp_rate):
        self.GUI_samp_rate = GUI_samp_rate
        self._GUI_samp_rate_callback(self.GUI_samp_rate)
        self.set_samp_rate_0(int(self.GUI_samp_rate))

    def get_text_samp_rate(self):
        return self.text_samp_rate

    def set_text_samp_rate(self, text_samp_rate):
        self.text_samp_rate = text_samp_rate
        Qt.QMetaObject.invokeMethod(self._text_samp_rate_label, "setText", Qt.Q_ARG("QString", self.text_samp_rate))

    def get_text_deviceID(self):
        return self.text_deviceID

    def set_text_deviceID(self, text_deviceID):
        self.text_deviceID = text_deviceID
        Qt.QMetaObject.invokeMethod(self._text_deviceID_label, "setText", Qt.Q_ARG("QString", self.text_deviceID))

    def get_text_USRP_Clock(self):
        return self.text_USRP_Clock

    def set_text_USRP_Clock(self, text_USRP_Clock):
        self.text_USRP_Clock = text_USRP_Clock
        Qt.QMetaObject.invokeMethod(self._text_USRP_Clock_label, "setText", Qt.Q_ARG("QString", self.text_USRP_Clock))

    def get_text_Device_addr(self):
        return self.text_Device_addr

    def set_text_Device_addr(self, text_Device_addr):
        self.text_Device_addr = text_Device_addr
        Qt.QMetaObject.invokeMethod(self._text_Device_addr_label, "setText", Qt.Q_ARG("QString", self.text_Device_addr))

    def get_subdev(self):
        return self.subdev

    def set_subdev(self, subdev):
        self.subdev = subdev

    def get_spec_data_fifo(self):
        return self.spec_data_fifo

    def set_spec_data_fifo(self, spec_data_fifo):
        self.spec_data_fifo = spec_data_fifo
        self.blocks_file_sink_5.open(self.spec_data_fifo)

    def get_spavg(self):
        return self.spavg

    def set_spavg(self, spavg):
        self.spavg = spavg
        self.logpwrfft_x_0.set_avg_alpha(1.0/float(self.spavg*self.fftrate))

    def get_scope_rate(self):
        return self.scope_rate

    def set_scope_rate(self, scope_rate):
        self.scope_rate = scope_rate

    def get_samp_rate_0(self):
        return self.samp_rate_0

    def set_samp_rate_0(self, samp_rate_0):
        self.samp_rate_0 = samp_rate_0

    def get_recfile_tpr(self):
        return self.recfile_tpr

    def set_recfile_tpr(self, recfile_tpr):
        self.recfile_tpr = recfile_tpr
        self.blocks_file_sink_4.open(self.recfile_tpr)

    def get_recfile_kelvin(self):
        return self.recfile_kelvin

    def set_recfile_kelvin(self, recfile_kelvin):
        self.recfile_kelvin = recfile_kelvin

    def get_noise_amplitude(self):
        return self.noise_amplitude

    def set_noise_amplitude(self, noise_amplitude):
        self.noise_amplitude = noise_amplitude
        self.analog_noise_source_x_0.set_amplitude(self.noise_amplitude)

    def get_integ(self):
        return self.integ

    def set_integ(self, integ):
        self.integ = integ
        self.TPR_0.set_integ(self.integ)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain

    def get_frequency(self):
        return self.frequency

    def set_frequency(self, frequency):
        self.frequency = frequency

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        Qt.QMetaObject.invokeMethod(self._freq_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.freq)))

    def get_file_rate(self):
        return self.file_rate

    def set_file_rate(self, file_rate):
        self.file_rate = file_rate
        self.blocks_keep_one_in_n_1.set_n(int(self.det_rate/self.file_rate))

    def get_fftrate(self):
        return self.fftrate

    def set_fftrate(self, fftrate):
        self.fftrate = fftrate
        self.blocks_keep_one_in_n_3.set_n(self.fftrate)
        self.logpwrfft_x_0.set_avg_alpha(1.0/float(self.spavg*self.fftrate))

    def get_devid(self):
        return self.devid

    def set_devid(self, devid):
        self.devid = devid

    def get_det_rate(self):
        return self.det_rate

    def set_det_rate(self, det_rate):
        self.det_rate = det_rate
        self.TPR_0.set_det_rate(self.det_rate)
        self.blocks_keep_one_in_n_1.set_n(int(self.det_rate/self.file_rate))

    def get_dc_gain(self):
        return self.dc_gain

    def set_dc_gain(self, dc_gain):
        self.dc_gain = dc_gain
        self._dc_gain_callback(self.dc_gain)
        self.blocks_multiply_const_vxx_0.set_k(self.dc_gain)

    def get_clock(self):
        return self.clock

    def set_clock(self, clock):
        self.clock = clock

    def get_calib_2(self):
        return self.calib_2

    def set_calib_2(self, calib_2):
        self.calib_2 = calib_2
        Qt.QMetaObject.invokeMethod(self._calib_2_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.calib_2)))
        self.blocks_add_const_vxx_1.set_k(self.calib_2)

    def get_calib_1(self):
        return self.calib_1

    def set_calib_1(self, calib_1):
        self.calib_1 = calib_1
        Qt.QMetaObject.invokeMethod(self._calib_1_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.calib_1)))
        self.blocks_multiply_const_vxx_1.set_k(self.calib_1)





def main(top_block_cls=N200_TPR_2, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()

    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()

if __name__ == '__main__':
    main()
