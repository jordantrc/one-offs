#!/bin/bash
# bash init script for iptables firewall

IPTABLES=/sbin/iptables

# start firewall function
start_firewall()
{
	# flush everything
	$IPTABLES --flush
	$IPTABLES --delete-chain
	
	# default rules
	$IPTABLES -P INPUT DROP
	$IPTABLES -P FORWARD DROP
	$IPTABLES -P OUTPUT DROP
	
	# anything on loopback is ok
	$IPTABLES -I INPUT 1 -i lo -j ACCEPT
	$IPTABLES -I OUTPUT 1 -o lo -j ACCEPT
	
	#####
	# INBOUND
	#####
	
	# anti-spoofing
	$IPTABLES -A INPUT -s 192.168.0.0/16 -j DROP
	$IPTABLES -A INPUT -s 172.16.0.0/12 -j DROP
	$IPTABLES -A INPUT -s 10.0.0.0/8 -j DROP
	
	# allow anything that's part of an established session
	$IPTABLES -A INPUT -j ACCEPT -m state --state ESTABLISHED,RELATED
	
	# allow inbound ssh, brute force limiting, drop any connections after four new sessions initiations in 60 seconds
	# third line is optional logging rule
	$IPTABLES -A INPUT -p tcp -m tcp --dport 2222 -m state --state NEW -m recent --set --name SSH
	$IPTABLES -A INPUT -p tcp -m tcp --dport 2222 -m state --state NEW -m recent --update --seconds 60 --hitcount 4 --rttl --name SSH -j DROP
	$IPTABLES -A INPUT -p tcp -m tcp --dport 2222 -m state --state NEW -m recent --update --seconds 60 --hitcount 4 --rttl --name SSH -j LOG --log-prefix "SSH brute force "
	$IPTABLES -A INPUT -p tcp -m tcp --dport 2222 -m state --state NEW -j ACCEPT
	
	# allow inbound www and https
	$IPTABLES -A INPUT -p tcp --dport 80 -m state --state NEW -j ACCEPT
	$IPTABLES -A INPUT -p tcp --dport 443 -m state --state NEW -j ACCEPT
	
	# allow inbound SMTP and SMTPAUTH
	#$IPTABLES -A INPUT -p tcp --dport 25 -m state --state NEW -j ACCEPT
	#$IPTABLES -A INPUT -p tcp --dport 587 -m state --state NEW -j ACCEPT
	
	# permit IMAP
	#$IPTABLES -A INPUT -p tcp --dport 993 -m state --state NEW -j ACCEPT
	
	# drop anything not allowed above
	$IPTABLES -A INPUT -j DROP
	
	#####
	# OUTBOUND
	#####
	# part of approved connect, allow
	$IPTABLES -A OUTPUT -j ACCEPT -m state --state ESTABLISHED,RELATED
	
	# allow outbound ping
	$IPTABLES -A OUTPUT -p icmp --icmp-type echo-request -j ACCEPT
	
	# allow outbound dns
	$IPTABLES -A OUTPUT -p udp --dport 53 -j ACCEPT
	$IPTABLES -A OUTPUT -p tcp --dport 53 -j ACCEPT
	
	# allow outbound smtp
	$IPTABLES -A OUTPUT -p tcp --dport 25 -j ACCEPT
	
	# allow outbound port 80 for updates
	$IPTABLES -A OUTPUT -p tcp --dport 80 -j ACCEPT	
}

stop_firewall() 
{
	$IPTABLES --flush
}

drop_firewall() 
{
	$IPTABLES --flush
	$IPTABLES -P INPUT ACCEPT
	$IPTABLES -P OUTPUT ACCEPT
	$IPTABLES -P FORWARD ACCEPT
}

case "$1" in
"status")
	echo "displaying current firewall rules"
	$IPTABLES --line-numbers -v --list
	;;
"start")
	echo "starting up firewall"
	start_firewall
	;;
"stop")
	echo "dropping firewall rules, leaving default drop policies in place"
	stop_firewall
	;;
"restart")
	echo "dropping firewall rules, leaving default drop policies in place"
	stop_firewall
	echo "starting up firewall"
	start_firewall
	;;
"wide-open")
	echo "WARNING - removing all firewall rules and allowing all traffic"
	drop_firewall
	;;
*)
	echo "Usage is iptables.sh [status|start|stop|restart|wide-open]"
	exit 1
	;;
esac

exit 0