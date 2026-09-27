import geopy
import mysql.connector 
import random


connection = mysql.connector.connect (
    host='airport.mysql.database.azure.com',
    port='3306',
    database='europe_airport_game',
    user='airport_simulator',
    password='Simulator@',
    autocommit=True
    )

