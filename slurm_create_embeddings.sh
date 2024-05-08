#!/bin/sh

# SLURM options:

#SBATCH --job-name=some4dem_db_creation # Nom du jobe
#SBATCH --output=logs/%j.log   # Standard output et error log

#SBATCH --partition=gpu               # Choix de partition

#SBATCH --ntasks=1                    # Exécuter une seule tâche
#SBATCH --mem=32G                    # Mémoire en MB par défaut
#SBATCH --time=6-023:00             # Déli max

#SBATCH --mail-user=jimena.royoletelier@sciencespo.fr  # Où envoyer l'e-mail
#SBATCH --mail-type=BEGIN,END,FAIL          # Événements déclencheurs (NONE, BEGIN, END, FAIL, ALL) 

#SBATCH --gres=gpu:v100:1

COUNTRY="$2"
CONFIG="$1"

cd /sps/humanum/user/jroyolet/dev/some4demDB
source environments/some4demdbpy3.9/bin/activate
export HUGGINGFACE_HUB_CACHE=/sps/humanum/user/jroyolet/cache
export PYTHONIOENCODING=utf-8
export SOME4DEMDATA=/sps/humanum/user/jroyolet/data/some4dem

python3 pipeline.py --country=$COUNTRY --config=$CONFIG

