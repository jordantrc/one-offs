#!/usr/bin/python
# GetIPAddress.py
# Retrieves the public IP address of the host by polling 
# a public IP address query site.  Emails
# the results to a specified address.

import urllib2
import smtplib

def main():
    '''checks the current IP address vs a text file in the local directory
        if the two values are different, updates the text file and 
        sends an email to a recipient.
    '''
    recipient = ""
    sender = ""
    mail_server = ""
    mail_server_port = ""
    mail_auth_user = ""
    mail_auth_pass = ""
    subject = ""
    
    # get the IP address from the local file
    f_ip = open("ip.txt")
    old_ip = f_ip.readline()
    f_ip.close()
    old_ip = old_ip.strip()

    # open the url and get the IP address
    f = urllib2.urlopen("http://api.ipify.org")
    ip = f.read(100)
    ip = ip.strip()

    # compare the two values
    if old_ip != ip:
        f_ip = open("ip.txt", "w")
        f_ip.write(ip)
        print("GetIPAddress.py: old ip = " + old_ip + ", new ip = " + ip)
        
        # create and send the message
        body = "The current IP address of this computer is " + ip
        message = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" % (sender,recipient,subject)
        message = message + body
        server = smtplib.SMTP(mail_server,mail_server_port)
        server.starttls()
        server.login(mail_auth_user,mail_auth_pass)
        server.sendmail(sender,recipient,message)
        server.quit()

        f_ip.close()
    else:
        print("GetIPAddress.py: " + old_ip + " = " + ip)
    

if __name__ == "__main__":
    main()