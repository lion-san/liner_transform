# -*- coding: utf-8 -*-
"""
Spyderエディタ

これは一時的なスクリプトファイルです
"""

import csv
import os
import sys

# データが格納されている作業ディレクトリまでパス指定
#os.chdir("/home/yokoi/python/liner_transform")

args = sys.argv

now_t = 0
save_t = 9
rem_t = 0

save_interval = 100 #ms

prev_row = []
out_row = []

count = 0
index = 0

#Count row num
f = open(args[1], "r")
all_num = sum(1 for line in f)
print("row = " + str(all_num))
f.close


wf = open("out_"+ str(save_interval) + "ms_" + args[1], "w")
header = ['dt', 'ax', 'ay', 'az', 'gx', 'gy', 'gz', 'mx', 'my', 'mz']
csv_writer = csv.writer(wf,  lineterminator='\n')
csv_writer.writerow(header)

rf = open(args[1], "r")
csv_reader = csv.reader(rf, delimiter=",", quotechar='"')


for row in csv_reader:
    
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
    now_t = now_t + float(row[0])

    if now_t < save_interval:
        prev_row = row
        rem_t += float(row[0])
        continue
    else:
        while save_t <= now_t:
            
            if save_t % save_interval == 0:
                out_row.append(str(save_interval))
                index = 1
                while index < 10:
                    
                    delta = save_t - rem_t
                    if now_t - save_t > save_interval:
                        #単位時間(ms)当たりの変化量
                        out_row.append(str(float(prev_row[index]) + (float(row[index]) - float(prev_row[index])) / float(row[0]) * delta ))
                    #間にprev_rowが複数ある場合
                    else:
                        #単位時間(ms)当たりの変化量(はみ出る場合)
                        out_row.append(str(float(prev_row[index]) + (float(row[index]) - float(prev_row[index])) / float(row[0]) * delta))
                    index += 1
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
    
    
