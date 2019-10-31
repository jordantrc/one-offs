#!/usr/bin/python

import sys
import string
import MySQLdb

def main():
	# get filename from command line
	if (len(sys.argv) != 2):
		print "No filename specified, exiting"
		sys.exit(1)

	print "Opening " + sys.argv[1]

	fi = open(sys.argv[1], "r")
	fo = open(sys.argv[1] + "_shares","w")
	for line in fi:
		line = line.strip() # remove extra spaces on both sides of the string
		words = line.split(" ")
		fo.write("\\\\" + sys.argv[1] + "\\")
		for w in words:
			if w == "Disk":
				break
			fo.write(w + " ")
		fo.write("\n")

	fi.close()
	fo.close()

	# upload to the database
	conn = MySQLdb.connect(host="localhost",
							user = "user",
							passwd = "password",
							db = "database")

	'''datalist_dataset | CREATE TABLE `datalist_dataset` (
		`id` int(11) NOT NULL AUTO_INCREMENT,
		`networkshare` varchar(150) NOT NULL,
		`size` int(11) NOT NULL,
		`absolutepath` varchar(255) NOT NULL,
		`dfspath` varchar(100) NOT NULL,
		`oldshare` varchar(150) NOT NULL,
		`pi` varchar(100) NOT NULL,
		`steward` varchar(100) NOT NULL,
		`geolocation` varchar(100) NOT NULL,
		`description` longtext NOT NULL,
		`systemtype` varchar(100) NOT NULL,
		`datatype` varchar(20) NOT NULL,
		`acquisitiondate` date NOT NULL,
		`status` varchar(10) NOT NULL,
		`fundingagency` varchar(100) NOT NULL,
		PRIMARY KEY (`id`) '''

	cursor = conn.cursor()

	fi = open(sys.argv[1] + "_shares","r")
	for line in fi:
		line = line.rstrip()
		line = conn.escape_string(line)
		sql = """INSERT INTO datalist_dataset (oldshare,networkshare,description)
			VALUES ('%s','%s','%s')""" % (line, line, "automatically added by GetShares.py")
		print sql
		cursor.execute(sql)

	conn.commit()
	fi.close()

	sys.exit(0)


if __name__ == "__main__":
	main()