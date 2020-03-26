"""日本の地方競馬場15会場
例外　帯広(レース場が直線、アニメ"銀の座時"にも書いてあった)
1  門別競馬場 30 7-12
2  盛岡競馬場 35 7-12
3  水沢競馬場 36 8-11
4  浦和競馬場 42 10-12
5  船橋競馬場 43 8-12
6  大井競馬場 44 12-16
7  川崎競馬場 45 5-14
8  金沢競馬場 46 9-10
9  笠松競馬場 47 8-9
10 名古屋競馬場 48 8-12
11 園田競馬場 50 9-12
12 姫路競馬場 51 7-12
13 高知競馬場 54 9-12
14 佐賀競馬場 55 9-12
http://www.keiba.go.jp/about/guidebook.html
"""

"""URLと数値12桁の意味
https://nar.netkeiba.com/?pid=race&id=p202046032210
2020 46 0322 10 → 年　金沢　月日　レース番号  46→金沢   
https://nar.netkeiba.com/?pid=race&id=p202054032202
2020 54 0322 02 → 年　高知　月日　レース番号　54→高知 
https://nar.netkeiba.com/?pid=race&id=p202036032208
2020 36 0322 08 → 年　高知　月日　レース番号　36→水沢 
https://db.netkeiba.com/race/202055032101　55→佐賀
https://db.netkeiba.com/race/202044031801　44→大井
https://db.netkeiba.com/race/202050031801　50→園田
https://db.netkeiba.com/race/202047031902　47→笠松
https://db.netkeiba.com/race/202043031201　43→船橋
https://db.netkeiba.com/race/202048031202　48→名古屋
https://db.netkeiba.com/race/202045030601　45→川崎
https://db.netkeiba.com/race/202042021701　42→浦和
https://db.netkeiba.com/race/202051020501　51→姫路
https://nar.netkeiba.com/?pid=race&id=p201942100701
https://db.netkeiba.com/race/201930110701　30→門別
https://db.netkeiba.com/race/201935102801　35→盛岡

2020 46 03 22 10 → 年 金沢 月 日 レース番号 
2020 46 03 22 10 → y place m d r
https://nar.netkeiba.com/?pid=race&id=p202042032311&mode=top 競走中止 
https://nar.netkeiba.com/?pid=race&id=p202048032301&mode=top 取消 

新URL　いきなり変わるとは・・・
https://narv3.netkeiba.com/race/result.html?race_id=201948031101
"""

"""
1.URLを作成
2.地方競馬のレース結果サイトURLが存在するかを確認する
3.レースが開催された馬数を取得する
4.レースの出走馬数別に分ける(ニューラルネットワークの入力数のため)
→最後の着順の値と取得できた着順の値をできるかを確認
→cssselectorの取得番号と値が一致するかが条件
5.レースの出走馬数におけるURLを分けてテキストに書き込む

A.とりあえずデータを全て取得しましょ！


"""
import requests
import lxml.html 
import itertools #多重ループ
#itertools.product() 常にすべての組み合わせの回数実行される
import csv #csvファイル
import os

rlt = []#結果
url_ = "https://narv3.netkeiba.com/race/result.html?race_id="

#内包表記
start_y, end_y = 2018, 2020
url_y = [str(i) for i in range(start_y, end_y)]#取得年
start_m, end_m = 1, 13
url_m = [str(i).zfill(2) for i in range(start_m, end_m)]#s.zfill(2) 2桁 12 1, 13
start_d, end_d = 1, 32
url_d = [str(i).zfill(2) for i in range(start_d, end_d)]#s.zfill(2) 2桁 31 1,32
start_r, end_r = 1, 13
url_r = [str(i).zfill(2) for i in range(start_r, end_r)]#s.zfill(2) 2桁 12
url_place = ["30","35","36","42","43","44","45","46","47","48","50","51","54","55"]#会場 14
#url_place = ["44","45","46","47","48","50","51","54","55"]#会場 13
#url_place = ["30"]
bool_loop = True

#フォルダ作成
main_folder_path = "url_folder"#フォルダ名
if not os.path.exists(main_folder_path):#ディレクトリがなかったら
    os.mkdir(main_folder_path)#作成したいフォルダ名を作成
folder_path = main_folder_path + "/get_url_" + str(start_y)#フォルダ名
if not os.path.exists(folder_path):#ディレクトリがなかったら
    os.mkdir(folder_path)#作成したいフォルダ名を作成
folder_path_ = main_folder_path + "/get_url_" + str(start_y + 1)#フォルダ名
if not os.path.exists(folder_path_):#ディレクトリがなかったら
    os.mkdir(folder_path_)#作成したいフォルダ名を作成
# 年 場所 月 日 レース番号
for p in url_place:    
    # 年 月 日
    for y, m, d in itertools.product(url_y, url_m, url_d):
        #レース1Rがなかったら飛ばす
        for r in url_r :
            
            #http://*** 年 場所 月 日 レース
            url = url_ + y + p + m + d + r 

            r = requests.get(url)#URLを指定 
            r.encoding = r.apparent_encoding #文字化けを防止
            html = lxml.html.fromstring(r.text) #取得した文字列データ

            #構成したURLが存在するか確認
            for css_id in html.cssselect("body#Netkeiba_Race_Nar_Result div.Race_Infomation_Box"):
                
                css_id = css_id.text_content()#Element番号のテキスト 
                #print("css_id",css_id)

                #指定文字があるか確認
                if "公開予定です" in css_id :                               
                    print("レース結果はありません", url)
                    bool_loop = False
                    break     

            #レース結果がないため2レース以降はbreak        
            if bool_loop == False:
                bool_loop = True
                break

            #URLを取得　途中でbreakされなかったら
            rlt.append(url) 
            print(len(rlt), url)

    #csvファイル
    csv_name = folder_path + "/URL_" + p + ".csv"
    with open(csv_name, 'w', newline='') as f: 
        wrt = csv.writer(f) 
        wrt.writerow(rlt) #抽出結果の書き込み

    #ファイルを書き込んだら、rltを空箱にする
    rlt = []#結果

