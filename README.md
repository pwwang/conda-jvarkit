# conda-jvarkit
Receipts for building jvarkit tools on conda

## Build jvarkit for conda
```shell
> python build.py build
```

## Run jvarkit
```shell
> jvarkit

Usage:
  jvarkit <command> [OPTIONS]

Available commands:
  install            - Install a jvarkit tool.
  list               - List available jvarkit tools.
  version            - Show current version of jvarkit.
  help [COMMAND]     - Print help message for the command and exit.

Installed tools:
  vcfstats           - Produce VCF statitics
  vcf2bam            - vcf to bam
  vcfgo              - Find the GO terms for VCF annotated with SNPEFF or VEP
```

## Run a single tool
```shell
> jvarkit vcfgo

There was an error in the input parameters.
The following options are required: [-G], [-A]
[INFO][Launcher]vcfgo Exited with failure (-1)
Description:
  Find the GO terms for VCF annotated with SNPEFF or VEP

Usage:
  jvarkit vcfgo [OPTIONS]

Optional options:
  --hh [BOOL]           - Show original help page.
                          Default: False
  --java <STR>          - Path to java executable.
                          Default: 'java'
  -h, -H, --help        - Show help message and exit.

Java options:
  -X../-D..             - Java Virtual Machine Parameters

Required tool options:
  -A                    - (goa input url)
                          Default: http://cvsweb.geneontology.org/cgi-bin/cvsweb.cgi/go/gene- \
                          associations/gene_association.goa_human.gz?rev=HEAD
  -G                    - (go  url)
                          Default: http://archive.geneontology.org/latest-termdb/go_daily- \
                          termdb.rdf-xml.gz

Optional tool options:
  -h, --help            - print help and exit
      --helpFormat      - What kind of help. One of [usage,markdown,xml].
  -o, --output          - Output file. Optional . Default: stdout
      --version         - print version and exit
  -C                    - (Go:Term) Add children to the list of go term to be filtered. Can be
                          used multiple times.
                          Default: []
  -F                    - if -C is used, don't remove the variant but set the filter
  -T                    - INFO tag.
                          Default: GOA
  -r                    - remove variant if no GO term is found associated to variant
                          Default: false
  -v                    - inverse filter if -C is used
                          Default: false
```
