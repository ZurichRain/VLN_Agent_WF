# 使用样例
# bash get_one_scan_path_360images.sh 2azQ1b91cZZ 6822_2 1320ad480d434d1d8d6d7304dc5f7854 pred

echo $1
scanInfo_FILE=./data/v1/scans/"$1"
files=$(ls $scanInfo_FILE/matterport_skybox_images/*_skybox_small.jpg 2> /dev/null | wc -l)

echo $files
if [[ "$files" == "0" ]]; then
    # deal dowsize imgs
    python3 dowsize_skybox.py $1
fi

# if [[ ! -d "$scanInfo_FILE" ]]; then
#     python3 dowsize_skybox.py x8F5xyUWy9e
# fi



# # deal dowsize imgs
# python3 dowsize_skybox.py x8F5xyUWy9e

# get viewpoint of a scan 
python3 get_img.py $1 $2 $3 $4