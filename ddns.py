#!/usr/bin/env python3

import urllib.parse
import urllib.request
import sys
import os.path
from requests import get

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
            urllib.request.urlopen('https://api.dreamhost.com/?' +
                           urllib.parse.urlencode(args)).readlines()]
  return result[0], result[1:]

def replace_record(hostname, ip):
  '''Replace DH DNS records'''
  # find existing records
  status, response = call('dns-list_records')
  if status == 'success':
    for account_id, zone, record, type, value, comment, editable in (r.split('\t') for r in response[1:]):
      # and remove them
      if record == hostname and editable == '1' and value != ip:
        print(f"Current Record: {hostname} | {type} | {value}")
        call('dns-remove_record', record=hostname, type=type, value=value)
  else:
    return False
  # add the new record
  if value == ip:
    status, response = call('dns-add_record', record=hostname, type='A', value=ip, comment='DDNS')
    return status == 'success'
  else:
    return False

myip = get('https://api.ipify.org').content.decode('utf8')
print('Public IP address is: {}'.format(myip))

if replace_record(hostname, myip):
  print ('Good: {} set to {}'.format(hostname,myip))
else:
  print (f'No change as {hostname} is already {myip}') # didn't need to be changed