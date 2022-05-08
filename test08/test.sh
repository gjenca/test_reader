#killall python3 2>/dev/null
source test_prepare.sh
python3 "$1"  >/dev/null& 
PIDRIESENIE=$!
sleep 0.2
python3 test.py
EXIT_STATUS=$?
kill -sTERM $PIDRIESENIE 2>/dev/null
echo '>>>' Killed PID "$PIDRIESENIE"
echo '>>> Checking with ps:' $(ps --pid $PIDRIESENIE)
echo '>>> Test exit status:' "$EXIT_STATUS"
source test_cleanup.sh
exit $EXIT_STATUS
