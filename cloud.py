#!/usr/bin/env python
# coding: utf-8

from helpers import *

def setUpCloud(loRouter, roRouter, cmd):
	logHeader("Constructing cloud")

	cloudNodes = createCloudNodes(cmd)

	logNodes("Cloud node count: ", cloudNodes)
	logDebug("Left office router: #", loRouter.GetId())
	logDebug("Right office router: #", roRouter.GetId())

	# Do not change the order of nodes. It is needed to skip first to nodes,
	# when cloud applications are installed
	cloudNodeWithOfficeGw = addToContainer(roRouter, loRouter, cloudNodes)
	cloudNodesDev = installCSMA(cmd.cloudCsmaDataRate, cmd.cloudCsmaDelay, cloudNodeWithOfficeGw)
	cloudNodesInterfaces = setUpIPAddresses(cmd.cloudNetwork, cmd.networkMask, cloudNodesDev)
	logAssignIPs(cloudNodeWithOfficeGw, cloudNodesInterfaces)

	setUpCloudApplications(cloudNodesInterfaces, cloudNodeWithOfficeGw, cmd)
	doCloudTracing(cloudNodeWithOfficeGw, cmd)

def setUpCloudApplications(cloudNodesInterfaces, cloudNodes, cmd):
	cloudServerNode = cloudNodes.Get(cmd.cloudServerNode)
	installUdpEchoServer(cloudServerNode, cmd.discardPort, cmd.serverStart, cmd.stopTime)

	log("Cloud server node #", cloudServerNode.GetId())
	logDebug("Cloud server node address: ", cloudNodesInterfaces.GetAddress(cmd.cloudServerNode))
	assertTrue(cloudNodesInterfaces.GetAddress(cmd.cloudServerNode), cmd.cloudServerIp)

	roServerClient = setUpOfficeServerClient(cmd.rightOfficeServerIp, cmd)
	loServerClient = setUpOfficeServerClient(cmd.leftOfficeServerIp, cmd)
	installUdpEchoClients(cloudNodes, loServerClient, roServerClient, cmd)

def installUdpEchoClients(cloudNodes, loServerClient, roServerClient, cmd):
	LO_ROUTER_POS = 0
	RO_ROUTER_POS = 1

	logDebug("Number of Cloud lan clients: ", cloudNodes.GetN())
	for host in range(cloudNodes.GetN()):
		node = cloudNodes.Get(host)
		if host in [LO_ROUTER_POS, RO_ROUTER_POS, cmd.cloudServerNode]:
			logDebug("Installing UdpEchoClient to cloud host: skipping node #", node.GetId())
			continue
		if connectToLeftOfficeServer(host):
			logDebug("Installing left office server UdpEchoClient to cloud host: node #", node.GetId())
			installUdpEchoClient(loServerClient, node, cmd.clientStart, cmd.stopTime)
		else:
			logDebug("Installing right office server UdpEchoClient to cloud host: node #", node.GetId())
			installUdpEchoClient(roServerClient, node, cmd.clientStart, cmd.stopTime)

def doCloudTracing(csmaNodes, cmd):
	doCSMATracing(cmd.cloudTracePrefix, csmaNodes, cmd)

def createCloudNodes(cmd):
	log("Creating ", cmd.cloudNodes, " cloud infra nodes")
	return createNodesWithStack(cmd.cloudNodes)

def connectToLeftOfficeServer(host):
	OFFICES_COUNT = 2
	return host % OFFICES_COUNT == 0
