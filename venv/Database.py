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

    cursor.execute("DELETE FROM OnlineUsers")                                   #Delete previous entries each time

    cursor = connection.cursor()

    for k in range(0,len(username)):
        user_data = [(username[k],ip[k],location[k],lastLogin[k],port[k])]
                                                                                                #Add online users 
        for p in user_data:                                                                     #to database 
            format_str = """INSERT INTO OnlineUsers (UPI, IP, Location, Last_Login, Port)                   
            VALUES ("{UPI}", "{IP}", "{Location}", "{Last_Login}", "{Port}");"""

            sql_command = format_str.format(UPI=p[0], IP=p[1], Location=p[2], Last_Login=p[3], Port=p[4],)
            cursor.execute(sql_command)

    # never forget this, if you want the changes to be saved:
    connection.commit()

    connection.close()

def ExtractUsers():
    Users = []
    connection = sqlite3.connect("Database.db")                                             #Extract UPI of all 
    cursor = connection.cursor()                                                            #online users to display
    cursor.execute("SELECT * FROM OnlineUsers")
    res = cursor.fetchall()
    connection.close()
    for i in range (0,len(res)):
        Users.append(res[i][0])

    return Users


def StoreMessage(sender,destination,message,stamp,status):
    connection = sqlite3.connect("Database.db")
    cursor = connection.cursor()

    sql_command = """
       CREATE TABLE IF NOT EXISTS Messages ( 
       Sender TEXT, 
       Destination TEXT,
       Message  TEXT,
       Time_Stamp TEXT,
       Status Text);"""

    cursor.execute(sql_command)

    cursor = connection.cursor()                                                                #Store new messages
                                                                                                #into a database

    cursor.execute('''INSERT INTO Messages(Sender, Destination, Message, Time_Stamp, Status)    
                      VALUES(?,?,?,?,?)''', (sender, destination, message, stamp, status))
    print('User inserted')

    # never forget this, if you want the changes to be saved:
    connection.commit()

    connection.close()

def StoreFile(sender,destination,file,filename,content_type,stamp,status):
    connection = sqlite3.connect("Database.db")
    cursor = connection.cursor()                                                                #Store new files
                                                                                                #into a database
    sql_command = """
       CREATE TABLE IF NOT EXISTS Files ( 
       Sender TEXT,                                                                                 
       Destination TEXT,
       File  TEXT,
       Filename TEXT,
       Content_Type TEXT,
       Time_Stamp TEXT,
       Status TEXT);"""

    cursor.execute(sql_command)

    cursor = connection.cursor()

    cursor.execute('''INSERT INTO Files(Sender, Destination, File, Filename,Content_Type
                    ,Time_Stamp,Status)
                VALUES(?,?,?,?,?,?,?)''', (sender, destination, file, filename, content_type, stamp, status))
    print('File inserted')

    connection.commit()

    connection.close()


def ExtractPort(ID):
    connection = sqlite3.connect("Database.db")
    fetch = connection.cursor()                                                             #Extract port based on
    connection.text_factory = str                                                           #user UPI
    fetch.execute('''SELECT Port FROM OnlineUsers WHERE UPI=?''', (ID,))
    user = fetch.fetchone()[0]
    connection.close()
    #user = ''.join(user)
    return user


def ExtractIP(ID):
    connection = sqlite3.connect("Database.db")                                             #Extract IP based on
    fetch = connection.cursor()                                                             #user UPI
    connection.text_factory = str
    fetch.execute('''SELECT IP FROM OnlineUsers WHERE UPI=?''', (ID,))
    user = fetch.fetchone()[0]
    connection.close()
    return user



def StoreProfile(timestamp,Name,Position,Location):

    connection = sqlite3.connect("Database.db")                                             #Store updated profile 
                                                                                            #details
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


