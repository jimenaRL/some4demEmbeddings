#!/bin/bash

users_limit=1

experiment="france_ideN_2_sources_min_followers_25_sources_min_outdegree_3"
embeddings="embeddings/$experiment"
logdir="logs/$experiment"

python viz_ideological.py --embeddings=$embeddings --logdir=$logdir --users_limit=$users_limit
tensorboard --bind_all --port 6006 --logdir $logdir &


att1="ches2019_enviro_salience"
att2="ches2019_eu_position"
experiment="${att1}_vs_$att2"

embeddings="$embeddings/$experiment"
logdir="$logdir/$experiment"
python viz_attitudinal.py --embeddings=$embeddings --logdir=$logdir --users_limit=$users_limit
tensorboard --bind_all --port 6007 --logdir $logdir &


