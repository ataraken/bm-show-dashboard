from bs4 import BeautifulSoup
import json
import os
import requests
import requests_cache
import urllib.parse

REST_EU_ROOT_URL = 'http://restcountries.eu/rest/v1/'

def request(field='all', name='', params=None):
    headers = {'User-Agent': 'Mozilla/5.0'}

    if params is None:
        params = {}

    url = ''
    if field == 'all':
        url = urllib.parse.urljoin(REST_EU_ROOT_URL, field)
    else:
        url = urllib.parse.urljoin(REST_EU_ROOT_URL, field, name)

    response = requests.get(url, params=params, headers=headers)
    if not response.status_code == 200:
        raise Exception('Request failed with status code: {0}'.format(response.status_code))

    return response.content

def cleaning(src):
    dst = {}

    for record in src:
        info = {
            'name': record['name'],
            'alpha3Code': record['alpha3Code'],
            'latlng': record['latlng']
        }
        dst[record['name']] = info

    return dst

def make_country_name_ja_to_en_tbl(src):
    dst = {}

    for record in src:
        en = record['name']
        ja = record['translations']['ja']
        dst[ja] = en

    return dst

def make_id_name_pair_list(src):
    dst = []

    for record in src:
        id = record['numericCode']
        name = record['name']
        
        if id != None:
            element = {
                'id': int(id),
                'name': name
            }
            dst.append(element)

    return dst


if __name__ == '__main__':
    res = request()
    info = json.loads(res)
    country_info = cleaning(info)
    cnv_tbl_country_name_ja_to_en = make_country_name_ja_to_en_tbl(info)
    id_name_pair = make_id_name_pair_list(info)

    folder_path = '../ui/static/data'
    country_info_file_name = 'country_info.json'
    tbl_file_name = 'tbl_country_name_ja_to_en.json'
    id_name_pair_file_name = 'country_id_name_pair.json'

    if not os.path.isdir(folder_path):
        os.path.makedirs(folder_path)

    with open(os.path.join(folder_path, country_info_file_name), 'w') as fw:
        json.dump(country_info, fw, indent=2, ensure_ascii=False)

    with open(os.path.join(folder_path, tbl_file_name), 'w') as fw:
        json.dump(cnv_tbl_country_name_ja_to_en, fw, indent=2, ensure_ascii=False)

    with open(os.path.join(folder_path, id_name_pair_file_name), 'w') as fw:
        json.dump(id_name_pair, fw, indent=2, ensure_ascii=False)

