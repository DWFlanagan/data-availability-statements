# Use `snakemake` to execute this workflow.
# Use `snakemake --dag | dot -Tpdf > dag.pdf` to visualize the DAG.


rule Finish:
    # Put the final output file as the first rule so all rules run.
    input: "models/lda_20.joblib"

rule Extract_data:
    output: "data/raw/das.feather"
    script: "src/data/0.1-DWFlanagan-Extract-data.py"

rule Filter_data:
    input: "data/raw/das.feather"
    output: "data/interim/data_statements.feather"
    script: "src/data/0.2-DWFlanagan-Prepare-and-filter.py"

rule Tokenize_data_Spacy:
    input: "data/interim/data_statements.feather"
    output: "data/processed/tokenized.feather"
    script: "src/features/0.4-DWFlanagan-Tokenize.py"

rule LDA_scikit_learn:
    input: "data/processed/tokenized.feather"
    output: "models/lda_20.joblib"
    script: "src/models/0.5-DWFlanagan-LDA.py"
