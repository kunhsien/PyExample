# coding=utf-8

from tkinter import *
from tkinter import messagebox
#import tkMessageBox
import traceback
import webbrowser
from functools import partial
import threading
import buyNsell
import price_calculator
import growth_rate

global day_select, rank_select
day_select 	= buyNsell.select_date
rank_select = buyNsell.num_rank
version 	= "V_2.1.1"
global_lock = threading.Lock()
sync_lock 	= threading.Lock()

class GUIDemo(Frame):
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.grid()
		self.createWidgets()

	def createWidgets(self):
		##### button area ###
		self.new = Button(self, text = "成長率圖", height = 2, width = 10, command = partial(self.plot_growth_rate))
		self.new.grid(row = 3, column = 0, rowspan = 2)

		self.new = Button(self, text = "基準買價與複查買價", height = 2, width = 20, command = partial(self.out_text_threading, self.out_text))
		self.new.grid(row = 3, column = 1, rowspan = 2)

		self.new = Button(self, text = "外資買賣超排行", height = 3, width = 20, command = partial(self.out_text_buyNsell_threading, self.out_text_buyNsell, "foreign"))
		self.new.grid(row = 0, column = 2, columnspan = 2, rowspan = 2, padx = 5, pady = 5)

		self.new = Button(self, text = "投信買賣超排行", height = 3, width = 20, command = partial(self.out_text_buyNsell_threading, self.out_text_buyNsell, "domestic"))
		self.new.grid(row = 2, column = 2, columnspan = 2, rowspan = 2, padx = 5, pady = 5)

		# ###### Input area #######
		self.inputText = Label(self, text = "Input Stock ID:")
		self.inputText.grid(row = 0, column = 0)
		self.inputField = Entry(self, width = 15)
		self.inputField.grid(row = 0, column = 1)

		self.inputText1 = Label(self, text = "Expect dividend(default=6.67%):")
		self.inputText1.grid(row = 1, column = 0)
		self.inputField1 = Entry(self, width = 15)
		self.inputField1.grid(row = 1, column = 1)

		self.inputText2 = Label(self, text = "Years to calculate(default=5):")
		self.inputText2.grid(row = 2, column = 0)
		self.inputField2 = Entry(self, width = 15)
		self.inputField2.grid(row = 2, column = 1)

	def callback(self, event):
		u_ID = self.inputField.get()
		url_river = "http://goodinfo.tw/StockInfo/ShowK_ChartFlow.asp?RPT_CAT=PER&STOCK_ID=" + u_ID + "&CHT_CAT=WEEK"
		webbrowser.open_new(url_river)

	def out_text(self):
		sync_lock.acquire()

		revenue_topic = ["年/月", "單月月增", "單月年增", "累積年增"]
		# import data
		u_ID = self.inputField.get()
		u_Year = self.inputField1.get()
		u_dividend = self.inputField2.get()
		
		# notice popout window
		window_p = Toplevel()

		# check input data
		if not self.inputField.get():
			self.proc = Label(window_p, text = "!!!!!!!要輸入股票阿蠢貨!!!!!!!", bd = 10)
			self.proc.grid(row = 0, column = 0, columnspan = 2)
			sync_lock.release()
			return
		if not self.inputField1.get():
			u_Year = "5"
		if not self.inputField2.get():
			u_dividend = "6.67"

		self.proc = Label(window_p, text = "calPrice processing...").grid(row = 0, column = 0)

		# process basic and second price
		try:
			result = price_calculator.start_cal(u_ID, u_Year, u_dividend)
		except:
			self.except_proc(list(sys.exc_info()))
			sync_lock.release()
			return

		# destroy notice popout window
		window_p.destroy()

		# result popout window
		window1 = Toplevel()
		window1.grid()
		window1.title("買價查詢")

		self.displayText_p = Label(window1, text = "Current price: %s" % result["price"][2])
		self.displayText_p.grid(row = 0, column = 0, columnspan = 4)

		self.displayText_p = Label(window1, text = "Basic price: %f" % result["price"][0])
		self.displayText_p.grid(row = 1, column = 0, columnspan = 4)

		self.displayText_p = Label(window1, text = "Second price: %f" % result["price"][1])
		self.displayText_p.grid(row = 2, column = 0, columnspan = 4)

		# list revenue table
		self.displayText_title = Label(window1, text = result["title"])
		self.displayText_title.grid(row = 4, column = 0, columnspan = 4)
		
		for i in range(len(revenue_topic)):
			self.displayText_fix = Label(window1, text = revenue_topic[i])
			self.displayText_fix.grid(row = 5, column = i+0, columnspan = 1)		

		for i in range(6):
            # year/month
			self.displayText3 = Label(window1, text = result["revenue"][i][0])
			self.displayText3.grid(row = i + 6, column = 0, columnspan = 1)

            # data
			for j in range(1,4):
                # check signed
				if result["revenue"][i][j][0] == "-":
					self.displayText2 = Label(window1, text = result["revenue"][i][j])
				else:
					self.displayText2 = Label(window1, text = result["revenue"][i][j], bg = "red")
				self.displayText2.grid(row = i + 6, column = j + 0, columnspan = 1)
				
		# 河流圖超連結
		self.hyperlink = Label(window1, text = "河流圖在這裡", fg="blue", cursor="hand2")
		self.hyperlink.grid(row = 3, column = 0, columnspan = 4)
		self.hyperlink.bind("<Button-1>", self.callback)
		sync_lock.release()

	def out_text_threading(self, call):
		threading.Thread(target = call).start()

	# put select stock into inputfield
	def price_callback(self, s_id, redu):
		# remove last value
		while(self.inputField.get()):
			self.inputField.delete(0)
		self.inputField.insert(0, s_id)

	def except_proc(self, message):
		#show_msg = "=============== Please try again ===============\n" + str(message[0]) + str(message[1]) + str(message[2])
		err_callstack = traceback.format_exc()
		messagebox.showerror("Error", err_callstack)

	def out_text_buyNsell(self, F_or_D):
		global_lock.acquire()

		# notice popout window
		window_p = Toplevel()
		self.proc = Label(window_p, text = "bNs processing...").grid(row = 0, column = 0)

		try:
			all_data = buyNsell.main_proc(F_or_D)
		except:
			self.except_proc(list(sys.exc_info()))
			window_p.destroy()
			global_lock.release()
			return
		# destroy notice popout window
		window_p.destroy()

		# result popout window, window1 for 集中市場, window2 for 店頭市場
		window1 = Toplevel()
		window2 = Toplevel()
		window1.grid()
		window2.grid()

		if F_or_D == "foreign":
			window1.title("外資買賣超列表_集中市場")
			self.label = Label(window1, text = "外資買超").grid(row = 0, column = 0, columnspan = day_select+1)
			self.label = Label(window1, text = "本日排行").grid(row = 1, column = 0)
			self.label = Label(window1, text = "外資賣超").grid(row = 0, column = 0 + day_select+1, columnspan = day_select+1)
			self.label = Label(window1, text = "本日排行").grid(row = 1, column = 0 + day_select+1)

			for index in range(day_select):
				if index < (day_select-1):
					self.label = Label(window1, text = all_data["date"][index+1]).grid(row = 1, column = index+1)
					self.label = Label(window1, text = all_data["date"][index+1]).grid(row = 1, column = index+1 + day_select+1)
				else:
					self.label = Label(window1, text = "    投信    ").grid(row = 1, column = index+1)
					self.label = Label(window1, text = "    投信    ").grid(row = 1, column = index+1 + day_select+1)

			window2.title("外資買賣超列表_店頭市場")
			self.label = Label(window2, text = "外資買超").grid(row = 0, column = 0, columnspan = day_select+1)
			self.label = Label(window2, text = "本日排行").grid(row = 1, column = 0)
			self.label = Label(window2, text = "外資賣超").grid(row = 0, column = 0 + day_select+1, columnspan = day_select+1)
			self.label = Label(window2, text = "本日排行").grid(row = 1, column = 0 + day_select+1)

			for index in range(day_select):
				if index < (day_select-1):
					self.label = Label(window2, text = all_data["date"][index+1]).grid(row = 1, column = index+1)
					self.label = Label(window2, text = all_data["date"][index+1]).grid(row = 1, column = index+1 + day_select+1)
				else:
					self.label = Label(window2, text = "    投信    ").grid(row = 1, column = index+1)
					self.label = Label(window2, text = "    投信    ").grid(row = 1, column = index+1 + day_select+1)

		else:
			window1.title("投信買賣超列表_集中市場")
			self.label = Label(window1, text = "投信買超").grid(row = 0, column = 0, columnspan = day_select+1)
			self.label = Label(window1, text = "本日排行").grid(row = 1, column = 0)
			self.label = Label(window1, text = "投信賣超").grid(row = 0, column = 0 + day_select+1, columnspan = day_select+1)
			self.label = Label(window1, text = "本日排行").grid(row = 1, column = 0 + day_select+1)

			for index in range(day_select):
				if index < (day_select-1):
					self.label = Label(window1, text = all_data["date"][index+1]).grid(row = 1, column = index+1)
					self.label = Label(window1, text = all_data["date"][index+1]).grid(row = 1, column = index+1 + day_select+1)
				else:
					self.label = Label(window1, text = "    外資    ").grid(row = 1, column = index+1)
					self.label = Label(window1, text = "    外資    ").grid(row = 1, column = index+1 + day_select+1)

			window2.title("投信買賣超列表_店頭市場")
			self.label = Label(window2, text = "投信買超").grid(row = 0, column = 0, columnspan = day_select+1)
			self.label = Label(window2, text = "本日排行").grid(row = 1, column = 0)
			self.label = Label(window2, text = "投信賣超").grid(row = 0, column = 0 + day_select+1, columnspan = day_select+1)
			self.label = Label(window2, text = "本日排行").grid(row = 1, column = 0 + day_select+1)

			for index in range(day_select):
				if index < (day_select-1):
					self.label = Label(window2, text = all_data["date"][index+1]).grid(row = 1, column = index+1)
					self.label = Label(window2, text = all_data["date"][index+1]).grid(row = 1, column = index+1 + day_select+1)
				else:
					self.label = Label(window2, text = "    外資    ").grid(row = 1, column = index+1)
					self.label = Label(window2, text = "    外資    ").grid(row = 1, column = index+1 + day_select+1)

		# display buy and sell list on window1
		self.bNs_result_display(all_data["TSE"], window1)

		# display buy and sell list on window2
		self.bNs_result_display(all_data["OTC"], window2)
		
		global_lock.release()

	def bNs_result_display(self, fund, window):
		for row_t in range(rank_select):
			#self.data1 = Button(window1, text = all_data["TSE"]["buy"][0][row_t*2]+" "+all_data["TSE"]["buy"][0][row_t*2+1], command = partial(self.price_callback, all_data["TSE"]["buy"][0][row_t*2])).grid(row = row_t+2, column = 0)
			self.data1 = Label(window, text = fund["buy"][0][row_t*2]+" "+fund["buy"][0][row_t*2+1])
			self.data1.grid(row = row_t+2, column = 0)
			self.data1.bind("<Button-1>", partial(self.price_callback, fund["buy"][0][row_t*2]))
			#self.data1 = Button(window1, text = all_data["TSE"]["sell"][0][row_t*2]+" "+all_data["TSE"]["sell"][0][row_t*2+1], command = partial(self.price_callback, all_data["TSE"]["sell"][0][row_t*2])).grid(row = row_t+2, column = 0 + day_select+1)
			self.data1 = Label(window, text = fund["sell"][0][row_t*2]+" "+fund["sell"][0][row_t*2+1])
			self.data1.grid(row = row_t+2, column = 0 + day_select+1)
			self.data1.bind("<Button-1>", partial(self.price_callback, fund["sell"][0][row_t*2]))

			for column_t in range(day_select):
				if not (fund["compare_buy"][column_t][row_t][0] == "-" or fund["compare_buy"][column_t][row_t] == "N/A"):
					self.data2 = Label(window, text = fund["compare_buy"][column_t][row_t], bg = "red").grid(row = row_t+2, column = column_t+1)
				else:
					self.data2 = Label(window, text = fund["compare_buy"][column_t][row_t]).grid(row = row_t+2, column = column_t+1)

				if fund["compare_sell"][column_t][row_t][0] == "-":
					self.data2 = Label(window, text = fund["compare_sell"][column_t][row_t], bg = "green").grid(row = row_t+2, column = column_t + day_select+1+1)
				else:
					self.data2 = Label(window, text = fund["compare_sell"][column_t][row_t]).grid(row = row_t+2, column = column_t + day_select+1+1)


	def out_text_buyNsell_threading(self, call, arg1):
		bNs_thread = threading.Thread(target = call, args = (arg1,))
		bNs_thread.start()

	def plot_growth_rate(self):
		sync_lock.acquire()
		# import data
		if not self.inputField.get():
			return

		try:
			u_ID = self.inputField.get()
			growth_rate.plot_task(u_ID)
		except:
			self.except_proc(list(sys.exc_info()))
			sync_lock.release()
			return
		sync_lock.release()

	"""
	### pyplot must in the tkinter main thread, can not threading ###
	def plot_growth_rate_threading(self, call):
		threading.Thread(target = call).start()
	"""

if __name__ == '__main__':
    root = Tk()
    app = GUIDemo(master=root)
    app.master.title("定存股查詢兼買賣超列表 - [LiLi, %s]" % version)
    app.mainloop()
