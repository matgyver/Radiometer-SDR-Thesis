#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Total Power Radiometer - N200
# Author: Matthew E Nelson
# Description: Total power radiometer connecting to a N200 SDR
# Generated: Sun Mar 23 00:54:34 2014
##################################################

from datetime import datetime
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

    def __init__(self, dcg=1, devid="addr=192.168.10.2", srate=10.0e6, spa=1, rxant="", tpint=2.0, rfgain=0.0, frequency=1.406e9, decln=-28.0, subdev="A:0", maxg=50, fftsize=8192, clock=100.0e6):
        grc_wxgui.top_block_gui.__init__(self, title="Total Power Radiometer - N200")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Parameters
        ##################################################
        self.dcg = dcg
        self.devid = devid
        self.srate = srate
        self.spa = spa
        self.rxant = rxant
        self.tpint = tpint
        self.rfgain = rfgain
        self.frequency = frequency
        self.decln = decln
        self.subdev = subdev
        self.maxg = maxg
        self.fftsize = fftsize
        self.clock = clock

        ##################################################
        # Variables
        ##################################################
        self.israte = israte = srate
        self.samp_rate = samp_rate = int(israte)
        self.prefix = prefix = "tpr_"
        self.variable_static_text_0_0_0_0 = variable_static_text_0_0_0_0 = clock
        self.variable_static_text_0_0_0 = variable_static_text_0_0_0 = devid
        self.variable_static_text_0_0 = variable_static_text_0_0 = subdev
        self.variable_static_text_0 = variable_static_text_0 = israte
        self.spec_data_fifo = spec_data_fifo = "spectrum_" + datetime.now().strftime("%Y.%m.%d.%H.%M.%S") + ".dat"
        self.spavg = spavg = int(spa)
        self.scope_rate = scope_rate = 2.0
        self.recfile_tpr = recfile_tpr = prefix + datetime.now().strftime("%Y.%m.%d.%H.%M.%S") + ".dat"
        self.recfile_kelvin = recfile_kelvin = prefix+"kelvin" + datetime.now().strftime("%Y.%m.%d.%H.%M.%S") + ".dat"
        self.rec_button_tpr = rec_button_tpr = 1
        self.rec_button_iq = rec_button_iq = 1
        self.noise_amplitude = noise_amplitude = .5
        self.integ = integ = tpint
        self.idecln = idecln = decln
        self.gain = gain = 23
        self.freq = freq = frequency
        self.file_rate = file_rate = 2.0
        self.fftrate = fftrate = int(samp_rate/fftsize)
        self.det_rate = det_rate = int(20.0)
        self.dc_gain = dc_gain = int(dcg)
        self.calib_2 = calib_2 = -342.774
        self.calib_1 = calib_1 = 4.0755e3
        self.add_noise = add_noise = 0

        ##################################################
        # Blocks
        ##################################################
        self.Main = self.Main = wx.Notebook(self.GetWin(), style=wx.NB_TOP)
        self.Main.AddPage(grc_wxgui.Panel(self.Main), "Continuum + Controls")
        self.Main.AddPage(grc_wxgui.Panel(self.Main), "Spectral")
        self.Main.AddPage(grc_wxgui.Panel(self.Main), "Meter")
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
        self._israte_chooser = forms.radio_buttons(
        	parent=self.Main.GetPage(0).GetWin(),
        	value=self.israte,
        	callback=self.set_israte,
        	label="Sample Rate (BW)",
        	choices=[1e6,2e6,5e6,10e6,25e6],
        	labels=['1 MHz','2 MHz','5 MHz','10 MHz','25 MHz'],
        	style=wx.RA_HORIZONTAL,
        )
        self.Main.GetPage(0).GridAdd(self._israte_chooser, 1, 3, 1, 1)
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
        	maximum=maxg,
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
        self.wxgui_scopesink2_0 = scopesink2.scope_sink_f(
        	self.Main.GetPage(0).GetWin(),
        	title="Total Power",
        	sample_rate=scope_rate,
        	v_scale=0,
        	v_offset=0,
        	t_scale=450,
        	ac_couple=False,
        	xy_mode=False,
        	num_inputs=1,
        	trig_mode=wxgui.TRIG_MODE_AUTO,
        	y_axis_label="Power Level",
        	size=(800,300),
        )
        self.Main.GetPage(0).Add(self.wxgui_scopesink2_0.win)
        self.wxgui_numbersink2_0 = numbersink2.number_sink_f(
        	self.Main.GetPage(2).GetWin(),
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
        	label="Number Plot",
        	peak_hold=False,
        	show_gauge=True,
        )
        self.Main.GetPage(2).Add(self.wxgui_numbersink2_0.win)
        self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
        	self.Main.GetPage(1).GetWin(),
        	baseband_freq=freq,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=50,
        	ref_scale=2.0,
        	sample_rate=israte,
        	fft_size=1024,
        	fft_rate=5,
        	average=True,
        	avg_alpha=0.1,
        	title="Spectrum",
        	peak_hold=False,
        	size=(800,400),
        )
        self.Main.GetPage(1).Add(self.wxgui_fftsink2_0.win)
        self._variable_static_text_0_0_0_0_static_text = forms.static_text(
        	parent=self.Main.GetPage(0).GetWin(),
        	value=self.variable_static_text_0_0_0_0,
        	callback=self.set_variable_static_text_0_0_0_0,
        	label="USRP Clock",
        	converter=forms.float_converter(),
        )
        self.Main.GetPage(0).GridAdd(self._variable_static_text_0_0_0_0_static_text, 2, 3, 1, 1)
        self._variable_static_text_0_0_0_static_text = forms.static_text(
        	parent=self.Main.GetPage(0).GetWin(),
        	value=self.variable_static_text_0_0_0,
        	callback=self.set_variable_static_text_0_0_0,
        	label="Device",
        	converter=forms.str_converter(),
        )
        self.Main.GetPage(0).GridAdd(self._variable_static_text_0_0_0_static_text, 2, 2, 1, 1)
        self._variable_static_text_0_0_static_text = forms.static_text(
        	parent=self.Main.GetPage(0).GetWin(),
        	value=self.variable_static_text_0_0,
        	callback=self.set_variable_static_text_0_0,
        	label="SubDev",
        	converter=forms.str_converter(),
        )
        self.Main.GetPage(0).GridAdd(self._variable_static_text_0_0_static_text, 2, 1, 1, 1)
        self._variable_static_text_0_static_text = forms.static_text(
        	parent=self.Main.GetPage(0).GetWin(),
        	value=self.variable_static_text_0,
        	callback=self.set_variable_static_text_0,
        	label="Samp rate",
        	converter=forms.float_converter(),
        )
        self.Main.GetPage(0).GridAdd(self._variable_static_text_0_static_text, 2, 0, 1, 1)
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	device_addr=devid,
        	stream_args=uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_center_freq(freq, 0)
        self.uhd_usrp_source_0.set_gain(gain, 0)
        self.single_pole_iir_filter_xx_0 = filter.single_pole_iir_filter_ff(1.0/((samp_rate*integ)/2.0), 1)
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
        self._idecln_text_box = forms.text_box(
        	parent=self.Main.GetPage(0).GetWin(),
        	value=self.idecln,
        	callback=self.set_idecln,
        	label="Declination",
        	converter=forms.float_converter(),
        )
        self.Main.GetPage(0).GridAdd(self._idecln_text_box, 1, 2, 1, 1)
        self.gr_multiply_const_vxx_1 = gr.multiply_const_vff((calib_1, ))
        self.gr_multiply_const_vxx_0 = gr.multiply_const_vff((dc_gain, ))
        self.gr_keep_one_in_n_3 = gr.keep_one_in_n(gr.sizeof_float*1, int(det_rate/file_rate))
        self.gr_keep_one_in_n_2 = gr.keep_one_in_n(gr.sizeof_float*1, int(det_rate/scope_rate))
        self.gr_keep_one_in_n_1 = gr.keep_one_in_n(gr.sizeof_float*fftsize, fftrate)
        self.gr_keep_one_in_n_0 = gr.keep_one_in_n(gr.sizeof_float*1, samp_rate/det_rate)
        self.gr_file_sink_3 = gr.file_sink(gr.sizeof_gr_complex*1, prefix+"iq_raw" + datetime.now().strftime("%Y.%m.%d.%H.%M.%S") + ".dat")
        self.gr_file_sink_3.set_unbuffered(False)
        self.gr_file_sink_2 = gr.file_sink(gr.sizeof_float*1, recfile_kelvin)
        self.gr_file_sink_2.set_unbuffered(True)
        self.gr_file_sink_1 = gr.file_sink(gr.sizeof_float*fftsize, spec_data_fifo)
        self.gr_file_sink_1.set_unbuffered(True)
        self.gr_file_sink_0 = gr.file_sink(gr.sizeof_float*1, recfile_tpr)
        self.gr_file_sink_0.set_unbuffered(True)
        self.gr_complex_to_mag_squared_0 = gr.complex_to_mag_squared(1)
        self.gr_add_const_vxx_0 = gr.add_const_vff((calib_2, ))
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
        self.connect((self.gr_keep_one_in_n_0, 0), (self.gr_multiply_const_vxx_0, 0))
        self.connect((self.gr_keep_one_in_n_1, 0), (self.gr_file_sink_1, 0))
        self.connect((self.gr_keep_one_in_n_2, 0), (self.wxgui_scopesink2_0, 0))
        self.connect((self.gr_multiply_const_vxx_0, 0), (self.gr_keep_one_in_n_2, 0))
        self.connect((self.gr_multiply_const_vxx_0, 0), (self.gr_keep_one_in_n_3, 0))
        self.connect((self.gr_keep_one_in_n_3, 0), (self.gr_multiply_const_vxx_1, 0))
        self.connect((self.gr_add_const_vxx_0, 0), (self.wxgui_numbersink2_0, 0))
        self.connect((self.gr_multiply_const_vxx_1, 0), (self.gr_add_const_vxx_0, 0))
        self.connect((self.gr_keep_one_in_n_3, 0), (self.blks2_valve_0, 0))
        self.connect((self.blks2_valve_0, 0), (self.gr_file_sink_0, 0))
        self.connect((self.gr_add_const_vxx_0, 0), (self.blks2_valve_1, 0))
        self.connect((self.blks2_valve_1, 0), (self.gr_file_sink_2, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.blks2_valve_2, 0))
        self.connect((self.blks2_valve_2, 0), (self.gr_file_sink_3, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.gr_complex_to_mag_squared_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.wxgui_fftsink2_0, 0))
        self.connect((self.gr_complex_to_mag_squared_0, 0), (self.single_pole_iir_filter_xx_0, 0))
        self.connect((self.single_pole_iir_filter_xx_0, 0), (self.gr_keep_one_in_n_0, 0))
        self.connect((self.logpwrfft_x_0, 0), (self.gr_keep_one_in_n_1, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.logpwrfft_x_0, 0))


