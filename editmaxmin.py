import pandas as pd
import numpy as np

def datedif(idx,listx,idy,listy):
    y = listy.loc[idy].values
    secy = y[3] * 3600 + y[4] * 60 + y[5]
    x = listx.loc[idx].values
    secx = x[3] * 3600 + x[4] * 60 + x[5]
    dif = secy - secx
    if(dif<0):
        dif += 24 * 3600
    return dif

def avg10(maxnorm, center,df):
    sum = 0
    num = 0
    len = maxnorm.size
    if(center > 1):
        for i in range(center-1,0,-1):
            dif = datedif(i+1,df,center+1,df)
            if(dif<=300):
                sum += maxnorm[i+1]
                num += 1
    elif(center == 1):
        dif = datedif(1,df,center+1,df)
        if(dif<=300):
            sum += maxnorm[1]
            num += 1
    if(center!=len):
        for i in range(center,len):
            dif = datedif(center+1,df,i+1,df)
            if(dif<=300):
                sum += maxnorm[i+1]
                num += 1
    elif(center==len):
        sum += maxnorm[len]
        num += 1
    return sum/num

def makeavg60(df):
    maxnorm = df['maxnorm']
    size = df.size
    avgmax = np.array([0]*size)
    for i in range(size):
        avgmax[i] = avg10(maxnorm,i,df)
    return avgmax

fname = input('filename: ')
df = pd.read_csv(fname, index_col=0)
# print(df)

avgmax3 = df['avgmax3']
#print(avgmax3)

#maxnorm = df['maxnorm']
maxnorm = df.query('maxnorm <= 0.1')
#print(maxnorm)


#maxhist = maxnorm['maxnorm'].value_counts(sort = False, bins = 100)
#print(maxhist)

maxnormarr = maxnorm['maxnorm'].values
#print(maxnormarr)
maxnormarr = (maxnormarr * 1000)

#print(maxnormarr)
maxhist = np.array([0]*100)
x = maxnormarr.size

for i in range(x):
    maxhist[int(maxnormarr[i])] += 1

print(maxhist)

mode = maxhist.argmax()
print(mode)

sleepline = mode * 0.002
print(sleepline)

overline = df.query('avgmax3 > ' + str(sleepline+0.005))
overline15 = df.query('avgmax3 > ' + str(sleepline+0.1))
#print(overline)
print('overline15')
#print(overline15)

y = overline['year'].size
startid = np.array([0]*y)
numarr = np.array([0]*y)
overid = overline.index.values
flag = False
k = 0

for i in range(y-1):
    if(flag==False):
        startid[k] = overid[i]
        if(overid[i]+1 == overid[i+1]):
            flag = True
            
            numarr[k] += 1
        else:
            numarr[k] += 1
            k += 1
    else:
        if(overid[i]+1 == overid[i+1]):
            numarr[k] += 1
        else:
            flag = False
            numarr[k] += 1
            k += 1

startid2 = np.trim_zeros(startid,trim='b')
numarr2 = np.trim_zeros(numarr, trim='b')
print(startid2)
print(numarr2) 

a = startid2.size
start = 0

for i in range(a-1):
    dif = datedif(startid2[i]+numarr2[i],df,startid2[i+1],df)
    if(dif > 600):
        sleepid = startid2[i]+numarr2[i]
        print('sleepid:',sleepid)
        print(df.loc[sleepid])
        sleeptime = df.loc[sleepid].values
        start = i+1
        break
    else:
        print('i,dif: ',i,dif)

overline15 = overline15.query('id > ' + str(sleepid))
y = overline15['year'].size
print('y: ',y)
startid15 = np.array([0]*y)
numarr15 = np.array([0]*y)
overid15 = overline15.index.values
flag = False
k = 0

if(y>1):
    for i in range(y-1):
        if(flag==False):
            startid15[k] = overid15[i]
            if(overid15[i]+1 == overid15[i+1]):
                flag = True
            
                numarr15[k] += 1
            else:
                numarr15[k] += 1
                k += 1
        else:
            if(overid15[i]+1 == overid15[i+1]):
                numarr15[k] += 1
            else:
                flag = False
                numarr15[k] += 1
                k += 1
else:
    startid15[0] = overid15[0]
    numarr15[0] = 1

startid152 = np.trim_zeros(startid15,trim='b')
numarr152 = np.trim_zeros(numarr15, trim='b')
print(startid152)
print(numarr152) 

a = startid152.size

print('wakeid:',startid15[a-1])
print(overline15.loc[startid15[a-1]])
waketime = overline15.loc[startid15[a-1]].values
end = a-1

midtimesum = 0
for i in range(end):
    if(numarr15[i]>=3):
        print('mid:',startid15[i])
        print(overline15.loc[startid15[i]])
        midstartid = startid15[i]
        midendid = startid15[i] + numarr15[i] - 1
        midstart = overline15.loc[midstartid]
        midend = overline15.loc[midendid]
        midstartsec = midstart[3] * 3600 + midstart[4] * 60 + midstart[5]
        midendsec = midend[3] * 3600 + midend[4] * 60 + midend[5]
        midtime = midendsec - midstartsec
        if(midtime < 0):
            midtime += 24*3600
        midtimesum += midtime

wakesec = waketime[3] * 3600 + waketime[4] * 60 + waketime[5]
sleepsec = sleeptime[3] * 3600 + sleeptime[4] * 60 + sleeptime[5]
sumtime = wakesec - sleepsec
if(sumtime<0):
    sumtime += 24 * 3600
sleepsum = sumtime - midtimesum
sleepseconds = sleepsum%60
midseconds = midtimesum%60
sleepminutes = ((sleepsum-sleepseconds)/60)%60
midminutes = ((midtimesum-midseconds)/60)%60
sleephour = (sleepsum-(sleepsum%3600))/3600
midhour = (midtimesum-(midtimesum%3600))/3600

print('makeavg: ',makeavg60(df))

print('**********')
print('sleep:',int(sleeptime[0]),int(sleeptime[1]),int(sleeptime[2]),' ',int(sleeptime[3]),int(sleeptime[4]),int(sleeptime[5]))
print('wake:',int(waketime[0]),int(waketime[1]),int(waketime[2]),' ',int(waketime[3]),int(waketime[4]),int(waketime[5]))
print('----------')
print(sleephour,':',sleepminutes,'.',sleepseconds)
print(midhour,':',midminutes,'.',midseconds)

