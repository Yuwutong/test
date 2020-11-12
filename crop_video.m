%% crop video to single diamond
clc;
close all;
clear;

src_dir = 'D:\data\291-350_C802\';
save_dir = src_dir;
video_filename = '10375722802(G)-R1-Darkfield-02.mp4';
file_id = video_filename(1:11);
vv = VideoWriter(strcat(save_dir,file_id,'_test'),'MPEG-4');
open(vv);
disp(video_filename)
v = VideoReader(strcat(src_dir,video_filename));
cnt = 400;
while cnt>0
    frame = read(v,cnt);
    cnt_str = sprintf('%03d',cnt);
    fprintf([cnt_str,'/400...'])
    frame_crop = frame(:,1:1440,:);
%     if cnt==1
%         frame_name = strcat(save_dir, file_id, '_',cnt_str,'.png');
%         imwrite(frame(:,1:1200,:), frame_name);
%     end
    writeVideo(vv,frame_crop);
    cnt = cnt - 1; 
    fprintf('\b\b\b\b\b\b\b\b\b\b')
end
close(vv)