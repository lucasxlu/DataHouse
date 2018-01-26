import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.feature_selection import VarianceThreshold, SelectKBest, chi2, f_regression
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, Imputer
from sklearn.linear_model import RidgeCV, LassoCV
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.svm import SVR


# import tensorflow as tf


def split_train_test(excel_path, test_ratio):
    # df = pd.read_excel(excel_path, sheetname="Preprocessed").fillna(value=0)
    df = pd.read_excel(excel_path, sheetname="Preprocessed")
    # df = df[df['review_score'] > 0]
    print("*" * 100)
    dataset = df.loc[:, ['duration', 'reply_message_count', 'source', 'purchasable', 'is_refundable',
                         'has_authenticated', 'user_type', 'gender', 'badge', 'tag_id', 'speaker_audio_message_count',
                         'attachment_count', 'liked_num', 'is_commercial', 'audition_message_count', 'is_audition_open',
                         'seats_taken', 'seats_max', 'speaker_message_count', 'amount', 'original_price',
                         'has_audition', 'has_feedback', 'review_count']]
    dataset['tag_id'] = dataset['tag_id'].fillna(value=0)

    imp = Imputer(missing_values='NaN', strategy='median', axis=0)
    imp.fit(dataset)

    source_le = LabelEncoder()
    source_labels = source_le.fit_transform(dataset['source'])
    dataset['source'] = source_labels
    # source_mappings = {index: label for index, label in enumerate(source_le.classes_)}

    enc = preprocessing.OneHotEncoder()
    enc.fit_transform(
        dataset[['source', 'purchasable', 'is_refundable', 'user_type', 'is_commercial', 'is_audition_open',
                 'has_audition', 'has_feedback']])

    tag_id_le = LabelEncoder()
    tag_id_labels = tag_id_le.fit_transform(dataset['tag_id'])
    dataset['tag_id'] = tag_id_labels

    min_max_scaler = preprocessing.MinMaxScaler()
    dataset = min_max_scaler.fit_transform(dataset)

    labels = df.loc[:, ['review_score']]

    dataset, labels = feature_selection(dataset, labels, k=15)

    dataset = pd.DataFrame(dataset)
    labels = pd.DataFrame(labels)
    print(dataset.describe())
    print("*" * 10)

    shuffled_indices = np.random.permutation(len(df))
    test_set_size = int(len(df) * test_ratio)
    test_indices = shuffled_indices[:test_set_size]
    train_indices = shuffled_indices[test_set_size:]

    return dataset.iloc[train_indices], dataset.iloc[test_indices], \
           labels.iloc[train_indices], labels.iloc[test_indices]


def train_and_test_model(train, test, train_Y, test_Y):
    # model = Pipeline([('poly', PolynomialFeatures(degree=3)),
    #                   ('linear', LinearRegression(fit_intercept=False))])

    # model = RidgeCV(alphas=[_ * 0.1 for _ in range(1, 1000, 1)])
    # model = SVR(kernel='rbf', C=1e3, gamma=0.1)
    # model = SVR(kernel='linear', C=1e3)
    # model = SVR(kernel='poly', C=1e3, degree=2)
    # model = KNeighborsRegressor(n_neighbors=10, n_jobs=4)

    model = MLPRegressor(hidden_layer_sizes=(16, 8, 8), early_stopping=True, alpha=1e-4,
                         batch_size=16, learning_rate='adaptive')
    model.fit(train, train_Y)
    predicted_score = model.predict(test)
    mae_lr = round(mean_absolute_error(test_Y, predicted_score), 4)
    rmse_lr = round(np.math.sqrt(mean_squared_error(test_Y, predicted_score)), 4)
    # pc = round(np.corrcoef(test_Y, predicted_score)[0, 1], 4)
    print('===============The Mean Absolute Error of Lasso Regression Model is {0}===================='.format(mae_lr))
    print('===============The Root Mean Square Error of Linear Model is {0}===================='.format(rmse_lr))
    # print('===============The Pearson Correlation of Model is {0}===================='.format(pc))

    from DataHouse.zhihu.zhihu_util import out_result
    out_result(predicted_score, test_Y)


def feature_selection(X, y, k=15):
    """
    feature selection
    :param X:
    :param y:
    :return:
    """
    print(X.shape)
    X = SelectKBest(f_regression, k=k).fit_transform(X, y)
    print(X.shape)

    return X, y


# def mtb_dnns(train, test, train_Y, test_Y):
#     """
#     play with MTB-DNNs
#     :param train:
#     :param test:
#     :param train_Y:
#     :param test_Y:
#     :return:
#     """
#     # Specify that all features have real-value data
#     feature_columns = [tf.feature_column.numeric_column("x", shape=[21])]
#
#     if not tf.gfile.Exists('./model') or tf.gfile.IsDirectory('./model'):
#         tf.gfile.MakeDirs('./model')
#
#     # Build 3 layer DNN with 10, 20, 10 units respectively.
#     classifier = tf.estimator.DNNRegressor(hidden_units=[16, 8, 8],
#                                            feature_columns=feature_columns,
#                                            model_dir="./model/mtb_dnns_tf",
#                                            label_dimension=1)
#     # Define the training inputs
#     train_input_fn = tf.estimator.inputs.numpy_input_fn(
#         x={"x": train},
#         y=train_Y,
#         num_epochs=None,
#         shuffle=True)
#
#     # Train model.
#     classifier.train(input_fn=train_input_fn, steps=100)
#
#     # Define the test inputs
#     test_input_fn = tf.estimator.inputs.numpy_input_fn(
#         x={"x": np.array(test)},
#         y=np.array(test_Y),
#         num_epochs=1,
#         shuffle=False)
#
#     # Evaluate accuracy.
#     accuracy_score = classifier.evaluate(input_fn=test_input_fn)["accuracy"]
#
#     print("\nTest Accuracy: {0:f}\n".format(accuracy_score))


if __name__ == '__main__':
    train_set, test_set, train_label, test_label = split_train_test("./ZhihuLiveDB.xlsx", 0.2)
    print(train_set.shape)
    train_and_test_model(train_set, test_set, train_label, test_label)
    # mtb_dnns(train_set, test_set, train_label, test_label)
