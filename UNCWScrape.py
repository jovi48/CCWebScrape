import csv
from bs4 import BeautifulSoup
import requests
import re

# import into CSV
rowList = ["Company Type","Company Name", "Address","City", "State", "Zip", "Phone Number","Website"]
with open("wilmington.csv", "w", newline='') as file:
    writer = csv.writer(file)
    writer.writerow(rowList)

# grab html for wilmington chamber of commercer
#using requests librariy

url = "https://www.wilmingtonchamber.org/list/"
result = requests.get(url)

#using Bs4 to parse request

doc = BeautifulSoup(result.text, "html.parser")

# class name in regualr expression
pattern = re.compile(r"gz-subcats-col\d")

directories = doc.find_all(["li"], class_=pattern)

for directory in directories:
    url = directory.find(["a"])["href"]
    companyType = url
    print(companyType)
    

    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")

    infoboxes = doc.find_all(["div"], class_="gz-list-card-wrapper")
    

    for infobox in infoboxes:

        # grabs company name from header
        header_info = infobox.find(["div"], class_="card-header")
        
        company_name = header_info.find(attrs={"alt": True})

        if company_name == None:
            continue


        # grabs address and phone number from body

        body_info = infobox.find(["div"], class_="card-body gz-results-card-body")

        try:
            street_address = body_info.find(["span"], class_="gz-street-address")
        except:
            street_address = None

        try:
            city_addy = body_info.find(["div"], itemprop="citystatezip")
        except:
            city_addy = None

        try:
            address_info = city_addy.find_all(["span"])
        except:
            address_info = None

        try:
            phone_number = body_info.find(["li"], class_="list-group-item gz-card-phone")
        except:
            phone_number = None

        

        if street_address == None:
            continue

        if city_addy == None:
            continue

        if phone_number == None:
            continue

        if address_info == None:
            continue

        phonenum = phone_number.span
        
        print(address_info)

        company = company_name["alt"]
        street = street_address.text
        city = address_info[0].text
        state = address_info[1].text
        zip = address_info[2].text
        phone = phonenum.text 
        

        # print(company, street, city, state, zip, phone)

        # grab website
        try:
            url = header_info.find(["a"])["href"]
            result = requests.get(url)
            doc = BeautifulSoup(result.text, "html.parser")
            website = doc.find(["li"], class_="list-group-item gz-card-website").find(["a"])["href"]
        except:
            website = None

        rowList = [companyType,company, street, city, state, zip, phone, website]
        print(rowList)
        with open("wilmington.csv", "a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(rowList)