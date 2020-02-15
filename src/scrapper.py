from tqdm import tqdm
from random import randint
from time import sleep
import json
import os
from operator import itemgetter
import argparse
import sys
sys.path.append('../')

from src.common import get_html_text, get_soup, get_file_name, write_json
from src.extracts import extract_movie_ids, extract_movie_info

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    # parse to argument
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--start', type=int, help='Start crawl year', required=True)
    parser.add_argument('-e', '--end', type=int, help='End crawl year')
    parser.add_argument('-d', '--directory', type=str, help='Outdata save directory', default='data')
    parser.add_argument('-g', '--genre', type=str, help='Select genre')
    parser.add_argument('-a', '--actor', type=str, help='Select actor')

    args = parser.parse_args()
    start = args.start
    end = start if not args.end else args.end
    directory = os.path.join(ROOT_DIR, args.directory) if args.directory == 'data' else args.directory
    if not os.path.exists(directory):
        os.makedirs(directory)
    # genre = args.genre
    # actor = args.actor

    years = [year for year in range(start, end + 1, 1)]

    # load to conf file
    with open(os.path.join(ROOT_DIR, 'rsc', 'conf.json'), 'r', encoding='cp949') as conf:
        urls = json.load(conf)['urls']

    # extract movie ids each year
    movie_ids = []
    for year in tqdm(years, desc='Scrapping years'):
        try:
            page = get_html_text(url=urls['sc_host'] + urls['sc_url_year'].format(year=year))
            soup = get_soup(page=page)
            movie_ids.append(extract_movie_ids(soup=soup))
        except Exception as e:
            print(e)
            continue

    # Remove duplicate ids and recursive list
    movie_ids = set([j for i in movie_ids for j in i])

    success_results = []
    fail_results = []

    # extract movie info each movie_id
    for movie_id in tqdm(movie_ids, desc='Extracting movie info'):
        sleep(randint(10, 100) / 50)
        try:
            page = get_html_text(url=urls['sc_host'] + urls['sc_url_id'].format(movie_id=movie_id))
            soup = get_soup(page=page)
            success_results.append(extract_movie_info(soup=soup))
        except Exception as e:
            fail_results.append({'movie_id': movie_id, 'exception': str(e)})
            continue

    # 개봉년도, 가나다 순으로 정렬
    success_results = sorted(success_results, key=itemgetter('date', 'title'))

    # json 파일로 쓰기
    success_result_out = os.path.join(directory, get_file_name(stat='success', ext='json', start=start, end=end))
    write_json(path=success_result_out, file=success_results)

    fail_result_out = os.path.join(directory, get_file_name(stat='fail', ext='json', start=start, end=end))
    write_json(path=fail_result_out, file=fail_results)


if __name__ == '__main__':
    main()
