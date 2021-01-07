import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from urllib.request import urlopen
import re


url = 'https://en.wikipedia.org/wiki/List_of_main_battle_tanks_by_country?fbclid=IwAR0g7YWlmOIOpQ-Z6oPJUojZXk5jm_Z6-I67QB_qg5qIicCEQxL49bTpzGI'
html = urlopen(url) 
soup = BeautifulSoup(html, 'html.parser')


tables = soup.find_all('table')
#print(tables)


countries = []
tank_types = []
quantities = []
origins = []


for table in tables:
    rows = table.find_all('tr')
    for row in rows:
        cells = row.find_all('td')
        if len(cells) >= 4 and cells[0]:
            if len(cells) == 4:
                country = countries[-1]
                countries.append(country)
            else:
                country = cells[0]
                countries.append(country.text.strip())

            tank_type, quantity, origin, _ = cells[-4:]


            tank_types.append(tank_type.text.strip())
            quantities.append(quantity.text.strip())
            origins.append(origin.text.strip())


#print(len(countries))
#print(countries)
#print(tank_types)
#print(quantities)

# Usuwanie odnosnikow i nawiasow
countries = [re.sub("[\(\[].*?[\)\]]", "", elem) for elem in countries]
tank_types = [re.sub("[\(\[].*?[\)\]]", "", elem) for elem in tank_types]
quantities = [re.sub("[\(\[].*?[\)\]]", "", elem) for elem in quantities]
origins = [re.sub("[\(\[].*?[\)\]]", "", elem) for elem in origins]


# dictionary
dict_tanks = {'Tank types': tank_types, 'Quantities': quantities, 'Origins': origins}

df1 = pd.DataFrame(dict_tanks, index = countries)

print(df1)



# zapis do .csv

df1.to_csv('out.csv')



# ---------------------------------------------------------------------------------------------
# Dane dotyczace sojuszy

url_parent = 'https://en.wikipedia.org/wiki/List_of_military_alliances?fbclid=IwAR3k0PJ2F2mSv_FypCsdonLtqz4aW7ZNL2KKDXn8vj4BT93gpOdNOHDiQ38'
html_parent = urlopen(url_parent) 
soup_parent = BeautifulSoup(html_parent, 'html.parser')

alliances_list = soup_parent.find_all('span', {'id': 'Current_military-security_alliances'})

alliances_list = soup_parent.find(id='Current_military-security_alliances').find_all('li')

soup_parent.find_all('h4')
alliances_list

