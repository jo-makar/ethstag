#!/usr/bin/env python3
# Generate bootnodes.rs based on go-ethereum/params/bootnodes.go

import pathlib
import re
import urllib.request

url = 'https://raw.githubusercontent.com/ethereum/go-ethereum/master/params/bootnodes.go'

resp = urllib.request.urlopen(url, timeout=100)
if not (200 <= resp.status and resp.status < 300):
    raise Exception(f'non-200 resp.status ({resp.status} {resp.reason})')
body = resp.read().decode()

bootnodes = {}
state = 'base'
for line in body.splitlines():
    if state == 'base':
        if m := re.match(r'^var (.*)Bootnodes = \[\]string{$', line):
            state = m.group(1).lower()
            bootnodes[state] = []
    else:
        if re.match(r'^}$', line):
            state = 'base'
        elif m := re.match(r'^\s+"([^"]+)",', line):
            bootnodes[state] += [m.group(1)]
            
with open(pathlib.Path(__file__).parent / 'bootnodes.rs', 'w') as file:
    file.write('use std::collections::HashMap;\n')
    file.write('\n')
    file.write('lazy_static::lazy_static! {\n')
    file.write("    pub static ref BOOTNODES: HashMap<&'static str, Vec<&'static str>> = HashMap::from([\n")

    for network, bootnodes in bootnodes.items():
        file.write(f'        ("{network}",\n')
        file.write( '          vec![\n')
        for bootnode in bootnodes:
            file.write(f'            "{bootnode}",\n')
        file.write( '          ]),\n')

    file.write('    ]);\n')
    file.write('}\n')
