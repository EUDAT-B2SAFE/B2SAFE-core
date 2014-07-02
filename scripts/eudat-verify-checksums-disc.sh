#! /bin/bash
#    file name   : eudat-verify-checksums-disc
#    created     : 02.06.2014
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

DEF_INPUT='checksum-verify-candidates'
DEF_OUTPUT='checksum-verify-results'

MKTEMP='mktemp -t eudat-verify-checksums-disc.XXXXXX'


###############################################
# usage
###############################################
usage()
{
  echo "Usage: $0 [-i <input_candidates_file>] [-o <output_results_dir>] [-l log_level] <root_path_of_the resource>"
  echo "       $0 -h | --help"
  echo "The script reads input file with candidates to verify checksum <input_candidates_file>>,"
  echo "recalculates the checksums and writes verification results to a file in <output_results_dir> directory."
  echo "The paths of the candidate files are relative to <root_path_of_the resource>."
  echo "Amount of logging info is controlled by <log_level>. Allowed values are $FAILED-$EXTRA_DEBUG."
  echo "Defaults:"
  echo "  <input_candidates_file> = <root_path_of_the resource>/../$DEF_INPUT"
  echo "  <output_results_dir> = <root_path_of_the resource>/../$DEF_OUTPUT"

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
# nds_consume_recalled_user
###############################################
serve_one_record()
{

  local subpath checksum prev_time curr_sec old_checksum new_checksum

  if [ "$#" -lt  3 ] ; then
    log $ERROR "Incorrect record: $1-$2-$3."
    return 1
  fi

  subpath=$1
  checksum=$2
  prev_time=$3

  if [[ $checksum == sha2:* ]]
  then
   #sha256
    log $DEBUG "Computing sha256 for $RES_PATH/$subpath..."
    old_checksum=`echo "$checksum"|sed 's/^sha2://'|base64 -d -i|hexdump -v -e '/1 "%02x" '`
    new_checksum=`sha256sum $RES_PATH/$subpath|gawk '{print $1}'`
  else
   #md5
    log $DEBUG "Computing md5 for $RES_PATH/$subpath..."
    old_checksum=$checksum
    new_checksum=`md5sum $RES_PATH/$subpath|gawk '{print $1}'`
  fi

  curr_sec=`date +"%s"`

  if [ "$old_checksum" = "$new_checksum" ]
  then
    echo "$subpath OK $curr_sec" >> $OUTPUT_TMP
    log $DEBUG "Checksum OK."
  else
    echo "$subpath ERR $curr_sec" >> $OUTPUT_TMP
    log $ERROR "Invalid checksum $RES_PATH/$subpath."
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

if ! [ -f "$INPUT" ] || ! [ -r "$INPUT" ]
then
  log $ERROR "The input candidates file $INPUT cannot be read."
  exit 1
fi

if ! [ -n "$OUTPUT" ]
then
  OUTPUT="$RES_PARENT/$DEF_OUTPUT"
fi

if ! [ -d "$OUTPUT" ] || ! [ -x "$OUTPUT" ] || ! [ -w "$OUTPUT" ]
then
  log $ERROR "The output results directory $OUTPUT cannot be written."
  exit 1
fi


log $NOTICE "$0 started, <input-candidates-file> = $INPUT, <output-results-dir> = $OUTPUT, <root_path_of_the resource>=$RES_PATH"

INPUT_TMP=`$MKTEMP`
OUTPUT_TMP=`$MKTEMP`

log $DEBUG "INPUT_TMP=$INPUT_TMP"
log $DEBUG "OUTPUT_TMP=$OUTPUT_TMP"

mv $INPUT $INPUT_TMP
if [ $? -ne 0 ]
then
  log $ERROR "Cannot move $INPUT to $INPUT_TMP."
  exit 1
fi

log $INFO "Input candidates file $INPUT moved to temporary file."

while read subpath checksum prev_time
do
  serve_one_record $subpath $checksum $prev_time
done < $INPUT_TMP

curr_sec=`date +"%s"`
OUTPUT_FILE="$OUTPUT/results.$curr_sec"
mv $OUTPUT_TMP $OUTPUT_FILE
if [ $? -ne 0 ]
then
  log $ERROR "Cannot move $OUTPUT_TMP to $OUTPUT_FILE."
  exit 1
fi


log $INFO "Temporary results file moved to $OUTPUT_FILE."

rm $INPUT_TMP

log $NOTICE "$0 finished, results stored in $OUTPUT_FILE."

exit 0
