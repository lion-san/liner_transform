# -*- coding: utf-8 -*-
"""
Spyderエディタ

これは一時的なスクリプトファイルです
"""

import csv
import sys

# データが格納されている作業ディレクトリまでパス指定
#os.chdir("/home/yokoi/python/liner_transform")

args = sys.argv

#Count row num
f = open(args[1], "r", encoding='utf-8', errors='ignore')
all_num = sum(1 for line in f)
print("row = " + str(all_num))
f.close

rf = open(args[1], "r", encoding='utf-8', errors='ignore')
csv_reader = csv.reader(rf, delimiter=",", quotechar='"')

count = 0
divide_num = 0
zero_counter = 0
now_writing = False

buf = []

for row in csv_reader:
    
    count += 1
    
    #eliminate header
    if count == 1:    
        continue

    buf.append(row)

    #センサー値の取得
    #ax = float(row[1])
    #ay = float(row[2])
    #az = float(row[3])
    #gx = float(row[4])
    #gy = float(row[5])
    #gz = float(row[6])
    #mx = float(row[7])
    #my = float(row[8])
    #mz = float(row[9])
    #direction   = float(row[10])
    speed       = float(row[11])
    time        = row[12]

    if speed > 5.0:
        zero_counter = 0
        if now_writing == False:
            divide_num += 1
            filename = "sub_" + args[1] + "_" + str(divide_num) + ".csv"
            print(filename)
            wf = open(filename, "w")
            header = ['dt', 'ax', 'ay', 'az', 'gx', 'gy', 'gz', 'mx', 'my', 'mz', 'heading', 'speed', 'time']
            csv_writer = csv.writer(wf,  lineterminator='\n')
            csv_writer.writerow(header)
            now_writing = True
            '''
            #Initial csv
            prev = 100
            c = 0
            for p in buf:
                #seek
                if c < count - prev:
                    c += 1
                    continue
                elif c == count:
                    break
                csv_writer.writerow(p)
                c =+ 1
            '''
            for p in buf:
                csv_writer.writerow(p)
            buf = []


    else:

        if now_writing == True:
            zero_counter += 1
            if zero_counter > 500:
                wf.close
                now_writing = False
                buf = []

    if now_writing:
        i = 0;
        buf_row = []
        while i <= 12:
            buf_row.append(row[i])
            i += 1
        csv_writer.writerow(buf_row)
    
rf.close()
wf.close()
    
    