def ExtractProfile():
    connection = sqlite3.connect("Database.db")                                 #Extract user profile details          
    cursor = connection.cursor()
    
    
    try:
        cursor.execute('''SELECT Name FROM Profile ''')                         #Retrieve required tuples if possible
        Name = cursor.fetchall()
    except:
        Name = "0"
    try:
        cursor.execute('''SELECT Position FROM Profile ''')
        Position = cursor.fetchall()
    except:
        Position = "0"
    try:
        cursor.execute('''SELECT Location FROM Profile ''')
        Location = cursor.fetchall()
    except:
        Location = "0"
    try:
        cursor.execute('''SELECT LastUpdated FROM Profile ''')
        LastUpdated = cursor.fetchall()
    except:
        LastUpdated = "0"

    connection.close()
    user = dict([("lastUpdated",''.join(LastUpdated[0])),("fullname",''.join(Name[0])), #Convert tuples into one dictionary
                  ("position",''.join(Position[0])),("location", ''.join(Location[0]))])
    return user


def ExtractMessages():                                                      #Extract & display last 15 messages
    
        Messages = []
        connection = sqlite3.connect("Database.db")
        cursor = connection.cursor()                                            #Extract messages to display
        
        sql_command = """
       CREATE TABLE IF NOT EXISTS Messages ( 
       Sender TEXT, 
       Destination TEXT,
       Message  TEXT,
       Time_Stamp TEXT,
       Status Text);"""
       
        cursor.execute(sql_command)

        cursor = connection.cursor()
       
        cursor.execute('''SELECT Sender, Destination, Message, Status FROM Messages''')
        res = cursor.fetchall()
        connection.close()
        
        if(len(res)==0):                                                        # If fields are empty 
            Messages.append("None available")                                   # return "None "available"
            return Messages
        
        if(len(res)>15):
            length = 15
        else:
            length = len(res)
        for i in range (0,length):
            Messages.append(res[len(res)-i-1][0] + " : " + res[len(res)-i-1][1]
                            + " : " + res[len(res)-i-1][2] + " - " + res[len(res)-i-1][3])
        return Messages

def ExtractFiles():
        Files = []                                                      #Extract & display last 5 files
        connection = sqlite3.connect("Database.db")
        cursor = connection.cursor()
        
        sql_command = """
       CREATE TABLE IF NOT EXISTS Files ( 
       Sender TEXT, 
       Destination TEXT,
       File  TEXT,
       Filename TEXT,
       Content_Type TEXT,
       Time_Stamp TEXT,
       Status TEXT);"""
       
        cursor.execute(sql_command)

        cursor = connection.cursor()
        
        cursor.execute('''SELECT Sender, Destination, Filename, Status FROM Files''')
        res = cursor.fetchall()
        connection.close()
        
        if(len(res)==0):                                                            # If fields are empty
            Files.append("None available")                                          # return "None "available"
            return Files
           
        if(len(res)>10):
            length = 10
        else:
            length = len(res)
        for i in range (0,length):
            Files.append(res[len(res)-i-1][0] + " : " + res[len(res)-i-1][1] + " : " +
                         res[len(res)-i-1][2] + " - " + res[len(res)-i-1][3])
        return Files
    
def ExtractFileName():
        Files = []                                                      #Extract & display last 5 filenames
        connection = sqlite3.connect("Database.db")
        cursor = connection.cursor()
        
        sql_command = """
       CREATE TABLE IF NOT EXISTS Files ( 
       Sender TEXT, 
       Destination TEXT,
       File  TEXT,
       Filename TEXT,
       Content_Type TEXT,
       Time_Stamp TEXT,
       Status TEXT);"""
       
        cursor.execute(sql_command)
        
        cursor = connection.cursor()
        
        cursor.execute('''SELECT Filename FROM Files''')
        res = cursor.fetchall()
        connection.close()
        
        if(len(res)==0):                                                        # If fields are empty
            Files.append("None available")                                      # return "None "available"
            return Files
        
        if(len(res)>10):
            length = 10
        else:
            length = len(res)
        for i in range (0,length):
            Files.append(res[len(res)-i-1][0])

        return Files
