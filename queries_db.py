import couchdb
from couchdb.design import ViewDefinition
from prettytable import PrettyTable

couch = couchdb.Server("http://admin:admin@localhost:5984")


tanks = couch['tanks']
alliances = couch['alliances']

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
        yield(_country, int(_quantity))
        
def summingReducer(keys, values, rereduce):
    return sum(values)

def summing_from_list_Reducer(keys, values, rereduce):
    return [0, sum(values[1])]

#for row in tanks.view('_all_docs'):
#    print(row.id)


view = ViewDefinition('index', 'count_threads', threadCountMapper, reduce_fun = summingReducer, language = 'python')
view.sync(tanks)

view = ViewDefinition('index', 'thread_tank_view',documentMapper, language = 'python')
view.sync(tanks)

view = ViewDefinition('index', 'thread_alliance_view',documentMapper, language = 'python')
view.sync(alliances)

#widok z krajem iloscia czolgow z danego zrodla
view = ViewDefinition('index', 'tank_orgin_view',tank_orgin_mapper, reduce_fun = summingReducer, language = 'python')
view.sync(tanks)

for row in tanks.view('index/tank_orgin_view', group_level = 1):
    print(str(row.key) + " " + str(row.value))

def country_tank_info(x_country):
    tank_quantity_list = []
    for vrow in tanks.view('index/thread_tank_view'):
        row  = vrow.value
        country = row.get('Country')
        if (country == x_country):
            tank_quantity_list.append((row.get('Type'), row.get('Quantity')))
    return tank_quantity_list

def country_aliance_info(x_country):
    country_aliance_list = []
    for vrow in alliances.view('index/thread_alliance_view'):
        row  = vrow.value
        countries = row.get('Countries')
        if x_country in countries:
            country_aliance_list.append(row.get('Name'))
    return country_aliance_list

def country_tank_seller_origin(x_country):
    country_tank_seller_origin_list = []
    for vrow in tanks.view('index/thread_alliance_view'):
        row  = vrow.value
        country = row.get('Country')
        if (country == x_country):
            country_tank_seller_origin_list.append(row.get('Name'))
    return country_tank_seller_origin_list

country_tank_info = country_tank_info("Iran")
country_aliance_info = country_aliance_info("Iran")

print(sum(int(n) for _,n in country_tank_info))
print(country_tank_info) 
print(country_aliance_info)
#for row in tanks.view('index/count_threads', group_level = 1):
#    print(str(row.key) + " " + str(row.value))




#for row in tanks.view('index/count_threads'):
#    print(str(row.key) + " " + str(row.value))
    #print("Country: " + row['Country'] + " Tank: " + row['type'])

#print(tanks.get("1"))
#print(next(ok))