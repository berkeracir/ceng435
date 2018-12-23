#!/bin/bash

USERNAME=$1
SSH_KEY=$2

REMOTE="pc1.lan.sdn.uky.edu"
S_PORT=26374
B_PORT=26370
R1_PORT=26372
R2_PORT=26373
D_PORT=26371

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

SOURCE_INPUT="dummy_5mb.txt"
BROKER_OUTPUT="broker_out.txt"
DESTINATION_OUTPUT="destination_out.txt"

if [ -n "$USERNAME" ]; then
	if [ -n "$SSH_KEY" ]; then
		if [ -f "$SSH_KEY" ]; then
			ssh-add $SSH_KEY
            gnome-terminal -x bash -c "ssh -X -t -i $SSH_KEY -p $B_PORT $USERNAME@$REMOTE \"echo 'BROKER'; python broker.py $BROKER_OUTPUT; bash -l\""
			gnome-terminal -x bash -c "ssh -X -t -i $SSH_KEY -p $D_PORT $USERNAME@$REMOTE \"echo 'DESTINATION'; python destination.py $DESTINATION_OUTPUT; bash -l\""
            gnome-terminal -x bash -c "ssh -X -t -i $SSH_KEY -p $S_PORT $USERNAME@$REMOTE \"echo 'SOURCE'; python source.py $DESTINATION_OUTPUT; bash -l\""
		else
			echo "SSH Key ($2) does not exist!"
		fi
	else
		echo "Missing Parameter: ${0##*/} $1 <SSH_KEY>"
	fi
else
	echo "Missing Parameter: ${0##*/} <USERNAME> <SSH_KEY>"
fi