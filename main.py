
from geopy.distance import geodesic
import mysql.connector 
import random


try:
    connection = mysql.connector.connect(
        host='',
        port=3306,
        user='',
        password='',
        database='europe_airport_game',
        #ssl_ca=r'',
        #ssl_verify_cert=True,
    )

    print("CONNECTED!")


except mysql.connector.Error as error:
    print("MYSQL ERROR:")
    print(error)

cursor = connection.cursor()
#MAIN PROGRAM GAME CODE BEGINS HERE:

#--------------------------------
#CHECK USERNAME
#--------------------------------

def get_username(username):
        
    cursor.execute(
        "SELECT id FROM player WHERE id = %s", 
        (username,)
    )

    result = cursor.fetchone()
    if result:
        return True
    else:
        return False

        
#------------------------------
#Get 4 airports from database execpt the current location of player
#--------------------------

def hae_lentokentat(current_airport):
    cursor.execute(""" 
    SELECT name, ident FROM airport WHERE type = 'large_airport' and continent = 'EU' and ident != %s
    """, (current_airport,))

    lentokentat = cursor.fetchall()

    return random.sample(lentokentat, 4)
    
#Starting the distance
#Initial point is always Vaclav Havel Airport Parague icao code = "LKPR"
#--------------------------
#Calculate distance
#------------------------


def find_destination(destination):
    
    sql = f"Select latitude_deg, longitude_deg from airport where ident = '{destination}'; "
    cursor.execute(sql)
    result = cursor.fetchone()
    return result

#----------------------------
#Calculate the distance between current_location and destinaton
#--------------------------

def calculate_distance(departure, destination):
    distance = geodesic(departure, destination).kilometers
    return distance

#-------------------------------
#Calculate fuel
#------------------------------
#Now we calculate the total fuel consumed and total co2 consumed
# 1liters of fuel = 1km
# 1liters 0.5 kg of co2


def fuel_consumed(distance, weather):

    fuel = distance
    if weather == "Cloudy":

        fuel = fuel * 1.05

    elif weather == "Storm":

        fuel = fuel * 1.15

    return fuel


#-----------------------
#Calculate co2
#-----------------

def co2_consumed(fuel):
    co2 = fuel * 0.5
    return co2

#------------------------------------------------------------
#This function calculates the points and also add bonus points according to the carbon emission when it is less.
#--------------------------------------------------

def calculate_points(distance, co2):

    if co2 <= 500:

        points = distance * 0.1 + 20

    elif co2 <= 1000:

        points = distance * 0.1

    else:

        points = distance * 0.1 - 10

    return points


#---------------------------------------------------
#This function updates the data to the database
#.-----------------------------------------

def update_data(
        username,
        destination,
        distance,
        fuel,
        co2,
        points
):

    cursor.execute("""
        UPDATE player
        SET
            current_airport = %s,
            Destination = %s,
            distance = distance + %s,
            Total_fuel = Total_fuel - %s,
            Total_fuel_consumed =
                Total_fuel_consumed + %s,
            Co2_consumed =
                Co2_consumed + %s,
            Goal_points =
                Goal_points + %s,
            Flights_completed =
                Flights_completed + 1
        WHERE id = %s
    """, (
        destination,
        destination,
        distance,
        fuel,
        fuel,
        co2,
        points,
        username
    ))

    connection.commit()


def refill_fuel(username):

    cursor.execute("""
        UPDATE player
        SET
            Total_fuel = Total_fuel + 2000,
            Goal_points = Goal_points - 20
        WHERE id = %s
        AND Goal_points >= 20
    """, (username,))

    connection.commit()

    if cursor.rowcount > 0:

        print("\nYou bought 2000 litres of fuel.")
        print("20 points were deducted.")

        return True

    else:

        print("\nYou do not have enough points.")

        return False


def show_player(username):

    cursor.execute("""
        SELECT
            current_airport,
            Total_fuel,
            Total_fuel_consumed,
            Co2_consumed,
            Goal_points,
            Flights_completed,
            distance
        FROM player
        WHERE id = %s
    """, (username,))

    player = cursor.fetchone()

    print("\n")
    print("------------------------------")
    print("PLAYER INFORMATION")
    print("------------------------------")

    print("Current airport:", player[0])
    print("Fuel remaining:", round(player[1], 2), "litres")
    print("Fuel consumed:", round(player[2], 2), "litres")
    print("CO2 produced:", round(player[3], 2), "kg")
    print("Points:", round(player[4], 2))
    print("Flights completed:", player[5])
    print("Total distance:", round(player[6], 2), "km")    


def show_leaderboard():

    cursor.execute("""
        SELECT
            screen_name,
            Goal_points,
            Flights_completed,
            distance
        FROM player
        ORDER BY Goal_points DESC
        limit 15
    """)

    players = cursor.fetchall()

    print("\n")
    print("==============================")
    print("        LEADERBOARD")
    print("==============================")

    number = 1

    for player in players:

        print(
            number,
            player[0],
            "-",
            round(player[1], 2),
            "points",
            "-",
            player[2],
            "flights",
            "-",
            round(player[3] or 0,  2),
            "km"
        )

        number = number + 1

    print("==============================")



#-------------------------------
#Actual Game
#-------------------------------

username = input("Enter your username \nNote:User name should be unique: ")

if get_username(username):
    print("Welcome back")

