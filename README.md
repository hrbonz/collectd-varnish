collectd varnish plugin in python
---------------------------------

A python plugin to collect data from a varnish service. It is meant to be used as a convenient replacement when the C plugin is not available or more datas are needed (the c plugin restricts the datas collected).

This plugin uses the ctypes module to call directly the `libvarnishapi.so.1` library.

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
            <Instance>
                Cache       true
                Connections true
                Backend     true
                SHM         true
                ESI         false
                Fetch       false
                HCB         false
                SMA         false
                SMS         false
                SM          false
                Totals      false
                Workers     false
            </Instance>
            <Instance "testdev">
                Cache       true
                Connections true
                Backend     false
                Uptime      true
            </Instance>
        </Module>
    </Plugin>

The default available statistics follow the [varnish plugin defaults](http://collectd.org/wiki/index.php/Plugin:Varnish#Available_statistics).

If no Instance name is given, get the default instance (varnish uses hostname as default).

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

* `Instance `<name>`: create an instance block per varnish instance to monitor. The name of the instance can be empty (considered as default instance). Context: Module.
* `Backend <bool>`: Back-end connection statistics, such as successful, reused, and closed connections. Default: True. Context: Instance.
* `Cache <bool>`: Cache hits and misses. Default: True. Context: Instance.
* `Connections <bool>`: Number of client connections received, accepted and dropped. Default: True. Context: Instance.
* `ESI <bool>`: Edge Side Includes (ESI) parse statistics. Default: False. Context: Instance.
* `Fetch <bool>`: Statistics about fetches (HTTP requests sent to the backend). Default: False. Context: Instance.
* `HCB <bool>`: Inserts and look-ups in the crit bit tree based hash. Look-ups are divided into locked and unlocked look-ups. Default: False. Context: Instance.
* `SHM <bool>`: Statistics about the shared memory log, a memory region to store log messages which is flushed to disk when full. Default: True. Context: Instance.
* `SM <bool>`: file (memory mapped file) storage statistics. Default: False. Context: Instance.
* `SMA <bool>`: malloc or umem (umem_alloc(3MALLOC) based) storage statistics. The umem storage component is Solaris specific. Default: False. Context: Instance.
* `SMS <bool>`: synth (synthetic content) storage statistics. This storage component is used internally only. Default: False. Context: Instance.
* `Totals <bool>`: Collects overview counters, such as the number of sessions created, the number of requests and bytes transferred. Default: False. Context: Instance.
* `Uptime <bool>`: Server uptime. Default: False. Context: Instance.
* `Workers <bool>`: Collect statistics about worker threads. Default: False. Context: Instance.

References
----------

* [collectd website](http://collectd.org/)
* [collectd's python plugin](http://collectd.org/wiki/index.php/Plugin:Python)
* [documentation of collectd's python plusgin](http://collectd.org/documentation/manpages/collectd-python.5.shtml)
* [collectd's varnish plugin](http://collectd.org/wiki/index.php/Plugin:Varnish)
* [varnish explanation of stats](https://www.varnish-cache.org/trac/wiki/StatsExplained)
* varnish source : `include/stat_field.h`, `lib/libvarnishapi/shmlog.c`
