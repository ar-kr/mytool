# -*- coding: utf-8
import numpy as np
import pandas as pd
import sys

line = np.ndarray
array = np.ndarray
i = 0

inputfname = input('入力ファイル名：')

with open(inputfname) as f:
    lines = f.readline()
    array = ([lines.rstrip()])
    #print(array)
    i += 1

    while(i<11):
        lines = f.readline()
        line = ([lines.rstrip()])
        array = np.hstack([array,line])
        #print(line)
        #print(i)
        i += 1

    array6 = array[6]
    widtharr = array6.split()
    width = widtharr[1]
    wid = int(width)
    array7 = array[7]
    heightarr = array7.split()
    height = heightarr[1]
    hei = int(height)

    points = wid * hei
    data = []
    j = 0
    k = 0

    while(j<points):
        lines = f.readline()
        data.append(lines.rstrip())
        #print(j)
        j += 1  

dataarr = np.array(data)
nwid = 10
nhei = hei*wid/10
dataarr2 = dataarr.reshape(nwid,int(nhei))
#print(dataarr2)

"""
command = 'w'
while((command == 'w') or (command == 'h')):
    print('w:行数削除 \nh:列数削除 \nothers:終了')
    command = input()
    if(command == 'w'):
        print('w')
        dele = input('何行削る？>>')
        dele = int(dele)
        tb = 'o'
        while((tb != 't') and (tb != 'b')):
            tb = input('top/bottom? [t/b] : ')
        
        if(tb == 't'):
            dataarr2 = dataarr2[dele:wid,:]
            print(dataarr2.shape)
            wid -= dele
            points = wid * hei
        elif(tb == 'b'):
            dataarr2 = dataarr2[0:(wid-dele),:]
            print(dataarr2.shape)
            wid -= dele
            points = wid * hei


    elif(command == 'h'):
        print('h')
        dele = input('何列削る？>>')
        dele = int(dele)
        tb = 'o'
        while((tb != 't') and (tb != 'b')):
            tb = input('top/bottom? [t/b] : ')

        if(tb == 't'):
            dataarr2 = dataarr2[:,dele:hei]
        elif(tb == 'b'):
            dataarr2 = dataarr2[:,0:(hei-dele)]
            
        print(dataarr2.shape)
        hei -= dele
        points = wid * hei
"""

dataarr2 = dataarr2[0,:]
nwid = hei*wid/100
nhei = 10
dataarr2 = dataarr2.reshape(int(nwid),nhei)
dataarr2 = dataarr2[:,0]
points /= 100
resizedata = dataarr2.reshape(int(points))

array[6] = 'WIDTH ' + str(wid)
array[7] = 'HEIGHT ' + str(hei)
array[9] = 'POINTS ' + str(points)

output = np.hstack([array, resizedata])

addfname = input('出力ファイル名　入力ファイル名の前につける文字 : ')
outfname = addfname + inputfname

#df = pd.DataFrame(array)
#df.to_csv(outfname, sep = "\n", header=None, index=None)
df = pd.DataFrame(output)
df.to_csv(outfname, sep = "\n", header=None, index=None)

