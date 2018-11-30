#!/bin/bash

USERNAME=$1
SSH_KEY=$2

S="pc1.instageni.hawaii.edu"
S_PORT=26014
B="pc1.instageni.hawaii.edu"
B_PORT=26010
R1="pc1.instageni.hawaii.edu"
R1_PORT=26012
R2="pc1.instageni.hawaii.edu"
R2_PORT=26013
D="pc1.instageni.hawaii.edu"
D_PORT=26011

if [ -n "$USERNAME" ]; then
	if [ -n "$SSH_KEY" ]; then
		if [ -f "$SSH_KEY" ]; then
			ssh-add $SSH_KEY
			scp -i $SSH_KEY -P $S_PORT source.py $USERNAME@$S:/users/$USERNAME
			scp -i $SSH_KEY -P $B_PORT broker.py $USERNAME@$B:/users/$USERNAME
			scp -i $SSH_KEY -P $R1_PORT router.py $USERNAME@$R1:/users/$USERNAME
			scp -i $SSH_KEY -P $R2_PORT router.py $USERNAME@$R2:/users/$USERNAME
			scp -i $SSH_KEY -P $D_PORT destionation.py $USERNAME@$D:/users/$USERNAME
		else
			echo "SSH Key with path: $2 does not exist!"
		fi
	else
		echo "Missing Parameter: ${0##*/} $1 <SSH_KEY>"
	fi
else
	echo "Missing Parameter: ${0##*/} <USERNAME> <SSH_KEY>"
fi