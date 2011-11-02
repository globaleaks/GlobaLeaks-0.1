#!/bin/sh

yellow="\e[1;33m"
blue="\e[1;34m"
violet="\e[1;35m"

help() {
    echo "${blue}This utility restore your directory to the not yet configured status of GlobaLeaks"
    echo "It's useful when:"
    echo "1]  you want delete all your service configuration and data."
    echo "2]  you want to restore the service plain."
    echo "${violet}To start the cleaning: run $0 clean"
    tput sgr0
    exit
}

clean() {
    echo "${yellow}clean shit"
    tput sgr0
}

if [ $# -lt 1 ]; then
    help
fi

if [ $1 = "clean" ]; then
    clean
else
    help
fi
