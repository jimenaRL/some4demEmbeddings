import yaml
import pandas as pd
from argparse import ArgumentParser

from some4demexp.inout import \
    set_output_folder, \
    set_output_folder_att, \
    load_att_embeddings, \
    load_issues_descriptions, \
    save_issues_benckmarks, \
    set_output_folder_emb, \
    load_ide_embeddings

from corg import \
    BenchmarkDimension, \
    DiscoverDimension

from some4demexp.conf import \
    CHESLIMS, \
    ATTDICT

# parse arguments and set paths
ap = ArgumentParser()
ap.add_argument('--config', type=str, required=True)
ap.add_argument('--country', type=str, required=True)
ap.add_argument('--output', type=str, required=True)
args = ap.parse_args()
config = args.config
country = args.country
output = args.output


with open(config, "r", encoding='utf-8') as fh:
    params = yaml.load(fh, Loader=yaml.SafeLoader)
print(yaml.dump(params, default_flow_style=False))

ATTDIMS = params['attitudinal_dimensions']
IDEDIMS = range(params['ideological_model']['n_latent_dimensions'])

# (0) Get embeddings and descriptions
folder = set_output_folder(params, country, output)

ide_folder = set_output_folder_emb(params, country, output)
ide_sources, _ = load_ide_embeddings(ide_folder)

att_folder = set_output_folder_att(params, country, output)
att_sources, _ = load_att_embeddings(att_folder)

benchmark_records = []
discover_records = []

for issue in ['Left-Right', 'Elites-People-Politicians-StartUp-Entrepreneur']:
    for attdim in ATTDIMS:

        data = load_issues_descriptions(folder, issue) \
            .merge(att_sources, on='entity', how='inner') \
            .merge(ide_sources, on='entity', how='inner') \


        # (1) Measure accuracy of estimated positions
        Y = data[['entity', 'label']]

        # (1.1) Benchmark attitudinal dimension
        mb = BenchmarkDimension()
        Xb = data[['entity', attdim]]
        mb.fit(Xb, Y)

        benchmark_records.append({
            'embedding': 'attitudinal',
            'dimension': attdim,
            'issue': issue,
            # 'beta0': mb.beta0_,
            # 'beta1': mb.beta1_,
            'precision_train_': mb.precision_train_,
            'recall_train_': mb.recall_train_,
            'f1_score_train_': mb.f1_score_train_,
        })

        for idedim in IDEDIMS:
            mb = BenchmarkDimension()
            Xb = data[['entity', f'latent_dimension_{idedim}']]
            mb.fit(Xb, Y)

            benchmark_records.append({
                'embedding': 'ideological',
                'dimension': idedim,
                'issue': issue,
                # 'beta0': mb.beta0_,
                # 'beta1': mb.beta1_,
                'precision_train_': mb.precision_train_,
                'recall_train_': mb.recall_train_,
                'f1_score_train_': mb.f1_score_train_,
            })



        # (1.2) Discover Dimension

        # # ideological embedding
        # md = DiscoverDimension()
        # Xd = data[['entity']+[f'latent_dimension_{idedim}' for idedim in IDEDIMS]]
        # md.fit(Xd, Y)

        # discover_records.append({
        #     'embedding': 'ideological',
        #     'issue': issue,
        #     'model_decision_boundary_': md.model_decision_boundary_,
        #     'beta1': md.decision_hyperplane_unit_normal,
        #     'precision_train_': md.precision_train_,
        #     'recall_train_': md.recall_train_,
        #     'f1_score_train_': md.f1_score_train_,
        # })

        # attitudinal embedding
        md = DiscoverDimension()
        Xd = data[['entity']+ATTDIMS]
        md.fit(Xd, Y)

        discover_records.append({
            'embedding': 'attitudinal',
            'issue': issue,
            'model_decision_boundary_': md.model_decision_boundary_,
            'beta1': md.decision_hyperplane_unit_normal,
            'precision_train_': md.precision_train_,
            'recall_train_': md.recall_train_,
            'f1_score_train_': md.f1_score_train_,
        })

benchmark = pd.DataFrame \
    .from_records(benchmark_records) \
    .drop_duplicates() \
    .sort_values(by=['embedding', 'issue', 'dimension'])

print(benchmark)
save_issues_benckmarks(
    att_folder,
    benchmark)

# discover_records = pd.DataFrame.from_records(discover_records)
# print(discover_records)
