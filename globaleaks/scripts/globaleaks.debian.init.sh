#! /bin/sh
### BEGIN INIT INFO
# Provides:			globaleaks
# Required-Start: 	$local_fs $remote_fs $syslog
# Required-Stop:	$local_fs $remote_fs $syslog
# Default-Start: 
# Default-Stop: 
# Short-Description: globaleaks initscript
# Description: This file starts up the globaleaks server.
### END INIT INFO

# startup script for VirtualBox ubuntu 11.10 - 
# strictly modified for run in a fixed environment
#
# THIS SCRIPT IS INTENDED TO WORKS ONLY WIH
# https://globaleaks.org/vecna/GL-virtual 
# and never shall be installed by hand

PATH=/usr/sbin:/usr/bin:/sbin:/bin
DESC="GlobaLeaks Node"
ADDRESS="172.16.254.2"
PORT="8000"
PASSWORD=""
NAME=globaleaks
PIDDIR=/var/run/$NAME
PIDFILE=$PIDDIR/$NAME.pid
SCRIPTNAME=/etc/init.d/$NAME
DAEMON=/usr/bin/python
DAEMON_DIR=/home/globaleaks/GL-01/$NAME
HS=/home/globaleaks/HS
DAEMON_ARGS="web2py.py -i $ADDRESS -p $PORT --password=$PASSWORD --pid_filename=$PIDFILE"
DAEMON_USER=globaleaks

# Exit if the package is not installed
[ -x "$DAEMON" ] || exit 0

# Read configuration variable file if it is present
[ -r /etc/default/$NAME ] && . /etc/default/$NAME

# Load the VERBOSE setting and other rcS variables
[ -f /etc/default/rcS ] && . /etc/default/rcS

# Define LSB log_* functions.
# Depend on lsb-base (>= 3.0-6) to ensure that this file is present.
. /lib/lsb/init-functions

trap_under_installation()
{
	if [ ! -e "$DAEMON_DIR/globaleaks.conf" ]; then
		echo "not found $DAEMON_DIR/globaleaks.conf -- GlobaLeaks not yet setup"
		return 0
	fi

	x=`grep "under_installation = True" "$DAEMON_DIR/globaleaks.conf"`
	if [ ! "$x" ]; then
		echo "Setup hidden service: it would be repeated until you validate the node at http://172.16.254.2:8000"
		do_stop

		# This command starts Tor
		$DAEMON_DIR/scripts/globaleaks_os_setup.sh

		if [ ! -f "$HS/hostname" ]; then
			return 1
	    else
			return 0
		fi
	else
		return 2
	fi
}

#
# Function that starts the daemon/service
#
do_start()
{
    # Return
    #   0 if daemon has been started
    #   1 if daemon was already running
    #   2 if daemon could not be started

	# Extra condition: if the globaleaks.conf contains under_installation = True
	# we need to invoke the globaleaks_os_setup.sh before the start
	trap_under_installation
	case "$?" in
		0)
			echo "Hidden service setup correctly"
			;; # Hidden service setup correctly, Tor already running
		1) 
			echo "Unable to setup hidden service!"
			;; # Old process is still running
		2) 
			echo "GlobaLeaks has been already setupped, starting Tor..."
			/etc/init.d/tor start
			;; # GLobaLeaks setupped, Tor not touched
	esac

    # The PIDDIR should normally be created during installation. This
    # fixes things just in case.
    [ -d $PIDDIR ] || mkdir -p $PIDDIR
        [ -n "$DAEMON_USER" ] && chown --recursive $DAEMON_USER $PIDDIR

    # Check to see if the daemon is already running.
    start-stop-daemon --stop --test --quiet --pidfile $PIDFILE \
        && echo "GlobaLeak already running" && return 1

    echo "Starting GlobaLeaks..."
    start-stop-daemon --start --quiet --pidfile $PIDFILE \
        ${DAEMON_USER:+--chuid $DAEMON_USER} --chdir $DAEMON_DIR \
        --background --exec $DAEMON -- $DAEMON_ARGS \
        || return 2

    return 0;
}

