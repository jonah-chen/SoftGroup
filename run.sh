#!/bin/bash

# Note you are running on two GPUs with 32 CPU cores.

mkdir dataset/s3dis/Stanford3dDataset_v1.2
mkdir dataset/s3dis/Stanford3dDataset_v1.2/Area_5

COUNTER=0
for fp in custom/input/*.ply
do
    let COUNTER=COUNTER+1
    fn=$(basename ${fp##*/} .ply)
    echo $COUNTER $fn
    mkdir dataset/s3dis/Stanford3dDataset_v1.2/Area_5/office_${COUNTER}
    python tools/ply_to_txt.py $fp dataset/s3dis/Stanford3dDataset_v1.2/Area_5/office_${COUNTER}/office_${COUNTER}.txt
done

mkdir dataset/s3dis/Stanford3dDataset_v1.2/Area_6
mkdir dataset/s3dis/Stanford3dDataset_v1.2/Area_1
mkdir dataset/s3dis/Stanford3dDataset_v1.2/Area_2
mkdir dataset/s3dis/Stanford3dDataset_v1.2/Area_3
mkdir dataset/s3dis/Stanford3dDataset_v1.2/Area_4

cd dataset/s3dis
bash prepare_data.sh
cd ../..

mkdir custom/intermediate
mkdir custom/intermediate/results
./tools/dist_test.sh ./configs/s3dis_like_eval.yaml ./custom/input/model.pth 2 --out custom/intermediate/results

while [ $COUNTER -gt 0 ]
do
    python tools/visualization.py --dataset s3dis --prediction_path custom/intermediate/results --data_split Area_5 --room_name Area_5_office_${COUNTER} --task instance_pred --out custom/output/${COUNTER}.ply

    let COUNTER=COUNTER-1
done
