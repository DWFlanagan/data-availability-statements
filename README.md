# Data availability statements

Chris Graf wants to be able to analyze the data availability statements we receive with actual submissions to see how they are used and if there are trends in the data.

## Building with snakemake

To build this pipeline, run

`snakemake`

To visualize the data pipeline, run

`snakemake --dag | dot -Tpdf > dag.pdf`