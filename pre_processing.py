# -*- coding: utf-8 -*-
"""
Spyderエディタ

これは一時的なスクリプトファイルです
"""

import csv
import os
import sys
import re

# データが格納されている作業ディレクトリまでパス指定
#os.chdir("/home/yokoi/python/liner_transform")

args = sys.argv

now_t = 0
save_t = 9
rem_t = 0

save_interval = 200 #ms

prev_row = []
out_row = []

count = 0
index = 0

#Count row num
f = open(args[1], "r", encoding='utf-8', errors='ignore')
all_num = sum(1 for line in f)
print("row = " + str(all_num))
f.close


wf = open("out_"+ str(save_interval) + "ms_" + args[1], "w")
header = ['dt', 'ax', 'ay', 'az', 'gx', 'gy', 'gz', 'mx', 'my', 'mz', 'heading', 'speed', 'time']
csv_writer = csv.writer(wf,  lineterminator='\n')
csv_writer.writerow(header)

rf = open(args[1], "r", encoding='utf-8', errors='ignore')
print('Now pre-processing')
buf=[]
'''
for hoge in rf:
    tmp = re.sub(r',', "z", hoge)
    tmp = re.sub(r'\.', "x", tmp)
    tmp = re.sub(r'-', "y", tmp)
    tmp = re.sub(r'\W', "", tmp)
    tmp = re.sub(r'x', ".", tmp)
    tmp = re.sub(r'y', "-", tmp)
    tmp = re.sub(r'z', ",", tmp)
    #print(hoge)
    #print(tmp)
    buf.append(tmp)
'''


csv_reader = csv.reader(rf, delimiter=",", quotechar='"')
#csv_reader = csv.reader(buf, delimiter=",", quotechar='"')


speed = 0
heading = 0
time = ""

for row in csv_reader:
    if len(row) == 0:
        continue
    if row[0] == '$GPRMC':
        if len(row) != 13:
            continue
        
        speed = float(row[7]) * 1.852
        heading = row[8]
        time = str(row[1])[0:6]
        
    elif row[0] == '$MOTION':
        
        if len(row) != 11:
            continue

        if count < 2:
            count += 1
            continue
        
        elif count == 2:
            count += 1
            prev_row = row
            #now_t = now_t + int(row[0])
            continue
    #    elif count == 3:
     #       count += 1
      #      rem_t = int(row[0])
    
        #ここから線形補完開始
        now_t = now_t + float(row[1])
    
        if now_t < save_interval:
            prev_row = row
            rem_t += float(row[1])
            continue
        else:
            while save_t <= now_t:
                
                if save_t % save_interval == 0:
                    out_row.append(str(save_interval))
                    index = 2
                    while index < 11:
                        
                        delta = save_t - rem_t
                        if now_t - save_t > save_interval:
                            if prev_row[index] == "":
                                continue
                            if row[index] == "":
                                row[index] = prev_row[index]
                            #単位時間(ms)当たりの変化量
                            out_row.append(str(float(prev_row[index]) + (float(row[index]) - float(prev_row[index])) / float(row[1]) * delta ))

                        #間にprev_rowが複数ある場合
                        else:
                            if prev_row[index] == "":
                                continue
                            if row[index] == "":
                                row[index] = prev_row[index]
                            #単位時間(ms)当たりの変化量(はみ出る場合)
                            out_row.append(str(float(prev_row[index]) + (float(row[index]) - float(prev_row[index])) / float(row[1]) * delta))

                        index += 1
                        
                    out_row.append(heading)
                    out_row.append(speed)
                    out_row.append(time)
                    #print(out_row)
                    csv_writer.writerow(out_row)
                    out_row = []
                save_t += 1
            
            #インターバル分終わったら、はみ出た分だけを記録
            save_t -= 1
            rem_t = save_t % save_interval
            now_t = rem_t
            save_t = 9
            prev_row = row
            
        print(int(csv_reader.line_num / all_num * 100))

    
rf.close()
wf.close()
    
    
