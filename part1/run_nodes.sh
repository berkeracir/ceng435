#!/bin/bash

gnome-terminal -x bash -c "echo destination.py; echo "============="; python $PWD/destination.py"
gnome-terminal -x bash -c "echo router.py; echo "========="; python $PWD/router.py"
gnome-terminal -x bash -c "echo source.py; echo "========="; python $PWD/source.py"