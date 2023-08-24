# -*- coding: utf-8 -*-
"""
Created on Mon Oct  1 15:26:31 2018

@author: ANUBHAV
"""

import os 
os.chdir(r"C:\Users\ANUBHAV SHUKLA\Desktop\netflix")
import json
import pandas as pd
import numpy as np
import ast
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
import random
from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq
path="netflix_recom.txt"
#%%
#originals list stored in list "l" only for netflix
url = 'https://www.netflix.com/in/originals'
uClient=uReq(url)
page_html=uClient.read()
uClient.close()
soup2 = BeautifulSoup(page_html,"html.parser")
cont=soup2.findAll("div",{"class":"originals"})
cont1=soup2.findAll("div",{"class":"original-title-wrapper"})
l=[]
j=0
for i in range(len(cont1)):
    try:
        c=cont1[i].findAll("div",{"class":"original-title-container"})
        d=c[0].findAll("a", href=True)
        l.append(d[0]["href"][10:18])
    except:
        a=1
#%%
data=open(path,"r")
msg=data.read()
#print(msg)
msg=ast.literal_eval(msg)
for x in msg:
  #count+=1
  i=np.shape(msg[x])
  msg[x]=np.reshape(msg[x],(i[1],)).tolist()
g=nx.DiGraph(msg)
in_degrees = g.in_degree() # dictionary node:degree
in_values = []
for x in g.in_degree():
  in_values.append(x[1])
values=sorted(set(in_values))
in_hist = [in_values.count(x) for x in values]
matplotlib.pyplot.loglog(values, in_hist)
cc = nx.strongly_connected_components(g)
lc = g.subgraph(cc.__next__())
scc = set(lc.nodes())
scc_node = random.sample(scc, 1)[0]
sp = dict(nx.all_pairs_shortest_path_length(g))

inc = {n for n in g.nodes() if scc_node in sp[n]}
inc -= scc
inc = {n for n in g.nodes() if scc_node in sp[n]}
inc -= scc
outc = set()

for n in scc:
    outc |= set(sp[n].keys())

outc -= scc
tube = set()
out_tendril = set()
in_tendril = set()
other = set()
remainder = set(g.nodes()) - scc - inc - outc
inc_out = set()

for n in inc:
    inc_out |= set(sp[n].keys())
inc_out = inc_out - inc - scc - outc

for n in remainder:
    if n in inc_out:
        if set(sp[n].keys()) & outc:
            tube.add(n)
        else:
            in_tendril.add(n)
    elif set(sp[n].keys()) & outc:
        out_tendril.add(n)
    else:
        other.add(n)
bow_tie = [inc, scc, outc, in_tendril, out_tendril, tube, other]
bow_tie = [100 * len(x)/len(g) for x in bow_tie]
zipped = zip(['inc', 'scc', 'outc', 'in_tendril', 'out_tendril','tube', 'other'], range(7))
c2a = {c: i for c, i in zipped}
bow_tie_dict = {}
for i, c in enumerate([inc, scc, outc, in_tendril, out_tendril, tube, other]):
    for n in c:
        bow_tie_dict[n] = i
prev_bow_tie_dict=None
if prev_bow_tie_dict:
    bow_tie_changes = np.zeros((len(c2a), len(c2a)))
    for n in g:
        bow_tie_changes[prev_bow_tie_dict[n],
                            bow_tie_dict[n]] += 1
    bow_tie_changes /= len(g)
print('SCC :',len(scc),' IN :',len(inc),' OUT :',len(outc),' In Tendril :',len(in_tendril),' Out Tendril :',len(out_tendril),' Tube :',len(tube),' Other :',len(other))
#%%
#page rank calculation in top 10,20,50,100
frac_pr=[]
pr = nx.pagerank(g, alpha=0.9)
top= [k for k in sorted(pr, key=pr.get, reverse=True)]
top_pr_10=top[0:10]
top_pr_20=top[0:20]
top_pr_50=top[0:50]
top_pr_100=top[0:100]
list_pr=[top_pr_10,top_pr_20,top_pr_50,top_pr_100]
for j in list_pr:
    count=0
    for i in j:
        if i in l:
            count+=1
    frac_pr.append(count/len(j))

#plot
x = np.arange(4)
plt.bar(x, height= frac_pr)
plt.xticks(x, ['top_10','top_20','top_50','top_100'])
plt.title('Page Rank')
plt.ylabel('Fraction of Netflix Movies')
plt.show()
#%%
#in degree calculation in top 10,20,50,100
frac_in_degree=[]
in_degree_r=nx.in_degree_centrality(g)
top_in= [k for k in sorted(in_degree_r, key=in_degree_r.get, reverse=True)]
top_in_10=top_in[0:10]
top_in_20=top_in[0:20]
top_in_50=top_in[0:50]
top_in_100=top_in[0:100]
list_in_degree=[top_in_10,top_in_20,top_in_50,top_in_100]
for j in list_in_degree:
    count=0
    for i in j:
        if i in l:
            count+=1
    frac_in_degree.append(count/len(j))

