from .ABRiannotate import ABRiannotate, os, logger


class ABRiannotateDocker(ABRiannotate):
    def __init__(self, *args, abricate_docker_image: str, docker_cmd: str = 'docker', uid_gid: str = None, **kwargs):
        self.abricate_docker_image = abricate_docker_image
        self.docker_cmd = docker_cmd
        self.uid_gid = uid_gid
        super().__init__(*args, **kwargs)

    def _build_cmd(self, args: [str], file: str = None) -> [str]:
        cmd = [self.docker_cmd, 'run', '--rm']
        if self.uid_gid:
            self.cmd.extend(['--user', self.uid_gid])

        if file is not None:
            file = os.path.abspath(file)
            assert os.path.isfile(file), f'File does not exist: {file}'
            dirname = os.path.dirname(file)
            cmd.extend(['-v', f'{dirname}:/data:z'])

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
        genome_identifier: str,
        outdir: str,
        markdown_file: str = None,
        dbs: [str] = None,
        merge_annotations: bool = False,
        verbose: bool = True,
        skip_bad_hits: bool = False,
        uid_gid: str = None,
        docker_cmd: str = None,
):
    abr = ABRiannotateDocker(
        abricate_docker_image=abricate_docker_image,
        merge_annotations=merge_annotations,
        skip_bad_hits=skip_bad_hits,
        docker_cmd=docker_cmd,
        uid_gid=uid_gid
    )

    abr.init_outdir_logging(outdir, genome_identifier, logfile=verbose)

    gta, atd = abr.abriannotate_multidb(gbk=gbk, genome_identifier=genome_identifier, dbs=dbs, outdir=outdir,
                                         markdown_file=markdown_file)

    logger.info(f'Success! ABRicate found {len(atd)} annotations for {len(gta)} genes.')


def main():
    from fire import Fire

    Fire(runner)


if __name__ == '__main__':
    main()
