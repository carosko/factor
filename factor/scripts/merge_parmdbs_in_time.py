#!/usr/bin/env python
"""
Script to merge parmdbs in time
"""
import argparse
from argparse import RawTextHelpFormatter
import os
import casacore.tables as pt
import lofar.parmdb as pdb
import sys
import numpy as np


def main(input_mslist, parmdb_name, outparmdb, clobber=True):
    """
    Merges parmdbs in time into a single parmdb

    The parmdbs are assumed to be located in the input MS with name
    parmdb_name

    Parameters
    ----------
    input_mslist : list
        List of input MS file names
    parmdb_name : str
        Name of parmdb (relative to MS files)
    outparmdb : str
        Name of output merged parmdb
    clobber : bool, optional
        If True, overwrite existing output file

    """
    if type(input_mslist) is str:
        input_mslist = input_mslist.strip('[]').split(',')
        input_mslist = [f.strip() for f in input_mslist]
    inparmdbs = [os.path.join(ms, parmdb_name) for ms in input_mslist]

    # Sort the parmdbs by start time (needed for the timewidth checks below)
    if len(inparmdbs) > 1:
        start_times = []
        start_times_dicts = [{} for i in range(len(inparmdbs))]
        for i, inparmdb in enumerate(inparmdbs):
            pdb_in = pdb.parmdb(inparmdb)
            for j, parmname in enumerate(pdb_in.getNames()):
                parms = pdb_in.getValuesGrid(parmname)
                if j == 0:
                    start_times.append(parms[parmname]['times'][0])
                start_times_dicts[i].update({parmname: parms[parmname]['times'][0]})
            pdb_in = False
    inparmdbs = np.array(inparmdbs)[np.argsort(start_times)].tolist()
    start_times_dicts = np.array(start_times_dicts)[np.argsort(start_times)].tolist()
    start_times.sort()

    if type(clobber) is str:
        if clobber.lower() == 'true':
            clobber = True
        else:
            clobber = False

    if os.path.exists(outparmdb):
        if clobber:
            os.system('rm -rf {0}'.format(outparmdb))
        else:
            return
    pdb_concat = pdb.parmdb(outparmdb, create=True)

    for i, inparmdb in enumerate(inparmdbs):
        pdb_add = pdb.parmdb(inparmdb)
        parms = pdb_add.getValuesGrid('*')
        for parmname in pdb_add.getNames():
            # Adjust last timewidth if necessary, as DPPP GainCal (as of 2.16.4) does not
            # truncate last solution timewidth to end of MS
            if i < len(inparmdbs) - 1:
                inter_chunk_timewidth = start_times_dicts[i+1][parmname] - parms[parmname]['times'][-1]
                if inter_chunk_timewidth < parms[parmname]['timewidths'][-1]:
                    parms[parmname]['timewidths'][-1] = inter_chunk_timewidth

                    # Adjust following chunk as well
                    pdb_next = pdb.parmdb(inparmdbs[i+1])
                    parms_next = pdb_next.getValuesGrid(parmname)
                    parms_next[parmname]['timewidths'][0] = inter_chunk_timewidth
                    pdb_next.deleteValues(parmname)
                    pdb_next.addValues(parmname, parms_next[parmname])
                    pdb_next.flush()
                    pdb_next = False

            ValueHolder = pdb_concat.makeValue(values=parms[parmname]['values'],
                                               sfreq=parms[parmname]['freqs'],
                                               efreq=parms[parmname]['freqwidths'],
                                               stime=parms[parmname]['times'],
                                               etime=parms[parmname]['timewidths'],
                                               asStartEnd=False)
            pdb_concat.addValues(parmname, ValueHolder)
        pdb_concat.flush()
        pdb_add = False
    pdb_concat = False


if __name__ == '__main__':
    descriptiontext = "Merge parmdbs in time.\n"

    parser = argparse.ArgumentParser(description=descriptiontext, formatter_class=RawTextHelpFormatter)
    parser.add_argument('mslist', help='list of ms with parmdbs to merge')
    parser.add_argument('parmdb_name', help='name of parmdbs to merge')
    parser.add_argument('outparmdb', help='output parmdb')
    parser.add_argument('-c', '--clobber', help='clobber existing file?', type=bool, default=True)

    args = parser.parse_args()
    main(args.mslist, args.parmdb_name, args.outparmdb, clobber=args.clobber)
