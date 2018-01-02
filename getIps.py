#!/usr/bin/python3

import os
import socket

class Backends(object):
	ips = []
	dir_path = os.path.dirname(os.path.abspath(__file__))
	newfile = os.path.join(dir_path,"dynamic_backends.new")
	tplfile = os.path.join(dir_path,"dynamic_backends.tpl")
	vclfile = os.path.join(dir_path,"dynamic_backends.vcl")

	def __init__(self):
		addrs = socket.getaddrinfo("localhost",80, proto=socket.IPPROTO_TCP)
		for addr in addrs:
			ip = addr[4]
			self.ips.append(ip[0])

	def _setips(self):
		ips = self.ips
		ips.sort()
		return ips

	def _setnewConFile(self):
		with open(self.tplfile) as f:
			data = f.read()
		f.closed
		ips = self._setips()
		data = data.replace("IP1",ips[0])
		data = data.replace("IP2",ips[1])
		return data

	def compareConf(self):
		with open(self.vclfile) as f:
			vcl_data = f.read()
		f.closed
		tmpl_data = self._setnewConFile()
		fo = open(self.newfile,"w")
		fo.write(tmpl_data)
		fo.closed
		if vcl_data == tmpl_data:
			return False
		else:
			return True

	def renewConf(self):
		os.rename(self.newfile, self.vclfile)
		os.system("systemctl status varnish")

if __name__ == '__main__':
	backend = Backends()
	if (backend.compareConf()):
		print("Are direferent")
		backend.renewConf()
	else:
		print("Are iqual")
