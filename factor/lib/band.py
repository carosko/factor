"""
Definition of the band class
"""
import logging
import pyrap.tables as pt
import numpy as np

log = logging.getLogger('parset')

class Band(object):
    """
    The Band object contains parameters needed for each band (MS)
    """
    def __init__(self, MSfile):
        """
        Create Band object

        Parameters
        ----------
        MSfile : str
            Filename of MS

        """
        self.file = MSfile
        self.msname = self.file.split('/')[-1]

        sw = pt.table(self.file+'::SPECTRAL_WINDOW', ack=False)
        self.freq = sw.col('REF_FREQUENCY')[0]
        sw.close()

        obs = pt.table(self.file+'::FIELD', ack=False)
        self.ra = np.degrees(float(obs.col('REFERENCE_DIR')[0][0][0]))
        if self.ra < 0.:
            self.ra = 360.0 + (self.ra)
        self.dec = np.degrees(float(obs.col('REFERENCE_DIR')[0][0][1]))
        obs.close()

        ant = pt.table(self.file+'::ANTENNA', ack=False)
        diam = float(ant.col('DISH_DIAMETER')[0])
        ant.close()

        self.fwhm_deg = 1.1 * ((3.0e8 / self.freq) / diam) * 180. / np.pi
        self.name = 'Band_{0:.2f}MHz'.format(self.freq/1e6)

        # Check for SUBTRACTED_DATA_ALL column
        tab = pt.table(self.file, ack=False)
        if 'SUBTRACTED_DATA_ALL' in tab.colnames():
            self.has_sub_data = True
        else:
            self.has_sub_data = False
        self.has_sub_data_new = False
        self.starttime = tab[0]['TIME']
        self.endtime = tab[-1]['TIME']
        for t2 in tab.iter(["ANTENNA1","ANTENNA2"]):
            if (t2.getcell('ANTENNA1',0)) < (t2.getcell('ANTENNA2',0)):
                self.timepersample = t2[1]['TIME'] - t2[0]['TIME']
                self.nsamples = t2.nrows()
                break
        tab.close()
