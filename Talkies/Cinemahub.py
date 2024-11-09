import mysql.connector


db_connection = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',  
    'database': 'cinemaHub'
}


def loginpage():
    username = input("Enter username: ")
    password = input("Enter password: ")

    try:
        
        conn = mysql.connector.connect(**db_connection)
        cursor = conn.cursor()

        
        cursor.execute("SELECT * FROM userinfo WHERE username = %s AND password = %s", (username, password))
        userinputes = cursor.fetchone()

        if userinputes:
            print(f"Welcome {username}!")
        else:
            print("Invalid username or password.")

       
        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        if conn.is_connected():
            cursor.close()
            conn.close()


loginpage()
