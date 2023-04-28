import os
import tensorflow as tf
from tensorboard.plugins import projector
import numpy as np
import pandas as pd

from argparse import ArgumentParser

# parse arguments and set paths
ap = ArgumentParser()
ap.add_argument('--logdir', type=str, required=True)
ap.add_argument('--embeddings', type=str, required=True)
ap.add_argument('--users_limit', type=int, required=True)
args = ap.parse_args()
logdir = args.logdir
embeddings = args.embeddings
users_limit = args.users_limit

os.makedirs(logdir, exist_ok=True)

targets = pd.read_csv(os.path.join(embeddings, 'att_targets.csv'))
targets_names = pd.read_csv(os.path.join(embeddings, 'mps_metadata.csv'))

targets = targets.merge(
    targets_names,
    how="left",
    left_on="entity",
    right_on="mp_pseudo_id") \
    .drop(columns=["mp_pseudo_id"])

targets = targets[~targets.group.isna()]

sources = pd.read_csv(os.path.join(embeddings, 'att_source.csv'))
sources = sources.assign(name="follower")
sources = sources.assign(group="F")

# groups = pd.read_csv(os.path.join(embeddings, 'att_groups.csv'))
# groups = groups.assign(entity=groups.group).assign(group="PARTY")
# groups = groups.assign(name=groups.entity.apply(lambda e: e.lower()))

sources = sources.sample(n=users_limit, random_state=666)

embeddings = pd.concat([
    sources,
    targets,
    # groups
    ],
    axis=0)


metadata_path = os.path.join(logdir, 'metadata.tsv')

embeddings[["group", "name"]].to_csv(
    metadata_path, sep='\t', index=False)

# with open(metadata_path, 'w') as metadata_file:
#     metadata_file.write(f"group\tentity\tname\n")
#     for _, row in embeddings.iterrows():
#         if row.group == 'LFI':
#         metadata_file.write(f"{row.group}\t{row.entity}\t{row['name']}\n")

print(f"Metadata saves at {metadata_path}")

data = embeddings.drop(columns=["entity", "group", "name"]) \
    .to_numpy() \
    .astype(np.float32)

weights = tf.Variable(data)

# Create a checkpoint from embedding, the filename and key are the
# name of the tensor.
checkpoint = tf.train.Checkpoint(embedding=weights)
checkpoint.save(os.path.join(logdir, "embedding.ckpt"))

# Set up config.
config = projector.ProjectorConfig()
embedding = config.embeddings.add()

# The name of the tensor will be suffixed by `/.ATTRIBUTES/VARIABLE_VALUE`.
embedding.tensor_name = "embedding/.ATTRIBUTES/VARIABLE_VALUE"
embedding.metadata_path = 'metadata.tsv'
projector.visualize_embeddings(logdir, config)


print(f"tensorboard --bind_all --logdir {logdir}")
