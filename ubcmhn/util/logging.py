import logging
import os

from ubcmhn.config import CfgClass

def configure_logging_from_config(config : CfgClass):
    # CONFIG
    _loglevel = config.LOGLEVEL
    _logstdout = config.LOGSTDOUT # Log to Stdout?

    # Prepare Root Logger.
    rootlogger = logging.getLogger()
    rootlogger.setLevel(logging.NOTSET) # Set the rootlogger to receive all log events.

    # Clear Handlers
    rootlogger.handlers = []

    # Log to STDOUT?
    if _logstdout:
        # Get StreamHandler
        handler_stdout = logging.StreamHandler()

        # Set this handler to receive only events higher than 'loglevel'
        handler_stdout.setLevel(_loglevel)

        # Get formatter for stdouthandler
        #formatstring_debug = "%(asctime)s %(name)s (%(module)s.py:%(lineno)s) %(levelname)s: %(message)s"
        formatstring_norm = "%(asctime)s %(name)s %(levelname)s: %(message)s"

        fmt_stdout = logging.Formatter(formatstring_norm)

        # Add formatter to stdouthandler
        handler_stdout.setFormatter(fmt_stdout)

        # Add handler to root logger.
        rootlogger.addHandler(handler_stdout)

    return rootlogger


#TODO: Implement 'to file' logtarget // For now, 'stdout'-only logging suffices for this experiment.
def bootstrap_logging(_loglevel=logging.DEBUG, _logtargets=('stdout',)):
    rootlogger = logging.getLogger()

    # If this environment variable is set, use it as the value of the wanted loglevel
    # during the application's bootstrap phase.
    real_loglevel = _loglevel
    if 'UBCMHNBOOTSTRAPLOGLEVEL' in os.environ:
        real_loglevel = int(os.environ['UBCMHNBOOTSTRAPLOGLEVEL'])

    # Set the rootlogger to receive all log events.
    rootlogger.setLevel(logging.NOTSET)
    logtargets_lower = [ld.lower() for ld in _logtargets]

    # Clear Handlers
    rootlogger.handlers = []

    # Log to STDOUT
    if 'stdout' in logtargets_lower:
        # Get stdouthandler
        handler_stdout = logging.StreamHandler()
        # Set this handler to receive only events higher than 'loglevel'
        handler_stdout.setLevel(real_loglevel)

        # Get formatter for stdouthandler
        #formatstring_debug = "%(asctime)s %(name)s (%(module)s.py:%(lineno)s) %(levelname)s: %(message)s"
        formatstring_norm = "%(asctime)s %(name)s %(levelname)s: %(message)s"

        fmt_stdout = logging.Formatter(formatstring_norm)

        # Add formatter to stdouthandler
        handler_stdout.setFormatter(fmt_stdout)

        # Add handler to root logger.
        rootlogger.addHandler(handler_stdout)

    logging.getLogger("bootstrap_logging()").debug("Starting simple log system...")
    
    return rootlogger

