#!/usr/bin/env python
# encoding: utf-8
"""
Prime.py

Created by Richard West on 2009-06-09.
Copyright (c) 2009 MIT. All rights reserved.
"""

import sys
import os
import unittest
import re
import xml, xml.dom.minidom
import cPickle as pickle # try import pickle if that doesn't work

class PrimeSpeciesList:
	def __init__(self,mirror="warehouse.primekinetics.org",cache="cache"):
		self.mirrorLocation=mirror
		self.cacheLocation=cache
		self.cas2primeids=dict()
		self.primeid2cas=dict()
		
		self.cacheItems=['cas2primeids','primeid2cas']
		try: 
			self.loadCache()
		except:
			print "couldn't load cache."
			self.readCAS()
			self.saveCache()
		
	def loadCache(self):
		for item in self.cacheItems:
			self.loadItem(item)
	def saveCache(self):
		for item in self.cacheItems:
			self.saveItem(item)
	def saveItem(self,itemName):
		obj=getattr(self,itemName)
		filePath=os.path.join(self.cacheLocation,itemName+'.pkl')
		pickle.dump(obj, file(filePath, 'wb'))
	def loadItem(self,itemName):
		filePath=os.path.join(self.cacheLocation,itemName+'.pkl')
		setattr(self,itemName,pickle.load(file(filePath, 'rb')))
		
	def readCAS(self):
		path=os.path.join(self.mirrorLocation,'depository','species','catalog')
		listOfFiles=os.listdir(path)
		reCas=re.compile('CASRegistryNumber">([0-9/-]+)</name>')
		for filename in listOfFiles:
			filePath=os.path.join(path,filename)
			if not os.path.isfile(filePath): continue
			data=file(filePath,'r').read()
			match=reCas.search(data)
			primeid=os.path.splitext(filename)[0]
			if match:
				cas=match.group(1)
				print primeid,cas
				# each primed has a unique cas so we just store it
				self.primeid2cas[primeid]=cas
				# each cas may have more than one primeid so we store as a list and append
				if self.cas2primeids.has_key(cas):
					self.cas2primeids[cas].append(primeid)
					print "Warning! species %s all have CAS %s"%(self.cas2primeids[cas], cas)
				else:
					self.cas2primeids[cas]=[primeid]
				
class BurcatThermo:
	"""needs BURCAT_THR.xml file"""
	def __init__(self,mirror="BURCAT_THR.xml"):
		self.dom=xml.dom.minidom.parse('BURCAT_THR.xml')



	
	for specie in burcat.getElementsByTagName('specie'):
		cas=specie.attributes.getNamedItem('CAS').value
		try:
			primeids=p.cas2primeids[cas]
		except KeyError:
			print "species with CAS %s not in prime"%cas
			continue
		for phase in specie.getElementsByTagName('phase'):
			phase
			
			
class PrimeThermo:
	def __init__(self,primeid,mirror="warehouse.primekinetics.org"):
		self.primeid=primeid
		self.mirrorLocation=mirror
	def readThermo(self):
		path=os.path.join(self.mirrorLocation,'depository','species','data')
		listOfFiles=os.listdir(path)
		for filename in listOfFiles:
			filePath=os.path.join(path,filename)
			if not os.path.isfile(filePath): continue
			if not re.match('thp\d+\.xml',filename): continue

class untitledTests(unittest.TestCase):
	def setUp(self):
		pass


if __name__ == '__main__':
	unittest.main()
	
	p=PrimeSpeciesList()
	
