#!/usr/bin/env python3

"""
Program: ftserve.py
	Written by: Ava Cordero
	Date: 11/29/2019
	Latest: 

Description:
	A simple file server.
	See ftlib.py for utility functions.

Usage: ftserver portnumber
"""

# imports
import signal
import sys
from socket import *
from ftlib import *



#Function: run_client_srv (Run server-side client)
#Description: Maintains the server-side file transfer functionality.
#Input: Connection socket, server handle, and client handle.
#Output: Returns 1 to start_srv to end the connection.
# def run_client_srv (connection_socket, handle_srv, handle_cl):
def run_client_srv (connection_socket):
	# keep prompting until the message is "\q"
	while 1:
		msg_in = recv_message(connection_socket, 500)
		print ("Client sent command: " + msg_in)
		if msg_in == "\\q": # if message is "\q"
		 	# close connection to client
			print ("Connection closing...")
			connection_socket.close() # close connection
			print ("Connection closed...")
			return 1

#Function: start_srv (Start server)
#Description: Starts and maintains the server functionality. Calls the run_client_srv function when a connection is established.
#Input: Port and socket on which to run the server, and server handle.
#Output: None.
def start_srv (server_port, server_socket):
# def start_srv (server_port, server_socket, handle_srv):
	# always
	while 1:
		# listen for a connection
		print ("Listening for a connection on port " + str(server_port) + "...")
		server_socket.listen (1) # wait for an incoming connection
		connection_socket, addr = server_socket.accept() # accept and get socket info
		print ("Client connected to server on port " + str(server_port) + "...")
		
		# keep connection open until message is "\quit"
		stop = 0
		while stop is 0:
			# run the server-based client until stop is returned
			stop = run_client_srv (connection_socket)


#Function: Main
#Description: Validates arguments, then calls functions to set up the socket, configure the user, and start the server.
#Input: Command line arguments.
#Output: None.
def main ():
	# check that usage is correct
	if len(sys.argv) != 2:
		print ("Error: Incorrect usage (chatserve.py serverport).")
		sys.exit(1)
	
	# assign server port and socket
	server_port = int(sys.argv[1]) # port comes from args
	server_socket = socket (AF_INET,SOCK_STREAM) # create socket
	server_socket.bind (("",server_port)) # bind socket to port

	print ("File server starting ...")

	# start server
	start_srv (server_port, server_socket)


# assign signal handler function
signal.signal(signal.SIGINT, sig_handle)

main()