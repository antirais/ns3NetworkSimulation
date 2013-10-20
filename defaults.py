#!/usr/bin/env python
# coding: utf-8

class Defaults(object):
	"""
	Default values for cmd options.
	"""
	printConfig					= (False,				"print configuration")
	logLevel					= ("warn",				"set logging level: [trace, debug, info, warn, error]")

	serverStart					= (0,					"time,when UDP echo servers will be online")
	clientStart					= (0,					"time,when UDP echo clients will be online")
	discardPort					= (9,					"UDP echo server discard port")
	packetInterval				= (1.0,					"time between two UDP echo clients packets")
	packetSize					= (1024,				"UDP echo client packet size in bytes")
	stopTime					= (10,					"simulation stop time(seconds)")
	outputFolder				= ("./output/",			"name of the folder to place .pcap files")
	wifiFileName				= ("wifi",				".pcap filename part for WiFi devices")
	csmaFileName				= ("csma",				".pcap filename part for CSMA devices")
	wifiMacType					= ("ns3::AdhocWifiMac",	"global WiFi MAC header type")
	wifiNodesDistance			= (5,					"distance between WiFi nodes")
	connectNthNodeToCloud		= (3,					"specify every n-th node, that will connect to the cloud server")

	networkMask					= ("255.255.255.0",		"common networking mask for all networks in simulation")

	leftOfficeInfraNodes		= (2,					"left office nodes for servers and routers")
	leftOfficeInfraNetwork		= ("192.168.107.0",		"left office infra network")
	leftOfficeServerIp			= ("192.168.107.2",		"left office UDP Echo server ip")
	leftOfficeWifiNodes			= (10,					"number of Wifi nodes in left office")
	leftOfficeWifiNetwork		= ("192.168.106.0",		"left office WiFi network")
	leftOfficeWifiSsid			= ("lo-wifi",			"SSID for the left office WiFi")
	leftOfficeWifiRouter		= (0,					"left office WiFi router node")
	leftOfficeLanNodes			= (10,					"number of LAN nodes in left office")
	leftOfficeLanNetwork		= ("192.168.108.0",		"left office LAN network")
	leftOfficeCsmaDataRate		= ("10Mbps",			"left office's CSMA data rate")
	leftOfficeCsmaDelay			= ("2ms",				"left office's CSMA delay")
	leftOfficeTracePrefix		= ("lo",				".pcap file prefix for left office devices")
	leftOfficeUdpEchoServer		= (1,					"left office UDP Echo Server node")

	cloudNodes					= (5,					"number of nodes in the cloud")
	cloudNetwork				= ("92.168.107.0",		"cloud network address")
	cloudServerIp				= ("92.168.107.3",		"cloud UDP Echo server address")
	cloudTracePrefix			= ("cloud",				".pcap file prefix for cloud devices")
	cloudServerNode 			= (2,					"server node in the cloud")
	cloudCsmaDataRate			= ("100Mbps",			"left office's CSMA data rate")
	cloudCsmaDelay				= ("4ms",				"left office's CSMA delay")

	rightOfficeInfraNodes		= (1,					"right office nodes for servers and routers")
	rightOfficeInfraNetwork		= ("192.168.7.0",		"right office infrastructure network")
	rightOfficeServerIp			= ("192.168.7.1",		"right office UDP Echo server ip")
	rightOfficeWifiNodes		= (10,					"number of Wifi nodes in right office")
	rightOfficeWifiNetwork		= ("192.168.6.0",		"right office WiFi network")
	rightOfficeWifiSsid			= ("ro-wifi",			"SSID for the right office WiFi")
	rightOfficeWifiRouter		= (0,					"right office WiFi router node")
	rightOfficeCsmaDataRate		= ("10Mbps",			"right office's CSMA data rate")
	rightOfficeCsmaDelay		= ("2ms",				"right office's CSMA delay")
	rightOfficeTracePrefix		= ("ro",				".pcap file prefix for right office devices")
	rightOfficeUdpEchoServer	= (0,					"right office UDP Echo Server node")
