from bs4 import BeautifulSoup
import requests
import requests_cache
import json
import os
import re
import copy
import urllib.parse

import datetime
import pandas as pd

requests_cache.install_cache('babymetal_pages', backend='sqlite', expire_after=7200)

class BabymetalWikipediaPage:
    _URL = 'https://ja.wikipedia.org'
    _URI = 'wiki/BABYMETAL'
    _HEADERS = {'User-Agent': 'Mozilla/5.0'}

    def __init__(self):
        pass

    def get_soup(self):
        url = urllib.parse.urljoin(self._URL, self._URI)
        response = requests.get(url, headers=self._HEADERS)
        return BeautifulSoup(response.content, "lxml")

class BabymetalShowTable:
    _NUM_OF_CELLS_IN_A_ROW = 5
    _INDEX_OF_TABLE = 18
    _headers = ['year', 'date', 'title', 'venue', 'remarks']
    _country_name_cnv_tbl = None

    def __init__(self, wikipedia_soup, table):
        self._table = soup.select('table.wikitable')[self._INDEX_OF_TABLE]
        self._country_name_cnv_tbl = table
        self._country_name_cnv_tbl['中華民国'] = 'Taiwan'
        self._country_name_cnv_tbl['ロシア'] = 'Russia'

    def save(self, path):
        with open(path, 'w') as fw:
            json.dump(self._show_list, fw, indent=2, ensure_ascii=False)

    def data_cleaning(self):
        df = pd.DataFrame(self._show_list)

        for idx, row in df.iterrows():
            date = pd.to_datetime(row.date, format='%m月%d日')
            date = datetime.date(int(row.year), date.month, date.day)
            row.date = date.strftime('%Y-%02m-%02d')

            row.country = re.sub('の旗', '', row.country)
            row.country = self._country_name_cnv_tbl[row.country]

        self._show_list = df.to_dict(orient='record')
        return self._show_list

    def parse(self):
        assert len(self._table.select('tr')[0].select('th')) == self._NUM_OF_CELLS_IN_A_ROW

        show_list = []

        rowspan_list = [0 for i in range(self._NUM_OF_CELLS_IN_A_ROW)]

        for row in self._table.select('tr')[1:]:
            assert sum(rowspan_list) != 0 or len(row.select('td')) == self._NUM_OF_CELLS_IN_A_ROW
            assert (self._NUM_OF_CELLS_IN_A_ROW - sum([1 for i in rowspan_list if i > 0])) == len(row.select('td'))

            if len(row.select('td')) == self._NUM_OF_CELLS_IN_A_ROW:
                values = []
                for idx, td in enumerate(row.select('td')):
                    values.append((self._headers[idx], td.text.rstrip('\n')))

                    if self._headers[idx] == 'venue':
                        img = row.select_one('img')
                        assert img.has_attr('alt')
                        values.append(('country', img.attrs['alt']))

                    if td.has_attr('rowspan'):
                        assert(rowspan_list[idx] == 0)
                        rowspan_list[idx] = int(td.attrs['rowspan'])

                    if rowspan_list[idx] != 0:
                        rowspan_list[idx] -= 1 

                show_list.append({value[0]:value[1] for value in values})

            else:
                assert show_list
                assert sum(rowspan_list) != 0

                cur_show = copy.deepcopy(show_list[-1])
                #values = []
                offset = 0

                for idx in range(self._NUM_OF_CELLS_IN_A_ROW):
                    if rowspan_list[idx] != 0:
                        rowspan_list[idx] -= 1
                        offset += 1
                    else:
                        td = row.select('td')[idx-offset]
                        cur_show[self._headers[idx]] = td.text.rstrip('\n')

                        if self._headers[idx] == 'venue':
                            img = row.select_one('img')
                            assert img.has_attr('alt')
                            cur_show['country'] = img.attrs['alt']

                        if td.has_attr('rowspan'):
                            assert(rowspan_list[idx] == 0)
                            rowspan_list[idx] = int(td.attrs['rowspan'])

                        if rowspan_list[idx] != 0:
                            rowspan_list[idx] -= 1 

                show_list.append(cur_show)

        self._show_list = show_list
        return show_list

if __name__ == '__main__':
    folder_path = '../ui/static/data'
    file_name = 'babymetal_show_list.json'
    table_name = 'tbl_country_name_ja_to_en.json'

    with open(os.path.join(folder_path, table_name), 'r') as f:
        tbl = json.load(f)

    page = BabymetalWikipediaPage()
    soup = page.get_soup()
    show_tbl = BabymetalShowTable(soup, tbl)
    show_tbl.parse()
    show_list = show_tbl.data_cleaning()

    folder_path = '../ui/static/data'
    file_name = 'babymetal_show_list.json'

    if not os.path.isdir(folder_path):
        os.path.makedirs(folder_path)

    show_tbl.save(os.path.join(folder_path, file_name))
