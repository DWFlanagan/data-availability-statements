#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging

import pandas as pd
import numpy as np
from sqlalchemy import create_engine, engine, MetaData, Table, select, or_
from snowflake.sqlalchemy import URL
from dotenv import load_dotenv, find_dotenv

logging.basicConfig(
    filename="das.log",
    level=logging.INFO,
    filemode="w",
    format="%(asctime)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
)


def get_secrets():
    load_dotenv(find_dotenv())

    secrets = {
        "SNOWFLAKE_USER": os.getenv("SNOWFLAKE_USER"),
        "SNOWFLAKE_PASSWORD": os.getenv("SNOWFLAKE_PASSWORD"),
        "SNOWFLAKE_ACCOUNT": os.getenv("SNOWFLAKE_ACCOUNT"),
        "SNOWFLAKE_ROLE": os.getenv("SNOWFLAKE_ROLE"),
        "SNOWFLAKE_DATABASE": os.getenv("SNOWFLAKE_DATABASE"),
        "SNOWFLAKE_SCHEMA": os.getenv("SNOWFLAKE_SCHEMA"),
        "SNOWFLAKE_WAREHOUSE": os.getenv("SNOWFLAKE_WAREHOUSE"),
    }

    return secrets


def make_engine(secrets):

    url = URL(
        user=secrets["SNOWFLAKE_USER"],
        password=secrets["SNOWFLAKE_PASSWORD"],
        account=secrets["SNOWFLAKE_ACCOUNT"],
        role=secrets["SNOWFLAKE_ROLE"],
        database=secrets["SNOWFLAKE_DATABASE"],
        schema=secrets["SNOWFLAKE_SCHEMA"],
        warehouse=secrets["SNOWFLAKE_WAREHOUSE"],
    )

    engine = create_engine(url)

    return engine


def connect_to_engine(engine):

    logging.info("Connecting to database.")
    conn = engine.connect()
    metadata = MetaData()

    questions = Table(
        "S1_ARTICLES_SUBMISSION_CUSTOM_QUESTIONS",
        metadata,
        autoload=True,
        autoload_with=engine,
    )
    articles = Table("S1_ARTICLES", metadata, autoload=True, autoload_with=engine)

    return (conn, questions, articles)


def download_data(conn, questions, articles):
    stmt = (
        select(
            [
                questions.c.site_name,
                questions.c.documentid,
                questions.c.customquestionid,
                questions.c.questiontext,
                questions.c.submissioncustomanswer_answertext.label("answertext"),
                articles.c.submissiondate,
            ]
        )
        .select_from(
            questions.join(articles, questions.c.documentid == articles.c.documentid)
        )
        .where(
            or_(
                questions.c.questiontext.ilike("%data%"),
                questions.c.submissioncustomanswer_answertext.ilike("%data%"),
            )
        )
    )

    logging.info("Connecting to data warehouse.")
    df = pd.read_sql(stmt, conn)

    conn.close()

    return df


def save_data(df):
    PROJ_ROOT = os.path.abspath(os.path.join(os.curdir))
    save_path = os.path.join(PROJ_ROOT + "/data/raw/" + "das.feather")
    df.to_feather(save_path)
    logging.info(f"Saved to {save_path}.")


secrets = get_secrets()
engine = make_engine(secrets)
(conn, questions, articles) = connect_to_engine(engine)
df = download_data(conn, questions, articles)
save_data(df)

