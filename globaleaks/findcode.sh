#!/bin/sh

red="\e[1;31m"
yellow="\e[1;33m"
blue="\e[1;34m"
violet="\e[1;35m"
white="\e[1;39m"

echo "${blue}Utility for lazy developers without Aptana: blame yourself, use Aptana ${white}"


if [ $# -lt 1 ]; then
    echo "${red}I need an argumnt or more: the pattenr your searching recursively in the code ${white}"
    exit
fi

DIRNAMES="./applications/globaleaks/*.py ./applications/globaleaks/controllers/*.py ./applications/globaleaks/cron/*.py ./applications/globaleaks/languages/*.py ./applications/globaleaks/models/*.py ./applications/globaleaks/modules/*.py ./applications/globaleaks/modules/logic/*.py ./applications/globaleaks/views/*.py"


if [ $# -lt 2 ]; then
    echo "${white}executing grep of [${red}$1${white}] in the code directories"
    tput sgr0
    grep -n $1 $DIRNAMES
else

    cmdline="grep -n $1 $DIRNAMES "
    debuglist=$1

    pattern=1

    for arg in "$@"; do
        if [ "$pattern" -gt 1 ]; then
            cmdline="$cmdline | grep $arg"
            debuglist="$debuglist | $arg"
        fi
        (( pattern ++ ))      
    done
    echo "${white}grepping for [${red}$debuglist${white}] in the code directories"
    tput sgr0

    # filename="/tmp/blah-$RANDOM-$RANDOM"
    sh -c "$cmdline" # > /tmp/filename
fi
