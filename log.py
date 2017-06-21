import sys


DEBUG = False

def error(msg):
 	sys.stderr.write(msg)

def debug(msg):
	if DEBUG:
		print msg