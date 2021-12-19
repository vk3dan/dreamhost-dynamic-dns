#!/usr/bin/env python3

import urllib.parse
import urllib.request
import sys
import os.path
from datetime import datetime

if not os.path.isfile("config.py"):
	sys.exit("'config.py' not found! Please add it and try again.")
else:
	import config

apikey = config.DREAMHOST_APIKEY
hostname = config.DDNS_HOSTNAME
myip = ""

def call(cmd, **args):
    '''Call a DreamHost API method. Turn each named python argument into named REST argument.'''
    args['key'] = apikey
    args['cmd'] = cmd
    result = [l.strip().decode('utf-8') for l in 
        urllib.request.urlopen('https://api.dreamhost.com/?' + urllib.parse.urlencode(args)).readlines()]
    return result[0], result[1:]

def replace_record(hostname, ip):
    '''Replace Dreamhost DNS records'''
    # find existing records
    status, response = call('dns-list_records')
    if status == 'success':
        for account_id, zone, record, type, value, comment, editable in (r.split('\t') for r in response[1:]):
            if record == hostname and editable == '1': # record exists of your hostname and isn't locked
                print(f'[{datetime.now()}] Current Record: {hostname} | {type} | {value}')
                if value != ip: # ip address is out of date, remove the old so we can add the new
                    print(f'[{datetime.now()}] Removing record {hostname} | A | {ip}')
                    call('dns-remove_record', record=hostname, type=type, value=value)
                else: # record is up to date, nothing needed.
                    return False
    else:
        sys.exit(f'[{datetime.now()}] Exiting: Failed to retrieve list from Dreamhost API')
    # add the new record
    if value != ip:
        print(f'[{datetime.now()}] Adding record {hostname} | A | {ip}')
        status, response = call('dns-add_record', record=hostname, type='A', value=ip, comment='DDNS')
        return status == 'success'
    else:
        return False

lookupip = urllib.request.urlopen('https://api.ipify.org') # returns external ip address so works behind NAT
myip = str(lookupip.read().decode('utf8'))
print(f'\n[{datetime.now()}] Public IP address is: {myip}')

if replace_record(hostname, myip):
    print (f'[{datetime.now()}] Done: {hostname} set to {myip}') # great success
else:
    print (f'[{datetime.now()}] Exiting: No change needed') # record was up to date so didn't need to be changed