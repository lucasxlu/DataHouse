import os
import numpy as np
import pandas as pd


def out_result(predicted_list, gt_lst, path="./result/testset_result.csv"):
    """
    output a result file
    :param predicted_list:
    :param gt_lst:
    :param path:
    :return:
    """
    col = ['predicted', 'groundtruth']
    arr = np.array([list(predicted_list), gt_lst.values.ravel()])
    df = pd.DataFrame(arr.T, columns=col)
    mkdirs_if_not_exist('./result/')
    df.to_csv(path, index=False, encoding='UTF-8')


def mkdirs_if_not_exist(dir_name):
    """
    make directory if not exist
    :param dir_name:
    :return:
    """
    if not os.path.isdir(dir_name) or not os.path.exists(dir_name):
        os.makedirs(dir_name)
