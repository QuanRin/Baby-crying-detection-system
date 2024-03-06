import torchaudio
import torch
from tqdm import tqdm
from dataset import CryDataset
from torch.utils.data import DataLoader
from model import CNNNetwork, AlexNet
from torch import nn
import csv


from audio_utils import CLASS_MAPPING, NUM_CLASSES, BATCH_SIZE, EPOCHS, LEARNING_RATE, N_MELS, SAMPLE_RATE, NFFT, HOP_LEN, WIN_LEN


def create_data_loader(train_data, batch_size):
    train_dataloader = DataLoader(train_data, batch_size=batch_size)
    return train_dataloader


def step(model, data_loader, loss_fn, optimiser, device, is_train=True):
    if is_train:
        model.train()
    total_loss = 0
    correct = 0
    total = 0
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    loop = tqdm(data_loader)
    for input, target in loop:
        input, target = input.to(device), target.to(device)

        # calculate loss
        prediction = model(input)
        loss = loss_fn(prediction, target)

        if is_train:
            # backpropagate error and update weights
            optimiser.zero_grad()
            loss.backward()
            optimiser.step()

        # Calculate accuracy
        _, predicted = torch.max(prediction, 1)
        total += target.size(0)
        correct += (predicted == target).sum().item()

        for t, p in zip(target, predicted):
            idx = CLASS_MAPPING.index("Cry")
            tp += (t.item() == idx and p.item() == idx)
            fn += (t.item() == idx and p.item() != idx)
            tn += (t.item() != idx and p.item() != idx)
            fp += (t.item() != idx and p.item() == idx)

        total_loss += loss.item()

        loop.set_postfix(loss=loss.item(), correct=(
            predicted == target).sum().item())

    # Calculate accuracy
    accuracy = 100 * correct / total
    average_loss = total_loss / len(data_loader)
    if tp + fp == 0:
        precision = 0
    else:
        precision = tp / (tp + fp)
    if tp + fn == 0:
        recall = 0
    else:
        recall = tp / (tp + fn)

    print(f"Loss: {average_loss:.4f}, Accuracy: {accuracy:.2f}%, Precision: {precision:.2f}, Recall: {recall:.2f}")
    return average_loss, accuracy, precision, recall


def train(model, train_data_loader, test_data_loader, loss_fn, optimiser, device, epochs):
    losses = []
    accs = []
    precisions = []
    recalls = []
    test_losses = []
    test_accs = []
    test_precisions = []
    test_recalls = []
    for i in range(epochs):
        if (i % 5 == 0 and i!=0):
          torch.save(model.state_dict(), f"audionet.{i}.pth")
        print(f"Epoch {i+1}")
        loss, acc, pre, rec = step(
            model, train_data_loader, loss_fn, optimiser, device)
        losses.append(loss)
        accs.append(acc)
        precisions.append(pre)
        recalls.append(rec)

        test_loss, test_acc, test_pre, test_rec = step(
            model, test_data_loader, loss_fn, optimiser, device, is_train=False)
        test_losses.append(test_loss)
        test_accs.append(test_acc)
        test_precisions.append(test_pre)
        test_recalls.append(test_rec)
        if i % 10 == 0:
            torch.save(cnn.state_dict(), f"cnnnet.{i}.pth")
    print("Finished training")
    return losses, accs, precisions, recalls, test_losses, test_accs, test_precisions, test_recalls

if __name__ == "__main__":
    if torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"
    print(f"Using {device}")

    # instantiating our dataset object and create data loader

    train_ds = CryDataset(device, csv_path='train_data.csv')
    test_ds = CryDataset(device, csv_path='val_data.csv')
    train_dataloader = create_data_loader(train_ds, BATCH_SIZE)
    test_dataloader = create_data_loader(test_ds, BATCH_SIZE)

    # construct model and assign it to device
    cnn = AlexNet(num_classes=NUM_CLASSES).to(device)
    # print(cnn)

    # initialise loss funtion + optimiser
    loss_fn = nn.CrossEntropyLoss()
    optimiser = torch.optim.Adam(cnn.parameters(),
                                 lr=LEARNING_RATE)

    # train model
    losses, accs, precisions, recalls, test_losses, test_accs, test_precisions, test_recalls = train(cnn, train_dataloader, test_dataloader, loss_fn,
                                                                                                     optimiser, device, EPOCHS)

    # save model
    torch.save(cnn.state_dict(), "audionet.pth")
    print("Trained feed forward net saved at audionet.pth")

    with open('history.csv', 'w') as f:
        column_headers = ['Train loss','Train accuracy','Train precision','Train recall','Validate loss','Validate accuracy','Validate precision','Validate recall']
        writer = csv.writer(f, lineterminator='\r')
        writer.writerow(column_headers)
        writer.writerows(zip(losses, accs, precisions, recalls,
                         test_losses, test_accs, test_precisions, test_recalls))

    with open('losses.txt', 'w') as f:
        f.write(str(losses))
    with open('accuracy.txt', 'w') as f:
        f.write(str(accs))

    with open('val_losses.txt', 'w') as f:
        f.write(str(test_losses))
    with open('val_accuracy.txt', 'w') as f:
        f.write(str(test_accs))
