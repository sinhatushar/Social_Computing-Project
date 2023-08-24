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
Stack_Data = {}
page_url = 'https://en.wikipedia.org/wiki/List_of_original_programs_distributed_by_Amazon'
source_code = requests.get(page_url).text
soup = BeautifulSoup(source_code,'html.parser')

l_name=[] #list of names of amazon prime originals
tablelist=soup.findAll('table')
for t in tablelist:
	try:
		tbody=t.find('tbody')
		tr=tbody.findAll('tr')
		for i in range(len(tr)-1):
			try:
				td=tr[i+1].findAll('td')
				title = td[0].find('a')['title']
				l_name.append(title)
				print(title)
				name=''
				for j in title:
					if(j=='('):
						name=name[:-1]
						l_name.append(name)
						print(name)
						break
					else:
						name=name+j
			except:
				continue	
	except:
		continue
print(len(l_name))
f = open('prime_originals_list.txt', 'w')
json.dump(l_name, f)
f.close()
#%%