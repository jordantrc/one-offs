#!C:\python27\python.exe
#
# Base64 decoder
#

import base64

infile = open('', 'r')
outfile = open('', 'wb')

for line in infile:
	s = base64.b64decode(line)
	outfile.write(s)

infile.close()
outfile.close()