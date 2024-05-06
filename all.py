import os
import pandas as pd

path = '/home/jimena/work/dev/some4demDB/data/annotations/surveys_and_P_numbers - EPO2023Collection.csv'
df = pd.read_csv(path)

config = "configs/embeddings.yaml"
for i, data in df.iterrows():
    data = data[~data.isna()]
    country = data['country']
    surveys = ','.join(data.keys()[1:].tolist())
    command = f"python pipeline.py --config={config} --output=tmp --surveys={surveys} --country={country}"
    # os.system(command)
    print(command)


