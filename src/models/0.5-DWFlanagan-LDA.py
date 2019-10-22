#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from joblib import dump

logging.basicConfig(
    filename="das.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
)


def load_data():
    logging.info(f"Proj root is {PROJ_ROOT}.")
    load_path = os.path.join(PROJ_ROOT + "/data/processed/" + "tokenized.feather")

    logging.info(f"Reading file from {load_path}.")

    tokenized_statments = pd.read_feather(load_path)

    logging.info(f"{len(tokenized_statments)} rows loaded.")

    return tokenized_statments


def vectorize(data_statements):
    tfidf_vectorizer = CountVectorizer(min_df=5, max_df=0.9)
    logging.info("Fitting TF-IDF.")
    tfidf = tfidf_vectorizer.fit_transform(data_statements["proc_answers"])

    return tfidf


def build_lda_model(tfidf, n_topics=20):
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=7)
    logging.info("Fitting LDA.")
    topic_model = lda.fit(tfidf)

    return topic_model


def save_model(topic_model):
    save_path = os.path.join(
        PROJ_ROOT + "/models/" + "lda_" + str(N_TOPICS) + ".joblib"
    )
    logging.info(f"Writing model to {save_path}.")
    dump(topic_model, save_path)


PROJ_ROOT = os.path.join(os.curdir)
N_TOPICS = 20

tokenized_statments = load_data()
tfidf = vectorize(tokenized_statments)
topic_model = build_lda_model(tfidf, N_TOPICS)
save_model(topic_model)
