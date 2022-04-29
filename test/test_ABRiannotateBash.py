import logging
from unittest import TestCase
from abri_annotate import ABRiannotateBash as ABRiannotate, bash_runner as runner

logging.getLogger().setLevel(logging.INFO)

ABRICATE_PATH = ['conda', 'run', '-n', 'abricate', 'abricate']


class TestABRiannotate(TestCase):
    def setUp(self) -> None:
        self.abr = ABRiannotate(abricate_path=ABRICATE_PATH)

    def test_version(self):
        print(self.abr.version)

    def test_check(self):
        print(self.abr.check)

    def test_db_versions(self):
        print(self.abr.db_versions)

    def test_runner_1(self):
        # --gbk='test/FAM23220-i1-1.1.gbk' --verbose --outdir=test/out/outmerge --merge_annotations=True
        runner(
            abricate_path=ABRICATE_PATH,
            gbk='FAM23220-i1-1.1.gbk',
            verbose=False,
            outdir='out/outmerge',
            merge_annotations=True,
        )

    def test_runner_2(self):
        # --gbk='test/FAM17654-i1-1.1.gbk' --verbose --outdir=test/out/prob --merge_annotations=True --dbs=[plasmidfinder]
        runner(
            abricate_path=ABRICATE_PATH,
            gbk='FAM17654-i1-1.1.gbk',
            verbose=False,
            outdir='out/prob',
            merge_annotations=True,
            dbs=['plasmidfinder'],
        )

    def test_runner_3(self):
        # --gbk='test/FAM23220-i1-1.1.gbk' --verbose --outdir=test/out/nomerge --merge_annotations=False
        runner(
            abricate_path=ABRICATE_PATH,
            gbk='FAM23220-i1-1.1.gbk',
            verbose=False,
            outdir='out/nomerge',
            merge_annotations=False,
        )
