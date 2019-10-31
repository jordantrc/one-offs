#!/usr/bin/python
# Author: Jordan Chadwick
# 7/21/2010
# This script checks the MySQL database containing Syslog-ng entries.
# It echoes the number of records in the specified time period and
# returns a status code so that Nagios knows what occurred.

# Usage:
# check_syslog_mysql.py [arguments]

# Required:
# -H: mysql host name
# -u: MySQL user name
# -a: MySQL password
# -d: database name
# -b: MySQL table to query
# -w: warning count range
# -c: critical count range

# Optional:
# -t: timeout in seconds
# -h: print help
# -T: time period to check in minutes, default is 10
# -v[vvv]: verbose (the more v's the more verbose)

import sys
import getopt
import MySQL

def main():
	'''Main program'''
	status = -1
	message = "none"
	try:
		opts, args = getopt.getopt(argv[1:], "H:u:a:d:t:hw:c:T:vb:")
	except getopt.GetoptError:
		print "Error parsing arguments"
		printHelp()
		status = 3
		sys.exit(status)
	
	#create options dictionaries
	required = {'host': None, 'user': None, 'password': None, 'db': None, 'table': None,
		'warning': None, 'critical': None}
	optional = {'timeout': None, 'period': 10, 'verbosity': None}
	
	#first check for verbosity
	
		

def printHelp():
	'''Prints the help message'''
	print """Usage:
		check_syslog_mysql.py [arguments]

		Required:
		-H: mysql host name
		-u: MySQL user name
		-a: MySQL password
		-d: database name
		-b: MySQL table to query
		-w: warning count range
		-c: critical count range

		Optional:
		-t: timeout in seconds
		-h: print help
		-T: time period to check in minutes, default is 10
		-v[vvv]: verbose (the more v's the more verbose)"""