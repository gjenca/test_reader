#!/bin/bash
# vim: et ts=4 sw=4 sta ai
cat ../../riesenia/repos |
    while read USER_REPO;
    do
        (cd ../../riesenia/
        SRC=$(find $USER_REPO -name '*.py')
        NUM=$(echo $SRC | wc -l)
        if [ ! "$NUM" == "1" ]
        then 
            echo 'Zly pocet zdrojakov v' $USER_REPO > /dev/stderr
            continue
        fi
        RIESENIE='../../riesenia/'"$SRC"
        NAME=`echo $RIESENIE | cut -f4 -d/`
        echo "$RIESENIE:$NAME"
        )
    done