#plot
x = np.arange(4)
plt.bar(x, height= frac_in_degree) 
plt.xticks(x, ['top_10','top_20','top_50','top_100'])
plt.title('In degree Centrality')
plt.ylabel('Fraction of Netflix Movies')
plt.show()
#%%
#ques number 6
#oo is original to original, on is original to non-original, no is non original to non original and nn is non original to non original
count_oo=0
count_on=0
count_nn=0
count_no=0
for i in g:
    if i in l:
        for j in g.neighbors(i):
            if j in l:
                count_oo +=1
            else:
                count_on +=1
    else:
        for j in g.neighbors(i):
            if j in l:
                count_no +=1
            else:
                count_nn +=1
#%%
#ques 4 and 5
netflix_data=pd.read_csv(r'C:\Users\ANUBHAV SHUKLA\Desktop\netflix\kk\netflix.csv')
imdb_data=pd.read_csv(r'C:\Users\ANUBHAV SHUKLA\Desktop\netflix\imdb_imdb\data.tsv', error_bad_lines=False,delimiter='\t')
imdb_rating=pd.read_csv(r'C:\Users\ANUBHAV SHUKLA\Desktop\netflix\imdb_imdb\data_1.tsv', error_bad_lines=False,delimiter='\t')
df = pd.merge(imdb_data[['tconst','originalTitle']],imdb_rating[['tconst','averageRating']],on='tconst', how='left')
testing=netflix_data.join(df.set_index(['originalTitle']), on=['Name'],how='left')
#netflix_data.to_csv('testing1.csv')
testing=testing[~testing['averageRating'].isna()]
testing=testing[~testing['Unnamed: 0'].duplicated(keep='last')]
df_pr=pd.DataFrame.from_dict(pr, orient='index',columns=['page_rank'])
df_pr['Unnamed: 0']=df_pr.index
df_pr['Unnamed: 0']=df_pr['Unnamed: 0'].apply(int)
df_pr['page_rank_int']=df_pr['page_rank'].rank(ascending=False)

df_in_degree=pd.DataFrame.from_dict(in_degree_r, orient='index',columns=['in_degree_centrality'])
df_in_degree['Unnamed: 0']=df_in_degree.index
df_in_degree['Unnamed: 0']=df_in_degree['Unnamed: 0'].apply(int)
df_in_degree['in_degree_rank']=df_in_degree['in_degree_centrality'].rank(ascending=False)

testing['imdb_rank']=testing['averageRating'].rank(ascending=False)
testing=pd.merge(testing,df_pr,on='Unnamed: 0', how='left')
testing=pd.merge(testing,df_in_degree,on='Unnamed: 0', how='left')
testing.to_csv('netflix_all_imdb.csv',index=False)

corr_imdb_pr=testing[['imdb_rank','page_rank_int']].corr(method='spearman')
corr_imdb_indegree=testing[['imdb_rank','in_degree_rank']].corr(method='spearman')
corr_indegree_pr=testing[['in_degree_rank','page_rank_int']].corr(method='spearman')


plt.title('Scatter Plot of IMDB Rank vs Page Rank of Netflix')
plt.scatter(testing['page_rank_int'],testing['imdb_rank'])
plt.ylabel('IMDB Ranking')
plt.xlabel('Page Rank')
plt.show()

plt.title('Scatter Plot of IMDB Rank vs In Degree Centrality Rank of Netflix')
plt.scatter(testing['in_degree_rank'],testing['imdb_rank'])
plt.ylabel('IMDB Ranking')
plt.xlabel('In Degree Rank')
plt.show()

plt.title('Scatter Plot of In Degree Cen. Rank vs Page Rank of Netflix')
plt.scatter(testing['in_degree_rank'],testing['page_rank_int'])
plt.ylabel('In Degree Rank')
plt.xlabel('Page Rank')
plt.show()

#%%
count_scc=0
count_in=0
count_out=0
count_intendril=0
count_outtendril=0
count_tubes=0
count_others=0
for i in l:
    if i in list(scc):
        count_scc+=1
    if i in list(inc):    
        count_in+=1
    if i in list(outc):
        count_out+=1
    if i in list(in_tendril):
        count_intendril+=1
    if i in list(out_tendril):
        count_outtendril+=1
    if i in list(tube):        
        count_tubes+=1
    if i in list(other):        
        count_others+=1
