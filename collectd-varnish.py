#!/usr/bin/python
import collectd
import socket

# binary to call for varnishstat(1)
varnishstat = '/usr/bin/varnishstat'

# stats collection defaults, see
# http://collectd.org/wiki/index.php/Plugin:Varnish#Available_statistics
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
         
instances = {
    '': dict(collects),
}

# --
# config
# plugin configuration, get a dict of instances and stats per instance
# > conf        object      collectd Config object
def config(conf):
    global varnishstat, instances
    # get through the nodes under <Module "...">
    for node in conf.children:
        # change varnishstat binary path
        if node.key == "varnishstatBin":
            varnishstat = node.values[0]
            continue

        if node.key == "Instance"
            # if the instance is named, get the first given name
            if len(node.values):
                if len(node.values) > 1:
                    collectd.info("%s: Ignoring extra instance names (%s)" % (__name__, ", ".join(node.values[1:])) )
                instance = node.values[0]
            # else register an empty name instance
            else:
                instance = ''
    
            _collects = dict(collects)
            # get the stats to collect
            for child in node.children:
                # get the stat collection name
                if child.key.find("Collect") == 0:
                    collection = child.key[7:].lower()
                else:
                    collection = child.key.lower()

                # check if this collection is known
                if collection in collects:
                    _collects[collection] = True
                else:
                    collectd.warning("%s: Ignoring unknown configuration option (%s)" % (__name__, child.key))
    
            # add this instance to the dict of instances
            instances[instance] = _collects
            continue

        # unknown configuration node
        collectd.warning("%s: Ignoring unknown node type (%s)" % (__name__, node.key))

# --
# init
# initialisation function
def init():
    pass

# configuration callback
collectd.register_config(config)
# init callback
collectd.register_init(init)
