#!/usr/bin/python
#Author: Jacques Coetzee
#Date: 18 May 2015
from netaddr import *
import os
import sys

menuspace = ' '*4

ipstats = {	'iprange' : '',
						'ipnetwork' : None,
						'totalips' : 0,
						'netmask' : ''

					}


pageheader = '''
%sAuthor:      Jacques Coetzee
%sDescription: Create a subnet breakdown based on your networking requirements

''' % (menuspace, menuspace)

def printit(message):
	global menuspace
	print "%s%s" % (menuspace, message)


def set_IPRange():
	global ipstats
	os.system('clear')
	print pageheader
	while 1==1:
		try:
			iprange = raw_input('%sEnter your IP Range for investigation: ' % menuspace)
			ipnetwork = IPNetwork(iprange)
			ipstats['iprange'] = iprange
			ipstats['ipnetwork'] = ipnetwork
			#Get the network Config
			ipstats['totalips'] = len(ipnetwork)
			ipstats['netmask'] = ipnetwork.netmask
			break;
		except:
			pass

def list_subnets():
	global ipstats
	if ipstats['iprange'] == '':
		printit('*** THERE IS NO IP RANGE SET! ***')
		raw_input('Press any key to continue...')
		return

	subnets = 0
	while subnets == 0:
		strsubnets = raw_input('Enter your netmask eg. [/24,/23,/22,etc]? :')
		try:
			strsubnets = strsubnets.replace('/', '')
			subnets = int(strsubnets)
		except:
			pass

	
	exportcsv = raw_input('Export the list to csv? [y/n]: ')

	os.system('clear')

	if exportcsv in ['y', 'Y']:	
		f = open('subnetlist.csv', 'wb')
		f.write("number|Hosts|Subnet|Block|Netmask|Network Addr|Broadcast\n")
		subnets = list(ipstats['ipnetwork'].subnet(subnets))
		for ix,subnet in enumerate(subnets):
			ip = IPNetwork(subnet)
			f.write("%s|%s|%s|%s|%s|%s|%s\n" % (ix, len(ip), subnet, str("%s - %s" % (ip[1], ip[-2])), ip.netmask,ip.network, ip.broadcast ) )
		f.close()	
		print "File subnetlist.csv created."		
	else:
		subnets = list(ipstats['ipnetwork'].subnet(subnets))
		print "Num.".ljust(6, ' ') + "Hosts".ljust(8," ") + "Subnet".ljust(20, ' ') +"Block".ljust(40, ' ')  + "Netmask".ljust(18,' ')	+ "Network Addr".ljust(15, " ") + "Broadcast"
		for ix,subnet in enumerate(subnets):
			ip = IPNetwork(subnet)
			number = '%s.' % ix
			print str(number).ljust(6, ' ') + str(len(ip)).ljust(8," ") + str(subnet).ljust(20, ' ')  + str("%s - %s" % (ip[1], ip[-2])).ljust(40,' ')  + str(ip.netmask).ljust(18,' ')	+ str(ip.network).ljust(15, " ") + str(ip.broadcast)
	
	raw_input('Press any key to continue...')	



while 1==1:
	os.system('clear')
	print pageheader
	printit('IP Stats:')
	printit('=========')
	printit('IP Range : %s' % ipstats['iprange'])
	printit('Total IPs: %s' % ipstats['totalips'])
	printit('Netmask  : %s' % ipstats['netmask'])

	print " "
	print " "
	print " "
	print '''
%sMENU
%s=====
%s1. Add/change IP Range		
%s2. List subnets
		
%sx. Exit
'''.replace('%s', menuspace)

	menuoption = raw_input('Menu Selection: ')
	if menuoption.lower() == 'x':
		print "Thanks for using the tool."
		break;


	if menuoption.lower() == '1':
		set_IPRange()
	
	if menuoption.lower() == '2':
		list_subnets()
