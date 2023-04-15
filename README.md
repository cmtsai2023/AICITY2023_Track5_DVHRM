# AICITY2023_Track5_DVHRM
The solutions ranked fourth, fifth, and sixth in Track 5 (Detecting Violations of Helmet Rules for Motorcyclists) of the NVIDIA AI City Challenge at the CVPR 2023 Workshop.
Our code will be open sourced soon
# Solution pipeline
1. Download the training_videos from [track5 of AI CIty Challenge](http://www.aicitychallenge.org/2023-track5-download/)
2. Extract images from Track 5 training_videos by using: bash ./run_extract_train_frames.sh
3. Convert gt.txt to yolo txt by using: python GTxywh2yolo.py
4. Uses [YOLOv7-E6E](https://github.com/WongKinYiu/yolov7) to train the seven classes Helmet detector: python -m torch.distributed.launch --nproc_per_node 4 --master_port 9527 train_aux.py --workers 8 --device 0,1,2,3 --sync-bn --batch-size 8 --data Helmet/Helmet.yaml --img 1920 1920 --cfg cfg/training/yolov7-e6e-Helmet.yaml --weights '' --name yolov7-e6e-Helmet --hyp data/hyp.scratch.p6.yaml --epochs 350
5. Uses YOLOv7-[CBAM](https://openaccess.thecvf.com/content_ECCV_2018/papers/Sanghyun_Woo_Convolutional_Block_Attention_ECCV_2018_paper.pdf) to train and the seven classes Helmet detector
6. Uses YOLOv7-[SimAM](https://proceedings.mlr.press/v139/yang21o.html) to train the seven classes Helmet detector
7. Download the testing_videos from [track5 of AI CIty Challenge](http://www.aicitychallenge.org/2023-track5-download/)
8. Extract images from Track 5 testing_videos by using: bash ./run_extract_test_frames.sh
9. Test YOLOv7-E6E seven classes Helmet detector
10. Test YOLOv7-CBAM seven classes Helmet detector
11. Test YOLOv7-SimAM seven classes Helmet detector
# Environment
Please refer to [YOLOv7](https://github.com/WongKinYiu/yolov7) and [PRBNet_PyTorch](https://github.com/pingyang1117/PRBNet_PyTorch) Installation
