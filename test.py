import openke
from openke.config import Trainer, Tester
from openke.module.model import TransE, TransR, TransH
from openke.module.loss import MarginLoss
from openke.module.strategy import NegativeSampling
from openke.data import TrainDataLoader, TestDataLoader

# dataloader for training
train_dataloader = TrainDataLoader(
    in_path="./data/2021/",
    nbatches=16,
    threads=8,
    sampling_mode="normal",
    bern_flag=1,
    filter_flag=1,
    neg_ent=10,
    neg_rel=0
)

# dataloader for test
test_dataloader = TestDataLoader("./data/2021/", "link")

# define the model
transe = TransE(
    ent_tot=train_dataloader.get_ent_tot(),
    rel_tot=train_dataloader.get_rel_tot(),
    dim=100,
    p_norm=1,
    norm_flag=True)

# define the loss function
model = NegativeSampling(
    model=transe,
    loss=MarginLoss(margin=5.0),
    batch_size=train_dataloader.get_batch_size()
)

# train the model
trainer = Trainer(model=model, data_loader=train_dataloader, train_times=500, alpha=0.5, use_gpu=True)
trainer.run()
transe.save_checkpoint('./checkpoints/transe.ckpt')
embeddings = transe.get_parameters()
with open('./data/2021/entity2vec.txt', 'w') as o1:
    with open('./data/2021/relation2vec.txt', 'w') as o2:
        for i in embeddings['ent_embeddings.weight']:
            for j in i:
                print('%.6f' % j, file=o1, end=' ')
            print(file=o1)
        for i in embeddings['rel_embeddings.weight']:
            for j in i:
                print('%.6f' % j, file=o2, end=' ')
            print(file=o2)

# test the model
transe.load_checkpoint('./checkpoints/transe.ckpt')
tester = Tester(model=transe, data_loader=test_dataloader, use_gpu=True)
tester.run_link_prediction(type_constrain=False)
