#!/bin/bash

R1_PORT = 10001
R2_PORT = 10002

#gnome-terminal -x bash -c "clean; echo destination.py; echo "============="; python $PWD/destination.py"
gnome-terminal -x bash -c "echo 1-router.py; echo "========="; python $PWD/router.py $R1_PORT"
gnome-terminal -x bash -c "echo 2-router.py; echo "========="; python $PWD/router.py $R2_PORT"
gnome-terminal -x bash -c "echo broker.py; echo "============="; python $PWD/broker.py"
gnome-terminal -x bash -c "echo source.py; echo "========="; python $PWD/source.py"
clear; echo destination.py; echo "============="; python $PWD/destination.py