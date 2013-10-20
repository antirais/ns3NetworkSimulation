#!/usr/bin/env python
# coding: utf-8

from ns.core import *
from ns.internet import *
from ns.mobility import *
from ns.network import *
from ns.wifi import *
from ns.csma import *
from ns.applications import *

from common import *

def connectToCloudServer(host, cmd):
	"""
	Calculates if host needs to connect to cloud server instead of local office's server
	Every N-th host should connect to the cluod
	"""
	return host % cmd.connectNthNodeToCloud == 0

def installUdpEchoWifiClients(cloudClient, localServerClient, localHosts, skipList, cmd):
	udpEchoClientInstaller("Wifi", cloudClient, localServerClient, localHosts, skipList, cmd)

def installUdpEchoLanClients(cloudClient, localServerClient, localLANs, skipList, cmd):
	udpEchoClientInstaller("LAN", cloudClient, localServerClient, localLANs, skipList, cmd)

def udpEchoClientInstaller(hostType, cloudClient, localServerClient, localNodes, skipList, cmd):
	for host in range(localNodes.GetN()):
		node = localNodes.Get(host)
		if host in skipList:
			logDebug("Installing UdpEchoClient to "+hostType+" host: skipping node #", node.GetId())
			continue
		if connectToCloudServer(host, cmd):
			logDebug("Installing cloud server UdpEchoClient to "+hostType+" host: node #", node.GetId())
			installUdpEchoClient(cloudClient, node, cmd.clientStart, cmd.stopTime)
		else:
			logDebug("Installing local server UdpEchoClient to "+hostType+" host: node #", node.GetId())
			installUdpEchoClient(localServerClient, node, cmd.clientStart, cmd.stopTime)


def setUpWifi(wifiPhy, wifiMac, nodes):
	wifiHelper = WifiHelper()
	wifiHelper.SetRemoteStationManager(
	                                   "ns3::ConstantRateWifiManager",
	                                   "DataMode", StringValue("OfdmRate54Mbps")
									  )
	return wifiHelper.Install(wifiPhy, wifiMac, nodes)

def setUpWifiPhy():
	wifiChannel = YansWifiChannelHelper.Default()
	wifiPhy = YansWifiPhyHelper.Default()
	wifiPhy.SetChannel(wifiChannel.Create())
	return wifiPhy

def setUpWifiMac(wifiType, ssid):
	wifiMac = NqosWifiMacHelper.Default()
	wifiMac.SetType(str(wifiType), "Ssid", SsidValue(ssid))
	return wifiMac

def createNodes(count):
	nodeContainer = NodeContainer()
	nodeContainer.Create(int(count))
	return nodeContainer

def createNodesWithStack(count):
	nodes = createNodes(count)
	installInternetStack(nodes)
	return nodes

def setUpIPAddresses(baseAddress, mask, devices):
	ipAddrs = Ipv4AddressHelper()
	ipAddrs.SetBase(Ipv4Address(baseAddress), Ipv4Mask(mask))
	return ipAddrs.Assign(devices)

def installInternetStack(nodes):
	internet = InternetStackHelper()
	internet.Install(nodes)

def setUpUdpEchoClient(address, port, interval, packetSize):
	client = UdpEchoClientHelper(address, port)
	client.SetAttribute("Interval", TimeValue(Seconds(interval)))
	client.SetAttribute("PacketSize", UintegerValue(packetSize))
	return client

def installUdpEchoClient(echoServer, host, start, end):
	clientApps = echoServer.Install(host)
	clientApps.Start(Seconds(start))
	clientApps.Stop(Seconds(end))

def installUdpEchoServer(node, port, start, end):
	server = UdpEchoServerHelper(port)
	serverApps = server.Install(node)
	serverApps.Start(Seconds(start))
	serverApps.Stop(Seconds(end))

def installCSMA(dataRate, delay, node):
	csma = CsmaHelper()
	csma.SetChannelAttribute("DataRate", StringValue(dataRate))
	csma.SetChannelAttribute("Delay", StringValue(delay))
	return csma.Install(node)

def addToContainer(collector, *nodes):
	allNodes = NodeContainer()
	allNodes.Add(collector)

	for node in nodes:
		allNodes.Add(node)

	return allNodes

def setUpWifiHostsMobility(nodes, wifiDistance):
	log("Installing static mobility; distance " + str(wifiDistance))
	mobility = MobilityHelper()
	mobility.SetPositionAllocator(
	                            	"ns3::GridPositionAllocator",
									"MinX", 		DoubleValue (0.0),
									"MinY", 		DoubleValue (0.0),
									"DeltaX",		DoubleValue (wifiDistance),
									"DeltaY", 		DoubleValue (wifiDistance*2),
									"LayoutType", 	StringValue ("RowFirst")
								 )
	mobility.SetMobilityModel("ns3::ConstantPositionMobilityModel")
	mobility.Install(nodes)
	return mobility

def doWifiTracing(infix, wifiPhy, wifiNodes, cmd):
	wifiLogPrefix = cmd.outputFolder+infix+"-"+cmd.wifiFileName
	wifiPhy.EnablePcap(wifiLogPrefix, wifiNodes)

def doCSMATracing(infix, csmaNodes, cmd):
	csmaLogPrefix = cmd.outputFolder+infix+"-"+cmd.csmaFileName
	CsmaHelper().EnablePcap(csmaLogPrefix, csmaNodes)

def logNodes(msg, cloudNodes):
	logDebug(msg, cloudNodes.GetN())
	for node in range(cloudNodes.GetN()):
		logDebug(" - Node id: ", cloudNodes.Get(node).GetId())

def logAssignIPs(nodes, nodeInterfaces):
	logDebug("Assigning IP addresses to nodes")
	for interface in range(nodeInterfaces.GetN()):
		logDebug(" - #", nodes.Get(interface).GetId(), "\t",
			nodeInterfaces.GetAddress(interface))

def setUpCloudUdpEchoClient(cmd):
	cloudServerAddress = Ipv4Address(cmd.cloudServerIp)
	return setUpUdpEchoClient(cloudServerAddress, cmd.discardPort, cmd.packetInterval, cmd.packetSize)

def setUpOfficeServerClient(serverIp, cmd):
	serverAddress = Ipv4Address(serverIp)
	return setUpUdpEchoClient(serverAddress, cmd.discardPort, cmd.packetInterval, cmd.packetSize)
