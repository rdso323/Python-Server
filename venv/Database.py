import sqlite3

def StoreUsers(username,ip,location,lastLogin,port):
    connection = sqlite3.connect("StoreUsers.db")
    cursor = connection.cursor()

    cursor.execute("DELETE FROM OnlineUsers")           #Delete previous entries each time

    sql_command = """
    CREATE TABLE IF NOT EXISTS OnlineUsers ( 
    UPI TEXT, 
    IP  TEXT, 
    Location INT, 
    Port INT, 
    Last_Login INT);"""

    cursor.execute(sql_command)

    cursor = connection.cursor()

 #   print(input_data)
    #user_data = [("rdso323", "10.07.07", "2", "10007", "1507328626")]
    # for x in len(0,username):
    #     user_data = username[x]+

    #print(input_data)
    for k in range(0,len(username)):
        user_data = [(username[k],ip[k],location[k],lastLogin[k],port[k])]

        for p in user_data:
            format_str = """INSERT INTO OnlineUsers (UPI, IP, Location, Last_Login, Port) 
            VALUES ("{UPI}", "{IP}", "{Location}", "{Last_Login}", "{Port}");"""

            sql_command = format_str.format(UPI=p[0], IP=p[1], Location=p[2], Last_Login=p[3], Port=p[4],)
            cursor.execute(sql_command)


    #print(res)
    # never forget this, if you want the changes to be saved:
    connection.commit()

    connection.close()

def ExtractUsers():
    Users = []
    connection = sqlite3.connect("StoreUsers.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM OnlineUsers")
    res = cursor.fetchall()
    for i in range (0,len(res)):
        Users.append(res[i][0])
        print res[i][0]

    return ', '.join(Users)     #Convert list into a string


def ExtractMessage(sender,destination,message,stamp):
    connection = sqlite3.connect("StoreMessages.db")
    cursor = connection.cursor()

    sql_command = """
       CREATE TABLE IF NOT EXISTS Messages ( 
       Sender TEXT, 
       Destination, TEXT,
       Message  TEXT,
       Time_Stamp);"""

    cursor.execute(sql_command)

    cursor = connection.cursor()

    # print(input_data)
    user_data = [(sender, destination, message, stamp)]

    for p in user_data:
        format_str = """INSERT INTO OnlineUsers (Sender,Destination,Message,Time_Stamp) 
           VALUES ("{Sender}", "{Destination}", "{Message}", "{Time_Stamp}");"""

        sql_command = format_str.format(sender=p[0], destination=p[1], message=p[2], stamp=p[3])
        cursor.execute(sql_command)

    # print(res)
    # never forget this, if you want the changes to be saved:
    connection.commit()

    connection.close()