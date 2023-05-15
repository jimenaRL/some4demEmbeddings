import os
import yaml
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix


# def saveMpsMetadata(db, country, pids, path):
#     table = f"mps_annotations_{country}"
#     mps_pids = [f"'{pid}'" for pid in pids]
#     columns = ['mp_pseudo_id', 'name']
#     query = f"SELECT {','.join(columns)} FROM {table} "
#     query += f"WHERE mp_pseudo_id IN ({','.join(mps_pids)}) "
#     res = retrieveSqlite(db, query)
#     pd.DataFrame(res, columns=columns).astype(str).to_csv(path, index=False)
#     print(f"MPs meatadata saved at {path}.")


def load_ide_embeddings(folder):

    print(f"Ideological embeddings load from folder {folder}.")

    ide_sources = pd.read_csv(os.path.join(folder, 'ide_sources.csv'))
    ide_targets = pd.read_csv(os.path.join(folder, 'ide_targets.csv'))

    return ide_sources, ide_targets


def save_ide_embeddings(model, sources_ids, targets_ids, folder):

    model.ideological_embedding_source_latent_dimensions_ \
        .reset_index()\
        .drop(columns=["source_id"]) \
        .assign(entity=sources_ids) \
        .to_csv(
            os.path.join(folder, 'ide_sources.csv'),
            index=False)

    model.ideological_embedding_target_latent_dimensions_ \
        .reset_index()\
        .drop(columns=["target_id"]) \
        .assign(entity=targets_ids) \
        .to_csv(
            os.path.join(folder, 'ide_targets.csv'),
            index=False)

    print(f"Ideological embeddings saved at folder {folder}.")


def save_att_embeddings(att_source, att_targets, att_groups, folder):

    att_source.to_csv(
        os.path.join(folder, 'att_source.csv'), index=False)
    att_targets.to_csv(
        os.path.join(folder, 'att_targets.csv'), index=False)
    att_groups.to_csv(
        os.path.join(folder, 'att_groups.csv'), index=False)

    print(f"Attitudinal embeddings saved at folder {folder}.")


def load_att_embeddings(folder):

    print(f"Attitudinal embeddings load from folder {folder}.")

    att_source = pd.read_csv(os.path.join(folder, 'att_source.csv'))
    att_targets = pd.read_csv(os.path.join(folder, 'att_targets.csv'))
    att_groups = pd.read_csv(os.path.join(folder, 'att_groups.csv'))

    return att_source, att_targets, att_groups


def load_targets_groups(folder):

    return pd.read_csv(os.path.join(folder, 'targets_groups.csv'))


def save_experiment_data(X, targets_pids, sources_pids, folder):

    np.savez(os.path.join(folder, "graph.npz"), X=X)
    np.save(
        os.path.join(folder, "targets_pids.npy"),
        targets_pids,
        allow_pickle=True)
    np.save(
        os.path.join(folder, "sources_pids.npy"),
        sources_pids,
        allow_pickle=True)

    print(f"Social graph and pseudo ids saved at {folder}.")


def load_experiment_data(folder):

    X = np.load(os.path.join(folder, "graph.npz"))['X']
    targets_pids = np.load(
        os.path.join(folder, "targets_pids.npy"),
        allow_pickle=True)
    sources_pids = np.load(
        os.path.join(folder, "sources_pids.npy"),
        allow_pickle=True)

    return X, targets_pids, sources_pids


def set_output_folder(params, country, output):

    emb_folder = f"min_followers_{params['sources_min_followers']}"
    emb_folder += f"_min_outdegree_{params['sources_min_outdegree']}"

    output_folder = os.path.join(output, country, emb_folder)

    os.makedirs(output_folder, exist_ok=True)

    config_file = os.path.join(output_folder, 'config.yaml')
    with open(config_file, 'w') as file:
        yaml.dump(params, file)

    print(f"YAML config saved at {output_folder}.")

    return output_folder


def set_output_folder_emb(params, country, output):
    output_folder_emb = os.path.join(
        set_output_folder(params, country, output),
        f"ideN_{params['ideological_model']['n_latent_dimensions']}")
    os.makedirs(output_folder_emb, exist_ok=True)
    return output_folder_emb


def set_output_folder_att(folder, dims):

    folder = os.path.join(folder, '_vs_'.join(dims))
    os.makedirs(folder, exist_ok=True)

    return folder


def save_targets_groups(targets_groups, folder):

    file = os.path.join(folder, "targets_groups.csv")
    targets_groups.to_csv(file, index=False)
    print(f"Target groups saved at {file}.")

