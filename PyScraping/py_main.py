import urllib
from urllib import request
from bs4 import BeautifulSoup




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
quote_page = 'http://www.bloomberg.com/quote/SPX:IND'
page = urllib.request.urlopen(quote_page)
soup = BeautifulSoup(page, 'html.parser')
name_box = soup.find('h1', attrs={'class': 'name'})
name = name_box.text.strip()
print(str(name))
# strip() 函數用於去除前後空格
price_box = soup.find('div', attrs={'class': 'price'})
price = price_box.text
print(str(price))


#Scraping for Facebook Reference : http://bhan0507.logdown.com/posts/1406669-python-facebook-api-comments

