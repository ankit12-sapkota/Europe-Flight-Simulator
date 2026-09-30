import geopy
import mysql.connector 
import random


try:
    connection = mysql.connector.connect(
        host='airport.mysql.database.azure.com',
        port=3306,
        database='europe_airport_game',
        user='airport_simulator',
        password='',
        ssl_ca=r'G:\Python projects\Europe-Flight-Simulator\DigiCertGlobalRootG2.crt.pem',
        ssl_verify_cert=True,
    )

    print("CONNECTED!")


except mysql.connector.Error as error:
    print("MYSQL ERROR:")
    print(error)

#MAIN PROGRAM GAME CODE BEGINS HERE:

class player():
    def co2(self, co2_max, co2_consumed):

        pass

    def fuel(self, fuel_max, fuel_consumed):
        pass    
    def identity(self, id, name):
        pass
    def location(self, current_airport, destination):
        pass




