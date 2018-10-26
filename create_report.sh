#!/bin/bash

#################
# Set up script #
#################

errcho(){ >&2 echo $@; }

# filenames are separated by newlines
IFS=$'\n'

TOOLDIR=$(dirname $0)
if [[ -d $1 ]]; then
    BASEDIR="$1"
else
    BASEDIR="."
fi

if [[ -d ${BASEDIR}/abgaben ]]; then
    ASSDIR=${BASEDIR}/abgaben
else
    echo ">>> No assignment dir found in $BASEDIR! <<<"
    exit 1
fi

if [[ ! -f ${TOOLDIR}/check_assignment.py ]]; then
    echo ">>> No check_assignment.py script found in $BASEDIR <<<"
    exit 1
fi

echo "#>> Using tooldir \"$TOOLDIR\""
echo "#>> Using basedir \"$BASEDIR\""
echo "#>> Using assignments dir \"$ASSDIR\""

echo 'ID,Name,Punkte,Bewertung,"Feedback als Kommentar"'
for f in `ls $ASSDIR/*.txt`; do
    errcho "Processing $f ..."
    ${TOOLDIR}/check_assignment.py $f
done

