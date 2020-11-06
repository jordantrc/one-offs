#!/bin/sh
if [ ! $# = 1 ]
  then
    echo "Usage: $0 username@domain"
    exit 1
  else
    user=`echo "$1" | cut -f1 -d "@"`
    domain=`echo "$1" | cut -s -f2 -d "@"`

    if [ -x $domain ]
      then
        echo "No domain given\nUsage: $0 username@domain"
        exit 2
    fi
  
   # Create the needed Maildir directories
    echo "Creating user directory /var/vmail/$domain/$user"
    # maildirmake.dovecot does only chown on user directory, we'll create domain directory instead
    if [ ! -x /var/vmail/$domain ]
      then
        mkdir /var/vmail/$domain
        chown 5000:5000 /var/vmail/$domain
        chmod 700 /var/vmail/$domain
    fi

    /usr/bin/maildirmake.dovecot /var/vmail/$domain/$user 5000:5000
    # Also make folders for Drafts, Sent, Junk and Trash
    /usr/bin/maildirmake.dovecot /var/vmail/$domain/$user/.Drafts 5000:5000
    /usr/bin/maildirmake.dovecot /var/vmail/$domain/$user/.Sent 5000:5000
    /usr/bin/maildirmake.dovecot /var/vmail/$domain/$user/.Junk 5000:5000
    /usr/bin/maildirmake.dovecot /var/vmail/$domain/$user/.Trash 5000:5000

    # To add user to Postfix virtual map file and reload Postfix
    echo "Adding user to /etc/postfix/vmailbox"
    echo $1  $domain/$user/ >> /etc/postfix/vmailbox
    postmap /etc/postfix/vmailbox
    postfix reload
fi

echo "\nCreate a password for $user@$domain"
#SWAP THE FOLLOWING passwd LINES IF USING A UBUNTU VERSION PRIOR TO 12.04
#passwd=`dovecotpw`
passwd=`doveadm pw -s ssha256 -u $user`
echo "Adding user $user@$domain to /etc/dovecot/users"
echo "$user@$domain:$passwd:5000:5000::/var/vmail/$domain/:/bin/false::" >> /etc/dovecot/users

exit 0
