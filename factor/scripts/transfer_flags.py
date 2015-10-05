#! /usr/bin/env python
"""
Script to tranfer flags from one MS file to another
"""
import argparse
from argparse import RawTextHelpFormatter
import pyrap.tables as pt
import sys
import os
import numpy as np


def main(ms1, ms2):
    """
    Transfer flags

    Parameters
    ----------
    ms1 : str or list
        Name of MS file or list of files from which the flags will be taken
    ms2 : str or list
        Name of MS file or list of files to which the flags will be transferred

    """
    if type(ms1) is str:
        if '[' in ms1:
            ms1 = ms1.strip('[]').split(',')
            ms1 = [m.strip() for m in ms1]
        else:
            ms1 = [ms1]
    if type(ms2) is str:
        if '[' in ms2:
            ms2 = ms2.strip('[]').split(',')
            ms2 = [m.strip() for m in ms2]
        else:
            ms2 = [ms2]

    for ms_from in ms1:
        print('Reading flags from {}'.format(ms_from))
        t1 = pt.table(ms_from, readonly=True, ack=False)
        flags1 = t1.getcol('FLAG', nrow=1)

        numberofchans1 = np.shape(flags1)[1]
        chanperms = len(ms2)/numberofchans1

        starttime = t1[0]['TIME']
        endtime = t1[-1]['TIME']

        for ms_id, ms_to in enumerate(ms2):
            if os.path.isdir(ms_to):
                print('Transfering flags to {}'.format(ms_to))
                flagsin = t1.getcolslice('FLAG', [chanperms*ms_id, 0], [(chanperms*(ms_id+1))-1, 3])

                t2 = pt.table(ms_to, readonly=False, ack=False)
                flags2 = t2.getcol('FLAG')
                times2 = t2.getcol('TIME')
                time_indx1 = np.where(times2 >= starttime)[0][0]
                time_indx2 = np.where(times2 == endtime)[0][-1] + 1

                # Expand flags to match output MS and perform logical OR to pick
                # up original flags
                numberofchans2 = np.shape(flags2)[1]
                numbertorepeat = np.ceil(float(numberofchans2)/float(numberofchans1))
                flagsout = np.logical_or(np.repeat(flagsin, numbertorepeat, axis=1),
                    flags2[time_indx1:time_indx2])

                # Write updated flags
                t2.putcolslice('FLAG', flagsout, [0, 0], [numberofchans2-1, 3],
                    startrow=time_indx1, nrow=time_indx2-time_indx1)
                t2.flush()
                t2.close()
        t1.close()


if __name__ == '__main__':
    descriptiontext = "Transfer flags from ms1 to ms2.\n"

    parser = argparse.ArgumentParser(description=descriptiontext, formatter_class=RawTextHelpFormatter)
    parser.add_argument('ms1', help='name of MS file 1')
    parser.add_argument('ms2', help='name of MS file 2')
    args = parser.parse_args()

    main(args.ms1, args.ms2)





