import os
import yaml
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix


def graphToAdjencyMatrix(res, min_outdegree, sparce=False):
    """
    # Format data from sqlite graph res and build (sparse) matrix
    """

    print(f"Building adjency matrix... ")

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

    # remove and keep repeated sources (rows)

    _, idx_valid_j, repeated_rows_counts = np.unique(
        ntwrk_csr.toarray(),
        axis=0,
        return_index=True,
        return_counts=True
    )
    ja = ntwrk_csr.shape[0]
    ntwrk_csr = ntwrk_csr[idx_valid_j, :]
    jb = ntwrk_csr.shape[0]
    columns_id = columns_id[idx_valid_j]

    assert ntwrk_csr.shape == (len(columns_id), len(rows_id))
    mssg = f"Drop {ja - jb} repeated sources "
    mssg += f"({100*(ja - jb)/ja:.2f}%), keeped {jb}."
    print(mssg)

    # remove targets (columns) with no source associated
    idx_valid_i = np.argwhere((np.abs(ntwrk_csr).sum(axis=0) != 0).tolist()[0])[:, 0]

    ia = ntwrk_csr.shape[1]
    ntwrk_csr = ntwrk_csr[:, idx_valid_i]
    ib = ntwrk_csr.shape[1]
    rows_id = rows_id[idx_valid_i]

    assert ntwrk_csr.shape == (len(columns_id), len(rows_id))
    mssg = f"Drop {ia - ib} targets with no sources associated "
    mssg += f"({100*(ia - ib)/ia:.2f}%), keeped {ib}."

    # checking if final network is bipartite:
    nb_shared = len(np.intersect1d(rows_id, columns_id))
    if not nb_shared == 0:
        raise ValueError(
            f"Created graph is not bipartited, found {nb_shared} common nodes.")

    mssg1 = f"Found {ntwrk_csr.nnz} links, from {len(columns_id)} unique sources "
    mssg1 += f"to {len(rows_id)} unique targets."

    if sparce:
        return ntwrk_csr, rows_id, columns_id

    print("done.")
    print(mssg)
    print(mssg1)

    return ntwrk_csr.toarray(), rows_id, columns_id, repeated_rows_counts
