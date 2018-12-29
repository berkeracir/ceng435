# HOW TO RUN (in order)
It would be **better** to read each script's text below before starting.

On local:
1. `./configure_delays.sh <GENI-Username> <Path-To-GENI-SSHKEY>`
2. `./configure_routing_tables.sh <GENI-Username> <Path-To-GENI-SSHKEY>`
3. `./update_nodes.sh <GENI-Username> <Path-To-GENI-SSHKEY>`
On Destination Node:
4. `python destination.py <Output-File-Name>`
On Broker Node:
5. `python broker.py <Output-File-Name>`
On Source Node:
6. `python source.py <Input-File-Name> >> <Experiment-Output-File-Name>`
On local:
7. `./get_experiment_results.sh <GENI-Username> <Path-To-GENI-SSHKEY>`

# configure_delays.sh
This script is used to configure network delays on remote hosts. Emulated
delays must be changed by hand before emulating on the hosts.

`chmod +x configure_delays.sh`
`./configure_delays.sh <GENI-Username> <Path-To-GENI-SSHKEY>`

# configure_routing_tables.sh
This script is used to configure routing tables on remote hosts. It enables the
scripts to send their messages directly to related addresses as routers will be
configured correctly.

`chmod +x configure_routing_tables.sh`
`./configure_routing_tables.sh <GENI-Username> <Path-To-GENI-SSHKEY>`

# get_experiment_results.sh
This script is used to retrieve experiment results from Source node.

`chmod +x get_experiment_results.sh`
`./get_experiment_results.sh <GENI-Username> <Path-To-GENI-SSHKEY>`

# update_nodes.sh
This script is used to upload our scripts from local to remote hosts.

`chmod +x update_nodes.sh`
`./update_nodes.sh <GENI-Username> <Path-To-GENI-SSHKEY>`

# destination.py
Script that runs on Destination. **Note that** it closes itself after 60 seconds
of idling, so be careful while running this script. `dest_timeout` variable can
be assigned to any bigger number. It writes the received messages from Broker
over UDP (RDT) connection into `<Output-File-Name>`.

`python destination.py <Output-File-Name>`

# broker.py
Script that runs on Broker. It must be running before the `source.py`. It
writes the received messages from Source over TCP connection into 
 `<Output-File-Name>`.

`python broker.py <Output-File-Name>`

# source.py
Script that runs on Source. It won't run properly if `broker.py` is not running
at that time. It reads from `<Output-File-Name>` and sends the data over TCP
channel to Broker.

`python broker.py <Output-File-Name>`

# local directory
It contains our implementations before we deploy the scripts to remote hosts.

# experiments directory
It contains experiment results, those files are gathered from the Source node.