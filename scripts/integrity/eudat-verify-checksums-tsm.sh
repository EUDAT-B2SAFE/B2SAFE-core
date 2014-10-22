#! /bin/bash
#    file name   : eudat-verify-checksums-tsm.sh
#    created     : 02.07.2014
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

MYNAME=$( basename $0 )
PIDFILE="/var/run/$MYNAME.pid"


DEF_INPUT='checksum-verify-candidates'
DEF_OUTPUT='checksum-verify-results'

MKTEMP='mktemp -t eudat-verify-checksums-tsm.XXXXXX'

STORAGE_PATH=""
SPACE_PATH=""

# Limit number of bytes to recall in single run, default is LTO5 max capacity
MAX_RECALL_BYTES=1649267441665

#the list of files that migration is locked
MIGRATION_BLACKLIST="migration.blacklist"

# Max. time in sec. for computing checksums 
# and for GPFS to lock migration of verified files 
# default: 12h
LOCK_MIGRATION_SEC=43200

#default mandatory days is one year +2 weeks (365+14)
VALID_DAYS=369

###############################################
# usage
###############################################
usage()
{
  echo "Usage: $0 [-i <input_candidates_file>] [-o <output_results_dir>] [-d <mandatory_valid_days>]"
  echo "          [-l <log_level>] -s <root_path_of_the_resource> -f <filesystem name>"    
  echo "       $0 -h | --help"
  echo
  echo "The script reads input <input_candidates_file> (default: <root_path_of_the_resource>/../$DEF_INPUT) "
  echo "with candidates to verify checksum. The paths of the candidate files are relative to <root_path_of_the_resource>."
  echo "The recomputation of checksums of candidates in state 'r' or 'p' is imediatelly started in recalculation process."
  echo "The candidates in state 'm' are subject for tape optimized recall operation. In the first step of the recall, "
  echo "the list of tapes and ordered files is prepared. In the next step, tapes that have no file with checksum time "
  echo "older than now - <mandatory_valid_days> (default: $VALID_DAYS) are excluded from the workflow."
  echo "Note, that <valid_days> of corresponding eudat-get-checksum-verify-candidates call shall be greater than "
  echo "<mandatory_valid_days> preferably by several days in order to optimize recall process."
  echo "Then, the script in a loop recalls files from a single tape and recalculates the checksums for them, "
  echo "until all the tapes are recalled. The parameter <filesystem name> is filesystem name used by TSM commands."
  echo "Results of the verification are written to files in <output_results_dir> directory "
  echo "(default: <root_path_of_the_resource>/../$DEF_OUPUT)."
  echo
  echo "Amount of logging info is controlled by <log_level>. Allowed values are $FAILED-$EXTRA_DEBUG."
  echo "Default <log_level> is $LOG_PRIORITY"
  echo
  echo "The script must be run with root privileges."
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

  local subpath checksum prev_time curr_sec old_checksum new_checksum output

  if [ "$#" -lt  4 ] ; then
    log $ERROR "Incorrect record: $1-$2-$3-$4."
    return 1
  fi

  subpath=$1
  checksum=$2
  prev_time=$3
  output=$4

  if [[ $checksum == sha2:* ]]
  then
   #sha256
    log $DEBUG "Computing sha256 for $STORAGE_PATH/$subpath..."
    old_checksum=`echo "$checksum"|sed 's/^sha2://'|base64 -d -i|hexdump -v -e '/1 "%02x" '`
    new_checksum=`sha256sum $STORAGE_PATH/$subpath|gawk '{print $1}'`
  else
   #md5
    log $DEBUG "Computing md5 for $STORAGE_PATH/$subpath..."
    old_checksum=$checksum
    new_checksum=`md5sum $STORAGE_PATH/$subpath|gawk '{print $1}'`
  fi

  curr_sec=`date +"%s"`

  if [ "$old_checksum" = "$new_checksum" ]
  then
    echo "$subpath OK $curr_sec" >> $output
    log $DEBUG "Checksum OK."
  else
    echo "$subpath ERR $curr_sec" >> $output
    log $ERROR "Invalid checksum $STORAGE_PATH/$subpath."
  fi
   
}

