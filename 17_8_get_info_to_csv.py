import pandas as pd
import requests
import lxml.html
import os
import csv
import pprint

########スキャルピングでテキスト取得
def get_scarping_data(key_page,css_select_str,*URL):
    #取得したURLの個数分の情報を取得する
    for i in range(len(URL)):
        #URLから文字列を取得       
        r = requests.get(URL[i])#URLを指定         
        r.encoding = r.apparent_encoding #文字化けを防止

        #URLが存在するが、テキストがnullだったらスキップする
        if not r.encoding :#nullのとき
            print('r.encoding ウェブページがnullです')
            if  key_page == "horse_race_data" :
                horse_past_data.append("")#行間を開ける　過去成績がない時もあるから
            if  key_page == "jockey_race_data" :
                jockey_past_data.append("")#行間を開ける　過去成績がない時もあるから 
        else:
            html = lxml.html.fromstring(r.text) #取得した文字列データ
        
            # 項目を取得
            for css_id in html.cssselect(css_select_str):        
                #レース結果サイトのレース環境
                if key_page == "condition_in_race_page" :
                    css_id = css_id.text_content()#Element番号のテキスト 
                    css_id_ = css_id.split("\n")
                    css_id_ = css_id.split("/")# ['\n11:50発走 ', ' ダ1300m (右)\n', ' 天候:晴\n', ' 馬場:良\n\n']
                    print('css_id_',css_id_)
                    race_cdt.append(css_id_)#リストに行のデータ(リストを追加)

                #レース結果サイトのレース結果
                if key_page == "result_in_race_page" :
                    css_id = css_id.text_content()#Element番号のテキスト 
                    css_id = css_id.split("\n")#改行("\n")をもとに分割する
                    #内包表記 空の要素を駆逐する　空文字を除く
                    css_id_ = [tag for tag in css_id if tag != '']
                    #1位はタイム記録なし #強引に加える必要がある 8番目に0
                    if len(css_id_) != 14 : css_id_.insert(8,0)
                    rlt.append(css_id_) #リストに行のデータ(リストを追加)
                    
                #レースした馬の過去成績サイト(別サイト)
                if key_page == "horse_race_contents" : 
                    #Element番号のテキスト 
                    css_id = css_id.text_content()
                    print(css_id)                
                    horse_contens.append(css_id) #リストに行のデータ(リストを追加)  

                if  key_page == "horse_race_data" :
                    css_id = css_id.text_content()#Element番号のテキスト 
                    css_id = css_id.split("\n")               
                    #内包表記 空と"\xa0"と"映像"を除去
                    css_id = [tag for tag in css_id 
                    if tag != '' and tag != "\xa0" and tag != "映像" and tag != "厩舎ｺﾒﾝﾄ" and tag != "備考" ]
                    print("css_id",css_id)                 
                    horse_past_data.append(css_id) #リストに行のデータ(リストを追加)

                #レースした馬の過去成績サイト(別サイト)
                if key_page == "jockey_race_contents" : 
                    css_id = css_id.text_content()#Element番号のテキスト 
                    jockey_contens.append(css_id)   #リストに行のデータ(リストを追加)

                if  key_page == "jockey_race_data" :
                    css_id = css_id.text_content()#Element番号のテキスト 
                    #取得したElement番号の
                    css_id = css_id.split("\n")
                    #内包表記 空と"\xa0"と"映像"を除去
                    css_id = [tag for tag in css_id 
                    if tag != '' and tag != "\xa0" and tag != "映像" and tag != "備考" and tag != "ペース"]
                    print("css_id",css_id)                  
                    jockey_past_data.append(css_id)  #リストに行のデータ(リストを追加)
                                
            if  key_page == "horse_race_data" :
                horse_past_data.append("")#行間を開ける　過去成績がない時もあるから
            if  key_page == "jockey_race_data" :
                jockey_past_data.append("")#行間を開ける　過去成績がない時もあるから    

##################################################################

#########レースした馬のURLを取得
def scarping_past_horse_date(URL):            
    response = requests.get(URL)
    root = lxml.html.fromstring(response.content)
    #1~12までの馬の情報を取得
    for i in range(1,18):#2~13  13 - 2 + 1 = 12 
        css_select_str = "table#All_Result_Table tr:nth-child({}) > td:nth-child(4) > span > a".format(i)
        #レースした馬の情報を取得
        for a in root.cssselect(css_select_str):
            horse_URL.append(a.get('href'))
##################################################################

#########レースした騎手のURLを取得
def scarping_past_jockey_date(URL):            
    response = requests.get(URL)
    root = lxml.html.fromstring(response.content)
    #1~12までの馬の情報を取得
    for i in range(1,18):#2~13  13 - 2 + 1 = 12 
        css_select_str = "table#All_Result_Table tr:nth-child({}) > td.Jockey > a".format(i)
        #レースした馬の情報を取得
        for a in root.cssselect(css_select_str):
            jockey_URL.append(a.get('href'))
##################################################################


