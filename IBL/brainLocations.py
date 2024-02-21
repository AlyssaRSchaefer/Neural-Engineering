import numpy as np
import matplotlib.pyplot as plt
from iblatlas.regions import BrainRegions

from one.api import ONE
ONE.setup(silent=True)
one = ONE(password='international')

eid = one.search(project='brainwide')[23]

#load in channel cluster dataset from eid
cluster_chans = one.load_dataset('05ccc92c-fcb0-4e92-84d3-de033890c7a8', 'clusters.channels.npy', collection=f'alf/probe00/pykilosort')

aligned_traj = one.alyx.rest('trajectories', 'list', session=eid,
                             probe='probe00', provenance='Ephys aligned histology track')
if len(aligned_traj) > 0:
    print('Getting channels for provenance ' + aligned_traj[0]['provenance'])

    channels = one.alyx.rest('channels', 'list', trajectory_estimate=aligned_traj[0]['id'])

    chans = {'atlas_id': np.array([ch['brain_region'] for ch in channels]),
             'x': np.array([ch['x'] for ch in channels]) / 1e6,
             'y': np.array([ch['y'] for ch in channels]) / 1e6,
             'z': np.array([ch['z'] for ch in channels]) / 1e6,
             'axial_um': np.array([ch['axial'] for ch in channels]),
             'lateral_um': np.array([ch['lateral'] for ch in channels])}

else:
    histology_traj = one.alyx.rest('trajectories', 'list', session=eid,
                                   probe='probe00', provenance='Histology track')
    if len(histology_traj) > 0:
        print('Getting channels for provenance ' + histology_traj[0]['provenance'])

        channels = one.alyx.rest('channels', 'list', trajectory_estimate=histology_traj[0]['id'])

        chans = {'atlas_id': np.array([ch['brain_region'] for ch in channels]),
                 'x': np.array([ch['x'] for ch in channels]) / 1e6,
                 'y': np.array([ch['y'] for ch in channels]) / 1e6,
                 'z': np.array([ch['z'] for ch in channels]) / 1e6,
                 'axial_um': np.array([ch['axial'] for ch in channels]),
                 'lateral_um': np.array([ch['lateral'] for ch in channels])}

if chans is not None:
    r = BrainRegions()
    chans['acronym'] = r.get(ids=chans['atlas_id']).acronym
    chans['rgb'] = r.get(ids=chans['atlas_id']).rgb
    cluster_brain_region = chans['acronym'][cluster_channels]
    cluster_colour = chans['rgb'][cluster_channels]
    cluster_xyz = np.c_[chans['x'], chans['y'], chans['z']][cluster_channels]
    regions, idx, n_clust = np.unique(cluster_brain_region, return_counts=True, return_index=True)

    region_cols = cluster_colour[idx, :]
    fig, ax = plt.subplots()
    ax.bar(x=np.arange(len(regions)), height=n_clust, tick_label=regions, color=region_cols / 255)
    ax.set_xlabel('Brain region acronym')
    ax.set_ylabel('No. of clusters')
    plt.show()