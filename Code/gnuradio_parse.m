%Radiometer Parsing script
%Matthew E. Nelson
%Updated 5/25/2014
%Rev. 2.1
%--------------------------------------------------------------------------
%Revision History
%1.7 - Added CSV input file format.  Gave up on reading LVM
%1.8 - Added User input box
%1.9 - Added Calibration points for square law detector
%1.91 - Cleaned up some code
%1.92 - Futher clean up of unused code
%1.93 - Fixed dialog boxes not showing the entire title
%2.0 - Added filter to clean up noisy x^2 data
%2.1 - Added NEdeltaT (NEAT) calculation, minor change to plot labels
%2.11 - Added square law voltage to dBm conversion

%This script uses the read_float_binary.m file to read in a file written by
%GNURadio.  This data can then be manipulated by Matlab and graphed.  This
%script can also accept calibration coefficients in order to calculate the
%calibrated noise temperature.  This requires that two data points are
%recorded to known sources such as LN2.

%Data files using the GNURadio flow diagram written by Matthew Nelson use a
%valve block to turn "on and off" recording.  However, data is still
%written to the file, but they will be all zeros.  This script has a simple
%routine to remove all zeros.  If this is not desired (for example turning
%on and off the recording) please comment it out.

%In April I switched from a UBW32 board to a NI USB DAQ to obtain the
%square law data.  This changed the output file from a csv file to NI's
%TDMS binary format.  The original CSV code will remain but will be
%commented out.

%In theory, this script may also run on Octave, but the file I/O package
%will be needed to use the file dialog box.
%--------------------------------------------------------------------------
%Clear the workspace
clear all;
%------------------------------------------------------------------------
%Constants
%set's the window size to filter the square-law data
windowSize = 200;
%Receiver Noise Temperature
Trec = 370;
%Integration Time
tau = 2;
%Bandwidth
beta = 10e6;
%------------------------------------------------------------------------
%User Dialog entry
%The User input box will accecpt the calibration points from the user and
%will output the calibration data.

%Setup dialog options
options.Resize='on';
options.WindowStyle='normal';
options.Interpreter='tex';
%Setup MsgBox options
CreateStruct.Interpreter = 'tex';
CreateStruct.WindowStyle = 'modal';
%-------------------------------------------------------------------------

%Ask for user input for calibration
prompt = {'                        Enter calibration temp 1 (K)','Enter calibration temp 2 (K)','Enter Calibration value 1:','Enter Clibration value 2:'};
dlg_title = 'Calibration for N200';
num_lines = 1;
def = {'371','77','.170','.103'};
N200answer = inputdlg(prompt,dlg_title,num_lines,def,options);


prompt = {'                        Enter calibration temp 1 (K):','Enter calibration temp 2 (K):','Enter Calibration value 1:','Enter Clibration value 2:'};
dlg_title = 'Calibration for X^2';
num_lines = 1;
def = {'371','77','2.1','1.9'};
x2answer = inputdlg(prompt,dlg_title,num_lines,def,options);

%Calibration variables based on two temperature points

N200temp1 = N200answer(1);
N200temp2 = N200answer(2);

%Enter the measured data points for temp1 and temp2
N200data1 = N200answer(3);
N200data2 = N200answer(4);

%Calibration variables based on two temperature points

x2temp1 = x2answer(1);
x2temp2 = x2answer(2);

%Enter the measured data points for temp1 and temp2
x2data1 = x2answer(3);
x2data2 = x2answer(4);

%Store the values into a and b
syms a b;

%Solve our two calibration points for the SDR
y = solve(N200data1*a+b==N200temp1,N200data2*a+b==N200temp2);

N200calib1 = double(y.a);
N200calib2 = double(y.b);

msgbox(sprintf('The calibrations points for the N200 is: %f and %f',N200calib1,N200calib2));

N200calibration = [y.a y.b];
fprintf('N200 Coefficient 1: %.2f N200 Coefficent 2: %.2f \r\n',N200calib1, N200calib2);

