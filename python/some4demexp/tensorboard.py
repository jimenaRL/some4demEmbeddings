import os
import tensorflow as tf
from tensorboard.plugins import projector
import numpy as np
import pandas as pd


embeddings = pd.read_csv(
    '/home/jimena/Desktop/dataSprint/Nahel/media_mean_user_attitudinal_positions.csv')

logdir = '/home/jimena/Desktop/dataSprint/Nahel/tensorboardviz'


metadata_path = os.path.join(logdir, 'metadata.tsv')

embeddings[["media_label"]].to_csv(
    metadata_path, sep='\t', index=False, header=False)

# with open(metadata_path, 'w') as metadata_file:
#     metadata_file.write(f"group\tentity\tname\n")
#     for _, row in embeddings.iterrows():
#         if row.group == 'LFI':
#         metadata_file.write(f"{row.group}\t{row.entity}\t{row['name']}\n")

print(f"Metadata saves at {metadata_path}")

data = embeddings.drop(columns=["media_label"]) \
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
