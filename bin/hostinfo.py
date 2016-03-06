#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, socket

if os.name != "nt":
	import fcntl
	import struct

	def get_interface(ifname):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s',ifname[:15]))[20:24])

class hostaddr(object):
	def __init__(self):
		self.text = "test"

	def __new__(self):
		ip = socket.gethostbyname(socket.gethostname())
		if ip.startswith("127.") and os.name != "nt":
			interfaces = [
				"vmbr0",
				"eth0",
				"eth1",
				"eth2",
				"wlan0",
				"wlan1",
				"wifi0",
				"ath0",
				"ath1",
				"ppp0",
				]
			for ifname in interfaces:
				try:
					ip = get_interface(ifname)
					break
				except IOError:
					pass
		return ip

class hostn(object):
	def __init__(self):
		self.text = "test"

	def __new__(self):
		hname = os.uname()[1]
		return (hname)
