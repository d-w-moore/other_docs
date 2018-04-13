#!/usr/bin/env python3
import sys
import os
from irods.session import iRODSSession
from irods.meta import iRODSMeta
from irods.models import DataObjectMeta , DataObject
from pprint import pprint,pformat

import re

whiteSpace = re.compile(r'\s+')

try:
    env_file = os.environ['IRODS_ENVIRONMENT_FILE']
except KeyError:
    env_file = os.path.expanduser('~/.irods/irods_environment.json')

session= iRODSSession(irods_env_file=env_file) 

do = 'foo.dat'
o = session.data_objects.get('/tempZone/home/rods/foo.dat')


m = o.metadata 

shouldContinue =True

while shouldContinue:

   x = input()

   x = whiteSpace.split(x.strip())
   x[0] = x[0].lower()

   if x[0].startswith( 's'):		pprint (m.items())
   elif x[0].startswith( 'c'):		m[ x[1] ] = iRODSMeta( *x[1:] )
   elif x[0].startswith( 'r'):		m.remove_all()
   elif x[0].startswith( 'q'):		shouldContinue = False
   elif x[0].startswith( 'a'):		m.add ( *x[1:] )
   else:

     print ('''
	s - show metadata
	a - add metadata
        r - remove all metadata
	c - change metadata
	q - quit ''', file = sys.stderr)
