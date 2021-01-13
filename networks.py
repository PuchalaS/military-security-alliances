import networkx as nx
import numpy as np
import queries_db
def draw_alliance_graph (start_date, end_date, k_core):
    
    '''państwa w sojuszach (państwa są węzłami; połączenie występuje gdy oba kraje są wspólnie w jakimkolwiek sojuszu) - 
    parametry filtrowanie po datach (wszyskie sojusze, które byly aktywne w danym okresie czasu) 
    filtrowanie po wielkosci k-rdzenia'''
    all_countries_connection = queries_db.get_coutries_connections(start_date, end_date) #zawiera duplikaty co chyba nie przeszkadza, a jak cos to [list(t) for t in set(tuple(element) for element in all_countries_connection)]
    print (len(all_countries_connection))


def draw_buyers_sellers_graph (k_core):
    '''sprzedaż kupno czołgów. Sieć państw lub sojuszy pokazująca czy między nimi dochodziło do sprzedaży uzbrojenia, 
    parametry filtrowanie po wielkosci k-rdzenia'''
    all_countries_connection = queries_db.get_buyers_sellers_connections() #[buyer, seller]
    print (all_countries_connection)


#draw_alliance_graph(1900,2000,1)
#draw_buyers_sellers_graph(1)