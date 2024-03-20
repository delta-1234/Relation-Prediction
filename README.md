代码部分引用自

[deepakn97/relationPrediction: ACL 2019: Learning Attention-based Embeddings for Relation Prediction in Knowledge Graphs (github.com)](https://github.com/deepakn97/relationPrediction)

[thunlp/OpenKE: An Open-Source Package for Knowledge Embedding (KE) (github.com)](https://github.com/thunlp/OpenKE)

## 一、准备环境

本人使用的Ubuntu版本为22.04

### 1.下载安装Miniconda

- [conda](https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh)

```bash
bash Miniconda3-latest-Linux-x86_64.sh
```

### 2.创建新环境并配置环境

- [torch](https://download.pytorch.org/whl/cu90/torch-1.0.0-cp35-cp35m-linux_x86_64.whl)

```bash
conda env create -f mypytorch.yml
conda activate mypytorch
bash prepare.sh
```

### 3. 如果已经配置好

```bash
source ~/miniconda3/bin/activate
conda activate mypytorch
```



## 二、生成数据集

```bash
cd ./data/2021
python main.py
cd ..
cd ..
```



## 三、开始训练

### 1.实体嵌入

```bash
cd openke/
bash make.sh
cd ..
python test.py
```

### 2.关系推理

**参数:**

`--data`: Specify the folder name of the dataset.

`--epochs_gat`: Number of epochs for gat training.

`--epochs_conv`: Number of epochs for convolution training.

`--lr`: Initial learning rate.

`--weight_decay_gat`: L2 reglarization for gat.

`--weight_decay_conv`: L2 reglarization for conv.

`--get_2hop`: Get a pickle object of 2 hop neighbors.

`--use_2hop`: Use 2 hop neighbors for training.  

`--partial_2hop`: Use only 1 2-hop neighbor per node for training.

`--output_folder`: Path of output folder for saving models.

`--batch_size_gat`: Batch size for gat model.

`--valid_invalid_ratio_gat`: Ratio of valid to invalid triples for GAT training.

`--drop_gat`: Dropout probability for attention layer.

`--alpha`: LeakyRelu alphas for attention layer.

`--nhead_GAT`: Number of heads for multihead attention.

`--margin`: Margin used in hinge loss.

`--batch_size_conv`: Batch size for convolution model.

`--alpha_conv`: LeakyRelu alphas for conv layer.

`--valid_invalid_ratio_conv`: Ratio of valid to invalid triples for conv training.

`--out_channels`: Number of output channels in conv layer.

`--drop_conv`: Dropout probability for conv layer.

```bash
tail -n +2 ./data/2021/entity2id.txt > temp
cat temp > ./data/2021/entity2id.txt
tail -n +2 ./data/2021/relation2id.txt > temp
cat temp > ./data/2021/relation2id.txt
rm -f temp
python3 main.py --data ./data/2021/ --epochs_gat 800 --epochs_conv 50 --weight_decay_gat 0.00001 --get_2hop True --partial_2hop FALSE --batch_size_gat 100 --margin 1 --out_channels 50 --drop_conv 0.05 --weight_decay_conv 0.000001 --output_folder ./checkpoints/2021/out/
```



## 四、知识图谱展示

安装neo4j-community-5.16.0，运行neo4j console，即可看到http://localhost:7474/browser/ 看到前端界面，运行node.py脚本，将知识图谱插入neo4j数据库，实现知识图谱的展示



