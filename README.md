# Program: quickft
	Written by: Ava Cordero
	Date: 11/29/2019
	Latest: 12/4/2019

# Description:
	A simple file transfer client/server application.

# Usage:
## ftserver
	To start the file server, use the following command, where portnumber is the port on the local machine you want to accept connections from:

./ftserve.py portnumber

## ftclient
	To start the file transfer client, use the following command, where servername is the name of the machine running the server program, and portnumber is the port you wish to connect to on that server.

./ftclient.py servername portnumber

## ftclient console
	The client starts up a console with three commands: get, list, and \quit or \q.

### get usage
	To get (download) a file from the file server use the collowing command, where filename is the name, including file extension, of the file you would like to get:

get filename

### list usage
	To list the files in the server directory, use the following command:

list

### \quit usage
	To quit the client and disconnect from the file server, use the following command:

\q[uit]