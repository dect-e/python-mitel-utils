#!/usr/bin/env python3

"""
Obtains the incoming caller number from Yate, finds the associated PP, and
continuously TTS-speaks the ID of the RFP the PP is connected to.
"""

import asyncio
import datetime
import logging
import os
import re
import uuid

import sys
import configparser

from OMMClient.OMMClient import OMMClient

import requests
from yate.protocol import MessageRequest
from yate.ivr import YateIVR


async def main(ivr: YateIVR):
    config = configparser.ConfigParser()
    config.read('pmu.ini')
    omm_ip = config['DEFAULT'].get('omm_ip')
    omm_port = config['DEFAULT'].getint('omm_port', 12622)
    omm_username = config['DEFAULT'].get('omm_username', 'omm')
    omm_password = config['DEFAULT'].get('omm_password')
    SOUNDS_PATH = config['DEFAULT'].get('sounds_path', '/opt/sounds')

    caller_id = ivr.call_params.get("caller", "")
    caller_id = re.sub("[^\\d]", "", caller_id)
    caller_id = re.sub("^\\+", "00", caller_id)

    await ivr.play_soundfile(os.path.join(SOUNDS_PATH, "intro.slin"), complete=True)
    await asyncio.sleep(0.5)

    await ivr.play_soundfile(os.path.join(SOUNDS_PATH, "parts", "TLN.slin"), complete=True)
    for digit in caller_id:
        await ivr.play_soundfile(os.path.join(SOUNDS_PATH, "parts", digit+".slin"), complete=True)

    client = OMMClient(omm_ip, omm_port)
    client.login(omm_username, omm_password)

    if not client:
        await ivr.play_soundfile(os.path.join(SOUNDS_PATH, "parts", "OMM.slin"), complete=True)
        await ivr.play_soundfile(os.path.join(SOUNDS_PATH, "parts", "unbekannt.slin"), complete=True)
        sys.exit(0)

    await ivr.play_soundfile(os.path.join(SOUNDS_PATH, "parts", "PP.slin"), complete=True)
    u = client.find_user({'num': caller_id})
    if not u:
        await ivr.play_soundfile(os.path.join(SOUNDS_PATH, "parts", "unbekannt.slin"), complete=True)
        sys.exit(0)
    for digit in str(u.ppn):
        await ivr.play_soundfile(os.path.join(SOUNDS_PATH, "parts", digit+".slin"), complete=True)

    previous_rfp = None
    while True:
        a = client.get_last_pp_dev_action(u.ppn)
        rfp = a.rfpId if a else None
        if rfp != previous_rfp:
            await ivr.play_soundfile(os.path.join(SOUNDS_PATH, "parts", "RFP.slin"), complete=True)
            if not rfp:
                await ivr.play_soundfile(os.path.join(SOUNDS_PATH, "parts", "unbekannt.slin"), complete=True)
                sys.exit(0)
            for digit in str(rfp):
                await ivr.play_soundfile(os.path.join(SOUNDS_PATH, "parts", digit+".slin"), complete=True)
            previous_rfp = rfp

    await asyncio.sleep(2)


app = YateIVR()
app.run(main)

