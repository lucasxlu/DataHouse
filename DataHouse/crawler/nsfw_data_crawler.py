# Python script for downloading NSFW images
# https://github.com/alexkimxyz/nsfw_data_scrapper.git

import os
import requests

TIMEOUT = 30


def mkdirs_if_not_exist(dir_name):
    """
    make directory if not exist
    :param dir_name:
    :return:
    """
    if not os.path.isdir(dir_name) or not os.path.exists(dir_name):
        os.makedirs(dir_name)


def download_img(img_url, save_filename):
    """
    download image from a given url
    :param img_url:
    :param save_filename:
    :return:
    """
    response = requests.get(img_url, timeout=TIMEOUT)
    if response.status_code not in [404, 403, 500]:
        with open(save_filename, mode='wb') as f:
            f.write(response.content)
            f.flush()
            f.close()

    print('{0} has been downloaded...'.format(save_filename))


def batch_download(raw_data_dir="/home/xulu/Project/nsfw_data_scrapper/raw_data"):
    """
    batch download
    :param raw_data_dir:
    :return:
    """
    for cat in os.listdir(raw_data_dir):
        print('Start processing {0} ...'.format(cat))
        url_txt = os.path.join(raw_data_dir, cat, 'urls_{0}.txt'.format(cat))

        mkdirs_if_not_exist(os.path.join(raw_data_dir, cat, 'IMAGES'))

        with open(url_txt, mode='rt', encoding='utf-8') as f:
            urls = f.readlines()

            file_index = 0
            for url in urls:
                try:
                    download_img(url,
                                 os.path.join(os.path.join(raw_data_dir, cat, 'IMAGES', '{0}.jpg'.format(file_index))))
                    file_index += 1
                except:
                    pass

    print('done!')


if __name__ == '__main__':
    batch_download()
