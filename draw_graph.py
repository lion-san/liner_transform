
# -*- coding: utf-8 -*-

#import numpy as np
import matplotlib.pyplot as plt
import csv
import sys
import math


display_org = False
display_gps = True


args = sys.argv
f = open(args[1], "r", encoding='utf-8', errors='ignore')
all_num = sum(1 for line in f)
print("row = " + str(all_num))
f.close

t = []
roll = []
pitch = []
yaw = []
direction = []
speed = []
time = []


soho_roll = []
soho_pitch = []
SOHO_K = 0.98
SOHO_C = 18.0

delta = []

#ロールのグラフ作成
def calcAngle():

    f = open(args[1], "r")
    data = csv.reader(f)
    
    prev_t = 0
    count = 0
    

    
    for row in data:
        
        count += 1
        
        #eliminate header
        if count == 1:    
            continue
        
        #経過時間
        dt = int(row[0]) / 1000
        prev_t = dt + prev_t
        t.append(prev_t)
        
        #センサー値の取得
        ax = float(row[1]);
        ay = float(row[2]);
        az = float(row[3]);
        gx = float(row[4]);
        gy = float(row[5]);
        gz = float(row[6]);  
        mx = float(row[7]);
        my = float(row[8]);
        mz = float(row[9]);
        if display_gps:
            direction.append(float(row[10]))
            speed.append(float(row[11]))
            time.append(row[12])
                   
        #ロール角
        if ay == 0.0 and az == 0.0:
            roll.append(math.degrees(math.atan(ax / math.sqrt(0.000000001))))
        else:
            roll.append(math.degrees(math.atan((ax / math.sqrt(pow(ay, 2) + pow(az, 2))))))
            
         #ピッチ角
        if ax == 0.0 and az == 0.0:
            pitch.append(math.degrees(math.atan(ay * -1 / math.sqrt(0.000000001))))
        else:
            pitch.append(math.degrees(math.atan((ay * -1 / math.sqrt(pow(ax, 2) + pow(az, 2))))))
            
        
        #相補フィルター
        if count > 2:
            #effect_accelaration EA
            #vector = math.sqrt(ax*ax + ay*ay + az*az)
            #print(str(ax) + ":" + str(ay) + ":" + str(az) + "===" + str(vector))
            #EA = 1 / math.pow(1 + math.pow(SOHO_C- SOHO_C*vector, 2), 2)

            soho_roll.append(SOHO_K*(soho_roll[count-3]+gx*dt/1000) + (1-SOHO_K)*roll[count-2])
            soho_pitch.append(SOHO_K*(soho_pitch[count-3]+gy*dt/1000) + (1-SOHO_K)*pitch[count-2])
        else:
            #初期化
            soho_roll.append(roll[count-2])
            soho_pitch.append(pitch[count-2]) 
        
            
        #ヨー角
        heading = math.atan2(mx, my)
        
        if (heading < 0) :
             heading = heading + 2 * math.pi
     
        if (heading > 2 * math.pi) :
            heading = heading - 2 * math.pi
     
        heading = heading * 180 / math.pi
        heading = heading + 6.6
     
        #if (heading > 360):
        #    heading = heading - 360
        
        if count >2:                
            delta.append(yaw[count-3] - heading)
        else:
            delta.append(0)
            
        '''
        if count > 2:
            #前回の値より180度以上の場合は、逆連続値とする
            if (yaw[count-3] - heading) < -180:
                heading = heading - 360
            
            elif(yaw[count-3] - heading) > 180:
                heading = heading + 360
        '''
        yaw.append(heading)                     
            
        
    
        #処理進捗の表示
        print(int(data.line_num / all_num * 100))
        
    f.close



#Roll Pitch Yawの計算
calcAngle()

        

#Generate Graph
plt.figure(figsize=(18, 8), dpi=80, facecolor='w', edgecolor='k')
plt.title(args[1])
plt.xlabel("t")
plt.ylabel("[degree]")


plt.subplot(3, 1, 1)
plt.title(args[1])
plt.grid(True)
if display_org:
    plt.plot(t, roll, label="roll")
plt.plot(t, soho_roll, label="soho_roll")
plt.legend()
if display_gps:
    spd = plt.twinx()
    spd.plot(t, speed, label="speed", color="r")
    spd.legend(loc='lower right')

plt.subplot(3, 1, 2)
plt.title(args[1])
plt.grid(True)
if display_org:
    plt.plot(t, pitch, label="pitch")
plt.plot(t, soho_pitch, label="soho_pitch")
plt.legend()
if display_gps:
    spd = plt.twinx()
    spd.plot(t, speed, label="speed", color="r")
    spd.legend(loc='lower right')

plt.subplot(3, 1, 3)
plt.title(args[1])
plt.grid(True)
plt.plot(t, yaw, label="yaw")
if display_gps:
    plt.plot(t, direction, label="direction")
#plt.plot(t, delta, label="delta")
plt.legend()
if display_gps:
    spd = plt.twinx()
    spd.plot(t, speed, label="speed", color="r")
    spd.legend(loc='lower right')

'''
fig = plt.figure(figsize=(18, 5))
ax = fig.add_subplot(1,1,1)
ax.set_title('SPEED')
ax.set_xlabel('time')
ax.set_ylabel('speed(km/h)')
ax.plot(t, speed, label="speed")
plt.legend()
'''
'''Histogram
fig = plt.figure()
ax = fig.add_subplot(1,2,2)
ax.hist(delta, bins=50, range=(10,360))
ax.set_title('first histogram $\mu=100,\ \sigma=15$')
ax.set_xlabel('delta')
ax.set_ylabel('freq')

ax = fig.add_subplot(1,2,1)
ax.hist(delta, bins=50, range=(-360,-10))
ax.set_title('first histogram $\mu=100,\ \sigma=15$')
ax.set_xlabel('delta')
ax.set_ylabel('freq')
End Histogram'''

plt.show()


