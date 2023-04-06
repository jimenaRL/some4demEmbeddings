import os
import sqlite3

import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix

import seaborn as sns
import matplotlib.pyplot as plt


def retrieveSqlite(db, query):

    if not os.path.exists(db):
        raise FileNotFoundError(f"Unnable to find database: '{db}'.")

    with sqlite3.connect(db) as con:
        print(f"Quering sqlite database at {db} with `{query}`... ",  end='')
        cur = con.cursor()
        cur.execute(query)
        res = cur.fetchall()
        print("done.")

    return res


def retrieveFollowersMpsGraph(db, country, limit=-1):
    query = f"SELECT * FROM mps_followers_{country} LIMIT {int(limit)}"
    return retrieveSqlite(db, query)


def retrieveMpsParties(db, country):
    query = f"SELECT mp_pseudo_id, party FROM mps_party_{country}"
    return retrieveSqlite(db, query)


def graphToAdjencyMatrix(res, sparce=False):
    """
    # Format data from sqlite graph res and build (sparse) matrix
    """
    sources = [r[1] for r in res]
    targets = [r[0] for r in res]

    n_i, rows_id = pd.factorize(targets)
    n_j, columns_id = pd.factorize(sources)
    n_in_j, tups = pd.factorize(list(zip(n_j, n_i)))

    ntwrk_csr = csr_matrix((np.bincount(n_in_j), tuple(zip(*tups))))

    mssg = f"Found {len(res)} links, from {len(columns_id)} unique sources "
    mssg += f"to {len(rows_id)} unique targets."
    print(mssg)

    if sparce:
        return ntwrk_csr, rows_id, columns_id

    return ntwrk_csr.toarray(), rows_id, columns_id


def getTargetGroups(res):
    return pd.DataFrame({
        "mp_pseudo_id": [r[0] for r in res],
        "party": [r[1] for r in res],
        })


def visualize(
    sources_coords_ide,
    targets_coords_ide,
    targets_ids,
    sources_ids,
    targets_groups,
    palette=None
):

    # plot sources embeddings
    g = sns.jointplot(
        data=sources_coords_ide.drop_duplicates(),
        x='latent_dimension_0',
        y='latent_dimension_1',
        kind="hex"
    )

    targets_coords_ide = targets_coords_ide.assign(target_pid=targets_ids)

    # plot targets embeddings
    targets_coords_ide = targets_coords_ide.merge(
            targets_groups,
            left_on="target_pid",
            right_on="mp_pseudo_id",
            how="inner"
        ) \
        .drop(columns="mp_pseudo_id")

    unique_parties = targets_coords_ide.party.unique().tolist()
    nunique_parties = targets_coords_ide.party.nunique()
    if palette is None:
        palette = sns.color_palette("viridis", nunique_parties)
    unique_parties.sort()
    palette_dict = dict(zip(unique_parties, palette))

    ax = g.ax_joint
    for p in unique_parties:
        sample = targets_coords_ide[targets_coords_ide.party == p] \
            .drop_duplicates()
        ax.scatter(
            sample['latent_dimension_0'],
            sample['latent_dimension_1'],
            marker='+',
            s=30,
            alpha=0.5,
            color=palette_dict[p]
        )

    plt.show()
