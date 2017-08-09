# coding=utf-8

import os
import sys
import time
import requests
from bs4 import BeautifulSoup

"""
Description: Global definition
"""
global url, select_date, rank_size, header, session_asp
url = {"foreign":"http://www.cnyes.com/twstock/a_QFII9.aspx", "domestic":"http://www.cnyes.com/twstock/a_IT3.aspx"}
header = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"}
session_asp = requests.session()
select_date = 5
num_rank = 30
current_dir = os.getcwd()
data_dir = current_dir+"\\web_data\\"

"""
Description: Get viewstate, eventvalidation, viewstategenerator, market name and date by requests.get()
"""
def get_needed_info(funds):
	menu_list = list()

	html = session_asp.get(url[funds], headers = header)

	soup = BeautifulSoup(html.text, "html.parser")

	# viewstate and enentvalidation
	viewstate = soup.select("#__VIEWSTATE")[0]["value"]
	eventvalidation = soup.select("#__EVENTVALIDATION")[0]["value"]
	viewstategenerator = soup.select("#__VIEWSTATEGENERATOR")[0]["value"]

	# date list, index "0", "1" select market and else select date
	menu_list_ori = soup.find_all("option")

	for menu in menu_list_ori:
		# get attribute value in option eg. <option value="OTC">, <option value="2016-08-19">
		menu_list.append(menu.attrs["value"])
	
	if funds == "foreign":
		needed_info = {"key": [viewstate, viewstategenerator, eventvalidation], "market": menu_list[0:2], "date":menu_list[2:]}
	else:
		needed_info = {"key": [viewstate, viewstategenerator, eventvalidation], "market": menu_list[0:2], "M_average":menu_list[2:7], "date":menu_list[7:]}

	time.sleep(0.5)
	return needed_info

"""
Description: Transfer whole web information to useful data
"""
def reform_web_data(ori_html):
	soup = BeautifulSoup(ori_html, "html.parser")
	table = soup.find_all("table")
	#print soup.find_all("option")

	buy_table = table[1].find_all("a")#, attrs = {"align":"center"})
	sell_table = table[2].find_all("a")#, attrs = {"align":"center"})
	#print len(table_row)

	for i in range(len(buy_table)):
		buy_table[i] = buy_table[i].string
		sell_table[i] = sell_table[i].string

	re_data_dict = {"buy":buy_table, "sell":sell_table}

	for i in range(0, len(re_data_dict["buy"]), 2):
		re_data_dict["buy"][i] = re_data_dict["buy"][i].replace("\r", "")
		re_data_dict["buy"][i] = re_data_dict["buy"][i].replace("\n", "")
		re_data_dict["buy"][i] = re_data_dict["buy"][i].replace("\t", "")
		re_data_dict["sell"][i] = re_data_dict["sell"][i].replace("\r", "")
		re_data_dict["sell"][i] = re_data_dict["sell"][i].replace("\n", "")
		re_data_dict["sell"][i] = re_data_dict["sell"][i].replace("\t", "")

	return re_data_dict

"""
Description: Get viewstate, viewstategenerator and eventvalidation for OTC market every time you get the wanted date.
"""
def req_market_valid_key(funds, market, key):
	formdata_market = {"__VIEWSTATE":key[0], "__VIEWSTATEGENERATOR":key[1], "__EVENTVALIDATION":key[2], "ctl00$ContentPlaceHolder1$D1":market}
	html_market = session_asp.post(url[funds], headers = header, data = formdata_market)
	soup = BeautifulSoup(html_market.text, "html.parser")

	# viewstate and enentvalidation
	viewstate = soup.select("#__VIEWSTATE")[0]["value"]
	eventvalidation = soup.select("#__EVENTVALIDATION")[0]["value"]
	viewstategenerator = soup.select("#__VIEWSTATEGENERATOR")[0]["value"]
	valid_key = [viewstate, viewstategenerator, eventvalidation]

	time.sleep(0.5)
	return valid_key

"""
Description: Post form data using date to get information with date input.
"""
def req_date_for_data(funds, market, date, key):
	# get correct form data for market
	if market == "TSE":
			formdata_date = {"__VIEWSTATE":key[0], "__VIEWSTATEGENERATOR":key[1], "__EVENTVALIDATION":key[2], "ctl00$ContentPlaceHolder1$D3":date}
	elif market == "OTC":
		formdata_OTC = req_market_valid_key(funds, market, key)
		formdata_date = {"__VIEWSTATE":formdata_OTC[0], "__VIEWSTATEGENERATOR":formdata_OTC[1], "__EVENTVALIDATION":formdata_OTC[2], "ctl00$ContentPlaceHolder1$D3":date}
	
	html_date = session_asp.post(url[funds], headers = header, data = formdata_date)
	html_date.encoding = "utf-8"
	date_reform_data = reform_web_data(html_date.text)

	# save data
	fileout = open(data_dir+funds+"_"+date+"_"+market, "w", encoding = "utf-8")
	fileout.write(html_date.text)
	fileout.close()

	time.sleep(0.5)
	return date_reform_data

"""
Description: Get rank of the other funds.
"""
def get_other_funds(funds, market, date):
	web_info = get_needed_info(funds)

	# check if the date is not the same, return None
	if web_info["date"].count(date) == 0:
		other_data = None
		return other_data
	
	#other_f_name = funds+"_"+web_info["date"][0]+"_"+market
	other_f_name = funds+"_"+date+"_"+market

	if os.path.isfile(data_dir+other_f_name):
		other_data = file_proc(other_f_name)
	else:
		other_data = req_date_for_data(funds, market, date, web_info["key"])

	return other_data

