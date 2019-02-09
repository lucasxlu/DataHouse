# a web crawler for meizitu
import sys
import os
from pprint import pprint

import requests
from bs4 import BeautifulSoup

IMAGE_DOWNLOAD_BASE_DIR = "D:/"


def get_all_topics():
    """
    get all topics
    :return:
    """
    headers = {
        'referer': 'https://www.mzitu.com/best/',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/72.0.3626.81 Safari/537.36',
    }
    response = requests.get("https://www.mzitu.com/zhuanti/", timeout=30, headers=headers)

    tags = {}

    if response.status_code == 200:
        bs = BeautifulSoup(response.text, "lxml")
        tags_div = bs.find_all('div', class_="postlist")[0].find_all('dl', class_="tags")[0]

        for child in tags_div.children:
            if child.name is not None:
                if child.name == 'dd':
                    tag = child.contents[0]
                    tags[tag.text] = tag['href']
    else:
        print('Error occurs during get all topics...')

    return tags


def get_tag_images_urls():
    """
    for example: all image batch URLs in https://www.mzitu.com/tag/barbie-ker/
    :return:
    """



def download_img(img_url, directory):
    """
    download image from a given URL
    :param img_url:
    :param directory:
    :return:
    """
    img_filename = img_url.split('/')[-1]
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/72.0.3626.81 Safari/537.36",
        "referer": "https://www.mzitu.com/55891/2",
        "upgrade-insecure-requests": "1"
    }
    response = requests.get(img_url, timeout=30, headers=headers)

    mkdirs_if_not_exists(os.path.join(IMAGE_DOWNLOAD_BASE_DIR, directory))

    if response.status_code in [200, 304]:
        with open(os.path.join(IMAGE_DOWNLOAD_BASE_DIR, directory, img_filename), mode='wb') as f:
            f.write(response.content)
            f.flush()
            f.close()
        print('{0} has been downloaded...'.format(img_url))
    else:
        print('Error occurs when download %s. Error code is %d.' % (img_url, response.status_code))


def mkdirs_if_not_exists(directory_):
    """
    create a new folder if it does not exist
    """
    if not os.path.exists(directory_) or not os.path.isdir(directory_):
        os.makedirs(directory_)


if __name__ == '__main__':
    # pprint(get_all_topics())
    download_img("https://i.meizitu.net/2015/12/29b02.jpg", "Barbie可儿")
