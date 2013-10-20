#!/usr/bin/env python
# coding: utf-8

import sys

class Colors(object):
	BLACK	 = '\033[90m'
	RED	 	 = '\033[91m'
	GREEN	 = '\033[92m'
	YELLOW	 = '\033[93m'
	BLUE	 = '\033[94m'
	MAGENTA	 = '\033[95m'
	CYAN	 = '\033[96m'
	WHITE	 = '\033[97m'
	RESET	 = '\033[99m'
	END		 = '\033[0m'
	FAIL	 = RED
	WARNING	 = YELLOW

class LogLevel(object):
	TRACE	 = 0
	DEBUG	 = 1
	INFO	 = 2
	WARN	 = 3
	ERROR	 = 4

HEADER_LEN 		= 40
FIELD_LEN 		= 30
HEADER_FORMAT 	= Colors.GREEN+"{0:*^{1}}"+Colors.END
DATA_FORMAT 	= Colors.YELLOW+"{0:<{2}} {1}"+Colors.END
WARNING_FORMAT 	= Colors.RED+"{0:<{2}} {1}"+Colors.END
PLAIN_FORMAT 	= Colors.YELLOW+"{0}"+Colors.END
DEBUG_FORMAT 	= Colors.BLUE+"{0}"+Colors.END
ERROR 			= Colors.RED+"{0}"+Colors.END
LOG_LEVEL 		= LogLevel.WARN

def setLogLevel(level):
	global LOG_LEVEL

	if level == "trace":
		LOG_LEVEL = LogLevel.TRACE
	elif level == "debug":
		LOG_LEVEL = LogLevel.DEBUG
	elif level == "info":
		LOG_LEVEL = LogLevel.INFO
	elif level == "warn":
		LOG_LEVEL = LogLevel.WARN
	elif level == "error":
		LOG_LEVEL = LogLevel.ERROR
	else:
		LOG_LEVEL = LogLevel.WARN

def logHeader(msg):
	print HEADER_FORMAT.format(msg, HEADER_LEN)

def logData(name, value):
	print DATA_FORMAT.format(name, value, FIELD_LEN)

def concatArgs(args):
	string = ""
	for e in args:
		string = string + str(e)
	return string

def log(msg, *args):
	print msg + concatArgs(args)

def logDebug(msg, *args):
	if(LOG_LEVEL > LogLevel.DEBUG):
		return
	print DEBUG_FORMAT.format(msg + concatArgs(args))

def logWarn(name, value):
	if(LOG_LEVEL > LogLevel.WARN):
		return
	print WARNING_FORMAT.format(name, value, FIELD_LEN)

def logError(msg):
	print ERROR.format(str(msg))
	sys.exit(0)
