#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging

import pandas as pd
import engarde.decorators as ed
import spacy
from spacy.lang.en import English
from spacy.lang.en.stop_words import STOP_WORDS
from spacy.tokenizer import Tokenizer
from spacy.attrs import ORTH, LEMMA

logging.basicConfig(
    filename="das.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
)


@ed.is_shape((None, 6))
def load_data():
    logging.info(f"Proj root is {PROJ_ROOT}.")
    load_path = os.path.join(PROJ_ROOT + "/data/interim/" + "data_statements.feather")

    logging.info(f"Reading file from {load_path}.")

    data_statements = pd.read_feather(load_path)

    logging.info(f"{len(data_statements)} rows loaded.")

    return data_statements


def customize_spacy():
    nlp = spacy.load("en_core_web_sm")

    # Add custom stop words to Spacy's list

    customize_stop_words = ["wiley", "br", "href", "url", "et", "al"]

    for w in customize_stop_words:
        nlp.vocab[w].is_stop = True

    # Define a special case to not change "data" to "datum"

    case = [{ORTH: "data", LEMMA: "data"}]
    nlp.tokenizer.add_special_case("data", case)

    return nlp


def spacy_tokenizer(sentence):

    doc = nlp(sentence)

    mytokens = [
        token.lemma_
        for token in doc
        if token.pos_ in ["NOUN", "ADJ", "PROPN"]
        and not token.is_stop
        and not token.like_url
    ]

    prepared_text = " ".join(mytokens)

    return prepared_text


def save_data(tokenized):
    save_path = os.path.join(PROJ_ROOT + "/data/processed/" + "tokenized.feather")
    logging.info(f"Writing tokenized data to {save_path}.")
    data_statements.reset_index(drop=True).to_feather(save_path)


PROJ_ROOT = os.path.join(os.curdir)

data_statments = load_data()
data_statements = data_statments.dropna(subset=["answertext", "submissiondate"])
nlp = customize_spacy()

logging.info("Tokenizing...")
data_statements["proc_answers"] = data_statements["answertext"].apply(spacy_tokenizer)
save_data(data_statements)
