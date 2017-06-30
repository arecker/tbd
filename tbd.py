import os

import boto3
import botocore
import click
import yaml


class Config(object):
    def __init__(self, path=None):
        path = path or os.path.join(os.getcwd(), 'tbd.yml')
        with open(path, 'r') as f:
            self.data = yaml.load(f)

    @property
    def regions(self):
        if not getattr(self, '_regions', None):
            self._regions = self.data.get('stacks', {}).keys()
        return self._regions

    @property
    def stacks(self):
        if not getattr(self, '_stacks', None):
            self._stacks = []
            for region in self.regions:
                stackdata = self.data.get('stacks', {}).get(region, {})
                for name, info in stackdata.items():
                    self._stacks.append(Stack(region, name, info))
        return self._stacks

    def apply(self):
        for stack in self.stacks:
            stack.apply()

    def destroy(self):
        for stack in self.stacks:
            stack.destroy()


class Stack(object):
    def __init__(self, region, name, info):
        self.region = region
        self.name = name
        self.template = info['template']

    def __repr__(self):
        return '<Stack {}>'.format(self.name)

    def client(self):
        return boto3.client('cloudformation', region_name=self.region)

    def read_template_as_string(self):
        with open(self.template, 'rb') as f:
            return f.read()

    @property
    def exists(self):
        client = self.client()
        try:
            response = client.describe_stacks(StackName=self.name)
            return response['Stacks'][0]['StackName'] == self.name
        except botocore.exceptions.ClientError as e:
            expected = 'Stack with id {} does not exist'.format(self.name)
            if expected in e.message:
                return False
            raise e

    def create(self):
        client = self.client()
        waiter = client.get_waiter('stack_create_complete')
        client.create_stack(
            StackName=self.name,
            TemplateBody=self.read_template_as_string()
        )
        waiter.wait(StackName=self.name)

    def update(self):
        client = self.client()
        waiter = client.get_waiter('stack_update_complete')
        client.update_stack(
            StackName=self.name,
            TemplateBody=self.read_template_as_string()
        )
        waiter.wait(StackName=self.name)

    def apply(self):
        if self.exists:
            self.create()
        else:
            self.create()

    def destroy(self):
        client = self.client()
        waiter = client.get_waiter('stack_delete_complete')
        client.delete_stack(StackName=self.name)
        waiter.wait(StackName=self.name)


@click.group()
def main():
    pass


@main.command()
def validate():
    pass


@main.command()
def apply():
    Config().apply()


@main.command()
def destroy():
    Config().destroy()


if __name__ == '__main__':
    main()
