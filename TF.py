import re
import time

import jieba
import pandas as pd
import os
import requests
from  lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By

word_path="E:\da_chuang\data\word_list.txt"
stop_word_path="E:\da_chuang\data\stopwordlist.txt"
text_path="E:\\da_chuang\data\\2022上市公司年报\\txt\\all_text"
os.chdir(text_path)

#关键词
word_df=pd.read_table(word_path,names=["word"])
word_list=list(word_df['word'])
for i in range(len(word_list)):
    word_list[i]=word_list[i].split(' ')[0]
    jieba.add_word(word_list[i])

#停顿词
with open(stop_word_path, encoding='UTF-8') as stop_word_file:
    stop_word_list = [re.sub(r'\r|\n', '', word) for word in stop_word_file]

print(stop_word_list)
#企业信息
gs_path1="E:\da_chuang\data\公司信息\企业信息1.xlsx"
gs_path2="E:\da_chuang\data\公司信息\企业信息2.xlsx"
gs_dict={}
gs_df=pd.read_excel(gs_path1)
for i in range(len(gs_df)):
    num=gs_df.iloc[i,0].split('.')[0]
    name=gs_df.iloc[i,1]
    gs_dict[num]=name

gs_df=pd.read_excel(gs_path2)
for i in range(len(gs_df)):
    num = gs_df.iloc[i, 0].split('.')[0]
    name = gs_df.iloc[i, 1]
    gs_dict[num] = name

#print(gs_dict,len(gs_dict))


def find_company_name(stock_code):
    option = webdriver.ChromeOptions()
    option.add_experimental_option("detach", True)
    driver=webdriver.Chrome(option)
    url="https://xueqiu.com/"
    driver.get(url)
    input=driver.find_element(By.TAG_NAME,'input')
    input.send_keys(stock_code)
    time.sleep(2)

    input.submit()
    time.sleep(2)

    #模拟登录雪球
    user_name=driver.find_element()


def num_of_word(path):
    with open(path) as f:
        content=f.read()
    for word in stop_word_list:
        content.replace(word,"")
    ans_dict={'num':0}
    word_cut=jieba.cut(content,cut_all=False)
    for word in word_list:
        ans_dict[word]=0

    for word  in  word_cut:
        if word in word_list:
            ans_dict[word]+=1
            ans_dict['num']+=1
    return ans_dict

#name=find_company_name('000001')
#rint(name)

if __name__=='__main__':
    cnt=0
    data_list=[]
    alllen=len(os.listdir())
    for file_name in os.listdir():
        file_part=file_name.split('_')
        num_of_gs=file_part[0]
        year=file_part[1][:4]
        '''
        if num_of_gs in gs_dict:
            newpath=num_of_gs+"_"+year+"_"+gs_dict[num_of_gs]+f'{cnt}'+'.txt'
        else:
            newpath=(num_of_gs+'_'+year+'_'+f'{cnt}' +'.txt')
        cnt+=1
        os.rename(file_name,newpath)
        '''
        tempdict={}
        tempdict['year']=year
        tempdict['stock_code']=num_of_gs
        if num_of_gs in gs_dict:
            worddict= num_of_word(text_path+'\\'+file_name)
            tempdict.update(worddict)
            print(tempdict)
            data_list.append(tempdict)
            #print(year,num_of_gs)
    data=pd.DataFrame(data_list)
    print('done')
    print(data.head())
    data.to_csv('E:\da_chuang\data\word_TF.csv',index=False)
