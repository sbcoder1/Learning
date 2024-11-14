import mysql.connector
import getpass
from cryptography.fernet import Fernet
import re
import uuid
import os
from colorama import Fore, init
import pyfiglet
from datetime import datetime
from tabulate import tabulate


#-------------------------------------------------------------------------CODE OF DISPLAY BANNER ---
# Initialize colorama
init()

# Clear the terminal screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Display "Cinema Hub" in big text with colors
def display_cinema_hub():
    clear_screen()
    # Generate ASCII art for Cinema Hub
    ascii_art = pyfiglet.figlet_format("Cinema Hub")
    
    # Add attractive colors (green for the header, yellow for the text)
    print(Fore.GREEN + ascii_art + Fore.RESET)
    print(Fore.YELLOW + "Welcome to Movie Hub! Your ultimate destination for movie browsing, ticket booking, and more!\n" + Fore.RESET)

#-----------DB CONNECTION --

db_connection = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'cinemaHub'
}

#-------------------------------------------------------------------------------CHOICE MENU CODE --
#CHOOSE CINEMAHUB
def welcome_cinemahub():
    # TASK ID : 1
    options = [
        [1, "Signup/Register"],
        [2, "Login"],
        [3, "Browse"]
    ]
    
    # Print the table with options
    print(tabulate(options, headers=["Option", "Action"], tablefmt="grid"))
    
    # Input choice from user
    select_choice = int(input("\nEnter your choice [1, 2, or 3]: "))
    
    if select_choice not in [1, 2, 3]:
        print("Invalid choice. Please enter 1, 2, or 3.")
        return welcome_cinemahub()  
    
    return select_choice


#--------------------------------------------------------------------------------------- SIGN UP CODE --

#Validating Code For SignUp
def validate_username(username):
    if re.fullmatch(r"^[a-zA-Z0-9]{8,15}$", username):
        return True
    else:
        print("Invalid username. Must be 8-15 alphanumeric characters and containing at least one number [a-z A-Z 0-9].")
        return False

