import geopy
from geopy.distance import geodesic
import mysql.connector 
import random


try:
    connection = mysql.connector.connect(
        host='airport.mysql.database.azure.com',
        port=3306,
        database='europe_airport_game',
        user='airport_simulator',
        password='Simulator@',
        #ssl_ca=r'G:\Python projects\Europe-Flight-Simulator\DigiCertGlobalRootG2.crt.pem',
        #ssl_verify_cert=True,
    )

    print("CONNECTED!")


except mysql.connector.Error as error:
    print("MYSQL ERROR:")
    print(error)

def hae_lentokentat():
    sql = "SELECT name, ident FROM airport WHERE TYPE = 'large_airport' and continent = 'EU' limit 30"
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    if cursor.rowcount > 0:
        pass

    return result
    




#Starting the distance
#Initial point is always Vaclav Havel Airport Parague icao code = "LKPR"

def distance(destination):
    
    sql = f"Select latitude_deg, longitude_deg from airport where ident = '{destination}'; "
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    return result

lentokentat = hae_lentokentat()
#print(lentokentat)
valitut = random.sample(lentokentat,4)
for i in valitut:
    print(i)
destination = input("Choose the ICAO code from the listed 4 airports.")

destination1 = distance(destination)



destination1_latitiude = destination1[0]
destination1_longitude = destination1[1]

parag_airport = (50.1008, 14.26)
destination_airport = (destination1[0], destination1[1])

distance_difference = (geodesic(parag_airport, destination_airport))
print(distance_difference)