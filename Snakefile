# Use `snakemake` to execute this workflow.
# Use `snakemake --dag | dot -Tpdf > dag.pdf` to visualize the DAG.


rule Finish:
    # Put the final output file as the first rule so all rules run.
    input: "reports/figures/0.6-07-topic-growth.html"

rule Extract_data:
    output: "data/raw/das.feather"
    shell: "papermill notebooks/0.1-DWFlanagan-Extract-data.ipynb notebooks/0.1-DWFlanagan-Extract-data.ipynb -k python3"

rule Filter_data:
    input: "data/raw/das.feather"
    output: "data/interim/data_statements.feather"
    shell: "papermill notebooks/0.2-DWFlanagan-Prepare-and-filter.ipynb notebooks/0.2-DWFlanagan-Prepare-and-filter.ipynb -k python3"

rule Tokenize_data_Spacy:
    input: "data/interim/data_statements.feather"
    output: "data/processed/tokenized.feather"
    shell: "papermill notebooks/0.4-DWFlanagan-Tokenize.ipynb notebooks/0.4-DWFlanagan-Tokenize.ipynb -k python3"

rule LDA_scikit_learn:
    input: "data/processed/tokenized.feather"
    output: "models/lda_20.joblib"
    output: "models/tfidf.joblib"
    shell: "papermill notebooks/0.5-DWFlanagan-LDA.ipynb notebooks/0.5-DWFlanagan-LDA.ipynb -k python3"
    
rule LDA_vis:
    input: "models/lda_20.joblib"
    input: "models/tfidf.joblib"
    output: "reports/figures/0.6-07-topic-growth.html"
    shell: "papermill notebooks/0.6-DWFlanagan-LDA-vis.ipynb notebooks/0.6-DWFlanagan-LDA-vis.ipynb -k python3"