else:
    print("New player!")
    screen_name = input("Enter your name: ")

    #LFPK is the starting airport
    #This stores the new players information in the database if there is no record before
    cursor.execute("""
    Insert into player (id, screen_name, current_airport
    )
    values (%s, %s , %s)""",(
        username,
        screen_name,
        "LFPK"
    ))
    connection.commit()

    print("Player created succesfully")
    print("Starting GAME EUROPE AIRPORT SIMULATOR.")
    print("======================")
    print("Starting game from the 'LFPK' airport in cheque republic. ")

#------------------------------
# GAME LOOP STARTS FROM HERE
# --------------------------------

while True:
    cursor.execute("""
    Select
        current_airport,
        Total_fuel,
        Total_fuel_consumed,
        Co2_consumed,
        Goal_points,
        Flights_completed,
        distance,
        Co2_Max
    From player
    where id = %s""", (username,))

    player = cursor.fetchone()

    current_airport = player[0]
    total_fuel = player[1]
    total_fuel_consumed = player[2]
    total_co2 = player[3]
    points = player[4]
    flights = player[5]
    total_distance = player[6]
    maximun_co2_limit = player[7]


    show_player(username)


    if points >= 500 and total_co2 < maximun_co2_limit:

        print("\n==============================")
        print("       CONGRATULATIONS!")
        print("==============================")

        print("You reached 500 points! and won the game.")

        print(
            "Flights completed:",
            flights
        )

        print(
            "Total distance:",
            round(total_distance, 2),
            "km"
        )

        print(
            "Total fuel consumed:",
            round(total_fuel_consumed, 2),
            "litres"
        )

        print(
            "Total CO2 produced:",
            round(total_co2, 2),
            "kg"
        )

        print(
            "Final points:",
            round(points, 2)
        )

        show_leaderboard()

        break
    elif total_co2 >= maximun_co2_limit:
        print("Caught By the Activists.")
        break


    #We get airports using hae_lentokennat function

    airports = hae_lentokentat(
        current_airport
    )

    print("\nChoose your destination Airport: ")

    for i in range(len(airports)):

        print(
            i + 1,
            airports[i][0],
            "(" + airports[i][1] + ")"
        )
    print("5. Show leaderboard")
    print("6. Quit")

    choice = input("Choose an option from 1 - 6: ")


    if choice == "5":
        show_leaderboard()
        continue
    if choice == "6":
        print("Game is quited:")
        print(f"You have completed {flights} flights.")   
        break

    if not choice.isdigit():
        print("Please inter a number from 1 - 6:")
        continue

    choice = int(choice)

    if choice < 1 or choice > 4:
        print("Invalid choice")


    #Here a player can select his her destination"
    destination = airports[choice -1]
    destination_name = destination[0]
    destination_ident = destination[1]

    #We get cordinates using the find destination function and ident of the airport

    departure_coordinates = find_destination(current_airport)
    destination_airport = find_destination(destination_ident)


    # caculate_distance between current airport and the destination airport using the coordinates and geodesic

    distance  = calculate_distance(departure_coordinates, destination_airport)

    weather = random.choice([
        "Clear",
        "Cloudy",
        "Storm"
    ])

    #Now next step is to calculate the fuel using distance and weather with function fuel consumed

    fuel = fuel_consumed(distance, weather)


    #Now calculate the co2_consumed using the fuel and co2_consumed function

    co2 = co2_consumed(fuel)

    #Now we calculate points using the distance and the bonus point as we consider sustainable development
    #Or we promote "kestävä kehitys". This features promote the player to get bonus point for less co2 emission

    flight_points = calculate_points(distance, co2)

    print("\n")
    print("==============================")
    print("       FLIGHT INFORMATION")
    print("==============================")

    print("From:", current_airport)
    print("To:", destination_name)
    print("Weather:", weather)
    print("Distance:", round(distance, 2), "km")
    print("Fuel needed:", round(fuel, 2), "litres")
    print("CO2:", round(co2, 2), "kg")
    print("Points:", round(flight_points, 2))

    print("==============================")

    if total_fuel < fuel:

        print("\nYou don't have enough fuel.")

        print(
            "Fuel available:",
            round(total_fuel, 2),
            "litres"
        )

        print(
            "Fuel needed:",
            round(fuel, 2),
            "litres"
        )


        refill = input(
            "\nBuy 2000 litres for 20 points? (y/n): "
        )


        if refill.lower() == "y":

            if refill_fuel(username):

                print("Fuel refilled.")
                print("Please select the flight again.")

            continue

        else:

            print("Flight cancelled.")

            continue 

    fly = input("\nDo you want to take this flight (y/n): ")
    if fly.lower() != "y":
        print("Flight is Cancelled.")
        continue

    #------------------------------
    #Now we update the every information of flights to database
    #--------------------------------------
    update_data(
        username,
        destination_ident,
        distance,
        fuel,
        co2,
        flight_points
    )

    cursor.execute("""
        SELECT Flights_completed
        FROM player
        WHERE id = %s
    """, (username,))

    completed_flights = cursor.fetchone()[0]


    print("\n==============================")
    print("       FLIGHT COMPLETED")
    print("==============================")

    print(
        "You earned",
        round(flight_points, 2),
        "points."
    )
    print(
        "Flights completed:",
        completed_flights
    )

cursor.close()
connection.close()    


