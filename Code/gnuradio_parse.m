%Radiometer Parsing script
%Matthew E. Nelson
%Updated 3/10/2013

%This script uses the read_float_binary.m file to read in a file written by
%GNURadio.  It will also read in the square law data and parse it as well
%It should work on both Matlab and Octave (you will need the IO package for octave)

%Clear the workspace
clear all;

%Calibration variables based on two temperature points
%Enter the temperatures in Kelvin
temp1 = 293;
temp2 = 77;

%Enter the measured data points for temp1 and temp2
data1 = .156;
data2 = .1057;

%Store the values into a and b
syms a b;

%Solve our two calibration points
y = solve(data1*a+b==temp1,data2*a+b==temp2);

calibration = [y.a y.b]

%calib1 = [y.a];
%calib2 = [y.b];

%Ask for the filename
gnuradio_file = uigetfile('*.*','Select the GNURadio data file');
disp('Importing Radiometer data...')
%square_law = uigetfile('*.*','Select the Square_law data file');
%disp('Importing Square Law data...')
%Call the read_float_binary script5
gnuradio = read_float_binary(gnuradio_file);
%Plot the data
% Create figure
%subplot(2,1,1);
calib_data = ((gnuradio*calibration(1))+calibration(2));
%conv_temp = convtemp(calib_data,'C','K');
%hist(conv_temp);
plot(calib_data);
%figure;
%plot(conv_temp);
title('N200 Data');
%hold all;

% Create axes
%axes1 = axes('Parent',figure1,'YScale','log','YMinorTick','on','XGrid','on',...
%    'Position',[0.13 0.0413625304136253 0.775 0.883637469586375]);
%box(axes1,'on');
%hold(axes1,'all');

% Create semilogy
%semilogy(Y);

% Create xlabel
xlabel('Time');

% Create ylabel
ylabel('Calibrated Noise Temperature in K');

% Create title
%title('Power data from N200');
%Now parse the Square law file which is comma delimited.
%First, it helps to open the file
%fid = fopen(square_law);
%C = textscan(fid,'%s %s %s %s %s %s','delimiter',',');
%[Date,VRAW,VdB,HRAW,HdB,HASH]=deal(C{:});

%We need to convert the cell to an array
%v_pol = str2double(VRAW);
%v_scale = v_pol(1:4.4:length(v_pol));
%subplot(2,1,2);
figure;
plot(gnuradio);
%plot(v_scale,'r')
%title('Square Law Data');