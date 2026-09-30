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

def get_username(name, username):

    sql = "SELECT id FROM player WHERE id = %s"

    cursor = connection.cursor()
    cursor.execute(sql, (username,))

    result = cursor.fetchone()

    if result:
        print("Username already taken")
    else:
        insert_sql = """
        INSERT INTO player (id, screen_name)
        VALUES (%s, %s)
        """

        cursor.execute(insert_sql, (username, name))
        connection.commit()

        print("User created successfully")

    cursor.close()


username = input("Enter the username: ")
name = input("Enter your name: ")

get_username(name, username)

def hae_lentokentat():
    sql = "SELECT name, ident FROM airport WHERE TYPE = 'large_airport' and continent = 'EU' limit 30"
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    if cursor.rowcount > 0:
        pass

    return result
    
lentokentat = hae_lentokentat()
#print(lentokentat)
valitut = random.sample(lentokentat,4)









