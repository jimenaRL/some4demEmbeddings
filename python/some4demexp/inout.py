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

    print(f"Ideological embeddings loaded from folder {folder}.")

    ide_sources = pd.read_csv(os.path.join(folder, 'ide_sources.csv'))
    ide_targets = pd.read_csv(os.path.join(folder, 'ide_targets.csv'))

    return ide_sources, ide_targets


def save_ide_embeddings(sources_embeddings, targets_embeddings, folder):

    sources_embeddings.to_csv(
            os.path.join(folder, 'ide_sources.csv'),
            index=False)

    targets_embeddings.to_csv(
            os.path.join(folder, 'ide_targets.csv'),
            index=False)

    mssg = f"Ideological embeddings ({len(targets_embeddings)} targets and "
    mssg += f"{len(sources_embeddings)} sources) saved at folder {folder}."
    print(mssg)


def save_att_embeddings(att_source, att_targets, folder):

    att_source.to_csv(
        os.path.join(folder, 'att_sources.csv'), index=False)
    att_targets.to_csv(
        os.path.join(folder, 'att_targets.csv'), index=False)

    mssg = f"Attitudinal embeddings ({len(att_targets)} targets and "
    mssg += f"{len(att_source)} sources) saved at folder {folder}."
    print(mssg)


def load_att_embeddings(folder):

    print(f"Attitudinal embeddings load from folder {folder}.")

    att_source = pd.read_csv(os.path.join(folder, 'att_sources.csv'))
    att_targets = pd.read_csv(os.path.join(folder, 'att_targets.csv'))

    return att_source, att_targets


def save_experiment_data(
    X, targets_pids, sources_pids, sources_map_pids, folder):

    # graph
    np.savez(os.path.join(folder, "graph.npz"), X=X)
    # targets
    np.save(
        os.path.join(folder, "targets_pids.npy"),
        targets_pids,
        allow_pickle=True)
    pd.DataFrame(data=targets_pids,columns=['entity']) \
        .to_csv(os.path.join(folder, "targets_pids.csv"), index=False)
    # sources
    np.save(
        os.path.join(folder, "sources_pids.npy"),
        sources_pids,
        allow_pickle=True)
    pd.DataFrame(data=sources_pids,columns=['entity']) \
        .to_csv(os.path.join(folder, "sources_pids.csv"), index=False)
    # sources map pids
    np.save(
        os.path.join(folder, "sources_map_pids.npy"),
        sources_map_pids,
        allow_pickle=True)
    print(f"Social graph, pseudo ids and counts saved at {folder}.")


def load_experiment_data(folder):

    X = np.load(os.path.join(folder, "graph.npz"))['X']
    targets_pids = np.load(
        os.path.join(folder, "targets_pids.npy"),
        allow_pickle=True)
    sources_pids = np.load(
        os.path.join(folder, "sources_pids.npy"),
        allow_pickle=True)
    sources_map_pids = np.load(
        os.path.join(folder, "sources_map_pids.npy"),
        allow_pickle=True)

    return X, targets_pids, sources_pids, sources_map_pids
def load_pids(folder):

    targets_pids = np.load(
        os.path.join(folder, "targets_pids.npy"),
        allow_pickle=True).tolist()
    sources_pids = np.load(
        os.path.join(folder, "sources_pids.npy"),
        allow_pickle=True).tolist()

    return targets_pids, sources_pids

def set_output_folder(params, country, output="outputs"):

    emb_folder = f"min_followers_{params['sources_min_followers']}"
    emb_folder += f"_min_outdegree_{params['sources_min_outdegree']}"

    output_folder = os.path.join(output, country, emb_folder)

    os.makedirs(output_folder, exist_ok=True)

    config_file = os.path.join(output_folder, 'config.yaml')

    if not os.path.exists(config_file):
        with open(config_file, 'w') as file:
            yaml.dump(params, file)
        print(f"YAML config saved at {output_folder}.")

    return output_folder


def set_output_folder_emb(params, country, survey, output="outputs"):
    output_folder_emb = os.path.join(
        set_output_folder(params, country, output),
        f"ideN_{len(params['attitudinal_dimensions'][survey])-1}")
    os.makedirs(output_folder_emb, exist_ok=True)
    return output_folder_emb


def set_output_folder_att(params, survey, country, output="outputs"):
    output_folder_att = os.path.join(
        set_output_folder_emb(params, country, survey, output),
        f"attM_{len(params['attitudinal_dimensions'][survey])}",
        '_vs_'.join(params["attitudinal_dimensions"][survey]))
    os.makedirs(output_folder_att, exist_ok=True)
    return output_folder_att

def save_issues(folder, data, issue):
    filepath = os.path.join(folder, f'{issue}.csv')
    data.to_csv(filepath, index=False, encoding='utf8')
    print(f"Descriptions, issues and sentiments save at {filepath}.")

def load_issues(folder, issue):
    filepath = os.path.join(folder, f'{issue}.csv')
    print(f"Loading issues and sentiments from {filepath}.")
    return pd.read_csv(filepath, encoding='utf8', lineterminator='\n')

def save_descriptions(folder, data):
    filepath = os.path.join(folder, f'followers_with_descriptions.csv')
    data.to_csv(filepath, index=False, encoding='utf8')
    print(f"Followers with descriptions save at {filepath}.")

def load_descriptions(folder):
    filepath = os.path.join(folder, f'followers_with_descriptions.csv')
    print(f"Loading followers with descriptions from {filepath}.")
    return pd.read_csv(filepath, encoding='utf8', lineterminator='\n')

def save_issues_benckmarks(folder, benchmark):
    filepath = os.path.join(folder, f'benckmarks.csv')
    benchmark.to_csv(filepath, index=False)
    print(f"Saving benckmarks at {filepath}.")

def load_issues_benckmarks(folder):
    filepath = os.path.join(folder, f'benckmarks.csv')
    print(f"Loading benckmarks from {filepath}.")
    return pd.read_csv(filepath, encoding='utf8', lineterminator='\n')
