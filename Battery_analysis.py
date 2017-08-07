

import re
import sys
import time
import threading
import xlsxwriter
sys.path.insert(0, '..')
import xls_report as xls_report
 
 
index_Volt = 6
index_Cap = 2
indwx_Temp = 10
 
 
 
def parse_value():
    for i in range(1000):
        message = "[battery_check]BATT cap 99 cap_count 0 vol 3981000 vol_count 0 temp 229 temp_count 0 batt_no_count 0 \r\n'"
        s_toke = message
        s_token = re.split(' ', s_toke)
        print(str(s_token))
        Volt_value = s_token[index_Volt]
        Cap_value = s_token[index_Cap]
        Temp_value = s_token[indwx_Temp]
        print("[Battery_analysis] - Volt_value: " + str(Volt_value) + ", Cap_value: " + str(Cap_value) + ", Temp_value: " + str(Temp_value) +"\n")
        for key in range(0,15):
            xls_report.VOLTAGE_QUEUE[key].append(Volt_value)
            xls_report.CAPACITY_QUEUE[key].append(Cap_value)
            xls_report.TEMPERTURE_QUEUE[key].append(Temp_value)
    for key_print in range(0, 15):
        print("KEY" + str(key_print) +" temperture : " + str(xls_report.TEMPERTURE_QUEUE[key_print]) + ".\n")
        print("KEY" + str(key_print) + " capacity : " + str(xls_report.CAPACITY_QUEUE[key_print]) + ".\n")
        print("KEY" + str(key_print) + " voltage : " + str(xls_report.VOLTAGE_QUEUE[key_print]) + ".\n")
    xls_report.battery_queue_finish = True
    xls_report.write_to_excel()


 
 
def main():
    #xls_report.create_xls()
    sendThr = threading.Thread(target=parse_value)
    #addThr = threading.Thread(target=xls_report.check_BattertQueue)
    sendThr.start()
    #addThr.start()
 
if __name__ == '__main__':
    main()
 
