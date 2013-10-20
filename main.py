#!/usr/bin/env python
# coding: utf-8

from ns.visualizer import *

from rightOffice import *
from leftOffice import *
from cloud import *
from config import *

def runSimulation(stopTime):
	logHeader("Executing")
	log("Starting simulation")
	Simulator.Stop(Seconds(int(stopTime)))
	Simulator.Run()
	Simulator.Destroy()
	log("Simulation finished")

def setUpGlobalRouting():
	Ipv4GlobalRoutingHelper.PopulateRoutingTables()

def main(argv):
	cmd = CommandLine()
	setConfig(argv, cmd)

	roRouter = setUpRightOffice(cmd)
	loRouter = setUpLeftOffice(cmd)
	setUpCloud(loRouter, roRouter, cmd)
	setUpGlobalRouting()

	logDebug("Nodes created in total: ", NodeList.GetNNodes())
	runSimulation(cmd.stopTime)

if __name__ == '__main__':
	import sys
	main(sys.argv)
