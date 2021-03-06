# -*- mode: python; coding: utf-8 -*-
# Copyright 2016 the HERA Collaboration
# Licensed under the 2-clause BSD license.

"""Some table info for configuration management.

"""

from __future__ import absolute_import, division, print_function

from . import part_connect, geo_location

# Locates the table and specifies the required order of deletion (inverse for creation.)
cm_tables = {'part_info': [part_connect.PartInfo, 0],
             'connections': [part_connect.Connections, 1],
             'parts': [part_connect.Parts, 2],
             'geo_location': [geo_location.GeoLocation, 3],
             'station_type': [geo_location.StationType, 4],
             'dubitable': [part_connect.Dubitable, 5]}
data_prefix = 'initialization_data_'


def order_the_tables(unordered_tables=None):
    if unordered_tables is None:
        unordered_tables = cm_tables.keys()
    ordered_tables = []
    for i in range(len(cm_tables.keys())):
        ordered_tables.append('NULL')
    for table in unordered_tables:
        try:
            ordered_tables[cm_tables[table][1]] = table
        except KeyError:
            print(table, 'not found')
    while 'NULL' in ordered_tables:
        ordered_tables.remove('NULL')
    return ordered_tables
