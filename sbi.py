import requests
from bs4 import BeautifulSoup
import datetime, re
import editcalendar

target_url = "https://www.sbisec.co.jp/ETGate/?OutSide=on&_ControlID=WPLETmgR001Control&_DataStoreID=DSWPLETmgR001Control&burl=search_domestic&dir=ipo%2F&file=stock_info_ipo.html&cat1=domestic&cat2=ipo&getFlg=on&int_pr1=150313_cmn_gnavi:6_dmenu_04"
html = requests.get(target_url)
soup = BeautifulSoup(html.content, "html.parser")

# 会社名取得、配列へ格納
company_list = []
company_dives = soup.find_all('div', class_='thM alL')
company_split = ' '
for div in company_dives:
  # 「（株）hoge  （xxxx）東証グロース」のフォーマット。会社名のみで良いので、会社名以降は除外して格納
    company_name = div.find('p', class_='fl01').text
    idx = company_name.find(company_split)
    splited = company_name[:idx]
    company_list.append(splited)

# ブックビル期間取得、配列へ格納
bookbuild_list = []
# class="tdM"指定は同じテーブル内のclass="tdM alC"の値も取得。子にpタグが存在せず後続でエラーとなるため、完全一致によって取得
bookbuild_dives = soup.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['tdM'])
# 漢字出現位置特定のための正規表現
regex = u'[一-龥]'
for i, div in enumerate(bookbuild_dives):
  if i == 0 or i%4 == 0:
    # テーブル要素は1社につき「ブックビル期間」「発行価格」「申込株数単位」「上場日」。そのうちブックビル期間のみ格納
    # 最短で〜日という情報が載っている場合が存在。期間のみを格納するため、左記は除外
    term = div.find('p', class_='fm01').text
    if re.search(regex, term):
      idx = re.search(regex, term).start()
      end = term[:idx]
      bookbuild_list.append(end)
    else:
      bookbuild_list.append(term)

# Googleカレンダー登録関数に引数として渡すデータの形成
currentDateTime = datetime.datetime.now()
date = currentDateTime.date()
year = date.strftime("%Y")

sbi_list = []
term_split = '〜'
for i, summary in enumerate(company_list):
  # ブックビル期間は「MM/dd HH:mm〜MM/dd HH:mm」の形式
  # 「〜」の前後を取得、開始日時と終了日時を変数へ格納
  term = bookbuild_list[i]
  idx = term.find(term_split)
  start = term[:idx]
  end = term[idx+1:]
  event= {
    # 予定のタイトル(会社名)
    'summary': company_list[i],
    # 予定の開始時刻(ISOフォーマットで指定)
    'start': {
      'dateTime': datetime.datetime.strptime(str(year) + "/" + str(start) + ":00", "%Y/%m/%d %H:%M:%S").isoformat(),
      'timeZone': 'Japan'
    },
    # 予定の終了時刻(ISOフォーマットで指定)
    'end': {
      'dateTime': datetime.datetime.strptime(str(year) + "/" + str(end) + ":00", "%Y/%m/%d %H:%M:%S").isoformat(),
      'timeZone': 'Japan'
    },
  }
  sbi_list.append(event)

# Googleカレンダー登録用関数呼び出し
editcalendar.add_schedule(sbi_list)