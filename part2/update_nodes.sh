#!/bin/bash

USERNAME=$1
SSH_KEY=$2

S="pc1.lan.sdn.uky.edu"
S_PORT=26374
B="pc1.lan.sdn.uky.edu"
B_PORT=26370
R1="pc1.lan.sdn.uky.edu"
R1_PORT=26372
R2="pc1.lan.sdn.uky.edu"
R2_PORT=26373
D="pc1.lan.sdn.uky.edu"
D_PORT=26371

if [ -n "$USERNAME" ]; then
	if [ -n "$SSH_KEY" ]; then
		if [ -f "$SSH_KEY" ]; then
			ssh-add $SSH_KEY
			scp -i $SSH_KEY -P $S_PORT source.py $USERNAME@$S:/users/$USERNAME
			scp -i $SSH_KEY -P $B_PORT broker.py $USERNAME@$B:/users/$USERNAME
			scp -i $SSH_KEY -P $D_PORT destination.py $USERNAME@$D:/users/$USERNAME
		else
			echo "SSH Key with path: $2 does not exist!"
		fi
	else
		echo "Missing Parameter: ${0##*/} $1 <SSH_KEY>"
	fi
else
	echo "Missing Parameter: ${0##*/} <USERNAME> <SSH_KEY>"
fi