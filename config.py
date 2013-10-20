#!/usr/bin/env python
# coding: utf-8

from defaults import *
from helpers import *

def validateConfig(cmd):
	if(cmd.cloudServerNode < 2):
		logError("Cloud server node cannot be less than 2, because 0 is left office router and 1 is right office router")

def setConfig(argv, cmd):
	defaults = Defaults()
	# For convenience, we add the local variables to the command line argument
	# system so that they can be overridden with flags such as
	# "--AnswerToTheUltimateQuestionOfLifeTheUniverseAndEverything=42"
	for field in dir(defaults):
		if field.startswith("__"):
			continue
		fieldValue = defaults.__getattribute__(field)[0]
		fieldDesc = defaults.__getattribute__(field)[1]
		cmd.__setattr__(field, fieldValue)
		cmd.AddValue(field, fieldDesc)

	cmd.Parse(argv)

	if(cmd.printConfig):
		printConfig(cmd, defaults)

	setLogLevel(cmd.logLevel)
	validateConfig(cmd)
	return cmd

def printConfig(cmd, defaults):
	logHeader("Config");
	for field in dir(defaults):
		if field.startswith("__"):
			continue
		logData(field, cmd.__getattribute__(field))
