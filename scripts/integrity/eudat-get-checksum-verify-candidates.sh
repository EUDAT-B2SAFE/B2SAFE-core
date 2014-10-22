#! /bin/bash
#    file name   : eudat-get-checksum-verify-candidates
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
VALID_DAYS=365

ATTR_NAME='eudat_dpm_checksum_date:'

MKTEMP="mktemp -t eudat-get-checksum-verify-candidates.XXXXXX"


###############################################
# usage
###############################################
usage()
{
  echo "Usage: $0 [-r iRods_resource] [-d valid_days] [-l log_level] <candidates_file>"
  echo "       $0 -h | --help"
  echo "The script queries iCAT and gets list of physisical data replicas that are candidates to verify checksum."
  echo "The result is written to <candidates_file>"
  echo "Only replicas located on <iRods_resource> and those having checksum verified before <valid_days>."
  echo "Amount of logging info is controlled by <log_level>. Allowed values are $FAILED-$EXTRA_DEBUG."
  echo "Defaults:"
  echo "  <iRods_resource> = $RES_NAME"
  echo "  <valid_days> = $VALID_DAYS"
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
    -d)
        VALID_DAYS=$2
        shift 2
        ;;
    *)
        log $ERROR "Invalid parameter $1."
        usage
        exit 2
        ;;
  esac
done

candidates_file=$1

if [ -z "$candidates_file" ]
then
  log $ERROR "<candidates_file> parameter is missing."
  usage
  exit 2
fi


log $NOTICE "$0 started, <iRods_resource>=$RES_NAME, <valid_days>=$VALID_DAYS <candidates_file>=$candidates_file"

touch $candidates_file
if [ $? -ne 0 ]
then
  log $ERROR "Cannot create candidates file $candidates_file."
  exit 2
fi

ATTR_NAME=$ATTR_NAME$RES_NAME

tmp_file1=`$MKTEMP`

iquest --no-page "SELECT COLL_NAME, DATA_NAME, DATA_CHECKSUM, META_DATA_ATTR_VALUE WHERE META_DATA_ATTR_NAME = '$ATTR_NAME' AND DATA_RESC_NAME = '$RES_NAME'" > $tmp_file1
if [ $? -ne 0 ]
then
  log $ERROR "iquest failed."
  exit 2
fi

no_results=`wc -l $tmp_file1|gawk '{print $1}'`
no_results=$((no_results/5))

log $INFO "iCAT query returned $no_results results."
log $DEBUG "Query results in $tmp_file1."

if (( $no_results < 1 )); then
  log $NOTICE "Query returned no result."
  exit 1
fi

curr_sec=`date +"%s"`
((valid_sec=$curr_sec - $VALID_DAYS*86400))

log $DEBUG "Current time is $curr_sec. Filtering objects with checksum date older than $valid_sec and convering to records."

tmp_file2=`$MKTEMP`
cat $tmp_file1|sed 's/^[A-Z_]* = //'|gawk -v VALID_SEC=$valid_sec 'BEGIN {RS = "\n-+\n"; FS= "\n"} (NF>=4) && (VALID_SEC>$4)  {print $1 "/" $2 " " $3 " " $4;}' > $tmp_file2

log $DEBUG "Results formatted in $tmp_file2"

no_results=`wc -l $tmp_file2|gawk '{print $1}'`
if (( $no_results < 1 ))
then
  log $NOTICE "There is no candidate to verify checksum."
  exit 1
fi

zone=`ilsresc -l hsmResc|grep zone|sed 's/^[a-z ]*: //'`
log $INFO "Removing zone $zone from the paths."

sed "s/\/$zone\///" $tmp_file2 > $candidates_file

log $NOTICE "$no_results candidates in $candidates_file"

rm $tmp_file1
rm $tmp_file2

exit 0