"""
Description: process exist file
"""
def file_proc(file_name):
	filein = open(data_dir+file_name, "r", encoding = "utf-8")
	file_read = filein.read()
	file_return = reform_web_data(file_read)
	filein.close()

	return file_return

"""
Description: main task
"""
def main_proc(funds):
	########## structure of return data ##########
	#{"TSE":{"buy":[0:5][0:60], "sell":[0:5][0:60], "compare_buy":[0:4][0:30], "compare_sell":[0:4][0:30]},
	# "OTC":{"buy":[0:5][0:60], "sell":[0:5][0:60], "compare_buy":[0:4][0:30], "compare_sell":[0:4][0:30]}}
	##############################################
	final_main_data = dict()

	# create directory for web data
	if not os.path.isdir("web_data"):
		os.mkdir("web_data")

	web_info = get_needed_info(funds)

	# get two market, index 0 for TSE, 1 for OTC
	for m in range(2):
		main_data_comb = {"buy":[], "sell":[], "compare_buy":[], "compare_sell":[]}
		compare_other_buy = list()
		compare_other_sell = list()

		# get other funds to compare
		if funds == "foreign":
			other_data_list = get_other_funds("domestic", web_info["market"][m], web_info["date"][0])
		else:
			other_data_list = get_other_funds("foreign", web_info["market"][m], web_info["date"][0])

		# get data for 5 days
		for i in range(select_date):
			# reset temp list
			compare_temp_buy = list()
			compare_temp_sell = list()

			# check if file exist and get data
			if os.path.isfile(data_dir+funds+"_"+web_info["date"][i]+"_"+web_info["market"][m]):
				data_list = file_proc(funds+"_"+web_info["date"][i]+"_"+web_info["market"][m])
			else:
				data_list = req_date_for_data(funds, web_info["market"][m], web_info["date"][i], web_info["key"])

			main_data_comb["buy"].append(data_list["buy"])
			main_data_comb["sell"].append(data_list["sell"])

			# w/o compare first day
			if i == 0:
				continue
				
			# compare with last few days
			for j in range(num_rank):
				# compare buy list
				if main_data_comb["buy"][0][j*2] in data_list["buy"][0::2]:
					compare_temp_buy.append(str(data_list["buy"][0::2].index(main_data_comb["buy"][0][j*2]) + 1))				# +1 for reindex
				elif main_data_comb["buy"][0][j*2] in data_list["sell"][0::2]:
					compare_temp_buy.append("-" + str(data_list["sell"][0::2].index(main_data_comb["buy"][0][j*2]) + 1))		# +1 for reindex
				else:
					compare_temp_buy.append("N/A")

				# compare sell list
				if main_data_comb["sell"][0][j*2] in data_list["sell"][0::2]:
					compare_temp_sell.append("-" + str(data_list["sell"][0::2].index(main_data_comb["sell"][0][j*2]) + 1))				# +1 for reindex
				elif main_data_comb["sell"][0][j*2] in data_list["buy"][0::2]:
					compare_temp_sell.append("+" + str(data_list["buy"][0::2].index(main_data_comb["sell"][0][j*2]) + 1))		# +1 for reindex
				else:
					compare_temp_sell.append("N/A")

				# compare other funds
				if i == select_date-1 and not other_data_list == None:
					# buy
					if main_data_comb["buy"][0][j*2] in other_data_list["buy"][0::2]:
						compare_other_buy.append(str(other_data_list["buy"][0::2].index(main_data_comb["buy"][0][j*2]) + 1))
					elif main_data_comb["buy"][0][j*2] in other_data_list["sell"][0::2]:
						compare_other_buy.append("-" + str(other_data_list["sell"][0::2].index(main_data_comb["buy"][0][j*2]) + 1))
					else:
						compare_other_buy.append("N/A")

					# sell
					if main_data_comb["sell"][0][j*2] in other_data_list["sell"][0::2]:
						compare_other_sell.append("-" + str(other_data_list["sell"][0::2].index(main_data_comb["sell"][0][j*2]) + 1))
					elif main_data_comb["sell"][0][j*2] in other_data_list["buy"][0::2]:
						compare_other_sell.append("+" + str(other_data_list["buy"][0::2].index(main_data_comb["sell"][0][j*2]) + 1))
					else:
						compare_other_sell.append("N/A")
				elif i == select_date-1 and other_data_list == None:
					compare_other_buy.append("-")
					compare_other_sell.append("-")

			#for item in main_data_comb["buy"][0][0::2]:
			#	if item in data_list["buy"][0::2]:
			#		compare_temp.append(str(data_list["buy"][0::2].index(item) + 1))
			#	elif item in data_list["sell"][0::2]:
			#		compare_temp.append("-" + str(data_list["sell"][0::2].index(item) + 1))
			#	else:
			#		compare_temp.append("N/A")

			# combine compare data for last 4 days
			main_data_comb["compare_buy"].append(compare_temp_buy)
			main_data_comb["compare_sell"].append(compare_temp_sell)

		# combine compare data for other funds
		main_data_comb["compare_buy"].append(compare_other_buy)
		main_data_comb["compare_sell"].append(compare_other_sell)

		if m == 0:
			final_main_data["TSE"] = main_data_comb
		else:
			final_main_data["OTC"] = main_data_comb
			
	final_main_data["date"] = web_info["date"]

	#print len(final_main_data["TSE"]["buy"][0])
	#print final_main_data["TSE"]["compare_buy"][0:]
	#print final_main_data["OTC"]["compare_buy"][0:]

	return final_main_data

if __name__ == '__main__':
	main_proc("foreign")