#######################################################################################
# compute_checksum
#######################################################################################
compute_checksum()
{
  local input output_tmp output_file
  input=$1

  log $INFO "Compute checksums for $input."
  
  output_tmp=`$MKTEMP`
  
  while read subpath checksum prev_time
  do
    serve_one_record $subpath $checksum $prev_time $output_tmp
  done < $input

  curr_sec=`date +"%s"`
  output_file="$OUTPUT/results.$curr_sec"

  mv $output_tmp $output_file
  if [ $? -ne 0 ]
  then
    log $ERROR "Cannot move $output_tmp $output_file."
    exit 1
  fi

  chown $INPUT_UID:$INPUT_UID $output_file
  log $NOTICE "Computed checksums written to $output_file."

  return 0
}

#######################################################################################
# remove obsolete blacklist entries
#######################################################################################
update_migration_blacklist()
{
  log $NOTICE "Updating migration blacklist file"
  timestamp=$(date +%s)
  migration_blacklist_file="$STORAGE_PATH/$MIGRATION_BLACKLIST"
  if [ -f $migration_blacklist_file ]
  then
     mv $migration_blacklist_file $migration_blacklist_file.bak
     gawk -v CDATE=$timestamp 'BEGIN{FS=";"}{if($2>CDATE)print $0}' $migration_blacklist_file.bak > $migration_blacklist_file
     rm $migration_blacklist_file.bak
  fi
  return 0
}

#######################################################################################
# prepare_recall_files
#######################################################################################
prepare_recall_files()
{
  local forrecall local_collection_list
  local tmp_input_for_dsmrecall tmp_dsmrecall_output
  forrecall=$1

  if [ ! -f $forrecall ] || [ ! -s $forrecall ]
  then
    log $INFO "Nothing to recall."
    log $DEBUG "$forrecall not exists or it is empty."
    return 1
  fi

  #prepare list for dsmrecall
  tmp_input_for_dsmrecall=`$MKTEMP`
  gawk  -v STORAGE_PATH=$STORAGE_PATH '{print STORAGE_PATH "/" $1;}' $forrecall > $tmp_input_for_dsmrecall

  log $DEBUG "Input for dsmrecall prepared."
  [ $EXTRA_DEBUG -le $LOG_PRIORITY ] && cat $tmp_input_for_dsmrecall

  #call dsmrecall with prepare option
  tmp_dsmrecall_output=`$MKTEMP`
  dsmrecall -p -FILElist=$tmp_input_for_dsmrecall $FS_NAME > $tmp_dsmrecall_output
  rm $tmp_input_for_dsmrecall
  log $INFO "dsmrecall with prepare called"
  [ $EXTRA_DEBUG -le $LOG_PRIORITY ] && cat $tmp_dsmrecall_output

  #get the collection list from the output
  local_collection_list=`grep "Output collection list created" $tmp_dsmrecall_output | sed 's/^.* : //'`

  if [ ! "$local_collection_list" ] || [ ! -f $local_collection_list ]
  then
    rm $tmp_dsmrecall_output
    log $ERROR "No output collection list created"
    return 1
  fi

  rm $tmp_dsmrecall_output

  log $INFO "Collection list is $local_collection_list"
  [ $EXTRA_DEBUG -le $LOG_PRIORITY ] && cat $local_collection_list

  eval "$2=$local_collection_list" 

  return 0
}


