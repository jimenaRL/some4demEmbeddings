import os
import sqlite3

import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix


def retrieveSqlite(db, query):

    if not os.path.exists(db):
        raise FileNotFoundError(f"Unnable to find database: '{db}'.")

    with sqlite3.connect(db) as con:
        print(
            f"Quering sqlite database at {db} with `{query[:100]}`... ",  end='')
        cur = con.cursor()
        cur.execute(query)
        res = cur.fetchall()
        print("done.")

    return res


def retrieveGraph(db, country, valid_followers, limit=-1):
    table = f"mps_followers_{country}"
    columns = ['mp_pseudo_id', 'follower_pseudo_id']
    valid_followers = [f"'{vf}'" for vf in valid_followers]
    query = f"SELECT {','.join(columns)} FROM {table} "
    query += f"WHERE follower_pseudo_id IN ({','.join(valid_followers)}) "
    query += f"ORDER BY RANDOM() LIMIT {int(limit)}"
    return retrieveSqlite(db, query)


def retrieveAndFormatUsersMetadata(db, country):
    table = f"users_metadata_{country}"
    columns = ['pseudo_id', 'followers']
    query = f"SELECT {','.join(columns)} FROM {table}"
    res = retrieveSqlite(db, query)
    dtypes = {'pseudo_id': str, 'followers': float}
    return pd.DataFrame(res, columns=columns) \
        .astype(dtypes) \
        .rename(columns={"followers": "nb_followers"})


def retrieveAndFormatPartiesMapping(db, country):

    columns = ['parliamentary_group', 'ches2019_party']

    table = f"parties_mapping_{country}"
    query = f"SELECT {','.join(columns)} FROM {table}"
    res = retrieveSqlite(db, query)

    dtypes = {'parliamentary_group': str, 'ches2019_party': str}

    return pd.DataFrame(res, columns=columns) \
        .astype(dtypes)


def retrieveAndFormatTargetGroups(db, country, parties_mapping):

    columns = ['mp_pseudo_id', 'parliamentary_group']

    table = f"mps_party_{country}"
    query = f"SELECT {','.join(columns)} FROM {table}"
    res = retrieveSqlite(db, query)

    dtypes = {'mp_pseudo_id': str, 'parliamentary_group': str}

    targets_groups = pd.DataFrame(res, columns=columns).astype(dtypes)

    g0 = len(targets_groups)
    targets_groups = targets_groups \
        .merge(parties_mapping) \
        .drop('parliamentary_group', axis=1) \
        .rename(columns={'ches2019_party': 'group'})
    g1 = len(targets_groups)
    if g0 > g1:
        print(
            f"Dropped {g0 - g1} targets with no group in mapping.")

    return targets_groups


def retrieveAndFormatTargetGroupsCoord(db, country, dims_names):

    columns = ['party']+list(dims_names)

    table = f"parties_attitude_{country}"
    query = f"SELECT {','.join(columns)} FROM {table}"
    res = retrieveSqlite(db, query)

    dtypes = {'party': str}
    dtypes.update({d: np.float32 for d in dims_names})

    df = pd.DataFrame(res, columns=columns) \
        .astype(dtypes) \
        .rename(columns={'party': 'group'})

    # /!\ /!\ /!\ /!\ /!\ /!\ /!\ HOTFIX  /!\/!\/!\/!\/!\/!\
    # ASSURE THIS IS DB CRATION
    df = df.dropna()

    return df


def graphToAdjencyMatrix(res, min_outdegree, sparce=False):
    """
    # Format data from sqlite graph res and build (sparse) matrix
    """
    sources = [r[1] for r in res]
    targets = [r[0] for r in res]

    # create sparse matrix
    n_i, rows_id = pd.factorize(targets)
    n_j, columns_id = pd.factorize(sources)
    n_in_j, tups = pd.factorize(list(zip(n_j, n_i)))

    ntwrk_csr = csr_matrix((np.bincount(n_in_j), tuple(zip(*tups))))

    # remove sources with too low out degree
    out_degrees_j = ntwrk_csr.sum(axis=1)
    idx_valid_j = np.argwhere(out_degrees_j >= min_outdegree)[:, 0]
    j0 = ntwrk_csr.shape[0]
    ntwrk_csr = ntwrk_csr[idx_valid_j, :]
    j1 = ntwrk_csr.shape[0]
    columns_id = columns_id[idx_valid_j]

    assert ntwrk_csr.shape == (len(columns_id), len(rows_id))
    mssg = f"Drop {j0 - j1} of {j0} sources ({100*(j0 - j1)/j0:.2f}%) "
    mssg += f"with outdegree less than {min_outdegree}, keeped {j1}."
    print(mssg)

    # remove repeated sources (rows)
    _, idx_valid_j = np.unique(ntwrk_csr.toarray(), axis=0, return_index=True)
    ja = ntwrk_csr.shape[0]
    ntwrk_csr = ntwrk_csr[idx_valid_j, :]
    jb = ntwrk_csr.shape[0]
    columns_id = columns_id[idx_valid_j]

    assert ntwrk_csr.shape == (len(columns_id), len(rows_id))
    mssg = f"Drop {ja - jb} of {ja} repeated sources "
    mssg += f"({100*(ja - jb)/ja:.2f}%), keeped {jb}."
    print(mssg)

    mssg = f"Found {ntwrk_csr.nnz} links, from {len(columns_id)} unique sources "
    mssg += f"to {len(rows_id)} unique targets."
    print(mssg)

    if sparce:
        return ntwrk_csr, rows_id, columns_id

    return ntwrk_csr.toarray(), rows_id, columns_id


def save_embeddings(embeddings, ide_output_folder, att_output_folder):

    os.makedirs(ide_output_folder, exist_ok=True)
    os.makedirs(att_output_folder, exist_ok=True)

    for name, df in embeddings.items():
        folder = ide_output_folder if name[-3:] == 'ide' else att_output_folder
        df.to_csv(os.path.join(folder, f"{name}.csv"), index=False)

    print(f"Ideological embeddings saved at folder {ide_output_folder}.")
    print(f"Attitudinal embeddings saved at folder {att_output_folder}.")
