# Use `snakemake` to execute this workflow.
# Use `snakemake --dag | dot -Tpdf > dag.pdf` to visualize the DAG.


rule Finish:
    # Put the final output file as the first rule so all rules run.
    input: "models/lda_20.joblib"

rule Extract_data:
    output: "data/raw/das.feather"
    shell: "papermill notebooks/0.1-DWFlanagan-Extract-data.ipynb notebooks/0.1-DWFlanagan-Extract-data.ipynb"

rule Filter_data:
    input: "data/raw/das.feather"
    output: "data/interim/data_statements.feather"
    shell: "papermill notebooks/0.2-DWFlanagan-Prepare-and-filter.ipynb notebooks/0.2-DWFlanagan-Prepare-and-filter.ipynb"

rule Tokenize_data_Spacy:
    input: "data/interim/data_statements.feather"
    output: "data/processed/tokenized.feather"
    shell: "papermill notebooks/0.4-DWFlanagan-Tokenize.ipynb notebooks/0.4-DWFlanagan-Tokenize.ipynb"

rule LDA_scikit_learn:
    input: "data/processed/tokenized.feather"
    output: "models/lda_20.joblib"
    output: "models/tfidf.joblib"
    shell: "papermill notebooks0.5-DWFlanagan-LDA.ipynb notebooks0.5-DWFlanagan-LDA.ipynb"
