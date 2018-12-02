#!/bin/bash

USERNAME=$1
SSH_KEY=$2

REMOTE="pc2.instageni.washington.edu"
S_PORT=28662
B_PORT=28658
R1_PORT=28660
R2_PORT=28661
D_PORT=28659

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

#TIME_SYNC="sudo ntpd -q 172.17.1.9"

#echo "ssh -X -t -i $SSH_KEY -p $B_PORT $USERNAME@$REMOTE \"python broker.py $IF_SB_2 $PORT $IF_BR1_2 $PORT $IF_BR2_2 $PORT\""
#echo "ssh -X -t -i $SSH_KEY -p $R1_PORT $USERNAME@$REMOTE \"python router.py $IF_BR1_2 $PORT $IF_R1D_2 $PORT\""
#echo "ssh -X -t -i $SSH_KEY -p $R2_PORT $USERNAME@$REMOTE \"python router.py $IF_BR2_2 $PORT $IF_R2D_2 $PORT\""
#echo "ssh -X -t -i $SSH_KEY -p $D_PORT $USERNAME@$REMOTE \"python destination.py $IF_R1D_2 $PORT $IF_R2D_2 $PORT\""
#echo "ssh -X -t -i $SSH_KEY -p $S_PORT $USERNAME@$REMOTE \"python source.py $IF_SB_2 $PORT\""
#exit

if [ -n "$USERNAME" ]; then
	if [ -n "$SSH_KEY" ]; then
		if [ -f "$SSH_KEY" ]; then
			ssh-add $SSH_KEY
            gnome-terminal -x bash -c "ssh -X -t -i $SSH_KEY -p $B_PORT $USERNAME@$REMOTE \"echo 'BROKER'; python broker.py $IF_SB_2 $PORT $IF_BR1_2 $PORT $IF_BR2_2 $PORT; bash -l\""
			gnome-terminal -x bash -c "ssh -X -t -i $SSH_KEY -p $R1_PORT $USERNAME@$REMOTE \"echo 'ROUTER1'; python router.py $IF_BR1_2 $PORT $IF_R1D_2 $PORT; bash -l\""
			gnome-terminal -x bash -c "ssh -X -t -i $SSH_KEY -p $R2_PORT $USERNAME@$REMOTE \"echo 'ROUTER2'; python router.py $IF_BR2_2 $PORT $IF_R2D_2 $PORT; bash -l\""
			gnome-terminal -x bash -c "ssh -X -t -i $SSH_KEY -p $D_PORT $USERNAME@$REMOTE \"echo 'DESTINATION'; python destination.py $IF_R1D_2 $PORT $IF_R2D_2 $PORT; bash -l\""
            gnome-terminal -x bash -c "ssh -X -t -i $SSH_KEY -p $S_PORT $USERNAME@$REMOTE \"sleep 5; echo 'SOURCE'; python source.py $IF_SB_2 $PORT; bash -l\""
		else
			echo "SSH Key ($2) does not exist!"
		fi
	else
		echo "Missing Parameter: ${0##*/} $1 <SSH_KEY>"
	fi
else
	echo "Missing Parameter: ${0##*/} <USERNAME> <SSH_KEY>"
fi