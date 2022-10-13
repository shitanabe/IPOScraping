import json
import csv
import os

"""
内部的に使用するファイルを作成・読み込みする
"""
registed_path = "./output/output.json"
companies_path = "./output/companies.csv"

# カレンダー登録済みのデータをjson形式で出力
def create_json(events):
  # 相対パス指定の場合、呼び出し元ファイルの位置に依存するため以下の指定
  with open(registed_path, 'w') as f:
    json.dump(events, f, ensure_ascii=False, indent=4)

# 登録済み会社名一覧をcsv形式で出力
def create_companyCSV(companies):
  f = open(companies_path, 'w')
  writer = csv.writer(f)
  writer.writerow(companies)
  f.close()

# 読み込み対象ファイルの存在確認
# 引数 1=登録済み会社名一覧csv 2=登録済みjson
def check_exist(type):
  target_path = ""
  if type == 1:
    target_path = companies_path
  else:
    target_path = registed_path

  if os.path.exists(target_path):
    return True
  else:
    return False

# 登録済み会社名一覧csvを読み込み
def read_companyCSV():
  csv_file = open(companies_path, "r", encoding="utf_8", errors="", newline="" )
  # リスト形式で取得[['aaa','bbb'],['ccc','ddd']]の形式で取得
  company_list = csv.reader(csv_file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
  return company_list