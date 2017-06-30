import os

import yaml

from stack import Stack


class ConfigMissing(Exception):
    pass


class Config(object):
    default_path = os.path.join(os.getcwd(), 'tbd.yml')

    def __init__(self, data={}, path=None, helpers=None):
        self.data = data
        self.path = os.path.abspath(path or self.default_path)
        self.base_dir = os.path.dirname(self.path)
        self.helpers_import = helpers or 'helpers'

    @classmethod
    def from_file(cls, path=None):
        path = path or cls.default_path

        if not os.path.exists(path):
            raise ConfigMissing

        with open(path, 'r') as f:
            return cls(data=yaml.load(f), path=path)

    @property
    def stack_data(self):
        return self.data.get('stacks', {})

    @property
    def regions(self):
        return self.stack_data.keys()

    @property
    def stacks(self):
        stacks = []

        for region in self.regions:
            for name, info in self.stack_data[region].items():
                stacks.append(Stack(
                    region=region,
                    name=name,
                    template=info['template'],
                    parameters=info.get('parameters', {})
                ))

        return stacks
