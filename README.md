# Data availability statements

Can we analyze the data availability statements we receive with actual submissions to see how they are used and if there are trends in the data?

## Building with snakemake

To build this pipeline, run

```
$ pip install snakemake
$ snakemake --use-conda
```

To visualize the data pipeline, run

`snakemake --dag | dot -Tpdf > dag.pdf`
