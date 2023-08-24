from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq

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