#######################################################################################
# recall_files
#######################################################################################
recall_files()
{

  local forrecall_records_mnd forrecall_records_opt
  local recall_collection_mnd recall_collection_opt recall_collection_fin
  local recall_tape_path_opt 
  local tmp_recall_tapes_mnd tmp_recall_tapes_opt tmp_recall_tapes_add
  local tape_file
  local tmp_forrecall_files_fin tmp_forrecall_files_sorted
  local tmp_forrecall_records_all tmp_forrecall_records_all_sorted
  local tmp_forrecall_records_fin

  forrecall_records_mnd=$1
  forrecall_records_opt=$2

  #prepare recall collection for mandatory files
  log $INFO "Preparing for recall records of mandatory files."
  prepare_recall_files $forrecall_records_mnd recall_collection_mnd
  if [ $? -ne 0 ]
  then
    log $INFO "No mandatory collection to process."
    return 1
  fi
  log $INFO "Mandatory collection is $recall_collection_mnd."

  #extract lists of mandatory tapes
  tmp_recall_tapes_mnd=`$MKTEMP`
  sed -e 's/^.*\///' $recall_collection_mnd|sort > $tmp_recall_tapes_mnd
  log $DEBUG "List of mandatory tapes $tmp_recall_tapes_mnd prepared."
  [ $EXTRA_DEBUG -le $LOG_PRIORITY ] && cat $tmp_recall_tapes_mnd

  tmp_forrecall_files_fin=`$MKTEMP`

  #prepare recall collection for optional files
  log $INFO "Preparing for recall records of optional files."
  prepare_recall_files $forrecall_records_opt recall_collection_opt
  if [ $? -ne 0 ]
  then
    log $INFO "No optional collection to process."
  else
    log $INFO "Optional collection is $recall_collection_opt."
    
    #get path to the collection lists of of the optional files
    recall_tape_path_opt=`head -n1 $recall_collection_opt|gawk '{print $3;}'|xargs dirname`
    log $DEBUG "Path to the collection lists of of the optional files: $recall_tape_path_opt"

    #extract lists of optional tapes
    tmp_recall_tapes_opt=`$MKTEMP`
    sed -e 's/^.*\///' $recall_collection_opt|sort > $tmp_recall_tapes_opt
    log $DEBUG "List of optional tapes $tmp_recall_tapes_opt prepared."
    [ $EXTRA_DEBUG -le $LOG_PRIORITY ] && cat $tmp_recall_tapes_opt


    tmp_recall_tapes_add=`$MKTEMP`
    comm -12 $tmp_recall_tapes_mnd $tmp_recall_tapes_opt |gawk -v OPATH=$recall_tape_path_opt '{print OPATH "/" $1;}' > $tmp_recall_tapes_add

    log $DEBUG "List of additional tapes $tmp_recall_tapes_add prepared."
    [ $EXTRA_DEBUG -le $LOG_PRIORITY ] && cat $tmp_recall_tapes_add

    # Read the tape files and extract files for the final recall
    while read tape_file
    do
      gawk '{print $4}' $tape_file >> $tmp_forrecall_files_fin
    done <  $tmp_recall_tapes_add
    rm $tmp_recall_tapes_opt
    rm $tmp_recall_tapes_add

  fi

  gawk '{print $3;}' $recall_collection_mnd > $tmp_recall_tapes_mnd
  log $DEBUG "List of mandatory tapes $tmp_recall_tapes_mnd prepared."
  [ $EXTRA_DEBUG -le $LOG_PRIORITY ] && cat $tmp_recall_tapes_mnd

  # Read the tape files and extract files for the final recall
  while read tape_file
  do
    gawk '{print $4}' $tape_file >> $tmp_forrecall_files_fin
  done <  $tmp_recall_tapes_mnd

  rm $tmp_recall_tapes_mnd

  tmp_forrecall_files_fin_sorted=`$MKTEMP`
  sed -e 's@^'"$STORAGE_PATH"'/@@' $tmp_forrecall_files_fin | sort | uniq > $tmp_forrecall_files_fin_sorted

  log $DEBUG "Final list of files to recall $tmp_forrecall_files_fin_sorted prepared and sorted."
  [ $EXTRA_DEBUG -le $LOG_PRIORITY ] && cat $tmp_forrecall_files_fin_sorted

  rm $tmp_forrecall_files_fin

  #prepare comon list of all records
  tmp_forrecall_records_all=`$MKTEMP`
  tmp_forrecall_records_all_sorted=`$MKTEMP`

  cp $forrecall_records_mnd $tmp_forrecall_records_all
  cat $forrecall_records_opt >> $tmp_forrecall_records_all
  sort $tmp_forrecall_records_all > $tmp_forrecall_records_all_sorted
  
  #join the final list of files with forrecall records
  #in order to select records for the final recall
  tmp_forrecall_records_fin=`$MKTEMP`
  join -j 1 $tmp_forrecall_records_all_sorted  $tmp_forrecall_files_fin_sorted > $tmp_forrecall_records_fin
  log $DEBUG "Records for the final recall $tmp_forrecall_records_fin prepared."
  [ $EXTRA_DEBUG -le $LOG_PRIORITY ] && cat $tmp_forrecall_records_fin

  rm $tmp_forrecall_records_all
  rm $tmp_forrecall_records_all_sorted
  rm $tmp_forrecall_files_fin_sorted
  
  #prepare recall collection for finally selected files
  log $INFO "Preparing for recall records of finally selected files."
  prepare_recall_files $tmp_forrecall_records_fin recall_collection_fin
  if [ $? -ne 0 ]
  then
    log $INFO "No final collection to process."
    return 1
  fi
  log $INFO "Final collection is $recall_collection_fin."

  #Do the actual recall
  tmp_final_recall_output=`$MKTEMP`
  log $DEBUG "Calling the actual dsmrecall."
  dsmrecall -FILElist=$recall_collection_fin $FS_NAME > $tmp_final_recall_output
  log $INFO "The actual dsmrecall called."
  [ $EXTRA_DEBUG -le $LOG_PRIORITY ] && cat $tmp_final_recall_output

  rm $tmp_final_recall_output
  
  compute_checksum $tmp_forrecall_records_fin  

  rm $tmp_forrecall_records_fin
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
    -d)
        VALID_DAYS=$2
        shift 2
        ;;
    -s)
        STORAGE_PATH=$2
        shift 2
        ;;
    -f)
        FS_NAME=$2
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
  log $ERROR "<root_path_of_the_resource> parameter is missing."
  usage
  exit 2
