# スカラネットスクショくん
日本学生支援機構の奨学金情報Webサイト  
"スカラネット"
(https://scholar-ps.sas.jasso.go.jp/mypage/)で,  
返済状況に関するページをスクショして保存するというものです。  

## 環境
- Python 3.6
- PhantomJS 2.1.1
- その他必要なPythonのパッケージは, "requirements.txt"を参照

## 使い方
### 1.
次のデータ形式で`profile.json`
を用意します.  
- id,passはスカラネットのIDとパスワードです.
- num1,2,3は奨学生番号("xxx-xx-xxxxxx"の形式)をハイフンで3つに分けたものです.  
- 利子なし(一種)の場合はtypeに"1", 利子付き(二種)の場合は"2"を指定してください.
```
{
"id":"YOURID",
"pass":"YOURPASSWORD",
"univ":{"num1":"111",
        "num2":"22",
        "num3":"333333"},
"type":"2"
}
```

### 2.
必要であれば, Pythonのパッケージをインストールします.  
実行する場合は, pyenv環境などでの作業をお勧めします.

```
$ pip3 install -r requirements.txt
```

### 3.
実行
```
$ python3 main.py
```

### 4.
次のようなメッセージがコンソールに出力され,  
pngファイルがローカルに保存されます.
```
ログイン中...
ログイン完了しました.
今回の更新日: 11月10日
次回の更新日: 12月12日
学校名: バカ田大学
貸与総額: 1,800,000円
月賦返還額: 12,214円
月賦返還残額(元金): 1,401,469円
```
出力内容は, `contents_[日付].json`ファイルとしてJSON形式で保存されます.
