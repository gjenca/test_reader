#!/bin/bash
# vim: et ts=4 sw=4 sta ai

WHICH="$1"

if ! command -v pygmentize >/dev/null
then
    exit 0
fi
echo '>>> Converting source code'
mkdir -p source
./riesenia"$WHICH".sh $@ |
while IFS=: read RIESENIE NAME ; do
    if [ "$NAME" == "" ]
    then
        NAME="noname"
    fi
    OUT="source/${NAME}.html"
    if [ \( ! -e "$OUT" \) -o \( "$RIESENIE" -nt "$OUT" \) ]; then
        echo "$RIESENIE" '->' "$OUT" > /dev/stderr
        pygmentize -l python -f html -O full -O linenos -o "$OUT" "$RIESENIE"
    fi
done
echo '>>> Done'

