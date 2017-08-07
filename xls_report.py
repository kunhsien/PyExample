
 
import xlsxwriter
import os
import sys
import re



Title_ADDR = ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1', 'J1', 'K1', 'L1', 'M1', 'N1', 'O1']

CAPACITY_SHEET_ADDR = ['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2', 'J2', 'K2', 'L2', 'M2', 'N2', 'O2']
TEMPERTURE_SHEET_ADDR = ['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2', 'J2', 'K2', 'L2', 'M2', 'N2', 'O2']
VOLTAGE_SHEET_ADDR = ['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2', 'J2', 'K2', 'L2', 'M2', 'N2', 'O2']

battery_queue_finish = True

sheet_is_processing = False
sheet_writing = False




capacity_q0 = []
capacity_q1 = []
capacity_q2 = []
capacity_q3 = []
capacity_q4 = []
capacity_q5 = []
capacity_q6 = []
capacity_q7 = []
capacity_q8 = []
capacity_q9 = []
capacity_q10 = []
capacity_q11 = []
capacity_q12 = []
capacity_q13 = []
capacity_q14 = []
CAPACITY_QUEUE = [capacity_q0, capacity_q1, capacity_q2, capacity_q3, capacity_q4,
                  capacity_q5, capacity_q6, capacity_q7, capacity_q8, capacity_q9,
                  capacity_q10, capacity_q11, capacity_q12, capacity_q13, capacity_q14]
voltage_q0 = []
voltage_q1 = []
voltage_q2 = []
voltage_q3 = []
voltage_q4 = []
voltage_q5 = []
voltage_q6 = []
voltage_q7 = []
voltage_q8 = []
voltage_q9 = []
voltage_q10 = []
voltage_q11 = []
voltage_q12 = []
voltage_q13 = []
voltage_q14 = []
VOLTAGE_QUEUE = [voltage_q0, voltage_q1, voltage_q2, voltage_q3, voltage_q4,
                 voltage_q5, voltage_q6, voltage_q7, voltage_q8, voltage_q9,
                 voltage_q10, voltage_q11, voltage_q12, voltage_q13, voltage_q14]
temp_q0 = []
temp_q1 = []
temp_q2 = []
temp_q3 = []
temp_q4 = []
temp_q5 = []
temp_q6 = []
temp_q7 = []
temp_q8 = []
temp_q9 = []
temp_q10 = []
temp_q11 = []
temp_q12 = []
temp_q13 = []
temp_q14 = []
TEMPERTURE_QUEUE = [temp_q0, temp_q1, temp_q2, temp_q3, temp_q4,
                    temp_q5, temp_q6, temp_q7, temp_q8, temp_q9,
                    temp_q10, temp_q11, temp_q12, temp_q13, temp_q14]

'''
def create_xls():
    WORKBOOK1 = xlsxwriter.Workbook("./Battery_values.xlsx")
    sheet_Capacity = WORKBOOK1.add_worksheet("Capacity")
    sheet_Voltage = WORKBOOK1.add_worksheet("Voltage")
    sheet_Temperture = WORKBOOK1.add_worksheet("Temperture")
    for index_num in range(len(Title_ADDR)):
        sheet_Capacity.write(Title_ADDR[index_num], "Key"+str(index_num))
        sheet_Voltage.write(Title_ADDR[index_num], "Key"+str(index_num))
        sheet_Temperture.write(Title_ADDR[index_num], "Key"+str(index_num))
'''

