#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################################################################
# RAID Reporter                                                                                           #
# Copyright (C) [2015]  [Guenter Bailey]                                                                  #
#                                                                                                         #
# This program is free software;                                                                          #
# you can redistribute it and/or modify it under the terms of the GNU General Public License              #
# as published by the Free Software Foundation;                                                           #
# either version 3 of the License, or (at your option) any later version.                                 #
#                                                                                                         #
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;               #
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.               #
# See the GNU General Public License for more details.                                                    #
#                                                                                                         #
# You should have received a copy of the GNU General Public License along with this program;              #
# if not, see <http://www.gnu.org/licenses/>.                                                             #
###########################################################################################################

from re import search
from sys import exit
from os.path import isfile
from optparse import OptionParser
from subprocess import Popen, PIPE
from bin import mailsend
from conf import mode

def testmail(msg):
    mailsend.emailsend(msg)
    print("sending Testmail...")

def wherecmd(cmds):
    cmd1 = ''
    if cmds == "mpt":
        cmd1 = "mpt-status"
    elif cmds == "tw":
        cmd1 = "tw_cli"

    c1 = ['which', cmd1]
    p1 = Popen(c1, stdout=PIPE)
    return p1.communicate()[0].replace('\n','')

def check_controller(type):
    ret = True

    cmd = []
    array = {}
    contr = {}
    drive = {}

    if type == 'mpt':
        cmd = [ wherecmd("mpt"), '-s']
        # cmd = [ '/usr/sbin/mpt-status', '-s' ]
        array = {'regex': '^log_id$',
                 'pos': 2,
                 'string': 'OPTIMAL'}
        drive = {'regex': '^phys_id$',
                 'pos': 2,
                 'string': 'ONLINE'}
    elif type == 'tw':
        cmd = [ wherecmd("tw"), 'info']
        # cmd = [ '/usr/bin/tw_cli', 'info' ]
        contr = {'regex': '^c\d+$'}
        array = {'regex': '^u\d+$',
                 'pos': 2,
                 'string': 'OK'}
        drive = {'regex': '^p\d+$',
                 'pos': 1,
                 'string': 'OK'}

    if not isfile(cmd[0]):
        print "%s: Utility not found" % cmd[0]
        return False

    controllers = []
    if type == 'tw':
        # controllers = []
        p = Popen(cmd, stdout=PIPE)
        o, e = p.communicate()
        if e:
            print e
        for c in o.split('\n'):
            c = c.split()
            if len(c) > 2 and search(contr['regex'], c[0]):
                controllers.append(c[0])
    elif type == 'mpt':
        controllers = ['']

    for c in controllers:
        p = Popen(cmd + [c], stdout=PIPE)
        o, e = p.communicate()
        if e:
            print e.split('\n')
        for v in o.split('\n'):
            v = v.split()
            if len(v) > 2:
                # Array check.
                if mode.silent == "yes" or mode.silent == "y":
                    if search(array['regex'], v[0]) and v[array['pos']] != array['string']:
                        if search(array['regex'], v[0]) and v[array['pos']] != "VERIFYING":
                            msg = ("Array failure: \n\t%s" % '\t'.join(v))
                            print(msg)
                            mailsend.emailsend(msg)
                            ret = False
                else:
                    if search(array['regex'], v[0]) and v[array['pos']] != array['string']:
                        msg = ("Array failure: \n\t%s" % '\t'.join(v))
                        print(msg)
                        mailsend.emailsend(msg)
                        ret = False
                # Drive check.
                if search(drive['regex'], v[0]) and v[drive['pos']] != drive['string']:
                    msg = ("Drive failure: \n\t%s" % '\t'.join(v))
                    print(msg)
                    mailsend.emailsend(msg)
                    ret = False
    return ret

def main():
    usage = "usage: %prog options"
    parser = OptionParser(usage=usage)
    parser.add_option("--mpt", action="store_true", default=False,
                      dest="mpt", help="MPT controller support.")
    parser.add_option("--tw", action="store_true", default=False,
                      dest="tw", help="3ware controller support.")
    parser.add_option("--testmail", action="store_true", default=False,
                      dest="testmail", help="Sending Testmail")
    (options, args) = parser.parse_args()

    if options.testmail:
        testmail("This is a test Report, for checking the Mail Settings.")
        exit(2)

    elif not options.mpt and not options.tw:
        parser.print_help()
        exit(2)

    fail = False

    if options.mpt:
        if not check_controller('mpt'):
            fail = True

    if options.tw:
        if not check_controller('tw'):
            fail = True

    if fail:
        exit(1)

if __name__ == "__main__":
    main()
