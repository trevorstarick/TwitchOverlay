#!/usr/bin/env python
import socket,sys
from time import sleep

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

Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) == 4:
  User = sys.argv[1]
	Server = User + ".jtvirc.com"
	Channel = "#"+str(sys.argv[3])
	Port = 6667
	Password = sys.argv[2]
else :
	print bcolors.FAIL + "ERROR: Run the script like this 'run.py [username] [password] [channel]'" + bcolors.ENDC
	sys.exit()

#Connect to JTVIRC
Socket.connect((Server, Port))
Socket.send("PASS %s \n" % (Password))
Socket.send("NICK %s \n" % (User))
Socket.send("USER %s 0 * :%s \n" % (User, User))
Socket.send("JOIN %s \n" % (Channel))
print bcolors.OKGREEN + 'Connected as '+User+' on channel '+ Channel[1:] + '!' + bcolors.ENDC

while 1:
	res = Socket.recv(4096).strip('\r\n')
	if "PRIVMSG "+Channel in res:
		sender = res.split(" ")[0].split("!")[0].strip(":")
		message = res.partition('PRIVMSG '+Channel+' :')[2]
		print  bcolors.OKBLUE+sender+bcolors.ENDC+': '+message
