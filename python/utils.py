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


def retrieveGraph(db, country, limit=-1):
    query = f"SELECT * FROM mps_followers_{country} LIMIT {int(limit)}"
    return retrieveSqlite(db, query)


def retrieveAndFormatTargetGroups(db, country):

    columns = ['mp_pseudo_id', 'party']

    table = f"mps_party_{country}"
    query = f"SELECT {','.join(columns)} FROM {table}"
    res = retrieveSqlite(db, query)

    dtypes = {'mp_pseudo_id': str, 'party': str}

    return pd.DataFrame(res, columns=columns) \
        .astype(dtypes) \
        .rename(columns={"party": "group"})


def retrieveAndFormatTargetGroupsCoord(db, country, dims_names):

    columns = ['party']+list(dims_names)

    table = f"parties_attitude_{country}"
    query = f"SELECT {','.join(columns)} FROM {table}"
    res = retrieveSqlite(db, query)

    dtypes = {'party': str}
    dtypes.update({d: np.float32 for d in dims_names})

    df = pd.DataFrame(res, columns=columns) \
        .astype(dtypes) \
        .rename(columns={"party": "group"}) \

    # /!\ /!\ /!\ /!\ /!\ /!\ /!\ HOTFIX  /!\/!\/!\/!\/!\/!\
    # ASSURE THIS IS DB CRATION
    df = df.dropna()

    return df


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


def visualize_ide(
    sources_coord_ide,
    targets_coord_ide,
    palette=None,
    path=None
):

    # plot sources embeddings
    g = sns.jointplot(
        data=sources_coord_ide.drop_duplicates(),
        x='latent_dimension_0',
        y='latent_dimension_1',
        kind="hex",
        height=6
    )

    # get unique groups and build color dictionary
    unique_groups = targets_coord_ide.group.unique().tolist()
    nunique_groups = targets_coord_ide.group.nunique()
    if palette is None:
        unique_groups.sort()
        palette = dict(zip(
            unique_groups,
            sns.color_palette("viridis", nunique_groups)
            )
        )

    # plot colored by groups target embeddings
    ax = g.ax_joint
    for p in unique_groups:
        sample = targets_coord_ide[targets_coord_ide.group == p] \
            .drop_duplicates()
        ax.scatter(
            sample['latent_dimension_0'],
            sample['latent_dimension_1'],
            marker='+',
            s=30,
            alpha=0.5,
            color=palette[p],
            label=p
        )
    plt.legend()

    if path:
        plt.savefig(path, dpi=150)


def visualize_att(
    sources_coord_att,
    targets_coord_att,
    groups_coord_att,
    dims,
    palette=None,
    path=None
):

    # plot sources embeddings
    g = sns.jointplot(
        data=sources_coord_att,
        x=dims['x'],
        y=dims['y'],
        kind="hex",
        height=6
    )

    # get unique groups and build color dictionary
    unique_groups = targets_coord_att.group.unique().tolist()
    nunique_groups = targets_coord_att.group.nunique()
    if palette is None:
        unique_groups.sort()
        palette = dict(zip(
            unique_groups,
            sns.color_palette("viridis", nunique_groups)
            )
        )

    ax = g.ax_joint

    # plot groups target

    for p in unique_groups:

        # plot colored by groups target embeddings
        sample = targets_coord_att[targets_coord_att.group == p] \
            .drop_duplicates()

        ax.scatter(
            sample[dims['x']],
            sample[dims['y']],
            marker='+',
            s=30,
            alpha=0.75,
            color=palette[p]
        )

        # plot estimated groups mean
        mean_group_estimated = sample[[dims['x'], dims['y']]].mean()
        ax.plot(
            mean_group_estimated[dims['x']],
            mean_group_estimated[dims['y']],
            marker='o',
            mec='k',
            color=palette[p],
            ms=7
        )

        # plot groups attitudinal_positions
        group_positions = groups_coord_att[groups_coord_att.group == p]
        if len(group_positions) > 1:
            raise ValueError("Bizarre")
        if len(group_positions) == 1:
            ax.plot(
                group_positions.iloc[0][dims['x']],
                group_positions.iloc[0][dims['y']],
                marker='^',
                mec='k',
                color=palette[p],
                ms=7,
                label=p
            )

        plt.legend()

    if path:
        plt.savefig(path, dpi=150)
