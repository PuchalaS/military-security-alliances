import couchdb
from save_restore_db import dump

couch = couchdb.Server("http://admin:admin@localhost:5984")

#couch = couchdb.Server("http://2840f3b8-e4d3-4326-bdbb-4e0db7f7e344-bluemix:admin@https://examples.cloudant.com/query-movies")
if 'tanks' in couch:
    #tanks = couch['tanks']
    del couch['tanks']
    tanks = couch.create('tanks')
else:
    tanks = couch.create('tanks')

if 'alliances' in couch:
    #alliances = couch['alliances']
    del couch['alliances']
    alliances = couch.create('alliances')
else:
    alliances = couch.create('alliances')


tanks['1'] = {'Id':"1",'Country':'Afghanistan','Type': 'T-55', 'Quantity': '601', 'Origin': 'Soviet Union'}
tanks['2'] = {'Id':"2",'Country':'Afghanistan','Type': 'T-62', 'Quantity': '170', 'Origin': 'Soviet Union'}
tanks['3'] = {'Id':"3",'Country':'Bangladesh','Type': 'Type 59G(BD) Durjoy', 'Quantity': '474', 'Origin': 'China'}
tanks['4'] = {'Id':"4",'Country':'Bangladesh','Type': 'Type 69', 'Quantity': '58', 'Origin': 'China'}
tanks['5'] = {'Id':"5",'Country':'Iran','Type': 'M48 Patton', 'Quantity': '108', 'Origin': 'United States'}
tanks['6'] = {'Id':"6",'Country':'Iran','Type': 'M60 Patton', 'Quantity': '150', 'Origin': 'United States'}
tanks['7'] = {'Id':"7",'Country':'Iran','Type': 'Chieftain (tank) MK3', 'Quantity': '100', 'Origin': 'United Kingdom'}
tanks['8'] = {'Id':"8",'Country':'Chad','Type': 'T-55', 'Quantity': '60', 'Origin': 'Soviet Union'}

alliances['1'] = {'Id':"1",'Name':'The U.S.–Afghanistan Strategic Partnership Agreement',
                                                                     'Countries': ['Afghanistan', 'USA'], 'Start':'2004 ','End':'0'}
alliances['2'] = {'Id':"2",'Name':'Axis of Resistance', 'Countries': ['Iran', 'Syria'], 'Start':'2004 ','End':'0'}
alliances['3'] = {'Id':"3",'Name':'Twoj stary', 'Countries': ['Iran', 'Syria'], 'Start':'2004 ','End':'0'}
#dump(database_name="tanks" dump --dump-to=tanks.json")