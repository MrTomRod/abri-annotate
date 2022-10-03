import os
from unittest import TestCase
from abri_annotate.markdown_generator import create_markdown, inject_markdown

os.chdir('..')

VERSION = 'abricate 1.0.1'

NON_EMPTY = '''
# TEST BEFORE

[comment]: <> (ABRICATE START)
OLD CONTENT
[comment]: <> (ABRICATE END)

# TEST AFTER
'''

TEST_DIR = 'test/out/md'


def write(file, text):
    with open(file, 'w') as f:
        f.write(text)
    return file


def read(file):
    with open(file) as f:
        return f.read()


class TestCreate(TestCase):
    def test_create_empty(self):
        md = create_markdown(version=VERSION, genome_identifier='test_id', n_genes=0, anno_type='AR', dbs=['A', 'B'])
        self.assertIn(member='nothing was found', container=md)

    def test_create_real(self):
        md = create_markdown(version=VERSION, genome_identifier='test_id', n_genes=10, anno_type='AR', dbs=[])
        self.assertIn(member='ABRicate found 10 genes', container=md)


class TestInject(TestCase):
    def setUp(self) -> None:
        os.makedirs(TEST_DIR, exist_ok=True)
        self.md = '<<<<<< FAKE CONTENT >>>>>>'

    def test_nonexistent_file(self):
        FILE = f'{TEST_DIR}/nonexistent.md'
        if os.path.isfile(FILE):
            os.remove(FILE)
        inject_markdown(FILE, self.md)
        self.assertEqual(self.md, read(FILE))

    def test_empty_file(self):
        FILE = write(f'{TEST_DIR}/empty.md', '')
        inject_markdown(FILE, self.md)
        self.assertEqual(self.md.strip(), read(FILE).strip())

    def test_inject_file(self):
        FILE = write(f'{TEST_DIR}/inject.md', NON_EMPTY)
        inject_markdown(FILE, self.md)
        result = read(FILE)
        self.assertIn(member=self.md, container=result)
        before, after = result.split(self.md)
        self.assertIn(member='TEST BEFORE', container=before)
        self.assertIn(member='TEST AFTER', container=after)

    def test_inject_file_fail(self):
        FILE = write(f'{TEST_DIR}/inject_fail.md', NON_EMPTY.replace('END', 'XXXXXXX'))
        with self.assertRaises(AssertionError):
            inject_markdown(FILE, self.md)
