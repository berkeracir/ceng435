#!/bin/bash

USERNAME=$1
SSH_KEY=$2

REMOTE="pc3.genirack.nyu.edu"
S_PORT=25894
B_PORT=25890
R1_PORT=25892
R2_PORT=25893
D_PORT=25891

if [ -n "$USERNAME" ]; then
	if [ -n "$SSH_KEY" ]; then
		if [ -f "$SSH_KEY" ]; then
			ssh-add $SSH_KEY
			scp -i $SSH_KEY -P $S_PORT $USERNAME@$REMOTE:/users/$USERNAME/exp*.txt  experiments/
		else
			echo "SSH Key with path: $2 does not exist!"
		fi
	else
		echo "Missing Parameter: ${0##*/} $1 <SSH_KEY>"
	fi
else
	echo "Missing Parameter: ${0##*/} <USERNAME> <SSH_KEY>"
fi