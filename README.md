collectd varnish plugin in python
---------------------------------

A python plugin to collect data from a varnish service. This plugin reproduces collectd's varnish plugin behavior. It is meant to be used as a convenient replacement when the plugin is not available.

The main difference with collectd's plugin is that the python plugin uses `varnishstat` instead of the varnishapi library. Also `uptime` is suppported by this plugin.

Usage
-----

The configuration of the plugin follows collectd's varnish plugin in a pythonic way :

    <LoadPlugin python>
        Globals true
    </LoadPlugin>
    # ...
    <Plugin python>
        ModulePath "/path/to/your/python/modules"
        LogTraces true
        Import "collectd-varnish"

        <Module "collectd-varnish">
            varnishstatBin "/usr/local/bin/varnishstat"
            <Instance>
                CollectCache       true
                CollectConnections true
                CollectBackend     true
                CollectSHM         true
                CollectESI         false
                CollectFetch       false
                CollectHCB         false
                CollectSMA         false
                CollectSMS         false
                CollectSM          false
                CollectTotals      false
                CollectWorkers     false
            </Instance>
            <Instance "testdev">
                CollectCache       true
                CollectConnections true
                CollectBackend     false
                CollectUptime      true
            </Instance>
        </Module>
    </Plugin>

The default available statistics follow the [varnish plugin defaults](http://collectd.org/wiki/index.php/Plugin:Varnish#Available_statistics).

If no Instance name is given, get the default instance.

For a very minimalistic configuration you can use the following, this configuration will use all the defaults :

    <LoadPlugin python>
        Globals true
    </LoadPlugin>
    # ...
    <Plugin python>
        ModulePath "/path/to/your/python/modules"
        LogTraces true
        Import "collectd-varnish"

        <Module "collectd-varnish">
            <Instance>
                # comment to avoid parsing error
            </Instance>
        </Module>
    </Plugin>

The different options available are as follow :

* `varnishstatBin`: specify the path of `varnishstat(1)` binary, defaults to `/usr/bin/varnishstat`. Context: Module.
* `Instance `<name>`: create an instance block per varnish vcl instance to monitor. The name of the instance can be empty (considered as default instance). Context: Module.
* `CollectBackend <bool>` or `Backend <bool>`: Back-end connection statistics, such as successful, reused, and closed connections. Default: True. Context: Instance.
* `CollectCache <bool>` or `Cache <bool>`: Cache hits and misses. Default: True. Context: Instance.
* `CollectConnections <bool>` or `Connections <bool>`: Number of client connections received, accepted and dropped. Default: True. Context: Instance.
* `CollectESI <bool>` or `ESI <bool>`: Edge Side Includes (ESI) parse statistics. Default: False. Context: Instance.
* `CollectFetch <bool>` or `Fetch <bool>`: Statistics about fetches (HTTP requests sent to the backend). Default: False. Context: Instance.
* `CollectHCB <bool>` or `HCB <bool>`: Inserts and look-ups in the crit bit tree based hash. Look-ups are divided into locked and unlocked look-ups. Default: False. Context: Instance.
* `CollectSHM <bool>` or `SHM <bool>`: Statistics about the shared memory log, a memory region to store log messages which is flushed to disk when full. Default: True. Context: Instance.
* `CollectSM <bool>` or `SM <bool>`: file (memory mapped file) storage statistics. Default: False. Context: Instance.
* `CollectSMA <bool>` or `SMA <bool>`: malloc or umem (umem_alloc(3MALLOC) based) storage statistics. The umem storage component is Solaris specific. Default: False. Context: Instance.
* `CollectSMS <bool>` or `SMS <bool>`: synth (synthetic content) storage statistics. This storage component is used internally only. Default: False. Context: Instance.
* `CollectTotals <bool>` or `Totals <bool>`: Collects overview counters, such as the number of sessions created, the number of requests and bytes transferred. Default: False. Context: Instance.
* `CollectUptime <bool>` or `Uptime <bool>`: Server uptime. Default: False. Context: Instance.
* `CollectWorkers <bool>` or `Workers <bool>`: Collect statistics about worker threads. Default: False. Context: Instance.

References
----------

* [collectd website](http://collectd.org/)
* [collectd's python plugin](http://collectd.org/wiki/index.php/Plugin:Python)
* [documentation of collectd's python plusgin](http://collectd.org/documentation/manpages/collectd-python.5.shtml)
* [collectd's varnish plugin](http://collectd.org/wiki/index.php/Plugin:Varnish)
