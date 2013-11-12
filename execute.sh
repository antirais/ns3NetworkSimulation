#!/bin/bash

#############################################################
# Simple script to run the NS3 simulation and gather data
#############################################################

RSV=$(($1*2))
LLN=$1
LWN=$1
LGW=$(($RSV+1))
LSV=$(($RSV+$LWN+1))

rm output/*.pcap; python scratch/main.py \
--leftOfficeLanNodes=$LLN \
--leftOfficeWifiNodes=$LWN \
--rightOfficeWifiNodes=$RSV \
--logLevel=disabled

RGW1=$(tcpdump -tt -n -r output/ro-wifi-0-1.pcap | wc -l)
RGW2=$(tcpdump -tt -n -r output/cloud-csma-0-2.pcap | wc -l)
RGW3=$(tcpdump -tt -n -r output/cloud-csma-0-3.pcap | wc -l)
RSRV=$(tcpdump -tt -n -r output/ro-csma-$RSV-1.pcap | wc -l)

LGW1=$(tcpdump -tt -n -r output/lo-wifi-$LGW-1.pcap | wc -l)
LGW2=$(tcpdump -tt -n -r output/cloud-csma-$LGW-2.pcap | wc -l)
LGW3=$(tcpdump -tt -n -r output/cloud-csma-$LGW-3.pcap | wc -l)
LGW4=$(tcpdump -tt -n -r output/cloud-csma-$LGW-4.pcap | wc -l)
LSRV=$(tcpdump -tt -n -r output/lo-csma-$LSV-1.pcap | wc -l)

echo
echo "Ro-server: " $RSRV
echo "Ro-gatewy: " $(($RGW1+$RGW2+$RGW3))
echo "Lo-server: " $LSRV
echo "Lo-gatewy: " $(($LGW1+$LGW2+$LGW3+$LGW4))
