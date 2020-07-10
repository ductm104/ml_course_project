import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from torchvision.datasets import DatasetFolder

from model import Model


index2label = {0: "black", 1: "draw", 2: "white"}
device = "cuda:0"


def sample_loader(path):
    sample = np.load(path)
    sample = sample.flatten()
    sample = torch.from_numpy(sample).float()
    return sample

def get_data_loader(data_root):
    train_dataset = DatasetFolder(
        root=data_root, 
        loader=sample_loader, 
        extensions="npy"
    )
    train_loader = DataLoader(
        train_dataset, batch_size=16, 
        shuffle=True, num_workers=32
    )
    return train_dataset, train_loader

def accuracy(preds, labels):
    preds = torch.argmax(preds, dim=1)
    corrects = torch.sum(preds == labels)
    total = preds.numel()
    return corrects.float(), float(total)


if __name__ == "__main__":
    train_dataset, train_loader = get_data_loader("/data.local/giangh/ml_course_project/reinforcement_learning/data/train_moves")
    val_dataset, val_loader = get_data_loader("/data.local/giangh/ml_course_project/reinforcement_learning/data/val_moves")
    
    model = Model().to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=3e-4)
    celoss = nn.CrossEntropyLoss()
    
    n_epochs = 100
    global_step = 0
    best_val_acc = 0.0
    for epoch in range(n_epochs):
        train_corrects, train_totals = 0.0, 0.0
        for moves, labels in train_loader:
            moves, labels = moves.to(device), labels.to(device)
            preds = model(moves)
            loss = celoss(preds, labels)
            correct, total = accuracy(preds, labels)
            train_corrects += correct
            train_totals += total

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            global_step += 1

            if global_step%50==0:
                best_model = False
                val_corrects, val_totals = 0.0, 0.0
                for moves, labels in val_loader:
                    moves, labels = moves.to(device), labels.to(device)
                    with torch.no_grad():
                        preds = model(moves)
                        correct, total = accuracy(preds, labels)
                        val_corrects += correct.item()
                        val_totals += total
                if val_corrects / val_totals > best_val_acc:
                    best_model = True
                    best_val_acc = val_corrects / val_totals
                    torch.save(model.state_dict(), f"ckpt/{best_val_acc:.4f}.pth")
                print(f"Train acc: {(train_corrects / train_totals):.4f} - val acc: {(val_corrects / val_totals):.4f}")
                if best_model:
                    print("### BEST MODEL!!!")