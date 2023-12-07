# Inspired from https://github.com/KEINOS/Dockerfile_of_SQLite3
# -----------------------------------------------------------------------------
#  Stage 0: build sqlite binary
# -----------------------------------------------------------------------------
FROM ubuntu:22.04 AS sqlite

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# install sqlite
COPY test_sqlite3.sh test_sqlite3.sh

RUN apt-get update && \
    apt-get install build-essential -y && \
    apt-get install wget -y
RUN wget https://www.sqlite.org/2023/sqlite-autoconf-3410100.tar.gz
RUN tar -xvf sqlite-autoconf-3410100.tar.gz
RUN ./sqlite-autoconf-3410100/configure && \
    make && \
    make install
RUN sqlite3 --version && \
    ./test_sqlite3.sh

# -----------------------------------------------------------------------------
#  Stage 1: install pyenv
# -----------------------------------------------------------------------------
FROM ubuntu:22.04 AS pyenv

ENV DEBIAN_FRONTEND=noninteractive

# install pyenv with pyenv-installer
COPY pyenv_dependencies.txt pyenv_dependencies.txt

ENV PYENV_GIT_TAG=v2.3.14

RUN apt-get update && \
    apt-get install -y $(cat pyenv_dependencies.txt)
RUN curl https://pyenv.run | bash
RUN apt-get clean && rm -rf /var/lib/apt/lists/*


ENV PYENV_ROOT /root/.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH

RUN pyenv install 3.9.16 && \
    pyenv global 3.9.16

# -----------------------------------------------------------------------------
#  Stage 2: user setup
# -----------------------------------------------------------------------------
FROM ubuntu:22.04

# sqlite settings
COPY --from=sqlite /usr/local/bin/sqlite3 /usr/local/bin/sqlite3
COPY --from=sqlite /usr/local/lib/libsqlite3.so.0 /usr/local/lib/libsqlite3.so.0
COPY test_sqlite3.sh test_sqlite3.sh
RUN sqlite3 --version && \
    ./test_sqlite3.sh

# pyenv settings
COPY --from=pyenv /root/.pyenv /root/.pyenv
ENV PYENV_ROOT /root/.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH
ENV PYTHONIOENCODING utf-8

RUN apt-get update && \
    apt-get install -y git && \
    apt-get install -y nano

RUN pyenv virtualenv some4demexp
RUN pyenv global 3.9.16/envs/some4demexp
RUN pip install --upgrade pip

RUN ls

# clone private project repo and install dependencies
ARG token
ENV env_token $token
RUN git clone https://${env_token}@github.com/jimenaRL/some4demDB.git

# clone public project repo and install dependencies
RUN git clone https://github.com/jimenaRL/some4demEmbeddings.git
WORKDIR /some4demEmbeddings
RUN git checkout validation

RUN pip install -r python/requirements.txt
RUN pip install -r python/some4demexp/validation/requirements.txt

# add manually packages (to later with)
RUN ln -fs /some4demDB/python/some4demdb /root/.pyenv/versions/3.9.16/envs/some4demexp/lib/python3.9/site-packages/some4demdb
RUN ln -fs /some4demEmbeddings/python/some4demexp /root/.pyenv/versions/3.9.16/envs/some4demexp/lib/python3.9/site-packages/some4demexp
