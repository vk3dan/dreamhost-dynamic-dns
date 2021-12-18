#!/usr/bin/env python3

import urllib.parse
import urllib.request
import sys
import os.path
from requests import get
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
    '''Replace DH DNS records'''
    # find existing records
    status, response = call('dns-list_records')
    if status == 'success':
        for account_id, zone, record, type, value, comment, editable in (r.split('\t') for r in response[1:]):
            if record == hostname and editable == '1':
                print(f'[{datetime.now()}] Current Record: {hostname} | {type} | {value}')
                if value != ip:
                    print(f'[{datetime.now()}] Adding record {hostname} | A | {ip}')
                    call('dns-remove_record', record=hostname, type=type, value=value)
                else:
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

myip = get('https://api.ipify.org').content.decode('utf8')
print(f'[{datetime.now()}] Public IP address is: {myip}')

if replace_record(hostname, myip):
    print (f'[{datetime.now()}] Done: {hostname} set to {myip}')
else:
    print (f'[{datetime.now()}] Exiting: No change needed') # didn't need to be changed