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

References
----------

* [collectd website](http://collectd.org/)
* [collectd's python plugin](http://collectd.org/wiki/index.php/Plugin:Python)
* [documentation of collectd's python plusgin](http://collectd.org/documentation/manpages/collectd-python.5.shtml)
* [collectd's varnish plugin](http://collectd.org/wiki/index.php/Plugin:Varnish)
