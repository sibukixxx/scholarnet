# -*- coding:utf-8 -*-
import json
from scholarnet import Scholarnet

# ログインデータの読み込み
with open("profile.json", 'r') as f:
    profile = json.load(f)

# 更新情報の取得
scholar = Scholarnet()
html_top, html_univ = scholar.get_pages(profile)
next_date, updated_date = scholar.get_dates(html_top)

# 返還データの取得
contents = scholar.get_contents(html_univ, profile["type"])

# 結果の表示
print("今回の更新日: %s" % updated_date)
print("次回の更新日: %s" % next_date)
for k,v in contents.items():
    print("%s: %s" % (k,v))

# データの保存
with open("contents_%s.json" % updated_date, 'w') as f:
    json.dump(contents,f,ensure_ascii=False,indent=2)
