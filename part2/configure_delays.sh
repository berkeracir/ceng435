#!/bin/bash

USERNAME=$1
SSH_KEY=$2

REMOTE="pc3.genirack.nyu.edu"
S_PORT=25894
B_PORT=25890
R1_PORT=25892
R2_PORT=25893
D_PORT=25891

#sudo tc qdisc change dev [INTERFACE] root netem loss L% corrupt C% duplicate D% delay Dms reorder R% r%
#EXP1:
#sudo tc qdisc change dev [INTERFACE] root netem loss 0.5% corrupt 0% duplicate 0% delay 3ms reorder 0% 0%
#sudo tc qdisc change dev [INTERFACE] root netem loss 10% corrupt 0% duplicate 0% delay 3ms reorder 0% 0%
#sudo tc qdisc change dev [INTERFACE] root netem loss 20% corrupt 0% duplicate 0% delay 3ms reorder 0% 0%
#EXP2:
#
#
#
#EXP3:
#
#
#

if [ -n "$USERNAME" ]; then
	if [ -n "$SSH_KEY" ]; then
		if [ -f "$SSH_KEY" ]; then
			ssh-add $SSH_KEY
            gnome-terminal -x bash -c "ssh -X -t -i $SSH_KEY -p $B_PORT $USERNAME@$REMOTE \"sudo tc qdisc change dev eth2 root netem loss 10% corrupt 0% duplicate 0% delay 3ms reorder 0% 0%; sudo tc qdisc change dev eth3 root netem loss 10% corrupt 0% duplicate 0% delay 3ms reorder 0% 0%\""
            gnome-terminal -x bash -c "ssh -X -t -i $SSH_KEY -p $R1_PORT $USERNAME@$REMOTE \"sudo tc qdisc change dev eth1 root netem loss 10% corrupt 0% duplicate 0% delay 3ms reorder 0% 0%; sudo tc qdisc change dev eth2 root netem loss 10% corrupt 0% duplicate 0% delay 3ms reorder 0% 0%\""
            gnome-terminal -x bash -c "ssh -X -t -i $SSH_KEY -p $R2_PORT $USERNAME@$REMOTE \"sudo tc qdisc change dev eth1 root netem loss 10% corrupt 0% duplicate 0% delay 3ms reorder 0% 0%; sudo tc qdisc change dev eth2 root netem loss 10% corrupt 0% duplicate 0% delay 3ms reorder 0% 0%\""
			gnome-terminal -x bash -c "ssh -X -t -i $SSH_KEY -p $D_PORT $USERNAME@$REMOTE \"sudo tc qdisc change dev eth1 root netem loss 10% corrupt 0% duplicate 0% delay 3ms reorder 0% 0%; sudo tc qdisc change dev eth2 root netem loss 10% corrupt 0% duplicate 0% delay 3ms reorder 0% 0%\""
		else
			echo "SSH Key ($2) does not exist!"
		fi
	else
		echo "Missing Parameter: ${0##*/} $1 <SSH_KEY>"
	fi
else
	echo "Missing Parameter: ${0##*/} <USERNAME> <SSH_KEY>"
fi