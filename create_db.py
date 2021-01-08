import couchdb
from couchdb.design import ViewDefinition

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

if 'combined' in couch:
    #alliances = couch['alliances']
    del couch['combined']
    combined = couch.create('combined')
else:
    combined = couch.create('combined')

tanks['1'] = {'Id':"1",'Country':'Afghanistan','Type': 'T-55', 'Quantity': '601', 'Origin': 'Soviet Union'}
tanks['2'] = {'Id':"2",'Country':'Afghanistan','Type': 'T-62', 'Quantity': '170', 'Origin': 'Soviet Union'}
tanks['3'] = {'Id':"3",'Country':'Bangladesh','Type': 'Type 59G(BD) Durjoy', 'Quantity': '474', 'Origin': 'China'}
tanks['4'] = {'Id':"4",'Country':'Bangladesh','Type': 'Type 69', 'Quantity': '58', 'Origin': 'China'}
tanks['5'] = {'Id':"5",'Country':'Iran','Type': 'M48 Patton', 'Quantity': '108', 'Origin': 'United States'}
tanks['6'] = {'Id':"6",'Country':'Iran','Type': 'M60 Patton', 'Quantity': '150', 'Origin': 'United States'}
tanks['7'] = {'Id':"7",'Country':'Iran','Type': 'Chieftain (tank) MK3', 'Quantity': '100', 'Origin': 'United Kingdom'}
tanks['8'] = {'Id':"8",'Country':'Chad','Type': 'T-55', 'Quantity': '60', 'Origin': 'Soviet Union'}

alliances['1'] = {'Id':"1",'Name':'The U.S.–Afghanistan Strategic Partnership Agreement','Countries': ['Afghanistan', 'USA'], 'Start':'2004 ','End':'0'}
alliances['2'] = {'Id':"2",'Name':'Axis of Resistance', 'Countries': ['Iran', 'Syria'], 'Start':'2004 ','End':'0'}
alliances['3'] = {'Id':"3",'Name':'random alliance', 'Countries': ['Iran', 'Syria', 'Chad','Afghanistan','Bangladesh'], 'Start':'2004 ','End':'0'}

#Mapping functions
def documentMapper(doc):
    if doc.get('Id'):
        _id = doc['Id']
        yield(_id, doc)

def threadCountMapper(doc):
    if doc.get('Country'):
        _author = doc['Country']
        yield(_author, 1)

def tank_orgin_mapper(doc):
    if doc.get('Id'):
        _country = doc['Country']
        _orgin = doc['Origin']
        _quantity = doc['Quantity']
        yield([_country,_orgin], int(_quantity))

def alliance_orgin_tanks_mapper(doc):
    if doc.get('Id'):
        _name = doc['Name']
        _orgin = doc['Origin']
        _quantity = doc['Quantity']
        yield([_name,_orgin], int(_quantity))

#Mapping reducing functions

def summingReducer(keys, values, rereduce):
    return sum(values)


#for row in tanks.view('_all_docs'):
#    print(row.id)

#View creation



view = ViewDefinition('index', 'thread_tank_view',documentMapper, language = 'python')
view.sync(tanks)

#view for country and tank quantity and orgin
view = ViewDefinition('index', 'tank_orgin_view',tank_orgin_mapper, reduce_fun = summingReducer, language = 'python')
view.sync(tanks)


view = ViewDefinition('index', 'thread_alliance_view',documentMapper, language = 'python')
view.sync(alliances)

i=1
for a_vrow in alliances.view('index/thread_alliance_view'):
    a_row  = a_vrow.value
    a_countries = a_row.get('Countries')
    a_alliance = a_row.get('Name')
    a_start = a_row.get('Start')
    a_end = a_row.get('End')
    for country in a_countries:
        for t_vrow in tanks.view('index/thread_tank_view'): 
            t_row  = t_vrow.value
            t_country = t_row.get('Country')
            if t_country == country:
                t_type = t_row.get('Type')
                t_quantity = t_row.get('Quantity')
                t_orgin = t_row.get('Origin')
                combined[str(i)] = {'Id':str(i),'Country': t_country,'Type': t_type, 'Quantity': t_quantity, 'Origin': t_orgin,'Name':a_alliance, 'Start':a_start,'End':a_end}
                print (combined[str(i)] )
                i+=1
                
            

view = ViewDefinition('index', 'thread_combined_view',documentMapper, language = 'python')
view.sync(combined)

#view for alliance - orgin and of quantity tanks 
view = ViewDefinition('index', 'alliance_tank_orgin_view',alliance_orgin_tanks_mapper, reduce_fun = summingReducer, language = 'python')
view.sync(combined)