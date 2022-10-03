from .ABRiannotate import ABRiannotate, os, logger


class ABRiannotateBash(ABRiannotate):
    def __init__(self, *args, abricate_path: list, **kwargs):
        if type(abricate_path) is str:
            abricate_path = [abricate_path]
        self.abricate_path = abricate_path
        super().__init__(*args, **kwargs)

    def _build_cmd(self, args: [str], file: str = None) -> [str]:
        cmd = list.copy(self.abricate_path)

        cmd.extend(args)

        if file is not None:
            assert os.path.isfile(file), f'File does not exist: {file}'
            cmd.append(file)

        return cmd


def runner(
        abricate_path: [str],
        gbk: str,
        genome_identifier: str,
        outdir: str,
        markdown_file: str = None,
        dbs: [str] = None,
        merge_annotations: bool = False,
        verbose: bool = True,
        skip_bad_hits: bool = False,
):
    gbka = ABRiannotateBash(
        abricate_path=abricate_path,
        merge_annotations=merge_annotations,
        skip_bad_hits=skip_bad_hits
    )

    gbka.init_outdir_logging(outdir, genome_identifier, logfile=verbose)

    gta, atd = gbka.abriannotate_multidb(gbk=gbk, genome_identifier=genome_identifier,
                                         dbs=dbs, outdir=outdir, markdown_file=markdown_file)

    logger.info(f'Success! ABRicate found {len(atd)} annotations for {len(gta)} genes.')


def main():
    from fire import Fire

    Fire(runner)


if __name__ == '__main__':
    main()
