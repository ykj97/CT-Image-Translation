% clear
% close all
% clc

addpath .\Prostate Dx Scans
%% one by one 

file = dicomread('\.\1.2.392.200036.9116.2.6.1.48.1214851791.1664675348.223776\00000.dcm');
info = dicominfo('\.\1.2.392.200036.9116.2.6.1.48.1214851791.1664675348.223776\00000.dcm');
ID = info.PatientID;
ID_new = strrep(ID, ' TGH', '');
info.PatientID = ID_new;

folder_path = '\.\1.2.392.200036.9116.2.6.1.3268.2060189566.1666485951.498258\';
file_list = dir(fullfile(folder_path, '*.dcm'));

output_filename = strrep(info.Filename, 'Prostate Dx Scans', 'Prostate Dx Scans clean MRN'); 

dicomwrite(file, output_filename, info);

%%
folder_path_prefix = '\.\' 
dir_list = dir(fullfile(folder_path_prefix));

% for i = 7:length(dir_list)
for i = 9:length(dir_list)
    path = strcat(dir_list(i).folder,'\',dir_list(i).name,'\');
    fldr_list = dir(fullfile(path));
    
    for itr = 3:length(fldr_list)
        current_path = strcat(path, fldr_list(itr).name,'\');
        save_path = strrep(current_path, 'Prostate Dx Scans', 'Prostate Dx Scans clean MRN');
        
        if ~exist(save_path, 'dir')
            mkdir(save_path)
        end
        
        file_list = dir(fullfile(current_path, '*.dcm'));
        
        for i = 1:length(file_list)
            file_path = fullfile(file_list(i).folder, file_list(i).name);
            file = dicomread(file_path);
            info = dicominfo(file_path);

            id = info.PatientID(1:7);
            info.PatientID = id;

            output_filename = strrep(info.Filename, 'Prostate Dx Scans', 'Prostate Dx Scans clean MRN');
            dicomwrite(file, output_filename, info);
        end

end
    end
  
%% strip STR with iteration

folder_path_prefix = '\.\' 
current_path = '\0281330\1.2.392.200036.9116.2.6.1.48.1214851791.1646477504.409699\';
folder_path = strcat(folder_path_prefix, current_path);

file_list = dir(fullfile(folder_path, '*.dcm'));
save_path = strrep(folder_path, 'Prostate Dx Scans', 'Prostate Dx Scans clean MRN');

if ~exist(save_path, 'dir')
       mkdir(save_path)
    end

for i = 1:length(file_list)
    file_path = fullfile(file_list(i).folder, file_list(i).name);
    file = dicomread(file_path);
    info = dicominfo(file_path);
    
    id = info.PatientID(1:7);
    info.PatientID = id;
    
    output_filename = strrep(info.Filename, 'Prostate Dx Scans', 'Prostate Dx Scans clean MRN');
    dicomwrite(file, output_filename, info);

end



%% check result

info_new = dicominfo('\.\00010.dcm');
info = dicominfo('\.\00000.dcm');


file_new = dicomread('\.\00000.dcm');
file = dicomread('\.\00000.dcm');

figure(1)
imagesc(file)

figure(2)
imagesc(file_new)

