from __future__ import with_statement  #  I think not needed in python 2.6
import sys
sys.path.append('restful_lib') # tell it where to look for restful_lib
import os
from restful_lib import Connection, ConnectionError

import xml, xml.dom.minidom
import re

class FailError(Exception):
    def __str__(self):
        return "Some error"

CHEMCASTER_ENDPOINT = "https://chemcaster.com/registries/19/"

class Chemcaster(object):
    def __init__(self, username='rwest@mit.edu',password='secret'):
        self._conn = Connection(CHEMCASTER_ENDPOINT, username, password)
        
    def post(self, body):
        resp = self._conn.request_post("structures",body=body )
        status= resp.get('headers').get('status') 
        if status not in ["200", 200, "204", 204]:
            print resp
            if status in ["422", 422]:
                resp['body']
                foo=xml.dom.minidom.parseString(resp['body'])
                for e in foo.getElementsByTagName('error'):
                    print e.firstChild.wholeText
            raise FailError
        return resp
        
class Structure:
    def __init__(self,name,molfile):
        (self.name,number_of_substitutions)=re.subn('[^A-Za-z0-9\-_~]','_',name) # Name can only have letters, numbers, and the symbols -_~
        if number_of_substitutions:
            print "Renamed %s to %s"%(name, self.name)
        self.mol=molfile
        
        self.dom=xml.dom.minidom.Document()
        d=self.dom
        structureNode=d.createElement('structure')
        d.appendChild(structureNode)
        nameNode=d.createElement('name')
        nameNode.appendChild(d.createTextNode(self.name))
        molNode=d.createElement('molfile')
        molNode.appendChild(d.createTextNode(self.mol))
        structureNode.appendChild(molNode)
        structureNode.appendChild(nameNode)
    def __del__(self):
        self.dom.unlink()
        
    def toxml(self):
        return self.dom.toxml()

def list_mol_files(path):
    """List paths to all the mol files in the directory."""
    listOfMols=[]
    listOfFiles=os.listdir(path)
    for filename in listOfFiles:
            (root, ext) = os.path.splitext(filename)
            if ext.lower() == '.mol':
                filePath=os.path.join(path,filename)
                listOfMols.append(filePath)
            else:
                print "I think %s isn't a mol file"%filename
    return listOfMols

def mol_name(path):
    """The name of the mol file from its path: Returns 'NAME' if given 'path/to/NAME.mol' """
    (head, tail) = os.path.split(path)
    (root,ext) = os.path.splitext(tail)
    return root
    
def upload_mol_files(dir):
    """Upload a directory full of mol files to Chemcaster."""
    list_of_mols=list_mol_files(dir)
    print list_of_mols
    repo = Chemcaster()
    for path in list_of_mols:
        with file(path) as f: # 'with' will close the filewhen done
            mol = f.read()
        name=mol_name(path)
        print name
        structure=Structure(name,mol)
        xml=structure.toxml()
        print xml
        print
        result=repo.post(xml)
        print result

if __name__ == "__main__":
    upload_mol_files(dir='BozzelliIJCK')
    
    
    