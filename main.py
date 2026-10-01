
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

#MAIN PROGRAM GAME CODE BEGINS HERE:

def get_username(username):


    while True:
        
        sql = "SELECT id FROM player WHERE id = %s"

        cursor = connection.cursor()
        cursor.execute(sql, (username,))

        result = cursor.fetchone()
    
        if result:
             print("Username already taken")
             username = input("Enter a new user name: ")
        else:
            return username 

        print("User created succesfully.")
        
    

user_name = input("Enter a user name: ")
username = get_username(user_name)

name = input("Enter your name for the user name: ")


print("Welcome to europe flight simulator")

print("We have a starting airport as parag international code. \n You get 4 option of airport where you wanna travel. \n You have 3000l of fuel, Get bonus point if you use less CO2. ")

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

def find_destination(destination):
    
    sql = f"Select latitude_deg, longitude_deg from airport where ident = '{destination}'; "
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    return result


current_airport = "LFPK"
lentokentat = hae_lentokentat()
#print(lentokentat)
valitut = random.sample(lentokentat,4)
for i in valitut:
    print(i)
destination = input("Choose the ICAO code from the listed 4 airports.")

destination1 = find_destination(destination)

def fuel_consumed(distance_travelled):
    return distance_travelled

def co2_consumed(consumed_fuel):
    co2_consumed = consumed_fuel * 0.5
    return co2_consumed


parag_airport = (50.1008, 14.26)
destination_airport = (destination1[0], destination1[1])

distance = (geodesic(parag_airport, destination_airport))
distance_travelled = distance.kilometers

#Now we calculate the total fuel consumed and total co2 consumed
# 1liters of fuel = 1km
# 1liters 0.5 kg of co2

consumed_fuel = fuel_consumed(distance_travelled)
co2_taken = co2_consumed(consumed_fuel)

def update_data():
    sql = """
        INSERT INTO player
        (id, screen_name, Destination, distance, Total_fuel_consumed, Co2_consumed)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    cursor = connection.cursor()

    cursor.execute(sql, (
        username,
        name,
        destination,
        distance_travelled,
        consumed_fuel,
        co2_taken
    ))

    connection.commit()

    cursor.close()

    print("Data updated successfully!")


data_update = update_data()
















