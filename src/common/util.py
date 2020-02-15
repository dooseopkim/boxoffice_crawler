from requests import Session
from bs4 import BeautifulSoup
import json
import os
from time import localtime


def get_html_text(**kwargs):
    # url을 입력하면 html text를 반환
    html = Session().get(kwargs['url'])
    if html.status_code != 200:
        raise Exception('올바르지 않은 URL 요청')
    return html.text


def get_soup(**kwargs):
    return BeautifulSoup(kwargs['page'], 'lxml')


def get_confs(*args):
    pass


def write_json(**kwargs):
    path = kwargs['path']
    json_file = kwargs['file']
    with open(path, 'w', encoding='utf8') as f:
        json.dump(json_file, f, ensure_ascii=False)


def get_file_name(**kwargs):
    stat = kwargs['stat']
    ext = kwargs['ext']
    start = kwargs['start']
    end = kwargs['end']

    t = localtime()
    f_name = ''
    f_name += str(t.tm_year)[2:]
    f_name += '0' + str(t.tm_mon) if t.tm_mon < 10 else str(t.tm_mon)
    f_name += '0' + str(t.tm_mday) if t.tm_mday < 10 else str(t.tm_mday)
    f_name += 'crawl_' + stat
    f_name += str(start) if start == end else str(start) + '_' + str(end)
    f_name += '.' + ext
    return f_name


def hello():
    return 'hello'
