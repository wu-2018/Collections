#!/bin/bash	
i=1
sleep 20
while (( $i<=100 ))
do
if ping -q -c 1 -W 1 xxx.xx.xx.xxx > /home/wqk/script/null; then
  echo "IPv4 is up"
  echo "starting frpc"
  /home/wqk/tool/frpc -c /home/wqk/Seafile/frpc.ini 
  break
else
  echo "IPv4 is down"
fi
sleep 2
done