def GetAndIncrease_Addr(key, sheet_name):
    str_ADDR = ''
    NOW_ADDR = ''
    NEW_ADDR = ''
    if sheet_name == "Capacity":
        NOW_ADDR = CAPACITY_SHEET_ADDR[key]
    elif sheet_name == "Temperture":
        NOW_ADDR = TEMPERTURE_SHEET_ADDR[key]
    elif sheet_name == "Voltage":
        NOW_ADDR = VOLTAGE_SHEET_ADDR[key]

    ADDR_header_temp = NOW_ADDR[0]
    ADDR_header = ADDR_header_temp
    sNOW_ADDR = NOW_ADDR.strip(ADDR_header_temp)

    iNEW_ADDR = int(sNOW_ADDR) + 1
    if sheet_name == "Capacity":
        CAPACITY_SHEET_ADDR[key] = ADDR_header + str(iNEW_ADDR)
    elif sheet_name == "Temperture":
        TEMPERTURE_SHEET_ADDR[key] = ADDR_header + str(iNEW_ADDR)
    elif sheet_name == "Voltage":
        VOLTAGE_SHEET_ADDR[key] = ADDR_header + str(iNEW_ADDR)
    else:
        print("Can't mapping any sheet name.\n")
    print("NOW_ADDR: " + str(NOW_ADDR))
    return NOW_ADDR

 
def write_to_excel():
    #if (battery_queue_finish == True):
        WORKBOOK = xlsxwriter.Workbook("Battery_values.xlsx")
        sheet_Capacity = WORKBOOK.add_worksheet("Capacity")
        sheet_Voltage = WORKBOOK.add_worksheet("Voltage")
        sheet_Temperture = WORKBOOK.add_worksheet("Temperture")
        for index_num in range(len(Title_ADDR)):
            sheet_Capacity.write(Title_ADDR[index_num], "Key" + str(index_num))
            sheet_Voltage.write(Title_ADDR[index_num], "Key" + str(index_num))
            sheet_Temperture.write(Title_ADDR[index_num], "Key" + str(index_num))

        print("[Xls_report] - Write_to_excel: Sheet -  \n")
        for key_index in range(0,15):
            print("Saving Battery information for Key(" +str(key_index)+")...\n")
            for TempQ_index in range(len(TEMPERTURE_QUEUE[key_index])):
                TempAddr = GetAndIncrease_Addr(key_index, 'Temperture')
                print(str(TempAddr))
                sheet_Temperture.write(TempAddr, TEMPERTURE_QUEUE[key_index][TempQ_index])
            for CapaQ_index in range(len(CAPACITY_QUEUE[key_index])):
                CapaAddr = GetAndIncrease_Addr(key_index, 'Capacity')
                sheet_Capacity.write(CapaAddr, CAPACITY_QUEUE[key_index][CapaQ_index])
            for VoltQ_index in range(len(VOLTAGE_QUEUE[key_index])):
                VoltAddr = GetAndIncrease_Addr(key_index, 'Voltage')
                sheet_Voltage.write(VoltAddr, VOLTAGE_QUEUE[key_index][VoltQ_index])
        print("Excel file write end.\n")
    #else:
        #pass
 
'''
def check_BattertQueue():
    #while (test_set.testing == True):
    while True:
        if(sheet_is_processing == False):
            for index_x in range(0, 15):
                if (len(TEMPERTURE_QUEUE[index_x]) != 0):
                    sheet_writing = False
                    print("[Xls_report] - pop_temperture: " + str(TEMPERTURE_QUEUE[index_x][0]))
                    write_to_excel(index_x, 'Temperture', TEMPERTURE_QUEUE[index_x].pop(0))
                else:
                    pass
            for index_y in range(0, 15):
                if (len(CAPACITY_QUEUE[index_y]) != 0):
                    sheet_writing = False
                    print("[Xls_report] - pop_capacity: " + str(CAPACITY_QUEUE[index_y][0]))
                    write_to_excel(index_y, 'Capacity', CAPACITY_QUEUE[index_y].pop(0))
 
                else:
                    pass
            for index_z in range(0, 15):
                if (len(VOLTAGE_QUEUE[index_z]) != 0):
                    sheet_writing = False
                    print("[Xls_report] - pop_voltage: " + str(VOLTAGE_QUEUE[index_z][0]))
                    write_to_excel(index_z, 'Voltage', VOLTAGE_QUEUE[index_z].pop(0))
                else:
                    pass
        else:
            pass
'''