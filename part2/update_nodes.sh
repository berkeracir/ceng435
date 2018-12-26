#!/bin/bash

USERNAME=$1
SSH_KEY=$2

S="pc3.genirack.nyu.edu"
S_PORT=25894
B="pc3.genirack.nyu.edu"
B_PORT=25890
R1="pc3.genirack.nyu.edu"
R1_PORT=25892
R2="pc3.genirack.nyu.edu"
R2_PORT=25893
D="pc3.genirack.nyu.edu"
D_PORT=25891

if [ -n "$USERNAME" ]; then
	if [ -n "$SSH_KEY" ]; then
		if [ -f "$SSH_KEY" ]; then
			ssh-add $SSH_KEY
			scp -i $SSH_KEY -P $S_PORT source.py dummy_5mb.txt  dummy_100kb.txt $USERNAME@$S:/users/$USERNAME
			scp -i $SSH_KEY -P $B_PORT broker.py dummy_5mb.txt dummy_100kb.txt $USERNAME@$B:/users/$USERNAME
			scp -i $SSH_KEY -P $D_PORT destination.py dummy_5mb.txt dummy_100kb.txt $USERNAME@$D:/users/$USERNAME
		else
			echo "SSH Key with path: $2 does not exist!"
		fi
	else
		echo "Missing Parameter: ${0##*/} $1 <SSH_KEY>"
	fi
else
	echo "Missing Parameter: ${0##*/} <USERNAME> <SSH_KEY>"
fi