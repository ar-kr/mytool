import pandas as pd
import numpy as np

ifilename = input("input file name : ")
df = pd.read_csv(ifilename, header=None)

ofilename = input("output file name : ")

#新しい配列にダウンサンプリングして格納
npArray = df[::4].values
df1 = pd.DataFrame(npArray)
df1.to_csv(ofilename, header=False)