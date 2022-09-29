import requests
from bs4 import BeautifulSoup
import re

target_url = "https://www.sbisec.co.jp/ETGate/?OutSide=on&_ControlID=WPLETmgR001Control&_DataStoreID=DSWPLETmgR001Control&burl=search_domestic&dir=ipo%2F&file=stock_info_ipo.html&cat1=domestic&cat2=ipo&getFlg=on&int_pr1=150313_cmn_gnavi:6_dmenu_04"
html = requests.get(target_url)
soup = BeautifulSoup(html.content, "html.parser")

# 会社名取得、配列へ格納。
company_list = []
company_dives = soup.find_all('div', class_='thM alL')
for div in company_dives:
    company_name = div.find('p', class_='fl01').text
    company_list.append(company_name)

# ブックビル期間取得、配列へ格納。
bookbuild_list = []
# class="tdM"指定は同じテーブル内のclass="tdM alC"の値も取得。子にpタグが存在せず後続でエラーとなるため、完全一致によって取得。
bookbuild_dives = soup.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['tdM'])
for i, div in enumerate(bookbuild_dives):
  if i == 0 or i%4 == 0:
    # テーブル要素は1社につき「ブックビル期間」「発行価格」「申込株数単位」「上場日」。そのうちブックビル期間のみ格納。
    bookbuild_list.append(div.find('p', class_='fm01').text)

for name in company_list:
  print(name)
print("=================================")

for term in bookbuild_list:
  print(term)