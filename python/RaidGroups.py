#!C:\python27\python.exe

# only options to provide are number of total disks available, and size of disks in GB
# script assumes RAID-DP is being used
# script will go from 0 to 10 spares

import sys

def main():
	'''does all the work'''

	if len(sys.argv) == 3:
		numDisks = int(sys.argv[1])
		diskSize = int(sys.argv[2])
	else:
		print 'Not enough arguments provided'
		sys.exit(1)

	# create the table
	table = []

	# header row
	row = []
	row.append('num disks')
	row.append('spares')

	for n in range(11):
		row.append('rg' + str(n+10) + ' - extra')
		row.append('rg' + str(n+10) + ' - space')

	table.append(row)
	most_space_table = [] # space, numDisks, rgsize

	# fill the rest of the table
	for n in range(numDisks - 10, numDisks + 1):
		row = []
		row.append(n)
		row.append(numDisks - n)
		for rgsize in range(10, 21):
			row.append(n % rgsize)
			
			avail_space = 0
			if(n < rgsize):
				avail_space = (rgsize - 2)*diskSize

			else:
				numrgs = int(n / rgsize)
				extra_disks = n % rgsize
				if extra_disks < 3:
					extra_disks = 0  # can't make a raid group out of less than three disks
				else:
					extra_disks = extra_disks - 2
				avail_space = (((numrgs * rgsize) - (2 * numrgs)) + extra_disks) * diskSize
				print 'num of disks = ' + str(n)
				print 'rgsize = ' + str(rgsize)
				print 'num raid groups = ' + str(numrgs)
				print 'extra_disks = ' + str(extra_disks)
				print 'avail_space = ' + str(avail_space)
				print '\n'

			if len(most_space_table) == 0:
				most_space_table = [avail_space, n, rgsize]
			else:
				if most_space_table[0] < avail_space:
					most_space_table = [avail_space, n, rgsize]
			row.append(avail_space)
		table.append(row)

	if numDisks >= 10:
		print 'Number of disks is ' + str(numDisks) + ', disk size is ' + str(diskSize) + ' GB'
		for r in table:
			print r
		print '\n\n'
		print 'Best fit:'
		print 'Num disks: ' + str(most_space_table[1]) + ', RAID group size: ' + str(most_space_table[2]) + ', Space: ' + str(most_space_table[0]) + ' GB'
	else:
		print 'Less than 10 disks provided, you should use all the disks in the raid group'
		print 'Doing so will provide ' + str((numDisks-2)*diskSize) + ' GB of space'

	return 0

if __name__ == '__main__':
	main()
	sys.exit(0)