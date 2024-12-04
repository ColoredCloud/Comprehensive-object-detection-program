import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
import torchvision.transforms as transforms
import os
from ImageOperation import tar2ImageWithAttributes
from torch.utils.data import Dataset, DataLoader

Image_size = 1366,1366

class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=16, kernel_size=5, stride=2, padding=0)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(in_channels=16, out_channels=4, kernel_size=4, stride=1, padding=0)
        self.fc1 = nn.Linear(4*85*85, 85*4)
        self.fc3 = nn.Linear(85*4,80)
        self.fc4 = nn.Linear(80,4)
    def forward(self, x):
        batch_size = x.size()[0]
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        #print(x.size())
        x = x.view(batch_size,-1)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc3(x))
        x = self.fc4(x)
        return x

def packBatch(imgs,lables,transform=None):

    class CustomDataset(Dataset):
        def __init__(self):
            nonlocal imgs, lables
            self.images = imgs
            self.lables = lables

        def __len__(self):
            return len(self.images)

        def __getitem__(self, idx):

            return self.images[idx], self.lables[idx]
    return CustomDataset()



def load_data(batch_size, path):
    images = []
    labels = []
    root, _, files = next(os.walk(path))

    transform = transforms.Compose([
        transforms.ToTensor()])

    for file in files:
        img, lb = tar2ImageWithAttributes(root + file)

        img = img.convert('RGB')
        img = transform(img)
        lb = torch.tensor(list(lb.values()))

        images.append(img)
        labels.append(lb)

    dataset = packBatch(images, labels, transform=transform)

    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
    return dataloader

def loss(target_pos, predict_pos):
    return torch.mean(torch.pow(torch.abs(target_pos - predict_pos), 2))