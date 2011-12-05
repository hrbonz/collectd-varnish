#!/usr/bin/python
import collectd
import socket
import os
# use ctypes to dlopen libvarnishapi.so.1
import ctypes

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

# library to use
libvarnishapi = 'libvarnishapi.so.1'

# library preloads
libpreload = ('libvarnishcompat.so.1', 'libvarnish.so.1')

# varnish_stats struct, see varnish-2.1.x/include/stats.h and
# varnish-2.1.x/include/stat_field.h
class varnish_stats(ctypes.Structure):
    _fields_ = [
        ("client_conn", ctypes.c_uint64),
        ("client_drop", ctypes.c_uint64),
        ("client_req", ctypes.c_uint64),
        ("cache_hit", ctypes.c_uint64),
        ("cache_hitpass", ctypes.c_uint64),
        ("cache_miss", ctypes.c_uint64),
        ("backend_conn", ctypes.c_uint64),
        ("backend_unhealthy", ctypes.c_uint64),
        ("backend_busy", ctypes.c_uint64),
        ("backend_fail", ctypes.c_uint64),
        ("backend_reuse", ctypes.c_uint64),
        ("backend_toolate", ctypes.c_uint64),
        ("backend_recycle", ctypes.c_uint64),
        ("backend_unused", ctypes.c_uint64),
        ("fetch_head", ctypes.c_uint64),
        ("fetch_length", ctypes.c_uint64),
        ("fetch_chunked", ctypes.c_uint64),
        ("fetch_eof", ctypes.c_uint64),
        ("fetch_bad", ctypes.c_uint64),
        ("fetch_close", ctypes.c_uint64),
        ("fetch_oldhttp", ctypes.c_uint64),
        ("fetch_zero", ctypes.c_uint64),
        ("fetch_failed", ctypes.c_uint64),
        ("n_sess_mem", ctypes.c_uint64),
        ("n_sess", ctypes.c_uint64),
        ("n_object", ctypes.c_uint64),
        ("n_vampireobject", ctypes.c_uint64),
        ("n_objectcore", ctypes.c_uint64),
        ("n_objecthead", ctypes.c_uint64),
        ("n_smf", ctypes.c_uint64),
        ("n_smf_frag", ctypes.c_uint64),
        ("n_smf_large", ctypes.c_uint64),
        ("n_vbe_conn", ctypes.c_uint64),
        ("n_wrk", ctypes.c_uint64),
        ("n_wrk_create", ctypes.c_uint64),
        ("n_wrk_failed", ctypes.c_uint64),
        ("n_wrk_max", ctypes.c_uint64),
        ("n_wrk_queue", ctypes.c_uint64),
        ("n_wrk_overflow", ctypes.c_uint64),
        ("n_wrk_drop", ctypes.c_uint64),
        ("n_backend", ctypes.c_uint64),
        ("n_expired", ctypes.c_uint64),
        ("n_lru_nuked", ctypes.c_uint64),
        ("n_lru_saved", ctypes.c_uint64),
        ("n_lru_moved", ctypes.c_uint64),
        ("n_deathrow", ctypes.c_uint64),
        ("losthdr", ctypes.c_uint64),
        ("n_objsendfile", ctypes.c_uint64),
        ("n_objwrite", ctypes.c_uint64),
        ("n_objoverflow", ctypes.c_uint64),
        ("s_sess", ctypes.c_uint64),
        ("s_req", ctypes.c_uint64),
        ("s_pipe", ctypes.c_uint64),
        ("s_pass", ctypes.c_uint64),
        ("s_fetch", ctypes.c_uint64),
        ("s_hdrbytes", ctypes.c_uint64),
        ("s_bodybytes", ctypes.c_uint64),
        ("sess_closed", ctypes.c_uint64),
        ("sess_pipeline", ctypes.c_uint64),
        ("sess_readahead", ctypes.c_uint64),
        ("sess_linger", ctypes.c_uint64),
        ("sess_herd", ctypes.c_uint64),
        ("shm_records", ctypes.c_uint64),
        ("shm_writes", ctypes.c_uint64),
        ("shm_flushes", ctypes.c_uint64),
        ("shm_cont", ctypes.c_uint64),
        ("shm_cycles", ctypes.c_uint64),
        ("sm_nreq", ctypes.c_uint64),
        ("sm_nobj", ctypes.c_uint64),
        ("sm_balloc", ctypes.c_uint64),
        ("sm_bfree", ctypes.c_uint64),
        ("sma_nreq", ctypes.c_uint64),
        ("sma_nobj", ctypes.c_uint64),
        ("sma_nbytes", ctypes.c_uint64),
        ("sma_balloc", ctypes.c_uint64),
        ("sma_bfree", ctypes.c_uint64),
        ("sms_nreq", ctypes.c_uint64),
        ("sms_nobj", ctypes.c_uint64),
        ("sms_nbytes", ctypes.c_uint64),
        ("sms_balloc", ctypes.c_uint64),
        ("sms_bfree", ctypes.c_uint64),
        ("backend_req", ctypes.c_uint64),
        ("n_vcl", ctypes.c_uint64),
        ("n_vcl_avail", ctypes.c_uint64),
        ("n_vcl_discard", ctypes.c_uint64),
        ("n_purge", ctypes.c_uint64),
        ("n_purge_add", ctypes.c_uint64),
        ("n_purge_retire", ctypes.c_uint64),
        ("n_purge_obj_test", ctypes.c_uint64),
        ("n_purge_re_test", ctypes.c_uint64),
        ("n_purge_dups", ctypes.c_uint64),
        ("hcb_nolock", ctypes.c_uint64),
        ("hcb_lock", ctypes.c_uint64),
        ("hcb_insert", ctypes.c_uint64),
        ("esi_parse", ctypes.c_uint64),
        ("esi_errors", ctypes.c_uint64),
        ("accept_fail", ctypes.c_uint64),
        ("client_drop_late", ctypes.c_uint64),
        ("uptime", ctypes.c_uint64),
    ]


# --
# config
# plugin configuration, get a dict of instances and stats per instance
# > conf        object      collectd Config object
def config(conf):
    global instances
    # get through the nodes under <Module "...">
    for node in conf.children:
        if node.key == "Instance":
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
    # load dependency libraries
    for lib in libpreload:
        try:
            ctypes.CDLL(lib, mode=ctypes.RTLD_GLOBAL)
        except OSError, e:
            collectd.error("%s: could not load dependency library (%s)" % (__name__, lib))
            raise
    try:
        api = ctypes.CDLL(libvarnishapi)
    except OSError, e:
        collectd.error("%s: could not load api library (%s)" % (__name__, libvarnishapi))
        raise

    # everything ok, let's start reading values
    collectd.register_read(read, data=api)

# --
# dispatch
def dispatch(instance, stats):
    print dir(stats)

# --
# read_instance
def read_instance(instance, api):
    # if instance is empty ('') use default instance and call api with None,
    # that will be translated to NULL by ctypes
    cinstance = instance and instance or None
    openstats = api.VSL_OpenStats
    # create a pointer to the struct
    varnish_stats_ptr = ctypes.POINTER(varnish_stats)
    # use it as return type for calls to VSL_OpenStats
    openstats.restype = varnish_stats_ptr
    stats_ptr = openstats(cinstance)
    stats = stats_ptr.contents
    dispatch(instance, stats)

# --
# read
def read(api):
    for instance in instances:
        read_instance(instance, api)

# configuration callback
collectd.register_config(config)
# init callback
collectd.register_init(init)
