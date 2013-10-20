Setup:
* install dependencies
	sudo apt-get install pygccxml

	To use --visualize, install the following
	sudo apt-get install python-gnuplot
	sudo apt-get install python-dev
	sudo apt-get install python-pygraphviz
	sudo apt-get install python-kiwi
	sudo apt-get install python-pygoocanvas
	sudo apt-get install python-gnome2
	sudo apt-get install python-gnomedesktop
	sudo apt-get install python-rsvg

	./waf configure

* screate folders in ns3 install folder ( or links :) )
	* ~/ns-allinone-3.18/ns-3.18/scratch
	* ~/ns-allinone-3.18/ns-3.18/output

	copy all files under scratch

To run:
	Execute these commands in ns3 folder, so that the current path is correct.
	Starts the waf shell and then python will execute correcty. Once is enough!

	~/ns-allinone-3.18/ns-3.18/ $ ./waf shell
	~/ns-allinone-3.18/ns-3.18/ $ python scratch/main.py

	Make sure you don't have a subdirectory in scratch, or the build will fail.

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
