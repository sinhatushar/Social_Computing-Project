# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 00:41:29 2018

@author: ANUBHAV
"""

import requests
from bs4 import BeautifulSoup
import operator
import os
import sys
#from queue import Queue
import pandas as pd
import sys
from time import sleep
import json
import signal
from urllib.request import urlopen as uReq
import os
os.chdir(r'C:\Users\ANUBHAV SHUKLA\Desktop\amazon_prime')
#url =r"https://www.amazon.com/s/ref=atv_me_ori_c_FJt44Q_2?field-is_prime_benefit=2470955011&node=2858778011%2C%213147522011%2C%213147524011%2C16549083011&lo=grid&bbn=16549083011&search-alias=instant-video"
#page_html=open()
#%%
f = open('source_code.txt','r')
page_html = f.read()
print(page_html)
f.close()

soup = BeautifulSoup(page_html,'html.parser')
cont1=soup.findAll("li")#,{"class":"DigitalVideoWebNodeStorefront_Card__CardWrapper dv-universal-hover-enabled"})
#cont1=soup2.findAll("div",{"class":"original-title-wrapper"})
l=[]
j=0
#%%
for i in range(len(cont1)):
    try:
        c=cont1[i].findAll("div",{"class":"original-title-container"})
        d=c[0].findAll("a", href=True)
        l.append(d[0]["href"][10:18])
    except:
        a=1