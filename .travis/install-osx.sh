#!/bin/bash

set -ev

# Install some dependencies
brew update;
brew outdated pyenv || brew upgrade pyenv;
brew install pyenv-virtualenv

# Install Python
pyenv install ${PYTHON}

# Prepare and initialize pyenv environment
eval "$(pyenv init -)";
eval "$(pyenv virtualenv-init -)";
pyenv rehash
python -m pip install --upgrade pip setuptools wheel tox tox-pyenv

# Create and activate python virtual environment
#pyenv virtualenv $PYTHON venv;
#pyenv activate venv;
