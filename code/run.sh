#! /bin/bash
:<<'COMMENT'
python takeoff.py &
echo "before sleep"
sleep 10
COMMENT
echo "after sleep"
killall -9 python
python controller.py
