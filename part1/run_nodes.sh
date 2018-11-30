#!/bin/bash

#gnome-terminal -x bash -c "clean; echo destination.py; echo "============="; python $PWD/destination.py"
gnome-terminal -x bash -c "echo 1-router.py; echo "========="; python $PWD/router.py 10001"
gnome-terminal -x bash -c "echo 2-router.py; echo "========="; python $PWD/router.py 10002"
gnome-terminal -x bash -c "echo broker.py; echo "============="; python $PWD/broker.py"
gnome-terminal -x bash -c "echo source.py; echo "========="; python $PWD/source.py"
clear; echo destination.py; echo "============="; python $PWD/destination.py