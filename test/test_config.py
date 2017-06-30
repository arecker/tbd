import os
import shutil
import tempfile
import unittest

from tbd.config import Config
from tbd.stack import Stack


class ConfigTests(unittest.TestCase):
    def test_config_file(self):
        contents = '''
stacks:
  us-west-2:
    vpc:
      template: something.yml
        '''

        tempdir = tempfile.mkdtemp()
        target = os.path.join(tempdir, 'config.yml')

        with open(target, 'w') as f:
            f.write(contents)

        actual = Config.from_file(path=target).data
        expected = {
            'stacks': {
                'us-west-2': {
                    'vpc': {'template': 'something.yml'}
                }
            }
        }

        try:
            self.assertEqual(actual, expected)
        finally:
            shutil.rmtree(tempdir)

    def test_regions(self):
        actual = Config(data={
            'stacks': {
                'us-west-2': {
                    'vpc': {
                        'template': 'templates/vpc.yml'
                    }
                },
                'us-east-2': {
                    'vpc': {
                        'template': 'templates/vpc.yml'
                    }
                }
            }
        }).regions

        self.assertEqual(actual, ['us-west-2', 'us-east-2'])

    def test_regions_empty(self):
        actual = Config(data={'stacks': {}}).regions
        self.assertEqual(actual, [])

    def test_stacks(self):
        actual = Config(data={
            'stacks': {
                'us-west-2': {
                    'vpc': {
                        'template': 'templates/vpc.yml'
                    }
                },
                'us-east-2': {
                    'vpc': {
                        'template': 'templates/vpc.yml'
                    }
                }
            }
        }).stacks

        expected = [
            Stack(
                region='us-west-2',
                name='vpc',
                template='templates/vpc.yml'
            ),
            Stack(
                region='us-east-2',
                name='vpc',
                template='templates/vpc.yml'
            ),
        ]

        self.assertListEqual(actual, expected)
