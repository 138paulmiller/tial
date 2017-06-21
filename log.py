import sys


DEBUG = False

def error(msg):
 	sys.stderr.write('\n'+msg)

def debug(msg):
	if DEBUG:
		print msg