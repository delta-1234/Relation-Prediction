#!/bin/bash
touch temp
tail -n +2 ./data/2021/entity2id.txt > temp
cat temp > ./data/2021/entity2id.txt
tail -n +2 ./data/2021/relation2id.txt > temp
cat temp > ./data/2021/relation2id.txt
rm -rf temp
python3 main.py --data ./data/2021/ --epochs_gat 100 --epochs_conv 20 --weight_decay_gat 0.00001 --get_2hop True --partial_2hop True --batch_size_gat 272 --margin 1 --out_channels 50 --drop_conv 0.3 --weight_decay_conv 0.000001 --output_folder ./checkpoints/2021/out/