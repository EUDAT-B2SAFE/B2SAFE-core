#! /bin/bash
#    file name   : eudat-update-checksums
#    created     : 26.05.2014
#    project     : EUDAT
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

RES_NAME='demoResc'
DEF_INPUT='checksum-verify-results'

ATTR_NAME='eudat_dpm_checksum_date:'

MKTEMP="mktemp -t eudat-update-checksums.XXXXXX"


###############################################
# usage
###############################################
usage()
{
  echo "Usage: $0 [-r <iRods_resource>] [-i <input_results_dir>] [-l log_level] <root_path_of_the resource>"
  echo "       $0 -h | --help"
  echo "The script reads files from <input_results_dir> in order of their creation."
  echo "The files contain results of the checksum verification, including verification time."
  echo "The script sets the new time in iCAT."
  echo "Amount of logging info is controlled by <log_level>. Allowed values are $FAILED-$EXTRA_DEBUG."
  echo "Defaults:"
  echo "  <iRods_resource> = $RES_NAME"
  echo "  <input_results_dir> = <root_path_of_the resource>/../$DEF_INPUT"
  echo "  <log_level> = $LOG_PRIORITY"
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
# update_one_file
###############################################
update_one_record()
{
  local subpath result ver_time
  subpath=$1
  result=$2
  ver_time=$3

  data_object="/$ZONE/$subpath"

  if [ "$result" != "OK" ]
  then
    log $ERROR "Verification of $data_object at $ver_time failed."
    return 1
  fi
  
  log $DEBUG "Processing $data_object at $ver_time."

  prev_time=`imeta ls -d $data_object $ATTR_NAME|tail -n+2|sed 's/^[a-z]*: //'|gawk -v resc=$RES_NAME 'BEGIN {RS = "\n-+\n"; FS= "\n"} {print $2;}'`

  if [ -z "$prev_time" ]
  then
    log $ERROR "Cannot process $data_object."
    return 1
  fi
  
  if (( $prev_time < $ver_time ))
  then
    imeta set -d $data_object $ATTR_NAME $ver_time
    irule -F updatePidChecksum.r "*path='$data_object'"
  fi
  
  return 0
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
    -r)
        RES_NAME=$2
        shift 2
        ;;
    -i)
        INPUT=$2
        shift 2
        ;;
    *)
        log $ERROR "Invalid parameter $1."
        usage
        exit 2
        ;;
  esac
done


RES_PATH=$1

if [ -z "$RES_PATH" ]
then
  log $ERROR "<root_path_of_the resource> parameter is missing."
  usage
  exit 2
fi

if ! [ -d "$RES_PATH" ]
then
  log $ERROR "The paths of the candidate files $RES_PATH is not a valid directory."
  exit 1
fi

RES_PARENT=`echo $RES_PATH| sed 's/[\/]*[^\/]*[\/]*$//'`

if ! [ -n "$INPUT" ]
then
  INPUT="$RES_PARENT/$DEF_INPUT"
fi

if ! [ -d "$INPUT" ] || ! [ -x "$INPUT" ] || ! [ -r "$INPUT" ]
then
  log $ERROR "The input results directory $INPUT cannot be read."
  exit 1
fi

tmp_ilsresc=`$MKTEMP`
ilsresc -l $RES_NAME > $tmp_ilsresc
if [ $? -ne 0 ]
then
  log $ERROR "Invalid resource $RES_NAME."
  exit 1
fi

ATTR_NAME=$ATTR_NAME$RES_NAME

log $NOTICE "$0 started, <iRods_resource>=$RES_NAME, <input_results_dir>=$INPUT <root_path_of_the resource>=$RES_PATH"

ZONE=`grep zone $tmp_ilsresc|sed 's/^[a-z ]*: //'`

log $INFO "Zone is $ZONE."
rm $tmp_ilsresc


for input_file in $INPUT/results.*
do
  log $INFO "Processing $input_file."
  while read subpath result ver_time
  do
    update_one_record $subpath $result $ver_time
  done < $input_file
done
