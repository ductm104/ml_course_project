import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


class Model(nn.Module):
    def __init__(self, in_channels=512, n_class=3, hidden_channels=[256]):
        super().__init__()
        self.features = nn.Sequential(
            nn.Linear(in_channels, hidden_channels[0]),
            nn.BatchNorm1d(hidden_channels[0]),
            nn.ReLU(),
        )
        self.classifier = nn.Linear(hidden_channels[0], n_class)
    
    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x


if __name__ == "__main__":
    model = Model()
    model.eval()
    
    x = np.load("/data.local/giangh/ml_course_project/reinforcement_learning/data/moves/black/0.npy")
    x = x.reshape(1, -1)
    x = torch.from_numpy(x).float()
    y = model(x)
    print(y.shape)