fi

if ! [ -d "$STORAGE_PATH" ]
then
  log $ERROR "<root_path_of_the_resource> $STORAGE_PATH is not a valid directory."
  exit 1
fi

if [ -z "$FS_NAME" ]
then
  log $ERROR "<filesystem_name> parameter is missing."
  usage
  exit 2
fi

SPACE_PATH=`echo $STORAGE_PATH| sed 's/[\/]*[^\/]*[\/]*$//'`

if ! [ -n "$INPUT" ]
then
  INPUT="$SPACE_PATH/$DEF_INPUT"
fi

if ! [ -f "$INPUT" ] || ! [ -r "$INPUT" ]
then
  log $NOTICE "There is no input file $INPUT, or it is empty. Nothing to do."
  exit 0
fi

INPUT_UID=`stat -c %u $INPUT`
INPUT_GID=`stat -c %g $INPUT`

if ! [ -n "$OUTPUT" ]
then
  OUTPUT="$SPACE_PATH/$DEF_OUTPUT"
fi

if ! [ -d "$OUTPUT" ] || ! [ -x "$OUTPUT" ] || ! [ -w "$OUTPUT" ]
then
  log $ERROR "The output results directory $OUTPUT cannot be written."
  exit 1
fi

log $NOTICE "$0 started, <input-candidates-file> = $INPUT, <output-results-dir> = $OUTPUT, <root_path_of_the resource> = $STORAGE_PATH, <tolerance_days> = $TOLERANCE_DAYS"


