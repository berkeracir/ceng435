#!/bin/bash

USERNAME=$1
SSH_KEY=$2

S="pc2.instageni.washington.edu"
S_PORT=28662
B="pc2.instageni.washington.edu"
B_PORT=28658
R1="pc2.instageni.washington.edu"
R1_PORT=28660
R2="pc2.instageni.washington.edu"
R2_PORT=28661
D="pc2.instageni.washington.edu"
D_PORT=28659

if [ -n "$USERNAME" ]; then
	if [ -n "$SSH_KEY" ]; then
		if [ -f "$SSH_KEY" ]; then
			ssh-add $SSH_KEY
			scp -i $SSH_KEY -P $S_PORT source.py $USERNAME@$S:/users/$USERNAME
			scp -i $SSH_KEY -P $B_PORT broker.py $USERNAME@$B:/users/$USERNAME
			scp -i $SSH_KEY -P $R1_PORT router.py $USERNAME@$R1:/users/$USERNAME
			scp -i $SSH_KEY -P $R2_PORT router.py $USERNAME@$R2:/users/$USERNAME
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