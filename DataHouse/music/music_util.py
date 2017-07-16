# a toolbox for music songs similarity weighting, song clustering, and so on
import csv
import logging
import os
import shutil

import numpy as np
import scipy
from matplotlib.pyplot import specgram
from scipy.io import wavfile
from sklearn.cluster import KMeans

SONGS_DIR = '/home/lucasx/Documents/Dataset/CloudMusic/1'
FFT_NPY_DIR = '/home/lucasx/Documents/Dataset/CloudMusic/fft_npy'


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
        fieldnames = ['songname', 'label']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for key, value in song_data.items():
            writer.writerow({'songname': key.split('/')[-1], 'label': value})
        print('CSV file Pre-processing done!!!')


def create_fft(filename):
    sample_rate, X = wavfile.read(filename)
    fft_features = abs(scipy.fft(X)[0:1000])
    base_fn, ext = os.path.splitext(filename)
    data_fn = FFT_NPY_DIR + base_fn.split('/')[-1] + '.fft'
    np.save(data_fn, fft_features)

    # draw the spec gram figure
    print(sample_rate, X.shape)
    # specgram(X, Fs=sample_rate, xextent=(0, 30))


def batch_create_fft():
    if os.path.exists(FFT_NPY_DIR):
        shutil.rmtree(FFT_NPY_DIR)
    os.makedirs(FFT_NPY_DIR)
    for _ in os.listdir(SONGS_DIR):
        create_fft(os.path.join(SONGS_DIR, _))
    logging.log(logging.INFO, 'All music files have been processed successfully~~~')


def read_fft(fft_npy_file_dir):
    X = []
    y = []
    for fft_npy_file in os.listdir(fft_npy_file_dir):
        y.append(1)
        if fft_npy_file.endswith('.fft.npy'):
            X.append(np.load(os.path.join(fft_npy_file_dir, fft_npy_file))[:1000])
        else:
            logging.error('unsupported format for file %s' % fft_npy_file)

    return np.array(X), np.array(y)


def batch_rename(dir_):
    num = 1
    for _ in os.listdir(dir_):
        os.rename(os.path.join(dir_, _), os.path.join(dir_, '%d.mp3' % num))
        num += 1
    print('All mp3 files have been renamed...')


if __name__ == '__main__':
    # generate_data_and_label(SONGS_DIR)
    # batch_create_fft()
    X, y = read_fft(FFT_NPY_DIR)
    kmeans_model = KMeans(n_clusters=8, random_state=1).fit(X)
    labels = kmeans_model.labels_
    print(labels)
