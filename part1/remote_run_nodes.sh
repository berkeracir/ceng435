#!/bin/bash

USERNAME=$1
SSH_KEY=$2

REMOTE="pc1.instageni.hawaii.edu"
S_PORT=26014
B_PORT=26010
R1_PORT=26012
R2_PORT=26013
D_PORT=26011

PORT=51795

IF_SB_1="10.10.1.1"
IF_SB_2="10.10.1.2"

IF_BR1_1="10.10.2.1"
IF_BR1_2="10.10.2.2"

IF_BR2_1="10.10.4.1"
IF_BR2_2="10.10.4.2"

IF_R1D_1="10.10.3.1"
IF_R1D_2="10.10.3.2"

IF_R2D_1="10.10.5.1"
IF_R2D_2="10.10.5.2"

TIME_SYNC="sudo sed -i 's/#NTP=/NTP=0.ro.pool.ntp.org 1.ro.pool.ntp.org/' /etc/systemd/timesyncd.conf; sudo sed -i 's/#FallbackNTP=/FallbackNTP=ntp.ubuntu.com 0.arch.pool.ntp.org/' /etc/systemd/timesyncd.conf; sudo timedatectl set-ntp true"

if [ -n "$USERNAME" ]; then
	if [ -n "$SSH_KEY" ]; then
		if [ -f "$SSH_KEY" ]; then
			ssh-add $SSH_KEY
            gnome-terminal -x bash -c "ssh -X -t -i $SSH_KEY -p $B_PORT $USERNAME@$REMOTE \"$TIME_SYNC; echo 'BROKER'; python broker.py $IF_SB_2 $PORT $IF_BR1_2 $PORT $IF_BR2_2 $PORT; bash -l\""
			gnome-terminal -x bash -c "ssh -X -t -i $SSH_KEY -p $R1_PORT $USERNAME@$REMOTE \"$TIME_SYNC; echo 'ROUTER1'; python router.py $IF_BR1_2 $PORT $IF_R1D_2 $PORT; bash -l\""
			gnome-terminal -x bash -c "ssh -X -t -i $SSH_KEY -p $R2_PORT $USERNAME@$REMOTE \"$TIME_SYNC; echo 'ROUTER2'; python router.py $IF_BR2_2 $PORT $IF_R2D_2 $PORT; bash -l\""
			gnome-terminal -x bash -c "ssh -X -t -i $SSH_KEY -p $D_PORT $USERNAME@$REMOTE \"$TIME_SYNC; echo 'DESTINATION'; python destination.py $IF_R1D_2 $PORT $IF_R2D_2 $PORT; bash -l\""
			sleep 5
            gnome-terminal -x bash -c "ssh -X -t -i $SSH_KEY -p $S_PORT $USERNAME@$REMOTE \"$TIME_SYNC; echo 'SOURCE'; python source.py $IF_SB_2 $PORT; bash -l\""
# \"kill -9 $(netstat -ap | grep :51795 | cut -d'/' -s -f1 | rev | cut -d' ' -f1 | rev); echo 'BROKER'; python broker.py $IF_SB_2 $PORT $IF_BR1_2 $PORT $IF_BR2_2 $PORT\""
            #gnome-terminal -x bash -c "ssh -X -i $SSH_KEY -p $S_PORT $USERNAME@$REMOTE \"echo 'SOURCE'; python source.py $IF_SB_2 $PORT\""
		else
			echo "SSH Key ($2) does not exist!"
		fi
	else
		echo "Missing Parameter: ${0##*/} $1 <SSH_KEY>"
	fi
else
	echo "Missing Parameter: ${0##*/} <USERNAME> <SSH_KEY>"
fi

#gnome-terminal -x bash -c "clean; echo destination.py; echo "============="; python $PWD/destination.py"
#gnome-terminal -x bash -c "echo 1-router.py; echo "========="; python $PWD/router.py $R1_IP $R1_PORT"
#gnome-terminal -x bash -c "echo 2-router.py; echo "========="; python $PWD/router.py $R2_IP $R2_PORT"
#gnome-terminal -x bash -c "echo broker.py; echo "============="; python $PWD/broker.py $B_IP $B_PORT $R1_IP $R1_PORT $R2_IP $R2_PORT"
#gnome-terminal -x bash -c "echo source.py; echo "========="; python $PWD/source.py $B_IP $B_PORT"
#clear; echo destination.py; echo "============="; python $PWD/destination.py $D_IP $D_PORT