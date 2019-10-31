#!/usr/bin/python
# This script checks the system uptime
# of a particular system and returns
# the current status with relevant information
# for updating the status of a service
# in Nagios.  The script utlizes the
# hrSystemUptime.0 SNMP key.  It also
# emulates the relevant command-line options
# for check_snmp, namely:
# -H: Host IP Address or name 
# -w: warn range, will go to warning status when
# the value is less than this, must be specified in
# days:hh:mm:ss
# -c: critical range, see -w for formatting
# -C: community
# -t: seconds to wait before timing out (default 10)
# -e: retries, number of times to retry the check
# -p: port number
# -P: SNMP protocol version [1|2c|3]
# -L: SNMPv3 sec security level [noAuthNoPriv|authNoPriv|authPriv]
# -U: SNMPv3 username
# -a: SNMPv3 authentication protocol [MD5|SHA]
# -A: SNMPv3 authentication password
# -x: SNMPv3 privacy protocol [DES|AES]
# -X: SNMPv3 privacy password
# Added arguments:
# -R: use hrSystemUptime MIB to determine uptime
# -S: use sysUpTime MIB to determine uptime

import sys
import getopt
import subprocess

def main(argv):
    '''Main function, parses options provided to script and
    invokes the appropriate function'''
    status = 0
    message = ""
    try:
        opts, args = getopt.getopt(argv, "hH:w:c:C:t:e:p:P:L:U:a:A:x:X:RS")
    except getopt.GetoptError:
    	printHelp()
    	sys.exit(3)
    # check for required options and set defaults
    host = ""
    warn = ""
    critical = ""
    version = ""
    uptimeMib = ""
    timeout = 10
    port = 161
    for o,a in opts:
    	if o == "-H":
    		host = a
    	if o == "-w":
    		warn = parseInTime(a)
    	if o == "-c":
    		critical = parseInTime(a)
    	if o == "-p":
    		port = a
    	if o == "-P":
    		version = a
    	if o == "-t":
    		timeout = a
    	if o == "-R":
    		uptimeMib = "hrSystemUptime"
    	if o == "-S":
    		uptimeMib = "sysUpTime"
    	if o == "-h":
    		printHelp()
    		sys.exit(3)
    # switch on version number
    if version == "1" or version == "2c":
    	status,message = snmpOld(host, warn, critical, uptimeMib, timeout, opts, args)
    elif version == "3":
    	snmp3(host, warn, critical, uptimeOid, timeout, opts, args)
    else
    	print "Unknown SNMP version"
    	sys.exit(3)
    
    
def snmpOld():
	'''Determines the SNMP value, parses it, and returns a list containing
	a message and status value.  Uses SNMP version 1 and 2c.'''
	
	global version, host, warn, critical, uptimeOid, timeout, port, opts
	community = ""
	
	for o, a in opts:
		if o == "-C":
			community = a
	
	# run the snmpget command
	stdin, stdout, stderr = None
	p = subprocess.popen("/usr/bin/snmpget -v %s -c %s -t %s %s %s" % (version, community, timeout, host, uptimeOid), 
						stdin=PIPE, stdout=PIPE, stderr=PIPE)
	(stdin, stdout, stderr) = (p.stdin, p.stdout, p.stderr)
	if stderr != None:
		status = 3
		msg = "error running snmpget command"
	elif stdout.search("No Such Instance"):
		status = 3
		msg = "unable to get a value for given OID"
	else:
		(uDays,uHours,uMinutes,uSeconds) = parseResponse(stdout)
	
	

def snmp3():
	'''Determines the SNMP value, parses it, and returns a list containing
	a message and status value.  Uses SNMP version 3.'''
	
	global host, warn, critical, uptimeOid, timeout, port, opts
	
def parseResponse(string):


def parseInTime(string):
  
    
def printHelp():
    '''Prints a message describing use of this script'''
    print """
    		-H: Host IP Address or name 
    		-h: print this help message
			-w: warn range, will go to warning status when
			    the value is less than this, must be specified in
                days:hours:minutes:seconds
            -c: critical range, see -w for formatting
			-C: community
			-t: seconds to wait before timing out (default 10)
			-e: retries, number of times to retry the check
            -p: port number
			-P: SNMP protocol version [1|2c|3]
			-L: SNMPv3 sec security level [noAuthNoPriv|authNoPriv|authPriv]
			-U: SNMPv3 username
			-a: SNMPv3 authentication protocol [MD5|SHA]
			-A: SNMPv3 authentication password
			-x: SNMPv3 privacy protocol [DES|AES]
			-X: SNMPv3 privacy password"""


if __name__ == '__main__':
    main(sys.argv[1:])
