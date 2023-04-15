# AICITY2023_Track5_DVHRM
The solutions ranked fourth, fifth, and sixth in Track 5 (Detecting Violations of Helmet Rules for Motorcyclists) of the NVIDIA AI City Challenge at the CVPR 2023 Workshop.

# Solution pipeline
1. Download the training_videos from [track5 of AI CIty Challenge](http://www.aicitychallenge.org/2023-track5-download/)
2. Extracts images from Track 5 training_videos: 
- bash ./run_extract_train_frames.sh
3. Convert gt.txt to yolo txt: 
- python GTxywh2yolo.py
4. Uses [YOLOv7-E6E](https://github.com/WongKinYiu/yolov7) to train the seven classes Helmet detector with 100 training videos and 100 validation videos: 
- python -m torch.distributed.launch --nproc_per_node 4 --master_port 9527 train_aux.py --workers 8 --device 0,1,2,3 --sync-bn --batch-size 8 --data Helmet/Helmet.yaml --img 1920 1920 --cfg cfg/training/yolov7-e6e-Helmet.yaml --weights '' --name yolov7-e6e-Helmet --hyp data/hyp.scratch.p6.yaml --epochs 350
5. Uses YOLOv7-[CBAM](https://openaccess.thecvf.com/content_ECCV_2018/papers/Sanghyun_Woo_Convolutional_Block_Attention_ECCV_2018_paper.pdf) to train the seven classes Helmet detector with 100 training videos and 50 validation videos: 
- python -m torch.distributed.launch --nproc_per_node 4 --master_port 9527 train_aux.py --workers 8 --device 0,1,2,3 --sync-bn --batch-size 12 --data Helmet/Helmet.yaml --img 1280 1280 --cfg cfg/training/yolov7-e6e-CBAM-Helmet.yaml --weights '' --name yolov7-e6e-CBAM-Helmet1280-10050 --hyp data/hyp.scratch.p6.yaml --epochs 300
6. Uses YOLOv7-[SimAM](https://proceedings.mlr.press/v139/yang21o.html) to train the seven classes Helmet detector with 75 training videos and 25 validation videos: 
- python -m torch.distributed.launch --nproc_per_node 4 --master_port 9527 train_aux.py --workers 8 --device 0,1,2,3 --sync-bn --batch-size 12 --data Helmet/Helmet.yaml --img 1280 1280 --cfg cfg/training/yolov7-e6e-siam-Helmet.yaml --weights best.pt --name yolov7-e6e-siam-Helmet1280-7525 --hyp data/hyp.scratch.p6.yaml --epochs 300
- Break at epoch 174 
7. Uses YOLOv7-[SimAM](https://proceedings.mlr.press/v139/yang21o.html) to fine-tune the seven classes Helmet detector with 100 training videos and 50 validation videos:
- &nbsp;python -m torch.distributed.launch --nproc_per_node 4 --master_port 9527 train_aux.py --workers 8 --device 0,1,2,3 --sync-bn --batch-size 12 --data Helmet/Helmet.yaml --img 1280 1280 --cfg cfg/training/yolov7-e6e-siam-Helmet.yaml --weights best.pt --name yolov7-e6e-siam-Helmet1280-10050 --hyp data/hyp.scratch.p6.yaml --epochs 300
8. Download the testing_videos from [track5 of AI CIty Challenge](http://www.aicitychallenge.org/2023-track5-download/)
9. Extracts images from Track 5 testing_videos: 
- bash ./run_extract_test_frames.sh
10. Rank 6: Test YOLOv7-E6E seven classes Helmet detector
- Download [YOLOv7-E6E seven classes Helmet detector model](https://drive.google.com/file/d/1rdo1H11KvoSBVlawouDmZiYYLEQZjeAh/view?usp=share_link) and reanme it to best.pt
- python detect_Helmet.py --source ../test --weights best.pt --conf 0.93 --iou-thres 0.45 --img-size 1920 --device 1 result_file_name y7e6eHelmet1920_93_45.txt
11. Rank 5: Test YOLOv7-CBAM seven classes Helmet detector
- Download [YOLOv7-CBAM seven classes Helmet detector model](https://drive.google.com/file/d/1KGx9E-hEDjgImkxih-W-YJHIQezyuRD7/view?usp=share_link) and rename it to best.pt
- python detect_Helmet.py --source ../test --weights best.pt --conf 0.93185 --iou-thres 0.35 --img-size 1280 --device 0 result_file_name y7e6eCBAMHelmet1280_93185_35.txt
12. Rank 4: Test YOLOv7-SimAM seven classes Helmet detector
- Download [YOLOv7-SimAM seven classes Helmet detector model](https://drive.google.com/file/d/1gmnUySGZsz438I-y1KBYS8KQsw33jLuL/view?usp=share_link) and rename it to best.pt
- pthon detect_Helmet.py --source ../test_images --weights best.pt --conf 0.92 --iou-thres 0.35 --img-size 1280 --device 3 result_file_name y7e6esiamHelmet1280_92_35.txt
# Environment
Please refer to [YOLOv7](https://github.com/WongKinYiu/yolov7) Installation
