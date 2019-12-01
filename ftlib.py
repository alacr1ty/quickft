#!/usr/bin/env python3

"""
Program: ftclient.py
	Written by: Ava Cordero
	Date: 11/29/2019
	Latest:

Description:
	A library for a simple file transfer client/server application.
"""

# imports
import sys
from socket import *



#Function: recv_message (Receive message)
#Description: Receives a message from the other machine.
#Input: Socket and maximum character length for the message.
#Output: String including prompt and message.
def recv_message (socket, message_max):
	# receive the message back from server
	return socket.recv (message_max).decode ("UTF-8") # must be UTF-8

#Function: send_message (Send message)
#Description: Prompts for and sends a command to the other user.
#Input: Socket, prompt, and maximum character length for the message.
#Output: String including message.
def send_message (socket, prompt, message_max):
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
		elif sentence.startswith("get"):
			print ("not yet configured - get")
			socket.send (sentence.encode ("UTF-8")) # send the message
		elif sentence.startswith("list"):
			print ("not yet configured - list")
			socket.send (sentence.encode ("UTF-8")) # send the message
		else:
			print ("Not a valid command, try again.")


	return (sentence) # must be UTF-8


# signal handler function
def sig_handle(sig, frame):
	sys.exit(0)
