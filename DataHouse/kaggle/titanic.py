"""
Titanic survive prediction
"""
from sklearn.feature_selection import VarianceThreshold
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
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
    X_train, y_train = load_training_set(TRAIN_CSV)
    print('loading data successfully~')
    print('=' * 100)
    X_test = load_test_data(TEST_CSV)
    y_test = pd.read_csv(GROUND_TRUTH)['Survived']

    sel = VarianceThreshold(threshold=(.7 * (1 - .7)))
    X_train = sel.fit_transform(X_train)

    print('start launching Random Forest Classifier......')
    clf = RandomForestClassifier(n_estimators=10)
    clf.fit(X_train, y_train)
    y_predict = clf.predict(X_test)

    dataframe = pd.DataFrame(pd.read_csv(TEST_CSV)['PassengerId'].tolist(), y_predict)
    # dataframe.to_csv('~/gender_submission.csv')
    print('finish launching Random Forest Classifier, the test accuracy is {:.5%}'.format(clf.score(X_test, y_test)))

    """
    print('=' * 100)
    print('start launching SVM Classifier......')
    svm = svm.SVC()
    svm.fit(X_train, y_train)
    svm.predict(X_test)
    print('finish launching SVM Classifier, the test accuracy is {:.5%}'.format(svm.score(X_test, y_test)))

    print('=' * 100)
    print('start launching KNN Classifier......')
    knn = NearestCentroid()
    knn.fit(X_train, y_train)
    knn.predict(X_test)
    print('finish launching KNN Classifier, the test accuracy is {:.5%}'.format(knn.score(X_test, y_test)))

    print('=' * 100)
    print('start launching Decision Tree Classifier......')
    dtree = tree.DecisionTreeClassifier()
    dtree.fit(X_train, y_train)
    print('finish launching Decision Tree Classifier, the test accuracy is {:.5%}'.format(dtree.score(X_test, y_test)))
    """
