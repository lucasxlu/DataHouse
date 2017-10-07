import itertools
from pprint import pprint

import requests
from bs4 import BeautifulSoup
from lxml import etree

INDUSTRY_XML_PATH = './industry.xml'
PLACE_XML_PATH = './place.xml'


def parse_industry_xml():
    """
    parse config xml info from industry.xml
    :return: dict
    """
    tree = etree.parse(INDUSTRY_XML_PATH)

    industry_name_list = tree.xpath('//industry/text()')
    industry_value_list = tree.xpath('//industry/@value')

    industry = dict(itertools.zip_longest(industry_name_list, industry_value_list[:len(industry_name_list)]))

    return industry


def parse_place_xml():
    """
    parse config xml info from place.xml
    :return: dict
    """
    tree = etree.parse(PLACE_XML_PATH)

    place_name_list = tree.xpath('//place/text()')
    place_value_list = tree.xpath('//place/@value')

    place = dict(itertools.zip_longest(place_name_list, place_value_list[:len(place_name_list)]))

    return place


if __name__ == '__main__':
    pprint(parse_place_xml())
