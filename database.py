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


tanks['1'] = {'Country':'Afghanistan','type': 'T-55', 'Quantity': '601', 'Origin': 'Soviet Union'}
tanks['2'] = {'Country':'Afghanistan','type': 'T-62', 'Quantity': '170', 'Origin': 'Soviet Union'}
tanks['3'] = {'Country':'Bangladesh','type': 'Type 59G(BD) Durjoy', 'Quantity': '474', 'Origin': 'China'}
tanks['4'] = {'Country':'Bangladesh','type': 'Type 69', 'Quantity': '58', 'Origin': 'China'}
tanks['5'] = {'Country':'Iran','type': 'M48 Patton', 'Quantity': '108', 'Origin': 'United States'}
tanks['6'] = {'Country':'Iran','type': 'M60 Patton', 'Quantity': '150', 'Origin': 'United States'}
tanks['7'] = {'Country':'Iran','type': 'Chieftain (tank) MK3', 'Quantity': '100', 'Origin': 'United Kingdom'}

alliances['The U.S.–Afghanistan Strategic Partnership Agreement'] = {'Name':'The U.S.–Afghanistan Strategic Partnership Agreement',
                                                                     'Countries': ['Afghanistan', 'USA'], 'Start':'','End':''}
alliances['Axis of Resistance'] = {'Name':'Axis of Resistance',
                                                                     'Countries': ['Iran', 'Syria']}

#dump(database_name="tanks" dump --dump-to=tanks.json")