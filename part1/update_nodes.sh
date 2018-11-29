#!/bin/bash

USERNAME=$1

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
	scp -P $S_PORT source.py $USERNAME@$S:/users/$USERNAME
	scp -P $B_PORT broker.py $USERNAME@$B:/users/$USERNAME
	scp -P $R1_PORT router.py $USERNAME@$R1:/users/$USERNAME
	scp -P $R2_PORT router.py $USERNAME@$R2:/users/$USERNAME
	scp -P $D_PORT destionation.py $USERNAME@$D:/users/$USERNAME
else
	echo "Missing parameter: ${0##*/} USERNAME"
fi
