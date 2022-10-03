import os.path
import logging

logger = logging.getLogger("ABRicate")

START_STRING = '[comment]: <> (ABRICATE START)'
END_STRING = '[comment]: <> (ABRICATE END)'

TEMPLATE_NO_PHAGES = '''
[comment]: <> (ABRICATE START)

# ABRicate summary

This genome was analyzed with [{version}](https://github.com/tseemann/abricate/),
but nothing was found.

[comment]: <> (ABRICATE END)

'''.lstrip()

TEMPLATE_PHAGES = '''
[comment]: <> (ABRICATE START)

# ABRicate summary

This genome was analyzed with [{version}](https://github.com/tseemann/abricate/) using the following databases: {dbs}.
ABRicate found [{n_genes} genes](/annotations/?genomes={genome_identifier}&anno_type={anno_type}) with putative antibiotic resistance markers.

[comment]: <> (ABRICATE END)

'''.lstrip()


def create_markdown(version: str, genome_identifier: str, dbs: [str], n_genes: int, anno_type: str) -> str:
    dbs = ', '.join(dbs)
    if n_genes == 0:
        return TEMPLATE_NO_PHAGES.format(version=version, dbs=dbs)
    else:
        return TEMPLATE_PHAGES.format(version=version, genome_identifier=genome_identifier, n_genes=n_genes,
                                      anno_type=anno_type, dbs=dbs)


def inject_markdown(file: str, new_content: str):
    if os.path.isfile(file):
        with open(file) as f:
            old_content = f.read()

        if START_STRING in old_content and END_STRING in old_content:
            logger.info(f'Replacing old ABRicate info in {file=}')
            assert old_content.count(START_STRING) == 1, f'{START_STRING=} occurs multiple times in {file}!'
            assert old_content.count(END_STRING) == 1, f'{END_STRING=} occurs multiple times in {file}!'
            old_content_start, rest = old_content.split(START_STRING)
            rest, old_content_end = rest.split(END_STRING)
            new_content = old_content_start + new_content.strip('\n') + old_content_end

        else:
            logger.info(f'Appending ABRicate info to {file=}')
            assert old_content.count(START_STRING) == 0 and old_content.count(END_STRING) == 0, \
                f'Only one of {END_STRING=} or {START_STRING=} occur in {file}! Both or neither expected!'
            new_content = old_content + '\n' + new_content

    else:
        logger.info(f'Writing ABRicate info to new {file=}')

    assert type(new_content) is str, f'Something went wrong! {type(new_content)=} {new_content=}'
    with open(file, 'w') as f:
        f.write(new_content)
