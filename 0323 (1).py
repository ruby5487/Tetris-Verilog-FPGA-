from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("http://lilina.csie.ncnu.edu.tw/~solomon/NCNU/ly.html")
bsObj = BeautifulSoup(html,"html.parser")
dict1 = {}

iList = bsObj.findAll("div",{"class":"legislatorname"})
aList = bsObj.findAll("img",{"class":"six-party-icon"})
for i in range(len(iList)):
    iiList = iList[i].get_text()
    aaList = aList[i]["alt"][0:-2]
    if aaList not in dict1:
        dict1[aaList] = [iiList]
    else:
        dict1[aaList].append(iiList)

for party in dict1:
    print(party)
    for name in dict1[party]:
        print('  ',name)
        





