#! /bin/sh
### BEGIN INIT INFO
# Provides:          skeleton
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Example initscript
# Description:       This file should be used to construct scripts to be
#                    placed in /etc/init.d.
### END INIT INFO

# Author: Foo Bar <foobar@baz.org>
#
# Please remove the "Author" lines above and replace them
# with your own name if you copy and modify this script.

# Do NOT "set -e"

# PATH should only include /usr/* if it runs after the mountnfs.sh script
PATH=/sbin:/usr/sbin:/bin:/usr/bin
DESC="GlobaLeaks Node"
ADDRESS="172.16.254.2"
NAME=globaleaks
CONFIG=/etc/glinstances.conf
DAEMON=/usr/bin/python
DAEMON_ARGS="--options args"
DAEMON_USER=globaleaks
DAEMON_DIR=/home/globaleaks/GlobaLeaks/globaleaks
PIDDIR=/var/run/$NAME
SCRIPTNAME=/etc/init.d/$NAME
PATH=$PATH:$DAEMON_DIR

# Exit if the package is not installed
[ -x "$DAEMON" ] || exit 0
# Read config
[ -r $CONFIG ] && . $CONFIG;

# split the config line into an array
INSTANCE=(`echo $instances | tr "," "\n"`)
#IFS=',' read -ra INSTANCE <<< $instances

# Load the VERBOSE setting and other rcS variables
. /lib/init/vars.sh

# Define LSB log_* functions.
# Depend on lsb-base (>= 3.2-14) to ensure that this file is present
# and status_of_proc is working.
. /lib/lsb/init-functions

#
# Function that starts the daemon/service
#
do_start()
{
    # Return
    #   0 if daemon has been started
    #   1 if daemon was already running
    #   2 if daemon could not be started

    # Starting Tor is one of this scripts jobs
    /etc/init.d/tor start

    for instance in ${INSTANCE[@]}; do
        instance_name=`expr match $instance "\(.*\):.*"`
        instance_port=`expr match $instance ".*:\(.*\)"`

        # check that the directory exists
        if [ ! -d $instance_dir"/"$instance_name ]; then
            echo "Path "$instance_dir"/"$instance_name" not found!"
            # skip missing instances
            continue
        else

            # look for the pid directory
            if [ ! -d $PIDDIR ]; then
                mkdir -m 0700 $PIDDIR
                chown $USERNAME $PIDDIR
            fi

                instance_pid_dir=$PIDDIR"/"$instance_name
            if [ ! -d $instance_pid_dir ]; then
                mkdir -m 0700 $instance_pid_dir
                chown $USERNAME $instance_pid_dir
            fi

            pidfile=$instance_pid_dir"/pid"


            # Skip launching if the daemon is already running.
            start-stop-daemon --stop --test --quiet --pidfile \
                $pidfile && continue

            echo Starting GlobaLeaks instance $instance_name
            DAEMON_ARGS= $DAEMON_DIR/web2py.py -i $ADDRESS -p $instance_port \
                --pid_filename=$pidfile

            # launch the daemon
            start-stop-daemon --start --quiet --pidfile $pidfile \
                ${DAEMON_USER:+--chuid $DAEMON_USER} --chdir \
                $instance_dir/$instance_name --background --exec \
                $DAEMON -- $DAEMON_ARGS || return 2

        fi

    done
    # figure out what proper return value should go here
    return 0
}

#
# Function that stops the daemon/service
#
do_stop()
{
    # Stopping Tor is one of this script jobs
    /etc/init.d/tor stop

    echo "Stopping GlobaLeaks..."

    for instance in ${INSTANCE[@]}; do
        instance_name=`expr match $instance "\(.*\):.*"`
        instance_port=`expr match $instance ".*:\(.*\)"`

        instance_pid=$PIDDIR"/"$instance_name"/"pid
        echo "Stopping GlobaLeaks instance "$instance_name
        start-stop-daemon --stop --quiet --retry=TERM/30/KILL/5 \
            --pidfile $instance_pid
        RETVAL=$? #XXX: do something with this
        rm -f $instance_pid
    done
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
    for instance in ${INSTANCE[@]}; do
        instance_name=`expr match $instance "\(.*\):.*"`
        instance_port=`expr match $instance ".*:\(.*\)"`

        instance_pid=$PIDDIR"/"$instance_name"/"pid
        echo "Sending HUP to GlobaLeaks instance "$instance_name
        start-stop-daemon --stop --signal 1 --quiet --pidfile \
            $instance_pid
    done
    return 0
}

do_status() {
    for instance in ${INSTANCE[@]}; do
        instance_name=`expr match $instance "\(.*\):.*"`
        instance_port=`expr match $instance ".*:\(.*\)"`

        instance_pid=$PIDDIR"/"$instance_name"/"pid
        echo "Sending HUP to GlobaLeaks instance "$instance_name

        start-stop-daemon --stop --test --quiet --pidfile $instance_pid \
            && echo "GlobaLeaks instance $instance_name running OK."
        [ -f $instance_pid ] && echo GlobaLeaks instance $instance_name not responding, but PIDFILE $instance_pid exists.
    done
    return 0
}

case "$1" in
  start)
    [ "$VERBOSE" != no ] && log_daemon_msg "Starting $DESC" "$NAME"
    do_start
    case "$?" in
        0|1) [ "$VERBOSE" != no ] && log_end_msg 0 ;;
        2) [ "$VERBOSE" != no ] && log_end_msg 1 ;;
    esac
    ;;
  stop)
    [ "$VERBOSE" != no ] && log_daemon_msg "Stopping $DESC" "$NAME"
    do_stop
    case "$?" in
        0|1) [ "$VERBOSE" != no ] && log_end_msg 0 ;;
        2) [ "$VERBOSE" != no ] && log_end_msg 1 ;;
    esac
    ;;
  status)
       status_of_proc "$DAEMON" "$NAME" && exit 0 || exit $?
       ;;
  #reload|force-reload)
    #
    # If do_reload() is not implemented then leave this commented out
    # and leave 'force-reload' as an alias for 'restart'.
    #
    #log_daemon_msg "Reloading $DESC" "$NAME"
    #do_reload
    #log_end_msg $?
    #;;
  restart|force-reload)
    #
    # If the "reload" option is implemented then remove the
    # 'force-reload' alias
    #
    log_daemon_msg "Restarting $DESC" "$NAME"
    do_stop
    case "$?" in
      0|1)
        do_start
        case "$?" in
            0) log_end_msg 0 ;;
            1) log_end_msg 1 ;; # Old process is still running
            *) log_end_msg 1 ;; # Failed to start
        esac
        ;;
      *)
        # Failed to stop
        log_end_msg 1
        ;;
    esac
    ;;
  *)
    #echo "Usage: $SCRIPTNAME {start|stop|restart|reload|force-reload}" >&2
    echo "Usage: $SCRIPTNAME {start|stop|status|restart|force-reload}" >&2
    exit 3
    ;;
esac

:
