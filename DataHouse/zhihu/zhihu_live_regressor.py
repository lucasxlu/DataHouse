import json
import os
from collections import OrderedDict

import numpy as np
import pandas as pd
import requests
from sklearn import preprocessing
from sklearn.feature_selection import VarianceThreshold, SelectKBest, chi2, f_regression
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, Imputer
from sklearn.linear_model import RidgeCV, LassoCV
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.svm import SVR
from sklearn.externals import joblib

import torch
from torch.optim import lr_scheduler
from torch.utils.data import Dataset, DataLoader
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.autograd import Variable

BATCH_SIZE = 16


class MTLoss(nn.Module):
    """
    Loss function for MTB-DNN
    """

    def __init__(self, k):
        super(MTLoss, self).__init__()
        self.k = k

    def forward(self, sum_loss):
        return torch.div(sum_loss, self.k)


class Branch(nn.Module):
    def __init__(self, params=[8, 4, 1]):
        """Constructs each branch necessary depending on input
        Args:
            b2(nn.Module()): An nn.Conv2d() is passed with specific params
        """
        super(Branch, self).__init__()
        self.bf1 = nn.Linear(params[0], params[1])
        self.bf2 = nn.Linear(params[1], params[2])

    def forward(self, x):
        return self.bf2(F.tanh(self.bf1(x)))


class MTBDNN(nn.Module):
    def __init__(self, K=2):
        super(MTBDNN, self).__init__()
        self.K = K
        self.layers = nn.Sequential(OrderedDict([
            ('fc1', nn.Sequential(nn.Linear(23, 16),
                                  nn.ReLU())),
            ('fc2', nn.Sequential(nn.Linear(16, 8),
                                  nn.ReLU())),
            ('fc3', nn.Sequential(nn.Linear(8, 8),
                                  nn.ReLU()))]))

        self.branch1 = Branch(params=[8, 4, 1])
        self.branch2 = Branch(params=[8, 3, 1])
        self.branch3 = Branch(params=[8, 5, 1])

    def forward(self, x):
        out = torch.zeros([BATCH_SIZE, 1])

        if torch.cuda.is_available():
            out = out.cuda()

        for idx, module in self.layers.named_children():
            x = F.tanh(module(x))

        temp = x

        return torch.div(torch.add(torch.add(self.branch1(temp), self.branch2(temp)), self.branch3(temp)), self.K)
        # return torch.min([self.branch1(temp), self.branch2(temp), self.branch3(temp)])


class MLP(nn.Module):

    def __init__(self):
        super(MLP, self).__init__()
        self.fc1 = nn.Linear(23, 16)
        self.fc2 = nn.Linear(16, 8)
        self.fc3 = nn.Linear(8, 8)
        # self.drop1 = nn.Dropout2d(0.7)
        self.fc4 = nn.Linear(8, 1)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        # x = self.drop1(x)
        x = self.fc4(x)

        return x

    def num_flat_features(self, x):
        size = x.size()[1:]  # all dimensions except the batch dimension
        num_features = 1
        for s in size:
            num_features *= s

        return num_features


def split_train_test(excel_path, test_ratio, dl=True):
    # df = pd.read_excel(excel_path, sheetname="Preprocessed").fillna(value=0)
    df = pd.read_excel(excel_path, sheetname="Preprocessed")
    # df = df[df['review_score'] > 0]
    print("*" * 100)
    if not dl:
        dataset = df.loc[:, ['duration', 'reply_message_count', 'source', 'purchasable', 'is_refundable',
                             'has_authenticated', 'user_type', 'gender', 'badge', 'tag_id',
                             'speaker_audio_message_count',
                             'attachment_count', 'liked_num', 'is_commercial', 'audition_message_count',
                             'is_audition_open',
                             'seats_taken', 'seats_max', 'speaker_message_count', 'amount', 'original_price',
                             'has_audition', 'has_feedback', 'review_count']]
        dataset['tag_id'] = dataset['tag_id'].fillna(value=0)
        print(dataset.describe())

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

    else:
        dataset = df.loc[:, ['duration', 'reply_message_count', 'source', 'purchasable', 'is_refundable',
                             'has_authenticated', 'user_type', 'gender', 'badge', 'speaker_audio_message_count',
                             'attachment_count', 'liked_num', 'is_commercial', 'audition_message_count',
                             'is_audition_open', 'seats_taken', 'seats_max', 'speaker_message_count', 'amount',
                             'original_price', 'has_audition', 'has_feedback', 'review_count']]
        print(dataset.describe())
        min_max_scaler = preprocessing.MinMaxScaler()
        dataset = min_max_scaler.fit_transform(dataset)
        dataset = pd.DataFrame(dataset)
        labels = df.loc[:, ['review_score']]

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

    # model = LassoCV(alphas=[_ * 0.1 for _ in range(1, 1000, 1)])
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
    print('===============The Mean Absolute Error is {0}===================='.format(mae_lr))
    print('===============The Root Mean Square Error is {0}===================='.format(rmse_lr))
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


