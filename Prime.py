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

class ThingWithCache:
	""" a parent class for things with caches. Classes inheriting from this can use various cache load/save functions"""
	def loadCache(self):
		try:
			for item in self.cacheItems:
				self.loadItem(item)
		except:
			print "couldn't load cache"
			return False
		return True
	def saveCache(self):
		try: # try to make the folder
			os.makedirs(self.cacheLocation)
		except OSError:
			pass # folder exists
		try:
			for item in self.cacheItems:
				self.saveItem(item)
		except:
			print "couldn't save cache"
			return False
		return True
	def saveItem(self,itemName):
		obj=getattr(self,itemName)
		filePath=os.path.join(self.cacheLocation,itemName+'.pkl')
		pickle.dump(obj, file(filePath, 'wb'))
	def loadItem(self,itemName):
		filePath=os.path.join(self.cacheLocation,itemName+'.pkl')
		setattr(self,itemName,pickle.load(file(filePath, 'rb')))
		
class PrimeSpeciesList(ThingWithCache):
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
				
class BurcatThermo(ThingWithCache):
	"""needs BURCAT_THR.xml file"""
	def __init__(self,mirror="BURCAT_THR.xml", cache="cache"):
		self.cacheLocation=cache
		# can't cache the dom because pickle's maximum recursion depth exceeded
		self.dom = self.readXML(mirror)

	def readXML(self,mirror):
		print "Reading in %s ..."%mirror
		dom=xml.dom.minidom.parse(mirror)
		print "Done!"
		return dom
		
	def loadCache(self):
		for item in self.cacheItems:
			self.loadItem(item)
	def saveCache(self):
		for item in self.cacheItems:
			self.saveItem(item)
			
	def species(self):
		for specie in self.dom.getElementsByTagName('specie'):
			yield BurcatSpecies(specie)
			
class BurcatSpecies:
	def __init__(self,dom):
		self.dom=dom
		if self.dom.attributes.has_key('CAS'):
			self.cas=self.dom.attributes.getNamedItem('CAS').value
		else: self.cas="No_CAS_in_Burcat"
	def phases(self):
		for phase in self.dom.getElementsByTagName('phase'):
			if len(phase.childNodes) > 1: # BURCAT_THR.xml has two types of <phase> node. One contains nested child nodes, the other just a text node "S|L|G". We only want the former.
				yield BurcatPhase(phase)
			else:
				print "I think %s is not a real phase"%phase.toxml()
			
class BurcatPhase:
	def __init__(self,dom):
		self.dom=dom
	def formula(self):
		formulas= self.dom.getElementsByTagName('formula')
		assert len(formulas)==1 ,"there should be only one formula"
		return formulas[0]
			
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
#	unittest.main()	
	p=PrimeSpeciesList()
	
	b=BurcatThermo()

	for specie in b.species():
		try:
			primeids=p.cas2primeids[specie.cas]
		except KeyError:
			print "species with CAS %s not in prime"%specie.cas
			continue			
		for phase in specie.phases():
			print phase.formula().firstChild.wholeText
			
	 b.dom.unlink() # memory explodes if you don't do this. 
	#comment it out though if you want to play around with things after running the script