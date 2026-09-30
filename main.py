import geopy
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





