#!/bin/bash

# declare -a Limits=(1e4 1e5 1e6 1e7 1.1e7)

declare -a Limits=(1e5)

for limit in ${Limits[@]}; do
    python python/dev.py --config=france.yaml --limit=$limit --output=outputs
done