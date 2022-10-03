# ABRiannotate

This script runs ABRicate using multiple reference databases and maps the results onto genes.

## Requirements

- Python 3.9+
- Working `abricate` (v1+) in `$PATH` or docker
- Python packages `pandas` and `fire`

### Installation

```bash
pip install git+https://github.com/MrTomRod/abri-annotate
```

## Input

- GenBank files (.gbk)

## Usage

### Bash

```shell
abriannotate-docker \
  --abricate-docker-image="quay.io/biocontainers/abricate:1.0.1--ha8f3691_1" \
  --gbk=test/assembly.gbk \
  --genome_identifier='identifier' \
  --dbs=[card,resfinder] \
  --outdir=test/out/XX \
  --merge_annotations=True \
  --verbose=True \
  --skip_bad_hits=False \
  --docker_cmd=podman


abriannotate-bash \
  --abricate_path="['conda', 'run', '-n', 'abricate', 'abricate']" \
  --gbk=test/assembly.gbk \
  --genome_identifier='identifier' \
  --dbs="['argannot', 'card', 'ecoh', 'ncbi', 'plasmidfinder', 'resfinder', 'vfdb']" \
  --outdir=test/out/YY \
  --merge_annotations=False \
  --verbose=False \
  --skip_bad_hits=False
```

### Python

See [test_ABRiannotateBash.py](test/test_ABRiannotateBash.py) / [test_ABRiannotateDocker.py](test/test_ABRiannotateDocker.py).

## Output:

With `merge_annotations=True`:

- `{genome-identifier}.abriannotate.annotations.AR`:

```tsv
FAM23220-i1-1.1_001490	AR:rep33_1_rep(pSMA198)
FAM23220-i1-1.1_001603	AR:rep33_2_rep(pK214)
FAM23220-i1-1.1_001463	AR:ErmB
FAM23220-i1-1.1_001999	AR:tetM
FAM23220-i1-1.1_000192	AR:lmrD
```

- `{genome-identifier}.abriannotate.descriptions.AR`:

```tsv
AR:rep33_1_rep(pSMA198)	GENE=rep33_1_rep(pSMA198), RESISTANCE=nan, ACCESSION=HE613570, DB=plasmidfinder
AR:rep33_2_rep(pK214)	GENE=rep33_2_rep(pK214), RESISTANCE=nan, ACCESSION=X92946, DB=plasmidfinder
AR:lmrD	GENE=lmrD, RESISTANCE=lincosamide, ACCESSION=CP033607.1:310893-312888, DB=card
AR:ErmB	GENE=ErmB, RESISTANCE=lincosamide;macrolide;streptogramin, ACCESSION=AF242872.1:2131-2878, DB=card
AR:tetM	GENE=tetM, RESISTANCE=tetracycline, ACCESSION=AM990992.1:1003680-1001760, DB=card
```

With `merge_annotations=False`:

- `{genome-identifier}.abriannotate.annotations.AR`:

```tsv
FAM23220-i1-1.1_001490	AR:plasmidfinder:rep33_1_rep(pSMA198)
FAM23220-i1-1.1_001603	AR:plasmidfinder:rep33_2_rep(pK214)
FAM23220-i1-1.1_001463	AR:argannot:(MLS)erm(B), AR:megares:ERMB, AR:ncbi:erm(B), AR:resfinder:erm(B)_18, AR:card:ErmB
FAM23220-i1-1.1_001999	AR:resfinder:tet(M)_7, AR:argannot:(Tet)tetM, AR:ncbi:tet(M), AR:card:tetM, AR:megares:TETM
FAM23220-i1-1.1_000192	AR:megares:LMRD, AR:card:lmrD
```

- `{genome-identifier}.abriannotate.descriptions.AR`:

```tsv
AR:plasmidfinder:rep33_1_rep(pSMA198)	GENE=rep33_1_rep(pSMA198), RESISTANCE=nan, ACCESSION=HE613570, DB=plasmidfinder
AR:plasmidfinder:rep33_2_rep(pK214)	GENE=rep33_2_rep(pK214), RESISTANCE=nan, ACCESSION=X92946, DB=plasmidfinder
AR:resfinder:erm(B)_18	GENE=erm(B)_18, RESISTANCE=Erythromycin;Lincomycin;Clindamycin;Quinupristin;Pristinamycin_IA;Virginiamycin_S, ACCESSION=X66468, DB=resfinder
AR:resfinder:tet(M)_7	GENE=tet(M)_7, RESISTANCE=Doxycycline;Tetracycline;Minocycline, ACCESSION=FN433596, DB=resfinder
AR:argannot:(MLS)erm(B)	GENE=(MLS)erm(B), RESISTANCE=nan, ACCESSION=M11180:714-1451, DB=argannot
AR:argannot:(Tet)tetM	GENE=(Tet)tetM, RESISTANCE=nan, ACCESSION=DQ534550:1451-3370, DB=argannot
AR:megares:LMRD	GENE=LMRD, RESISTANCE=nan, ACCESSION=MEG_3597, DB=megares
AR:megares:ERMB	GENE=ERMB, RESISTANCE=nan, ACCESSION=MEG_2801, DB=megares
AR:megares:TETM	GENE=TETM, RESISTANCE=nan, ACCESSION=MEG_7146, DB=megares
AR:ncbi:erm(B)	GENE=erm(B), RESISTANCE=MACROLIDE, ACCESSION=NG_047801.1, DB=ncbi
AR:ncbi:tet(M)	GENE=tet(M), RESISTANCE=TETRACYCLINE, ACCESSION=NG_048252.1, DB=ncbi
AR:card:lmrD	GENE=lmrD, RESISTANCE=lincosamide, ACCESSION=CP033607.1:310893-312888, DB=card
AR:card:ErmB	GENE=ErmB, RESISTANCE=lincosamide;macrolide;streptogramin, ACCESSION=AF242872.1:2131-2878, DB=card
AR:card:tetM	GENE=tetM, RESISTANCE=tetracycline, ACCESSION=AM990992.1:1003680-1001760, DB=card
```
