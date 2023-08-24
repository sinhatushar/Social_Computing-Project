# -*- coding: utf-8 -*-
"""
Created on Sat Sep  1 18:24:08 2018

@author: ANUBHAV
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-


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
os.chdir(r'C:\Users\ANUBHAV SHUKLA\Desktop\netflix')
crawled=[]
next_visit=["80115328"]
Stack_Data = {}
base_url = 'https://www.netflix.com/title/'
df = pd.DataFrame(columns = ['Name','Actor', 'Genre','Directors','Maturity','Story-line','Popularity'])# Sequence in which data is stored in the corresponding .csv file
df.to_csv('prime.csv', encoding='utf-8')
json.dump(next_visit,open('netflix_next_visit.txt','w'))
json.dump(list(set(crawled)),open('netflix_visited.txt','w'))
json.dump(Stack_Data, open('netflix_recom.txt','w'))
#%%
def start():
	print('Starting the crawl')
	#The BASE_URL + end_url will be the complete url to the webpage to be crawled.
    
	#To extract the data about the next pages to be visited and the pages those have been visited from the next_visit and visited files respectively
	with open('netflix_visited.txt','r') as jsonfile:
		crawled = json.load(jsonfile)
		jsonfile.close()
	with open('netflix_next_visit.txt','r') as jsonfile:
		next_visit = json.load(jsonfile)
		jsonfile.close()
	df = pd.DataFrame(columns = ['Name','Actor','Directors','Genre','Maturity','Story-line','Popularity']).from_csv('netflix.csv',encoding='utf-8')
	with open('netflix_recom.txt','r') as jsonfile:
		Stack_Data = json.load(jsonfile)
		jsonfile.close()
	page_no=55246
	err_count=0
	def signal_handler(*args):
		print("Exiting after save")
		df.to_csv('netflix.csv', encoding='utf-8')
		json.dump(next_visit,open('netflix_next_visit.txt','w'))
		json.dump(list(set(crawled)),open('netflix_visited.txt','w'))
		json.dump(Stack_Data, open('netflix_recom.txt','w'))
		sys.exit()
	signal.signal(signal.SIGINT,signal_handler)
	try:
		while(len(next_visit)>0):
			end_url = next_visit.pop(0)
			key = end_url
			print(str(page_no)+": "+end_url)
	
			#If the page has already been visited then it should be there in crawled list
			if end_url in crawled:
				json.dump(next_visit,open('netflix_next_visit','w'))
				print("End url is in crawled")
				continue
			Stack_Data[key]=[] #Dictionary to be inserted to the recomendation file
			page_url = base_url + end_url
			try:
				source_code = requests.get(page_url).text
				soup = BeautifulSoup(source_code,'html.parser')
			except Exception as e:
				print(e)
				next_visit.insert(0,end_url)
				json.dump(next_visit,open('netflix_next_visit.txt','w'))
				sleep(25)
				print("Request denied")
				err_count+=1
				if err_count == 10:
					raise Exception("10 continuous requests denied")
				continue
			err_count=0
			#Name Extraction
			try:
				df.loc[key,'Name']=soup.find('h1',{'class':'show-title'}).text
			except:
				continue
            
			#Popularity Extraction
			try:
				df.loc[key,'Popularity']=soup.find('div',{'class':'hook-text'}).text
			except:
				df.loc[key,'Popularity']=""
			
         #Storyline Extraction
			try:
				df.loc[key,'Story-line']=soup.find('p',{'class':'synopsis'}).text
			except:
				df.loc[key,'Story-line']=""
                
			try:
				df.loc[key,'Actor']=soup.find('span',{'class':'actors-list'}).text
			except:
				df.loc[key,'Actor']=""                
			try:
				df.loc[key,'Maturity']=soup.find('span',{'class':'maturity-number'}).text
			except:
				df.loc[key,'Maturity']=""  
			try:
				df.loc[key,'Genre']=soup.find('span',{'class':'genre-list'}).text
			except:
				df.loc[key,'Genre']="" 
			try:
				df.loc[key,'Directors']=soup.find('span',{'class':'director-name more-details-content'}).text
			except:
				df.loc[key,'Directors']=""
			#print(soup.find('div',{'class':'style-scope ytd-metadata-row-renderer'}).find('a').text)
			
			#Director Extraction
			#df.loc[key,'Directors']=soup.find('span',{'class':'director-name more-details-content'}).text

	

			#Related or Recomended videos Extraction
			related_vids=[]
			for rq in soup.find_all('a', {'class' : 'similar-link'}):
				vid_end_url = rq.get('href').split('/')[3]
				related_vids.append(vid_end_url)
				if vid_end_url not in crawled and vid_end_url not in next_visit:
					next_visit.append(vid_end_url) # Next_link to be visited which should be added to the end of the queue
			Stack_Data[key].append(related_vids)
			# print(Stack_Data)
	
			'''
			Dumping the data so as to in any case the crawler stops it can be restarted from where it left. Just make sure that if it happens you have to first 
			save the data in the .csv and recom files because all these are in write mode and we are not getting those data from the source files. While we are
			extracting the data for the visited and next_visit files in the initial phase of this function
			'''
	
			crawled.append(end_url)
			page_no = page_no + 1
			if page_no%10==0:
				df.to_csv('netflix.csv', encoding='utf-8')
				json.dump(next_visit,open('netflix_next_visit.txt','w'))
				json.dump(list(set(crawled)),open('netflix_visited.txt','w'))
				json.dump(Stack_Data, open('netflix_recom.txt','w'))
	except Exception as ee:
		print(ee)
		df.to_csv('netflix.csv', encoding='utf-8')
		json.dump(next_visit,open('netflix_next_visit','w'))
		json.dump(list(set(crawled)),open('netflix_visited.txt','w'))
		json.dump(Stack_Data, open('netflix_recom.txt','w'))
#%%
start()