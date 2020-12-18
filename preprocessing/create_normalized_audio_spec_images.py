import librosa
import os
from os import path
from os.path import normpath as npath, join as pjoin
from shutil import rmtree
import csv

DATA_PATH = npath(path.abspath('../Data'))
CATS = (str(i) for i in range(1, 6))
IMG_DIR = 'images'
IMG_NORMAL = 'normal'
IMG_FORMAT = 'formatted'
CSV_DIR = 'csv'

SPEC_CENTROIDS_CSV = 'spec_centroids.csv'
SPEC_ROLLOFF_CSV = 'spec_rolloff.csv'
SPEC_BANDWIDTH_CSV = 'spec_bandwidth.csv'
ZERO_CROSSING_CSV = 'zero_crossing.csv'
MFCC_CSV = 'mfcc.csv'


BAD_FILES = '2\\03-01-02-01-01-02-01_A1.wav 2\\03-01-02-01-02-02-05_A5.wav 3\\03-01-03-01-02-01-20_A20.wav'.split()
BAD_FILES_PATHS = {pjoin(DATA_PATH, file) for file in BAD_FILES}

FR = 48000

STFT_FRAMES = 1024 * 4
WINDOWS_AMOUNT = 177090.946262 // STFT_FRAMES
csl_set = set()
mfcc_set = set()

for cat in CATS:
    cat_path = pjoin(DATA_PATH, cat)

    img_path = pjoin(cat_path, IMG_DIR)
    if os.path.exists(img_path):
        rmtree(img_path)
    os.makedirs(img_path)

    img_path_n = pjoin(img_path, IMG_NORMAL)
    img_path_f = pjoin(img_path, IMG_FORMAT)
    os.makedirs(img_path_n)
    os.makedirs(img_path_f)

    img_path_csv = pjoin(cat_path, CSV_DIR)
    if os.path.exists(img_path_csv):
        rmtree(img_path_csv)
    os.makedirs(img_path_csv)

    print(f'Category: {cat_path}')
    wave_files = list(filter(lambda p: os.path.isfile(p) and p[-4:] == '.wav' and p not in BAD_FILES_PATHS,
                             list(map(lambda p: pjoin(cat_path, p), os.listdir(cat_path)))))

    time_series = {file: librosa.load(file, offset=1, sr=FR)[0] for file in wave_files}
    tss = {file: (ts, int(len(ts) // WINDOWS_AMOUNT)) for file, ts in time_series.items()}

    # spec_centroids
    with open(pjoin(DATA_PATH, cat, CSV_DIR, SPEC_CENTROIDS_CSV), 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['file', *list(range(44))])
        for file in wave_files:
            centroids = librosa.feature.spectral_centroid(tss[file][0], sr=FR, hop_length=tss[file][1], win_length=tss[file][1] // 2, n_fft=tss[file][1] // 2)[0]
            writer.writerow([file, *centroids[:43]])

    # spec_rolloff
    with open(pjoin(DATA_PATH, cat, CSV_DIR, SPEC_ROLLOFF_CSV), 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['file', *list(range(44))])
        for file in wave_files:
            rolloffs = librosa.feature.spectral_rolloff(tss[file][0], sr=FR, hop_length=tss[file][1], win_length=tss[file][1] // 2, n_fft=tss[file][1] // 2)[0]
            writer.writerow([file, *rolloffs[:43]])

    # bandwidths
    with open(pjoin(DATA_PATH, cat, CSV_DIR, SPEC_BANDWIDTH_CSV), 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['file', *list(range(44))])
        for file in wave_files:
            bandwidths = librosa.feature.spectral_bandwidth(tss[file][0], sr=FR, hop_length=tss[file][1], win_length=tss[file][1] // 2, n_fft=tss[file][1] // 2)[0]
            writer.writerow([file, *bandwidths[:43]])

    # zero crossing rare
    with open(pjoin(DATA_PATH, cat, CSV_DIR, ZERO_CROSSING_CSV), 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['file', *list(range(44))])
        for file in wave_files:
            rates = librosa.feature.zero_crossing_rate(tss[file][0], frame_length=tss[file][1] // 2, hop_length=tss[file][1])[0]
            writer.writerow([file, *rates[:43]])
            csl_set.add(rates.shape)

    # mfcc?
    for file in wave_files:
        mfcc = librosa.feature.mfcc(tss[file][0], sr=FR, n_mfcc=16)
        mfcc_set.add(mfcc.shape)
