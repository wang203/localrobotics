#! /bin/bash
python takeoff.py &
echo "before sleep"
sleep 10
echo "after sleep"
killall -9 python
python controller.py
