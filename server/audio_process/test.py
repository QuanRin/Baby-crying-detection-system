import torch
from audio_utils import *
from dataset import CryDataset
from model import CNNNetwork, AlexNet
from torch.utils.data import DataLoader
from sklearn.metrics import precision_score, recall_score, accuracy_score

def predict(model, input, target, device):
    model = model.to(device)
    model.eval()
    with torch.no_grad():
        input = input.to(device)
        predictions = model(input)
        predicted_index = predictions[0].argmax(0)
        if predicted_index < 0 or predicted_index >= NUM_CLASSES:
            print("Predicted index is out of range.")
            return None
        return predicted_index.item(), target.item()


def start_test():
    if torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"
    print(f"Using {device}")
    # load back the model
    cnn = AlexNet(num_classes=NUM_CLASSES)
    state_dict = torch.load("audionet.pth", map_location=torch.device(device))
    cnn.load_state_dict(state_dict)

    ds = CryDataset(device=device, csv_path='test_data.csv')

    batch_size = 1
    data_loader = DataLoader(ds, batch_size=batch_size, shuffle=False)

    # Initialize variables to accumulate TP, FP, and FN
    y_true = []
    y_pred = []

    for batch in data_loader:
        inputs, targets = batch

        for i in range(len(inputs)):
            input = inputs[i].unsqueeze(0)
            predicted_index, target_index = predict(cnn, input, targets[i], device)

            # Append true labels and predicted labels
            y_true.append(target_index)
            y_pred.append(predicted_index)

            # predicted = CLASS_MAPPING[predicted_index]
            # expected = CLASS_MAPPING[target_index]
            # print(f"Predicted: '{predicted}', Expected: '{expected}'")

    # Calculate precision for each class
    precision = precision_score(y_true, y_pred, average=None)

    # Recall
    recall = recall_score(y_true, y_pred, average=None)

    # Accuracy
    accuracy = accuracy_score(y_true, y_pred)
    for i, (class_precision, class_recall) in enumerate(zip(precision, recall)):
      class_name = CLASS_MAPPING[i]
      print(f'Class: {class_name}')
      print(f'  Precision: {class_precision}')
      print(f'  Recall: {class_recall}')
      print()

    # Overall accuracy
    print(f'Overall Accuracy: {accuracy}')

start_test()