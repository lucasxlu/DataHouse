import os
import shutil

import gensim
import jieba
import jieba.analyse
from gensim.models import Word2Vec
from sklearn.feature_extraction.text import TfidfTransformer, HashingVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn import tree
from sklearn.neighbors.nearest_centroid import NearestCentroid

TEXT_DIR = '/home/lucasx/Desktop/corpus_6_4000/'
# TEXT_DIR = '/home/lucasx/Desktop/20_newsgroups/'
# TEXT_DIR = '/home/lucasx/Desktop/FudanNLPCorpus/'
FEATURE_NUM = 5000
STOPWORDS_FILE = 'stopwords.txt'
USER_DICT = 'userdict.txt'
WORD2VEC_SAVE_PATH = '/tmp/word2vector2.model'


def split_corpus_6_4000_train_and_test_dataset(dir_):
    """
    init the corpus_6_4000 text data and return the feature vectors in TF-IDF mode
    :param dir_:
    :return:
    """

    def get_all_categories(dir_):
        category_list = []
        for _ in os.listdir(dir_):
            category = _.split('_')[0].strip()
            if category not in category_list:
                category_list.append(category)

        return category_list

    category_list = get_all_categories(dir_)
    training_data_ratio = 0.7
    dataset = {
        'name': 'dataset'
    }
    training_set = {
    }

    test_set = {
    }

    category_num = {}
    for category in category_list:
        if category == 'Military':
            category_num[category] = 0
        elif category == 'Culture':
            category_num[category] = 1
        elif category == 'Economy':
            category_num[category] = 2
        elif category == 'Sports':
            category_num[category] = 3
        elif category == 'Auto':
            category_num[category] = 4
        else:
            category_num[category] = 5
        dataset[category_num[category]] = [os.path.join(dir_, _) for _ in os.listdir(dir_) if category in _]

    for category, num in category_num.items():
        training_set[num] = dataset[num][0: int(len(dataset[num]) * training_data_ratio)]
        test_set[num] = dataset[num][int(len(dataset[num]) * training_data_ratio): len(dataset[num])]

    training_text = []
    training_label = []
    test_text = []
    test_label = []
    for label, filepath_list in training_set.items():
        training_text += [read_document_from_text(_) for _ in filepath_list]
        training_label += [label for _ in range(len(filepath_list))]

    for label, filepath_list in test_set.items():
        test_text += [read_document_from_text(_) for _ in filepath_list]
        test_label += [label for _ in range(len(filepath_list))]

    return training_text, training_label, test_text, test_label


def get_corpus_6_4000_feature_veactor_in_tf_idf(training_text, test_text):
    training_X = documents_to_tfidf_vec(training_text)
    test_X = documents_to_tfidf_vec(test_text)

    return training_X, test_X


def init_20groups_data(base_dir):
    """
    init training and test text data and return the feature vector in TF-IDF mode
    :param base_dir:
    :return:
    """

    def get_labels():
        label_and_num = {}
        i = 0
        for _ in os.listdir(base_dir):
            label_and_num[_] = i
            i += 1
        return label_and_num

    training_set = {}
    training_label = []
    test_set = {}
    test_label = []
    label_and_num = get_labels()
    for _ in os.listdir(base_dir):
        files_in_category = [os.path.join(base_dir, _, txt) for txt in os.listdir(os.path.join(base_dir, _))]
        print(files_in_category)
        training_set[_] = [read_document_from_text(textfilepath) for textfilepath in
                           files_in_category[0: int(len(files_in_category) * 0.8)]]
        training_label += [label_and_num[_] for i in range(int(len(files_in_category) * 0.8))]

        test_set[_] = [read_document_from_text(_) for _ in
                       files_in_category[int(len(files_in_category) * 0.8): len(files_in_category)]]
        test_label += [label_and_num[_] for i in range(len(files_in_category) - int(len(files_in_category) * 0.8))]

    train_X = documents_to_tfidf_vec(training_set)
    test_X = documents_to_tfidf_vec(test_set)

    return train_X, training_label, test_X, test_label


def init_corpus_6_4000_in_word2vec(training_text, test_text):
    train_X = []
    test_X = []
    for text in training_text:
        train_X.append([word2vector(word) for word in cut_words(text)])

    for text in test_text:
        test_X.append([word2vector(word) for word in cut_words(text)])

    return train_X, test_X


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


