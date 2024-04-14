import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator
path="E:\da_chuang\data\word_TF.csv"
data=pd.read_csv(path)

print(data.head(50))
def time_num():
    plt.figure(figsize=(16,9))
    tempgroup=data.groupby('year').sum('num')
    x=np.arange(2001,2024)
    y=np.array(tempgroup['num'])
    plt.plot(x,y,'ro-',color='#4169E1', alpha=0.8, linewidth=1)

    plt.xticks(np.arange(2001,2024,1),rotation=45)

    plt.xlabel('年份',fontproperties='stsong')
    plt.ylabel('数字化指数(次数)',fontproperties='SimHei')

    plt.savefig("E:\\da_chuang\\time_num.svg")
    plt.show()
    plt.close()
    #print(x)
   # print(y)

#time_num()

def gs_num():
    plt.figure(figsize=(16, 9))
    tempgroup=data.groupby('stock_code').sum('num')
    name_list=list(tempgroup.index)
    for i in range(len(name_list)):
        name_list[i]=f"{name_list[i]:0{6}d}"
        #print(name_list[i])
    x=name_list
    y = list(tempgroup['num'])
    y.sort()
    #print(y)
    fig, ax = plt.subplots()
    ax.bar(x, y, color='#4169E1')
    ax.xaxis.set_visible(False)
    ax.set_ylabel('数字化指数（次数）', fontproperties='SimHei')
    plt.show()  # 显示图形
    plt.savefig("E:\\da_chuang\\gs_num.svg")  # 保存图形
    plt.close()  # 关闭图形
gs_num()