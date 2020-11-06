#!/bin/bash
#
# 
# chkconfig: 2345 96 10
# description: oracledb start/stop script
#
# /etc/init.d/oracledb
#
# Run-level Startup script for the Oracle Listener and Instances
# It relies on the information on /etc/oratab

export ORACLE_SID=testoracle
export ORACLE_BASE=/u01/app/oracle
export ORACLE_HOME=/u01/app/oracle/product/11.2.0/dbhome_1
export ORACLE_OWNR=oracle
export PATH=$PATH:$ORACLE_HOME/bin
export ORACLE_UNQNAME=testoracle.ccom.nh

echo "Oracle Script init.d"

if [ ! -f $ORACLE_HOME/bin/dbstart -o ! -d $ORACLE_HOME ]
then
echo "Oracle startup: cannot start"
exit 1
fi

case "$1" in
start)
	# Oracle listener and instance startup
	echo -n "Starting Oracle: "
	su $ORACLE_OWNR -c "$ORACLE_HOME/bin/lsnrctl start"
	su $ORACLE_OWNR -c "$ORACLE_HOME/bin/dbstart $ORACLE_HOME"
	su $ORACLE_OWNR -c "$ORACLE_HOME/bin/emctl start dbconsole"
	touch /var/lock/oracle
	echo "OK"
	;;
stop)
# Oracle listener and instance shutdown
echo -n "Shutdown Oracle: "
	su $ORACLE_OWNR -c "$ORACLE_HOME/bin/emctl stop dbconsole"
	su $ORACLE_OWNR -c "$ORACLE_HOME/bin/lsnrctl stop"
	su $ORACLE_OWNR -c "$ORACLE_HOME/bin/dbshut $ORACLE_HOME"
	rm -f /var/lock/oracle
	echo "OK"
	;;
reload|restart)
	$0 stop
	$0 start
	;;
*)
echo "Usage: `basename $0` start|stop|restart|reload"
exit 1
esac

exit 0