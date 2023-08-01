from torch.utils.data import Dataset
import torch
import pandas as pd
import torchaudio
import os
device = "cpu"
class BPMFeelDataset(Dataset):
    def __init__(self, annotations_file, target_sample_rate, num_samples, set_type, device=device):
        self.set_type = set_type
        self.annotations = pd.read_csv(annotations_file)
        self.device = device
        self.transformation = torchaudio.transforms.MelSpectrogram(
            sample_rate=target_sample_rate,
            n_fft=1024, # frame size
            hop_length=512,
            n_mels=64
        )
        self.target_sample_rate = target_sample_rate
        self.num_samples = num_samples #Signal should have num samples == num_samples
    def __len__(self): #len(dataset)
        return len(self.annotations)
    def __getitem__(self, index): # loads waveform of audio sample associated with certain index, also return the label associated with it
        audio_sample_path = self._get_audio_sample_path(index)
        label = self._get_audio_sample_label(index)
        signal, sr = torchaudio.load(audio_sample_path) # sr is sample rate, we're gonna have to resample so everything is standardized
        signal = signal.to(self.device)
        signal = self._resample_if_necessary(signal, sr)
        # signal -> (num_channels, samples) -> eg (2, 16000) want to mix it down to (1, 16000), we wanna agregate across dimension 0 and put everything on one channel (mono)
        # need to standardize signals to mono, some might be in stereo
        signal = self._mix_down_if_necessary(signal)
        # print(signal.shape)
        signal = self._cut_if_necessary(signal) # truncate signal if it's too long
        signal = self._right_pad_if_necessary(signal) # if we don't have enough samples
        # print(signal.shape)
        signal = self.transformation(signal) # this is now the mel spectrogram of the signal: signal goes from (num_channes, samples) to 3 dims: (num_channels (1), frequency, time)
        # print(f"shape of signal: {signal.shape}")
        return signal, label
    def _cut_if_necessary(self, signal):
        # signal -> Tensor -> (num channels, samples) -> (1, num_samples) -> (1, 50000) -> (1, 22050)
        if signal.shape[1] > self.num_samples:
            signal = signal[:, :self.num_samples] # slice the signal down
        return signal
    def _right_pad_if_necessary(self, signal):
        length_signal = signal.shape[1]
        if length_signal < self.num_samples:
            num_missing_samples = self.num_samples - length_signal
            last_dim_padding = (0, num_missing_samples) # num to prepend, then num to append
            # [1, 1, 1] -> [1, 1, 1, 0, 0]
            # (1, num_samples)
            signal = torch.nn.functional.pad(signal, last_dim_padding)
        return signal
    def _resample_if_necessary(self, signal, sr): #resample if the sample rate is not correct
        if sr != self.target_sample_rate:
            resampler = torchaudio.transforms.Resample(sr, self.target_sample_rate)
            signal = resampler(signal)
        return signal
    def _mix_down_if_necessary(self, signal): # get everything into mono
        if signal.shape[0] > 1:
            signal = torch.mean(signal, dim=0, keepdim=True)
        return signal
    def _get_audio_sample_path(self, index):
        folder = self.annotations.iloc[index, 1]
        file_name = self.annotations.iloc[index, 0]
        path = os.path.join(folder, file_name)
        # print(f"audio path: {path}")
        return path
    def _get_audio_sample_label(self, index):
        if self.set_type == 'bpm':
            return self.annotations.iloc[index, 2]
        elif self.set_type == 'key':
            return self.annotations.iloc[index, 3]
        elif self.set_type == 'feel':
            return self.annotations.iloc[index, 4]
        else: #returns the mode
            return self.annotations.iloc[index, 5]
SAMPLE_RATE = 22050
NUM_SAMPLES = 176400 # each tensor will represent 8 seconds of audio
TRAIN_DATA_PATH = os.path.join(os.path.dirname(__file__), 'train_data')
TEST_DATA_PATH = os.path.join(os.path.dirname(__file__), 'test_data')
ANNOTATIONS_FILE='annotations.csv'
TRAIN_ANNOTATIONS=os.path.join(TRAIN_DATA_PATH,ANNOTATIONS_FILE)
TEST_ANNOTATIONS=os.path.join(TEST_DATA_PATH,ANNOTATIONS_FILE)