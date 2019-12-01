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

#Function: conex_srv (Connect to Server)
#Description: Connects the client to the server.
#Input: Server name and port to which to connect
#Output: Tuple containing the client socket and server handle.
def conex_srv (server_name, server_port):
# try:
	# connect to the server
	client_socket = socket (AF_INET, SOCK_STREAM) # create TCP socket
	client_socket.connect ((server_name,server_port)) # connect to server
	print ("Client connected to server '" + server_name + "' on port " + str(server_port) + "...")

	# returns the socket
	return client_socket

#Function: run_client (Run client)
#Description: Runs and maintains the client functionality.
#Input: Client socket.
#Output: None.
# maintains the client file transfer functionality
def run_client (client_socket):
	# continuously prompt for a message until the message is "\q"
	while 1:
		msg_out = send_cmd (client_socket, ">", 500)

#Function: send_message (Send message)
#Description: Prompts for and sends a command to the other machine.
#Input: Socket, prompt, and maximum character length for the message.
#Output: String including message.
def send_cmd (socket, prompt, message_max):
	sentence = ""

	# prompt user for a message that is no longer than the maximum
	while len(sentence) > message_max or len(sentence) == 0:
		sentence = input (prompt)
		if len(sentence) > message_max:
			print ("Exceeded maximum characters allowed (" + str(message_max) + "), try again.")
		elif sentence == "\\q": # if message is "\q", 
			print ("Connection closed...")
			socket.send (sentence.encode ("UTF-8")) # send the message
			exit(0)
		elif sentence.startswith("get"): # if client wants to get a file
			print ("Downloading file: " + sentence.split()[1])
			socket.send (sentence.encode ("UTF-8")) # send the message
		elif sentence == "list": # if client wants to list directory contents
			print ("Directory Contents: " + "")
			socket.send (sentence.encode ("UTF-8")) # send the message
		else: # otherwise
			print ("Not a valid command, try again.")


	return (sentence) # must be UTF-8

# signal handler function
def sig_handle(sig, frame):
	sys.exit(0)


# Function: Main
# Description: Validates arguments, then calls functions to configure the user, connect to the server, and run the file transfer client.
# Input: Command line arguments.
# Output: None.
def main ():
	# check for proper usage
	if len(sys.argv) != 3:
		print ("Error: Incorrect usage (ftclient.py servername portnumber).")
		exit(1)

	# assign host and port from args
	server_name = sys.argv[1]
	server_port = int (sys.argv[2])

	print ("File transfer client starting ...")

	# connect to the server, get socket and handle
	client_socket = conex_srv (server_name, server_port)

	# run the file transfer client
	run_client (client_socket) 


# assign signal handler function
signal.signal(signal.SIGINT, sig_handle)

main()