def documents_to_tfidf_vec(documents):
    """
    convert the document text list into the TF-IDF feature matrix X
    :param documents:
    :return:
    """
    transformer = TfidfTransformer(smooth_idf=True)
    hasher = HashingVectorizer(n_features=FEATURE_NUM,
                               stop_words=get_stopwords(STOPWORDS_FILE), non_negative=True,
                               norm=None, binary=False)
    vectorizer = make_pipeline(hasher, transformer)
    X = vectorizer.fit_transform(documents)

    return X


def read_document_from_text(text_filepath):
    """
    read document content from txt file
    :param text_filepath:
    :return:
    """
    with open(text_filepath, mode='rt') as f:
        document = ''.join(f.readlines())
        f.close()

    return document


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


def train_word2vec():
    """
    train word2vec model
    :return:
    """

    class MyCorpus(object):
        def __init__(self):
            pass

        def __iter__(self):
            for fname in os.listdir(TEXT_DIR):
                text = read_document_from_text(os.path.join(TEXT_DIR, fname))
                segmented_words = '/'.join(cut_words(''.join(text))).split('/')
                yield segmented_words

    sentences = MyCorpus()
    model = gensim.models.Word2Vec(sentences, workers=8)

    model.save(WORD2VEC_SAVE_PATH)


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


def word2vector(word):
    model = Word2Vec.load(WORD2VEC_SAVE_PATH)

    return model[word]


def hotwords_to_vec_weighted_with_tfidf(hotword_list_with_tfidf):
    for hotword, tfidf in hotword_list_with_tfidf.items():
        word2vector(hotword) * tfidf
        pass


def hotwords_to_vec_weighted_without_tfidf(hotword_list):
    """
    sum up all word2vec vectors and calculate the mean as the text feature vector
    :param hotword_list:
    :return:
    """
    text_vec = []
    for hotword in hotword_list:
        text_vec += word2vector(hotword)

    return text_vec / len(hotword_list)


if __name__ == '__main__':
    print('=' * 100)
    print('start training word2vec...')
    train_word2vec()
    print('finish training word2vec...')
    print('=' * 100)

    training_text, training_label, test_text, test_label = split_corpus_6_4000_train_and_test_dataset(TEXT_DIR)
    # train_X, test_X = get_corpus_6_4000_feature_veactor_in_tf_idf(training_text, test_text)
    train_X, test_X = init_corpus_6_4000_in_word2vec(training_text, test_text)

    print('=' * 100)
    print('start launching MLP Classifier......')
    mlp = MLPClassifier(solver='lbfgs', alpha=1e-4, hidden_layer_sizes=(50, 30, 20, 20), random_state=1)
    mlp.fit(train_X, training_label)
    print('finish launching MLP Classifier, the test accuracy is {:.5%}'.format(mlp.score(test_X, test_label)))

    print('=' * 100)
    print('start launching Decision Tree Classifier......')
    dtree = tree.DecisionTreeClassifier()
    dtree.fit(train_X, training_label)
    print('finish launching Decision Tree Classifier, the test accuracy is {:.5%}'.format(
        dtree.score(test_X, test_label)))

    print('=' * 100)
    print('start launching KNN Classifier......')
    knn = NearestCentroid()
    knn.fit(train_X, training_label)
    print('finish launching KNN Classifier, the test accuracy is {:.5%}'.format(knn.score(test_X, test_label)))

    print('=' * 100)
    print('start launching Random Forest Classifier......')
    rf = RandomForestClassifier(n_estimators=10)
    rf.fit(train_X, training_label)
    print('finish launching Random Forest Classifier, the test accuracy is {:.5%}'.format(rf.score(test_X, test_label)))

"""
    train_X, training_label, test_X, test_label = init_20groups_data(TEXT_DIR)
    

    print('=' * 100)
    print('start launching MLP Classifier......')
    mlp = MLPClassifier(solver='lbfgs', alpha=1e-4, hidden_layer_sizes=(50, 30, 20, 20), random_state=1)
    mlp.fit(train_X, training_label)
    print('finish launching MLP Classifier, the test accuracy is {:.5%}'.format(mlp.score(test_X, test_label)))
"""
