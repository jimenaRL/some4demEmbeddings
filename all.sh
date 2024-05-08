#!/bin/bash

sbatch slurm_create_embeddings.sh configs/embeddings.yaml gps2019 tmp argentina
sbatch slurm_create_embeddings.sh configs/embeddings.yaml gps2019 tmp australia
sbatch slurm_create_embeddings.sh configs/embeddings.yaml ches2019,gps2019,ches2023 tmp austria
sbatch slurm_create_embeddings.sh configs/embeddings.yaml ches2019,gps2019,ches2023 tmp belgium
sbatch slurm_create_embeddings.sh configs/embeddings.yaml gps2019 tmp canada
sbatch slurm_create_embeddings.sh configs/embeddings.yaml gps2019 tmp chile
sbatch slurm_create_embeddings.sh configs/embeddings.yaml gps2019 tmp colombia
sbatch slurm_create_embeddings.sh configs/embeddings.yaml ches2019,gps2019,ches2023 tmp croatia
sbatch slurm_create_embeddings.sh configs/embeddings.yaml ches2019,gps2019 tmp cyprus
sbatch slurm_create_embeddings.sh configs/embeddings.yaml ches2019,gps2019,ches2023 tmp czechia
sbatch slurm_create_embeddings.sh configs/embeddings.yaml ches2019,gps2019,ches2023 tmp denmark
sbatch slurm_create_embeddings.sh configs/embeddings.yaml gps2019 tmp ecuador
sbatch slurm_create_embeddings.sh configs/embeddings.yaml ches2019,gps2019,ches2023 tmp estonia
sbatch slurm_create_embeddings.sh configs/embeddings.yaml ches2019,gps2019,ches2023 tmp finland
sbatch slurm_create_embeddings.sh configs/embeddings.yaml ches2019,gps2019,ches2023 tmp france
sbatch slurm_create_embeddings.sh configs/embeddings.yaml ches2019,gps2019,ches2023 tmp germany
sbatch slurm_create_embeddings.sh configs/embeddings.yaml ches2019,gps2019,ches2023 tmp greece
sbatch slurm_create_embeddings.sh configs/embeddings.yaml ches2019,gps2019,ches2023 tmp hungary
sbatch slurm_create_embeddings.sh configs/embeddings.yaml ches2019,gps2019,ches2023 tmp iceland
sbatch slurm_create_embeddings.sh configs/embeddings.yaml gps2019 tmp india
sbatch slurm_create_embeddings.sh configs/embeddings.yaml ches2019,gps2019,ches2023 tmp ireland
sbatch slurm_create_embeddings.sh configs/embeddings.yaml gps2019 tmp israel
sbatch slurm_create_embeddings.sh configs/embeddings.yaml ches2019,gps2019,ches2023 tmp italy
sbatch slurm_create_embeddings.sh configs/embeddings.yaml gps2019 tmp japan
sbatch slurm_create_embeddings.sh configs/embeddings.yaml ches2019,gps2019,ches2023 tmp latvia
sbatch slurm_create_embeddings.sh configs/embeddings.yaml ches2019,gps2019,ches2023 tmp lithuania
sbatch slurm_create_embeddings.sh configs/embeddings.yaml ches2019,gps2019 tmp luxembourg
sbatch slurm_create_embeddings.sh configs/embeddings.yaml ches2019,gps2019,ches2023 tmp malta
sbatch slurm_create_embeddings.sh configs/embeddings.yaml gps2019 tmp mexico
sbatch slurm_create_embeddings.sh configs/embeddings.yaml ches2019,gps2019,ches2023 tmp netherlands
sbatch slurm_create_embeddings.sh configs/embeddings.yaml gps2019 tmp newzealand
sbatch slurm_create_embeddings.sh configs/embeddings.yaml gps2019 tmp nigeria
sbatch slurm_create_embeddings.sh configs/embeddings.yaml ches2019,gps2019,ches2023 tmp norway
sbatch slurm_create_embeddings.sh configs/embeddings.yaml gps2019 tmp peru
sbatch slurm_create_embeddings.sh configs/embeddings.yaml ches2019,gps2019,ches2023 tmp poland
sbatch slurm_create_embeddings.sh configs/embeddings.yaml ches2019,gps2019,ches2023 tmp portugal
sbatch slurm_create_embeddings.sh configs/embeddings.yaml ches2019,gps2019,ches2023 tmp romania
sbatch slurm_create_embeddings.sh configs/embeddings.yaml gps2019 tmp serbia
sbatch slurm_create_embeddings.sh configs/embeddings.yaml ches2019,gps2019,ches2023 tmp slovakia
sbatch slurm_create_embeddings.sh configs/embeddings.yaml ches2019,gps2019,ches2023 tmp slovenia
sbatch slurm_create_embeddings.sh configs/embeddings.yaml gps2019 tmp southafrica
sbatch slurm_create_embeddings.sh configs/embeddings.yaml ches2019,gps2019,ches2023 tmp spain
sbatch slurm_create_embeddings.sh configs/embeddings.yaml ches2019,gps2019,ches2023 tmp sweden
sbatch slurm_create_embeddings.sh configs/embeddings.yaml ches2019,gps2019,ches2023 tmp switzerland
sbatch slurm_create_embeddings.sh configs/embeddings.yaml ches2019,gps2019,ches2023 tmp uk
sbatch slurm_create_embeddings.sh configs/embeddings.yaml gps2019 tmp ukraine
sbatch slurm_create_embeddings.sh configs/embeddings.yaml gps2019 tmp uruguay
sbatch slurm_create_embeddings.sh configs/embeddings.yaml gps2019 tmp venezuela

sbatch slurm_create_embeddings_512G.sh configs/embeddings.yaml gps2019 tmp brazil
sbatch slurm_create_embeddings_512G.sh configs/embeddings.yaml gps2019 tmp turkey
sbatch slurm_create_embeddings_512G.sh configs/embeddings.yaml gps2019 tmp us

sbatch slurm_create_embeddings.sh configs/embeddings.yaml _ tmp eu

