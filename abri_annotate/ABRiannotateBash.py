from .ABRiannotate import ABRiannotate, os, logging


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
        outdir: str,
        dbs: [str] = None,
        merge_annotations: bool = False,
        verbose: bool = False,
        skip_bad_hits: bool = False
):
    gbka = ABRiannotateBash(
        abricate_path=abricate_path,
        merge_annotations=merge_annotations,
        skip_bad_hits=skip_bad_hits
    )

    gbka.init_outdir(outdir)

    if verbose:
        logging.getLogger().setLevel(logging.INFO)
        logging.info(gbka.version)
        logging.info(gbka.db_versions)

    gta, atd = gbka.abriannotate_multidb(gbk=gbk, dbs=dbs, outdir=outdir)

    logging.info(f'Success! ABRicate found {len(atd)} annotations for {len(gta)} genes.')


def main():
    from fire import Fire

    Fire(runner)


if __name__ == '__main__':
    main()
