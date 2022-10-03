import os
from io import StringIO
import logging
from subprocess import run, PIPE
from functools import cached_property
from tempfile import TemporaryDirectory
from typing import Union

import pandas as pd
from Bio import SeqIO, BiopythonWarning
import warnings

from .markdown_generator import create_markdown, inject_markdown
from .utils import logger, init_logfile

expected_columns = {'#FILE', 'SEQUENCE', 'START', 'END', 'STRAND', 'GENE', 'COVERAGE', 'COVERAGE_MAP', 'GAPS',
                    '%COVERAGE', '%IDENTITY', 'DATABASE', 'ACCESSION', 'PRODUCT', 'RESISTANCE'}


class ABRiannotate:
    def __init__(self, merge_annotations: bool = False, skip_bad_hits: bool = False):
        self.merge_annotations = merge_annotations
        self.skip_bad_hits = skip_bad_hits
        self.__db_versions = None

    def _build_cmd(self, args: [str], file: str = None) -> [str]:
        raise NotImplementedError('This is an abstract class!')

    def init_outdir_logging(self, outdir: str, genome_identifier: str, logfile: bool = False):
        os.makedirs(outdir, exist_ok=True)

        if logfile:
            init_logfile(genome_identifier, logfile=f'{outdir}/{genome_identifier}.abricate.log')

        logger.info(f'Annotating {genome_identifier} with {self.version}...')
        logger.info(f'Available databases: {self.db_versions}...')

    @cached_property
    def version(self) -> str:
        command = self._build_cmd(['--version'])
        subprocess = run(command, stdout=PIPE, stderr=PIPE, encoding='ascii')
        assert subprocess.returncode == 0, F'command failed: {command},\n stdout: {subprocess.stdout},\n stderr: {subprocess.stderr}'
        return subprocess.stdout.strip()

    @cached_property
    def check(self) -> str:
        command = self._build_cmd(['--check'])
        subprocess = run(command, stdout=PIPE, stderr=PIPE, encoding='ascii')
        assert subprocess.returncode == 0, F'command failed: {command},\n stdout: {subprocess.stdout},\n stderr: {subprocess.stderr}'
        return subprocess.stderr.strip()

    @cached_property
    def db_versions(self) -> pd.DataFrame:
        if self.__db_versions is None:
            command = self._build_cmd(['--list'])
            subprocess = run(command, stdout=PIPE, stderr=PIPE, encoding='ascii')
            assert subprocess.returncode == 0, F'command failed: {command},\n stdout: {subprocess.stdout},\n stderr: {subprocess.stderr}'
            databases_table = pd.read_csv(StringIO(subprocess.stdout), sep="\t", index_col=0, parse_dates=['DATE'])
            self.__db_versions = databases_table
        return self.__db_versions

    def abricate(self, file: str, db: str, outdir: str = None) -> pd.DataFrame:
        assert os.path.isfile(file), F'file does not exist: {file}'
        assert ' ' not in file, F'file path may not contain blanks: {file}'
        if outdir:
            assert os.path.isdir(outdir), F'outdir does not exist: {outdir}'
            assert ' ' not in outdir, F'outdir path may not contain blanks: {outdir}'

        command = self._build_cmd(
            args=['--quiet', '--db', db],
            file=file
        )

        logger.info(' '.join(command))

        subprocess = run(command, stdout=PIPE, stderr=PIPE, encoding='ascii')

        error_message = F'command failed: {command},\n stdout: {subprocess.stdout},\n stderr: {subprocess.stderr}'
        assert subprocess.stderr == '', error_message
        assert subprocess.returncode == 0, error_message

        if outdir:
            self.__dump(outdir, file=f'db_{db}.original.tsv', content=subprocess.stdout)

        logger.debug(f'Output:\n{subprocess.stdout}')
        abricate_df = pd.read_csv(StringIO(subprocess.stdout), sep="\t")
        columns = set(abricate_df.columns.tolist())
        assert columns == expected_columns, f'Columns do not match: {columns}! Please update abricate to v1+'

        return abricate_df

    def abriannotate(
            self, gbk: str, db: str, genes_df: pd.DataFrame = None,
            save_output=True, outdir: str = None, anno_prefix: str = None
    ) -> (dict, dict):
        if outdir:
            assert os.path.isdir(outdir), F'outdir does not exist: {outdir}'
            assert ' ' not in outdir, F'outdir path may not contain blanks: {outdir}'
        if genes_df is None:
            genes_df = self.load_gbk(gbk=gbk)

        abricate_df = self.abricate(file=gbk, db=db, outdir=outdir)

        gene_to_annotations = {}
        annotation_to_description = {}

        for i, abricate_hit in abricate_df.iterrows():
            hit_location = abricate_hit.START + abricate_hit.END * 1j  # imaginary number
            hit_length = abs(abricate_hit.END - abricate_hit.START)

            # calculate distance between hit and all genes (distance between imaginary numbers = euclidian distance)
            genes_df['distance'] = (genes_df.location - hit_location).abs().astype(float)

            # pick closest gene
            best_gene = genes_df.nsmallest(1, 'distance').iloc[0]
            description = f'GENE={abricate_hit.GENE}, RESISTANCE={abricate_hit.RESISTANCE}, ACCESSION={abricate_hit.ACCESSION}, DB={db}'

            # print warning if closest gene does not match hit well
            if best_gene.distance > hit_length / 20:
                logger.warning(
                    f'Error in {gbk}:{abricate_hit.SEQUENCE}:{hit_location}:{abricate_hit.GENE}, db={db}\n'
                    f'\tDistance between closest gene ({best_gene.name}) and hit is large: best_gene.distance={best_gene.distance}'
                )
                if self.skip_bad_hits:
                    continue

            # (over)write result to dict
            annotation_name = self.filter_string(
                abricate_hit.GENE if self.merge_annotations else f'{db}:{abricate_hit.GENE}')
            if anno_prefix:
                annotation_name = f'{anno_prefix}{annotation_name}'

            gene_to_annotations[best_gene.name] = gene_to_annotations \
                .get(best_gene.name, set()) \
                .union([annotation_name])
            annotation_to_description[annotation_name] = description

        if outdir and save_output:
            self.__dump(outdir, file=f'db_{db}.annotations.tsv', content=gene_to_annotations)
            self.__dump(outdir, file=f'db_{db}.descriptions.tsv', content=annotation_to_description)

        return gene_to_annotations, annotation_to_description

    def abriannotate_multidb(
            self,
            gbk: str,
            genome_identifier: str,
            outdir: str,
            dbs: [str] = None,
            abricate_dir: str = None,
            anno_prefix: str = 'AR:',
            markdown_file: str = None
    ) -> (dict, dict):
        if abricate_dir:
            logger.debug(f'Storing raw output of ABRicate here: {abricate_dir=}')
            os.makedirs(abricate_dir, exist_ok=True)
            tempdir, workdir = None, abricate_dir
        else:
            tempdir = TemporaryDirectory()
            workdir = tempdir.name
            logger.debug(f'Created temporary directory: {workdir}')

        assert os.path.isdir(outdir), F'outdir does not exist: {outdir}'
        assert ' ' not in outdir, F'outdir path may not contain blanks: {outdir}'

        if dbs is None:
            dbs = ['card', 'ncbi', 'megares', 'argannot', 'vfdb', 'resfinder', 'ecoli_vf', 'ecoh', 'plasmidfinder']
        for db in dbs:
            assert db in self.db_versions.index, f'db={db} does not exist. ABRicate has these dbs: {self.db_versions.index.to_list()}'

        genes_df = self.load_gbk(gbk=gbk)

        gene_to_annotations = {}
        annotation_to_description = {}

        for db in reversed(dbs):
            logger.info(f'Working on db={db} (gbk={gbk})')

            new_gene_to_annotations, new_annotation_to_description = self.abriannotate(
                gbk=gbk, db=db, genes_df=genes_df, save_output=False, outdir=workdir, anno_prefix=anno_prefix)

            gene_to_annotations = self.__merge_dicts(
                old=gene_to_annotations, new=new_gene_to_annotations, replace=self.merge_annotations
            )
            annotation_to_description.update(new_annotation_to_description)

        used_annotations = set(a for as_ in gene_to_annotations.values() for a in as_)
        obsolete_annotations = {a for a in annotation_to_description if a not in used_annotations}

        if not self.merge_annotations:
            assert len(obsolete_annotations) == 0
        for anno in obsolete_annotations:
            del annotation_to_description[anno]

        for as_ in gene_to_annotations.values():
            for a in as_:
                assert a in annotation_to_description, f'Failed to describe annotation: {a}'

        self.__dump(outdir, file=f'{genome_identifier}.abriannotate.annotations.AR',
                    content=gene_to_annotations, values_are_lists=True)
        self.__dump(outdir, file=f'{genome_identifier}.abriannotate.descriptions.AR',
                    content=annotation_to_description)

        markdown = create_markdown(self.version, genome_identifier=genome_identifier, dbs=dbs,
                                   n_genes=len(gene_to_annotations), anno_type=anno_prefix.strip(':_-'))
        if markdown_file:
            inject_markdown(markdown_file, markdown)
        else:
            self.__dump(outdir, file=f'{genome_identifier}.vibrant.summary.md', content=markdown)

        return gene_to_annotations, annotation_to_description

    def load_gbk(self, gbk) -> pd.DataFrame:
        genes_df = pd.DataFrame(columns=['location', 'scf_id', 'strand'])
        with open(gbk) as input_handle, warnings.catch_warnings():
            warnings.simplefilter('ignore', BiopythonWarning)
            for scf in SeqIO.parse(input_handle, "genbank"):
                for f in scf.features:
                    if 'locus_tag' in f.qualifiers:
                        genes_df.loc[f.qualifiers['locus_tag'][0]] = [
                            f.location.nofuzzy_start + f.location.nofuzzy_end * 1j,  # imaginary number
                            scf.id,
                            '+' if f.strand else '-'
                        ]
        return genes_df

    @staticmethod
    def __dump(outdir: str, file: str, content: Union[str, dict, pd.DataFrame], values_are_lists: bool = False):
        if values_are_lists:
            content = {k: ', '.join(vs) for k, vs in content.items()}
        with open(os.path.join(outdir, file), 'w') as f:
            if type(content) is str:
                f.write(content)
            elif type(content) is dict:
                content = '\n'.join(f"{k}\t{v}" for k, v in content.items())
                f.write(content)
            elif type(content) is pd.DataFrame:
                content.to_csv(f, sep='\t')
            else:
                raise AssertionError(f'Cannot dump content of unknown type: {type(content)}')

    @staticmethod
    def __merge_dicts(old: dict, new: dict, replace: bool) -> dict:
        if replace:
            old.update(new)
        else:
            for shared_key in set(old).intersection(set(new)):
                old[shared_key].update(new[shared_key])
            for new_key in set(new).difference(set(old)):
                old[new_key] = new[new_key]
        return old

    @staticmethod
    def filter_string(string: str, allowed_chars=':()_-/') -> str:
        return ''.join(char for char in string if char.isalnum() or char in allowed_chars)
