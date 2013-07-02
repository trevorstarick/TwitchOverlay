#!/usr/bin/env python
import socket,sys,urllib2,time,os,json

# Screen clearing magic

def cls():
	os.system(['clear','cls'][os.name == 'nt'])

# COLOURS!
class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'

	def disable(self):
		self.HEADER = ''
		self.OKBLUE = ''
		self.OKGREEN = ''
		self.WARNING = ''
		self.FAIL = ''
		self.ENDC = ''

# Setup socket connection
Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) == 4:
	User = sys.argv[1]
	Server = User+".jtvirc.com"
	Channel = "#"+str(sys.argv[3])
	Port = 6667
	Password = sys.argv[2]
else :
	print bcolors.FAIL+"ERROR: Run the script like this 'run.py <username> <password> <channel>'"+bcolors.ENDC
	sys.exit()

# Connect to JTVIRC
Socket.connect((Server, Port))
Socket.send("PASS %s \n" % (Password))
Socket.send("NICK %s \n" % (User))
Socket.send("USER %s 0 * :%s \n" % (User, User))
Socket.send("JOIN %s \n" % (Channel))
print bcolors.OKGREEN+'Connected as '+User+' on channel '+Channel[1:]+'!'+bcolors.ENDC

# Set time in UNIX timestamp mode
initialTime = time.time()
currentTime = time.time()+30

while 1:
	if currentTime >= initialTime+30:
		cls()
		res = urllib2.urlopen('http://api.justin.tv/api/stream/summary.json?channel='+Channel[1:])
		data = json.load(res)
		print bcolors.OKGREEN+'Connected as '+bcolors.ENDC+bcolors.HEADER+User+bcolors.OKGREEN+' on channel '+bcolors.HEADER+Channel[1:]+bcolors.ENDC+'! '+bcolors.WARNING+'Viewer count: '+bcolors.ENDC+str(data['viewers_count'])
		initialTime = time.time()
		currentTime = time.time()
	else:
		currentTime = time.time()
	res = Socket.recv(4096).strip('\r\n')
	if "PRIVMSG "+Channel in res:
		sender = res.split(" ")[0].split("!")[0].strip(":")
		message = res.partition('PRIVMSG '+Channel+' :')[2]
		print  bcolors.OKBLUE+sender+bcolors.ENDC+': '+message
