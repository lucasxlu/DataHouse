import pandas as pd

MOOC_CSV_DATA = 'E:/DataSet/MOOC/HMXPC13_DI_v2_5-14-14.csv'


def data_pre_processing():
    df = pd.read_csv(MOOC_CSV_DATA)
    # df = df.fillna(df.mean()['YoB', 'grade', 'last_event_DI', 'nevents', 'ndays_act', 'nplay_video', 'nchapters'])
    df = df.fillna(df.mean()['YoB'])
    print(df)


if __name__ == '__main__':
    data_pre_processing()
