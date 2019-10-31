########################################
# MySQL Database interfacing
########################################
import MySQLdb

# create database connection
conn = MySQLdb.connect (host = "localhost",
							user = "syslog",
							passwd = "",
							db = "syslog")
cursor = conn.cursor()
sql = "SELECT COUNT(*) FROM logs"
cursor.execute(sql)
result = cursor.fetchone() #fetch a single record
while(result): # result will be set to None when there are no records remaining
	print result[0] # individual results are accessed using list syntax
	result = cursor.fetchone() #loop

sql = "SELECT DISTINCT(date(datetime)) AS date, COUNT(*) AS count FROM logs GROUP BY date"
cursor.execute(sql)
result = cursor.fetchall() # result becomes a list of lists
print result
for row in result:
	print "Date: %s, count: %s" % (row[0], row[1])
print "Number of rows returned: %s" % (cursor.rowcount)