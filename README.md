NS3 network simulation in Python
================================

Overview
========

This is a network simulation with NS3. There are three main segments: left office, right office and internet.
Right office has one local server, one Wifi router and multiple wifi hosts.
Left office has in addition to right office a multiple LAN hosts connected to local Wifi router.
Both Wifi routers are connected to internet nodes.
About 70% of office's traffic goes to local server and other 30% goes to internet.
Some additional traffic comes from internet to local office's server.

Setup
=====

1) install dependencies
* pygccxml

To use --visualize, install the following
* python-gnuplot
* python-dev
* python-pygraphviz
* python-kiwi
* python-pygoocanvas
* python-gnome2
* python-gnomedesktop
* python-rsvg

2) configure waf

	./waf configure

3) screate folders in ns3 install folder ( or links :) )

	* ~/ns-allinone-3.18/ns-3.18/scratch
	* ~/ns-allinone-3.18/ns-3.18/output

4) copy all files under scratch

5) start waf shell

Execute these commands in ns3 folder, so that the current path is correct.
Starts the waf shell and then python will execute correcty.

	~/ns-allinone-3.18/ns-3.18/ $ ./waf shell
	~/ns-allinone-3.18/ns-3.18/ $ python scratch/main.py

	Make sure you don't have a subdirectory in scratch, or the build will fail.

Actions
-------

To print help:

	~/ns-allinone-3.18/ns-3.18/ $ python scratch/main.py --PrintHelp

To view .pcap files:

	~/ns-allinone-3.18/ns-3.18/ $ tcpdump -n -tt -r output/node-28-0.pcap

	 * -n	Don't convert addresses (i.e., host addresses, port numbers, etc.) to names.
	 * -tt	Print an unformatted timestamp on each dump line.
	 * -r	file

	 node-28-0 represents a node number 28 and net device 0 there.

To run with config:

	~/ns-allinone-3.18/ns-3.18/ $ python scratch/main.py --stopTime=34 --backboneNodes=6
	~/ns-allinone-3.18/ns-3.18/ $ rm output/*.pcap; python scratch/main.py && echo && ls -1 output | sort -V

To run visualizer, exit waf shell and run:

	~/ns-allinone-3.18/ns-3.18/ $ ./waf --pyrun scratch/main.py --vis
