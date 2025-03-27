#!/usr/bin/env bash
set -m
if which rkill ; then
    KILL=rkill
elif which kill ; then
    KILL=kill # rkill je na Mac OS
    echo '>>> WARNING: Cannot find rkill, using kill instead. Some child processes may stay hanging.'
    echo '>>> WARNING: Install pslist package to avoid this message.'
fi
if [ -e test_prepare.sh ]
then	
	echo '>>> Running test_prepare.sh'
	source test_prepare.sh
fi
echo '>>> Starting server'
sleep 0.02
python3 "$1"  >"$2" & 
PIDRIESENIE=$!
sleep 0.1
echo '>>> Running test.py'
python3 test.py
EXIT_STATUS=$?
echo ">>> Killing server process with $KILL"
$KILL $PIDRIESENIE 2>&1
if [ $? != 0 ]; then
    echo ">>> $KILL failed, the server probably already exitted"
else
    echo '>>>' Killed server PID "$PIDRIESENIE"
fi
wait $PIDRIESENIE 2>/dev/null
echo '>>> Checking with ps:' $(ps -p $PIDRIESENIE)
echo '>>> Test exit status:' "$EXIT_STATUS"
if [ -e test_cleanup.sh ]
then	
	echo '>>> Running test_cleanup.sh'
	source test_cleanup.sh
fi
echo '>>> Exitting test.sh'
exit $EXIT_STATUS
