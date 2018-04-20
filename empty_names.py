#!/usr/bin/env python

from __future__ import print_function
from pprint import pprint
from irods.models import DataObject, DataObjectMeta, Collection
import os, sys
from irods.session import iRODSSession
from getopt import getopt

opts,args = getopt(sys.argv[1:],'c')
optD = {}; optD.update(opts)

try:
    env_file = os.environ['IRODS_ENVIRONMENT_FILE']
except KeyError:
    env_file = os.path.expanduser('~/.irods/irods_environment.json')

root = '/tempZone/home/rods'
assert len( args [:1] ) > 0

if args[:1]:
  root = args[0]

with iRODSSession(irods_env_file=env_file)  as ses:
  root += '/foo' 
  if optD.get('-c') is not None:

    dummy_filename = os.path.expanduser('~/dummy')
    open(dummy_filename,'wb').write(b'')
    ses.collections.create(root)	# <--- this is a different object in ICAT ...
    ses.collections.create(root+'/a')
    ses.collections.create(root+'/')	# <--- ... than this
    ses.collections.create(root+'/c')
    ses.data_objects.register (dummy_filename, root+'/a/b')
    ses.data_objects.register (dummy_filename, root+'/a/d')
    ses.data_objects.register (dummy_filename, root+'/c/b')
    ses.data_objects.register (dummy_filename, root+'/c/')
    ses.data_objects.register (dummy_filename, root+'/c/d')
    ses.collections.create(root+'//d')
  else:
    c1 = ses.collections.get(root+'')	# <--- this shows what was claimed above , that the two
    c2 = ses.collections.get(root+'/')	#      collections have different ID's in ICAT
    print (c1.id, c2.id)
    objs_in_coll = ses.collections.get(root+'/a').data_objects
    pprint(objs_in_coll)
    try:
      objs_in_coll = ses.collections.get(root+'/c').data_objects
      pprint(objs_in_coll)
    except TypeError as e : print ( "Caught exception -- {}".format(repr(e)))
