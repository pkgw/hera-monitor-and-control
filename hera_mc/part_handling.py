#! /usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
# Copyright 2016 the HERA Collaboration
# Licensed under the 2-clause BSD license.

"""
This is meant to hold utility scripts for parts and connections

"""
from __future__ import absolute_import, division, print_function
from tabulate import tabulate

from hera_mc import mc, part_connect, geo_location, correlator_levels
import copy, datetime

def _get_datetime(_date,_time):
    if _date.lower() == 'now':
        dt_d = datetime.datetime.now()
    else:
        data = _date.split('/')
        dt_d = datetime.datetime(int(data[2])+2000,int(data[0]),int(data[1]))
    if _time.lower() == 'now':
        dt_t = datetime.datetime.now()
    else:
        data = _time.split(':')
        dt_t = datetime.datetime(dt_d.year,dt_d.month,dt_d.day,int(data[0]),int(data[1]),0)
    dt = datetime.datetime(dt_d.year,dt_d.month,dt_d.day,dt_t.hour,dt_t.minute)
    return dt
def _get_stopdate(stop_date):
    if type(stop_date) == datetime.datetime:
        return stop_date
    else:
        return datetime.datetime(2020,12,31)

class PartsAndConnections:
    """
    Class to allow various manipulations of parts and their properties etc.  Things are 
    manipulated/passed as dictionaries currently.
    """
    no_connection_designator = '--'
    last_revisions = {}
    connections_dictionary = {}
    parts_dictionary = {}
    current = ''

    def __init__(self):
        pass

    def is_part_connected(self,args,hpn_query,rev_query='last',check_if_current=True):
        if check_if_current:
            current = _get_datetime(args.date,args.time)
        revq = rev_query.upper()
        if revq == 'LAST':
            revq = self.last_revisions[hpn_query]
        if hpn_query in self.parts_dictionary.keys() and self.parts_dictionary[hpn_query]['rev']==revq:
            return self.parts_dictionary[hpn_query]['is_connected']
        db = mc.connect_to_mc_db(args)
        with db.sessionmaker() as session:
            connected_query = session.query(part_connect.Connections).filter( ((part_connect.Connections.up      == hpn_query) &
                                                                               (part_connect.Connections.up_rev  == revq) )    | 
                                                                              ((part_connect.Connections.down    == hpn_query) &
                                                                               (part_connect.Connections.down_rev== revq) ))
            if connected_query.count() > 0:
                found_connected = True
            else:
                found_connected = False
            if found_connected and check_if_current:
                for cq in connected_query.all():
                    stop_date = _get_stopdate(cq.stop_date)
                    if current > cq.start_date and current < stop_date:
                        found_connected=True
                        break
                    else:
                        found_connected=False
        return found_connected

    def show_part(self, args, part_dict):
        """
        Print out part information.  Uses tabulate package.

        Parameters
        -----------
        args:  arguments as per mc and parts argument parser
        part_dict:  input dictionary of parts, generated by self.get_part
        """
        if args.show_active:
            current = _get_datetime(args.date,args.time)
        table_data = []
        if args.verbosity == 'm':
            headers = ['HERA P/N','Rev','Part Type','Mfg #','Start','Stop','Connected']
        elif args.verbosity == 'h':
            headers = ['HERA P/N','Rev','Part Type','Mfg #','Start','Stop','Connected','A ports','B ports','Info','Geo']
        for hpn in sorted(part_dict.keys()):
            stop_date = _get_stopdate(part_dict[hpn]['stop_date'])
            if args.show_active and current>part_dict[hpn]['start_date'] and current<stop_date:
                pass
            elif not args.show_active:
                pass
            else:
                continue
            connected = 'No'
            if part_dict[hpn]['is_connected']:
                connected = 'Yes'
            if args.verbosity == 'h':
                td = [hpn, part_dict[hpn]['rev'], part_dict[hpn]['hptype'],
                      part_dict[hpn]['manufacturer_number'],
                      part_dict[hpn]['start_date'], part_dict[hpn]['stop_date'],
                      connected]
                pts = ''
                for a in part_dict[hpn]['a_ports']:
                    pts+=(a+', ')
                td.append(pts.strip().strip(','))
                pts = ''
                for b in part_dict[hpn]['b_ports']:
                    pts+=(b+', ')
                td.append(pts.strip().strip(','))
                td.append(part_dict[hpn]['short_description'])
                if part_dict[hpn]['geo'] is not None:
                    s = "{:.1f}E, {:.1f}N, {:.1f}m".format(part_dict[hpn]['geo']['easting'],
                         part_dict[hpn]['geo']['northing'],part_dict[hpn]['geo']['elevation'])
                    td.append(s)
                table_data.append(td)
            elif args.verbosity == 'm':
                table_data.append([hpn, part_dict[hpn]['rev'], part_dict[hpn]['hptype'],
                    part_dict[hpn]['manufacturer_number'],
                    part_dict[hpn]['start_date'], part_dict[hpn]['stop_date'],
                    connected])
            else:
                print(hpn, part_dict[hpn]['repr'])
        if args.verbosity=='m' or args.verbosity=='h':
            print(tabulate(table_data,headers=headers,tablefmt='orgtbl'))

    def get_part(self, args, hpn_query=None, rev_query=None, exact_match=False, return_dictionary=True, show_part=False):
        """
        Return information on a part.  It will return all matching first characters unless exact_match==True.

        Returns part_dict, a dictionary keyed on hera part number with part data as found in hera_mc tables

        Parameters
        -----------
        args:  arguments as per mc and parts argument parser
        hpn_query:  the input hera part number (whole or first part thereof)
        exact_match:  boolean to enforce full part number match
        show_part:  boolean to call show_part or not
        """

        if hpn_query is None:
            hpn_query = args.hpn
            exact_match = args.exact_match
        if rev_query is None:
            rev_query = args.revision_number
        if not exact_match and hpn_query[-1]!='%':
            hpn_query = hpn_query+'%'

        local_parts_keys = []
        part_dict = {}
        db = mc.connect_to_mc_db(args)
        with db.sessionmaker() as session:
            ### Get parts to check and fill in last_revisions and connections_dictionary as able
            for match_part in session.query(part_connect.Parts).filter(part_connect.Parts.hpn.like(hpn_query)):
                if match_part.hpn not in local_parts_keys:
                    local_parts_keys.append(match_part.hpn)
                    if match_part.hpn not in self.last_revisions.keys():
                        self.last_revisions[match_part.hpn] = part_connect.get_last_revision_number(args,match_part.hpn,False)
                    if match_part.hpn not in self.connections_dictionary.keys():
                        self.get_connection(args, hpn_query=match_part.hpn, rev_query = rev_query, port_query='all', 
                                        exact_match=True, return_dictionary=False, show_connection=False)
            ### Now get unique part/rev and put into dictionary
            for match_key in local_parts_keys:
                revq = rev_query.upper()
                if revq == 'LAST':
                    revq = self.last_revisions[match_key]
                part_query = session.query(part_connect.Parts).filter( (part_connect.Parts.hpn==match_key) &
                                                                       (part_connect.Parts.hpn_rev==revq) )
                part_and_rev = part_query.all()
                part_cnt = part_query.count()
                if not part_cnt:     ### None found.
                    continue
                elif part_cnt == 1:
                    part = part_and_rev[0]   ### Found only one.
                    is_connected = self.is_part_connected(args,part.hpn,part.hpn_rev,True)
                    psd_for_dict = part.stop_date
                    if not part.stop_date:
                        psd_for_dict = 'N/A'
                    part_dict[part.hpn] = {'rev':part.hpn_rev, 'is_connected':is_connected,
                                           'hptype': part.hptype,
                                           'manufacturer_number': part.manufacturer_number,
                                           'start_date': part.start_date, 'stop_date': psd_for_dict,
                                           'a_ports': [], 'b_ports': [], 'short_description':'', 'geo':None}
                    part_dict[part.hpn]['repr'] = part.__repr__()  # Keep for now
                    for part_info in session.query(part_connect.PartInfo).filter( (part_connect.PartInfo.hpn == part.hpn) &
                                                                                  (part_connect.PartInfo.hpn_rev == part.hpn_rev) ):
                        part_dict[part.hpn]['short_description'] = part_info.short_description
                    part_dict[part.hpn]['a_ports'] = self.connections_dictionary[part.hpn]['a_ports']
                    part_dict[part.hpn]['b_ports'] = self.connections_dictionary[part.hpn]['b_ports']
                    if part.hptype == 'station':
                        args.locate = part.hpn
                        part_dict[part.hpn]['geo'] = geo_location.locate_station(args, show_geo=False)
                    if part.hpn not in self.parts_dictionary.keys():
                        self.parts_dictionary[part.hpn] = part_dict[part.hpn]  ### This only handles the most recent revs.
                else:   ### Found more than one, which shouldn't happen.
                    print("Warning part_handling:125:  Well, being here is a surprise -- should only be one part.", part.hpn)
        if show_part:
            if len(part_dict.keys()) == 0:
                print(hpn_query,' not found.')
            else:
                self.show_part(args, part_dict)
        if return_dictionary:
            return part_dict

    def __pull_out_component(self,cmpt_list,i):
        try:
            c = cmpt_list[i]
        except IndexError:
            try:
                c = cmpt_list[-1]
            except IndexError:
                c = self.no_connection_designator
        return c
    def show_connection(self, args, connection_dict):
        """
        Print out connection information.  Uses tabulate package.

        Parameters
        -----------
        args:  arguments as per mc and parts argument parser
        connection_dict:  input dictionary of parts, generated by self.get_connection
        """

        if args.show_active:
            current = _get_datetime(args.date,args.time)
        table_data = []
        if args.verbosity == 'm':
            headers = ['Upstream', '<Port b:', ':Port a>', 'Part', '<Port b:', ':Port a>', 'Downstream']
        elif args.verbosity == 'h':
            headers = ['Upstream', '<Port b:', ':Port a>', 'Part', '<Port b:', ':Port a>', 'Downstream']
        for pkey in sorted(connection_dict.keys()):
            for i in range(len(connection_dict[pkey]['a_ports'])):
                up        = self.__pull_out_component(connection_dict[pkey]['up_parts'],i)
                dn        = self.__pull_out_component(connection_dict[pkey]['down_parts'],i)
                pta       = self.__pull_out_component(connection_dict[pkey]['a_ports'],i)
                ptb       = self.__pull_out_component(connection_dict[pkey]['b_ports'],i)
                bup       = self.__pull_out_component(connection_dict[pkey]['b_on_up'],i)
                adn       = self.__pull_out_component(connection_dict[pkey]['a_on_down'],i)
                rup       = self.__pull_out_component(connection_dict[pkey]['repr_up'],i)
                rdown     = self.__pull_out_component(connection_dict[pkey]['repr_down'],i)
                startup   = self.__pull_out_component(connection_dict[pkey]['start_on_up'],i)
                stopup    = self.__pull_out_component(connection_dict[pkey]['stop_on_up'],i)
                startdown = self.__pull_out_component(connection_dict[pkey]['start_on_down'],i)
                stopdown  = self.__pull_out_component(connection_dict[pkey]['stop_on_down'],i)
                if args.show_active:
                    stopup = _get_stopdate(stopup)
                    stopdown = _get_stopdate(stopdown)
                    show_it = (current>startup and current<stopup) and (current>startdown and current<stopdown)
                else:
                    show_it = True
                if show_it:
                    if args.verbosity == 'h':
                        if stopup>current:
                            stopup = '-'
                        if stopdown>current:
                            stopdown = '-'
                        table_data.append([startup,stopup,' ',' ',' ',startdown,stopdown])
                        table_data.append([up,bup,pta,pkey,ptb,adn,dn])
                    elif args.verbosity == 'm':
                        if not args.show_active:
                            if stopup>current:
                                stop = '-'
                            if stopdown>current:
                                stopdown = '-'
                            table_data.append([startup,stopup,' ',' ',' ',startdown,stopdown])
                        table_data.append([up,bup,pta,pkey,ptb,adn,dn])
                    else:
                        print(rup,rdown)
        if args.verbosity=='m' or args.verbosity=='h':
            print(tabulate(table_data,headers=headers,tablefmt='orgtbl'))


    def get_connection(self, args, hpn_query=None, rev_query=None, port_query=None, exact_match=False, 
                             return_dictionary=True, show_connection=False):
        """
        Return information on parts connected to args.connection -- NEED TO INCLUDE USING START/STOP_TIME!!!
        It should get connections immediately adjacent to one part (upstream and downstream).

        Returns connection_dict, a dictionary keyed on part number of adjacent connections

        Parameters
        -----------
        args:  arguments as per mc and parts argument parser
        hpn_query:  the input hera part number (whole or first part thereof)
        port_query:  a specifiable port name,  default is 'all'
        exact_match:  boolean to enforce full part number match
        show_connection:  boolean to call show_part or not
        """

        if hpn_query is None:
            hpn_query = args.connection
            exact_match = args.exact_match
        if rev_query is None:
            rev_query = args.revision_number
        if not exact_match and hpn_query[-1]!='%':
            hpn_query = hpn_query+'%'
        if port_query is None:
            port_query = args.specify_port
        connection_dict = {}
        db = mc.connect_to_mc_db(args)
        with db.sessionmaker() as session:
            ### Find where the part is in the upward connection
            for match_connection in session.query(part_connect.Connections).filter(part_connect.Connections.up.like(hpn_query)):
                if port_query=='all' or match_connection.b_on_up == port_query:
                    #-#THIS SHOULD HAVE WORKED BUT DOESN'T#-#
                    #-#if match_connection.up not in connection_dict.keys() and match_connection.up in self.connections_dictionary.keys():
                    #-#    connection_dict[match_connection.up] = copy.deepcopy(self.connections_dictionary[match_connection.up])
                    #-#    continue
                    if match_connection.up not in connection_dict.keys():
                        revq = rev_query.upper()
                        if revq == 'LAST':
                            if match_connection.up not in self.last_revisions.keys():
                                self.last_revisions[match_connection.up] = part_connect.get_last_revision_number(args,match_connection.up,False)
                            revq = self.last_revisions[match_connection.up]
                        connection_dict[match_connection.up] = {'rev':revq,
                                                                'a_ports':[], 'up_parts':[],   'up_rev':[],  'b_on_up':[], 
                                                                'b_ports':[], 'down_parts':[], 'down_rev':[],'a_on_down':[],
                                                                'start_on_down':[], 'stop_on_down':[], 'repr_down':[],
                                                                'start_on_up':[],   'stop_on_up':[],   'repr_up':[]}
                    connection_dict[match_connection.up]['b_ports'].append(match_connection.b_on_up)
                    connection_dict[match_connection.up]['down_parts'].append(match_connection.down)
                    connection_dict[match_connection.up]['down_rev'].append(match_connection.down_rev)
                    connection_dict[match_connection.up]['a_on_down'].append(match_connection.a_on_down)
                    connection_dict[match_connection.up]['start_on_down'].append(match_connection.start_date)
                    connection_dict[match_connection.up]['stop_on_down'].append(match_connection.stop_date)
                    connection_dict[match_connection.up]['repr_down'].append(match_connection.__repr__())
            ### Find where the part is in the downward connection
            for match_connection in session.query(part_connect.Connections).filter(part_connect.Connections.down.like(hpn_query)):
                if port_query=='all' or match_connection.a_on_down == port_query:
                    #-#THIS SHOULD HAVE WORKED BUT DOESN'T#-#
                    #-#if match_connection.down not in connection_dict.keys() and match_connection.down in self.connections_dictionary.keys():
                    #-#    connection_dict[match_connection.down] = copy.deepcopy(self.connections_dictionary[match_connection.down])
                    #-#    continue
                    if match_connection.down not in connection_dict.keys():
                        revq = rev_query.upper()
                        if revq == 'LAST':
                            if match_connection.down not in self.last_revisions.keys():
                                self.last_revisions[match_connection.down] = part_connect.get_last_revision_number(args,match_connection.down,False)
                            revq = self.last_revisions[match_connection.down]
                        connection_dict[match_connection.down] = {'rev':revq,
                                                                  'a_ports':[], 'up_parts':[],   'up_rev':[],  'b_on_up':[], 
                                                                  'b_ports':[], 'down_parts':[], 'down_rev':[],'a_on_down':[],
                                                                  'start_on_down':[], 'stop_on_down':[], 'repr_down':[],
                                                                  'start_on_up':[],   'stop_on_up':[],   'repr_up':[]}
                    connection_dict[match_connection.down]['a_ports'].append(match_connection.a_on_down)
                    connection_dict[match_connection.down]['up_parts'].append(match_connection.up)
                    connection_dict[match_connection.down]['up_rev'].append(match_connection.up_rev)
                    connection_dict[match_connection.down]['b_on_up'].append(match_connection.b_on_up)
                    connection_dict[match_connection.down]['start_on_up'].append(match_connection.start_date)
                    connection_dict[match_connection.down]['stop_on_up'].append(match_connection.stop_date)
                    connection_dict[match_connection.down]['repr_up'].append(match_connection.__repr__())
        connection_dict = self.__check_ports(args,connection_dict,rev_query)
        for pkey in connection_dict.keys():
            if pkey not in self.connections_dictionary.keys():
                self.connections_dictionary[pkey] = copy.copy(connection_dict[pkey])
        if show_connection:
            self.show_connection(args, connection_dict)
        if return_dictionary:
            return connection_dict

    def __check_ports(self,args,connection_dict, rev_query):
        """
        Check and balance the ports on all of the parts in the connection dictionary
        """
        ### Check and balance ports
        for pkey in connection_dict.keys():
            number_of_ports = {'A':len(connection_dict[pkey]['a_ports']),'B':len(connection_dict[pkey]['b_ports'])}
            if number_of_ports['A']==0:
                connection_dict[pkey]['a_ports'] = [self.no_connection_designator]
            if number_of_ports['B']==0:
                connection_dict[pkey]['b_ports'] = [self.no_connection_designator]
            if number_of_ports['A'] > number_of_ports['B']:
                for i in range(number_of_ports['A']-1):
                    connection_dict[pkey]['b_ports'].append(self.no_connection_designator)
            elif number_of_ports['B'] > number_of_ports['A']:
                for i in range(number_of_ports['B']-1):
                    connection_dict[pkey]['a_ports'].append(self.no_connection_designator)
            elif number_of_ports['A']>1:  # #A==#B > 1, (2)
                part_to_check = {}
                part_to_check[pkey] = {'a_ports':connection_dict[pkey]['a_ports'], 'b_ports':connection_dict[pkey]['a_ports']}
                for i,p in enumerate(part_to_check[pkey]['a_ports']):
                    check_port = self.__get_next_port(args,pkey,rev_query,p,direction='down',check_part=part_to_check)
                    if check_port != part_to_check[pkey]['b_ports'][i]:
                        print('Ports differ from expected:  ',p,check_port,part_to_check[pkey]['b_ports'][i])
                        print('Reset to ',connection_dict[pkey]['b_ports'][i],'to',check_port)
                        connection_dict[pkey]['b_ports'][i] = check_port
        return connection_dict

    def __get_next_port(self,args,hpn,rev,port,direction,check_part):
        """
        Get port on correct side of a given part to move up/down stream.
        """
        if check_part:
            part_dict = check_part
        else:
            part_dict = self.get_part(args,hpn_query=hpn,rev_query=rev,
                exact_match=True, return_dictionary=True, show_part=False)
        if direction=='up':
            ports = [part_dict[hpn]['a_ports'],part_dict[hpn]['b_ports']]
            replacing = ['b','a']
        elif direction=='down':
            ports = [part_dict[hpn]['b_ports'],part_dict[hpn]['a_ports']]
            replacing = ['a','b']
        number_of_ports = [len(ports[0]),len(ports[1])]
        for i,p in enumerate(ports):
            if self.no_connection_designator in p: #This will only take out one.
                number_of_ports[i]-=1
        if port in ports[0]:
            return_port = port
        elif number_of_ports[0] == 1:
            return_port = ports[0][0]
        elif number_of_ports[0] == 0:
            return_port = None
        elif port in ports[1]:
            if number_of_ports[1] == number_of_ports[0]:
                return_port = port.replace(replacing[0],replacing[1])
            elif number_of_ports[1] > number_of_ports[0]: # SHOULDN'T GET HERE
                return_port = ports[0][0]                 #   BUT JUST IN CASE PICK ONE
            else:                                         # HERE IS THE ILL-DEFINED BRANCHING CASE
                return_port = ports[0][0]                 #   PICK ONE FOR NOW
        else:
            print('Error:  port not found',port)
            return_port = None 
        return return_port

    def __go_upstream(self, args, hpn, rev, port):
        """
        Find the next connection up the signal chain.
        """
        up_port = self.__get_next_port(args,hpn,rev,port,direction='up',check_part=False)
        if up_port == self.no_connection_designator or up_port is None:
            return
        connection_dict = self.get_connection(args, hpn_query=hpn, rev_query=rev, port_query=up_port, 
                                              exact_match=True, show_connection=False)
        for i,hpn_up in enumerate(connection_dict[hpn]['up_parts']):
            port = connection_dict[hpn]['b_on_up'][i]
            if hpn_up not in self.upstream:
                stopup = _get_stopdate(connection_dict[hpn]['stop_on_up'][i])
                if (self.current>connection_dict[hpn]['start_on_up'][i]) and (self.current<stopup):
                    hpn_up_pr = hpn_up
                else:
                    hpn_up_pr = '**'+str(hpn_up)
                self.upstream.append([hpn_up_pr,port])
            self.__go_upstream(args, hpn_up, rev, port)

    def __go_downstream(self, args, hpn, rev, port):
        """
        Find the next connection down the signal chain
        """
        down_port = self.__get_next_port(args,hpn,rev,port,direction='down',check_part=False)
        if down_port == self.no_connection_designator or down_port is None:
            return
        connection_dict = self.get_connection(args, hpn_query=hpn, rev_query=rev, port_query=down_port, 
                                              exact_match=True, show_connection=False)
        for i,hpn_down in enumerate(connection_dict[hpn]['down_parts']):
            port = connection_dict[hpn]['a_on_down'][i]
            if hpn_down not in self.downstream:
                stopdown = _get_stopdate(connection_dict[hpn]['stop_on_down'][i])
                if (self.current>connection_dict[hpn]['start_on_down'][i]) and (self.current<stopdown):
                    hpn_down_pr = hpn_down
                else:
                    hpn_down_pr = '**'+str(hpn_down)
                self.downstream.append([hpn_down_pr,port])
            self.__go_downstream(args, hpn_down, rev, port)


    def get_hookup(self, args, hpn_query=None, rev_query=None, port_query=None, show_hookup=False):
        """
        Return the full hookup.  Note that if a part is selected up or down stream of a branching part, 
        it picks one and doesn't give all options -- something to work on.
        Returns hookup_dict, a dictionary keyed on derived key of hpn:port

        Parameters
        -----------
        args:  arguments as per mc and parts argument parser
        hpn_query:  the input hera part number (whole or first part thereof)
        port_query:  a specifiable port name,  default is 'all'
        show_hookup:  boolean to call show_hookup or not

        """
        self.current = _get_datetime(args.date,args.time)
        exact_match = False
        if hpn_query is None:
            hpn_query = args.mapr
            exact_match = args.exact_match
        if rev_query is None:
            rev_query = args.revision_number
        if port_query is None:
            port_query = args.specify_port
        parts = self.get_part(args, hpn_query=hpn_query, rev_query=rev_query, 
                exact_match=exact_match, return_dictionary=True, show_part=False)
        connections = None
        hookup_dict = {}
        for hpn in parts.keys():
            if parts[hpn]['is_connected'] == False:
                continue
            number_a_ports = len(parts[hpn]['a_ports'])
            number_b_ports = len(parts[hpn]['b_ports'])
            if port_query == 'all':
                if number_b_ports>number_a_ports:
                    pq = 'b_ports'
                    alt_pq = 'a_ports'
                else:
                    pq = 'a_ports'
                    alt_pq = 'b_ports'
                port_query = parts[hpn][pq]
                if self.no_connection_designator in port_query:
                    port_query = parts[hpn][alt_pq]
            elif type(port_query) is not list:
                port_query = [port_query]
            for p in port_query:
                if p == self.no_connection_designator:
                    continue
                self.upstream = [[hpn,p]]
                self.downstream = []
                self.__go_upstream(args, hpn, rev_query, p)
                self.__go_downstream(args, hpn, rev_query, p)
                furthest_up = self.upstream[-1][0].strip('*')
                try_station = self.get_part(args,hpn_query=furthest_up,rev_query=rev_query,
                              exact_match=True, return_dictionary=True, show_part=False)
                keep_entry = True
                hukey = hpn+':'+p
                if try_station[furthest_up]['hptype'] == 'station':
                    hookup_dict[hukey] = [[try_station[furthest_up]['geo']['station_number'],'S']]
                else:
                    hookup_dict[hukey] = []
                for pn in reversed(self.upstream):
                    hookup_dict[hukey].append(pn)
                    if self.parts_dictionary[pn[0].strip('*')]['is_connected'] == False:
                        keep_entry = False
                        break
                if keep_entry:
                    for pn in self.downstream:
                        hookup_dict[hukey].append(pn)
                        if self.parts_dictionary[pn[0].strip('*')]['is_connected'] == False:
                            keep_entry = False
                            break
                if keep_entry == False:
                    del hookup_dict[hukey]
                #-#for pkey in hookup_dict.keys():
                #-#    print('#-#==>', hookup_dict[pkey])
        if len(hookup_dict.keys())==0:
            print(hpn_query,'not found')
            return None
        tkey = hookup_dict.keys()[0]
        hookup_dict['columns'] = []
        for hu in hookup_dict[tkey]:
            pn = hu[0].strip('*')
            print(hu)
            if hu[1]=='S':
                hookup_dict['columns'].append(['station','column'])
            else:
                get_part_type = self.get_part(args,hpn_query=pn,rev_query=rev_query,
                                exact_match=True, return_dictionary=True, show_part=False)
                hookup_dict['columns'].append([get_part_type[pn]['hptype'],'column'])
        if args.show_levels:
            hookup_dict = self.__get_correlator_levels(hookup_dict,args.levels_testing)
        if show_hookup:
            self.show_hookup(hookup_dict,args.mapr_cols,args.show_levels)
        return hookup_dict


    def __get_correlator_levels(self,hookup_dict,testing):
        hookup_dict['columns'].append(['levels','column'])
        pf_input = []
        for k in sorted(hookup_dict.keys()):
            if k=='columns':
                continue
            f_engine = hookup_dict[k][-1][0].strip('*')
            pf_input.append(f_engine)
        levels = correlator_levels.get_levels(pf_input,testing)
        for i,k in enumerate(sorted(hookup_dict.keys())):
            if k=='columns':
                continue
            lstr = '%s' % (levels[i])
            hookup_dict[k].append([lstr,pf_input[i]])
        return hookup_dict


    def show_hookup(self, hookup_dict, cols_to_show, show_levels):
        """
        Print out the hookup table -- uses tabulate package.  
        Station is used twice, so grouped together and applies some ad hoc formatting.

        Parameters
        -----------
        hookup_dict:  generated in self.get_hookup
        """

        headers = []
        show_flag = []
        if cols_to_show != 'all':
            cols_to_show=cols_to_show.split(',')
            if show_levels:
                cols_to_show.append('levels')
        for col in hookup_dict['columns']:
            if col[0][-2:]=='_e' or col[0][-2:]=='_n': #Makes these specific pol parts generic
                colhead = col[0][:-2]
            else:
                colhead = col[0]
            if cols_to_show == 'all' or colhead in cols_to_show:
                show_flag.append(True)
            else:
                show_flag.append(False)
                continue
            if colhead not in headers: #Accounts for station used twice
                headers.append(colhead)
        if show_levels:
            show_flag.append(True)
        table_data = []
        for hukey in sorted(hookup_dict.keys()):
            if hukey=='columns':
                continue
            if len(hookup_dict[hukey]) != len(hookup_dict['columns']):
                print('Issues with ',hukey)
                continue
            td = []
            for i,pn in enumerate(hookup_dict[hukey]):
                if not i or not show_flag[i]:  #If station first time or not shown
                    continue
                if i==1:
                    s = "{:0>3}  {}".format(str(hookup_dict[hukey][0][0]), str(hookup_dict[hukey][1][0]))
                else:
                    if pn[0] == hukey.split(':')[0]:
                        s = '['+str(pn[0])+']'
                    else:
                        s = str(pn[0])
                td.append(s)
            table_data.append(td)
        print(tabulate(table_data,headers=headers,tablefmt='orgtbl'))

    def get_part_types(self, args, show_hptype=False):
        """
        Goes through database and pulls out part types and some other info to display in a table.

        Returns part_type_dict, a dictionary keyed on part type

        Parameters
        -----------
        args:  arguments as per mc and parts argument parser
        show_hptype:  boolean variable to print it out
        """
        
        self.part_type_dict = {}
        db = mc.connect_to_mc_db(args)
        with db.sessionmaker() as session:
            for part in session.query(part_connect.Parts).all():
                if part.hptype not in self.part_type_dict.keys():
                    self.part_type_dict[part.hptype] = {'part_list':[part.hpn], 'a_ports':[], 'b_ports':[]}
                else:
                    self.part_type_dict[part.hptype]['part_list'].append(part.hpn)
        if show_hptype:
            headers = ['Part type','# in dbase','A ports','B ports']
            table_data = []
        for k in self.part_type_dict.keys():  ###ASSUME FIRST PART IS FULLY CONNECTED
            pa = self.part_type_dict[k]['part_list'][0]  
            pd = self.get_part(args,pa,show_part=False)
            self.part_type_dict[k]['a_ports'] = pd[pa]['a_ports']
            self.part_type_dict[k]['b_ports'] = pd[pa]['b_ports']
            if show_hptype:
                td = [k,len(self.part_type_dict[k]['part_list'])]
                pts = ''
                for a in self.part_type_dict[k]['a_ports']:
                    pts+=(a+', ')
                td.append(pts.strip().strip(','))
                pts = ''
                for b in self.part_type_dict[k]['b_ports']:
                    pts+=(b+', ')
                td.append(pts.strip().strip(','))
                table_data.append(td)
        if show_hptype:
            print(tabulate(table_data,headers=headers,tablefmt='orgtbl'))          
        return self.part_type_dict

