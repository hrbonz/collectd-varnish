#!/usr/bin/python
import collectd
import socket

instances = {}

def config(conf):
    for node in conf.children:
        # unknown configuration node
        if node.key != "Instance":
            collectd.warning("%s: Ignoring unknown node type (%s)" % (__name__, node.key))
            continue

        if len(node.values):
            if len(node.values) > 1:
                collectd.info("%s: Ignoring extra instance names (%s)" % (__name__, ", ".join(node.values[1:])) )
            instance = node.values[0]
        else:
            instance = ''

        collects = {
            'backend': True,
            'cache': True,
            'connections': True,
            'esi': False,
            'fetch': False,
            'hcb': False,
            'shm': True,
            'sm': False,
            'sma': False,
            'sms': False,
            'totals': False,
            'uptime': False,
            'workers': False,
        }
         
        for child in node.children:
            if child.key.find("Collect") == 0:
                collection = child.key[7:].lower()
                if collection in collects:
                    collects[collection] = True
                else:
                    collectd.warning("%s: Ignoring unknown configuration option (%s)" % (__name__, child.key))
            else:
                collectd.warning("%s: Ignoring unknown configuration option (%s)" % (__name__, child.key))

        instances[instance] = collects

# configuration callback
collectd.register_config(config)
