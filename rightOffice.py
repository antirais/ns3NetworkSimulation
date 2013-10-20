#!/usr/bin/env python
# coding: utf-8

from helpers import *

def setUpRightOffice(cmd):
	logHeader("Constructing right office")
	roHosts = createRightOfficeWifiNodes(cmd)
	roWifiPhy = setUpWifiPhy()
	roWifiMac = setUpWifiMac(cmd.wifiMacType, Ssid(cmd.rightOfficeWifiSsid))
	roWifiDev = setUpWifi(roWifiPhy, roWifiMac, roHosts)
	setUpWifiHostsMobility(roHosts, cmd.wifiNodesDistance)

	roWifiInterfaces = setUpIPAddresses(cmd.rightOfficeWifiNetwork, cmd.networkMask, roWifiDev)

	roInfra = createRightOfficeInfraNodes(cmd)
	logNodes("Right office infra node count: ", roInfra)
	roInfraWithWifiAP = addToContainer(roInfra, roHosts.Get(cmd.rightOfficeWifiRouter))
	roInfraDev = installCSMA(cmd.rightOfficeCsmaDataRate, cmd.rightOfficeCsmaDelay, roInfraWithWifiAP)

	roInfraInterfaces = setUpIPAddresses(cmd.rightOfficeInfraNetwork, cmd.networkMask, roInfraDev)

	rightOfficeGw = setUpRoApplications(roWifiInterfaces, roInfraInterfaces, roHosts, roInfra, cmd)
	doRightOfficeTracing(roWifiPhy, roHosts, roInfra, cmd)

	return rightOfficeGw

def setUpRoApplications(roWifiInterfaces, roInfraInterfaces, roHosts, roInfra, cmd):
	roServerNode = roHosts.Get(cmd.rightOfficeUdpEchoServer)
	roRouterNode = roInfra.Get(cmd.rightOfficeWifiRouter)

	installUdpEchoServer(roRouterNode, cmd.discardPort, cmd.serverStart, cmd.stopTime)

	roServerAddress = roInfraInterfaces.GetAddress(cmd.rightOfficeUdpEchoServer)
	roServerClient = setUpUdpEchoClient(roServerAddress, cmd.discardPort, cmd.packetInterval, cmd.packetSize)

	log("Right office server node #", roServerNode.GetId())
	logDebug("Right office server node address: ", roServerAddress)
	log("Right office router node #", roRouterNode.GetId())

	cloudClient = setUpCloudUdpEchoClient(cmd)
	installUdpEchoWifiClients(cloudClient, roServerClient, roHosts, [cmd.rightOfficeWifiRouter], cmd)
	return roRouterNode

def doRightOfficeTracing(wifiPhy, wifiNodes, csmaNodes, cmd):
	doWifiTracing(cmd.rightOfficeTracePrefix, wifiPhy, wifiNodes, cmd)
	doCSMATracing(cmd.rightOfficeTracePrefix, csmaNodes, cmd)

def createRightOfficeWifiNodes(cmd):
	log("Creating ", cmd.rightOfficeWifiNodes, " right office wifi nodes")
	return createNodesWithStack(cmd.rightOfficeWifiNodes)

def createRightOfficeInfraNodes(cmd):
	log("Creating ", cmd.rightOfficeInfraNodes, " right office infra nodes")
	return createNodesWithStack(cmd.rightOfficeInfraNodes)
