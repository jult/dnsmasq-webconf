#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import datetime
import json
import os
import re
import subprocess
import sys

from bottle import route, run, static_file, request, response, TEMPLATE_PATH
from bottle import jinja2_template as template

TEMPLATE_PATH.append('./views')
static_dir = './static'

config_file = '/etc/dnsmasq.conf'
reload_command = None

def get_config():
    if not os.path.isfile(config_file):
        return []
    with open(config_file, 'r') as f:
        lines = f.readlines()
    config = []
    for line in lines:
        line = line.strip()
        if line.startswith('dhcp-host='):
            data = line[len('dhcp-host='):].split('#', 1)
            fields = [f.strip() for f in data[0].split(',')]
            host = {
                'mac': fields[0] if len(fields) > 0 else None,
                'addr': fields[1] if len(fields) > 1 else None,
                'name': fields[2] if len(fields) > 2 else None,
                'comment': data[1].strip() if len(data) > 1 else None
            }
            config.append(host)
    return config

def host_to_line(host):
    # Ensure correct order and format: MAC, IP, hostname
    fields = [host.get('mac', ''), host.get('addr', ''), host.get('name', '')]
    fields = [field for field in fields if field]  # Remove empty fields
    line = f"dhcp-host={','.join(fields)}"
    if host.get('comment'):
        line += f" # {host['comment'].strip()}"
    return line

@route('/')
def index():
    config = get_config()
    return template('main.html.j2', config=config)

@route('/static/<path:path>')
def static_files(path):
    return static_file(path, root=static_dir)

@route('/api/config', method='GET')
def api_config():
    config = get_config()
    response.content_type = 'application/json'
    return json.dumps(config)

@route('/api/config', method='POST')
def save_config():
    data = request.json
    with open(config_file, 'w') as f:
        for host in data:
            f.write(host_to_line(host) + '\n')
    if reload_command:
        subprocess.call(reload_command, shell=True)
    response.content_type = 'application/json'
    return json.dumps({'status': 'ok'})

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Dnsmasq Web Configurator")
    parser.add_argument('--config', type=str, default=config_file, help='Path to dnsmasq config file')
    parser.add_argument('--reload', type=str, help='Command to reload dnsmasq')
    args = parser.parse_args()

    config_file = args.config
    reload_command = args.reload

    run(host='0.0.0.0', port=8080, debug=True)
