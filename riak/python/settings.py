import riak

_default_settings = {
    'TRANSPORT_CLASS': riak.RiakPbcTransport,
    'HOST': '127.0.0.1',
    'PORT': 8087,
}

try:
    from local_settings import settings as local_settings
    settings = dict(_default_settings.items() + local_settings.items())
except ImportError:
    settings = _default_settings

