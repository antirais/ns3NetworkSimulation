#!/bin/bash

#find $out_dir/*.pcap -type f 
ro_IP="192.168.7.1.9"
lo_IP="192.168.107.2"
out_dir="./output"
tcpdump=`which tcpdump`
ro_server=`find ./output/ro-csma* -type f | sed -n 1p`
#ro_router="ro-csma-10-1.pcap"
lo_server=`find ./output/lo-csma* -type f | sed -n 2p`
#lo_router="lo-csma-22-1.pcap"
ns3_args=$1

find_server=``

rm -f $out_dir/*.pcap
python scratch/main.py $ns3_args

echo "right office server responses:"
$tcpdump -n -tt -r $ro_server | grep "$ro_IP >" | wc -l
echo "left office server responses:"
$tcpdump -n -tt -r $lo_server | grep "$lo_IP >" | wc -l
#tcpdump -n -tt -r output/lo-csma-21-1.pcap | grep "192.168.107.2 >" | wc -l
