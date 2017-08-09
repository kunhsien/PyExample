# coding=utf-8

import sys
#import lxml
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import matplotlib.dates as md

def get_input_info():
	stock_id = raw_input("Input stock ID: ")
	
	# collect input into a dictionary and return
	stock_info = stock_id
	return stock_info

def request_data(id):
	# Goodinfo
	session = requests.session()
	header = {"Host":"goodinfo.tw", "Upgrade-Insecure-Requests":"1", "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"}
	payload = {"STOCK_ID":id}
	html = session.get("http://goodinfo.tw/StockInfo/ShowSaleMonChart.asp", headers = header, params = payload)

	header2 = {	"Accept-Encoding":"gzip, deflate",
				"Accept-Language":"zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4",
				"Content-Type":"application/x-www-form-urlencoded",
				"Host":"goodinfo.tw",
				"Origin":"http://goodinfo.tw",
				"Referer":"http://goodinfo.tw/StockInfo/ShowSaleMonChart.asp?STOCK_ID=" + id,
				"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"}
	data = {"STOCK_ID":id, "STEP":"DATA", "CHT-CAT":"10Y"}
	post_url = "http://goodinfo.tw/StockInfo/ShowSaleMonChart.asp?STOCK_ID=" + id + "&STEP=DATA&CHT_CAT=10Y"

	html2 = session.post(post_url, cookies = html.cookies, headers = header2, data = data)

	return html

def get_revenue_per_mon(html):
	element_list = list()

	html.encoding = "utf-8"
	soup = BeautifulSoup(html.text, 'html.parser')
	row_data = soup.find_all('tr', id = True)

	for item in row_data:
		element = item.find_all('td')

		# correct revenue string
		if "," in element[len(element)-2].string:
			revenue_o = element[len(element)-2].string.replace(",", "")
		elif "-" in element[len(element)-2].string:
			revenue_o = 0
		else:
			revenue_o = element[len(element)-2].string

		# struct: [year/month, revenue, price high, price low]
		element_list.append([element[0].string, revenue_o, element[3].string, element[4].string])

	return element_list

def info_for_plot(data, cal_month):
	growth_rate_list = list()
	month_list = list()
	price_high = list()
	price_low = list()
	return_data = dict()
	data_index = 0

	while(data_index + 12 + cal_month <= len(data)):
		sum_revenue = 0
		pre_sum_revenue = 0
		growth_rate = 0
	
		# get month list
		month_list.append(data[data_index][0])

		# check if data exist
		if data[data_index][1] == 0 or data[data_index+12+cal_month-1][1] == 0:
			break

		# calculate revenue growth
		for i in range(cal_month):
			sum_revenue = round(sum_revenue + float(data[data_index+i][1]), 2)
			pre_sum_revenue = round(pre_sum_revenue + float(data[data_index+12+i][1]), 2)

		growth_rate = (sum_revenue - pre_sum_revenue)*100/pre_sum_revenue
		growth_rate_list.append("%.2f" % growth_rate)	

		# get price high
		price_high.append(data[data_index][2])

		# get price low
		price_low.append(data[data_index][3])

		data_index += 1

	return_data = {"date": month_list, "rate": growth_rate_list, "p_high": price_high, "p_low": price_low}

	return return_data

	#return growth_rate_list

def plot_task(id):
	html = request_data(id)
	info = get_revenue_per_mon(html)

	data_short = info_for_plot(info, 3)
	data_long = info_for_plot(info, 12)

	#x1 = range(0, len(data_short["rate"]), 2)
	x2 = range(0, len(data_long["rate"]), 2)
			
	fig, host = plt.subplots()

	plt.xlim(0, len(data_long["rate"])-1)
	plt.xticks(x2, data_long["date"][0::2], rotation=30)
	par1 = host.twinx()

	l1, = host.plot(data_short["rate"], "rs-", label = "3 months")
	l2, = host.plot(data_long["rate"], "bs-", label = "12 months")
	l3, = par1.plot(data_long["p_high"], "y", label = "price high")
	l4, = par1.plot(data_long["p_low"], "c", label = "price low")
	
	lines = [l1, l2, l3, l4]
	host.set_xlabel("year/month")
	host.set_ylabel("rate(%)")
	par1.set_ylabel("price(NT)")
	host.set_title("map")

	legend = plt.legend(lines, [l.get_label() for l in lines], loc = "upper right", shadow = True)

	plt.show()

if __name__ == '__main__':
	id = get_input_info()
	plot_task(id)