%Radiometer Parsing script
%Matthew E. Nelson
%Updated 5/12/2014
%Rev. 1.8

%Revision History
%1.7 - Added CSV input file format.  Gave up on reading LVM
%1.8 - Added User input box

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

%Clear the workspace
clear all;

%User Dialog entry
%The User input box will accecpt the calibration points from the user and
%will output the calibration data.

prompt = {'Enter calibration temp 1 (K):','Enter calibration temp 2 (K):','Enter Calibration value 1:','Enter Clibration value 2:'};
dlg_title = 'Calibration Input';
num_lines = 1;
def = {'371','77','.170','.103'};
answer = inputdlg(prompt,dlg_title,num_lines,def);

%Calibration variables based on two temperature points
%Enter the temperatures in Kelvin
temp1 = answer(1);
temp2 = answer(2);

%Enter the measured data points for temp1 and temp2
data1 = answer(3);
data2 = answer(4);

%Store the values into a and b
syms a b;

%Solve our two calibration points
y = solve(data1*a+b==temp1,data2*a+b==temp2);

calib1 = double(y.a);
calib2 = double(y.b);

h = msgbox(sprintf('The calibrations points are: %f and %f',calib1,calib2));

calibration = [y.a y.b];
fprintf('Coefficient 1: %.2f Coefficent 2: %.2f \r\n',calib1, calib2);

%Ask for the filename that has the TPR data from GNURadio
gnuradio_file = uigetfile('*.*','Select the GNURadio data file');
disp('Importing Radiometer data...')

%Ask for the filename of the Square law detector.  Comment out if not using
square_law = uigetfile('*.lvm','Select the Square_law data file');
disp('Importing Square Law data...')

x2=csvread(square_law);


%Call the read_float_binary script
gnuradio = read_float_binary(gnuradio_file);


%Remove zeros which is common in files that use the valve feature to
%control flow
gnuradio = gnuradio(gnuradio~=0);

%Calculate the calibrated noise temperature
calib_data = ((gnuradio*calibration(1))+calibration(2));


%Plot the calibrated data
plot(calib_data);

title('N200 TPR Calibrated Data');

% Create xlabel
xlabel('Time');

% Create ylabel
ylabel('Calibrated Noise Temperature in K');

%Plot the raw data
figure;
subplot(2,1,1);
plot(gnuradio);
title('N200 TPR Raw Data');
xlabel('Time');
ylabel('Raw Noise Power Data');
subplot(2,1,2);
plot(x2);

% Create title
%title('Power data from N200');

%Parse the NI TDMS file

%-------------------------------------------------------
%Now parse the Square law file which is comma delimited.
%Comment out if not parsing square law file

%First, it helps to open the file
%fid = fopen(square_law);
%C = textscan(fid,'%s %s %s %s %s %s','delimiter',',');
%[Date,VRAW,VdB,HRAW,HdB,HASH]=deal(C{:});

%We need to convert the cell to an array
%v_pol = str2double(VRAW);
%v_scale = v_pol(1:4.4:length(v_pol));

%Now graph
%subplot(2,1,2);
%plot(v_scale,'r')
%title('Square Law Data');