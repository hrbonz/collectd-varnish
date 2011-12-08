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
    'client': True,
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
        ('client_conn', ctypes.c_uint64),    # client
        ('client_drop', ctypes.c_uint64),    # client
        ('client_req', ctypes.c_uint64),    # client
        ('cache_hit', ctypes.c_uint64),    # cache
        ('cache_hitpass', ctypes.c_uint64),    # cache
        ('cache_miss', ctypes.c_uint64),    # cache
        ('backend_conn', ctypes.c_uint64),    # backend
        ('backend_unhealthy', ctypes.c_uint64),    # backend
        ('backend_busy', ctypes.c_uint64),    # backend
        ('backend_fail', ctypes.c_uint64),    # backend
        ('backend_reuse', ctypes.c_uint64),    # backend
        ('backend_toolate', ctypes.c_uint64),    # backend
        ('backend_recycle', ctypes.c_uint64),    # backend
        ('backend_unused', ctypes.c_uint64),    # backend
        ('fetch_head', ctypes.c_uint64),    # fetch
        ('fetch_length', ctypes.c_uint64),    # fetch
        ('fetch_chunked', ctypes.c_uint64),    # fetch
        ('fetch_eof', ctypes.c_uint64),    # fetch
        ('fetch_bad', ctypes.c_uint64),    # fetch
        ('fetch_close', ctypes.c_uint64),    # fetch
        ('fetch_oldhttp', ctypes.c_uint64),    # fetch
        ('fetch_zero', ctypes.c_uint64),    # fetch
        ('fetch_failed', ctypes.c_uint64),    # fetch
        ('n_sess_mem', ctypes.c_uint64),
        ('n_sess', ctypes.c_uint64),
        ('n_object', ctypes.c_uint64),
        ('n_vampireobject', ctypes.c_uint64),
        ('n_objectcore', ctypes.c_uint64),
        ('n_objecthead', ctypes.c_uint64),
        ('n_smf', ctypes.c_uint64),
        ('n_smf_frag', ctypes.c_uint64),
        ('n_smf_large', ctypes.c_uint64),
        ('n_vbe_conn', ctypes.c_uint64),
        ('n_wrk', ctypes.c_uint64),    # workers
        ('n_wrk_create', ctypes.c_uint64),    # workers
        ('n_wrk_failed', ctypes.c_uint64),    # workers
        ('n_wrk_max', ctypes.c_uint64),    # workers
        ('n_wrk_queue', ctypes.c_uint64),    # workers
        ('n_wrk_overflow', ctypes.c_uint64),    # workers
        ('n_wrk_drop', ctypes.c_uint64),    # workers
        ('n_backend', ctypes.c_uint64),
        ('n_expired', ctypes.c_uint64),
        ('n_lru_nuked', ctypes.c_uint64),
        ('n_lru_saved', ctypes.c_uint64),
        ('n_lru_moved', ctypes.c_uint64),
        ('n_deathrow', ctypes.c_uint64),
        ('losthdr', ctypes.c_uint64),
        ('n_objsendfile', ctypes.c_uint64),
        ('n_objwrite', ctypes.c_uint64),
        ('n_objoverflow', ctypes.c_uint64),
        ('s_sess', ctypes.c_uint64),    # totals
        ('s_req', ctypes.c_uint64),    # totals
        ('s_pipe', ctypes.c_uint64),    # totals
        ('s_pass', ctypes.c_uint64),    # totals
        ('s_fetch', ctypes.c_uint64),    # totals
        ('s_hdrbytes', ctypes.c_uint64),    # totals
        ('s_bodybytes', ctypes.c_uint64),    # totals
        ('sess_closed', ctypes.c_uint64),
        ('sess_pipeline', ctypes.c_uint64),
        ('sess_readahead', ctypes.c_uint64),
        ('sess_linger', ctypes.c_uint64),
        ('sess_herd', ctypes.c_uint64),
        ('shm_records', ctypes.c_uint64),    # shm
        ('shm_writes', ctypes.c_uint64),    # shm
        ('shm_flushes', ctypes.c_uint64),    # shm
        ('shm_cont', ctypes.c_uint64),    # shm
        ('shm_cycles', ctypes.c_uint64),    # shm
        ('sm_nreq', ctypes.c_uint64),    # sm
        ('sm_nobj', ctypes.c_uint64),    # sm
        ('sm_balloc', ctypes.c_uint64),    # sm
        ('sm_bfree', ctypes.c_uint64),    # sm
        ('sma_nreq', ctypes.c_uint64),    # sma
        ('sma_nobj', ctypes.c_uint64),    # sma
        ('sma_nbytes', ctypes.c_uint64),    # sma
        ('sma_balloc', ctypes.c_uint64),    # sma
        ('sma_bfree', ctypes.c_uint64),    # sma
        ('sms_nreq', ctypes.c_uint64),    # sms
        ('sms_nobj', ctypes.c_uint64),    # sms
        ('sms_nbytes', ctypes.c_uint64),    # sms
        ('sms_balloc', ctypes.c_uint64),    # sms
        ('sms_bfree', ctypes.c_uint64),    # sms
        ('backend_req', ctypes.c_uint64),    # backend
        ('n_vcl', ctypes.c_uint64),
        ('n_vcl_avail', ctypes.c_uint64),
        ('n_vcl_discard', ctypes.c_uint64),
        ('n_purge', ctypes.c_uint64),
        ('n_purge_add', ctypes.c_uint64),
        ('n_purge_retire', ctypes.c_uint64),
        ('n_purge_obj_test', ctypes.c_uint64),
        ('n_purge_re_test', ctypes.c_uint64),
        ('n_purge_dups', ctypes.c_uint64),
        ('hcb_nolock', ctypes.c_uint64),    # hcb
        ('hcb_lock', ctypes.c_uint64),    # hcb
        ('hcb_insert', ctypes.c_uint64),    # hcb
        ('esi_parse', ctypes.c_uint64),    # esi
        ('esi_errors', ctypes.c_uint64),    # esi
        ('accept_fail', ctypes.c_uint64),
        ('client_drop_late', ctypes.c_uint64),
        ('uptime', ctypes.c_uint64),    # uptime
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
# dispatch_metric
def dispatch_metric(instance, stats, value, type):
    metric = collectd.Values()
    metric.plugin = 'varnish'
    metric.plugin_instance = instance and instance or 'default'
    metric.type = type
    metric.type_instance = value
    metric.values = [getattr(stats, value)]
    metric.dispatch()

