# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 16:20:28 2018

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
os.chdir(r'C:\Users\ANUBHAV SHUKLA\Desktop\amazon_prime')
Stack_Data = {}
crawled=[]
next_visit=["0RZG6XRLLQ2SMTSFU8FG9YB6UV"]
base_url = 'https://www.primevideo.com/detail/'
#base_url2 = 'https://en.wikipedia.org/wiki/'
df = pd.DataFrame(columns = ['Key','Name','Actor', 'Genre','Directors','Maturity','Story-line','Popularity','Production','Distributed_by','imdb','Time'])# Sequence in which data is stored in the corresponding .csv file
df.to_csv('prime.csv', encoding='utf-8')
json.dump(next_visit,open('prime_next_visit.txt','w'))
json.dump(list(set(crawled)),open('prime_visited.txt','w'))
json.dump(Stack_Data, open('prime_recom.txt','w'))
#%%
def start():
	print('Starting the crawl')
	#The BASE_URL + end_url will be the complete url to the webpage to be crawled.
    
	#To extract the data about the next pages to be visited and the pages those have been visited from the next_visit and visited files respectively
	with open('prime_visited.txt','r') as jsonfile:
		crawled = json.load(jsonfile)
		jsonfile.close()
	with open('prime_next_visit.txt','r') as jsonfile:
		next_visit = json.load(jsonfile)
		jsonfile.close()
	df = pd.read_csv('prime.csv',encoding='utf-8')
	with open('prime_recom.txt','r') as jsonfile:
		Stack_Data = json.load(jsonfile)
		jsonfile.close()
	page_no=55246
	err_count=0
	def signal_handler(*args):
		print("Exiting after save")
		df.to_csv('prime.csv', encoding='utf-8')
		json.dump(next_visit,open('prime_next_visit.txt','w'))
		json.dump(list(set(crawled)),open('prime_visited.txt','w'))
		json.dump(Stack_Data, open('prime_recom.txt','w'))
		sys.exit()
	signal.signal(signal.SIGINT,signal_handler)
	try:
		while(len(next_visit)>0):
			end_url = next_visit.pop(0)
			key = end_url
			print(str(page_no)+": "+end_url)
	
			#If the page has already been visited then it should be there in crawled list
			if end_url in crawled:
				json.dump(next_visit,open('prime_next_visit.txt','w'))
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
				json.dump(next_visit,open('prime_next_visit.txt','w'))
				sleep(25)
				print("Request denied")
				err_count+=1
				if err_count == 10:
					raise Exception("10 continuous requests denied")
				continue
			err_count=0
			#Name Extraction
			try:
				name_url = soup.title.text.split(":")[1].split(' ')[1:]
				df.loc[key,'Name']=" ".join(name_url)
				df.loc[key,'imdb']=float(soup.find('span', {'data-automation-id':"imdb-rating-badge"}).text)
				df.loc[key,'Time']=float(soup.findAll('span', {'class':"av-badge-text"})[1].text[:-4])
            
			except:
				1

			for i in range(len(soup.find_all('dl'))):
                            a=[]
                            for child in soup.find_all('dl')[i].descendants:
                                if str(type(child))=="<class 'bs4.element.Tag'>":
                                    a.append(child.text)
                                else:
                                    continue
                            try:
                                if (a[0]=="Director"):
                                    df.loc[key,'Directors']=a[1]
                            except:
                                    df.loc[key,'Directors']=""
                            try:
                                if (a[0]=="Starring"):
                                    df.loc[key,'Actor']=a[1]
                            except:
                                    df.loc[key,'Actor']=""                                
                            
                            try:
                                if (a[0]=="Genres"):
                                    df.loc[key,'Genre']=a[1]
                            except:
                                    df.loc[key,'Genre']=""                                     
                            try:
                                if (a[0]=="Amazon Maturity Rating"):
                                    df.loc[key,'Maturity']=a[1].split(".")[0]
                            except:
                                    df.loc[key,'Maturity']=""                                 
                            try:
                                if (a[0]=="startYear"):
                                    df.loc[key,'Production']=a[1]
                            except:
                                df.loc[key,'Production']=""
                            try:
                                if (a[0]=="Studio"):
                                    df.loc[key,'Production']=a[1]
                            except:
                                df.loc[key,'Production']=""
			#try:
			#	df.loc[key,'Story-line']=soup.find('div',{'class':'av-synopsis avu-full-width'}).text
			#except:
			#	df.loc[key,'Story-line']=""
			
			related_vids=[]
			for rq in soup.find_all('a', {'class' : 'a-link-normal dv-core'}):
				vid_end_url = rq.get('href').split('/')[4]
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
				df.to_csv('prime.csv', encoding='utf-8')
				json.dump(next_visit,open('prime_next_visit.txt','w'))
				json.dump(list(set(crawled)),open('prime_visited.txt','w'))
				json.dump(Stack_Data, open('prime_recom.txt','w'))
	except Exception as ee:
		print(ee)
		df.to_csv('prime.csv', encoding='utf-8')
		json.dump(next_visit,open('prime_next_visit.txt','w'))
		json.dump(list(set(crawled)),open('prime_visited.txt','w'))
		json.dump(Stack_Data, open('prime_recom.txt','w'))
#%%
start()
