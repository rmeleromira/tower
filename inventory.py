#!/usr/bin/env python
import os
import sys
import argparse
import json
import libvirt

class LibvirtInventory(object):

    def __init__(self):
        self.inventory = {}
        self.read_cli_args()
        self.conn = libvirt.open('qemu+ssh://root@192.168.1.96/system')
        if self.conn == None:
            print('Failed to open connection to libvirt')
            exit(1)
        self.domains = self.conn.listDomainsID()
        if self.domains == None:
            print('Failed to get a list of domain IDs')
            exit(1)
        if len(self.domains) == 0:
            print('No Active Hosts')
            exit(1)

        if self.args.list:
            self.inventory = self.get_inventory()
        elif self.args.host:
            self.inventory = self.empty_inventory()

        print json.dumps(self.inventory);
        self.conn.close()

    def get_inventory(self):
        inventory = {
            'all': {'hosts': []},
            '_meta': {'hostvars': {}}
        }
        for domainid in self.domains:
            domain = self.conn.lookupByID(domainid)
            name = domain.name()
            if 'tower' in name:
                continue
            ip = domain.interfaceAddresses(libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_LEASE).popitem()[1]['addrs'][0]['addr']
            inventory['all']['hosts'].append(name)
            inventory['_meta']['hostvars'][name] = { 'ansible_host': ip }
        return inventory

    def empty_inventory(self):
        return {'_meta': {'hostvars': {}}}

    def read_cli_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--list', action = 'store_true')
        parser.add_argument('--host', action = 'store')
        self.args = parser.parse_args()
LibvirtInventory()
