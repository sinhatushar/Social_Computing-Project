# -*- coding: utf-8 -*-
"""
Created on Sun Nov  4 22:15:14 2018

@author: ANUBHAV
"""
import pandas as pd
import os
os.chdir(r'C:\Users\ANUBHAV SHUKLA\Desktop\amazon_prime')
#%%
data_1=pd.read_csv(r'C:\Users\ANUBHAV SHUKLA\Desktop\amazon_prime\imdb_imdb\data_1.tsv', error_bad_lines=False,sep="\t")
data=pd.read_csv(r'C:\Users\ANUBHAV SHUKLA\Desktop\amazon_prime\imdb_imdb\data.tsv', sep="\t")
#%%
data_join=pd.merge(data_1,data,how='inner')
data_join=data_join[['tconst','averageRating','numVotes','primaryTitle','originalTitle']]
prime=pd.read_csv(r'C:\Users\ANUBHAV SHUKLA\Desktop\amazon_prime\prime.csv')
#%%
prime_new=pd.merge(prime,data_join,how='right',left=['Name'],right=['originalTitle'])
