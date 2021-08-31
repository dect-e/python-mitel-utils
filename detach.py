#!/usr/bin/env python3

"""
Detach a user and device from each other (making them "Unbound").
May return "failure" even if the operation was successful. Reason for this
currently unknown.
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

print('success' if client.detach_user_device(int(sys.argv[1], 0), int(sys.argv[2], 0)) else 'failure')
