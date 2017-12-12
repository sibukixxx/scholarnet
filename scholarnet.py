# -*- coding:utf-8 -*-
import re
import sys
import json
from bs4 import BeautifulSoup
from selenium import webdriver as wd
from selenium.webdriver.support.ui import Select

class Scholarnet:
    css = "#main > div > div > div.content-syosaiJoho > div > div.content-l-syosaiJoho > "
    css += "div.content-l-main-syosaiJoho > table > tbody > tr > td.syosaiJoho-area > div:nth-of-type(1) > "
    css += "div.content-m-main-syosaiJoho > table > tbody > "

    # ページの取得とスクリーンショット
    def get_pages(self,profile):
        print("ログイン中...")
        url = "https://scholar-ps.sas.jasso.go.jp/mypage/login_open.do"
        driver = wd.PhantomJS()
        driver.implicitly_wait(30)
        driver.get(url)

        # ログイン
        try:
            driver.find_element_by_id("login_open_userId").send_keys(profile["id"])
            driver.find_element_by_id("login_open_password").send_keys(profile["pass"])
            driver.find_element_by_id("login_open_login_submit").click()
            # 奨学生番号の入力
            driver.find_element_by_id("syogkseiBgKakunin_open_syogkseiBg1").send_keys(profile["univ"]["num1"])
            select = Select(driver.find_element_by_id("syogkseiBgKakunin_open_syogkseiBg2"))
            select.select_by_visible_text(profile["univ"]["num2"])
            driver.find_element_by_id("syogkseiBgKakunin_open_syogkseiBg3").send_keys(profile["univ"]["num3"])
            driver.find_element_by_id("syogkseiBgKakunin_submit_button").click()
            print("ログイン完了しました.")
        except:
            print("ログインに失敗しました.")
            sys.exit()

        # トップページの取得
        html_top = driver.page_source

        # 詳細ページの取得
        num = "%s%s%s" % (str(profile["univ"]["num1"]), str(profile["univ"]["num2"]), str(profile["univ"]["num3"]))
        element = driver.find_element_by_xpath("//input[@value=%s]" % num)
        element.click()
        html_univ = driver.page_source

        # スクリーンショット
        name = driver.find_element_by_css_selector(self.css + "tr:nth-of-type(3) > td.content-td-syosaiJoho").text
        driver.save_screenshot("%s.png" % name)

        driver.close()
        return html_top, html_univ

    # 更新日の取得
    def get_dates(self, html_top):
        soup = BeautifulSoup(html_top, 'lxml')
        css_information = "#main > div > div > div.content-zentaiGaiyo > div > div.content-l-infomation > div.content-l-main-infomation > div"
        information = soup.select(css_information)
        for i in information:
            if i.prettify().count("次回の更新予定日は"):
                update_info = i.prettify().split("次回の更新予定日は")[1] # この辺スマートじゃない
        pattern = re.compile("\d+"+u"月"+"\d+"+u"日")
        dates = pattern.findall(update_info)
        next_date = dates[0]
        updated_date = dates[1]

        return next_date, updated_date

    # 返済状況の取得
    def get_contents(self, html_univ, type):
        soup = BeautifulSoup(html_univ, 'lxml')
        if type == '2':
            #利子あり
            name  = soup.select_one(self.css + "tr:nth-of-type(3) > td.content-td-syosaiJoho").get_text()
            total = soup.select_one(self.css + "tr:nth-of-type(5) > td.content-td-syosaiJoho").get_text()
            pay   = soup.select_one(self.css + "tr:nth-of-type(11) > td.content-td-syosaiJoho").get_text()
            balance = soup.select_one(self.css + "tr:nth-of-type(14) > td.content-td-syosaiJoho").get_text()
        elif type == '1':
            #利子なし
            name  = soup.select_one(self.css + "tr:nth-of-type(3) > td.content-td-syosaiJoho").get_text()
            total = soup.select_one(self.css + "tr:nth-of-type(6) > td.content-td-syosaiJoho").get_text()
            pay   = soup.select_one(self.css + "tr:nth-of-type(9) > td.content-td-syosaiJoho").get_text()
            balance = soup.select_one(self.css + "tr:nth-of-type(12) > td.content-td-syosaiJoho").get_text()
        else:
            print("profile.jsonで, typeの値を正しく記入してください.")
            sys.exit()

        # 空白と改行の除去
        name  = re.sub('[\n ]', '', name)
        total = re.sub('[\n ]', '', total)
        pay   = re.sub('[\n ]', '', pay)
        balance  = re.sub('[\n ]', '', balance)
        contents = {"学校名":name,"貸与総額":total,"月賦返還額":pay,"月賦返還残額(元金)":balance}
        return contents
