#!/bin/sh

yellow="\e[1;33m"
blue="\e[1;34m"
violet="\e[1;35m"
red="\e[1;31m"
green="\e[1;32m"

INSTORG="installstorage"

fancy_quit() {
    tput sgr0
    exit
}

help() {
    echo "${blue}This utility restore your directory to the not yet configured status of GlobaLeaks"
    echo "It's useful when:"
    echo "1]  you want delete all your service configuration and data."
    echo "2]  you want to restore the service plain."
    echo "${violet}To start the cleaning: run $0 clean"
    fancy_quit
}

clean() {
    echo "${yellow}checking directory..."
    if [ -d $INSTORG ]; then 
        echo "   ${green}$PWD: ${yello}ok"
    else
        echo "   ${red}$PWD: run this script without a prefix path"; fancy_quit
    fi

    # TODO - use a python wrapper to a portable rm/ln effects
    echo "${yellow}removing databased..."
    rm -f applications/globaleaks/databases/*
    echo "${green}   done"
    echo "${yellow}restoring pre install files..."
    rm -f routes.py
    rm -f $INSTORG/.installed
    ln -s $INSTORG/install_only_routes.py routes.py
    echo "${green}   done"
    echo "${yellow}restoring default configuration..."
    echo "${red}   TODO"
    fancy_quit
}

if [ $# -lt 1 ]; then
    help
fi

if [ $1 = "clean" ]; then
    clean
else
    help
fi
