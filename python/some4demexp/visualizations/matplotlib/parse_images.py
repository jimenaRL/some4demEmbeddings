import os
import yaml
import shutil
from glob import glob
from argparse import ArgumentParser
from some4demexp.inout import set_output_folder_emb



# parse arguments and set paths
ap = ArgumentParser()
ap.add_argument('--config', type=str, required=True)
ap.add_argument('--country', type=str, required=True)
ap.add_argument('--images', type=str, required=True)
args = ap.parse_args()
config = args.config
country = args.country
images = args.images

with open(config, "r", encoding='utf-8') as fh:
    params = yaml.load(fh, Loader=yaml.SafeLoader)
print(yaml.dump(params, default_flow_style=False))

parent_path =  set_output_folder_emb(params, country)
sources = [
    y for x in os.walk(parent_path)
    for y in glob(os.path.join(x[0], '*.png'))
]

output_folder = os.path.join(images, country)
os.makedirs(output_folder, exist_ok=True)

for src in sources:
    kind = os.path.split(src)[-1][:11]
    if kind == "latent_dims":
        dst = os.path.join(
            output_folder,
            f"{country}-{os.path.split(src)[-1]}")
    elif kind == "attitudinal":
        dst = os.path.join(
            output_folder,
            f"{country}-{os.path.split(os.path.split(src)[0])[-1]}.png")
    else:
        raise ValueError(f"Unexpected image path: {src}.")
    shutil.copyfile(src, dst)
    print(dst)


