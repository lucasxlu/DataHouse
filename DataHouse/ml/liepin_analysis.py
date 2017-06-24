import logging
import os

from gensim import corpora, models, similarities
import jieba
import jieba.analyse

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
STOPWORDS_FILE = 'stopwords.txt'
USER_DICT = 'userdict.txt'


def main(documents):
    # remove common words and tokenize
    stoplist = get_stopwords()
    texts = [[word for word in document.lower().split() if word not in stoplist] for document in documents]


def get_stopwords(stopwords_filepath):
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
    pass


if __name__ == '__main__':
    document_dir = '/home/lucasx/PycharmProjects/DataHouse/DataSet/liepin/'
    documents = [read_document_from_text(os.path.join(document_dir, _)) for _ in os.listdir(document_dir)]
    print(get_tfidf_top_words(documents))
