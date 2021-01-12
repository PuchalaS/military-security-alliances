import couchdb
from couchdb.design import ViewDefinition
from prettytable import PrettyTable
from collections import defaultdict 


couch = couchdb.Server("http://admin:admin@localhost:5984")


tanks = couch['tanks']
alliances = couch['alliances']
combined = couch['combined']




#for row in tanks.view('index/tank_orgin_view', group_level = 2):
#    print(str(row.key) + " " + str(row.value))

def create_table(fields, data):
    pt = PrettyTable(field_names = fields)
    for f in fields:
        pt.align = 'l'
    data.sort(key=lambda x: x[1],reverse=True)
    for row in data:
        pt.add_row([row[0], row[1]])
    return pt.get_string()

def create_table_1col(fields, data):
    pt = PrettyTable(field_names = fields)
    for f in fields:
        pt.align = 'l'
    data.sort()
    for row in data:
        pt.add_row([row])
    return pt.get_string()

#
#Queries
#

def country_tank_info(x_country, formated = False):
    '''Query for country - getting tanks information
    returns: tuple list of (tank_type, quantity)'''
    tank_quantity_list = []
    for vrow in tanks.view('index/thread_tank_view'):
        row  = vrow.value
        country = row.get('Country')
        if (country == x_country):
            tank_quantity_list.append((row.get('Type'), row.get('Quantity')))
    if not formated:
        return tank_quantity_list
    else:
        return create_table( ['Type' , 'Count'], tank_quantity_list)

def country_aliance_info(x_country, formated = False):
    '''Query for country - alliance  information
    returns: list of country alliances'''
    country_aliance_list = []
    for vrow in alliances.view('index/thread_alliance_view'):
        row  = vrow.value
        countries = row.get('Countries')
        if x_country in countries:
            country_aliance_list.append(row.get('Name'))
    if not formated:
        return country_aliance_list
    else:
        return create_table_1col(["Alliance"], country_aliance_list)

def country_tank_seller_origin_info(x_country, formated = False):
    '''Query for country - tanks orgin information
    returns: tuple list of (orgin, quantity)'''
    country_tank_seller_origin_list = []
    for vrow in tanks.view('index/tank_orgin_view', group_level = 2):
        row  = vrow.key
        country = row[0]
        if (country == x_country):
            country_tank_seller_origin_list.append((row[1], vrow.value))
    if not formated:
        return country_tank_seller_origin_list
    else:
        return create_table( ['Orgin' , 'Count'], country_tank_seller_origin_list)

def alliance_tanks_info(x_alliance, formated = False):
    '''Query for alliance - getting tanks information
    returns: tuple list of (tank_type, quantity)'''
    alliance_tank_list = []
    for vrow in combined.view('index/alliance_tank_type_view', group_level = 2):
        row  = vrow.key
        alliance = row[0]
        if (alliance == x_alliance):
            alliance_tank_list.append((row[1], vrow.value))
    if not formated:
        return alliance_tank_list
    else:
        return create_table( ['Orgin' , 'Count'], alliance_tank_list)

def alliance_countries_info(x_alliance, formated = False):
    '''Query for alliance - getting member countries information
    returns: list of alliance members'''
    for vrow in alliances.view('index/thread_alliance_view'):
        row  = vrow.value
        alliance = row.get('Name')
        if alliance == x_alliance:
            if not formated:
                return row.get('Countries')
            else:
                return create_table_1col(["Country"], row.get('Countries'))

def alliance_tanks_origin_info(x_alliance, formated = False):
    '''Query for alliance - tanks orgin information
    returns: tuple list of (orgin, quantity)'''
    country_tank_seller_origin_list = []
    for vrow in combined.view('index/alliance_tank_orgin_view', group_level = 2):
        row  = vrow.key
        alliance = row[0]
        if (alliance == x_alliance):
            country_tank_seller_origin_list.append((row[1], vrow.value))
    if not formated:
        return country_tank_seller_origin_list
    else:
        return create_table( ['Orgin' , 'Count'], country_tank_seller_origin_list)


def overall_tanks_quantity(formated = False):
    '''Query for whole db - type quantity information
    returns: tuple list of (type, quantity)'''
    overall_tanks_quantity_list = []
    for vrow in tanks.view('index/overall_tank_type_quantity_view', group_level = 1):
        row  = vrow.key
        overall_tanks_quantity_list.append((row, vrow.value))
    if not formated:
        return overall_tanks_quantity_list
    else:
        return create_table( ['Orgin' , 'Count'], overall_tanks_quantity_list)

def overall_orgin_quantity(formated = False):
    '''Query for whole db - orgin quantity information
    returns: tuple list of (orgin, quantity)'''
    overall_orgin_quantity_list = []
    for vrow in tanks.view('index/overall_tank_orgin_quantity_view', group_level = 1):
        row  = vrow.key
        overall_orgin_quantity_list.append((row, vrow.value))
    if not formated:
        return overall_orgin_quantity_list
    else:
        return create_table( ['Orgin' , 'Count'], overall_orgin_quantity_list)

def overall_alliances_tank_quantity(formated = False):
    '''Query for whole db - orgin quantity information
    returns: tuple list of (orgin, quantity)'''
    overall_alliances_tank_quantity_list = []
    for vrow in combined.view('index/overall_alliance_tanks_quantity_view', group_level = 1):
        row  = vrow.key
        overall_alliances_tank_quantity_list.append((row, vrow.value))
    if not formated:
        return overall_alliances_tank_quantity_list
    else:
        return create_table( ['Orgin' , 'Count'], overall_alliances_tank_quantity_list)

def get_all_countries():
    all_countries = []
    for vrow in tanks.view('index/thread_tank_view'):
        row  = vrow.value
        country = row.get('Country')
        if country not in all_countries:
            all_countries.append(country)
    return sorted(all_countries)

def get_all_alliances():
    all_alliances = []
    for vrow in alliances.view('index/thread_alliance_view'):
        row  = vrow.value
        name = row.get('Name')
        if isinstance(name, list):
            name = name[0]
        if name not in all_alliances:
            name.replace("Â", "")
            all_alliances.append(name)
    return all_alliances

'''
country_tanks = country_tank_info("Iran")
country_aliance_info = country_aliance_info("Iran")
country_tank_seller_origin_info = country_tank_seller_origin_info("Iran")
alliance_tanks = alliance_tanks_info('random alliance')
alliance_countries = alliance_countries_info('random alliance')
alliance_tanks_origin = alliance_tanks_origin_info('random alliance')

print(sum(int(n) for _,n in country_tanks))
print(country_tanks) 
print(country_aliance_info)
print(country_tank_seller_origin_info)
print(alliance_tanks)
print(alliance_countries)
print(alliance_tanks_origin)
print(overall_tanks_quantity())
print(overall_orgin_quantity())
print(overall_alliances_tank_quantity())
print(get_all_countries())
'''
#for row in tanks.view('index/count_threads', group_level = 1):
#    print(str(row.key) + " " + str(row.value))




#for row in tanks.view('index/count_threads'):
#    print(str(row.key) + " " + str(row.value))
    #print("Country: " + row['Country'] + " Tank: " + row['type'])

#print(tanks.get("1"))
#print(next(ok))