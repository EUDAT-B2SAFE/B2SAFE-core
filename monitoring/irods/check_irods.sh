#!/bin/bash
#The MIT License (MIT)
#
#Copyright (c) 2015 Johan Guldmyr CSC
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
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
# Tested with IRODS 4.0.3, API Version=d, OS authentication
# Irods updates the available free space once a day.
##

VERSION="0.4"

### Settings
# Nagios return codes
OK="0"
WARN="1"
CRITICAL="2"
UNKNOWN="3"

usage() {
	echo "This is an Irods health check. It currently takes no arguments."
	echo "Version: $VERSION"
	exit "$UNKNOWN"
}

TEMPFILE=$(mktemp)
if [ "$?" != 0 ]; then
	echo "UNKNOWN: problem creating tempfile as user $USER on hostname $HOSTNAME."
	exit 3
fi
# This removes the path to the file
FILENAMEONIRODS=$(basename $TEMPFILE)

# Set this to 1 for some extra output
DEBUG=0

#COMMANDS
iput="iput"
iget="iget"
irm="irm"
irmtrash="irmtrash"
ils="ils"
rm="rm"

if [ "$DEBUG" != 0 ]; then
iput_opt="-v"
iget_opt="-v"
irm_opt="-v"
irmtrash_opt="-v"
ils_opt="-v"
rm_opt="-v"
fi

### End of settings

safety() {

	which ils >/dev/null 2>&1
	if [ "$?" != 0 ]; then
		echo "UNKNOWN: Could not find ils in \$PATH"
		exit $UNKNOWN
	fi
	 
        if [ "$TEMPFILE" == "/" ] || [ "$TEMPFILE" == "/etc" ]; then
                echo "UNKNOWN: $TEMPFILE looks bad."
                exit 3
        fi
 
	ils >/dev/null 2>&1
	if [ "$?" != 0 ]; then
		echo "UNKNOWN: Could not list with ils"
		exit $UNKNOWN
	fi
}

perfdataf() {
	which ilsresc >/dev/null 2>&1
	if [ "$?" != 0 ]; then
		echo "UNKNOWN: Could not find ilsresc in \$PATH"
		exit $UNKNOWN
	fi
	 
	RESOURCES="$(ilsresc |grep -v "resource group")"
	re='^[0-9]+$'

	# To find out free space of irods resouces that publish this information via ilsresc
	for res in $RESOURCES; do
		FREESPACE=$(ilsresc -l|grep -A 8 "resource name: $res"|grep "free space"|cut -d ":" -f2|sed -e 's/\ //')
		if [[ $FREESPACE =~ $re ]] ; then
		perfdata="$perfdata $res$_free_space=$FREESPACE"
		fi
	done

	# Number of users/groups:
	users=$(iquest "%s" "select count(USER_ID) where USER_TYPE <> 'rodsgroup'")
	groups=$(iquest "%s" "select count(USER_NAME) where USER_TYPE = 'rodsgroup'")
	perfdata="$perfdata users=$users groups=$groups"
	echo $perfdata|sed -e 's/^,//'
}

writeafile() {

        which iput >/dev/null 2>&1
        if [ "$?" != 0 ]; then
                echo "UNKNOWN: Could not find iput in \$PATH"
                exit $UNKNOWN
        fi

	date >> "$TEMPFILE"
	if [ "$DEBUG" != 0 ]; then
		echo "contents of $TEMPFILE:"
		cat "$TEMPFILE"
                "$iput" "$iput_opt" "$TEMPFILE"
        else
                "$iput" "$TEMPFILE"
	fi
	return "$?"
}

listafile() {
        which ils >/dev/null 2>&1
        if [ "$?" != 0 ]; then
                echo "UNKNOWN: Could not find ils in \$PATH"
                exit $UNKNOWN
        fi
        
        if [ "$DEBUG" != 0 ]; then
  		"$ils" "$ils_opt" "$FILENAMEONIRODS"
        else
                "$ils" "$FILENAMEONIRODS"
	fi
	return "$?"
}

getafile() {

        which iget >/dev/null 2>&1
        if [ "$?" != 0 ]; then
                echo "UNKNOWN: Could not find iget in \$PATH"
                exit $UNKNOWN
        fi

	cd
        if [ "$DEBUG" != 0 ]; then
                "$iget" "$iget_opt" "$FILENAMEONIRODS"
        else
                "$iget" "$FILENAMEONIRODS"
        fi
        IGETSTATUS="$?"
        if [ "$DEBUG" != 0 ]; then
                "$rm" "$rm_opt" "$FILENAMEONIRODS"
        else
                "$rm" "$FILENAMEONIRODS"
        fi
	return "$IGETSTATUS"
}

removeafile() {

        which irm >/dev/null 2>&1
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
	        "$irm" "$irm_opt" "$FILENAMEONIRODS"
        else
                "$irm" "$FILENAMEONIRODS"
        fi
	IRMSTATUS="$?"

        if [ "$DEBUG" != 0 ]; then
                "$rm" "$rm_opt" "$TEMPFILE"
        else
		"$rm" "$TEMPFILE"
        fi
        
	return "$IRMSTATUS"
}

removetrash() {

        which irmtrash >/dev/null 2>&1
        if [ "$?" != 0 ]; then
                echo "UNKNOWN: Could not find irmtrash in \$PATH"
                exit $UNKNOWN
        fi

	"$irmtrash" "$irmtrash_opt" 2>/dev/null
	IRMTSTATUS="$?"
	return "$?"
}


### Execution

# argument check
if [ "$1" != "" ];then
	usage
fi

safety

PERFDATA="$(perfdataf)"

writeafile
writestatus="$?"
#listafile
#liststatus="$?"
getafile
getstatus="$?"
removeafile
removestatus="$?"
removetrash
removetrashstatus="$?"

### Checking the returns of the functions

if [ "$writestatus" != 0 ] || [ "$getstatus" != 0 ] || [ "$removestatus" != 0 ] || [ "$removetrashstatus" != 0 ]; then
	echo "CRITICAL: writestatus = $writestatus, getstatus = $getstatus, removestatus = $removestatus, removetrashstatus = $removetrashstatus | $PERFDATA"
	exit $WARNING
elif [ "$writestatus" == 0 ] || [ "$getstatus" == 0 ] || [ "$removestatus" == 0 ] || [ "$removetrashstatus" == 0 ]; then
	echo "OK: writestatus = $writestatus, getstatus = $getstatus, removestatus = $removestatus, removetrashstatus = $removetrashstatus | $PERFDATA"
	exit $OK

fi
