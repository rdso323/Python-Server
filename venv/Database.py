import sqlite3

def StoreUsers(username,ip,location,lastLogin,port):
    connection = sqlite3.connect("Database.db")
    cursor = connection.cursor()


    sql_command = """
    CREATE TABLE IF NOT EXISTS OnlineUsers ( 
    UPI TEXT, 
    IP  TEXT, 
    Location TEXT, 
    Port TEXT, 
    Last_Login TEXT);"""

    cursor.execute(sql_command)

    cursor.execute("DELETE FROM OnlineUsers")  # Delete previous entries each time



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
    connection = sqlite3.connect("Database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM OnlineUsers")
    res = cursor.fetchall()
    connection.close()
    for i in range (0,len(res)):
        Users.append(res[i][0])
        #print res[i][0]

    return ', '.join(Users)     #Convert list into a string


def StoreMessage(sender,destination,message,stamp):
    connection = sqlite3.connect("Database.db")
    cursor = connection.cursor()

    sql_command = """
       CREATE TABLE IF NOT EXISTS Messages ( 
       Sender TEXT, 
       Destination TEXT,
       Message  TEXT,
       Time_Stamp TEXT);"""

    cursor.execute(sql_command)

    cursor = connection.cursor()

    # print(input_data)
    # user_data = [(sender, destination, message, stamp)]
    #
    #
    # format_str = """INSERT INTO OnlineUsers (Sender,Destination,Message,Time_Stamp)
    #     VALUES ("{Sender}", "{Destination}", "{Message}", "{Time_Stamp}");"""
    #
    # sql_command = format_str.format(sender, destination, message, stamp)
    # cursor.execute(sql_command)

    cursor.execute('''INSERT INTO Messages(Sender, Destination, Message, Time_Stamp)
                      VALUES(?,?,?,?)''', (sender, destination, message, stamp))
    print('User inserted')

    # print(res)
    # never forget this, if you want the changes to be saved:
    connection.commit()

    connection.close()

def StoreFile(sender,destination,file,filename,content_type,stamp):
    connection = sqlite3.connect("Database.db")
    cursor = connection.cursor()

    sql_command = """
       CREATE TABLE IF NOT EXISTS Files ( 
       Sender TEXT, 
       Destination TEXT,
       File  TEXT,
       Filename TEXT,
       Content_Type TEXT,
       Time_Stamp TEXT);"""

    cursor.execute(sql_command)

    cursor = connection.cursor()

    cursor.execute('''INSERT INTO Files(Sender, Destination, File, Filename,Content_Type
                    ,Time_Stamp)
                VALUES(?,?,?,?,?,?)''', (sender, destination, file, filename, content_type, stamp))
    print('File inserted')

    connection.commit()

    connection.close()


def ExtractPort(ID):
    connection = sqlite3.connect("Database.db")
    cursor = connection.cursor()

    cursor.execute('''SELECT Port FROM OnlineUsers WHERE UPI=?''', (ID,))
    user = cursor.fetchone()
    connection.close()
    user = ''.join(user)
    return user


def ExtractIP(ID):
    connection = sqlite3.connect("Database.db")
    cursor = connection.cursor()

    cursor.execute('''SELECT IP FROM OnlineUsers WHERE UPI=?''', (ID,))
    user = cursor.fetchone()
    connection.close()
    user = ''.join(user)
    return user



def StoreProfile(timestamp,Name,Position,Location):

    connection = sqlite3.connect("Database.db")

    cursor = connection.cursor()

    sql_command = """
           CREATE TABLE IF NOT EXISTS Profile ( 
           Name TEXT, 
           Position TEXT,
           Location  TEXT,
           LastUpdated TEXT);"""

    cursor.execute(sql_command)

    cursor.execute("DELETE FROM Profile")  # Delete previous entries each time

    cursor = connection.cursor()

    cursor.execute('''INSERT INTO Profile(Name, Position, Location, LastUpdated)
                     VALUES(?,?,?,?)''',(Name, Position, Location, timestamp))

    print('Details inserted')

    connection.commit()

    connection.close()