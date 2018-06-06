#!/usr/bin/python
""" cherrypy_example.py

    COMPSYS302 - Software Design
    Author: Andrew Chen (andrew.chen@auckland.ac.nz)
    Last Edited: 19/02/2018

    This program uses the CherryPy web server (from www.cherrypy.org).
"""
# Requires:  CherryPy 3.2.2  (www.cherrypy.org)
#            Python  (We use 2.7)

import cherrypy
import urllib
import urllib2
import hashlib
import socket
import json
import Database
import os,os.path
import base64
import time
import threading
import datetime
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader(""))
global count
count = 0


# The address we listen for connections on
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip = (s.getsockname()[0])			#Attain IP
s.close()

listen_ip = '0.0.0.0'
listen_port = 10007


class MainApp(object):

    #CherryPy Configuration
    _cp_config = {'tools.encode.on': True,
                  'tools.encode.encoding': 'utf-8',
                  'tools.sessions.on' : 'True',
                 }

    # If they try somewhere we don't know, catch it here and send them to the right place.
    @cherrypy.expose
    def default(self, *args, **kwargs):
        """The default page, given when we don't recognise where the request is for."""
        Page = "I don't know where you're trying to go, so have a 404 Error."
        cherrypy.response.status = 404
        return Page

    # PAGES (which return HTML that can be viewed in browser)
    @cherrypy.expose
    def index(self):
        try:
            username = cherrypy.session['username']
            if(count==0):                                       #Only for first Login
                self.TracktoMain()                              # Prevent timing out
                global count
                count = 1
            Users = self.UserDisplay()
            return env.get_template('Main_Screen.html').render(username=username, Users=Users)
            Page = file('Main_Screen.html')
        except KeyError: #There is no username
            Page = "Welcome to the COMPSYS302 Login Page!<br/>"
            Page += "Click here to <a href='login'>Login</a>"
        return Page

    @cherrypy.expose
    def TracktoMain(self):                                      #Prevent timing out
        if(LogIn == 1):                                         #Ensure user can't stay logged in once logged out
            respdata = urllib2.urlopen(Login_url).read()        #Call log in IP
            print(respdata)
            threading.Timer(30, self.TracktoMain).start()      #Set timer to call function every 30 seconds

    @cherrypy.expose
    def login(self):
        Page = file('SignIn.html')                              #Html for logging in  
        return Page

    @cherrypy.expose			#Display users online
    def UserDisplay(self):
        url = 'http://cs302.pythonanywhere.com/getList?'
        values = {'username': 'rdso323',
                  'password': '8f61a0b4911467540cd6df03e59e40d041323bc8beb1a3744e22bf4e7458b869',
                  'enc': '0',
                  'json': '1'}

        data = urllib.urlencode(values)                           #Set values in dictionary together (Seperated with &)
        respdata = urllib2.urlopen(url + data).read()             #Call log in API
        input_data = json.loads(respdata)


        username= []					           #Create lists
        ip = []
        location = []
        lastLogin = []
        port = []

        for x in range (0,len(input_data)):                        #Store respective information in lists
            username.append(input_data[str(x)]['username'])
            ip.append(input_data[str(x)]['ip'])
            location.append(input_data[str(x)]['location'])
            lastLogin.append(input_data[str(x)]['lastLogin'])
            port.append(input_data[str(x)]['port'])

        Database.StoreUsers(username,ip,location,lastLogin,port)   #Store the users in a database
        Users = Database.ExtractUsers()
        return Users

    @cherrypy.expose
    def sum(self, a=0, b=0):                                        #All inputs are strings by default
        output = int(a)+int(b)
        return str(output)

    # LOGGING IN AND OUT
    @cherrypy.expose
    def signin(self, username=None, password=None):
        """Check their name and password and send them either to the main page, or back to the main login screen."""
        error = self.authoriseUserLogin(username,password)
        if (error == 0):                                            #If signin is possible
            global LogIn
            LogIn = 1
            cherrypy.session['username'] = username;                #Store username & password
            cherrypy.session['password'] = password;
            raise cherrypy.HTTPRedirect('/')
        else:
            raise cherrypy.HTTPRedirect('/login')

    @cherrypy.expose
    def signout(self):
        """Logs the current user out, expires their session"""

        username = cherrypy.session.get('username')
        password = cherrypy.session.get('password')
        password_hash = hashlib.sha256(password + username).hexdigest()  # Hash the password

        url = 'http://cs302.pythonanywhere.com/logoff?'
        values = {'username': username,
                  'password': password_hash,
                  'enc': '0'}

        if (username == None):
            pass
        else:
            data = urllib.urlencode(values)                           # Set values in dictionary together (Seperated with &)
            respdata = urllib2.urlopen(url + data).read()
            cherrypy.lib.sessions.expire()
        global LogIn
        LogIn = 0                                                       #Stop calling Login API
        global count
        count = 0                                                       #Allow function to be called next log in 
        raise cherrypy.HTTPRedirect('/')

    def authoriseUserLogin(self, username, password):
        print username
        print password
        password_hash = hashlib.sha256(password+username).hexdigest()	  #Hash the password
        if(ip.count('10.103')>0):
            location = 0
        elif(ip.count('172.2')>0):
            location = 1
        else:
            location = 2

        url = 'http://cs302.pythonanywhere.com/report?'
        values = {'username' : username,
            'password' : password_hash,
            'location' : location,
            'ip' : ip,	#'10.0.2.15',
            'port' : listen_port,
            'enc' : '0'}
        try:
            data = urllib.urlencode(values)			  #Set values in dictionary together (Seperated with &)
            global Login_url
            Login_url = url + data
            respdata = urllib2.urlopen(url+data).read()
            if(respdata.count('0')>=1):                            #Check if login was succesful 
                return 0
            elif(respdata.count('1')>=0):
                return 1

        except Exception as e:
            return 1

    @cherrypy.expose
    def ping(self,sender):                                          #Call ping
        print 'ping working'
        return '0'


    @cherrypy.expose
    def composeMessage(self):                                                   
        Messages = Database.ExtractMessages()                               #Extract last 15 message from database
        return env.get_template('Message.html').render(Messages=Messages)
        Page = file('Message.html')                                         #Open html
        return Page

    @cherrypy.expose
    def composeFile(self):
        Files = Database.ExtractFiles()                                     #Extract last 15 file details and name
        Filename = Database.ExtractFileName()
        Length = len(Files)
        return env.get_template('Files.html').render(Files=Files,Filename=Filename,Len=Length)
        Page = file('Files.html')                                           #Pass into html to print
        return Page


    @cherrypy.expose
    def sendMessage(self,UPI,Message):
        output = {"sender":cherrypy.session['username'],"destination":UPI,          #Create a dictionary to send
                  "message":Message,"stamp":time.time()}

        data = json.dumps(output)                                                   
        try:
            IP = Database.ExtractIP(UPI)                                            #Find the desired users IP & Port
            Port = Database.ExtractPort(UPI)
        except:
            Database.StoreMessage(output['sender'], output['destination'], output['message'],   #If not possible set 
                                  output['stamp'], "Failed")                                    #status to failed
            return "User not in database"

        URL = 'http://' + IP + ':' + Port + '/receiveMessage'

        req = urllib2.Request(URL, data, {'Content-Type': 'application/json'})     
        
        try:
            response = urllib2.urlopen(req).read()                                              #Call the API
        except:
            Database.StoreMessage(output['sender'], output['destination'], output['message'],   
                                                                                                
                                  output['stamp'], "Failed")
            return "Delivery Failed"
    
        if (response.count('0') >= 1):                                                          #Check if message is sent
            Database.StoreMessage(output['sender'], output['destination'], output['message'],   #succesfully
                            output['stamp'], "Delivered")
        else:
            Database.StoreMessage(output['sender'], output['destination'], output['message'],   #Otherwise the satus
                                                                                                #is failed
                                  output['stamp'], "Failed")
            return "Delivery Failed"

        return response


    @cherrypy.expose
    @cherrypy.tools.json_in()
    def receiveMessage(self):
        input_data = cherrypy.request.json
        Database.StoreMessage(input_data['sender'],input_data['destination'],input_data['message'],input_data['stamp'],"Received")                                                                                  #Store Message details
        return '0'                                                                              #in a database

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def receiveFile(self):                                                                          
        input_data = cherrypy.request.json
        Database.StoreFile(input_data['sender'], input_data['destination'], input_data['file'],     
                        input_data['filename'], input_data['content_type'], input_data['stamp'],
                           "Received")                                                          #Store file details
                                                                                                #in database
        file = base64.b64decode(input_data['file'])                                             
        path = "static/"
        filename = input_data['filename']
        full_path = os.path.join(path,filename)
        with open(full_path, 'wb') as f:                                                        #Decode file and write to a
            f.write(file)                                                                       #blank file
        return '0'

    @cherrypy.expose
    def sendFile(self,UPI,File):
        filename = File
        path = "static/"
        full_path = os.path.join(path,filename)
        with open(full_path, "rb") as image_file:                                               #Setup path and decode
            file = base64.b64encode(image_file.read())                                          #file
        output = {"sender":cherrypy.session.get('username'),"destination":UPI,
                  "file":file,"filename":filename,"content_type":'image/jpeg',"stamp":time.time()}  #Encode desire output
        data = json.dumps(output)

        try:
            IP = Database.ExtractIP(UPI)                                                        #Attempt to extract IP
            Port = Database.ExtractPort(UPI)                                                    #& Port
        except:
            Database.StoreFile(output['sender'], output['destination'], output['file'],         #Store file data
                               output['filename'], output['content_type'], output['stamp'],     #in database with a
                               "Failed")                                                        #fail status
            return "User not in database"


        URL = 'http://' + IP + ':' + Port + '/receiveFile'                                      

        req = urllib2.Request(URL, data, {'Content-Type': 'application/json'})                  #Call desired protocol
        
        try:
            response = urllib2.urlopen(req).read()
        except:
            Database.StoreFile(output['sender'], output['destination'], output['file'],
                               output['filename'], output['content_type'], output['stamp'],
                               "Failed")
            return "Delivery Failed"

        if (response.count('0') >= 1):                                                          #Check if file sent 
            Database.StoreFile(output['sender'], output['destination'], output['file'],         #successfully
                               output['filename'], output['content_type'], output['stamp'],
                               "Delivered")
        else:
            Database.StoreFile(output['sender'], output['destination'], output['file'],
                               output['filename'], output['content_type'], output['stamp'],
                               "Failed")
            return "Delivery Failed"

        return response


    @cherrypy.expose
    def InputProfile(self):                                                             #Page to display profile information
        Page = file('GetProfile.html')
        return Page

    @cherrypy.expose
    def CallProfile(self,UPI):                                                           
        Param = []                                                  
        output = {"profile_username": UPI,                                              #Create data to call 
                  "sender": cherrypy.session['username']}                               #Desired users profile
        data = json.dumps(output)
        try:
            IP = Database.ExtractIP(UPI)
            Port = Database.ExtractPort(UPI)
        except:
            return "Unretrievable"

        URL = 'http://' + IP + ':' + Port+ '/getProfile'                                

        req = urllib2.Request(URL, data, {'Content-Type': 'application/json'})          #Call getProfile API
        try:
            response = urllib2.urlopen(req).read()
        except:
            return "Unretrievable"
        
        response = json.loads(response)

        try:                                                                            #Try displaying user parameters
            Param.append("Name: "+response['fullname'])                                 #if possible
        except:
            Param.append("Name: N/A")
        try:
            Param.append("Position: "+response['position'])
        except:
            Param.append("Position: N/A")
        try:
            Param.append("Location: "+response['location'])
        except:
            Param.append("Location: N/A")
        
        Param.append("Last Fetched: "+ time.strftime("%D %H:%M", time.localtime(int(float(response['lastUpdated'])))))
        return env.get_template('DisplayProfile.html').render(Param=Param)

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def getProfile(self):
        output = Database.ExtractProfile()                                               #Extract details from database 
        data = json.dumps(output)                                                        #and return
        return data


    @cherrypy.expose
    def SaveProfile(self,Position,Name,Location):                                        #Save updated users bio
        Database.StoreProfile(time.time(),Name,Position,Location)
        return 'Details Updated'


def runMainApp():
    #Setup CSS
    conf = {                                                                              #Used to display unicode and  
        '/':{                                                                             #css
            'tools.sessions.on': True,                                  
            'tools.staticdir.root':os.path.abspath(os.getcwd()),
            'tools.encode.on': True,
            'tools.encode.encoding': 'utf-8',
        },
        '/static':{
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './static'
        }
    }

    # Create an instance of MainApp and tell Cherrypy to send all requests under / to it. (ie all of them)
    cherrypy.tree.mount(MainApp(), "/",conf)

    # Tell Cherrypy to listen for connections on the configured address and port.
    cherrypy.config.update({'server.socket_host': listen_ip,
                            'server.socket_port': listen_port,
                            'engine.autoreload.on': True,
                           })

    print "========================="
    print "University of Auckland"
    print "COMPSYS302 - Software Design Application"
    print "========================================"

    # Start the web server
    cherrypy.engine.start()

    # And stop doing anything else. Let the web server take over.
    cherrypy.engine.block()
 
#Run the function to start everything
runMainApp()
