from torch.utils.data import Dataset
import torch
import pandas as pd
import torchaudio
import os
import data_config
device = data_config.device
class PredictionAudio(Dataset): # the audio that we wanna predict on - we don't need annotations here
    def __init__(self, audio_path, target_sample_rate, num_samples, device=device):
        self.audio_path = audio_path
        self.annotation = -1 
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
        return 1
    def __getitem__(self, index): # loads waveform of audio sample associated with certain index, also return the label associated with it
        audio_sample_path = self.audio_path
        label = self.annotation
        signal, sr = torchaudio.load(audio_sample_path) # sr is sample rate, we're gonna have to resample so everything is standardized
        signal = signal.to(self.device)
        signal = self._resample_if_necessary(signal, sr)
        signal = self._mix_down_if_necessary(signal)
        signal = self._cut_if_necessary(signal) # truncate signal if it's too long
        signal = self._right_pad_if_necessary(signal) # if we don't have enough samples
        signal = self.transformation(signal) # this is now the mel spectrogram of the signal: signal goes from (num_channes, samples) to 3 dims: (num_channels (1), frequency, time)
        return signal, label
    def _cut_if_necessary(self, signal):
        if signal.shape[1] > self.num_samples:
            signal = signal[:, :self.num_samples] # slice the signal down
        return signal
    def _right_pad_if_necessary(self, signal):
        length_signal = signal.shape[1]
        if length_signal < self.num_samples:
            num_missing_samples = self.num_samples - length_signal
            last_dim_padding = (0, num_missing_samples) # num to prepend, then num to append
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