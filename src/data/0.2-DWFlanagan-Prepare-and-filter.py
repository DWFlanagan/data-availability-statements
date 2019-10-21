#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging

import pandas as pd
import engarde.decorators as ed

logging.basicConfig(
    filename="das.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
)


@ed.is_shape((None, 6))
def load_data():
    logging.info(f"Proj root is {PROJ_ROOT}.")
    load_path = os.path.join(PROJ_ROOT + "/data/raw/" + "das.feather")

    logging.info(f"Reading file from {load_path}.")

    all_statements = pd.read_feather(load_path)

    logging.info(f"{len(all_statements)} unfiltered rows loaded.")

    return all_statements


def filter_questions(df):
    data_statements = df[
        df["questiontext"].str.contains(
            r"data availability|data accessibility",
            na=False,  # Ignore rows with NaNs
            case=False,  # Ignore case
        )
    ]

    return data_statements


def save_data(data_statements):
    save_path = os.path.join(PROJ_ROOT + "/data/interim/" + "data_statements.feather")
    logging.info(f"Writing filtered data to {save_path}.")
    data_statements.reset_index(drop=True).to_feather(save_path)


PROJ_ROOT = os.path.join(os.curdir)

all_statements = load_data()
data_statements = filter_questions(all_statements)
save_data(data_statements)