def validate_email(email):
    if re.fullmatch(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
        return True
    else:
        print("Invalid email format")
        return False

def validate_password(password):
    if re.fullmatch(r"^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{8,}$", password):
        return True
    else:
        print("Invalid password. Must be at least 8 characters, containing at least one number and one special symbol [!@#$%^&*].")
        return False

#SIGNUP CODE  
def signupUser():
    print("SignUp Here")
    print("Username Must be of 8-15 alphanumeric characters and containing at least one number [a-z A-Z 0-9].")
    uname=input("Enter the UserName:")
    while not validate_username(uname):
        uname = input("Enter the UserName:")
    fname=input("Enter the First Name:")
    lname=input("Enter the Lirst Name:")
    
    email=input("Enter the Email Address:")
    while not validate_email(email):
        email = input("Enter your Email Address:")
    print("Must be at least 8 characters, containing at least one number and one special symbol [!@#$%^&*].")
    passwd = getpass.getpass("Enter your password: ")
    while not validate_password(passwd):
        passwd = input("Enter your Password:")
    roles=int(input("Enter the role(admin=0 / user=1)"))
    
        

    key = Fernet.generate_key()
    f = Fernet(key)
    passwd = f.encrypt(passwd.encode())
    passwd

    try:
        conn = mysql.connector.connect(**db_connection)
        cursor = conn.cursor()

        

        cursor.execute("insert into cinemahub.userinfo(username,password,fname,lname,email,encrypt_key,role) values(%s,%s,%s,%s,%s,%s,%s)",(uname,passwd,fname,lname,email,key,roles))
        print("You Regestired Succesfully ...")
        conn.commit()
        loginpage()
        conn.close()
        
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        if conn.is_connected():
            cursor.close()
            conn.close()
    
    
#--------------------------------------------------------------------------------  LOGIN PAGE CODE --   
#LOGIN PAGE CODE
def loginpage():
    print("Enter Your Login Details")
    username = input("Enter username: ")
    password = getpass.getpass("Enter your password: ")

    try:
        conn = mysql.connector.connect(**db_connection)
        cursor = conn.cursor()

        cursor.execute("SELECT password, encrypt_key, role, username FROM userinfo WHERE BINARY username = %s", (username,))
        userinputes = cursor.fetchone()

        
        if userinputes:
            passwd, key, role, stored_username = userinputes
            f = Fernet(key)

            
            decrypt_pass = f.decrypt(passwd).decode()

            
            if decrypt_pass == password:
                print(f"Welcome {stored_username}!")

                
                if role == 0:  
                    adminMenu(stored_username)
                else:  
                    userMenu()
            else:
                print("Incorrect password!")
                loginpage()
        else:
            print("Username not found!")
            loginpage()

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        if conn.is_connected():
            cursor.close()
            conn.close()
            
#------------------------------------------------------------------------------------------------ THEATER CODE --
#SHOW THEATER           
def showTheater(username):
    
    try:
        conn = mysql.connector.connect(**db_connection)
        cursor = conn.cursor()

        
        cursor.execute("SELECT theater_id,theater_name from cinemahub.theater")
        dis_theater = cursor.fetchall()
        
        headers = ["theater_id", "theater_name"]
        print(tabulate(dis_theater, headers=headers, tablefmt="fancy_grid"))
        
        print(dis_theater)
        conn.commit()

        print("Theater displayed successfully.")
        
        #adminMenu(username)  
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

#ADD THEATER ...         
def addTheater(username):
    tid=str(uuid.uuid4())
    tname=input("Enter the Theater Name:")
    tlocation=input("Enter the Theater Location:")
    tscreen=input("Enter the Theater Screen avaible:")
    tstatus=input("Enter the Theater Status(Open/Close):")
    tcapacity=input("Enter the Theater Capacity:")
    tlayout=input("Enter the Theater Layout:")
    tadd_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        conn = mysql.connector.connect(**db_connection)
        cursor = conn.cursor()

        
        sqlTheater="INSERT INTO theater (theater_uuid, theater_name, theater_location, theater_screen, theater_status, theater_capacity, theater_layout, theater_add_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        print(sqlTheater,tid, tname, tlocation, tscreen, tstatus, tcapacity, tlayout, tadd_date)
        cursor.execute(sqlTheater, (tid, tname, tlocation, tscreen, tstatus, tcapacity, tlayout, tadd_date))
        print("YOU ADDED THEATER DEATILS SUCCESFULLY ...")
        conn.commit()
        
        adminMenu(username)
        
        conn.close()
        
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        if conn.is_connected():
            cursor.close()
            conn.close()

#DELETE THEATER
def deleteTheater(username):
    print("\nHere are the list of all Theaters. Type the Theater ID you want to delete:\n")
    showTheater(username)
    
    deleteTheaterId = input("Enter the Theater ID to be deleted: ")

    try:
        conn = mysql.connector.connect(**db_connection)
        cursor = conn.cursor()

        cursor.execute("SELECT theater_id FROM theater WHERE theater_id = %s", (deleteTheaterId,))
        result = cursor.fetchone()

        if result is None:
            print("\nTheater ID does not exist. Please enter a valid Theater ID.")
        else:
            cursor.execute("DELETE FROM theater WHERE theater_id = %s", (deleteTheaterId,))
            conn.commit()

            
            cursor.execute("SELECT theater_id FROM theater WHERE theater_id = %s", (deleteTheaterId,))
            v_result = cursor.fetchone()
            
            if v_result is None:
                print("\nTheater deleted successfully.")
            else:
                print("Theater deletion failed. The theater still exists.")
        
        adminMenu(username)  

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            
#------------------------------------------------------------------------------------------------------ CINEMA CODE --
#ADD CINEMA

def addCinema(username):
    print("\nHere are the list of all Theaters. Type the Theater ID you want to add the Cinema for:\n")
    showTheater(username)  

    theater_id = input("Enter the Theater ID to add Cinema: ")

    try:
        conn = mysql.connector.connect(**db_connection)
        cursor = conn.cursor()

        cursor.execute("SELECT theater_uuid FROM theater WHERE theater_id = %s", (theater_id,))
        theater_result = cursor.fetchone()

        if theater_result is None:
            print("Theater ID does not exist. Please enter a valid Theater ID.")
        else:
            theater_uuid = theater_result[0]  
            print(f"Proceeding with the Cinema addition for Theater ID: {theater_id}")

            print(theater_uuid)

            cinema_uuid = str(uuid.uuid4())  
            cinema_name = input("Enter the Cinema Name: ")
            cinema_title = input("Enter the Cinema Title: ")
            cinema_details = input("Enter Cinema Details: ")
            cinema_lang = input("Enter Cinema Language: ")
            cinema_date = input("Enter Cinema Date (YYYY-MM-DD): ")
            cinema_start_time = input("Enter Cinema Start Time (HH:MM): ")
            cinema_end_time = input("Enter Cinema End Time (HH:MM): ")
            cinema_duration = input("Enter Cinema Duration (in minutes): ")
            cinema_type = input("Enter Cinema Type : ")
            cinema_cost = float(input("Enter Cinema Cost (Ticket Price): "))
            cinema_add_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S')

           
            sql = """INSERT INTO cinema 
                     (cinema_uuid, cinema_name, cinema_title, cinema_details, cinema_lang, cinema_date, cinema_start_time, 
                     cinema_end_time, cinema_duration, cinema_type, cinema_cost,cinema_add_date,cinema_theater_uuid)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            
            cursor.execute(sql, (cinema_uuid, cinema_name, cinema_title, cinema_details, cinema_lang, cinema_date, 
                                 cinema_start_time, cinema_end_time, cinema_duration, cinema_type, cinema_cost,cinema_add_date,theater_uuid))

            
            conn.commit()
            print("Cinema added successfully!")

        
        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        if conn.is_connected():
            cursor.close()
            conn.close()

#DELETE CINEMA
def deleteCinema(username):
    print("\nHere are the list of all Cinemas. Type the Cinema ID you want to delete:\n")
    showCinema(username)  
    
    deleteCinemaId = input("Enter the Cinema ID to be deleted: ")

    try:
        conn = mysql.connector.connect(**db_connection)
        cursor = conn.cursor()

        cursor.execute("SELECT cinema_id FROM cinema WHERE cinema_id = %s", (deleteCinemaId,))
        result = cursor.fetchone()

        if result is None:
            print("\nCinema ID does not exist. Please enter a valid Cinema ID.")
        else:
            cursor.execute("DELETE FROM cinema WHERE cinema_id = %s", (deleteCinemaId,))
            conn.commit()

            cursor.execute("SELECT cinema_id FROM cinema WHERE cinema_id = %s", (deleteCinemaId,))
            v_result = cursor.fetchone()

            if v_result is None:
                print("\nCinema deleted successfully.\n")
            else:
                print("Cinema deletion failed. The cinema is still exists.")

        adminMenu(username)

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# SHOW CINEMA 
def showCinema(username):
    try:
        conn = mysql.connector.connect(**db_connection)
        cursor = conn.cursor()

        cursor.execute("SELECT cinema_id, cinema_name, cinema_title FROM cinema")
        dis_cinema = cursor.fetchall()

        headers = ["Cinema ID", "Cinema Name", "Cinema Title"]
        print(tabulate(dis_cinema, headers=headers, tablefmt="fancy_grid"))

        conn.commit()

        print("Cinema displayed successfully.")
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


#ADD CINEMA SHOWS

def addCinemaShows(username):
    print("\nHere are the list of all Theaters:\n")
    showTheater(username)
    
    selectTheaterId = input("\nEnter the Theater ID to be Selected: ")

    try:
        conn = mysql.connector.connect(**db_connection)
        cursor = conn.cursor()

        cursor.execute("""SELECT t.theater_id, t.theater_name, c.cinema_id, c.cinema_name, c.cinema_title FROM theater t 
                          JOIN cinema c ON t.theater_uuid = c.cinema_theater_uuid WHERE t.theater_id = %s""", (selectTheaterId,))
        
        result = cursor.fetchall()

        if not result:
            print("\nNo cinema data found for the selected Theater ID. Please try again.")
        else:
            print(f"\nSelected Theater and Cinema Details for Theater ID {selectTheaterId}:\n")
            
            theater_data = []
            for row in result:
                theater_id, theater_name, cinema_id, cinema_name, cinema_title = row
                theater_data.append([theater_id, theater_name, cinema_id, cinema_name])

            headers = ["Theater ID", "Theater Name", "Cinema ID", "Cinema Name"]
            print(tabulate(theater_data, headers=headers, tablefmt='fancy_grid'))

            selectCinemaId = input("\nEnter the Cinema ID to be Selected: ")

            cursor.execute("""SELECT t.theater_id, t.theater_name, c.cinema_id, c.cinema_name 
                              FROM theater t JOIN cinema c ON t.theater_uuid = c.cinema_theater_uuid WHERE c.cinema_id = %s """, (selectCinemaId,))
            
            selectedCinemaResult = cursor.fetchone()

            if selectedCinemaResult:
                theater_id, theater_name, cinema_id, cinema_name = selectedCinemaResult
                print(f"\nSelected Cinema ID : {selectCinemaId} Details:")
                selectedCinemaData = [[theater_id, theater_name, cinema_id, cinema_name]]
                print(tabulate(selectedCinemaData, headers=["Theater ID", "Theater Name", "Cinema ID", "Cinema Name"], tablefmt='fancy_grid'))

                
                cursor.execute("""SELECT t.theater_name, t.theater_screen, t.theater_start_time, t.theater_end_time, 
                                  c.cinema_name, c.cinema_duration 
                                  FROM theater t 
                                  JOIN cinema c ON t.theater_uuid = c.cinema_theater_uuid 
                                  WHERE c.cinema_id = %s""", (selectCinemaId,))

                show_details = cursor.fetchall()

                if show_details:
                    print(f"\nShow Details for Selected Cinema ID {selectCinemaId}:\n")
                    show_data = []
                    for show in show_details:
                        theater_name, theater_screen, theater_start_time, theater_end_time, cinema_name, _cinema_duration = show
                        show_data.append([theater_name, theater_screen, theater_start_time, theater_end_time, cinema_name, _cinema_duration])

                    show_headers = ["Theater Name", "Theater Screen", "Start Time", "End Time", "Cinema Name", "Cinema Duration"]
                    print(tabulate(show_data, headers=show_headers, tablefmt='fancy_grid'))

                    scheduleShows(theater_id, cinema_id, cinema_name)
                else:
                    print("\nNo show details found for the selected Cinema.")
            else:
                print("\nInvalid Cinema ID selected.")

            

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn:
            conn.close()


def scheduleShows(theater_id, cinema_id, cinema_name):
    try:
        
        conn = mysql.connector.connect(**db_connection)
        cursor = conn.cursor()

        
        cursor.execute("""SELECT t.theater_uuid, c.cinema_uuid FROM theater t JOIN cinema c ON t.theater_uuid = c.cinema_theater_uuid WHERE t.theater_id = %s AND c.cinema_id = %s """, (theater_id, cinema_id))

        result = cursor.fetchone()

        if result:
            theater_uuid, cinema_uuid = result

            
            num_shows = int(input(f"\nEnter the number of shows for Cinema '{cinema_name}' (Cinema ID: {cinema_id}): "))

            
            for i in range(num_shows):
                print(f"\n--- Show {i+1} ---")
                start_time = input("Enter the Start Time for Show (YYYY-MM-DD HH:MM:SS): ")
                end_time = input("Enter the End Time for Show (YYYY-MM-DD HH:MM:SS): ")
                screen_number = int(input("Enter the Screen Number: "))
                seats_available = int(input("Enter the number of seats available: "))

                show_time = start_time  

                
                cursor.execute("""
                    INSERT INTO shows (theater_uuid, cinema_uuid, screen_number, show_time, seats_available, status)
                    VALUES (%s, %s, %s, %s, %s, 'Scheduled')
                """, (theater_uuid, cinema_uuid, screen_number, show_time, seats_available))

            
            conn.commit()

            
            print(f"\n{num_shows} shows successfully scheduled for Cinema '{cinema_name}' (Cinema ID: {cinema_id}).")
            
            
            cursor.execute("""SELECT t.theater_name, c.cinema_name, s.show_time, s.seats_available, s.screen_number, s.status FROM shows s JOIN theater t ON s.theater_uuid = t.theater_uuid JOIN cinema c ON s.cinema_uuid = c.cinema_uuid WHERE t.theater_id = %s AND c.cinema_id = %s ORDER BY s.show_time """, (theater_id, cinema_id))

          
            shows = cursor.fetchall()

            
            if shows:
                print(f"\nScheduled Shows for Cinema '{cinema_name}' (Cinema ID: {cinema_id}):")
                show_data = []
                for show in shows:
                    theater_name, cinema_name, show_time, seats_available, screen_number, status = show
                    show_data.append([theater_name, cinema_name, show_time, seats_available, screen_number, status])

                show_headers = ["Theater Name", "Cinema Name", "Show Time", "Seats Available", "Screen Number", "Status"]
                print(tabulate(show_data, headers=show_headers, tablefmt='fancy_grid'))
            else:
                print("\nNo scheduled shows found for this Cinema.")

        else:
            print("\nNo data found for the provided Theater ID and Cinema ID combination.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if conn:
            conn.close()
        
        


def displaySchedule(username):
    print("\nHere are the list of all Theaters:\n")
    
    try:
        conn = mysql.connector.connect(**db_connection)
        cursor = conn.cursor()

        
        cursor.execute("SELECT theater_id, theater_name FROM theater")
        theaters = cursor.fetchall()

        if not theaters:
            print("No theaters available.")
            return
        
        
        theater_headers = ["Theater ID", "Theater Name"]
        print(tabulate(theaters, headers=theater_headers, tablefmt='fancy_grid'))

        
        selectTheaterId = input("\nEnter the Theater ID to view schedule: ")

        
        cursor.execute("""SELECT cinema_id, cinema_name FROM cinema 
                          WHERE cinema_theater_uuid = (SELECT theater_uuid FROM theater WHERE theater_id = %s)""",
                       (selectTheaterId,))
        cinemas = cursor.fetchall()

        if not cinemas:
            print("\nNo cinemas available for the selected Theater ID.")
            return
        
       
        cinema_headers = ["Cinema ID", "Cinema Name"]
        print(tabulate(cinemas, headers=cinema_headers, tablefmt='fancy_grid'))

        
        selectCinemaId = input("\nEnter the Cinema ID to view show schedule: ")

        
        cursor.execute("""SELECT t.theater_name, c.cinema_name, s.show_time, s.seats_available, s.screen_number, s.status 
                          FROM shows s
                          JOIN theater t ON s.theater_uuid = t.theater_uuid
                          JOIN cinema c ON s.cinema_uuid = c.cinema_uuid
                          WHERE t.theater_id = %s AND c.cinema_id = %s
                          ORDER BY s.show_time""",
                       (selectTheaterId, selectCinemaId))
        shows = cursor.fetchall()

        if shows:
            show_headers = ["Theater Name", "Cinema Name", "Show Time", "Seats Available", "Screen Number", "Status"]
            print("\nScheduled Shows for the selected cinema:")
            print(tabulate(shows, headers=show_headers, tablefmt='fancy_grid'))
        else:
            print("\nNo scheduled shows found for the selected cinema.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if conn:
            conn.close()





def deleteShows(username):
    print("\nDelete Shows by Selecting Theater and Cinema:\n")

    try:
        conn = mysql.connector.connect(**db_connection)
        cursor = conn.cursor()

    
        cursor.execute("SELECT theater_id, theater_name FROM theater")
        theaters = cursor.fetchall()

        if not theaters:
            print("No theaters available.")
            return


        theater_headers = ["Theater ID", "Theater Name"]
        print(tabulate(theaters, headers=theater_headers, tablefmt='fancy_grid'))

    
        selectTheaterId = input("\nEnter the Theater ID to view schedule: ")

        
        cursor.execute("""SELECT cinema_id, cinema_name FROM cinema WHERE cinema_theater_uuid = (SELECT theater_uuid FROM theater WHERE theater_id = %s)""",(selectTheaterId,))
        cinemas = cursor.fetchall()

        if not cinemas:
            print("\nNo cinemas available for the selected Theater ID.")
            return

        cinema_headers = ["Cinema ID", "Cinema Name"]
        print(tabulate(cinemas, headers=cinema_headers, tablefmt='fancy_grid'))


        selectCinemaId = input("\nEnter the Cinema ID to display show schedule: ")

        
        cursor.execute("""SELECT s.show_id, t.theater_name, c.cinema_name, s.show_time,s.seats_available, s.screen_number, s.status FROM shows s JOIN theater t ON s.theater_uuid = t.theater_uuid JOIN cinema c ON s.cinema_uuid = c.cinema_uuid WHERE t.theater_id = %s AND c.cinema_id = %s ORDER BY s.show_time""",(selectTheaterId, selectCinemaId))
        shows = cursor.fetchall()

        if shows:
            show_headers = ["Show ID", "Theater Name", "Cinema Name", "Show Time", "Seats Available", "Screen Number", "Status"]
            print("\nScheduled Shows for the selected cinema:")
            print(tabulate(shows, headers=show_headers, tablefmt='fancy_grid'))
            
            deleteShowId = input("\nEnter the Show ID to delete: ")

            cursor.execute("DELETE FROM shows WHERE show_id = %s", (deleteShowId,))
            conn.commit()
            print("\nShow deleted successfully.")

        else:
            print("\nNo scheduled shows found for the selected cinema.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if conn:
            conn.close()
   


    
    
#--------------------------------------------------------------------------------------------- USER AND ADMIN CODE --

                       
#USER MENU
def userMenu():
    print(f"Welcome user {username}")


#ADMIN MENU    
def adminMenu(username):
    while True:
        print(f"Welcome admin {username}\n")

        menu_options = [
            ["0", "Show Theater"],
            ["1", "Add Theater"],
            ["2", "Delete Theater"],
            ["3", "Add Movie"],
            ["4", "Delete Movie"],
            ["5", "Set Seat Price"],
            ["6", "Set Theater Shutdown Time"],
            ["7", "View Bookings"],
            ["8", "Add Cinema Shows "],
            ["9", "Delete Cinema Shows "],
            ["10", "Add Shows Cimema Schedule "],
            ["11", "Delete Cimema Schedule Shows"],
            ["exit", "Exit"]
        ]

        # Display the menu in table format
        print(tabulate(menu_options, headers=["Option", "Menu"], tablefmt="fancy_grid"))

        # Get the user's choice
        adminch = input("Enter your Option:(0-11):")
        
        if adminch == '0':
            showTheater(username)
        elif adminch == '1':
            addTheater(username)
        elif adminch == '2':
            deleteTheater(username)
        elif adminch == '3':
            addCinema(username)
        elif adminch == '4':
            deleteCinema(username)
        elif adminch == '5':
            setSeatPrice(username)
        elif adminch == '6':
            setShutdownTime(username)
        elif adminch == '7':
            viewBookings(username)
        elif adminch == '8':
            addCinemaShows(username)
        elif adminch == '9':
            deleteCinemaShows(username)
        elif adminch == '10':
            displaySchedule(username)
        elif adminch == '11':
            deleteShows(username)
        elif adminch == 'exit':
            print("You exited the ADMIN MENU ...")
            break
        else:
            print("Invalid Choice")
           
            

#----------------------------------- CALLING FUNCTION --    
display_cinema_hub()
choice = welcome_cinemahub()

if choice == 1:
    signupUser()
elif choice == 2:
    loginpage()
elif choice == 3:
    print("Browsing ...")













