def mtb_dnns(train, test, train_Y, test_Y, epoch=100):
    """
    train and test with MTB-DNN
    :param train:
    :param test:
    :param train_Y:
    :param test_Y:
    :return:
    """

    class ZhihuLiveDataset(Dataset):

        def __init__(self, X, y, transform=None):
            self.data = X
            self.labels = y
            self.transform = transform

        def __len__(self):
            return len(self.labels)

        def __getitem__(self, idx):
            sample = {'data': self.data.iloc[idx - 1].as_matrix().astype(np.float32),
                      'label': self.labels.iloc[idx - 1].as_matrix().astype(np.float32)}

            if self.transform:
                sample = self.transform(sample)

            return sample

    trainloader = torch.utils.data.DataLoader(ZhihuLiveDataset(train, train_Y), batch_size=BATCH_SIZE,
                                              shuffle=True, num_workers=4)
    testloader = torch.utils.data.DataLoader(ZhihuLiveDataset(test, test_Y), batch_size=BATCH_SIZE,
                                             shuffle=False, num_workers=4)

    mtbdnn = MTBDNN(K=3)
    print(mtbdnn)
    # mlp = MLP()
    criterion = nn.MSELoss()
    optimizer = optim.Adam(mtbdnn.parameters(), lr=0.001, weight_decay=1e-3)
    # optimizer = optim.SGD(mtbdnn.parameters(), lr=0.0001, momentum=0.9, weight_decay=1e-4)
    # optimizer = optim.SGD(mlp.parameters(), lr=0.001, momentum=0.9)
    # learning_rate_scheduler = lr_scheduler.ExponentialLR(optimizer, gamma=0.5)

    for epoch in range(epoch):  # loop over the dataset multiple times

        running_loss = 0.0
        for i, data_batch in enumerate(trainloader):
            # learning_rate_scheduler.step()
            inputs, labels = data_batch['data'], data_batch['label']

            inputs, labels = Variable(inputs, requires_grad=True), Variable(labels)
            if torch.cuda.is_available():
                inputs = inputs.cuda()
                labels = labels.cuda()
                mtbdnn = mtbdnn.cuda()
                # mlp = mlp.cuda()

            optimizer.zero_grad()

            # outputs = mlp.forward(inputs)
            outputs = mtbdnn.forward(inputs)
            loss = criterion(outputs, labels)
            # loss.requires_grad = True  # explicitly declare require gradient

            # [ERROR HERE!!!] WHY CANNOT BE UPDATED???
            loss.backward()
            optimizer.step()

            running_loss += loss.data[0]
            if i % 10 == 0:
                print('[%d, %5d] loss: %.3f' %
                      (epoch + 1, i + 1, running_loss / 100))
                running_loss = 0.0

    print('Finished Training\n')
    print('save trained model...')
    model_path_dir = './model'
    if not os.path.isdir(model_path_dir) or not os.path.exists(model_path_dir):
        os.makedirs(model_path_dir)
    torch.save(mtbdnn.state_dict(), os.path.join(model_path_dir, 'zhihu_live_mtbdnn.pth'))
    # torch.save(mlp.state_dict(), os.path.join(model_path_dir, 'zhihu_live_mlp.pth'))

    predicted_labels = []
    gt_labels = []
    for data_batch in testloader:
        inputs, labels = data_batch['data'], data_batch['label']
        if torch.cuda.is_available():
            inputs = inputs.cuda()
            mtbdnn = mtbdnn.cuda()
            # mlp = mlp.cuda()

        # outputs = mlp.forward(Variable(inputs))
        outputs = mtbdnn.forward(Variable(inputs))
        predicted_labels += outputs.cpu().data.numpy().tolist()
        gt_labels += labels.numpy().tolist()

    mae_lr = round(mean_absolute_error(np.array(gt_labels), np.array(predicted_labels)), 4)
    rmse_lr = round(np.math.sqrt(mean_squared_error(np.array(gt_labels), np.array(predicted_labels))), 4)
    print('===============The Mean Absolute Error of MTB-DNN is {0}===================='.format(mae_lr))
    print('===============The Root Mean Square Error of MTB-DNN is {0}===================='.format(rmse_lr))


def predict_score(zhihu_live_id):
    """
    predict a Zhihu Live's score with ML model
    :Note: Normalization need to be done!!!
    :param zhihu_live_id:
    :return:
    """
    req_url = 'https://api.zhihu.com/lives/%s' % str(zhihu_live_id).strip()
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Host': 'api.zhihu.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        'Upgrade-Insecure-Requests': '1'
    }
    cookies = dict(
        cookies_are='')
    response = requests.get(req_url, headers=headers, cookies=cookies)
    if response.status_code == 200:
        live = response.json()
        print(live)
        if live['review']['count'] < 18:
            print('The number of scored people is scarce, please buy this Live carefully!')
        else:
            # if tf.gfile.Exists('./model/regression.pkl'):
            #     reg = joblib.load('./model/regression.pkl')
            #     score = reg.predict()
            if os.path.exists('./model/zhihu_live_mlp.pth'):
                net = MLP()
                net.load_state_dict(torch.load('./model/zhihu_live_mlp.pth'))
                input = np.array([live['duration'], live['reply_message_count'], 1 if live['source'] == 'admin' else 0,
                                  int(live['purchasable']), int(live['is_refundable']), int(live['has_authenticated']),
                                  0 if live['speaker']['member']['user_type'] == 'organization' else 1,
                                  live['speaker']['member']['gender'], len(live['speaker']['member']['badge']),
                                  live['speaker_audio_message_count'], live['attachment_count'], live['liked_num'],
                                  int(live['is_commercial']), live['audition_message_count'],
                                  int(live['is_audition_open']),
                                  live['seats']['taken'], live['seats']['max'], live['speaker_message_count'],
                                  live['fee']['amount'],
                                  live['fee']['original_price'] / 100, int(live['has_audition']),
                                  int(live['has_feedback']), live['review']['count']], dtype=np.float32)
                if torch.cuda.is_available():
                    net = net.cuda()
                    input = Variable(torch.from_numpy(input)).cuda()

                score = net.forward(input)
                print('Score is %d' % score)
    else:
        print(response.status_code)


if __name__ == '__main__':
    train_set, test_set, train_label, test_label = split_train_test("./ZhihuLiveDB.xlsx", 0.2)
    # train_and_test_model(train_set, test_set, train_label, test_label)
    mtb_dnns(train_set, test_set, train_label, test_label, 30)

    # predict_score('788099469471121408')
