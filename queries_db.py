import couchdb
from couchdb.design import ViewDefinition
from prettytable import PrettyTable
from collections import defaultdict 


couch = couchdb.Server("http://admin:admin@localhost:5984")


tanks = couch['tanks']
alliances = couch['alliances']
combined = couch['combined']




for row in tanks.view('index/tank_orgin_view', group_level = 2):
    print(str(row.key) + " " + str(row.value))


#
#Queries
#
def country_tank_info(x_country):
    '''Query for country - getting tanks information
    returns: tuple list of (tank_type, quantity)'''
    tank_quantity_list = []
    for vrow in tanks.view('index/thread_tank_view'):
        row  = vrow.value
        country = row.get('Country')
        if (country == x_country):
            tank_quantity_list.append((row.get('Type'), row.get('Quantity')))
    return tank_quantity_list

def country_aliance_info(x_country):
    '''Query for country - alliance  information
    returns: list of country alliances'''
    country_aliance_list = []
    for vrow in alliances.view('index/thread_alliance_view'):
        row  = vrow.value
        countries = row.get('Countries')
        if x_country in countries:
            country_aliance_list.append(row.get('Name'))
    return country_aliance_list

def country_tank_seller_origin_info(x_country):
    '''Query for country - tanks orgin information
    returns: tuple list of (orgin, quantity)'''
    country_tank_seller_origin_list = []
    for vrow in tanks.view('index/tank_orgin_view', group_level = 2):
        row  = vrow.key
        country = row[0]
        if (country == x_country):
            country_tank_seller_origin_list.append((row[1], vrow.value))
    return country_tank_seller_origin_list

def alliance_tanks_info(x_alliance):
    '''Query for alliance - getting tanks information
    returns: tuple list of (tank_type, quantity)'''
    alliance_tank_list = []
    for vrow in combined.view('index/alliance_tank_type_view', group_level = 2):
        row  = vrow.key
        alliance = row[0]
        if (alliance == x_alliance):
            alliance_tank_list.append((row[1], vrow.value))
    return alliance_tank_list

def alliance_countries_info(x_alliance):
    '''Query for alliance - getting member countries information
    returns: list of alliance members'''
    for vrow in alliances.view('index/thread_alliance_view'):
        row  = vrow.value
        alliance = row.get('Name')
        if alliance == x_alliance:
            return row.get('Countries')

def alliance_tanks_origin_info(x_alliance):
    '''Query for alliance - tanks orgin information
    returns: tuple list of (orgin, quantity)'''
    country_tank_seller_origin_list = []
    for vrow in combined.view('index/alliance_tank_orgin_view', group_level = 2):
        row  = vrow.key
        alliance = row[0]
        if (alliance == x_alliance):
            country_tank_seller_origin_list.append((row[1], vrow.value))
    return country_tank_seller_origin_list


def overall_tanks_quantity():
    '''Query for whole db - type quantity information
    returns: tuple list of (type, quantity)'''
    overall_tanks_quantity_list = []
    for vrow in tanks.view('index/overall_tank_type_quantity_view', group_level = 1):
        row  = vrow.key
        overall_tanks_quantity_list.append((row, vrow.value))
    return overall_tanks_quantity_list

def overall_orgin_quantity():
    '''Query for whole db - orgin quantity information
    returns: tuple list of (orgin, quantity)'''
    overall_orgin_quantity_list = []
    for vrow in tanks.view('index/overall_tank_orgin_quantity_view', group_level = 1):
        row  = vrow.key
        overall_orgin_quantity_list.append((row, vrow.value))
    return overall_orgin_quantity_list

def overall_alliances_tank_quantity():
    '''Query for whole db - orgin quantity information
    returns: tuple list of (orgin, quantity)'''
    overall_alliances_tank_quantity_list = []
    for vrow in combined.view('index/overall_alliance_tanks_quantity_view', group_level = 1):
        row  = vrow.key
        overall_alliances_tank_quantity_list.append((row, vrow.value))
    return overall_alliances_tank_quantity_list


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
#for row in tanks.view('index/count_threads', group_level = 1):
#    print(str(row.key) + " " + str(row.value))




#for row in tanks.view('index/count_threads'):
#    print(str(row.key) + " " + str(row.value))
    #print("Country: " + row['Country'] + " Tank: " + row['type'])

#print(tanks.get("1"))
#print(next(ok))