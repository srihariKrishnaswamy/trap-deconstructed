import os
import csv
from pydub import AudioSegment
import random
import shutil
bpms = {
    0: "100",
    1: "110",
    2: "120",
    3: "130",
    4: "140",
    5: "150",
    6: "160",
    7: "170",
    8: "180",
    9: "190"
}
feels = {
    0: "angry",
    1: "chill",
    2: "vibey",
    3: 'lit'
}
keys = {
    0: "C", 1: "C Sharp", 2: "D", 3: "D Sharp", 4: "E",
    5: "F", 6: "F Sharp", 7: "G", 8: "G Sharp",
    9: "A", 10: "A Sharp", 11: "B",
} # bpm-key-feel-mode
modes = {
    0: 'minor',
    1: 'major'
}
def get_all_songs(path): # returns a list of all the song names without the .wav suffix
    all_pending = os.listdir(path)
    if ".DS_Store" in all_pending: all_pending.remove(".DS_Store")
    for i in range(len(all_pending)):
        all_pending[i] = all_pending[i][:len(all_pending[i]) - 4]
    return all_pending
def get_labels(song):
    bpm = ""
    key = ""
    feel = ""
    mode = ""
    dashcount = 0
    for c in song:
        if c == '-':
            dashcount += 1
        elif dashcount == 1:
            bpm += c
        elif dashcount == 2:
            key += c
        elif dashcount == 3:
            feel += c
        elif dashcount == 4:
            mode += c
    print(f"BPM: {bpms[int(bpm)]}, KEY: {keys[int(key)]} MODE: {modes[int(mode)]}, FEEL: {feels[int(feel)]}")
    return bpm, key, feel, mode
MODE="test" #train or test
GENRE="trap"
PENDING_FILES_PATH = os.path.join(os.path.dirname(__file__), "to_be_processed", GENRE)
SONG_NAMES = get_all_songs(PENDING_FILES_PATH)
NUM_TO_COLLECT = 10
SECONDS_PER_CHOP = 8 # eight seconds per chop
DATA_DIR = os.path.join(os.path.dirname(__file__), f"./{MODE}_data")
ANNOTATIONS_PATH=os.path.join(DATA_DIR,"annotations.csv")
PROCESSED_PATH = os.path.join(os.path.dirname(__file__), "processed_songs", GENRE)
if __name__ == "__main__":
    for i in range(len(SONG_NAMES)):
        SONG_NAME = SONG_NAMES[i]
        SONG_PATH = os.path.join(PENDING_FILES_PATH,SONG_NAME+".wav")
        annotations_data = []
        good_to_chop = True
        song = AudioSegment.from_wav(SONG_PATH)
        chops_dir = os.path.join(DATA_DIR, SONG_NAME)
        if not os.path.isdir(chops_dir): 
            os.mkdir(chops_dir)
        else:
            contents = os.listdir(chops_dir)
            if len(contents) > 0:
                good_to_chop = False
                print("Folder already exists and is populated, re-chopping the song will jumble the associated annotations")
        if good_to_chop:
            print(f"song number {i + 1}")
            bpm, key, feel, mode = get_labels(SONG_NAME)
            interval = SECONDS_PER_CHOP * 1000
            print("Chopping up the song...")
            num_collected = 0
            while num_collected < NUM_TO_COLLECT: # we get every other four second interval
                random_start = random.randint(0, len(song) - interval)
                chop = song[random_start:random_start+interval] # we get a random 8-second part of the song
                snippet_title = f"{SONG_NAME}-{str(num_collected)}.wav"
                chop.export(os.path.join(chops_dir,snippet_title), format="wav")
                annotations_data.append([snippet_title,chops_dir,bpm,key,feel,mode])
                num_collected += 1
            print("Finished chopping")
            with open(ANNOTATIONS_PATH, mode='a', newline='') as f:
                writer = csv.writer(f)
                for row in annotations_data:
                    writer.writerow(row)
            print("Finished annotations")
    # move the songs to the processed songs folder
    for i in range(len(SONG_NAMES)):
        source_path = os.path.join(PENDING_FILES_PATH,SONG_NAMES[i]+".wav")
        shutil.move(source_path, PROCESSED_PATH)