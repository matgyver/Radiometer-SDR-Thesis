#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Total Power Radiometer - N200
# Author: Matthew E Nelson
# Description: Total power radiometer connecting to a N200 SDR
# Generated: Tue Feb 24 17:35:30 2015
##################################################

# Call XInitThreads as the _very_ first thing.
# After some Qt import, it's too late
import ctypes
import sys
if sys.platform.startswith('linux'):
    try:
        x11 = ctypes.cdll.LoadLibrary('libX11.so')
        x11.XInitThreads()
    except:
        print "Warning: failed to XInitThreads()"

from datetime import datetime
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import uhd
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import logpwrfft
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from gnuradio.wxgui import numbersink2
from gnuradio.wxgui import scopesink2
from grc_gnuradio import blks2 as grc_blks2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import time
import wx

class N200_TPR(grc_wxgui.top_block_gui):

    def __init__(self, subdev="A:0", devid="addr=192.168.10.2", frequency=1.4125e9, fftsize=8192):
        grc_wxgui.top_block_gui.__init__(self, title="Total Power Radiometer - N200")

        ##################################################
        # Parameters
        ##################################################
        self.subdev = subdev
        self.devid = devid
        self.frequency = frequency
        self.fftsize = fftsize

        ##################################################
        # Variables
        ##################################################
        self.GUI_samp_rate = GUI_samp_rate = 10e6
        self.samp_rate = samp_rate = int(GUI_samp_rate)
        self.prefix = prefix = "tpr_"
        self.text_samp_rate = text_samp_rate = GUI_samp_rate
        self.text_deviceID = text_deviceID = subdev
        self.text_Device_addr = text_Device_addr = devid
        self.spec_data_fifo = spec_data_fifo = "spectrum_" + datetime.now().strftime("%Y.%m.%d.%H.%M.%S") + ".dat"
        self.spavg = spavg = 1
        self.scope_rate = scope_rate = 2
        self.recfile_tpr = recfile_tpr = prefix + datetime.now().strftime("%Y.%m.%d.%H.%M.%S") + ".dat"
        self.recfile_kelvin = recfile_kelvin = prefix+"kelvin" + datetime.now().strftime("%Y.%m.%d.%H.%M.%S") + ".dat"
        self.rec_button_tpr = rec_button_tpr = 1
        self.rec_button_iq = rec_button_iq = 1
        self.noise_amplitude = noise_amplitude = .5
        self.integ = integ = 2
        self.gain = gain = 26
        self.freq = freq = frequency
        self.file_rate = file_rate = 2.0
        self.fftrate = fftrate = int(samp_rate/fftsize)
        self.det_rate = det_rate = int(20.0)
        self.dc_gain = dc_gain = 1
        self.calib_2 = calib_2 = -342.774
        self.calib_1 = calib_1 = 4.0755e3
        self.add_noise = add_noise = 0

        ##################################################
        # Blocks
        ##################################################
        self.Main = self.Main = wx.Notebook(self.GetWin(), style=wx.NB_TOP)
        self.Main.AddPage(grc_wxgui.Panel(self.Main), "N200 Control Panel")
        self.Main.AddPage(grc_wxgui.Panel(self.Main), "TPR Measurements")
        self.Add(self.Main)
        _spavg_sizer = wx.BoxSizer(wx.VERTICAL)
        self._spavg_text_box = forms.text_box(
        	parent=self.Main.GetPage(0).GetWin(),
        	sizer=_spavg_sizer,
        	value=self.spavg,
        	callback=self.set_spavg,
        	label="Spectral Averaging (Seconds)",
        	converter=forms.int_converter(),
        	proportion=0,
        )
        self._spavg_slider = forms.slider(
        	parent=self.Main.GetPage(0).GetWin(),
        	sizer=_spavg_sizer,
        	value=self.spavg,
        	callback=self.set_spavg,
        	minimum=1,
        	maximum=20,
        	num_steps=20,
        	style=wx.SL_HORIZONTAL,
        	cast=int,
        	proportion=1,
        )
        self.Main.GetPage(0).GridAdd(_spavg_sizer, 1, 1, 1, 1)
        self._rec_button_tpr_chooser = forms.button(
        	parent=self.Main.GetPage(0).GetWin(),
        	value=self.rec_button_tpr,
        	callback=self.set_rec_button_tpr,
        	label="Record TPR Data",
        	choices=[0,1],
        	labels=['Stop','Start'],
        )
        self.Main.GetPage(0).GridAdd(self._rec_button_tpr_chooser, 4, 1, 1, 1)
        self._rec_button_iq_chooser = forms.button(
        	parent=self.Main.GetPage(0).GetWin(),
        	value=self.rec_button_iq,
        	callback=self.set_rec_button_iq,
        	label="Record I/Q Data",
        	choices=[0,1],
        	labels=['Stop','Start'],
        )
        self.Main.GetPage(0).GridAdd(self._rec_button_iq_chooser, 4, 0, 1, 1)
        _integ_sizer = wx.BoxSizer(wx.VERTICAL)
        self._integ_text_box = forms.text_box(
        	parent=self.Main.GetPage(0).GetWin(),
        	sizer=_integ_sizer,
        	value=self.integ,
        	callback=self.set_integ,
        	label="Integration Time (Seconds)",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._integ_slider = forms.slider(
        	parent=self.Main.GetPage(0).GetWin(),
        	sizer=_integ_sizer,
        	value=self.integ,
        	callback=self.set_integ,
        	minimum=1,
        	maximum=60,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Main.GetPage(0).GridAdd(_integ_sizer, 0, 2, 1, 1)
        _gain_sizer = wx.BoxSizer(wx.VERTICAL)
        self._gain_text_box = forms.text_box(
        	parent=self.Main.GetPage(0).GetWin(),
        	sizer=_gain_sizer,
        	value=self.gain,
        	callback=self.set_gain,
        	label="RF Gain (dB)",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._gain_slider = forms.slider(
        	parent=self.Main.GetPage(0).GetWin(),
        	sizer=_gain_sizer,
        	value=self.gain,
        	callback=self.set_gain,
        	minimum=0,
        	maximum=50,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Main.GetPage(0).GridAdd(_gain_sizer, 0, 1, 1, 1)
        self._freq_text_box = forms.text_box(
        	parent=self.Main.GetPage(0).GetWin(),
        	value=self.freq,
        	callback=self.set_freq,
        	label="Center Frequency (Hz)",
        	converter=forms.float_converter(),
        )
        self.Main.GetPage(0).GridAdd(self._freq_text_box, 0, 0, 1, 1)
        self._dc_gain_chooser = forms.radio_buttons(
        	parent=self.Main.GetPage(0).GetWin(),
        	value=self.dc_gain,
        	callback=self.set_dc_gain,
        	label="DC Gain",
        	choices=[1, 10, 100, 1000, 10000],
        	labels=[],
        	style=wx.RA_HORIZONTAL,
        )
        self.Main.GetPage(0).GridAdd(self._dc_gain_chooser, 1, 0, 1, 1)
        self._calib_2_text_box = forms.text_box(
        	parent=self.Main.GetPage(0).GetWin(),
        	value=self.calib_2,
        	callback=self.set_calib_2,
        	label="Calibration value 2",
        	converter=forms.float_converter(),
        )
        self.Main.GetPage(0).GridAdd(self._calib_2_text_box, 3, 1, 1, 1)
        self._calib_1_text_box = forms.text_box(
        	parent=self.Main.GetPage(0).GetWin(),
        	value=self.calib_1,
        	callback=self.set_calib_1,
        	label="Calibration value 1",
        	converter=forms.float_converter(),
        )
        self.Main.GetPage(0).GridAdd(self._calib_1_text_box, 3, 0, 1, 1)
        self._GUI_samp_rate_chooser = forms.radio_buttons(
        	parent=self.Main.GetPage(0).GetWin(),
        	value=self.GUI_samp_rate,
        	callback=self.set_GUI_samp_rate,
        	label="Sample Rate (BW)",
        	choices=[1e6,2e6,5e6,10e6,25e6],
        	labels=['1 MHz','2 MHz','5 MHz','10 MHz','25 MHz'],
        	style=wx.RA_HORIZONTAL,
        )
        self.Main.GetPage(0).GridAdd(self._GUI_samp_rate_chooser, 1, 3, 1, 1)
        self.wxgui_scopesink2_2 = scopesink2.scope_sink_f(
        	self.Main.GetPage(1).GetWin(),
        	title="Total Power",
        	sample_rate=2,
        	v_scale=.1,
        	v_offset=0,
        	t_scale=100,
        	ac_couple=False,
        	xy_mode=False,
        	num_inputs=1,
        	trig_mode=wxgui.TRIG_MODE_STRIPCHART,
        	y_axis_label="power level",
        )
        self.Main.GetPage(1).Add(self.wxgui_scopesink2_2.win)
        self.wxgui_numbersink2_2 = numbersink2.number_sink_f(
        	self.GetWin(),
        	unit="Units",
        	minval=0,
        	maxval=1,
        	factor=1.0,
        	decimal_places=10,
        	ref_level=0,
        	sample_rate=GUI_samp_rate,
        	number_rate=15,
        	average=False,
        	avg_alpha=None,
        	label="Number Plot",
        	peak_hold=False,
        	show_gauge=True,
        )
        self.Add(self.wxgui_numbersink2_2.win)
        self.wxgui_numbersink2_0_0 = numbersink2.number_sink_f(
        	self.Main.GetPage(1).GetWin(),
        	unit="",
        	minval=0,
        	maxval=.2,
        	factor=1,
        	decimal_places=6,
        	ref_level=0,
        	sample_rate=scope_rate,
        	number_rate=15,
        	average=True,
        	avg_alpha=.01,
        	label="Raw Power level",
        	peak_hold=False,
        	show_gauge=True,
        )
        self.Main.GetPage(1).Add(self.wxgui_numbersink2_0_0.win)
        self.wxgui_numbersink2_0 = numbersink2.number_sink_f(
        	self.Main.GetPage(1).GetWin(),
        	unit="Kelvin",
        	minval=0,
        	maxval=400,
        	factor=1,
        	decimal_places=6,
        	ref_level=0,
        	sample_rate=scope_rate,
        	number_rate=15,
        	average=False,
        	avg_alpha=None,
        	label="Calibrated Temperature",
        	peak_hold=False,
        	show_gauge=True,
        )
        self.Main.GetPage(1).Add(self.wxgui_numbersink2_0.win)
        self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
        	self.Main.GetPage(0).GetWin(),
        	baseband_freq=freq,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=20,
        	ref_scale=2.0,
        	sample_rate=GUI_samp_rate,
        	fft_size=1024,
        	fft_rate=5,
        	average=True,
        	avg_alpha=0.1,
        	title="Spectrum",
        	peak_hold=False,
        	size=(800,400),
        )
        self.Main.GetPage(0).Add(self.wxgui_fftsink2_0.win)
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join((devid, "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_samp_rate(GUI_samp_rate)
        self.uhd_usrp_source_0.set_center_freq(freq, 0)
        self.uhd_usrp_source_0.set_gain(gain, 0)
        (self.uhd_usrp_source_0).set_processor_affinity([0])
        self._text_samp_rate_static_text = forms.static_text(
        	parent=self.Main.GetPage(0).GetWin(),
        	value=self.text_samp_rate,
        	callback=self.set_text_samp_rate,
        	label="Samp rate",
        	converter=forms.float_converter(),
        )
        self.Main.GetPage(0).GridAdd(self._text_samp_rate_static_text, 2, 0, 1, 1)
        self._text_deviceID_static_text = forms.static_text(
        	parent=self.Main.GetPage(0).GetWin(),
        	value=self.text_deviceID,
        	callback=self.set_text_deviceID,
        	label="SubDev",
        	converter=forms.str_converter(),
        )
        self.Main.GetPage(0).GridAdd(self._text_deviceID_static_text, 2, 1, 1, 1)
        self._text_Device_addr_static_text = forms.static_text(
        	parent=self.Main.GetPage(0).GetWin(),
        	value=self.text_Device_addr,
        	callback=self.set_text_Device_addr,
        	label="Device Address",
        	converter=forms.str_converter(),
        )
        self.Main.GetPage(0).GridAdd(self._text_Device_addr_static_text, 2, 2, 1, 1)
        self.single_pole_iir_filter_xx_0 = filter.single_pole_iir_filter_ff(1.0/((samp_rate*integ)/2.0), 1)
        (self.single_pole_iir_filter_xx_0).set_processor_affinity([1])
        _noise_amplitude_sizer = wx.BoxSizer(wx.VERTICAL)
        self._noise_amplitude_text_box = forms.text_box(
        	parent=self.Main.GetPage(0).GetWin(),
        	sizer=_noise_amplitude_sizer,
        	value=self.noise_amplitude,
        	callback=self.set_noise_amplitude,
        	label='noise_amplitude',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._noise_amplitude_slider = forms.slider(
        	parent=self.Main.GetPage(0).GetWin(),
        	sizer=_noise_amplitude_sizer,
        	value=self.noise_amplitude,
        	callback=self.set_noise_amplitude,
        	minimum=.01,
        	maximum=1,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Main.GetPage(0).GridAdd(_noise_amplitude_sizer, 3, 2, 1, 1)
        self.logpwrfft_x_0 = logpwrfft.logpwrfft_c(
        	sample_rate=samp_rate,
        	fft_size=fftsize,
        	ref_scale=2,
        	frame_rate=fftrate,
        	avg_alpha=1.0/float(spavg*fftrate),
        	average=True,
        )
        self.blocks_peak_detector_xb_0 = blocks.peak_detector_fb(0.25, 0.40, 10, 0.001)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_vff((calib_1, ))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((dc_gain, ))
        self.blocks_keep_one_in_n_4 = blocks.keep_one_in_n(gr.sizeof_float*1, samp_rate/det_rate)
        self.blocks_keep_one_in_n_3 = blocks.keep_one_in_n(gr.sizeof_float*fftsize, fftrate)
        self.blocks_keep_one_in_n_1 = blocks.keep_one_in_n(gr.sizeof_float*1, int(det_rate/file_rate))
        self.blocks_file_sink_5 = blocks.file_sink(gr.sizeof_float*fftsize, spec_data_fifo, False)
        self.blocks_file_sink_5.set_unbuffered(True)
        self.blocks_file_sink_4 = blocks.file_sink(gr.sizeof_float*1, recfile_tpr, False)
        self.blocks_file_sink_4.set_unbuffered(True)
        self.blocks_file_sink_1 = blocks.file_sink(gr.sizeof_gr_complex*1, prefix+"iq_raw" + datetime.now().strftime("%Y.%m.%d.%H.%M.%S") + ".dat", False)
        self.blocks_file_sink_1.set_unbuffered(False)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_float*1, recfile_kelvin, False)
        self.blocks_file_sink_0.set_unbuffered(True)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_mag_squared_1 = blocks.complex_to_mag_squared(1)
        self.blocks_char_to_float_0 = blocks.char_to_float(1, 1)
        self.blocks_add_const_vxx_1 = blocks.add_const_vff((calib_2, ))
        self.blks2_valve_2 = grc_blks2.valve(item_size=gr.sizeof_gr_complex*1, open=bool(rec_button_iq))
        self.blks2_valve_1 = grc_blks2.valve(item_size=gr.sizeof_float*1, open=bool(0))
        self.blks2_valve_0 = grc_blks2.valve(item_size=gr.sizeof_float*1, open=bool(rec_button_tpr))
        self._add_noise_chooser = forms.button(
        	parent=self.Main.GetPage(0).GetWin(),
        	value=self.add_noise,
        	callback=self.set_add_noise,
        	label="Noise Source",
        	choices=[0,1],
        	labels=['Off','On'],
        )
        self.Main.GetPage(0).GridAdd(self._add_noise_chooser, 3, 3, 1, 1)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blks2_valve_0, 0), (self.blocks_file_sink_4, 0))    
        self.connect((self.blks2_valve_1, 0), (self.blocks_file_sink_0, 0))    
        self.connect((self.blks2_valve_2, 0), (self.blocks_file_sink_1, 0))    
        self.connect((self.blocks_add_const_vxx_1, 0), (self.blks2_valve_1, 0))    
        self.connect((self.blocks_add_const_vxx_1, 0), (self.wxgui_numbersink2_0, 0))    
        self.connect((self.blocks_char_to_float_0, 0), (self.wxgui_numbersink2_2, 0))    
        self.connect((self.blocks_complex_to_mag_squared_1, 0), (self.single_pole_iir_filter_xx_0, 0))    
        self.connect((self.blocks_complex_to_real_0, 0), (self.blocks_peak_detector_xb_0, 0))    
        self.connect((self.blocks_keep_one_in_n_1, 0), (self.blks2_valve_0, 0))    
        self.connect((self.blocks_keep_one_in_n_1, 0), (self.blocks_multiply_const_vxx_1, 0))    
        self.connect((self.blocks_keep_one_in_n_1, 0), (self.wxgui_scopesink2_2, 0))    
        self.connect((self.blocks_keep_one_in_n_3, 0), (self.blocks_file_sink_5, 0))    
        self.connect((self.blocks_keep_one_in_n_4, 0), (self.blocks_multiply_const_vxx_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_keep_one_in_n_1, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.wxgui_numbersink2_0_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.blocks_add_const_vxx_1, 0))    
        self.connect((self.blocks_peak_detector_xb_0, 0), (self.blocks_char_to_float_0, 0))    
        self.connect((self.logpwrfft_x_0, 0), (self.blocks_keep_one_in_n_3, 0))    
        self.connect((self.single_pole_iir_filter_xx_0, 0), (self.blocks_keep_one_in_n_4, 0))    
        self.connect((self.uhd_usrp_source_0, 0), (self.blks2_valve_2, 0))    
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_complex_to_mag_squared_1, 0))    
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_complex_to_real_0, 0))    
        self.connect((self.uhd_usrp_source_0, 0), (self.logpwrfft_x_0, 0))    
        self.connect((self.uhd_usrp_source_0, 0), (self.wxgui_fftsink2_0, 0))    


    def get_subdev(self):
        return self.subdev

    def set_subdev(self, subdev):
        self.subdev = subdev
        self.set_text_deviceID(self.subdev)

    def get_devid(self):
        return self.devid

    def set_devid(self, devid):
        self.devid = devid
        self.set_text_Device_addr(self.devid)

    def get_frequency(self):
        return self.frequency

    def set_frequency(self, frequency):
        self.frequency = frequency
        self.set_freq(self.frequency)

    def get_fftsize(self):
        return self.fftsize

    def set_fftsize(self, fftsize):
        self.fftsize = fftsize
        self.set_fftrate(int(self.samp_rate/self.fftsize))

    def get_GUI_samp_rate(self):
        return self.GUI_samp_rate

    def set_GUI_samp_rate(self, GUI_samp_rate):
        self.GUI_samp_rate = GUI_samp_rate
        self.set_samp_rate(int(self.GUI_samp_rate))
        self.set_text_samp_rate(self.GUI_samp_rate)
        self._GUI_samp_rate_chooser.set_value(self.GUI_samp_rate)
        self.uhd_usrp_source_0.set_samp_rate(self.GUI_samp_rate)
        self.wxgui_fftsink2_0.set_sample_rate(self.GUI_samp_rate)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_fftrate(int(self.samp_rate/self.fftsize))
        self.logpwrfft_x_0.set_sample_rate(self.samp_rate)
        self.single_pole_iir_filter_xx_0.set_taps(1.0/((self.samp_rate*self.integ)/2.0))
        self.blocks_keep_one_in_n_4.set_n(self.samp_rate/self.det_rate)

    def get_prefix(self):
        return self.prefix

    def set_prefix(self, prefix):
        self.prefix = prefix
        self.set_recfile_kelvin(self.prefix+"kelvin" + datetime.now().strftime("%Y.%m.%d.%H.%M.%S") + ".dat")
        self.set_recfile_tpr(self.prefix + datetime.now().strftime("%Y.%m.%d.%H.%M.%S") + ".dat")
        self.blocks_file_sink_1.open(self.prefix+"iq_raw" + datetime.now().strftime("%Y.%m.%d.%H.%M.%S") + ".dat")

    def get_text_samp_rate(self):
        return self.text_samp_rate

    def set_text_samp_rate(self, text_samp_rate):
        self.text_samp_rate = text_samp_rate
        self._text_samp_rate_static_text.set_value(self.text_samp_rate)

    def get_text_deviceID(self):
        return self.text_deviceID

    def set_text_deviceID(self, text_deviceID):
        self.text_deviceID = text_deviceID
        self._text_deviceID_static_text.set_value(self.text_deviceID)

    def get_text_Device_addr(self):
        return self.text_Device_addr

    def set_text_Device_addr(self, text_Device_addr):
        self.text_Device_addr = text_Device_addr
        self._text_Device_addr_static_text.set_value(self.text_Device_addr)

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
        self._spavg_slider.set_value(self.spavg)
        self._spavg_text_box.set_value(self.spavg)

    def get_scope_rate(self):
        return self.scope_rate

    def set_scope_rate(self, scope_rate):
        self.scope_rate = scope_rate

    def get_recfile_tpr(self):
        return self.recfile_tpr

    def set_recfile_tpr(self, recfile_tpr):
        self.recfile_tpr = recfile_tpr
        self.blocks_file_sink_4.open(self.recfile_tpr)

    def get_recfile_kelvin(self):
        return self.recfile_kelvin

    def set_recfile_kelvin(self, recfile_kelvin):
        self.recfile_kelvin = recfile_kelvin
        self.blocks_file_sink_0.open(self.recfile_kelvin)

    def get_rec_button_tpr(self):
        return self.rec_button_tpr

    def set_rec_button_tpr(self, rec_button_tpr):
        self.rec_button_tpr = rec_button_tpr
        self._rec_button_tpr_chooser.set_value(self.rec_button_tpr)
        self.blks2_valve_0.set_open(bool(self.rec_button_tpr))

    def get_rec_button_iq(self):
        return self.rec_button_iq

    def set_rec_button_iq(self, rec_button_iq):
        self.rec_button_iq = rec_button_iq
        self.blks2_valve_2.set_open(bool(self.rec_button_iq))
        self._rec_button_iq_chooser.set_value(self.rec_button_iq)

    def get_noise_amplitude(self):
        return self.noise_amplitude

    def set_noise_amplitude(self, noise_amplitude):
        self.noise_amplitude = noise_amplitude
        self._noise_amplitude_slider.set_value(self.noise_amplitude)
        self._noise_amplitude_text_box.set_value(self.noise_amplitude)

    def get_integ(self):
        return self.integ

    def set_integ(self, integ):
        self.integ = integ
        self._integ_slider.set_value(self.integ)
        self._integ_text_box.set_value(self.integ)
        self.single_pole_iir_filter_xx_0.set_taps(1.0/((self.samp_rate*self.integ)/2.0))

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self._gain_slider.set_value(self.gain)
        self._gain_text_box.set_value(self.gain)
        self.uhd_usrp_source_0.set_gain(self.gain, 0)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self._freq_text_box.set_value(self.freq)
        self.uhd_usrp_source_0.set_center_freq(self.freq, 0)
        self.wxgui_fftsink2_0.set_baseband_freq(self.freq)

    def get_file_rate(self):
        return self.file_rate

    def set_file_rate(self, file_rate):
        self.file_rate = file_rate
        self.blocks_keep_one_in_n_1.set_n(int(self.det_rate/self.file_rate))

    def get_fftrate(self):
        return self.fftrate

    def set_fftrate(self, fftrate):
        self.fftrate = fftrate
        self.logpwrfft_x_0.set_avg_alpha(1.0/float(self.spavg*self.fftrate))
        self.blocks_keep_one_in_n_3.set_n(self.fftrate)

    def get_det_rate(self):
        return self.det_rate

    def set_det_rate(self, det_rate):
        self.det_rate = det_rate
        self.blocks_keep_one_in_n_4.set_n(self.samp_rate/self.det_rate)
        self.blocks_keep_one_in_n_1.set_n(int(self.det_rate/self.file_rate))

    def get_dc_gain(self):
        return self.dc_gain

    def set_dc_gain(self, dc_gain):
        self.dc_gain = dc_gain
        self._dc_gain_chooser.set_value(self.dc_gain)
        self.blocks_multiply_const_vxx_0.set_k((self.dc_gain, ))

    def get_calib_2(self):
        return self.calib_2

    def set_calib_2(self, calib_2):
        self.calib_2 = calib_2
        self._calib_2_text_box.set_value(self.calib_2)
        self.blocks_add_const_vxx_1.set_k((self.calib_2, ))

    def get_calib_1(self):
        return self.calib_1

    def set_calib_1(self, calib_1):
        self.calib_1 = calib_1
        self._calib_1_text_box.set_value(self.calib_1)
        self.blocks_multiply_const_vxx_1.set_k((self.calib_1, ))

    def get_add_noise(self):
        return self.add_noise

    def set_add_noise(self, add_noise):
        self.add_noise = add_noise
        self._add_noise_chooser.set_value(self.add_noise)

if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    parser.add_option("", "--subdev", dest="subdev", type="string", default="A:0",
        help="Set USRP Subdevice ID [default=%default]")
    parser.add_option("", "--devid", dest="devid", type="string", default="addr=192.168.10.2",
        help="Set USRP Device ID [default=%default]")
    parser.add_option("", "--frequency", dest="frequency", type="eng_float", default=eng_notation.num_to_str(1.4125e9),
        help="Set Center Frequency [default=%default]")
    parser.add_option("", "--fftsize", dest="fftsize", type="intx", default=8192,
        help="Set fftsize [default=%default]")
    (options, args) = parser.parse_args()
    tb = N200_TPR(subdev=options.subdev, devid=options.devid, frequency=options.frequency, fftsize=options.fftsize)
    tb.Start(True)
    tb.Wait()
