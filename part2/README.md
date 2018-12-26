# update_nodes.sh
This script is used to upload our scripts from local to remote hosts.

`chmod +x update_nodes.sh`
`./update_nodes.sh <GENI-Username> <Path-To-GENI-SSHKEY>`

# remote_run_nodes.sh
This script is used to run the uploaded scripts on remote hosts. It opens new
gnome terminals separately. You are free on the remote host terminals after the
execution of scripts.

`chmod +x update_nodes.sh`
`./update_nodes.sh <GENI-Username> <Path-To-GENI-SSHKEY>`

# destination.py
Script that runs on Destination. **Note that** it closes itself after 10 seconds
of idling, so be careful while running this script. `dest_timeout` variable can
be assigned to any bigger number. It writes the received messages from Broker
over UDP (RDT) connection into `<Output-File-Name>`.

`python destination.py <Output-File-Name>`

# broker.py
Script that runs on Broker. It must be running before the `source.py`. It
writes the received messages from Source over TCP connection into 
 `<Output-File-Name>`.

`python broker.py <Output-File-Name>`

# destination.py
Script that runs on Source. It won't run properly if `broker.py` is not running
at that time. It reads from `<Output-File-Name>` and sends the data over TCP
channel to Broker.

`python broker.py <Output-File-Name>`

# RUN ORDER:
1. `python destination.py <Output-File-Name>`
2. `python broker.py <Output-File-Name>`
3. `python broker.py <Output-File-Name>`