#
# Function that stops the daemon/service
#
do_stop()
{
    # Return
    #   0 if daemon has been stopped
    #   1 if daemon was already stopped
    #   2 if daemon could not be stopped
    #   other if a failure occurred

    # Stopping Tor is one of this script jobs
	/etc/init.d/tor stop

    echo "Stopping GlobaLeaks..."
    start-stop-daemon --stop --quiet --retry=TERM/30/KILL/5 --pidfile $PIDFILE
    RETVAL=$?
    # Many daemons don't delete their pidfiles when they exit.
    rm -f $PIDFILE
    return "$RETVAL"
}

#
# Function that restarts the daemon/service
#
do_restart()
{
    # Return
    #   0 if daemon was (re-)started
    #   1 if daemon was not strated or re-started

    do_stop
    case "$?" in
        0|1)
            do_start
            case "$?" in
                0) RETVAL=0 ;;
                1) RETVAL=1 ;; # Old process is still running
                *) RETVAL=1 ;; # Failed to start
            esac
            ;;
        *) RETVAL=1 ;; # Failed to stop
    esac

    return "$RETVAL"
}

#
# Function that sends a SIGHUP to the daemon/service
#
do_reload() {
    #
    # If the daemon can reload its configuration without
    # restarting (for example, when it is sent a SIGHUP),
    # then implement that here.
    #
    start-stop-daemon --stop --signal 1 --quiet --pidfile $PIDFILE
    return 0
}

#
# Function that queries the status of the daemon/service
#
do_status()
{
    # Return
    #   0 if daemon is responding and OK
    #   1 if daemon is not responding, but PIDFILE exists
    #   2 if daemon is not responding, but LOCKFILE exists
    #   3 if deamon is not running
    #   4 if daemon status is unknown

    # Check to see if the daemon is already running.
    start-stop-daemon --stop --test --quiet --pidfile $PIDFILE \
        && echo "GlobaLeaks running OK." && return 0
    [ -f $PIDFILE ] && echo "GlobaLeaks not responding, but PIDFILE exists." && return 1
    echo "GlobaLeaks is not running"
    return 3
}

case "$1" in
  start)
    [ "$VERBOSE" != no ] && log_daemon_msg "Starting $DESC" "$NAME"
	do_status
    RETVAL=$?
    case "$RETVAL" in
      0) log_success_msg "$NAME is running" 
		 do_restart
		 ;;
      *) log_failure_msg "$NAME is not running" 
		 do_start
		 ;;
	esac
    RETVAL=$?
    [ "$VERBOSE" != no ] &&
    case "$RETVAL" in
        0|1) log_end_msg 0 ;;
        *)   log_end_msg 1 ;;
    esac
    exit "$RETVAL"
    ;;
  stop)
    [ "$VERBOSE" != no ] && log_daemon_msg "Stopping $DESC" "$NAME"
    do_stop
    RETVAL=$?
    [ "$VERBOSE" != no ] &&
    case "$RETVAL" in
        0|1) log_end_msg 0 ;;
        *)   log_end_msg 1 ;;
    esac
    exit "$RETVAL"
    ;;
  #reload|force-reload)
    #
    # If do_reload() is not implemented then leave this commented out
    # and leave 'force-reload' as an alias for 'restart'.
    #
    #[ "$VERBOSE" != no ] && log_daemon_msg "Reloading $DESC" "$NAME"
    #do_reload
    #RETVAL=$?
    #[ "$VERBOSE" != no ] && log_end_msg $?
    #exit "$RETVAL"
    #;;
  restart|force-reload)
    #
    # If the "reload" option is implemented then remove the
    # 'force-reload' alias
    #
    [ "$VERBOSE" != no ] && log_daemon_msg "Restarting $DESC" "$NAME"
    do_restart
    RETVAL=$?
    [ "$VERBOSE" != no ] && log_end_msg "$RETVAL"
    exit "$RETVAL"
    ;;
  status)
    do_status
    RETVAL=$?
    [ "$VERBOSE" != no ] &&
    case "$RETVAL" in
      0) log_success_msg "$NAME is running" ;;
      *) log_failure_msg "$NAME is not running" ;;
    esac
    exit "$RETVAL"
    ;;
  *)
    echo "Usage: $SCRIPTNAME {start|stop|restart|force-reload|status}" >&2
    exit 3
    ;;
esac
