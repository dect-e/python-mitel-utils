#!/usr/bin/env python3

"""
Obtains the incoming caller number from the first commandline argument, finds
the associated PP, and continuously prints the ID of the RFP the PP is
connected to, along with its most recent action.
"""

import sys
import configparser
import time
import datetime

from OMMClient.OMMClient import OMMClient

caller_id = sys.argv[1]

config = configparser.ConfigParser()
config.read('pmu.ini')
omm_ip = config['DEFAULT'].get('omm_ip')
omm_port = config['DEFAULT'].getint('omm_port', 12622)
omm_username = config['DEFAULT'].get('omm_username', 'omm')
omm_password = config['DEFAULT'].get('omm_password')

client = OMMClient(omm_ip, omm_port)
client.login(omm_username, omm_password)

print('num =', caller_id)
u = client.find_user({'num': caller_id})
print('PP ID =', u.ppn)

previous_rfp_trtype = None
while True:
    a = client.get_last_pp_dev_action(u.ppn)
    if not a.rfpId:
        print('RFP ID =', 'unbekannt')
        sys.exit(0)
    rfp_trtype = (a.rfpId, a.trType)
    if rfp_trtype != previous_rfp_trtype:
        print()
        print('RFP ID =', a.rfpId)
        print('trType =', a.trType)
        print('relTime =', -int(a.relTime), 'sec', '=', (datetime.datetime.now() + datetime.timedelta(seconds=-int(a.relTime))).strftime('%F %T %Z'))
        previous_rfp_trtype = rfp_trtype
        time.sleep(2)
