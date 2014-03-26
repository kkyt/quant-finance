import commandr

from pyutils import log, debug, env_utils

from quant_serviced import serviced
import quant_finance.server

mod = 'quant_finance'
env = env_utils.Env(mod)

@commandr.command
def server(bind=None):
    endpoint = env.get('endpoint', 'tcp://0.0.0.0:99999')
    e = bind or endpoint
    log.info("%s server bind to %s" % (mod,e))

    config = {
        'endpoint': e
    }
    server = quant_finance.server.create_server(config)

    attr = {
        'module': mod
    }
    serviced.create_service('zerorpc', mod, e, server, attr)

def main():
    try:
        commandr.Run()
    except:
        print debug.pretty_traceback()


