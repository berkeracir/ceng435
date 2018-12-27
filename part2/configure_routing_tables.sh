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
            #gnome-terminal -x bash -c "ssh -X -t -i $SSH_KEY -p $S_PORT $USERNAME@$REMOTE \"sudo ip route add 10.0.0.0\8 via 10.10.1.1 dev eth1\""
            gnome-terminal -x bash -c "ssh -X -t -i $SSH_KEY -p $B_PORT $USERNAME@$REMOTE \"sudo route add -net 10.10.3.0 netmask 255.255.255.0 gw 10.10.2.2 dev eth2; sudo route add -net 10.10.5.0 netmask 255.255.255.0 gw 10.10.4.2 dev eth3\""
            #gnome-terminal -x bash -c "ssh -X -t -i $SSH_KEY -p $R1_PORT $USERNAME@$REMOTE \"sudo ip route add 10.10.2.0\24 via 10.10.2.2 dev eth1; sudo ip route add 10.10.3.0\24 via 10.10.3.1 dev eth2\""
            #gnome-terminal -x bash -c "ssh -X -t -i $SSH_KEY -p $R2_PORT $USERNAME@$REMOTE \"sudo ip route add 10.10.4.0\24 via 10.10.4.2 dev eth1; sudo ip route add 10.10.5.0\24 via 10.10.5.1 dev eth2\""
            gnome-terminal -x bash -c "ssh -X -t -i $SSH_KEY -p $D_PORT $USERNAME@$REMOTE \"sudo route add -net 10.10.2.0 netmask 255.255.255.0 gw 10.10.3.1 dev eth1; sudo route add -net 10.10.4.0 netmask 255.255.255.0 gw 10.10.5.1 dev eth2\""
			#sudo route add -net  netmask 255.255.255.0 dev eth; 
		else
			echo "SSH Key ($2) does not exist!"
		fi
	else
		echo "Missing Parameter: ${0##*/} $1 <SSH_KEY>"
	fi
else
	echo "Missing Parameter: ${0##*/} <USERNAME> <SSH_KEY>"
fi