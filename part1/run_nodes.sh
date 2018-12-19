#!/bin/bash

S_IP="localhost"
S_PORT="10004"

B_IP="localhost"
B_PORT="10003"

R1_IP="localhost"
R1_PORT="10001"

R2_IP="localhost"
R2_PORT="10002"

D_IP="localhost"
D_PORT="10000"

#gnome-terminal -x bash -c "clean; echo destination.py; echo "============="; python $PWD/destination.py"
gnome-terminal -x bash -c "echo 1-router.py; echo "========="; python $PWD/router.py $R1_IP $R1_PORT"
gnome-terminal -x bash -c "echo 2-router.py; echo "========="; python $PWD/router.py $R2_IP $R2_PORT"
gnome-terminal -x bash -c "echo broker.py; echo "============="; python $PWD/broker.py $B_IP $B_PORT $R1_IP $R1_PORT $R2_IP $R2_PORT"
gnome-terminal -x bash -c "echo source.py; echo "========="; python $PWD/source.py $B_IP $B_PORT"
clear; echo destination.py; echo "============="; python $PWD/destination.py $D_IP $D_PORT