"""
load config from env vars
"""
import os

def options(opts=None):
    """ return options as dict from env vars """

    if opts is None:
        opts = {}

    def _opt(optkey, key, default):
        if optkey not in opts:
            opts[optkey] = os.environ.get(key, default)

    _opt('pg-host', 'PGHOST', '127.0.0.1')
    _opt('pg-username', 'PGUSER', 'bitwrap')
    _opt('pg-database', 'PGDATABASE', 'bitwrap')
    _opt('pg-password', 'PGPASSWORD', 'bitwrap')
    _opt('listen-port', 'LISTEN_PORT', '8080')
    _opt('listen-ip', 'LISTEN_IP', '0.0.0.0')

    return opts
