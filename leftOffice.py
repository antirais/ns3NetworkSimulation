#!/usr/bin/env python
# coding: utf-8

from helpers import *

def setUpLeftOffice(cmd):
	logHeader("Constructing left office")
	loHosts = createLeftOfficeWifiNodes(cmd)
	loWifiPhy = setUpWifiPhy()
	loWifiMac = setUpWifiMac(cmd.wifiMacType, Ssid(cmd.leftOfficeWifiSsid))
	loWifiDev = setUpWifi(loWifiPhy, loWifiMac, loHosts)
	setUpWifiHostsMobility(loHosts, cmd.wifiNodesDistance)

	loWifiInterfaces = setUpIPAddresses(cmd.leftOfficeWifiNetwork, cmd.networkMask, loWifiDev)

	loInfra = createLeftOfficeInfraNodes(cmd)
	logNodes("Left office infra node count: ", loInfra)
	loInfraWithWifiAP = addToContainer(loInfra, loHosts.Get(cmd.leftOfficeWifiRouter))
	loInfraDev = installCSMA(cmd.leftOfficeCsmaDataRate, cmd.leftOfficeCsmaDelay, loInfraWithWifiAP)

	loLANs = createLeftOfficeLanNodes(cmd)
	logNodes("Left office lan node count: ", loLANs)
	loLANWithGW = addToContainer(loLANs, loHosts.Get(cmd.leftOfficeWifiRouter))
	loLanDev = installCSMA(cmd.leftOfficeCsmaDataRate, cmd.leftOfficeCsmaDelay, loLANWithGW)

	loInfraInterfaces = setUpIPAddresses(cmd.leftOfficeInfraNetwork, cmd.networkMask, loInfraDev)
	loLanInterfaces = setUpIPAddresses(cmd.leftOfficeLanNetwork, cmd.networkMask, loLanDev)

	leftOfficeGw = setUpLoApplications(
	                                   loWifiInterfaces,
	                                   loInfraInterfaces,
	                                   loLanInterfaces,
	                                   loHosts,
	                                   loInfra,
	                                   loLANs,
	                                   cmd
	                                  )

	doLeftOfficeTracing(loWifiPhy, loHosts, addToContainer(loInfra, loLANs), cmd)

	return leftOfficeGw

def setUpLoApplications(loWifiInterfaces, loInfraInterfaces, loLanInterfaces, loHosts, loInfra, loLANs, cmd):
	loServerNode = loHosts.Get(cmd.leftOfficeUdpEchoServer)
	loRouterNode = loInfra.Get(cmd.leftOfficeWifiRouter)

	installUdpEchoServer(loRouterNode, cmd.discardPort, cmd.serverStart, cmd.stopTime)

	loServerAddress = loInfraInterfaces.GetAddress(cmd.leftOfficeUdpEchoServer)
	loServerClient = setUpUdpEchoClient(loServerAddress, cmd.discardPort, cmd.packetInterval, cmd.packetSize)

	log("Left office server node #", loServerNode.GetId())
	logDebug("Left office server node address: ", loServerAddress)
	log("Left office router node #", loRouterNode.GetId())

	cloudClient = setUpCloudUdpEchoClient(cmd)

	logDebug("Number of left office WiFi clients: ", loHosts.GetN())
	installUdpEchoWifiClients(cloudClient, loServerClient, loHosts, [cmd.leftOfficeWifiRouter], cmd)

	logDebug("Number of left office LAN clients: ", loLANs.GetN())
	installUdpEchoLanClients(cloudClient, loServerClient, loLANs, [cmd.leftOfficeWifiRouter], cmd)
	return loRouterNode

def doLeftOfficeTracing(wifiPhy, wifiNodes, csmaNodes, cmd):
	doWifiTracing(cmd.leftOfficeTracePrefix, wifiPhy, wifiNodes, cmd)
	doCSMATracing(cmd.leftOfficeTracePrefix, csmaNodes, cmd)

def createLeftOfficeWifiNodes(cmd):
	log("Creating ", cmd.leftOfficeWifiNodes, " left office wifi nodes")
	return createNodesWithStack(cmd.leftOfficeWifiNodes)

def createLeftOfficeInfraNodes(cmd):
	log("Creating ", cmd.leftOfficeInfraNodes, " left office infra nodes")
	return createNodesWithStack(cmd.leftOfficeInfraNodes)

def createLeftOfficeLanNodes(cmd):
	log("Creating ", cmd.leftOfficeLanNodes, " left office lan nodes")
	return createNodesWithStack(cmd.leftOfficeLanNodes)