# --
# dispatch_gauge
def dispatch_gauge(instance, stats, value):
    dispatch_metric(instance, stats, value, 'gauge')

# --
# dispatch_derive
def dispatch_derive(instance, stats, value):
    dispatch_metric(instance, stats, value, 'derive')

# --
# dispatch
def dispatch(instance, stats):
    conf = instances[instance]
    if conf['backend']:
        dispatch_derive(instance, stats, 'backend_conn')
        dispatch_derive(instance, stats, 'backend_unhealthy')
        dispatch_derive(instance, stats, 'backend_busy')
        dispatch_derive(instance, stats, 'backend_fail')
        dispatch_derive(instance, stats, 'backend_reuse')
        dispatch_derive(instance, stats, 'backend_toolate')
        dispatch_derive(instance, stats, 'backend_recycle')
        dispatch_derive(instance, stats, 'backend_unused')
        dispatch_derive(instance, stats, 'backend_req')
    if conf['cache']:
        dispatch_derive(instance, stats, 'cache_hit')
        dispatch_derive(instance, stats, 'cache_hitpass')
        dispatch_derive(instance, stats, 'cache_miss')
    if conf['client']:
        dispatch_derive(instance, stats, 'client_conn')
        dispatch_derive(instance, stats, 'client_drop')
        dispatch_derive(instance, stats, 'client_req')
    if conf['esi']:
        dispatch_derive(instance, stats, 'esi_parse')
        dispatch_derive(instance, stats, 'esi_errors')
    if conf['fetch']:
        dispatch_derive(instance, stats, 'fetch_head')
        dispatch_derive(instance, stats, 'fetch_length')
        dispatch_derive(instance, stats, 'fetch_chunked')
        dispatch_derive(instance, stats, 'fetch_eof')
        dispatch_derive(instance, stats, 'fetch_bad')
        dispatch_derive(instance, stats, 'fetch_close')
        dispatch_derive(instance, stats, 'fetch_oldhttp')
        dispatch_derive(instance, stats, 'fetch_zero')
        dispatch_derive(instance, stats, 'fetch_failed')
    if conf['hcb']:
        dispatch_derive(instance, stats, 'hcb_nolock')
        dispatch_derive(instance, stats, 'hcb_lock')
        dispatch_derive(instance, stats, 'hcb_insert')
    if conf['shm']:
        dispatch_derive(instance, stats, 'shm_records')
        dispatch_derive(instance, stats, 'shm_writes')
        dispatch_derive(instance, stats, 'shm_flushes')
        dispatch_derive(instance, stats, 'shm_cont')
        dispatch_derive(instance, stats, 'shm_cycles')
    if conf['sm']:
        dispatch_derive(instance, stats, 'sm_nreq')
        dispatch_gauge(instance, stats, 'sm_nobj')
        dispatch_derive(instance, stats, 'sm_balloc')
        dispatch_derive(instance, stats, 'sm_bfree')
    if conf['sma']:
        dispatch_derive(instance, stats, 'sma_nreq')
        dispatch_gauge(instance, stats, 'sma_nobj')
        dispatch_gauge(instance, stats, 'sma_nbytes')
        dispatch_derive(instance, stats, 'sma_balloc')
        dispatch_derive(instance, stats, 'sma_bfree')
    if conf['sms']:
        dispatch_derive(instance, stats, 'sms_nreq')
        dispatch_gauge(instance, stats, 'sms_nobj')
        dispatch_gauge(instance, stats, 'sms_nbytes')
        dispatch_derive(instance, stats, 'sms_balloc')
        dispatch_derive(instance, stats, 'sms_bfree')
    if conf['totals']:
        dispatch_derive(instance, stats, 's_sess')
        dispatch_derive(instance, stats, 's_req')
        dispatch_derive(instance, stats, 's_pipe')
        dispatch_derive(instance, stats, 's_pass')
        dispatch_derive(instance, stats, 's_fetch')
        dispatch_derive(instance, stats, 's_hdrbytes')
        dispatch_derive(instance, stats, 's_bodybytes')
    if conf['uptime']:
        dispatch_derive(instance, stats, 'uptime')
    if conf['workers']:
        dispatch_gauge(instance, stats, 'n_wrk')
        dispatch_derive(instance, stats, 'n_wrk_create')
        dispatch_derive(instance, stats, 'n_wrk_failed')
        dispatch_derive(instance, stats, 'n_wrk_max')
        dispatch_derive(instance, stats, 'n_wrk_queue')
        dispatch_derive(instance, stats, 'n_wrk_overflow')
        dispatch_derive(instance, stats, 'n_wrk_drop')

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
    print instances
    for instance in instances:
        read_instance(instance, api)

# configuration callback
collectd.register_config(config)
# init callback
collectd.register_init(init)