"""csvファイルを指定"""
url_place = ["30","35","36","42","43","44","45","46","47","48","50","51","54","55"]#会場 14
X = 1
url_place_ = url_place[X]
file_name_ = "URL_2018_" + url_place_ + ".csv"
with open(file_name_) as f:
    reader = csv.reader(f)
    l = [row for row in reader]#もう少し賢い書き方があるはず

#テキストの1行目のURLをそれぞれ分割
url_reader = [row for row in l[0]]#2行目のURLリストを獲得


#取得したURLのサイトからデータを抽出
for num_url in url_reader:

    """URLからフォルダを作成"""
    url_12_ = num_url[-12:] #URLから12桁の情報を抽出
    print(url_12_, num_url)

    main_folder = "race_data_" + url_place_
    if not os.path.exists(main_folder):#ディレクトリがなかったら
        os.mkdir(main_folder)#作成したいフォルダ名を作成
    new_path = main_folder + "/" + url_12_#ディレクトリとフォルダ名
    if not os.path.exists(new_path):#ディレクトリがなかったら
        os.mkdir(new_path)#作成したいフォルダ名を作成

    """URLからレース環境とレース結果の情報を取得"""
    #レース環境とレース結果
    race_cdt, rlt = [], []
    #馬のURLと項目と過去成績
    horse_URL, horse_contens, horse_past_data  = [], [], [""]
    #騎手のURLと項目と過去成績
    jockey_URL, jockey_contens,  jockey_past_data=  [], [], []
    #レース環境を取得し、race_cdtに代入
    get_scarping_data("condition_in_race_page","#Netkeiba_Race_Nar_Result > div.Wrap.fc > div.RaceColumn01 > div > div.RaceMainColumn > div.RaceList_NameBox > div.RaceList_Item02 > div.RaceData01",num_url)
    #レース結果の項目を取得し、rltに代入
    get_scarping_data("result_in_race_page","#All_Result_Table > thead",num_url)
    #レース結果を取得し、rltに代入
    for i in range(1,18):#1から18までの出走馬と仮定する
        get_scarping_data("result_in_race_page","#All_Result_Table > tbody > tr:nth-child({})".format(i), num_url)

    """フォルダにcsvファイルを書き込む"""
    file_name = new_path + "/1_race_data.csv"
    with open(file_name, 'w', newline='',encoding='CP932', errors='ignore') as f: 
        wrt = csv.writer(f)    
        wrt.writerows(race_cdt) #抽出結果の書き込み
        wrt.writerows(rlt) #抽出結果の書き込み  

    """レースした馬のURLを取得"""
    scarping_past_horse_date(num_url)
    print("horse_URL",len(horse_URL))#出走馬12に対し、出力結果は12

    """レースした馬のURLから過去成績を取得"""
    #horse_URLが0だったら、全てスキップする
    if len(horse_URL) != 0 :
 
        #項目(1行分)を取得
        get_scarping_data("horse_race_contents", "div#contents th", num_url)
        horse_contens = [tag for tag in horse_contens 
        if tag != '' and tag != "\xa0" and tag != "映像" and tag != "厩舎ｺﾒﾝﾄ" and tag != "備考"] #and
        horse_contens = horse_contens[15:]#いらない要素を削り取る
        print("horse_contens",horse_contens)
        #項目以外の成績データ
        get_scarping_data("horse_race_data", "#contents > div.db_main_race.fc > div > table > tbody > tr",*horse_URL)

        """フォルダにcsvファイルを書き込む""" 
        file_nasme_horse = new_path + "/2_horse_past_data.csv"
        with open(file_nasme_horse, 'w', newline='',encoding='CP932', errors='ignore') as f:
            wrt = csv.writer(f)
            wrt.writerow(horse_contens) #馬の項目
            wrt.writerows(horse_past_data) #抽出結果の書き込み

        """レースした騎手のURLを取得"""
        scarping_past_jockey_date(num_url)
        print("jockey_URL",len(jockey_URL))#出走馬12に対し、出力結果は12

        """レースした騎手のURLから過去成績を取得"""
        #項目(1行分)を取得
        get_scarping_data("jockey_race_contents", "div#contents_liquid th", jockey_URL[0])
        print("jockey_contens",jockey_contens)
        #項目以外の成績データ
        get_scarping_data("jockey_race_data", "div#contents_liquid tr",*jockey_URL)
        print("horse_past_data",jockey_past_data)

        """フォルダにcsvファイルを書き込む"""
        file_nasme_jockey = new_path + "/3_jockey_past_data.csv"
        with open(file_nasme_jockey, 'w', newline='',encoding='CP932', errors='ignore') as f:
            wrt = csv.writer(f)
            wrt.writerows(jockey_past_data) #馬の項目も入っている抽出結果の書き込み




##URLがそもそも指定されていない騎手が存在した。。。。
#https://narv3.netkeiba.com/race/result.html?race_id=201936042101
#▲塚本涼人	
#https://db.netkeiba.com/jockey/a03db/






"""
URLを取得
取得したURLからフォルダを作成
URLのレース環境を取得
URLのレース結果を取得
フォルダにcsvファイルを書き込む
出場した馬の過去成績を取得
フォルダにcsvに書き込む
出場した騎手の過去成績を取得
フォルダにcsvに書き込む
"""
