#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -U pip setuptools wheel
pip install -U spacy
python -m spacy download de_core_news_sm
pip install -U fastapi[standard]
pip install -U jptranscription