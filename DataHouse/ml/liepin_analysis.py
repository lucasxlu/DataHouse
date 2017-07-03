"""
Data mining and NLP task with liepin job detailed description corpus.
"""
import logging
import os
from shutil import copyfile

import gensim
import jieba
import jieba.analyse
from gensim.models import Word2Vec
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfTransformer, HashingVectorizer
from sklearn.pipeline import make_pipeline

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
STOPWORDS_FILE = 'stopwords.txt'
USER_DICT = 'userdict.txt'
DOCUMENT_DIR = '/home/lucasx/PycharmProjects/DataHouse/DataSet/liepin/'
WORD2VEC_SAVE_PATH = '/tmp/word2vector2.model'
FEATURE_NUM = 30
CLUSTER_NUM = 6


def train_word2vec():
    """
    train word2vec model
    :return:
    """

    class MyCorpus(object):
        def __init__(self):
            pass

        def __iter__(self):
            for fname in os.listdir(DOCUMENT_DIR):
                text = read_document_from_text(os.path.join(DOCUMENT_DIR, fname))
                segmented_words = '/'.join(cut_words(''.join(text))).split('/')
                yield segmented_words

    sentences = MyCorpus()
    model = gensim.models.Word2Vec(sentences, workers=8)

    model.save(WORD2VEC_SAVE_PATH)
    # print(model.similarity('机器学习', '深度学习'))


def word2vector(word):
    model = Word2Vec.load(WORD2VEC_SAVE_PATH)

    return model[word]


def documents_to_tfidf_vec(documents):
    transformer = TfidfTransformer(smooth_idf=True)
    hasher = HashingVectorizer(n_features=FEATURE_NUM,
                               stop_words=get_stopwords(STOPWORDS_FILE), non_negative=True,
                               norm=None, binary=False)
    vectorizer = make_pipeline(hasher, transformer)
    X = vectorizer.fit_transform(documents)

    return X


def kmeans_cluster(feature_matrix):
    km = KMeans(n_clusters=CLUSTER_NUM, init='k-means++', max_iter=100, n_init=1, verbose=True)
    km.fit(feature_matrix)

    print('=======================================')
    folder = '/tmp/liepin/'
    for _ in os.listdir(DOCUMENT_DIR):
        X = documents_to_tfidf_vec([read_document_from_text(os.path.join(DOCUMENT_DIR, _))])
        label_ = str(km.predict(X).astype(int))
        if os.path.exists(os.path.join(folder, label_)) is False:
            os.makedirs(os.path.join(folder, label_))
        copyfile(os.path.join(DOCUMENT_DIR, _), os.path.join(folder, label_, _))
    print('processing done!!')


def get_stopwords(stopwords_filepath):
    """
    read stopwords and return as a python list
    :param stopwords_filepath:
    :return:
    """
    with open(stopwords_filepath, mode='rt', encoding='UTF-8') as f:
        stopwords = f.readlines()
        f.close()

    return stopwords


def read_document_from_text(text_filepath):
    """
    read document content from txt file
    :param text_filepath:
    :return:
    """
    with open(text_filepath, mode='rt', encoding='UTF-8') as f:
        document = ''.join(f.readlines())
        f.close()

    return document


def get_tfidf_top_words(documents):
    """
    calculate the top hot 30 keywords with TF-IDF value
    :param documents:
    :return:
    """
    jieba.load_userdict(USER_DICT)
    jieba.analyse.set_stop_words(STOPWORDS_FILE)
    hot_words = jieba.analyse.extract_tags(''.join(documents), topK=30, withWeight=True, allowPOS=(), withFlag=True)

    return hot_words


def cut_words(document):
    """
    cut the document text and return its word list
    :param document:
    :return:
    """
    jieba.load_userdict(USER_DICT)
    jieba.analyse.set_stop_words(STOPWORDS_FILE)
    seg_list = jieba.cut(document, cut_all=True)
    return '/'.join(seg_list).split('/')


if __name__ == '__main__':
    # train_word2vec()
    # model = Word2Vec.load(WORD2VEC_SAVE_PATH)
    # print(model.similarity('阿里巴巴', '腾讯'))

    documents = [read_document_from_text(os.path.join(DOCUMENT_DIR, _)) for _ in os.listdir(DOCUMENT_DIR)]

    X = documents_to_tfidf_vec(documents)
    kmeans_cluster(X)
