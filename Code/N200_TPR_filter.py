#!/usr/bin/env python2
##################################################
# GNU Radio Python Flow Graph
# Title: Total Power Radiometer - N200 with Filter
# Author: Matthew E Nelson
# Description: Total power radiometer connecting to a N200 SDR with a bandpass filter
# Generated: Mon Jul 27 11:21:54 2015
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

execfile("/Users/matthewnelson/.grc_gnuradio/TPR.py")
from datetime import datetime
from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
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
import wx

class N200_TPR_filter(grc_wxgui.top_block_gui):

    def __init__(self, clock=100.0e6, dcg=1, decln=-28.0, devid="addr=192.168.10.2", fftsize=8192, frequency=1.406e9, maxg=50, rfgain=0.0, rxant="", spa=1, srate=10.0e6, subdev="A:0", tpint=2.0):
        grc_wxgui.top_block_gui.__init__(self, title="Total Power Radiometer - N200 with Filter")

        ##################################################
        # Parameters
        ##################################################
        self.clock = clock
        self.dcg = dcg
        self.decln = decln
        self.devid = devid
        self.fftsize = fftsize
        self.frequency = frequency
        self.maxg = maxg
        self.rfgain = rfgain
        self.rxant = rxant
        self.spa = spa
        self.srate = srate
        self.subdev = subdev
        self.tpint = tpint

        ##################################################
        # Variables
        ##################################################
        self.israte = israte = srate
        self.samp_rate = samp_rate = int(israte)
        self.prefix = prefix = "tpr_"
        self.filter_band = filter_band = 500e3
        self.variable_static_text_0_0_0_0 = variable_static_text_0_0_0_0 = clock
        self.variable_static_text_0_0_0 = variable_static_text_0_0_0 = devid
        self.variable_static_text_0_0 = variable_static_text_0_0 = subdev
        self.variable_static_text_0 = variable_static_text_0 = israte
        self.taps = taps = firdes.low_pass(1.0, samp_rate,filter_band, 1000)
        self.spec_data_fifo = spec_data_fifo = "spectrum_" + datetime.now().strftime("%Y.%m.%d.%H.%M.%S") + ".dat"
        self.spavg = spavg = int(spa)
        self.scope_rate = scope_rate = 2
        self.recfile_tpr = recfile_tpr = prefix + datetime.now().strftime("%Y.%m.%d.%H.%M.%S") + ".dat"
        self.recfile_kelvin = recfile_kelvin = prefix+"kelvin" + datetime.now().strftime("%Y.%m.%d.%H.%M.%S") + ".dat"
        self.rec_button_tpr = rec_button_tpr = 1
        self.rec_button_iq = rec_button_iq = 1
        self.integ = integ = tpint
        self.idecln = idecln = decln
        self.gain = gain = 26
        self.freq = freq = frequency
        self.file_rate = file_rate = 2.0
        self.fftrate = fftrate = int(samp_rate/fftsize)
        self.det_rate = det_rate = int(20.0)
        self.dc_gain = dc_gain = int(dcg)
        self.calib_2 = calib_2 = -342.774
        self.calib_1 = calib_1 = 4.0755e3
        self.add_filter = add_filter = 0

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
        self._add_filter_chooser = forms.button(
        	parent=self.Main.GetPage(0).GetWin(),
        	value=self.add_filter,
        	callback=self.set_add_filter,
        	label="Filter On/Off",
        	choices=[0,1],
        	labels=['Off','On'],
        )
        self.Main.GetPage(0).GridAdd(self._add_filter_chooser, 3, 3, 1, 1)
        self.wxgui_scopesink2_2 = scopesink2.scope_sink_f(
        	self.Main.GetPage(1).GetWin(),
        	title="Total Power",
        	sample_rate=2,
        	v_scale=0,
        	v_offset=0,
        	t_scale=0,
        	ac_couple=False,
        	xy_mode=False,
        	num_inputs=1,
        	trig_mode=wxgui.TRIG_MODE_STRIPCHART,
        	y_axis_label="power level",
        )
        self.Main.GetPage(1).Add(self.wxgui_scopesink2_2.win)
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
        	average=False,
        	avg_alpha=None,
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
        self.Main.GetPage(0).Add(self.wxgui_fftsink2_0.win)
        self._variable_static_text_0_0_0_0_static_text = forms.static_text(
        	parent=self.Main.GetPage(0).GetWin(),
        	value=self.variable_static_text_0_0_0_0,
        	callback=self.set_variable_static_text_0_0_0_0,
        	label="N200 Clock",
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
        _filter_band_sizer = wx.BoxSizer(wx.VERTICAL)
        self._filter_band_text_box = forms.text_box(
        	parent=self.Main.GetPage(0).GetWin(),
        	sizer=_filter_band_sizer,
        	value=self.filter_band,
        	callback=self.set_filter_band,
        	label="Filter Bandwidth",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._filter_band_slider = forms.slider(
        	parent=self.Main.GetPage(0).GetWin(),
        	sizer=_filter_band_sizer,
        	value=self.filter_band,
        	callback=self.set_filter_band,
        	minimum=100e3,
        	maximum=9e6,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Main.GetPage(0).GridAdd(_filter_band_sizer, 3, 2, 1, 1)
        self.fft_filter_xxx_0 = filter.fft_filter_ccc(1, (taps), 1)
        self.fft_filter_xxx_0.declare_sample_delay(0)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_vff((calib_1, ))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((dc_gain, ))
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
        self.blocks_add_const_vxx_1 = blocks.add_const_vff((calib_2, ))
        self.blks2_valve_2 = grc_blks2.valve(item_size=gr.sizeof_gr_complex*1, open=bool(rec_button_iq))
        self.blks2_valve_1 = grc_blks2.valve(item_size=gr.sizeof_float*1, open=bool(0))
        self.blks2_valve_0 = grc_blks2.valve(item_size=gr.sizeof_float*1, open=bool(rec_button_tpr))
        self.blks2_selector_0 = grc_blks2.selector(
        	item_size=gr.sizeof_gr_complex*1,
        	num_inputs=2,
        	num_outputs=1,
        	input_index=add_filter,
        	output_index=0,
        )
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, .5, 0)
        self.TPR_0 = TPR(
            integ=integ,
            samp_rate=samp_rate,
            det_rate=det_rate,
        )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.TPR_0, 0), (self.blocks_multiply_const_vxx_0, 0))    
        self.connect((self.analog_noise_source_x_0, 0), (self.blks2_selector_0, 0))    
        self.connect((self.analog_noise_source_x_0, 0), (self.fft_filter_xxx_0, 0))    
        self.connect((self.blks2_selector_0, 0), (self.TPR_0, 0))    
        self.connect((self.blks2_selector_0, 0), (self.blks2_valve_2, 0))    
        self.connect((self.blks2_selector_0, 0), (self.logpwrfft_x_0, 0))    
        self.connect((self.blks2_selector_0, 0), (self.wxgui_fftsink2_0, 0))    
        self.connect((self.blks2_valve_0, 0), (self.blocks_file_sink_4, 0))    
        self.connect((self.blks2_valve_1, 0), (self.blocks_file_sink_0, 0))    
        self.connect((self.blks2_valve_2, 0), (self.blocks_file_sink_1, 0))    
        self.connect((self.blocks_add_const_vxx_1, 0), (self.blks2_valve_1, 0))    
        self.connect((self.blocks_add_const_vxx_1, 0), (self.wxgui_numbersink2_0, 0))    
        self.connect((self.blocks_keep_one_in_n_1, 0), (self.blks2_valve_0, 0))    
        self.connect((self.blocks_keep_one_in_n_1, 0), (self.blocks_multiply_const_vxx_1, 0))    
        self.connect((self.blocks_keep_one_in_n_3, 0), (self.blocks_file_sink_5, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_keep_one_in_n_1, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.wxgui_numbersink2_0_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.wxgui_scopesink2_2, 0))    
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.blocks_add_const_vxx_1, 0))    
        self.connect((self.fft_filter_xxx_0, 0), (self.blks2_selector_0, 1))    
        self.connect((self.logpwrfft_x_0, 0), (self.blocks_keep_one_in_n_3, 0))    


    def get_clock(self):
        return self.clock

    def set_clock(self, clock):
        self.clock = clock
        self.set_variable_static_text_0_0_0_0(self.clock)

    def get_dcg(self):
        return self.dcg

    def set_dcg(self, dcg):
        self.dcg = dcg
        self.set_dc_gain(int(self.dcg))

    def get_decln(self):
        return self.decln

    def set_decln(self, decln):
        self.decln = decln
        self.set_idecln(self.decln)

    def get_devid(self):
        return self.devid

    def set_devid(self, devid):
        self.devid = devid
        self.set_variable_static_text_0_0_0(self.devid)

    def get_fftsize(self):
        return self.fftsize

    def set_fftsize(self, fftsize):
        self.fftsize = fftsize
        self.set_fftrate(int(self.samp_rate/self.fftsize))

    def get_frequency(self):
        return self.frequency

    def set_frequency(self, frequency):
        self.frequency = frequency
        self.set_freq(self.frequency)

    def get_maxg(self):
        return self.maxg

    def set_maxg(self, maxg):
        self.maxg = maxg

    def get_rfgain(self):
        return self.rfgain

    def set_rfgain(self, rfgain):
        self.rfgain = rfgain

    def get_rxant(self):
        return self.rxant

    def set_rxant(self, rxant):
        self.rxant = rxant

    def get_spa(self):
        return self.spa

    def set_spa(self, spa):
        self.spa = spa
        self.set_spavg(int(self.spa))

    def get_srate(self):
        return self.srate

    def set_srate(self, srate):
        self.srate = srate
        self.set_israte(self.srate)

    def get_subdev(self):
        return self.subdev

    def set_subdev(self, subdev):
        self.subdev = subdev
        self.set_variable_static_text_0_0(self.subdev)

    def get_tpint(self):
        return self.tpint

    def set_tpint(self, tpint):
        self.tpint = tpint
        self.set_integ(self.tpint)

    def get_israte(self):
        return self.israte

    def set_israte(self, israte):
        self.israte = israte
        self._israte_chooser.set_value(self.israte)
        self.set_samp_rate(int(self.israte))
        self.set_variable_static_text_0(self.israte)
        self.wxgui_fftsink2_0.set_sample_rate(self.israte)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_fftrate(int(self.samp_rate/self.fftsize))
        self.set_taps(firdes.low_pass(1.0, self.samp_rate,self.filter_band, 1000))
        self.TPR_0.set_samp_rate(self.samp_rate)
        self.logpwrfft_x_0.set_sample_rate(self.samp_rate)

    def get_prefix(self):
        return self.prefix

    def set_prefix(self, prefix):
        self.prefix = prefix
        self.set_recfile_kelvin(self.prefix+"kelvin" + datetime.now().strftime("%Y.%m.%d.%H.%M.%S") + ".dat")
        self.set_recfile_tpr(self.prefix + datetime.now().strftime("%Y.%m.%d.%H.%M.%S") + ".dat")
        self.blocks_file_sink_1.open(self.prefix+"iq_raw" + datetime.now().strftime("%Y.%m.%d.%H.%M.%S") + ".dat")

    def get_filter_band(self):
        return self.filter_band

    def set_filter_band(self, filter_band):
        self.filter_band = filter_band
        self._filter_band_slider.set_value(self.filter_band)
        self._filter_band_text_box.set_value(self.filter_band)
        self.set_taps(firdes.low_pass(1.0, self.samp_rate,self.filter_band, 1000))

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

    def get_taps(self):
        return self.taps

    def set_taps(self, taps):
        self.taps = taps
        self.fft_filter_xxx_0.set_taps((self.taps))

    def get_spec_data_fifo(self):
        return self.spec_data_fifo

    def set_spec_data_fifo(self, spec_data_fifo):
        self.spec_data_fifo = spec_data_fifo
        self.blocks_file_sink_5.open(self.spec_data_fifo)

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
        self._rec_button_iq_chooser.set_value(self.rec_button_iq)
        self.blks2_valve_2.set_open(bool(self.rec_button_iq))

    def get_integ(self):
        return self.integ

    def set_integ(self, integ):
        self.integ = integ
        self._integ_slider.set_value(self.integ)
        self._integ_text_box.set_value(self.integ)
        self.TPR_0.set_integ(self.integ)

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

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self._freq_text_box.set_value(self.freq)
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
        self.blocks_keep_one_in_n_3.set_n(self.fftrate)
        self.logpwrfft_x_0.set_avg_alpha(1.0/float(self.spavg*self.fftrate))

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

    def get_add_filter(self):
        return self.add_filter

    def set_add_filter(self, add_filter):
        self.add_filter = add_filter
        self._add_filter_chooser.set_value(self.add_filter)
        self.blks2_selector_0.set_input_index(int(self.add_filter))


