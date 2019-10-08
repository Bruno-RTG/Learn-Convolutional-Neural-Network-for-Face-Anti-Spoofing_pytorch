"""
Created on 19.10.8 20:47
@File:train.py
@author: coderwangson
"""
"#codeing=utf-8"
import os
import torch
from torch import nn
from torch.nn import functional as F
from torch.utils import data
from Data import Data
from Nets import Net

os.environ['CUDA_VISIBLE_DEVICES']='1'
# Detect devices
use_cuda = torch.cuda.is_available()
device = torch.device("cuda" if use_cuda else "cpu")   # use CPU or GPU
learning_rate = 0.01

params = {'batch_size': 30, 'shuffle': True, 'num_workers': 8,
              'pin_memory': True} if use_cuda else {}
if use_cuda:
    net = Net(2).to(device)
if torch.cuda.device_count() > 1:# if train using DataParallel,test must using DataParallel
    print("Using", torch.cuda.device_count(), "GPUs!")
    model = nn.DataParallel(net)

train_data_set = Data("/home/userwyh/code/dataset/CASIA_scale/scale_1.0/",True)
test_data_set = Data("/home/userwyh/code/dataset/CASIA_scale/scale_1.0/",False)
train_data_loader = data.DataLoader(train_data_set, **params)
# test_data_loader = data.DataLoader(test_data_set, **params)

optimizer = torch.optim.SGD(list(net.parameters()), lr=learning_rate)

def train(net,dataloader,optimizer,epoch):
    net.train()
    for e in range(epoch):
        for batch_idx, (X, y) in enumerate(dataloader):

            X, y = X.to(device), y.to(device).view(-1, )
            optimizer.zero_grad()
            output = net(X)
            loss = F.cross_entropy(output, y)

            loss.backward()

            optimizer.step()
        if e%5==0:
            print("the loss is",loss.item())
            # val(net,test_data_loader,batch_idx)

def val(net,dataloader,batch):
    net.eval()
    for batch_idx, (X, y) in enumerate(dataloader):

        X, y = X.to(device), y.to(device).view(-1, )
        optimizer.zero_grad()
        output = net(X)
    print("epoch %d ,"%(batch))

if __name__ == '__main__':

    train(net,train_data_loader,optimizer,50)