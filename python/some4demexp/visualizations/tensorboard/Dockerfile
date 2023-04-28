# syntax=docker/dockerfile:1

FROM tensorflow/tensorflow:2.8.1 AS base

# In [4]: tf.__version__
# Out[4]: '2.8.1'

# In [3]: tensorboard.__version__
# Out[3]: '2.8.0'

RUN apt-get update && \
    apt-get install nano -y && \
    apt-get install git -y

RUN python -m pip install --upgrade pip
RUN pip install ipython
RUN pip install pandas==1.1.5


WORKDIR /app

# clone project repo and install dependencies
ARG token
ENV env_token $token
RUN git clone https://${env_token}@github.com/jimenaRL/some4demVIZ.git

WORKDIR /app/some4demVIZ/tensorboard/viz



