import os
import sqlite3

import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix


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


def retrieveGraph(db, country, valid_followers, limit=-1):
    table = f"mps_followers_{country}"
    columns = ['mp_pseudo_id', 'follower_pseudo_id']
    valid_followers = [f"'{vf}'" for vf in valid_followers]
    query = f"SELECT {','.join(columns)} FROM {table} "
    query += f"WHERE follower_pseudo_id IN ({','.join(valid_followers)}) "
    # query += f"ORDER BY RANDOM() LIMIT {int(limit)}"
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


def save_embeddings(embeddings, output_folder):

    os.makedirs(output_folder, exist_ok=True)

    for name, df in embeddings.items():
        df.to_csv(os.path.join(output_folder, f"{name}.csv"), index=False)

    print(f"Embeddings saved at {output_folder}.")
