# coding=utf-8

import sys
#import lxml
import requests
from bs4 import BeautifulSoup

def get_input_info():
	stock_id = raw_input("Input stock ID: ")
	total_year = raw_input("Input the number of years: ")
	expect_dividend = raw_input("Input default dividend value: ")
	
	# collect input into a dictionary and return
	stock_info = {"id":stock_id, "count_year":total_year, "exp_dividend":expect_dividend}
	return stock_info

def get_table(id):
	# Goodinfo for dividend
	payload = {"STOCK_ID":id}
	header = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"}
	html_dividend = requests.get("http://goodinfo.tw/StockInfo/StockDividendPolicy.asp", params = payload, headers = header)

	html_dividend.encoding = "utf-8"
	#soup = BeautifulSoup(html.text,'lxml')                   # avoid parser error in .exe
	soup = BeautifulSoup(html_dividend.text, 'html.parser')
	table_dividend = soup.find_all('table', attrs={"border":"0", "cellpadding":"0", "cellspacing":"0"})
	
	# HiStock for EPR and revenue
	Hi_URL_EPR = "http://histock.tw/stock/financial.aspx?no="+id+"&t=6"
	html_EPR = requests.get(Hi_URL_EPR)
	Hi_URL_revenue = "http://histock.tw/stock/financial.aspx?no="+id
	html_revenue = requests.get(Hi_URL_revenue)
	
	html_EPR.encoding = "utf-8"
	#soup = BeautifulSoup(html.text,'lxml')                   # avoid parser error in .exe
	soup = BeautifulSoup(html_EPR.text, 'html.parser')
	table_EPR = soup.find_all('table', attrs={"class":"tb-stock tb-outline", "cellspacing":"2"})
	
	html_revenue.encoding = "utf-8"
	#soup = BeautifulSoup(html.text,'lxml')                   # avoid parser error in .exe
	soup = BeautifulSoup(html_revenue.text, 'html.parser')
	table_revenue = soup.find_all('table', attrs={"class":"tb-stock text-center"})
	revenue_title = soup.title.string               # get stock revenue title

	# Yahoo for EPS, need user-agent headers
	headers_Y = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"}
	Ya_URL = "https://tw.stock.yahoo.com/d/s/company_"+id+".html"
	html_EPS = requests.get(Ya_URL, headers = headers_Y)
	
	#soup = BeautifulSoup(html.text,'lxml')                   # avoid parser error in .exe
	soup = BeautifulSoup(html_EPS.text, 'html.parser')
	table_EPS = soup.find_all("table", attrs={"width":"630", "border":"0", "cellspacing":"1", "cellpadding":"4"})
	
	# combine found table into dictionary
	table_t = {"Stock_title":revenue_title,"G_dividend":table_dividend, "H_PER":table_EPR, "H_revenue":table_revenue, "Y_EPS":table_EPS}

	return table_t

def get_current_price_G(table):
	if not table:
		return "Error"

	# get current price
	current_price_t = table[2].find_all('tr', attrs={"align":"center", "bgcolor":"white", "height":"24px"})
	current_price = current_price_t[0].find("td").string
	
	return current_price
	
def get_dividend_G(table, count_year, default_divi):
	sum_dividend_float = 0.00
	average_dividend_float = 0.00
	element_dividend = list()
	element_table = list()

	# sheck stock id valid or not
	if not table:
		return "Error"
		#sys.exit()

	########## reformat the table ##########

	# get wanted row data(表格內數據, table index "5") in table
	rows_dividend = table[5].find_all("tr", attrs={"align":"center", "height":"23px"})
	
	# check read column
	read_col = 5 if (rows_dividend[4].find_all("td"))[7].string == '-' else 4

	# get wanted element(年度與殖利率) into a element_table(list)
	for y in range(int(count_year)):
		element_table = rows_dividend[y + read_col].find_all("td")
		sum_dividend_float += float(element_table[7].string)

	########## end of reformat ##########

	average_dividend_float = sum_dividend_float / int(count_year)

	return average_dividend_float

def get_PER_H(table):
	element_table = list()
	element_PER = list()
	
	# sheck stock id valid or not
	if not table:
		return "Error"
		#sys.exit()

	########## reformat the table ##########

	rows = table[0].find_all("tr")
	del rows[0]
	
	# get wanted element(本益比) into a element_table(list)
	for item in rows:
		element_table = item.find_all("td", attrs={"style":"width:50px;"})

		for i in range(int(len(item)/2)):
			element_PER.append(float(element_table[i].string))
	
	# delete oldest 5 months, total 60 months
	del element_PER[64:45:-5]

	########## end of reformat ##########

	return sum(element_PER) / len(element_PER)

def get_revenue_H(table):
	element_table = list()
	element_revenue = list()

	# sheck stock id valid or not
	if not table:
		return "Error"

	rows = table[0].find_all("tr")
	element_table = rows[3].find_all("td")
	
	# 
	for i in range(6):
		element_revenue.append([str(element_table[i*8].string),
								str(element_table[i*8+3].string),
								str(element_table[i*8+4].string),
								str(element_table[i*8+7].string)])

	return element_revenue

def get_EPS_Y(table):
	element_table = list()
	element_EPS = list()
	element_EPS_data = list()

	# sheck stock id valid or not
	if not table:
		return "Error"
		#sys.exit()

	########## reformat the table ##########

	rows = table[0].find_all("tr", attrs={"bgcolor":"#FFFFFF"})

	# get first 4 row
	for i in range(len(rows)-1):
		element_table = rows[i].find_all("td", attrs={"align":"center"})
		#element_EPS.append(str(element_table[1].string.encode("utf8")))
		element_EPS.append(element_table[1].string)

	# print (element_EPS)
	# delete 元 in each element
	for i in range(len(element_EPS)):
		element_EPS_data.append(float(element_EPS[i][0:3]))

	########## end of reformat ##########

	return sum(element_EPS_data)

def start_cal(id, year, dividend):
	table_dict = get_table(id)
	average_dividend = get_dividend_G(table_dict["G_dividend"], year, dividend)
	average_PER = get_PER_H(table_dict["H_PER"])
	sum_EPS = get_EPS_Y(table_dict["Y_EPS"])
	revenue_table = get_revenue_H(table_dict["H_revenue"])
	curr_price = get_current_price_G(table_dict["G_dividend"])
	
	# check function return
	if average_dividend == "Error":
		basic_price = "!!!!!Table not found in Goodinfo!!!!!"
	else:
		basic_price = 100.00 / float(dividend) * average_dividend
	
	if average_PER == "Error" or sum_EPS == "Error":
		second_price = "!!!!!Table not found in HiStock or Yahoo!!!!!"
	else:
		second_price = average_PER * sum_EPS
	
	#price = [str(basic_price), str(second_price)]
	cal_result = dict({"price":[basic_price, second_price, curr_price], "revenue":revenue_table, "title":table_dict["Stock_title"]})

	#print "Current price: ", cal_result["price"][2]
	#print "Basic price: ", cal_result["price"][0]
	#print "Second price:", cal_result["price"][1]
	#print cal_result["title"]
	#print cal_result["revenue"]
	return cal_result

if __name__ == '__main__':
	while True:
		info_stock = get_input_info()
		start_cal(info_stock["id"], info_stock["count_year"], info_stock["exp_dividend"])
