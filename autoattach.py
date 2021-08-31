#!/usr/bin/env python3

"""
Print all currently unbound user and device entries from the OMM.
If there is exactly one unbound user and one unbound device, attach them to
each other.
"""

import sys
import configparser

from OMMClient.OMMClient import OMMClient

config = configparser.ConfigParser()
config.read('pmu.ini')

omm_ip = config['DEFAULT'].get('omm_ip')
omm_port = config['DEFAULT'].getint('omm_port', 12622)
omm_username = config['DEFAULT'].get('omm_username', 'omm')
omm_password = config['DEFAULT'].get('omm_password')

client = OMMClient(omm_ip, omm_port)
client.login(omm_username, omm_password)

ub_users = list(client.find_users({'ppn': '0'}))
print('Unbound users:', [u.num + ' (' + u.uid + ')' for u in ub_users])

ub_devs = list(client.find_devices({'relType': 'Unbound'}))
print('Unbound devices:', [d.ipei + ' (' + d.ppn + ')' for d in ub_devs])

if len(ub_users) == 1 and len(ub_devs) == 1:
    print('success' if client.attach_user_device(int(ub_users[0].uid), int(ub_devs[0].ppn)) else 'failure')
else:
    print('No unique user-device pair, please run attach.py manually.')

