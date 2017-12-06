'''
@Riyaz-Ul-Haque

'''

import socket

class Chat:

	#Initialise the Chat Server
	def __init__(self):
		self.serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	#Bind the socket to a particular port in the host machine and accept connections from any machine '0.0.0.0'
	#This is done by the person starting the chat
	def bind(self):
		port = 1234
		self.serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Used to reuse the port and avoid the "Error: Address already in use"
		self.serversock.bind(('0.0.0.0', port))
		self.serversock.listen(5)#Number of simultaneous connections to queue [Not needed here]

	#Accept the 'connect' request from your friend and return the 'clientsocket' created.
	#Called by the Student starting the game
	#Waits until a friend tries to connect to this student
	def accept(self):
		(clientsocket, address) = self.serversock.accept()
		return clientsocket

	#Connect to the host and port of the student specified
	def connect(self, host, port):
		self.serversock.connect((host,port))
	
	#Send the message to a friend
	def send(self, msg):
		self.serversock.send(msg)

	#Receive the move from your friend
	def receive(self):
		return self.serversock.recv(1024)

	#Stop the game
	def stopChat(self):
		print 'Chat Ended!'
		self.serversock.close()

def main():
	StudentChat = Chat()
	student = raw_input("Do you want to start a chat(y/n):")
	if student == 'y':
		print 'Waiting for the other person to connect.'
		StudentChat.bind()
		friend = StudentChat.accept()
		print 'Welcome to the Riyaz-Ul-Haque Chat Program!'
		reply = 'init'
		while reply != '0':#Until one of the member says stop
			mesg = raw_input('Enter your message: [0 to stop]')
			friend.send(str(mesg))
			reply = friend.recv(1024)
			print 'Reply: '+reply
		friend.close()
		StudentChat.stopChat()	
	elif student == 'n':
		friend = raw_input("Enter your friends' name to connect to: ")#Get the ipaddress of your friend
		StudentChat.connect(friend, 1234)
		print 'Welcome to the Students Chat!'
		reply = 'init'
		while reply != '0':#Until one of the member says stop
			mesg = StudentChat.receive()
			print 'Mesg: '+mesg
			if mesg == '0':
				reply = '0'
				StudentChat.send('0')#Send reply to stop
				break
			reply = raw_input('Enter your message: [0 to stop]')
			StudentChat.send(reply)
		StudentChat.stopChat()			
	else:
		print 'Please enter a valid answer.'

if __name__ == '__main__':
	main()
