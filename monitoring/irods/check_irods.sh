#!/bin/bash
#The MIT License (MIT)
#
#Copyright (c) 2015 Johan Guldmyr CSC
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation fi/les (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.
# 
### 
# This is a nagios check that checks if one can write, ils, get and remove to
# a preconfigured irods.
# Tested with IRODS 4.1.7, API Version=d, OS authentication
# Irods updates the available free space once a day.
##

VERSION="0.6"
SUB_VERSION="0"

### Settings
# Nagios return codes
OK="0"
WARN="1"
CRITICAL="2"
UNKNOWN="3"

usage() {
	echo "This is an iRODS health check."
        echo "Usage: check_irods.sh [-h|-v|-n|-d|-t time|-f file|-p file]"
        echo "       -h help"
        echo "       -v version"
        echo "       -f the path of the iRODS environment json file. See iRODS documentation for details."
        echo "       -p the path of the file containing the password to connect to iRODS."
        echo "       -n implies no trash can enabled within the iRODS instance."
        echo "       -d debug enabled."
        echo "       -t timeout limit in seconds. The default is 30 s."
}

TEMPFILE=$(mktemp)
if [ "$?" != 0 ]; then
	echo "UNKNOWN: problem creating tempfile as user $USER on hostname $HOSTNAME."
	exit 3
fi
WORK_DIR=$(mktemp -d)
if [ "$?" != 0 ]; then
        echo "UNKNOWN: problem creating tempdir as user $USER on hostname $HOSTNAME."
        exit 3
fi
# This removes the path to the file
FILENAMEONIRODS=$(basename $TEMPFILE)

# Set this to 1 for some extra output
DEBUG=0

# Set this to 1 if iRODS has not enabled the trash can 
NOTRASHCAN=0

#COMMANDS
iput="iput"
iget="iget"
irm="irm"
irmtrash="irmtrash"
ilsresc="ilsresc"
iinit="iinit"
iquest="iquest"
ils="ils"
rm="rm"

### End of settings

safety() {

	which $ils >/dev/null 2>&1
	if [ "$?" != 0 ]; then
		echo "UNKNOWN: Could not find ils in \$PATH"
		exit $UNKNOWN
	fi
	 
        if [ "$TEMPFILE" == "/" ] || [ "$TEMPFILE" == "/etc" ]; then
                echo "UNKNOWN: $TEMPFILE looks bad."
                exit 3
        fi
 
	$ils >/dev/null 2>&1
	if [ "$?" != 0 ]; then
		echo "UNKNOWN: Could not list with ils"
		exit $UNKNOWN
	fi
}

perfdataf() {
	which $ilsresc >/dev/null 2>&1
	if [ "$?" != 0 ]; then
		echo "UNKNOWN: Could not find ilsresc in \$PATH"
		exit $UNKNOWN
	fi
	 
	RESOURCES="$($ilsresc |grep -v "resource group")"
	re='^[0-9]+$'

	# To find out free space of irods resources that publish this information via ilsresc
	for res in $RESOURCES; do
		FREESPACE=$($ilsresc -l|grep -A 8 "resource name: $res"|grep "free space"|cut -d ":" -f2|sed -e 's/\ //')
		if [[ $FREESPACE =~ $re ]] ; then
		perfdata="$perfdata $res$_free_space=$FREESPACE"
		fi
	done

	# Number of users/groups:
	users=$($iquest "%s" "select count(USER_ID) where USER_TYPE <> 'rodsgroup'")
	groups=$($iquest "%s" "select count(USER_NAME) where USER_TYPE = 'rodsgroup'")
	perfdata="$perfdata users=$users groups=$groups"
	echo $perfdata|sed -e 's/^,//'
}

writeafile() {
        which $iput >/dev/null 2>&1
        if [ "$?" != 0 ]; then
                echo "UNKNOWN: Could not find iput in \$PATH"
                exit $UNKNOWN
        fi

	date >> "$TEMPFILE"
	if [ "$DEBUG" != 0 ]; then
		echo "contents of $TEMPFILE:"
		cat "$TEMPFILE"
                echo "Executing command: $iput -v $TEMPFILE"
                $iput -v "$TEMPFILE"
        else
                $iput "$TEMPFILE"
	fi
	return "$?"
}

listafile() {
        which $ils >/dev/null 2>&1
        if [ "$?" != 0 ]; then
                echo "UNKNOWN: Could not find ils in \$PATH"
                exit $UNKNOWN
        fi
        
        if [ "$DEBUG" != 0 ]; then
                echo "Executing command: $ils -v $FILENAMEONIRODS"
  		$ils -v "$FILENAMEONIRODS"
        else
                $ils "$FILENAMEONIRODS" >/dev/null 2>&1
	fi
	return "$?"
}

getafile() {
        which $iget >/dev/null 2>&1
        if [ "$?" != 0 ]; then
                echo "UNKNOWN: Could not find iget in \$PATH"
                exit $UNKNOWN
        fi
	cd 
        if [ "$DEBUG" != 0 ]; then
                echo "Executing command: $iget -v $FILENAMEONIRODS"
                $iget -v "$FILENAMEONIRODS"
        else
                $iget "$FILENAMEONIRODS"
        fi
        IGETSTATUS="$?"
        if [ "$DEBUG" != 0 ]; then
                $rm -v "$FILENAMEONIRODS"
        else
                $rm "$FILENAMEONIRODS"
        fi
	return "$IGETSTATUS"
}

removeafile() {

        which $irm >/dev/null 2>&1
        if [ "$?" != 0 ]; then
                echo "UNKNOWN: Could not find irm in \$PATH"
                exit $UNKNOWN
        fi
	if [ "$TEMPFILE" == "/" ] || [ "$TEMPFILE" == "/etc" ]; then
		echo "UNKNOWN: $TEMPFILE looks bad."
		exit 3
	fi

	cd
        if [ "$DEBUG" != 0 ]; then
                echo "Executing command: $irm -v $FILENAMEONIRODS"
	        $irm -v "$FILENAMEONIRODS"
        else
                $irm "$FILENAMEONIRODS"
        fi
	IRMSTATUS="$?"

        if [ "$DEBUG" != 0 ]; then
                echo "Executing command: $rm -v $TEMPFILE"
                $rm -v "$TEMPFILE"
        else
		$rm "$TEMPFILE"
        fi
        
	return "$IRMSTATUS"
}

removetrash() {

        which $irmtrash >/dev/null 2>&1
        if [ "$?" != 0 ]; then
                echo "UNKNOWN: Could not find irmtrash in \$PATH"
                exit $UNKNOWN
        fi

        if [ "$DEBUG" != 0 ]; then
                echo "Executing command: $irmtrash -v"
                $irmtrash -v
        else
                $irmtrash
        fi
        IRMTSTATUS="$?"
	return "$IRMTSTATUS"
}

function run_with_timeout { 
    cmd="$1"; timeout="$2";
    grep -qP '^\d+$' <<< $timeout || timeout=30

    ( 
        eval "$cmd" &
        child=$!
        trap -- "" SIGTERM 
        (       
                sleep $timeout
                kill $child 2> /dev/null 
        ) &     
        wait $child
        return $?
    )
}

execute_checks() {
    
        if [ "$DEBUG" != 0 ]; then
             echo "Exporting IRODS_ENVIRONMENT_FILE=$opt_f"
             echo "Exporting HOME=$WORK_DIR"
        fi
        declare -x IRODS_ENVIRONMENT_FILE="$opt_f"
        declare -x HOME="$WORK_DIR"

        if [ "$DEBUG" != 0 ]; then
             echo "Initializing credentials: $iinit < $opt_p"
             $iinit < $opt_p
        else
             $iinit < $opt_p >/dev/null 2>&1
        fi

        safety

        PERFDATA="$(perfdataf)"

        writeafile
        writestatus="$?"
        listafile
        liststatus="$?"
        getafile
        getstatus="$?"
        removeafile
        removestatus="$?"
        if [ $NOTRASHCAN == 0 ]; then
            removetrash
            removetrashstatus="$?"
        else
            removetrashstatus=0
        fi

        unset IRODS_ENVIRONMENT_FILE

        if [ "$DEBUG" != 0 ]; then
                echo "Executing command: $rm -v -rf $WORK_DIR"
                $rm -v -rf "$WORK_DIR"
        else
                $rm -rf "$WORK_DIR"
        fi        

        ### Checking the returns of the functions

        if [ "$writestatus" != 0 ] || [ "$liststatus" != 0 ] || [ "$getstatus" != 0 ] || [ "$removestatus" != 0 ] || [ "$removetrashstatus" != 0 ]; then
	    echo "CRITICAL: writestatus = $writestatus, liststatus = $liststatus, getstatus = $getstatus, removestatus = $removestatus, removetrashstatus = $removetrashstatus | $PERFDATA"
	    exit $CRITICAL
        elif [ "$writestatus" == 0 ] || [ "$liststatus" != 0 ] || [ "$getstatus" == 0 ] || [ "$removestatus" == 0 ] || [ "$removetrashstatus" == 0 ]; then
	    echo "OK: writestatus = $writestatus, liststatus = $liststatus, getstatus = $getstatus, removestatus = $removestatus, removetrashstatus = $removetrashstatus | $PERFDATA"
	    exit $OK
        fi
}


### Execution

if [ "$#" == "0" ]; then
    usage
    exit 1
fi

while getopts "vhndt:f:p:" opt; do
  if [ "$opt" == "?" ]; then
      exit 1
  fi
  declare "opt_$opt=${OPTARG:-0}"
done

if [ "$opt_h" == "0" ]; then
      usage
      exit 0
fi

if [ "$opt_v" == "0" ]; then
      echo "version $VERSION"
      exit 0
fi

if [ "$opt_n" == "0" ]; then
      NOTRASHCAN=1
fi

if [ "$opt_d" == "0" ]; then
      DEBUG=1
fi

if [ "$opt_f" == "" ]; then
      echo "Error: irods env json file is manadatory"
      exit 1
fi

if [ "$opt_p" == "" ]; then
      echo "Error: irods password file is manadatory"
      exit 1
fi

if [ "$opt_t" == "" ]; then
      TIMEOUT=30
else
      TIMEOUT=$opt_t
fi

run_with_timeout execute_checks $TIMEOUT

if [ "$?" != "0" ]; then
      echo "CRITICAL: timed out after $TIMEOUT seconds"
      exit $CRITICAL
fi