curr_sec=`date +"%s"`
((valid_sec=$curr_sec - $VALID_DAYS*86400))

log $DEBUG "Current time is $curr_sec. Objects with checksum date older than $valid_sec must be racalled mandatory."

#remove obsolete locks for GPFS migration
update_migration_blacklist

#optimize input: remove empty lines, sort, remove duplicates
tmp_optimized_input=`$MKTEMP`

sort -n -k 3,3 $INPUT | sed '/^[[:space:]]*$/d' > $tmp_optimized_input

log $DEBUG "Input optimized."
[ $EXTRA_DEBUG -le $LOG_PRIORITY ] && cat $tmp_optimized_input

rm $INPUT
log $DEBUG "The original input file removed."

#prepare list for dsmls
tmp_input_for_dsmls=`$MKTEMP`
gawk  -v STORAGE_PATH=$STORAGE_PATH '{print STORAGE_PATH "/" $1 }' $tmp_optimized_input > $tmp_input_for_dsmls

log $DEBUG "Input for dsmls prepared."
[ $EXTRA_DEBUG -le $LOG_PRIORITY ] && cat $tmp_input_for_dsmls

# call dsmls, remove unnecesary lines from output (empty, not begining with number) and select 4. and 5. column - (file state and name)
tmp_dsmls_result=`$MKTEMP`
dsmls -FILElist=$tmp_input_for_dsmls|sed '/^$/d'|sed 's/^[ \t]*//'|sed '/^[^0-9]/d'|sed 's/[ \t]\+/ /g'|gawk '{ print $4 " " $NF;}' > $tmp_dsmls_result
rm $tmp_input_for_dsmls

log $DEBUG "dsmls finished."
[ $EXTRA_DEBUG -le $LOG_PRIORITY ] && cat $tmp_dsmls_result

# merge dsmls result with the input
tmp_dsmls_merged=`$MKTEMP`
paste -d " " $tmp_optimized_input $tmp_dsmls_result > $tmp_dsmls_merged
rm $tmp_optimized_input
rm $tmp_dsmls_result

log $DEBUG "dsmls result merged with input."
[ $EXTRA_DEBUG -le $LOG_PRIORITY ] && cat $tmp_dsmls_merged

#split the result into 2 files: incache and forrecall
tmp_incache=`$MKTEMP`
tmp_forrecall=`$MKTEMP`
tmp_forrecall_opt=`$MKTEMP`

gawk -v INCACHE=$tmp_incache -v FORRECALL=$tmp_forrecall -v FORRECALLOPT=$tmp_forrecall_opt -v VALIDSEC=$valid_sec '{regexp="/" $5 "$"; if (match($1, regexp)  || $1==$5) { if($4=="m") { if($3 < VALIDSEC) print $1 FS $2 FS $3 > FORRECALL; else print $1 FS $2 FS $3 > FORRECALLOPT; } else print $1 FS $2 FS $3 > INCACHE;} else print "ERROR: " $5 " not in path " $1 "/" $2; }' $tmp_dsmls_merged

rm $tmp_dsmls_merged

no=`wc -l $tmp_forrecall`
log $INFO "Total $no files for mandatory recall."
[ $EXTRA_DEBUG -le $LOG_PRIORITY ] && cat $tmp_forrecall

no=`wc -l $tmp_forrecall_opt`
log $INFO "Total $no files for optional recall."
[ $EXTRA_DEBUG -le $LOG_PRIORITY ] && cat $tmp_forrecall_opt

no=`wc -l $tmp_incache`
log $INFO "Total $no files in cache."
[ $EXTRA_DEBUG -le $LOG_PRIORITY ] && cat $tmp_incache

#Add files present in cache to the output
compute_checksum $tmp_incache
rm $tmp_incache

#recall those for recall
recall_files $tmp_forrecall $tmp_forrecall_opt
rm $tmp_forrecall
rm $tmp_forrecall_opt

log $INFO "Script finished with success."

