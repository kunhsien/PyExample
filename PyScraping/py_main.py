import urllib
from urllib import request
from bs4 import BeautifulSoup # BeautifulSoup 庫使用簡單，適合小量的網站抓取，若是大量網站資訊的抓取可以考慮其他數據抓取框架 Scrapy。
#您可以試試把一些公共應用程序接口 (Application programming interface, API) 整合入您的代碼。
#這個獲取數據的方法遠比網頁抓取高效。舉個例子來說，您可以試試 Facebook Graph API，這個應用程序接口可以幫助您獲取臉書網站上不顯示的隱藏信息。
#如果數據量過大，您可以考慮使用類似 MySQL 的數據庫後端來存儲數據。
import csv
from datetime import datetime



x = urllib.request.urlopen('https://www.google.com');
print(x.read()); #呈現請求後的結果…出現一堆看不懂的資料


try:
    url = 'https://www.google.com.tw/search?q=python';
    #url = 'https://www.google.com.tw/#q=python'; #雖然在google網址上看到搜尋時是這個方式，但是實際操作起來是不成功的
    headers = {};
    headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17';
    #headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0';
    req = urllib.request.Request(url, headers=headers);
    resp = urllib.request.urlopen(req);
    respData = str(resp.read().decode('utf-8')); #將所得的資料解碼
    saveFile = open('withHeaders.txt','w', encoding='utf8');
    saveFile.write(str(respData));
    saveFile.close();
except Exception as e:
    print(str(e));

#Sample 2 Reference : https://buzzorange.com/techorange/2017/08/04/python-scraping/
quote_page = ['http://www.bloomberg.com/quote/SPX:IND', 'http://www.bloomberg.com/quote/CCMP:IND']
data = []
for pg in quote_page:
    page = urllib.request.urlopen(pg) # 檢索網站並返回 HTML 代碼，存入變量’page’
    soup = BeautifulSoup(page, 'html.parser') # 用 beautifulSoup 解析 HTML 代碼並存入變量`soup`
    name_box = soup.find('h1', attrs = {'class': 'name'}) # 獲取“名稱”類的<div> 代碼段落並提取相應值
    name = name_box.text.strip()  # strip() is used to remove starting and trailing
    price_box = soup.find('div', attrs = {'class': 'price'}) # 獲取股指價格數據
    price = price_box.text
    data.append((name, price)) # 用元組類型存儲數據
    with open('index.csv', 'a') as csv_file: # 以“添加”模式打開一個 csv 文件，以保證文件原有信息不被覆蓋
        writer = csv.writer(csv_file) # 以“添加”模式打開一個 csv 文件，以保證文件原有信息不被覆蓋
        for name, price in data: # for 循環
            writer.writerow([name, price, datetime.now()])

#Yahoo stock
quote_page = "http://www.cnyes.com/twstock/profile/2317.html"
page = urllib.request.urlopen(quote_page) # 檢索網站並返回 HTML 代碼，存入變量’page’
soup = BeautifulSoup(page, 'html.parser') # 用 beautifulSoup 解析 HTML 代碼並存入變量`soup`
name_box = soup.find('h1', attrs={'class': 'name'}) # 獲取“名稱”類的<div> 代碼段落並提取相應值
name = name_box.text.strip()
print(str(name))
#// strip() 函數用於去除前後空格
price_box = soup.find('div', attrs={'class': 'price'})
price = price_box.text
print(str(price))


#Scraping for Facebook Reference : http://bhan0507.logdown.com/posts/1406669-python-facebook-api-comments