%Store the values into a and b
syms a b;

%Solve our two calibration points for the X^2
y = solve(x2data1*a+b==x2temp1,x2data2*a+b==x2temp2);

x2calib1 = double(y.a);
x2calib2 = double(y.b);

msgbox(sprintf('The calibrations points for the X^2 is: %f and %f',x2calib1,x2calib2),CreateStruct);

x2calibration = [y.a y.b];
fprintf('X^2 Coefficient 1: %.2f X^2 Coefficent 2: %.2f \r\n',x2calib1, x2calib2);

%Calculate N E Delta T (NEAT)
%First calculatation is the NEAT expected based on BW and other parameters
%NEAT = (Ta+Tsys)/SQRT(tau+beta)

NEAT = (Trec)./sqrt(tau+beta);

%Now we can calculate the actual NEAT
estNEAT = std(gnuradio);

%Now print this information out
msgbox(sprintf('The calculated NE \Delta T is: %f and the actual NE \Delta T is: ',NEAT,estNEAT),CreateStruct);

%---------------------------------------------------------------------------
%Read data files.  
%GNURadio outputs a binary file and LabView outputs a TDMS file


%Ask for the filename that has the TPR data from GNURadio
gnuradio_file = uigetfile('*.*','Select the GNURadio data file');
disp('Importing Radiometer data...')

%Ask for the filename of the Square law detector.  Comment out if not using
square_law = uigetfile('*.tdms','Select the Square_law data file');
disp('Importing Square Law data...')

%Call the program that will convert the TDMS file format to a .mat file

tdms = convertTDMS2(true,square_law);

%The data created is nested in the array, we need to pull the data we want
x2=tdms.Data.MeasuredData(1,4).Data;

%Call the read_float_binary script.  This scripts reads the GNURadio
%binary protocol
gnuradio = read_float_binary(gnuradio_file);

%--------------------------------------------------------------------
%Remove zeros which is common in files that use the valve feature to
%control flow
gnuradio = gnuradio(gnuradio~=0);
%Create a time index
time=(1:length(gnuradio))./1e3;

%Convert voltage from square-law to dBm.  53 mV is 1 dBm
dbmx2=x2./.053;
%-------------------------------------------------------------------
%Calculate the calibrated noise temperature for the SDR
N200calib_data = ((gnuradio*N200calibration(1))+N200calibration(2));

%Calculate the calibrated noise temperature for the X^2
x2calib_data = ((x2*x2calibration(1))+x2calibration(2));

%-------------------------------------------------------------------
%The square-law data is fairly noise, so we will filter it to smooth
%it out.  
%First, convert from a sym matrix to a double
temp1=double(x2calib_data);
temp2=double(x2);
%Now filter it
avgx2_calib=filter(ones(1,windowSize)/windowSize,1,temp1);
avgx2=filter(ones(1,windowSize)/windowSize,1,temp2);
%-------------------------------------------------------------------
%Calculate N E Delta T (NEAT)
%First calculatation is the NEAT expected based on BW and other parameters

%NEAT = (Ta+Tsys)/SQRT(tau+beta)

NEAT = (Trec)./sqrt(tau+beta);

%Now we can calculate the actual NEAT
expNEAT = std(gnuradio);
%-------------------------------------------------------------------

%Plot the calibrated data
figure;
subplot(2,1,1);
plot(N200calib_data);
title('N200 TPR Calibrated Data');

% Create xlabel
xlabel('Time');

% Create ylabel
ylabel('Calibrated Noise Temperature in K');
subplot(2,1,2);
plot(avgx2_calib);
title('x^2 Calibrated Data');

%Plot the raw data
figure;
subplot(2,1,1);
plot(gnuradio);
title('N200 TPR Raw Data');
xlabel('Time');
ylabel('rQ Value');
subplot(2,1,2);
plot(avgx2);
title('x^2 Raw Data');
ylabel('Raw Voltage');
axis([-inf inf 2.1 2.4]);