if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    parser.add_option("", "--clock", dest="clock", type="eng_float", default=eng_notation.num_to_str(100.0e6),
        help="Set Clock rate [default=%default]")
    parser.add_option("", "--dcg", dest="dcg", type="eng_float", default=eng_notation.num_to_str(1),
        help="Set DC (post-detector) gain [default=%default]")
    parser.add_option("", "--decln", dest="decln", type="eng_float", default=eng_notation.num_to_str(-28.0),
        help="Set Declination [default=%default]")
    parser.add_option("", "--devid", dest="devid", type="string", default="addr=192.168.10.2",
        help="Set USRP Device ID [default=%default]")
    parser.add_option("", "--fftsize", dest="fftsize", type="intx", default=8192,
        help="Set fftsize [default=%default]")
    parser.add_option("", "--frequency", dest="frequency", type="eng_float", default=eng_notation.num_to_str(1.406e9),
        help="Set Center Frequency [default=%default]")
    parser.add_option("", "--maxg", dest="maxg", type="intx", default=50,
        help="Set maxg [default=%default]")
    parser.add_option("", "--rfgain", dest="rfgain", type="eng_float", default=eng_notation.num_to_str(0.0),
        help="Set Gain of RF Front-End [default=%default]")
    parser.add_option("", "--rxant", dest="rxant", type="string", default="",
        help="Set RX Antenna selection [default=%default]")
    parser.add_option("", "--spa", dest="spa", type="eng_float", default=eng_notation.num_to_str(1),
        help="Set Spectral Averaging Constant [default=%default]")
    parser.add_option("", "--srate", dest="srate", type="eng_float", default=eng_notation.num_to_str(10.0e6),
        help="Set Sample Rate [default=%default]")
    parser.add_option("", "--subdev", dest="subdev", type="string", default="A:0",
        help="Set USRP Subdevice ID [default=%default]")
    parser.add_option("", "--tpint", dest="tpint", type="eng_float", default=eng_notation.num_to_str(2.0),
        help="Set Integration Time [default=%default]")
    (options, args) = parser.parse_args()
    tb = N200_TPR_filter(clock=options.clock, dcg=options.dcg, decln=options.decln, devid=options.devid, fftsize=options.fftsize, frequency=options.frequency, maxg=options.maxg, rfgain=options.rfgain, rxant=options.rxant, spa=options.spa, srate=options.srate, subdev=options.subdev, tpint=options.tpint)
    tb.Start(True)
    tb.Wait()
