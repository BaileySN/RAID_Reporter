#!/usr/bin/env bash
###########################################################################################################
# HW RAID Reporter v$ver                                                                                   #
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
cmd="$1"
crontime="$2"
ver="0.8"
echo """
##############################################################################################
#                                  HW Raid Reporter v$ver                                     #
#--------------------------------------------------------------------------------------------#
#                                         by BS @2015                                        #
#--------------------------------------------------------------------------------------------#
#               this thool set the hw_raid_reporter and a cronjob in /etc/crontab            #
##############################################################################################
    """
sleep 1
if [ "$(id -u)" != "0" ]; then
    echo "script must start with root Permissions (sudo)"
    exit 1
fi
echo """
###########################################################################################
# HW RAID Reporter v$ver  Copyright (C) 2015  Guenter Bailey                               #
# This program comes with ABSOLUTELY NO WARRANTY.                                         #
# This is free software, and you are welcome to redistribute it under certain conditions. #
###########################################################################################
    """
if [ "$cmd" = "tw" ] || [ "$cmd" = "mpt" ]; then
    if [ $crontime -ge 0 ]; then
        echo "create cronjob for checking RAID Health every $crontime"
        echo "0 */$crontime * * *   root	cd $PWD &&python reporter.py --$cmd " >> /etc/crontab
        echo "cronjob in /etc/crontab created"
        echo "create config.py and open in your default editor"
        cp -R ./conf/config.py.orig ./conf/config.py
        editor ./conf/config.py
        echo "setup finished"
        sleep 1
        echo "sending Testmail"
        echo "please check your inbox for Testmail"
        python reporter.py --testmail
        sleep 1
        echo "If you would change the settings, is stored under:"
        echo "cronjob -> /etc/crontab"
        echo "config -> ./conf/config.py"
    else
        echo "time to low"
        echo "the integer must greater than 0"
    fi
else
    echo """
    start setup.sh with option tw or mpt and checktime in hour
    -------------------------------------------------------------
    for example:

    for 3ware RAID controllers (tool tw_cli)
    sh setup.sh tw 3
    -------------------------------------------------------------
    for MPT controllers (tool mpt-status)
    sh setup.sh mpt 3
    -------------------------------------------------------------
    System requirement:
    Python 2.7.x
    tw_cli -> 3ware based controllers
    mpt-status -> Adaptec based controllers
    -------------------------------------------------------------
    the tool tw_cli or mpt-status must run from the commandline
    in example:
    root@vm1: tw_cli or mpt-status
        """
fi
