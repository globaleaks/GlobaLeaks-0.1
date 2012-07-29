#! /bin/sh
### BEGIN INIT INFO
# Provides:                     globaleaks
# Required-Start:       $local_fs $remote_fs $syslog
# Required-Stop:        $local_fs $remote_fs $syslog
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
CONFIG=/etc/glinstances.conf
DAEMON=/usr/bin/python
DAEMON_DIR=/home/globaleaks/GL-01/$NAME
HS=/home/globaleaks/HS
DAEMON_ARGS="web2py.py -i $ADDRESS -p $PORT --password=$PASSWORD --pid_filename=$PIDFILE"
DAEMON_USER=globaleaks
WGL="http://172.16.254.2:8000"

# Exit if the package is not installed
[ -x "$DAEMON" ] || exit 0

# Read configuration variable file if it is present
[ -r /etc/default/$NAME ] && . /etc/default/$NAME

# Load the VERBOSE setting and other rcS variables
[ -f /etc/default/rcS ] && . /etc/default/rcS

# Define LSB log_* functions.
# Depend on lsb-base (>= 3.0-6) to ensure that this file is present.
#. /lib/lsb/init-functions

# Read config
[ -r $CONFIG ] && . $CONFIG;

IFS=',' read -ra INSTANCE <<< $instances

trap_under_installation()
{
        if [ ! -e "$DAEMON_DIR/globaleaks.conf" ]; then
                echo "not found $DAEMON_DIR/globaleaks.conf -- GlobaLeaks not yet setup"
                return 0
        fi

        under_install=`grep "under_installation = True" "$DAEMON_DIR/globaleaks.conf"`
        hs_virginity=`grep "_BCDEF" "$DAEMON_DIR/globaleaks.conf"`

    # debug
    if [ "$under_install" ]; then
        echo "under install True"
    else
        echo "not yet under installation!"
    fi

    if [ "$hs_virginity" ]; then
        echo "the hidden service is not yet initialized"
    else
        echo "the hidden service has been yet initialized"
    fi

        if [ "$under_install" ] && [ "$hs_virginity" ]; then
        echo "(U!I) the start_setup.html has been used, creating HS..."
                echo "Setup hidden service: it would be repeated until you configure the node at $WGL"
                do_stop

                # This command starts Tor
                $DAEMON_DIR/scripts/globaleaks_os_setup.sh

                if [ ! -f "$HS/hostname" ]; then
            echo "try to start HS, failing"
                        return 1
            else
                        return 0
                fi
        fi

    if [ "$under_install" ] && [ ! "$hs_virginity" ]; then
        echo "(UI) HS available, starting Tor and finalize virtual_setup.html in $WGL"
        # return code 2 start Tor
        return 2
        fi

        if [ ! "$under_install" ] && [ ! "$hs_virginity" ]; then
        echo "(!UI) the virtual_setup.html has not yet filled, connect to $WGL"
                return 2
    fi

    if [ ! "$under_install" ] && [ "$hs_virginity" ]; then
        echo "(!U!I) the start_setup.html need to be filled, connect to $WGL"
        return 3
    fi

    echo "not handled condition!"
    return 4
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
            echo "GlobaLeaks setup is going well, starting Tor..."
            /etc/init.d/tor start
            ;; # GLobaLeaks setupped, Tor not touched
        3)
             echo "this shall be the first boot of the Virtual Machine of GL!"
             sleep 1
             ;;
         4)
             echo "urgh !? this bug need to be handled"
             echo "mail to info@globaleaks.org!"
             ;;
        esac

        # launch GlobaLeaks instances
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
    
                    echo "Starting GlobaLeaks instance "$instance_name
                DAEMON_ARGS=web2py.py -i $ADDRESS -p $instance_port \
                    --pid_filename=$pidfile
    
                # launch the daemon
                start-stop-daemon --start --quiet --pidfile $pidfile \
                    ${DAEMON_USER:+--chuid $DAEMON_USER} --chdir \
                    $instance_dir/$instance_name --background --exec \
                    $DAEMON -- $DAEMON_ARGS || return 2
            
            fi
        done
    return 0
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
    #XXX: should Tor be restarted or HUP also?

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
    # Return
    #   0 if daemon is responding and OK
    #   1 if daemon is not responding, but PIDFILE exists
    #   2 if daemon is not responding, but LOCKFILE exists
    #   3 if deamon is not running
    #   4 if daemon status is unknown

    for instance in ${INSTANCE[@]}; do
        instance_name=`expr match $instance "\(.*\):.*"`
        instance_port=`expr match $instance ".*:\(.*\)"`

        instance_pid=$PIDDIR"/"$instance_name"/"pid
        echo Sending HUP to GlobaLeaks instance $instance_name

        start-stop-daemon --stop --test --quiet --pidfile $instance_pid \
            && echo GlobaLeaks instance $instance_name running OK.
        RETVAL=$?
        [ "$RETVAL" != 0 ] && echo GlobaLeaks instance $instance_name returned status $RETVAL && return $RETVAL
        [ -f $instance_pid ] && echo GlobaLeaks instance $instance_name not responding, but PIDFILE $instance_pid exists.
    done
    return 0
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
