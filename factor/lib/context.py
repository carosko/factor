"""
Definition of context managers (with statements) used for operations
"""
import time
import logging

class Timer():
    """
    Context manager used to time operations
    """
    def __init__(self, log=None):
        """
        Create Direction object

        Parameters
        ----------
        log : logging instance
            The logging instance to use. If None, root is used
        """
        if log is None:
            self.log = logging
        else:
            self.log = log


    def __enter__(self):
        self.start = time.time()


    def __exit__(self, type, value, tb):
        if type is not None:
            raise type, value, tb

        elapsed = (time.time() - self.start)
        self.log.debug('Time for operation: %i sec' % (elapsed))

