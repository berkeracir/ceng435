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

ssh -i ~/.ssh/id_geni_ssh_rsa $USERNAME@$S -p $S_PORT "echo 'source.py:'; cat source.py; exit;"
ssh -i ~/.ssh/id_geni_ssh_rsa $USERNAME@$B -p $B_PORT "echo 'broker.py:'; cat broker.py; exit;"
ssh -i ~/.ssh/id_geni_ssh_rsa $USERNAME@$R1 -p $R1_PORT "echo '1 router.py:'; cat router.py; exit;"
ssh -i ~/.ssh/id_geni_ssh_rsa $USERNAME@$R2 -p $R2_PORT "echo '2 router.py:'; cat router.py; exit;"
ssh -i ~/.ssh/id_geni_ssh_rsa $USERNAME@$D -p $D_PORT "echo 'destionation.py:'; cat destionation.py; exit;"
sftp -vvv -P $S_PORT $USERNAME@$S <<< $'put source.py'
sftp -P $B_PORT $USERNAME@$B <<< $'put broker.py'
sftp -P $R1_PORT $USERNAME@$R1 <<< $'put router.py'
sftp -P $R2_PORT $USERNAME@$R2 <<< $'put router.py'
sftp -P $D_PORT $USERNAME@$D <<< $'put destionation.py'
