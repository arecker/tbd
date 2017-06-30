import unittest

from tbd import template


class FunctionsTest(unittest.TestCase):
    def test_ref(self):
        self.assertEqual(
            template.ref('MyReference'),
            {'Ref': 'MyReference'}
        )

    def test_tags(self):
        actual = template.tags(**{
            'Name': 'testname',
            'created-by': 'kitchen'
        })
        expected = [{
            'Key': 'Name',
            'Value': 'testname'
        }, {
            'Key': 'created-by',
            'Value': 'kitchen'
        }]
        self.assertEqual(sorted(actual), sorted(expected))
