"""
Data mining and NLP task with liepin job detailed description corpus.
"""
import logging
import os

import gensim
from gensim import corpora, models, similarities
import jieba
import jieba.analyse

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
STOPWORDS_FILE = 'stopwords.txt'
USER_DICT = 'userdict.txt'
DOCUMENT_DIR = '/home/lucasx/PycharmProjects/DataHouse/DataSet/liepin/'


def main(documents):
    # remove common words and tokenize
    texts = [cut_words(document) for document in documents]
    dictionary = corpora.Dictionary(texts)

    class MyCorpus(object):
        def __init__(self, dirname):
            self.dirname = dirname

        def __iter__(self):
            for fname in os.listdir(self.dirname):
                with open(os.path.join(self.dirname, fname), mode='rt',
                          encoding='UTF-8') as f:
                    yield cut_words(''.join(f.readlines()))

    sentences = MyCorpus(DOCUMENT_DIR)
    model = gensim.models.Word2Vec(sentences=sentences, iter=5, min_count=3, size=100, workers=2)
    model.build_vocab(sentences=sentences)
    model.train(sentences=sentences)
    model.accuracy('/tmp/questions-words.txt')


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
    return seg_list


if __name__ == '__main__':
    documents = [read_document_from_text(os.path.join(DOCUMENT_DIR, _)) for _ in os.listdir(DOCUMENT_DIR)]
    main(documents)
