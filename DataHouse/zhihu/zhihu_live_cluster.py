import pandas as pd
from sklearn import preprocessing
from sklearn.cluster import KMeans


def prepare_data(excel_path):
    df = pd.read_excel(excel_path, sheetname="Preprocessed").fillna(value=0)
    df = df[df['review_score'] > 0]
    print(df.describe())
    print("*" * 100)
    dataset = df.loc[:, ['duration', 'reply_message_count', 'source', 'purchasable', 'is_refundable',
                         'has_authenticated', 'user_type', 'gender', 'badge', 'speaker_audio_message_count',
                         'attachment_count', 'liked_num', 'is_commercial', 'audition_message_count', 'seats_taken',
                         'seats_max', 'speaker_message_count', 'original_price', 'has_audition', 'has_feedback',
                         'review_count']]
    min_max_scaler = preprocessing.MinMaxScaler()
    dataset = min_max_scaler.fit_transform(dataset)
    dataset = pd.DataFrame(dataset)
    kmeans = KMeans(n_clusters=5, random_state=0, n_jobs=4).fit(dataset)
    print(kmeans.score(dataset))


if __name__ == '__main__':
    prepare_data('./ZhiHuLiveDB.xlsx')
