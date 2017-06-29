"""
Titanic survive prediction
"""
from sklearn.feature_selection import VarianceThreshold
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.neighbors.nearest_centroid import NearestCentroid
from sklearn import tree
import pandas as pd
import numpy as np

TRAIN_CSV = '/home/lucasx/Documents/Kaggle/Data/train.csv'
TEST_CSV = '/home/lucasx/Documents/Kaggle/Data/test.csv'
GROUND_TRUTH = '/home/lucasx/Documents/Kaggle/Data/gender_submission.csv'


def load_training_set(csv_filepath):
    df = pd.read_csv(csv_filepath)
    y = df['Survived'].tolist()
    sex_num = []
    for _ in df['Sex']:
        if _ == 'male':
            sex_num.append(1)
        elif _ == 'female':
            sex_num.append(0)
    embarked_num = []
    for _ in df['Embarked']:
        if _ == 'S':
            embarked_num.append(0)
        elif _ == 'Q':
            embarked_num.append(1)
        elif _ == 'C':
            embarked_num.append(2)
        else:
            counts = np.bincount(embarked_num)
            embarked_num.append(np.argmax(counts))
    X = pd.DataFrame([df['Pclass'].tolist(), sex_num, df['Age'].tolist(), df['SibSp'].tolist(), df['Parch'].tolist(),
                      df['Fare'].tolist(), embarked_num])

    return X.fillna(value=np.mean(df['Age'])).T, y


def load_test_data(csv_filepath):
    df = pd.read_csv(csv_filepath)
    sex_num = []
    for _ in df['Sex']:
        if _ == 'male':
            sex_num.append(1)
        elif _ == 'female':
            sex_num.append(0)
    embarked_num = []
    for _ in df['Embarked']:
        if _ == 'S':
            embarked_num.append(0)
        elif _ == 'Q':
            embarked_num.append(1)
        elif _ == 'C':
            embarked_num.append(2)
    X = pd.DataFrame([df['Pclass'].tolist(), sex_num, df['Age'].tolist(), df['SibSp'].tolist(), df['Parch'].tolist(),
                      df['Fare'].tolist(), embarked_num])

    return X.fillna(value=np.mean(df['Age'])).T


if __name__ == '__main__':
    percentage = 0.9
    X_train, y_train = load_training_set(TRAIN_CSV)
    X_train, y_train = X_train[0: int(len(X_train) * percentage)], y_train[0: int(len(y_train) * percentage)]
    X_val, y_val = X_train[int(len(X_train) * percentage): len(X_train)], y_train[
                                                                          int(len(y_train) * percentage): len(y_train)]
    print('loading data successfully~')
    print('=' * 100)
    X_test = load_test_data(TEST_CSV)
    y_test = pd.read_csv(GROUND_TRUTH)['Survived']

    sel = VarianceThreshold(threshold=(.7 * (1 - .7)))
    X_train = sel.fit_transform(X_train)

    print('start launching Random Forest Classifier......')
    rf = RandomForestClassifier(n_estimators=10)
    rf.fit(X_train, y_train)
    print('finish launching Random Forest Classifier, the test accuracy is {:.5%}'.format(rf.score(X_val, y_val)))
    rf_predict = rf.predict(X_test)

    print('=' * 100)
    print('start launching SVM Classifier......')
    svm = svm.SVC()
    svm.fit(X_train, y_train)
    print('finish launching SVM Classifier, the test accuracy is {:.5%}'.format(svm.score(X_val, y_val)))
    svm_predict = svm.predict(X_test)

    print('=' * 100)
    print('start launching KNN Classifier......')
    knn = NearestCentroid()
    knn.fit(X_train, y_train)
    print('finish launching KNN Classifier, the test accuracy is {:.5%}'.format(knn.score(X_val, y_val)))
    knn.predict(X_test)

    print('=' * 100)
    print('start launching Decision Tree Classifier......')
    dtree = tree.DecisionTreeClassifier()
    dtree.fit(X_train, y_train)
    print('finish launching Decision Tree Classifier, the test accuracy is {:.5%}'.format(dtree.score(X_val, y_val)))
    dtree_predict = dtree.predict(X_test)

    print('=' * 100)
    print('start launching MLP Classifier......')
    mlp = MLPClassifier(solver='lbfgs', alpha=1e-4, hidden_layer_sizes=(7, 2), random_state=1)
    mlp.fit(X_train, y_train)
    print('finish launching MLP Classifier, the test accuracy is {:.5%}'.format(mlp.score(X_val, y_val)))
    mlp_predict = mlp.predict(X_test)

    dataframe = pd.DataFrame(pd.read_csv(TEST_CSV)['PassengerId'].tolist(), dtree_predict)
    dataframe.to_csv('~/gender_submission.csv')
