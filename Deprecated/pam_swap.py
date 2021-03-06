#! /usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
# Copyright 2016 the HERA Collaboration
# Licensed under the 2-clause BSD license.

"""
Script to handle swapping of PAMs.
"""

from __future__ import absolute_import, division, print_function

from hera_mc import mc, cm_utils, part_connect, cm_handling
import sys
import copy


def query_args(args):
    """
    Gets information from user
    """
    if args.receiverator is None:
        args.receiverator = raw_input('Receiverator containing the PAM:  ')
    if args.r_input is None:
        args.r_input = raw_input('What input on the receiverator (A1-B8):  ')
    if args.pam_number is None:
        print('The PAM has a five digit number on the front bottom.')
        args.pam_number = raw_input('What is the number:  ')
    args.date = cm_utils._query_default('date', args)
    return args


if __name__ == '__main__':
    parser = mc.get_mc_argument_parser()
    parser.add_argument('-r', '--receiverator', help="Receiverator number (1-8)",
                        default=None)
    parser.add_argument('-i', '--input', dest='r_input', help="Input to receiverator (A1-B8)",
                        default=None)
    parser.add_argument('-p', '--pam-number', dest='pam_number', help="Serial number of PAM",
                        default=None)
    parser.add_argument('--rev', help="Revision number of PAM (currently B)",
                        default='B')
    parser.add_argument('--actually_do_it', help="Flag to actually do it, as "
                        "opposed to printing out what it would do.",
                        action='store_true')
    cm_utils.add_date_time_args(parser)
    cm_utils.add_verbosity_args(parser)
    args = parser.parse_args()

    if args.receiverator is None or args.r_input is None or args.pam_number is None:
        args = query_args(args)

    # Pre-process some args
    args.r_input = args.r_input.upper()
    args.verbosity = args.verbosity.lower()
    at_date = cm_utils._get_astropytime(args.date, args.time)

    db = mc.connect_to_mc_db(args)
    session = db.sessionmaker()
    connect = part_connect.Connections()
    part = part_connect.Parts()
    handling = cm_handling.Handling(session)

    # Check for PAM and find RCVR
    new_hpn = 'PAM' + args.pam_number
    new_rev = 'B'  # This is the current revision number of the supplied PAMs
    rie = 'RI' + args.receiverator + args.r_input + 'E'
    rin = 'RI' + args.receiverator + args.r_input + 'N'
    roe = 'RO' + args.receiverator + args.r_input + 'E'
    ron = 'RO' + args.receiverator + args.r_input + 'N'
    if handling.is_in_connections(new_hpn, new_rev):
        go_ahead = False
        print("Error:  {} is already connected".format(new_hpn))
        print("Stopping this swap.")
    else:
        go_ahead = True
        rc = handling.get_connection_dossier(hpn_list=[rie], rev='A', port='b',
                                             at_date=at_date, exact_match=True)
        k = rc['connections'].keys()[0]
        old_rcvr = rc['connections'][k].downstream_part
        old_rrev = rc['connections'][k].down_part_rev
        print('Replacing {}:{} with {}:{}'.format(old_rcvr, old_rrev, new_hpn, new_rev))

    if go_ahead:
        # Add new PAM
        new_pam = [(new_hpn, new_rev, 'post-amp module', args.pam_number)]
        part_connect.add_new_parts(session, part, new_pam, at_date, args.actually_do_it)

        # Disconnect previous RCVR on both sides (RI/RO)
        pcs = [(old_rcvr, old_rrev, 'ea'), (old_rcvr, old_rrev, 'na'),
               (old_rcvr, old_rrev, 'eb'), (old_rcvr, old_rrev, 'nb')]
        part_connect.stop_existing_connections_to_part(session, handling, pcs, at_date,
                                                       args.actually_do_it)

        # Connect new PAM on both sides (RI/RO)
        npc = [(rie, 'A', 'b', new_hpn, new_rev, 'ea'),
               (rin, 'A', 'b', new_hpn, new_rev, 'na'),
               (new_hpn, new_rev, 'eb', roe, 'A', 'a'),
               (new_hpn, new_rev, 'nb', ron, 'A', 'a')]
        part_connect.add_new_connections(session, connect, npc, at_date, args.actually_do_it)
