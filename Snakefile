# Use `snakemake` to execute this workflow.


rule Finish:
    input: "data/interim/data_statements.feather"
    # Put the final output file as the first rule so all rules run.

rule Extract_data:
    output: "data/raw/das.feather"
    script: "src/data/0.1-DWFlanagan-Extract-data.py"

rule Filter_data:
    input: "data/raw/das.feather"
    output: "data/interim/data_statements.feather"
    script: "src/data/0.2-DWFlanagan-Prepare-and-filter.py"
