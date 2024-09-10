from bs4 import BeautifulSoup
import requests
import re

url = "https://members.bhpchamber.org/list" #Store URL in variable 
result = requests.get(url) #Store Http in result 


#BS4 Parsing Request
doc = BeautifulSoup(result.text, "html.parser")
#print(doc)

pattern = re.compile(r"gz-subcats-col\d")

directories = doc.find_all(["li"], class_ = pattern) #Find all li elements
#doc.find_all(["HTML_TAG"])

#print(directories)

for directory in directories:
    
    url = directory.find(["a"])["href"]
    print(url)

    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")


    infoboxes = doc.find_all(["div"], class_="gz-list-card-wrapper")
    print(infoboxes)

    









