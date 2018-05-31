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
import time




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
		Page = "Welcome to the COMPSYS302 Login Page!<br/>"

		try:
			Page += "Hello " + cherrypy.session['username'] + "!<br/>"
			Page += "Here is some bonus text because you've logged in! <br/><br/>"
			Page += "Online Users:<br/>"
			Page += self.UserDisplay()
			Page += "<br/><br/>Click here to <a href='signout'>Logout</a>."
			Page += "<br/>Click here to <a href='sendMessage'>send message</a>"
			#Page += "<br/>" + cherrypy.session['sender'] + ":" + cherrypy.session['message']
		except KeyError: #There is no username
			Page += "Click here to <a href='login'>Login</a>."
		return Page

	@cherrypy.expose
	def login(self):
		# Page = '<form action="/signin" method="post" enctype="multipart/form-data">'
		# Page += 'Username: <input type="text" name="username"/><br/>'
		# Page += 'Password: &nbsp<input type="password" name="password"/><br/><br/>'
		# Page += '<input type="submit" value="Login"/></form>'
		Page = file('Layout.html')
		return Page

	@cherrypy.expose			#Display users online
	def UserDisplay(self):
		url = 'http://cs302.pythonanywhere.com/getList?'
		values = {'username': 'rdso323',
				  'password': '8f61a0b4911467540cd6df03e59e40d041323bc8beb1a3744e22bf4e7458b869',
				  'enc': '0',
				  'json': '1'}

		data = urllib.urlencode(values)  # Set values in dictionary together (Seperated with &)
		respdata = urllib2.urlopen(url + data).read()
		input_data = json.loads(respdata)


		username= []					#Create a list
		ip = []
		location = []
		lastLogin = []
		port = []

		for x in range (0,len(input_data)):
			username.append(input_data[str(x)]['username'])
			ip.append(input_data[str(x)]['ip'])
			location.append(input_data[str(x)]['location'])
			lastLogin.append(input_data[str(x)]['lastLogin'])
			port.append(input_data[str(x)]['port'])


		#for x in range(0, len(username)):
			#print username[x]
			# print ip[x]
			# print location[x]
			# print lastLogin[x]
			# print port[x]

		Database.StoreUsers(username,ip,location,lastLogin,port)
		Users = Database.ExtractUsers()
		return Users

	@cherrypy.expose
	def sum(self, a=0, b=0): #All inputs are strings by default
		output = int(a)+int(b)
		return str(output)

	# LOGGING IN AND OUT
	@cherrypy.expose
	def signin(self, username=None, password=None):
		print 'hey'
		"""Check their name and password and send them either to the main page, or back to the main login screen."""
		error = self.authoriseUserLogin(username,password)
		if (error == 0):
			cherrypy.session['username'] = username;
			cherrypy.session['password'] = password;
			raise cherrypy.HTTPRedirect('/')
		else:
			raise cherrypy.HTTPRedirect('/login')

		#http://cs302.pythonanywhere.com/getList?username=rdso323&password=8f61a0b4911467540cd6df03e59e40d041323bc8beb1a3744e22bf4e7458b869&enc=0&json=0
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
			data = urllib.urlencode(values)  # Set values in dictionary together (Seperated with &)
			respdata = urllib2.urlopen(url + data).read()
			cherrypy.lib.sessions.expire()
		raise cherrypy.HTTPRedirect('/')

	def authoriseUserLogin(self, username, password):
		print username
		print password
		if (username.lower() == "rdso323") and (password.lower() == "remainnail"):
			password_hash = hashlib.sha256(password+username).hexdigest()			#Hash the password
			if(ip.count('10.103')>0):
				location = 0
			elif(ip.count('172.2')>0):
				location = 1
			else:
				location = 2

			print location
			url = 'http://cs302.pythonanywhere.com/report?'
			values = {'username' : username,
				'password' : password_hash,
				'location' : location,
				'ip' : ip,	#'10.0.2.15',
				'port' : listen_port,
				'enc' : '0'}
			print(location)
			try:
				data = urllib.urlencode(values)					#Set values in dictionary together (Seperated with &)
				respdata = urllib2.urlopen(url+data).read()
				#print(respdata)
				if(respdata.count('0')>=1):
					return 0
				elif(respdata.count('1')>=0):
					return 1

			except Exception as e:
				print(str(e))
				return 1

		else:
			return 1

	@cherrypy.expose
	def ping(self,sender):
		print 'ping working'
		return '0'


	@cherrypy.expose
	def sendMessage(self):
		output = {"sender":cherrypy.session['username'],"destination":'dtri722',
				  "message":'Suck a dick',"stamp":time.time()}

		data = json.dumps(output)
		IP = Database.ExtractIP('jpat331')
		Port = Database.ExtractPort('jpat331')

		URL = 'http://' + IP + ':' + Port+ '/receiveMessage'

		req = urllib2.Request(URL, data, {'Content-Type': 'application/json'})
		response = urllib2.urlopen(req)
		return response
	# 	cherrypy.session['sender'] = sender;
	# 	cherrypy.session['message'] = message;
	# 	Database.ExtractMessage(sender,destination,message,stamp)
	# 	return 'Message Recieved'

	@cherrypy.expose
	@cherrypy.tools.json_in()
	def receiveMessage(self):
		input_data = cherrypy.request.json
		print input_data

		Database.ExtractMessage(input_data['sender'],input_data['destination'],input_data['message'],input_data['stamp'])
		return '0'


	# @cherrypy.expose
	# def getProfile(self):



def runMainApp():
	#Setup CSS
	conf = {
		'/':{
			'tools.sessions.on': True,
			'tools.staticdir.root':os.path.abspath(os.getcwd())
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
