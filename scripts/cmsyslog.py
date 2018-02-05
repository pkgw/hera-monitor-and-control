#! /usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
# Copyright 2017 the HERA Collaboration
# Licensed under the 2-clause BSD license.

"""
Script to handle adding a system-wide comment to the part_info table.
"""

from __future__ import print_function

from hera_mc import mc, cm_utils, part_connect, sys_handling

SYSTEM = 'System'  # word used in part_info as hpn for these comments


if __name__ == '__main__':
    parser = mc.get_mc_argument_parser()
    parser.add_argument('-k', '--keyword', help="Keyword for comments [general]", default='geneRAL')
    parser.add_argument('-c', '--comment', help="Comment on part", default=None)
    parser.add_argument('-l', '--library_file', help="Library filename", default=None)
    parser.add_argument('-v', '--view', help='View all (or just keyword, if supplied) system comments', action='store_true')
    cm_utils.add_date_time_args(parser)
    args = parser.parse_args()

    # Pre-process some args
    at_date = cm_utils.get_astropytime(args.date, args.time)
    if args.view:
        if args.keyword == 'geneRAL':
            args.keyword = 'ALL'
    else:
        if args.comment is None:
            args.comment = raw_input('Comment:  ')
    args.keyword = args.keyword.lower()

    db = mc.connect_to_mc_db(args)
    session = db.sessionmaker()

    # Check for part
    if args.view:
        print("Comments - {}:{}".format(SYSTEM, args.keyword))
        handling = sys_handling.Handling(session)
        print(handling.system_comments(system_kw=SYSTEM, kword=args.keyword))
    else:
        print("Adding system info:  {}:{}".format(SYSTEM, args.keyword))
        part_connect.add_part_info(session, SYSTEM, args.keyword, at_date, args.comment, args.library_file)
