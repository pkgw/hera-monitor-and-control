#! /usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
# Copyright 2017 the HERA Collaboration
# Licensed under the 2-clause BSD license.

"""
Script to add quality metrics file to M&C database.
"""
from __future__ import absolute_import, division, print_function

import os
import numpy as np
import warnings

import hera_mc.mc as mc

parser = mc.get_mc_argument_parser()
parser.add_argument('files', metavar='files', type=str, nargs='+',
                    help='json files to read and enter into db.')
parser.add_argument('--type', dest='type', type=str, default=None,
                    help='File type to add to db. Options = ["ant", "firstcal", "omnical"]')
args = parser.parse_args()
db = mc.connect_to_mc_db(args)
session = db.sessionmaker()

files = args.files
if len(files) == 0:
    import sys
    print >>sys.stderr, 'Please provide a list of quality metric files.'
    sys.exit(1)

for f in files:
    session.ingest_metrics_file(f, args.type)

session.commit()
