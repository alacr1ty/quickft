#!/usr/bin/env python3

"""
Program: ftclient.py
	Written by: Ava Cordero
	Date: 11/29/2019
	Latest:

Description:
	A simple file transfer client.

Usage: ftclient.py servername portnumber
"""

# imports
import signal
import sys
from socket import *



#Function: conex_ctrl (Connect to Server control connection)
#Description: Connects the client to the server control connection.
#Input: Server name and port to which to connect
#Output: Control connection socket..
def conex_ctrl(server_name, server_port):
	# connect to the server
	client_socket = socket(AF_INET, SOCK_STREAM) # create TCP socket
	client_socket.settimeout(3) # set the timeout period
	client_socket.connect((server_name,server_port)) # connect to server
	print("Client connected to server '" + server_name + "' on port " + str(server_port) + "...")

	# returns the socket
	return client_socket
#Function: conex_data (Connect to Server)
#Description: Accepts a data connection from the server.
#Input: Control connection socket.
#Output: Data connection socket
def conex_data(server_socket):
	try:
		# set variables
		client_sock_def = server_socket.getsockname()
		client_name = client_sock_def[0]
		client_port = int(sys.argv[2])+1

		server_socket = socket(AF_INET,SOCK_STREAM) # create socket
		server_socket.settimeout(3) # set the timeout period
		server_socket.bind (("",client_port)) # bind socket to port

		# print("Listening for data connection with server on port " + str(client_port) + "...")
		server_socket.listen(1) # wait for an incoming connection
		connection_socket, addr = server_socket.accept() # accept and get socket info
		# print("Data connection established with server on port " + str(client_port) + ".")
		return connection_socket
	except:
		print("Connection broken.")
		exit(1)

#Function: recv_list (Receive directory list)
#Description: Receives a directory list from the server.
#Input: Socket.
#Output: None.
def recv_list(socket):
	# establish data connection
	data_socket = conex_data(socket)

	# receive and print the directory list
	dir_contents = data_socket.recv(4096).decode("UTF-8")
	print(dir_contents)

	# close data connection
	data_socket.close()

#Function: recv_file (Receive file)
#Description: Receives a file from the other machine.
#Input: Socket and maximum character length for the message.
#Output: None.
def recv_file(socket, filename):
	# establish data connection
	data_socket = conex_data(socket)

	# receive the length of the file
	len = int(socket.recv(32).decode("UTF-8"))

	# assemble the file in chunks
	x = 0
	data = ""
	while (x in range(0, len)):
		data += data_socket.recv(4096).decode("UTF-8")
		x += 4096

	# receive the response
	# data = data_socket.recv(4096).decode("UTF-8")

	if data == "0":
		print("File not found.")
	else:
		print("Downloading file: " + filename)
		f = open(filename, "w+")
		f.write(data)
		print("File downloaded.")

	# close data connection
	data_socket.close()

#Function: run_client (Run client)
#Description: Runs and maintains the client functionality.
#Input: Client socket.
#Output: None.
# maintains the client file transfer functionality
def run_client(client_socket):
	# continuously prompt for a message until the message is "\q"
	print("File transfer client starting...")
	while 1:
		msg_out = proc_cmd(client_socket, ">", 4096)

#Function: proc_cmd (Process command)
#Description: Prompts for and sends a command to the other machine.
#Input: Socket, prompt, and maximum character length for the message.
#Output: String including message.
def proc_cmd(socket, prompt, message_max):
	sentence = ""
	# prompt user for a message that is no longer than the maximum
	while len(sentence) > message_max or len(sentence) == 0:
		sentence = input(prompt)
		
		if len(sentence) > message_max:
			print("Exceeded maximum characters allowed (" + str(message_max) + "), try again.")
		
		elif sentence == "\\q": # if message is "\q", 
			print("Connection closed...")
			socket.send(sentence.encode("UTF-8")) # send the message
			exit(0)
		
		elif sentence.startswith("get ") and len(sentence.split()) == 2: # if client wants to get a file
			# send the command using the control connection
			socket.send(sentence.encode ("UTF-8"))

			filename = sentence.split()[1]
			recv_file(socket, filename)

		elif sentence == "list": # if client wants to list directory contents
			# send the command
			socket.send(sentence.encode ("UTF-8"))

			recv_list(socket)

		else: # otherwise
			print("Not a valid command, try again.")

	return(sentence) # must be UTF-8

# signal handler function
def sig_handle(sig, frame):
	sys.exit(0)


# Function: Main
# Description: Validates arguments, then calls functions to configure the connect to the server and run the file transfer client.
# Input: Command line arguments.
# Output: None.
def main ():
	# check for proper usage
	if len(sys.argv) != 3:
		print("Error: Incorrect usage(ftclient.py servername portnumber).")
		exit(1)

	# assign host and port from args
	server_name = sys.argv[1]
	server_port = int(sys.argv[2])

	# connect to the server, get socket and handle
	client_socket = conex_ctrl(server_name, server_port)

	# run the file transfer client
	run_client(client_socket) 


# assign signal handler function
signal.signal(signal.SIGINT, sig_handle)

main()