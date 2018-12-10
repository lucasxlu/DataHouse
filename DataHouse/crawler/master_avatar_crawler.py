import os
import requests

URL_TEMPLATE = ""
SAVE_TO_DIR_ROOT = None


def mkdirs_if_not_exist(dir_name):
    """
    create new folder if not exist
    :param dir_name:
    :return:
    """
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


def crawl_avatar(avatar_url):
    response = requests.get(avatar_url, timeout=20)
    if response.status_code != 404:
        avatar_filename = avatar_url.split('/')[-1]
        year = avatar_filename[0:4]
        college = avatar_filename[4:7]

        mkdirs_if_not_exist(os.path.join(SAVE_TO_DIR_ROOT, year, college))

        with open(os.path.join(SAVE_TO_DIR_ROOT, year, college, avatar_filename), mode='wb') as f:
            f.write(response.content)
            f.flush()
            f.close()

        print('{0} has been downloaded...'.format(avatar_filename))
    else:
        print('File {0} does not exist...'.format(avatar_url.split('/')[-1]))


if __name__ == '__main__':
    for year in [2016, 2017, 2018]:
        for college in [_ for _ in range(301, 320)]:
            for i in range(200):
                if i < 10:
                    idx = str(year) + str(college) + str(11000) + str(i)
                elif 10 <= i < 100:
                    idx = str(year) + str(college) + str(1100) + str(i)
                else:
                    idx = str(year) + str(college) + str(110) + str(i)

                try:
                    crawl_avatar(URL_TEMPLATE % str(idx))
                except:
                    pass
