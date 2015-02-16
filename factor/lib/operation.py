"""
General operation library

Contains the master class for operations
"""
import os
import logging


class Operation(object):
    """
    Generic operation class.

    All operations should be in a separate module. Every module must have a
    class called in the same way of the module which inherits from this class.
    """
    def __init__(self, parset, bands, direction=None, reset=False, name=None):
        self.parset = parset.copy()
        self.bands = bands
        self.name = name
        self.parset['op_name'] = name
        self.direction = direction
        self.reset = reset
        self.exit_on_error = True
        self.log = logging.getLogger(self.name)

        if self.direction is not None:
            self.statebasename = 'state/{0}-{1}'.format(self.name, self.direction.name)
        else:
            self.statebasename = 'state/{0}'.format(self.name)

        self.mapbasename = 'datamaps/{0}/'.format(self.name)
        if not os.path.exists(self.mapbasename):
            os.makedirs(self.mapbasename)


    def setup(self):
        """
        Set up the operation
        """
        if self.direction is None:
            self.log.info('<-- Operation %s started.' % self.name)
        else:
            self.log.info('<-- Operation %s started (direction: %s).' % (self.name, self.direction.name))


    def make_datamap(self, data_list, prefix=None):
        """
        Returns the mapfile for the input data list
        """
        from factor.lib.datamap_lib import write_mapfile

        mapfile = write_mapfile(data_list, self.name, prefix=prefix,
            direction=self.direction)

        return mapfile


    def run(self):
        """
        Run the operation
        """
        raise(NotImplementedError)


    def finalize(self):
        """
        Finalize the operation
        """
        self.set_state(0)
        if self.direction is None:
            self.log.info('--> Operation %s terminated.' % self.name)
        else:
            self.log.info('--> Operation %s terminated (direction: %s).' % (self.name, self.direction.name))


    def set_state(self, returncode):
        success_file = self.statebasename + '.done'
        failure_file = self.statebasename + '.failed'
        if returncode == 0:
            state_file = success_file
            if os.path.exists(failure_file):
                os.remove(failure_file)
        else:
            state_file = failure_file
            if os.path.exists(success_file):
                os.remove(success_file)
        with open(state_file, 'w') as f:
            f.write(' ')
        if returncode != 0 and self.exit_on_error:
            import sys
            sys.exit(1)


    def unset_state(self):
        success_file = self.statebasename + '.done'
        failure_file = self.statebasename + '.failed'
        if os.path.exists(failure_file):
            os.remove(failure_file)
        if os.path.exists(success_file):
            os.remove(success_file)

