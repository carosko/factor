import os
import glob
from lofarpipe.support.data_map import DataMap
from lofarpipe.support.data_map import DataProduct


def plugin_main(args, **kwargs):
    """
    Updates the hosts in an input datamap

    Parameters
    ----------
    mapfile_in : str, optional
        Filename of datamap
    mapfile_dir: str, optional
        Directory containing mapfiles. All mapfiles in this directory will be
        updated
    hosts : str
        List of hosts/nodes. May be given as a list or as a string
        (e.g., '[host1, host2]'

    Returns
    -------
    result : dict
        Input datamap filename (first only if more than one)

    """
    if 'mapfile_dir' in kwargs:
        mapfiles_in = glob.glob(os.path.join(kwargs['mapfile_dir'], '*.mapfile'))
    else:
        mapfiles_in = [kwargs['mapfile_in']]

    if type(kwargs['hosts']) is str:
        hosts = kwargs['hosts'].strip('[]').split(',')
        hosts = [h.strip() for h in hosts]

    for mapfile_in in mapfiles_in:
        map = DataMap.load(mapfile_in)
        for i in range(len(map)-len(hosts)):
            hosts.append(hosts[i])

        for item, host in zip(map, hosts):
            item.host = host

        map.save(mapfile_in)
    result = {'mapfile': mapfiles_in[0]}

    return result
