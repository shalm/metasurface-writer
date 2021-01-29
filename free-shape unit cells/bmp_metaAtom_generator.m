%% GENERATOR OF BMP META-ATOM PATTERNS

%% by M. Y. SHALAGINOV AUGUST 2020

%% CLEAN IT UP
clc;clear all; close all;
%%

%% UNITS AND CONSTANTS 

%%

%% DATA IMPORT FROM MAT FILE
userpath('C:\Users\Misha Shalaginov\Desktop\Python codes\metasurface\free-shape unit cells');
data = load('4sym_32x32.mat').pattern_4sym;
selected_cells = [92320,63941,84580,52072]; %cell # of selected meta-atoms

%%

%% DATA PROCESSING

%%

%% DATA EXPORT

for i = 1:length(selected_cells)
    filename = ['meta-atom', num2str(i),'.bmp'];
    imwrite(data(:,:,selected_cells(i)),filename);
end
