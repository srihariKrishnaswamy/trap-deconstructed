import models
import torch
import data_creation
import os
from pydub import AudioSegment
from data_creation import bpms, feels, keys, modes
from prediction_audio import PredictionAudio
import data_config
from torch.utils.data import DataLoader

BPM_MODEL_NAME = "bpm_model_17_8s_with_BN_insane_train_acc.pt"
FEEL_MODEL_NAME = "feel_model_3_8s.pt"
MAJOR_KEY_MODEL_NAME = os.path.join('major', 'key_model_9_8s_major.pt')
MINOR_KEY_MODEL_NAME = os.path.join('minor', 'key_model_11_8s_minor.pt')
MODE_MODEL_NAME = 'mode_model_2_8s.pt'

BPM_MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models/bpm', BPM_MODEL_NAME)
FEEL_MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models/feel', FEEL_MODEL_NAME)
MAJOR_KEY_MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models/key', MAJOR_KEY_MODEL_NAME)
MINOR_KEY_MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models/key', MINOR_KEY_MODEL_NAME)
MODE_MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models/mode',MODE_MODEL_NAME)

SECONDS_PER_CHOP = data_creation.SECONDS_PER_CHOP
SAMPLE_RATE = data_config.SAMPLE_RATE
NUM_SAMPLES = data_config.NUM_SAMPLES
TEMP_NAME = "temp_snippet.wav"
INT_FOLDER = os.path.join(os.path.dirname(__file__), "prediction_processing")

# for now, we only take wav, need to convert mp3s to wavs and get this workaround

def get_middle(og_path):
    if os.path.exists(og_path) and os.path.isfile(og_path) and og_path.lower().endswith('.wav'):
        song = AudioSegment.from_wav(og_path)
        interval = 1000 * SECONDS_PER_CHOP
        if len(song) < interval:
            print("Given audio file is not long enough to predict on (at least 8s)")
            return None
        start = int(len(song)//2 - interval//2)
        chop = song[start:start+interval] # we get the middle 8 seconds of the song
        new_path = os.path.join(INT_FOLDER, TEMP_NAME)
        chop.export(new_path, format='wav')
        return new_path
    return None
def make_preds_from_path(song_path, bpm_model, feel_model, major_key_model, minor_key_model, mode_model): # assumes that song_path is valid, which it will be since we created it right before this method call
    bpm_feel_key = []
    bpm_model.eval()
    feel_model.eval()
    major_key_model.eval()
    minor_key_model.eval()
    song = PredictionAudio(song_path, SAMPLE_RATE, NUM_SAMPLES)
    song_dataloader = DataLoader(dataset=song, batch_size=1, shuffle=False)
    with torch.inference_mode():
        for batch, (x, y) in enumerate(song_dataloader): # this will only iterate once, I just needed a way to get the x alone
            bpm = torch.softmax(bpm_model(x), dim=1).argmax(dim=1)
            feel = torch.softmax(feel_model(x), dim=1).argmax(dim=1)
            mode = torch.softmax(mode_model(x), dim=1).argmax(dim=1)
            if int(mode) == 1: # major
                key = torch.softmax(major_key_model(x), dim=1).argmax(dim=1)
            elif int(mode) == 0: # minor
                key = torch.softmax(minor_key_model(x), dim=1).argmax(dim=1)
            else:
                print("THERE IS AN ERROR")
            bpm_feel_key.append(bpm)
            bpm_feel_key.append(feel)
            bpm_feel_key.append(key)
            bpm_feel_key.append(mode)
    return bpm_feel_key
def process_song_and_make_preds(og_path, bpm_model, feel_model, major_key_model, minor_key_model, mode_model):
    new_path = get_middle(og_path)
    if new_path is not None:
        bpm, feel, key, mode = make_preds_from_path(new_path, bpm_model, feel_model, major_key_model, minor_key_model, mode_model)
        os.remove(new_path)
        return bpm, feel, key, mode
    else:
        print("File does not exist or is of invalid format")
        return None, None, None, None
if __name__ == '__main__':
    bpm_model = models.BPM_Predictor(1, len(bpms))
    bpm_sd = torch.load(BPM_MODEL_PATH)
    bpm_model.load_state_dict(bpm_sd)

    feel_model = models.Feel_Predictor(1, len(feels))
    feel_sd = torch.load(FEEL_MODEL_PATH)
    feel_model.load_state_dict(feel_sd)

    major_key_model = models.Key_Predictor(1, len(keys))
    major_key_sd = torch.load(MAJOR_KEY_MODEL_PATH)
    major_key_model.load_state_dict(major_key_sd)

    minor_key_model = models.Key_Predictor(1, len(keys))
    minor_key_sd = torch.load(MINOR_KEY_MODEL_PATH)
    minor_key_model.load_state_dict(minor_key_sd)

    mode_model = models.Mode_Predictor(1)
    mode_sd = torch.load(MODE_MODEL_PATH)
    mode_model.load_state_dict(mode_sd)

    pred_path = input("Enter file path of song to find its bpm and vibe (must be a .wav file): ")
    bpm, feel, key, mode = process_song_and_make_preds(pred_path, bpm_model, feel_model, major_key_model, minor_key_model, mode_model)
    if bpm is not None and feel is not None and key is not None and mode is not None:
        print(f"BPM: {bpms[int(bpm)]} | Key: {keys[int(key)]} | Mode: {modes[int(mode)]} | Feel: {feels[int(feel)]}")
    else:
        print("there was an issue in processing")