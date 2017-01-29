# -*- coding: utf-8 -*-

#import numpy as np
import matplotlib.pyplot as plt
import csv
import sys
import math

#----------Global 変数--------------
Q_angle = 0.001
Q_bias = 0.003
R_measure = 0.03
angle = 0.0
bias = 0.0
P = [[0, 0],[0, 0]]
#-----------------------------------
def kalmanAngle(newAngle, newRate, dt):
    
    S = 0.0
    K = [0, 0]
    y = 0.0

    P00_temp = 0.0
    P01_temp = 0.0
    
    rate = 0.0
    
    global Q_angle
    global Q_bias
    global R_measure
    global angle
    global bias
    global P
    

    
    #--- execute ---------------------
    
    #step1
    rate = newRate - bias
    angle = angle + dt * rate

    #step2
    P[0][0] = P[0][0] + dt * (dt * P[1][1] - P[0][1] - P[1][0] + Q_angle)
    P[0][1] = P[0][1] - dt * P[1][1]
    P[1][0] = P[1][0] - dt * P[1][1]
    P[1][1] = P[1][1] + Q_bias * dt
    
    #step4
    S = P[0][0] + R_measure
    
    #step5
    K[0] = P[0][0] / S
    K[1] = P[1][0] / S
    
    #step3
    y = newAngle - angle
    
    #step6
    angle = angle + K[0] * y
    bias = bias + K[1] * y
    
    #step7
    P00_temp = P[0][0]
    P01_temp = P[0][1]
    
    P[0][0] = P[0][0] - K[0] * P00_temp
    P[0][1] = P[0][1] - K[0] * P01_temp
    P[1][0] = P[1][0] - K[1] * P00_temp
    P[1][1] = P[1][1] - K[1] * P01_temp

    return angle
#---End Kalmanangle---------------------------

args = sys.argv
f = open(args[1], "r")
all_num = sum(1 for line in f)
print("row = " + str(all_num))
f.close

t = []
roll = []
pitch = []
kalman_roll = []
kalman_pitch = []
soho_roll = []
soho_pitch = []
SOHO_K = 0.98
SOHO_C = 18.0

#ロールのグラフ作成
def drawKalmanRoll():

    f = open(args[1], "r")
    data = csv.reader(f)

    global Q_angle
    global Q_bias
    global R_measure
    global angle
    global bias
    global P
    global kalman_roll
    global roll
    global t
    
    prev_t = 0
    t = []
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
        
        #ロール角
        if ay == 0.0 and az == 0.0:
            roll.append(math.degrees(math.atan(ax / math.sqrt(0.000000001))))
        else:
            roll.append(math.degrees(math.atan((ax / math.sqrt(pow(ay, 2) + pow(az, 2))))))
            
        #カルマンロール角
        if count > 2:
            newRate = gx / 131 #gx  Convert to deg/s
            newAngle =  roll[count-2]
            angle = kalmanAngle(newAngle, newRate, dt)
        else:
            #初期化
            Q_angle = 0.001
            Q_bias = 0.003
            R_measure = 0.03
            P = [[0, 0], [0, 0]]
            angle = roll[count-2]
    
        kalman_roll.append(angle)
        
        
        #相補ロール角
        if count > 2:
            #effect_accelaration EA
            #vector = math.sqrt(ax*ax + ay*ay + az*az)
            #print(str(ax) + ":" + str(ay) + ":" + str(az) + "===" + str(vector))
            #EA = 1 / math.pow(1 + math.pow(SOHO_C- SOHO_C*vector, 2), 2)

            soho_roll.append(SOHO_K*(soho_roll[count-3]+gx*dt/1000) + (1-SOHO_K)*roll[count-2])
        else:
            #初期化
            soho_roll.append(roll[count-2])
        
    
        #処理進捗の表示
        print(int(data.line_num / all_num * 100))
        
    f.close

#ピッチのグラフ作成
def drawKalmanPitch():
    
    f = open(args[1], "r")
    data = csv.reader(f)
    
    global Q_angle
    global Q_bias
    global R_measure
    global angle
    global bias
    global P
    global kalman_pitch
    global pitch
    global t
    
    prev_t = 0
    t = []
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

        #ピッチ角
        if ax == 0.0 and az == 0.0:
            pitch.append(math.degrees(math.atan(ay / math.sqrt(0.000000001))))
        else:
            pitch.append(math.degrees(math.atan((ay / math.sqrt(pow(ax, 2) + pow(az, 2))))))
            
        #カルマンピッチ角
        if count > 2:
            newRate = gy / 131 #gy  Convert to deg/s
            newAngle =  pitch[count-2]
            angle = kalmanAngle(newAngle, newRate, dt)
        else:
            #初期化
            Q_angle = 0.001
            Q_bias = 0.003
            R_measure = 0.03
            P = [[0, 0], [0, 0]]
            angle = pitch[count-2]
    
        kalman_pitch.append(angle)

        
        #相補ロール角
        if count > 2:            
            soho_pitch.append(SOHO_K*(soho_pitch[count-3]+gy*dt/1000) + (1-SOHO_K)*pitch[count-2])
        else:
            #初期化
            soho_pitch.append(pitch[count-2])        

            
        #処理進捗の表示
        print(int(data.line_num / all_num * 100))
 
    f.close
        
drawKalmanRoll()
drawKalmanPitch()

        

#Generate Graph
plt.figure(figsize=(18, 8), dpi=80, facecolor='w', edgecolor='k')
plt.title("data")
plt.xlabel("t")
plt.ylabel("[degree]")


plt.subplot(211)
plt.grid(True)
plt.plot(t, roll, label="roll")
plt.plot(t, kalman_roll, label="kalman_roll")
plt.plot(t, soho_roll, label="soho_roll")
plt.legend()

plt.subplot(212)
plt.grid(True)
plt.plot(t, pitch, label="pitch")
plt.plot(t, kalman_pitch, label="kalman_pitch")
plt.plot(t, soho_pitch, label="soho_pitch")
plt.legend()

plt.show()


