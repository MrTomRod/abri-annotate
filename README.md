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
  --dbs=[card,resfinder] \
  --outdir=test/out/XX \
  --merge_annotations=True \
  --verbose=True \
  --skip_bad_hits=False


abriannotate-bash \
  --abricate_path="['conda', 'run', '-n', 'abricate', 'abricate']" \
  --gbk=test/assembly.gbk \
  --dbs="['argannot', 'card', 'ecoh', 'ncbi', 'plasmidfinder', 'resfinder', 'vfdb']" \
  --outdir=test/out/YY \
  --merge_annotations=False \
  --verbose=False \
  --skip_bad_hits=False
```

### Python

```python
from abri_annotate import ABRiannotateBash

abr = ABRiannotateBash(
    abricate_path=['conda', 'run', '-n', 'abricate', 'abricate'],
)
abr.init_outdir('test/out/YY')  # or: os.makedirs('test/out/YY')
abr.abriannotate_multidb(gbk='test/assembly.gbk', dbs=['card', 'resfinder'], outdir='test/out/YY')
```

## Output:

With `merge_annotations=True`:

`*.annotations.tsv`:

```tsv
ADT70_01470	repUS76_1_rep(pSE12228p05)
ADT70_01530	rep5c_1_rep(pRJ9)
ADT70_06020	PC1_beta-lactamase_(blaZ)
ADT70_08700	fosB-251804940
ADT70_02295	APH3-PRIME
ADT70_06010	blaI_of_Z
ADT70_06015	blaR1
ADT70_08030	dfrC
ADT70_05195	norA
ADT70_05235	mgrA
ADT70_09285	RLMH
```

`*.descriptions.tsv`:

```tsv
repUS76_1_rep(pSE12228p05)	GENE=repUS76_1_rep(pSE12228p05), RESISTANCE=nan, ACCESSION=AE015934, DB=plasmidfinder
rep5c_1_rep(pRJ9)	GENE=rep5c_1_rep(pRJ9), RESISTANCE=nan, ACCESSION=AF447813, DB=plasmidfinder
APH3-PRIME	GENE=APH3-PRIME, RESISTANCE=nan, ACCESSION=MEG_1060, DB=megares
RLMH	GENE=RLMH, RESISTANCE=nan, ACCESSION=MEG_6058, DB=megares
blaI_of_Z	GENE=blaI_of_Z, RESISTANCE=BETA-LACTAM, ACCESSION=NG_047499.1, DB=ncbi
blaR1	GENE=blaR1, RESISTANCE=BETA-LACTAM, ACCESSION=NG_047539.1, DB=ncbi
dfrC	GENE=dfrC, RESISTANCE=diaminopyrimidine, ACCESSION=AE015929.1:1129419-1128933, DB=card
fosB-251804940	GENE=fosB-251804940, RESISTANCE=FOSFOMYCIN, ACCESSION=NG_047889.1, DB=ncbi
norA	GENE=norA, RESISTANCE=acridine_dye;fluoroquinolone, ACCESSION=AY566250:391-1555, DB=card
mgrA	GENE=mgrA, RESISTANCE=acridine_dye;cephalosporin;fluoroquinolone;penam;peptide;tetracycline, ACCESSION=BA000018.3:735860-735416, DB=card
PC1_beta-lactamase_(blaZ)	GENE=PC1_beta-lactamase_(blaZ), RESISTANCE=penam, ACCESSION=CP000732.1:10528-9682, DB=card
```

With `merge_annotations=False`:

`*.annotations.tsv`:

```tsv
ADT70_01470	plasmidfinder:repUS76_1_rep(pSE12228p05)
ADT70_01530	plasmidfinder:rep5c_1_rep(pRJ9)
ADT70_06020	resfinder:blaZ_138, argannot:(Bla)blaZ, megares:BLAZ, ncbi:blaZ, card:PC1_beta-lactamase_(blaZ)
ADT70_08700	resfinder:fosB_3, megares:FOSA, ncbi:fosB-251804940
ADT70_06015	argannot:(Bla)blaR1_Bacilli, megares:BLAR, ncbi:blaR1
ADT70_02295	argannot:(AGly)apH-Stph, megares:APH3-PRIME
ADT70_08030	argannot:(Tmt)dfrC, ncbi:dfrC, card:dfrC
ADT70_06010	argannot:(Bla)blaI, megares:BLAI, ncbi:blaI_of_Z
ADT70_05235	megares:MGRA, card:mgrA
ADT70_05195	megares:NORA, card:norA
ADT70_09285	megares:RLMH
```

`*.descriptions.tsv`:

```tsv
plasmidfinder:repUS76_1_rep(pSE12228p05)	GENE=repUS76_1_rep(pSE12228p05), RESISTANCE=nan, ACCESSION=AE015934, DB=plasmidfinder
plasmidfinder:rep5c_1_rep(pRJ9)	GENE=rep5c_1_rep(pRJ9), RESISTANCE=nan, ACCESSION=AF447813, DB=plasmidfinder
resfinder:blaZ_138	GENE=blaZ_138, RESISTANCE=Amoxicillin;Ampicillin;Penicillin;Piperacillin, ACCESSION=CP003979, DB=resfinder
resfinder:fosB_3	GENE=fosB_3, RESISTANCE=Fosfomycin, ACCESSION=ACHE01000077, DB=resfinder
argannot:(AGly)apH-Stph	GENE=(AGly)apH-Stph, RESISTANCE=nan, ACCESSION=HE579073:1778413-1779213, DB=argannot
argannot:(Bla)blaI	GENE=(Bla)blaI, RESISTANCE=nan, ACCESSION=NG_047499:101-481, DB=argannot
argannot:(Bla)blaR1_Bacilli	GENE=(Bla)blaR1_Bacilli, RESISTANCE=nan, ACCESSION=NG_047539:1-1758, DB=argannot
argannot:(Bla)blaZ	GENE=(Bla)blaZ, RESISTANCE=nan, ACCESSION=AB245469:2235-3080, DB=argannot
argannot:(Tmt)dfrC	GENE=(Tmt)dfrC, RESISTANCE=nan, ACCESSION=Z48233:337-822, DB=argannot
megares:APH3-PRIME	GENE=APH3-PRIME, RESISTANCE=nan, ACCESSION=MEG_1060, DB=megares
megares:NORA	GENE=NORA, RESISTANCE=nan, ACCESSION=MEG_4208, DB=megares
megares:MGRA	GENE=MGRA, RESISTANCE=nan, ACCESSION=MEG_3943, DB=megares
megares:BLAI	GENE=BLAI, RESISTANCE=nan, ACCESSION=MEG_1287, DB=megares
megares:BLAR	GENE=BLAR, RESISTANCE=nan, ACCESSION=MEG_1302, DB=megares
megares:BLAZ	GENE=BLAZ, RESISTANCE=nan, ACCESSION=MEG_1411, DB=megares
megares:FOSA	GENE=FOSA, RESISTANCE=nan, ACCESSION=MEG_2992, DB=megares
megares:RLMH	GENE=RLMH, RESISTANCE=nan, ACCESSION=MEG_6058, DB=megares
ncbi:blaI_of_Z	GENE=blaI_of_Z, RESISTANCE=BETA-LACTAM, ACCESSION=NG_047499.1, DB=ncbi
ncbi:blaR1	GENE=blaR1, RESISTANCE=BETA-LACTAM, ACCESSION=NG_047539.1, DB=ncbi
ncbi:blaZ	GENE=blaZ, RESISTANCE=BETA-LACTAM, ACCESSION=NG_055999.1, DB=ncbi
ncbi:dfrC	GENE=dfrC, RESISTANCE=TRIMETHOPRIM, ACCESSION=NG_047752.1, DB=ncbi
ncbi:fosB-251804940	GENE=fosB-251804940, RESISTANCE=FOSFOMYCIN, ACCESSION=NG_047889.1, DB=ncbi
card:norA	GENE=norA, RESISTANCE=acridine_dye;fluoroquinolone, ACCESSION=AY566250:391-1555, DB=card
card:mgrA	GENE=mgrA, RESISTANCE=acridine_dye;cephalosporin;fluoroquinolone;penam;peptide;tetracycline, ACCESSION=BA000018.3:735860-735416, DB=card
card:PC1_beta-lactamase_(blaZ)	GENE=PC1_beta-lactamase_(blaZ), RESISTANCE=penam, ACCESSION=CP000732.1:10528-9682, DB=card
card:dfrC	GENE=dfrC, RESISTANCE=diaminopyrimidine, ACCESSION=AE015929.1:1129419-1128933, DB=card
```