# -*- mode: python; coding: utf-8 -*-
# Copyright 2016 the HERA Collaboration
# Licensed under the 2-clause BSD license.

"""Testing for `hera_mc.geo_location and geo_handling`.


"""

from __future__ import absolute_import, division, print_function

import unittest

from hera_mc import geo_location, geo_handling, mc, cm_transfer
from hera_mc.tests import TestHERAMC


class TestGeo(TestHERAMC):


    def test_add_loc(self):
        st = geo_location.StationType()
        st.station_type_name='test_element'
        st.prefix='TE'
        self.test_session.add(st)
        self.test_session.commit()
        gl = geo_location.GeoLocation()
        gl.station_name = 'ELEMENT'
        gl.station_type_name = 'test_element'
        gl.created_gpstime = 1172530000
        self.test_session.add(gl)
        self.test_session.commit()
        self.assertTrue

    def test_cofa(self):
        st = geo_location.StationType()
        st.station_type_name='cofa'
        st.prefix='COFA'
        self.test_session.add(st)
        self.test_session.commit()
        gl = geo_location.GeoLocation()
        gl.station_name = 'cofa_null'
        gl.station_type_name = 'cofa'
        gl.created_gpstime = 1172530000
        self.test_session.add(gl)
        self.test_session.commit()
        h = geo_handling.Handling(self.test_session)
        cofa = h.cofa()
        self.assertTrue('cofa' in cofa.station_name.lower())

    def test_get_location(self):
        st = geo_location.StationType()
        st.station_type_name='test_element'
        st.prefix='TE'
        self.test_session.add(st)
        self.test_session.commit()
        gl = geo_location.GeoLocation()
        gl.station_name = 'ELEMENT'
        gl.station_type_name = 'test_element'
        gl.created_gpstime = 1172530000
        self.test_session.add(gl)
        self.test_session.commit()
        h = geo_handling.Handling(self.test_session)
        located = h.get_location(['ELEMENT'], 'now')
        self.assertTrue(located[0].station_name == 'ELEMENT')


if __name__ == '__main__':
    unittest.main()
