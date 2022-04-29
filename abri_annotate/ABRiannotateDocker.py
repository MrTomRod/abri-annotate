from .ABRiannotate import ABRiannotate, os, logging


class ABRiannotateDocker(ABRiannotate):
    def __init__(self, *args, abricate_docker_image: str, **kwargs):
        self.abricate_docker_image = abricate_docker_image
        super().__init__(*args, **kwargs)

    def _build_cmd(self, args: [str], file: str = None) -> [str]:
        cmd = ['docker', 'run', '--rm']

        if file is not None:
            file = os.path.abspath(file)
            assert os.path.isfile(file), f'File does not exist: {file}'
            dirname = os.path.dirname(file)
            cmd.extend(['-v', f'{dirname}:/data'])

        cmd.append(self.abricate_docker_image)
        cmd.append('abricate')
        cmd.extend(args)
        if file is not None:
            basename = os.path.basename(file)
            cmd.append(f'/data/{basename}')

        return cmd


def runner(
        abricate_docker_image: str,
        gbk: str,
        outdir: str,
        dbs: [str] = None,
        merge_annotations: bool = False,
        verbose: bool = False,
        skip_bad_hits: bool = False
):
    gbka = ABRiannotateDocker(
        abricate_docker_image=abricate_docker_image,
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