# QT sink close method reimplementation

    def get_dcg(self):
        return self.dcg

    def set_dcg(self, dcg):
        self.dcg = dcg
        self.set_dc_gain(int(self.dcg))

    def get_devid(self):
        return self.devid

    def set_devid(self, devid):
        self.devid = devid
        self.set_variable_static_text_0_0_0(self.devid)

    def get_srate(self):
        return self.srate

    def set_srate(self, srate):
        self.srate = srate
        self.set_israte(self.srate)

    def get_spa(self):
        return self.spa

    def set_spa(self, spa):
        self.spa = spa
        self.set_spavg(int(self.spa))

    def get_rxant(self):
        return self.rxant

    def set_rxant(self, rxant):
        self.rxant = rxant

    def get_tpint(self):
        return self.tpint

    def set_tpint(self, tpint):
        self.tpint = tpint
        self.set_integ(self.tpint)

    def get_rfgain(self):
        return self.rfgain

    def set_rfgain(self, rfgain):
        self.rfgain = rfgain

    def get_frequency(self):
        return self.frequency

    def set_frequency(self, frequency):
        self.frequency = frequency
        self.set_freq(self.frequency)

    def get_decln(self):
        return self.decln

    def set_decln(self, decln):
        self.decln = decln
        self.set_idecln(self.decln)

    def get_subdev(self):
        return self.subdev

    def set_subdev(self, subdev):
        self.subdev = subdev
        self.set_variable_static_text_0_0(self.subdev)

    def get_maxg(self):
        return self.maxg

    def set_maxg(self, maxg):
        self.maxg = maxg

    def get_fftsize(self):
        return self.fftsize

    def set_fftsize(self, fftsize):
        self.fftsize = fftsize
        self.set_fftrate(int(self.samp_rate/self.fftsize))

    def get_clock(self):
        return self.clock

    def set_clock(self, clock):
        self.clock = clock
        self.set_variable_static_text_0_0_0_0(self.clock)

    def get_israte(self):
        return self.israte

    def set_israte(self, israte):
        self.israte = israte
        self.set_samp_rate(int(self.israte))
        self._israte_chooser.set_value(self.israte)
        self.set_variable_static_text_0(self.israte)
        self.wxgui_fftsink2_0.set_sample_rate(self.israte)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_fftrate(int(self.samp_rate/self.fftsize))
        self.single_pole_iir_filter_xx_0.set_taps(1.0/((self.samp_rate*self.integ)/2.0))
        self.gr_keep_one_in_n_0.set_n(self.samp_rate/self.det_rate)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
        self.logpwrfft_x_0.set_sample_rate(self.samp_rate)

    def get_prefix(self):
        return self.prefix

    def set_prefix(self, prefix):
        self.prefix = prefix
        self.set_recfile_kelvin(self.prefix+"kelvin" + datetime.now().strftime("%Y.%m.%d.%H.%M.%S") + ".dat")
        self.set_recfile_tpr(self.prefix + datetime.now().strftime("%Y.%m.%d.%H.%M.%S") + ".dat")
        self.gr_file_sink_3.open(self.prefix+"iq_raw" + datetime.now().strftime("%Y.%m.%d.%H.%M.%S") + ".dat")

    def get_variable_static_text_0_0_0_0(self):
        return self.variable_static_text_0_0_0_0

    def set_variable_static_text_0_0_0_0(self, variable_static_text_0_0_0_0):
        self.variable_static_text_0_0_0_0 = variable_static_text_0_0_0_0
        self._variable_static_text_0_0_0_0_static_text.set_value(self.variable_static_text_0_0_0_0)

    def get_variable_static_text_0_0_0(self):
        return self.variable_static_text_0_0_0

    def set_variable_static_text_0_0_0(self, variable_static_text_0_0_0):
        self.variable_static_text_0_0_0 = variable_static_text_0_0_0
        self._variable_static_text_0_0_0_static_text.set_value(self.variable_static_text_0_0_0)

    def get_variable_static_text_0_0(self):
        return self.variable_static_text_0_0

    def set_variable_static_text_0_0(self, variable_static_text_0_0):
        self.variable_static_text_0_0 = variable_static_text_0_0
        self._variable_static_text_0_0_static_text.set_value(self.variable_static_text_0_0)

    def get_variable_static_text_0(self):
        return self.variable_static_text_0

    def set_variable_static_text_0(self, variable_static_text_0):
        self.variable_static_text_0 = variable_static_text_0
        self._variable_static_text_0_static_text.set_value(self.variable_static_text_0)

    def get_spec_data_fifo(self):
        return self.spec_data_fifo

    def set_spec_data_fifo(self, spec_data_fifo):
        self.spec_data_fifo = spec_data_fifo
        self.gr_file_sink_1.open(self.spec_data_fifo)

    def get_spavg(self):
        return self.spavg

    def set_spavg(self, spavg):
        self.spavg = spavg
        self._spavg_slider.set_value(self.spavg)
        self._spavg_text_box.set_value(self.spavg)
        self.logpwrfft_x_0.set_avg_alpha(1.0/float(self.spavg*self.fftrate))

    def get_scope_rate(self):
        return self.scope_rate

    def set_scope_rate(self, scope_rate):
        self.scope_rate = scope_rate
        self.wxgui_scopesink2_0.set_sample_rate(self.scope_rate)
        self.gr_keep_one_in_n_2.set_n(int(self.det_rate/self.scope_rate))

    def get_recfile_tpr(self):
        return self.recfile_tpr

    def set_recfile_tpr(self, recfile_tpr):
        self.recfile_tpr = recfile_tpr
        self.gr_file_sink_0.open(self.recfile_tpr)

    def get_recfile_kelvin(self):
        return self.recfile_kelvin

    def set_recfile_kelvin(self, recfile_kelvin):
        self.recfile_kelvin = recfile_kelvin
        self.gr_file_sink_2.open(self.recfile_kelvin)

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
        self._rec_button_iq_chooser.set_value(self.rec_button_iq)
        self.blks2_valve_2.set_open(bool(self.rec_button_iq))

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

    def get_idecln(self):
        return self.idecln

    def set_idecln(self, idecln):
        self.idecln = idecln
        self._idecln_text_box.set_value(self.idecln)

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
        self.wxgui_fftsink2_0.set_baseband_freq(self.freq)
        self.uhd_usrp_source_0.set_center_freq(self.freq, 0)

    def get_file_rate(self):
        return self.file_rate

    def set_file_rate(self, file_rate):
        self.file_rate = file_rate
        self.gr_keep_one_in_n_3.set_n(int(self.det_rate/self.file_rate))

    def get_fftrate(self):
        return self.fftrate

    def set_fftrate(self, fftrate):
        self.fftrate = fftrate
        self.gr_keep_one_in_n_1.set_n(self.fftrate)
        self.logpwrfft_x_0.set_avg_alpha(1.0/float(self.spavg*self.fftrate))

    def get_det_rate(self):
        return self.det_rate

    def set_det_rate(self, det_rate):
        self.det_rate = det_rate
        self.gr_keep_one_in_n_3.set_n(int(self.det_rate/self.file_rate))
        self.gr_keep_one_in_n_2.set_n(int(self.det_rate/self.scope_rate))
        self.gr_keep_one_in_n_0.set_n(self.samp_rate/self.det_rate)

    def get_dc_gain(self):
        return self.dc_gain

    def set_dc_gain(self, dc_gain):
        self.dc_gain = dc_gain
        self._dc_gain_chooser.set_value(self.dc_gain)
        self.gr_multiply_const_vxx_0.set_k((self.dc_gain, ))

    def get_calib_2(self):
        return self.calib_2

    def set_calib_2(self, calib_2):
        self.calib_2 = calib_2
        self.gr_add_const_vxx_0.set_k((self.calib_2, ))
        self._calib_2_text_box.set_value(self.calib_2)

    def get_calib_1(self):
        return self.calib_1

    def set_calib_1(self, calib_1):
        self.calib_1 = calib_1
        self.gr_multiply_const_vxx_1.set_k((self.calib_1, ))
        self._calib_1_text_box.set_value(self.calib_1)

    def get_add_noise(self):
        return self.add_noise

    def set_add_noise(self, add_noise):
        self.add_noise = add_noise
        self._add_noise_chooser.set_value(self.add_noise)

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    parser.add_option("", "--dcg", dest="dcg", type="eng_float", default=eng_notation.num_to_str(1),
        help="Set DC (post-detector) gain [default=%default]")
    parser.add_option("", "--devid", dest="devid", type="string", default="addr=192.168.10.2",
        help="Set USRP Device ID [default=%default]")
    parser.add_option("", "--srate", dest="srate", type="eng_float", default=eng_notation.num_to_str(10.0e6),
        help="Set Sample Rate [default=%default]")
    parser.add_option("", "--spa", dest="spa", type="eng_float", default=eng_notation.num_to_str(1),
        help="Set Spectral Averaging Constant [default=%default]")
    parser.add_option("", "--rxant", dest="rxant", type="string", default="",
        help="Set RX Antenna selection [default=%default]")
    parser.add_option("", "--tpint", dest="tpint", type="eng_float", default=eng_notation.num_to_str(2.0),
        help="Set Integration Time [default=%default]")
    parser.add_option("", "--rfgain", dest="rfgain", type="eng_float", default=eng_notation.num_to_str(0.0),
        help="Set Gain of RF Front-End [default=%default]")
    parser.add_option("", "--frequency", dest="frequency", type="eng_float", default=eng_notation.num_to_str(1.406e9),
        help="Set Center Frequency [default=%default]")
    parser.add_option("", "--decln", dest="decln", type="eng_float", default=eng_notation.num_to_str(-28.0),
        help="Set Declination [default=%default]")
    parser.add_option("", "--subdev", dest="subdev", type="string", default="A:0",
        help="Set USRP Subdevice ID [default=%default]")
    parser.add_option("", "--maxg", dest="maxg", type="intx", default=50,
        help="Set maxg [default=%default]")
    parser.add_option("", "--fftsize", dest="fftsize", type="intx", default=8192,
        help="Set fftsize [default=%default]")
    parser.add_option("", "--clock", dest="clock", type="eng_float", default=eng_notation.num_to_str(100.0e6),
        help="Set Clock rate [default=%default]")
    (options, args) = parser.parse_args()
    tb = N200_TPR(dcg=options.dcg, devid=options.devid, srate=options.srate, spa=options.spa, rxant=options.rxant, tpint=options.tpint, rfgain=options.rfgain, frequency=options.frequency, decln=options.decln, subdev=options.subdev, maxg=options.maxg, fftsize=options.fftsize, clock=options.clock)
    tb.Start(True)
    tb.Wait()

