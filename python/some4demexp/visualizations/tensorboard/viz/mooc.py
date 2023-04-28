import os
import tensorflow as tf
from tensorboard.plugins import projector
import numpy as np

# Set up a logs directory, so Tensorboard knows where to look for files.
log_dir = 'logs/mooc/'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

with open(os.path.join(log_dir, 'metadata.tsv'), 'w') as metadata_file:
    for _ in range(8184):
        metadata_file.write('%d\n' % np.random.randint(10))

data = np.random.randint(100, size=(8184, 3)).astype(np.float32)

weights = tf.Variable(data)
# Create a checkpoint from embedding, the filename and key are the
# name of the tensor.
checkpoint = tf.train.Checkpoint(embedding=weights)
checkpoint.save(os.path.join(log_dir, "embedding.ckpt"))

# Set up config.
config = projector.ProjectorConfig()
embedding = config.embeddings.add()
# The name of the tensor will be suffixed by `/.ATTRIBUTES/VARIABLE_VALUE`.
embedding.tensor_name = "embedding/.ATTRIBUTES/VARIABLE_VALUE"
embedding.metadata_path = 'metadata.tsv'
projector.visualize_embeddings(log_dir, config)

print("tensorboard --bind_all --logdir /viz/logs/some4dem/")
