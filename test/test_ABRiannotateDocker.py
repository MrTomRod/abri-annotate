import logging
from unittest import TestCase
from abri_annotate import ABRiannotateDocker as ABRiannotate, docker_runner as runner

logging.getLogger().setLevel(logging.INFO)

CURRENT_IMAGE = 'quay.io/biocontainers/abricate:1.0.1--ha8f3691_1'


class TestABRiannotate(TestCase):
    def setUp(self) -> None:
        self.docker_cmd = 'podman'
        self.abr = ABRiannotate(abricate_docker_image=CURRENT_IMAGE, docker_cmd=self.docker_cmd)

    def test_version(self):
        print(self.abr.version)

    def test_check(self):
        print(self.abr.check)

    def test_db_versions(self):
        print(self.abr.db_versions)

    def test_runner_1(self):
        # --gbk='test/FAM23220-i1-1.1.gbk' --verbose --outdir=test/out/outmerge --merge_annotations=True
        runner(
            abricate_docker_image=CURRENT_IMAGE,
            gbk='FAM23220-i1-1.1.gbk',
            genome_identifier='FAM23220-i1-1.1',
            verbose=True,
            outdir='out/outmerge',
            merge_annotations=True,
            docker_cmd=self.docker_cmd
        )

    def test_runner_2(self):
        # --gbk='test/FAM17654-i1-1.1.gbk' --verbose --outdir=test/out/prob --merge_annotations=True --dbs=[plasmidfinder]
        runner(
            abricate_docker_image=CURRENT_IMAGE,
            gbk='FAM17654-i1-1.1.gbk',
            genome_identifier='FAM17654-i1-1.1',
            verbose=True,
            outdir='out/prob',
            merge_annotations=True,
            dbs=['plasmidfinder'],
            docker_cmd=self.docker_cmd,
            markdown_file='out/runner2.md'
        )

    def test_runner_3(self):
        # --gbk='test/FAM23220-i1-1.1.gbk' --verbose --outdir=test/out/nomerge --merge_annotations=False
        runner(
            abricate_docker_image=CURRENT_IMAGE,
            gbk='FAM23220-i1-1.1.gbk',
            genome_identifier='FAM23220-i1-1.1',
            verbose=True,
            outdir='out/nomerge',
            merge_annotations=False,
            docker_cmd=self.docker_cmd
        )
