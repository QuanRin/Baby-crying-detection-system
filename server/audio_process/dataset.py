import os
from torch.utils.data import Dataset
import torchaudio
import random
from util import AudioUtil
from audio_utils import CLASS_MAPPING
import csv


class CryDataset(Dataset):

    def __init__(self,
                 device,
                 csv_path):
        self.device = device
        self.transformation = AudioUtil.spectro_gram().to(self.device)
        self.annotations = []
        self.shift_pct = 0.4
        with open(csv_path) as f:
            reader = csv.reader(f)
            for data in reader:
                self.annotations.append(data)
        # classes = os.listdir(audio_dir)
        # for _cls in classes:
        #     src_dir = os.path.join(audio_dir, _cls)
        #     for fn in os.listdir(src_dir):
        #         self.annotations.append(
        #             [CLASS_MAPPING.index(_cls), os.path.join(src_dir, fn)])

    def __len__(self):
        return len(self.annotations)

    def __getitem__(self, index):
        audio_sample_path = self._get_audio_sample_path(index)
        label = int(self._get_audio_sample_label(index))
        signal, sr = torchaudio.load(audio_sample_path)
        shift_aud = AudioUtil.time_shift(signal, self.shift_pct)
        shift_aud = shift_aud.to(self.device)
        sgram = self.transformation(shift_aud)
        aug_sgram = AudioUtil.spectro_augment(sgram, max_mask_pct=0.1, n_freq_masks=2, n_time_masks=2)
        return aug_sgram, label

    def _get_audio_sample_path(self, index):
        return self.annotations[index][1]

    def _get_audio_sample_label(self, index):
        return self.annotations[index][0]


if __name__ == "__main__":
    data = []
    classes = os.listdir("clean")
    for _cls in classes:
        if _cls not in CLASS_MAPPING:
            continue
        src_dir = os.path.join("clean", _cls)
        for fn in os.listdir(src_dir):
            data.append([CLASS_MAPPING.index(_cls), os.path.join(src_dir, fn)])
            # self.annotations.append(
            #     [CLASS_MAPPING.index(_cls), os.path.join(src_dir, fn)])
    train_data = []
    val_data = []
    test_data = []
    for i in range(len(CLASS_MAPPING)):
        filtered_data = [row for row in data if row[0] == i]
        n = len(filtered_data)
        random.shuffle(filtered_data)
        train_data += filtered_data[:int(7*n/10)]
        val_data += filtered_data[int(7*n/10):int(7*n/10)+int(2*n/10)]
        test_data += filtered_data[int(7*n/10)+int(2*n/10):]

    with open('train_data.csv', 'w') as f:
        writer = csv.writer(f, lineterminator='\r')
        writer.writerows(train_data)
    with open('val_data.csv', 'w') as f:
        writer = csv.writer(f, lineterminator='\r')
        writer.writerows(val_data)
    with open('test_data.csv', 'w') as f:
        writer = csv.writer(f, lineterminator='\r')
        writer.writerows(test_data)
