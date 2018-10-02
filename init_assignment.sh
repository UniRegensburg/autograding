#!/bin/bash
# Script for initializing a directory for grading assignments.
# to be executed in the respective directory where a ZIP file with all assignments lies.


#################
# Set up script #
#################

# filenames are separated by newlines
IFS=$'\n'

TOOLDIR=$(dirname "$0")
if [[ -d $1 ]]; then
    BASEDIR="$1"
else
    BASEDIR="."
fi

NAME_PATTERN='s/\.\/abgaben\/(.+) (.+)_(\d+)_assignsubmission_file_\/(.*)/.\/abgaben\/$2_$1_$3_$4/'

echo ">> Using tooldir \"$TOOLDIR\""
echo ">> Using basedir \"$BASEDIR\""


######################################
# Get, extract, and preprocess files #
######################################

# get ZIP file with assignments and $TODO file with grading template from Moodle
# TODO: automate this, manually at the moment

ZIPFILE=$(ls $BASEDIR/EIMI_*.zip)
if [[ ! -f $ZIPFILE ]]; then
    echo "no zip file with assignments found in $BASEDIR"
    exit 1
fi

# create directory for all assignments
mkdir "$BASEDIR/abgaben"
7z -o"$BASEDIR/abgaben" x "$ZIPFILE"

# rename files so that the surname comes first
#for f in $(ls -1 $BASEDIR/abgaben/); do
#    echo "$f"
#    rename -v -e "${NAME_PATTERN}" "$f"
#done

rename -v -e ${NAME_PATTERN} $BASEDIR/abgaben/*/*
rmdir $BASEDIR/abgaben/* 2>/dev/null

# generate encoding statistics
echo 
echo "Encodings used in submissions:"
(for f in ${BASEDIR}/abgaben/*.txt; do file -b "$f"; done) | sort | uniq -c | sort -nr 


