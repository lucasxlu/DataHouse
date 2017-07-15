import glob
import os
import csv

import pandas as pd
import numpy as np
import scipy
from scipy.io import wavfile
from matplotlib.pyplot import specgram


SONGS_DIR= 'C:/CloudMusic/'

def generate_data_and_label(songs_dir):
    """
    genertate dataset with its label
    :param songs_dir:
    :return:
    """
    song_data = dict()
    for label_dir in os.listdir(songs_dir):
        if label_dir == '1':
            for _ in os.listdir(os.path.join(songs_dir, label_dir)):
                song_filepath = os.path.join(songs_dir, label_dir, _)
                # print(song_filepath)
                song_data[_] = 1
        elif label_dir == '0':
            for _ in os.listdir(os.path.join(songs_dir, label_dir)):
                song_filepath = os.path.join(songs_dir, label_dir, _)
                # print(song_filepath)
                song_data[_] = 0

    with open('dataset.csv', 'wt', encoding='UTF-8', newline='') as csvfile:
        fieldnames = ['songname', 'filename', 'label']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for key, value in song_data.items():
            writer.writerow({'songname': key, 'filename': key.replace(' ', ''), 'label': value})
        print('Pre-processing done!!!')


def create_fft(filename):
    sample_rate, X = wavfile.read(filename)
    fft_features = abs(scipy.fft(X)[0:1000])
    base_fn, ext = os.path.splitext(filename)
    data_fn = base_fn + '.fft'
    np.save(data_fn, fft_features)

    # draw the spec gram figure
    print(sample_rate, X.shape)
    specgram(X, Fs=sample_rate, xextent=(0, 30))


def read_fft(genre_list, base_dir):
    X = []
    y = []
    for label, genre in enumerate(genre_list):
        genre_dir = os.path.join(base_dir, genre, '*.fft.npy')
        file_list = glob.glob(genre_dir)
        for fn in file_list:
            fft_features = np.load(fn)
            X.append(fft_features[:1000])
            y.append(label)

    return np.array(X), np.array(y)


if __name__ == '__main__':
    # generate_data_and_label(SONGS_DIR)
    # create_fft("D:/1.wav")
    read_fft([0, 1], base_dir='D:/')
