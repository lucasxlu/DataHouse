"""
Data mining and NLP task with liepin job detailed description corpus.
"""
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
    texts = [cut_words(document) for document in documents]
    dictionary = corpora.Dictionary(texts)

    class MyCorpus(object):
        def __iter__(self):
            with open('/home/lucasx/PycharmProjects/DataHouse/DataSet/liepin/191938818.txt', mode='rt',
                      encoding='UTF-8') as f:
                # assume there's one document per line, tokens separated by whitespace
                yield dictionary.doc2bow(cut_words(''.join(f.readlines())))

    print(dictionary.doc2bow(
        cut_words(read_document_from_text('/home/lucasx/PycharmProjects/DataHouse/DataSet/liepin/191938818.txt'))))
    print('===========================================')
    corpus_memory_friendly = MyCorpus()
    tfidf = models.TfidfModel(corpus_memory_friendly)  # step 1 -- initialize a model
    corpus_tfidf = tfidf[corpus_memory_friendly]
    for doc in corpus_tfidf:
        print(doc)


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
    document_dir = '/home/lucasx/PycharmProjects/DataHouse/DataSet/liepin/'
    documents = [read_document_from_text(os.path.join(document_dir, _)) for _ in os.listdir(document_dir)]
    main(documents)
