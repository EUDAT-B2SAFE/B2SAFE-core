#! /bin/bash
#    file name   : eudat-verify-checksums-hpss-hsi
#    created     : 02.06.2014
#    project     : EUDAT
#    author      : John Alan Kennedy
#    email       : jkennedy@mpcdf.mpg.de
#    note        : Adapted from original work by                                                                                                                           
#    author      : Michal Jankowski                                                                                                                                         
#    email       : jankowsk@man.poznan.pl                                                                                                                                   

PRIORITIES=(FAILED ERROR WARNING NOTICE INFO DEBUG)
FAILED=0
ERROR=1
WARNING=2
NOTICE=3
INFO=4
DEBUG=5
EXTRA_DEBUG=6
LOG_PRIORITY=$NOTICE

MYNAME=$( basename $0 )
#PIDFILE="/var/run/$MYNAME.pid"
PIDFILE="/tmp/$MYNAME.pid"

MKTEMP='mktemp -t eudat-verify-checksums.XXXXXX'

###############################################
# usage
###############################################
usage()
{
	echo "Usage: $0 [-i <input_candidates_file>] [-o <output_results_dir>] [-l log_level] -s <root_path_of_the resource>"
	echo "       $0 -h | --help"
	echo 
	echo "This script is the local variant of the hpss checksum verification - to be run on the same node as the irods server"
	echo "The script reads a local input file with candidates to verify checksum <input_candidates_file>,"
	echo "recalculates the checksums, via hsi, and writes the verification results to a file in the <output_results_dir> directory."
	echo "The input_candidates_file needs to be an absolute path (not just a filename)"
	echo ""
	echo "The Output dir <output_results_dir> is filesystem dir where the results file should be finally placed"
	echo ""
	echo "The root path of the resource <root_path_of_the resource> is the base of the HPSS namespace where the irods reource is anchored"
	echo ""
}


###############################################
# log
###############################################
log()
{
	local priority message
	priority=$1
	message=$2

	if [ $priority -le $LOG_PRIORITY ]
	then
		echo "${PRIORITIES[$priority]}: $$: `date +\"%Y.%m.%d %H:%M:%S\"`: $message"
	fi
}

###############################################
# check if script is already running
###############################################
isrunning()
{
	  if [ -e "$PIDFILE" ]; then
		  cpid=$(cat "$PIDFILE")
		  if [[ "$cpid" =~ ^[0-9]+$ ]] &&  [[ $( ps -p "$cpid"   --no-headers -o args ) =~ "$MYNAME" ]]; then
			  echo "$MYNAME is already running"
			  return 0
		  else
			  rm -f "$PIDFILE"
		  fi
	  fi
	  echo $$ > $PIDFILE
	  return 1
}

###############################################
# compare_checksums:
# compare the from the input and output files
###############################################
compare_checksums()
{

	local old_checksum_file new_checksum_file output

	old_checksum_file=$1
	new_hecksum_file=$2
	output=$3 

	while read subpath checksum prev_time
	do
		old_checksum=$(echo ${checksum} | cut -d: -f2)
		new_checksum=$(grep -E "${subpath}\$"  ${new_hecksum_file} | cut -d' ' -f1) 
		curr_sec=`date +"%s"`

		if [ "$old_checksum" = "$new_checksum" ]
		then
			echo "$subpath OK $curr_sec" >> $OUTPUT_TMP
		else
			echo "$subpath ERR $curr_sec" >> $OUTPUT_TMP
		fi

	done < $old_checksum_file

}

###############################################
# run_hsi_command_file:
# small wrapper to call hsi with a commands file as input
###############################################
run_hsi_command_file()
{

	local hsi_command_file output
	hsi_command_file=$1
	output=$2

	hsi "out ${output}; in ${hsi_command_file}" > /dev/null 2>&1
	#hsi "out ${output}; in ${hsi_command_file}" 

}

###############################################
# create_hsi_command_file:
# create the hsi commands file which will run multiple checksum creates on HPSS resident files
###############################################
create_hsi_command_file()
{

	local input output hpss_root_path
	input=$1
	output=$2
	hpss_root_path=$3

	rm -rf $output
	touch $output

	while read subpath checksum prev_time
	do
		if [[ $checksum == sha2:* ]]
		then
			#sha256
			echo "hashcreate -A -H sha256  ${hpss_root_path}/${subpath}" >> $output
		else
			#md5
			echo "hashcreate -A -H md5  ${hpss_root_path}/${subpath}" >> $output
		fi

	done < $input


}


#######################################################################################
#
# main
#
#######################################################################################
if [ "$1" == "-h" ]
then
	usage
	exit 0
fi


while [ $# -gt 1 ]
do
	case $1 in
		-l)
			LOG_PRIORITY=$2
			shift 2
			;;
		-s)
			STORAGE_PATH=$2
			shift 2
			;;
		-i)
			INPUT=$2
			shift 2
			;;
		-o)
			OUTPUT=$2
			shift 2
			;;
		*)
			log $ERROR "Invalid parameter $1."
			usage
			exit 1
			;;
	esac
done

# exit if script is already running
isrunning && exit 1


if [ -z "$STORAGE_PATH" ]
then
	log $ERROR "<root_path_of_the resource> parameter is missing."
	usage
	exit 2
fi

if [ -z "$INPUT" ]
then
	log $ERROR "The input candidates file parameter is missing."
	exit 1
fi

if [ -z "$OUTPUT" ]
then
	log $ERROR "The output results directory parameter is missing."
	exit 1
fi


log $NOTICE "$0 started, <input-candidates-file> = $INPUT, <output-results-dir> = $OUTPUT, <root_path_of_the resource>=$STORAGE_PATH"

INPUT_TMP=`$MKTEMP`
OUTPUT_TMP=`$MKTEMP`

log $DEBUG "INPUT_TMP=$INPUT_TMP"
log $DEBUG "OUTPUT_TMP=$OUTPUT_TMP"

cp $INPUT $INPUT_TMP

log $INFO "Input candidates file $INPUT moved to temporary file."

create_hsi_command_file $INPUT_TMP hsi_commnds_file.hsi $STORAGE_PATH

run_hsi_command_file hsi_commnds_file.hsi hsi_commnds_output.log

compare_checksums $INPUT_TMP hsi_commnds_output.log $OUTPUT_TMP

# remove the hsi output file
rm hsi_commnds_output.log

curr_sec=`date +"%s"`
OUTPUT_FILE="$OUTPUT/results.$curr_sec"

cp $OUTPUT_TMP $OUTPUT_FILE

log $INFO "Temporary results file moved to HPSS $OUTPUT_FILE."

# Clean the temp files
rm $INPUT_TMP
rm $OUTPUT_TMP

log $NOTICE "$0 finished, results stored in HPSS $OUTPUT_FILE."

exit 0



