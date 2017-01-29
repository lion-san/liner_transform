# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 15:17:32 2017

@author: yokoi
"""
import pandas as pd
import csv
import sys




args = sys.argv

gps = pd.read_csv(args[2], header=None)

f = open(args[1], "r")
all_num = sum(1 for line in f)
print("row = " + str(all_num))
f.close
csv_reader = csv.reader(open(args[1], "r"), delimiter=",", quotechar='"')

header = ['dt', 'ax', 'ay', 'az', 'gx', 'gy', 'gz', 'mx', 'my', 'mz', 'heading', 'speed']
csv_writer = csv.writer(open("gps_"+ args[1], "w"),  lineterminator='\n')
csv_writer.writerow(header)

count = 0
prev_time = 0
out_row = []
proceed_time = 0

for key, row in gps.iterrows():
    if(count == 0):
         prev_time = pd.to_datetime(row[0])
         count += 1
         continue
    
    delta = (pd.to_datetime(row[0]) - prev_time).total_seconds()
    print(delta)
    prev_time = pd.to_datetime(row[0])
    

    
    time_counter = 0
    time_seeker = 0
    for csv_row in csv_reader:
        if csv_reader.line_num <= 1:
            continue
        
        if all_num * 10 <= proceed_time*1000:
            break
        
        while time_seeker < proceed_time*1000:
            time_seeker += int(csv_row[0])
            continue
        
        if time_counter <  delta*1000:        
            index = 0
            while index < 10:
                out_row.append(csv_row[index])
                index += 1
            out_row.append(row[4]) #heading
            out_row.append(row[3]) #speed
            csv_writer.writerow(out_row)
        else:
            break;
        time_counter += int(csv_row[0])
    
            
    proceed_time += delta
    

#gps.head()