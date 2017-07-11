# data mining and machine learning with douban movie data
import sklearn
import pandas as pd

DOUBAN_MOVIE_CSV = '/home/lucasx/PycharmProjects/DataHouse/DataSet/douban/movie.csv'


def pre_processing(csv_data):
    df = pd.read_csv(csv_data)
    return df


if __name__ == '__main__':
    director_list = []
    for _ in pre_processing(DOUBAN_MOVIE_CSV)['directors']:
        if _ not in director_list:
            director_list.append(_)

    print(director_list)
