#!/bin/bash

#find $out_dir/*.pcap -type f
ro_IP="192.168.7.1.9"
lo_IP="192.168.107.2"
out_dir="./output"
tcpdump=`which tcpdump`

find_server=``

rm -f $out_dir/*.pcap
python scratch/main.py --cloudNodes=$1
ro_server=`find ./output/ro-csma* -type f | sort -V | sed -n 1p`
ro_wifi_gw=`find ./output/ro-wifi* -type f | sort -V | sed -n 1p`

lo_server=`find ./output/lo-csma* -type f | sort -V | sed -n 2p`
lo_lan_gw=`find ./output/lo-csma* -type f | sort -V | sed -n 1p`
lo_wifi_gw=`find ./output/lo-wifi* -type f | sort -V | sed -n 1p`

echo "right office server responses:"
$tcpdump -n -tt -r $ro_server | grep "$ro_IP >" | wc -l
echo "right office wifi gateway traffic:"
$tcpdump -n -tt -r $ro_wifi_gw | grep "$ro_IP >" | wc -l

echo "left office server responses:"
$tcpdump -n -tt -r $lo_server | grep "$lo_IP >" | wc -l
echo "left office LAN gateway traffic:"
$tcpdump -n -tt -r $lo_lan_gw | grep "$lo_IP >" | wc -l
echo "left office wifi gateway traffic:"
$tcpdump -n -tt -r $lo_wifi_gw | grep "$lo_IP >" | wc -l
