# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 22:54:54 2018

@author: ANUBHAV
"""
countoo=0
counton=0
countnn=0
countno=0
count_oo=0
count_on=0
count_nn=0
count_no=0
#flag_oo=0
#flag_on=0
for i in g:
    if i in l:
        #flag_oo=0
        #flag_on=0
        for j in g.neighbors(i):
            if j in l:
                #flag_oo +=1
                count_oo +=1
            else:
                #flag_on +=1
                count_on +=1
    #if (flag_oo >0):
    #    countoo+=1
    #if flag_on >0:
    #    counton+=1
    else:
        #flag_no=0
        #flag_nn=0
        for j in g.neighbors(i):
            if j in l:
                #flag_no +=1
                count_no +=1
            else:
                #flag_nn +=1
                count_nn +=1
    #if flag_no >0:
    #    countno +=1
    #if flag_nn >0:
    #    countnn +=1
#%%
