#!/usr/bin/env bash
echo "Start to process AICity2023 task5 test videos:"
starttime=`date +%s`
echo "---------------------------------------------------"
#get all videos names
ROOT_PATH=$(pwd)
video_list_txt=$ROOT_PATH"/list_test_video_id.txt"
echo $video_list_txt
#get video list
videos_list=()
while read -r line || [[ -n "$line" ]]; do
    stringarray=($line)
    videoname=${stringarray[1]%%.*}
    videos_list+=(${videoname})
done < ${video_list_txt}

#extract all frames
bash extract_test_frames.sh "${videos_list[@]}"
