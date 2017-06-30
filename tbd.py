import os

import boto3
import botocore
import click
import jinja2
import yaml as yamllib


jinjaenv = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.getcwd())
)


def ref(refname):
    return {'Ref': refname}


def tags(**kwargs):
    return [{'Key': k, 'Value': v} for k, v in kwargs.items()]


def yaml(data):
    return yamllib.dump(data, default_flow_style=True)


jinjaenv.globals.update(ref=ref, tags=tags)
jinjaenv.filters.update(yaml=yaml)


class Config(object):
    def __init__(self, path=None):
        path = path or os.path.join(os.getcwd(), 'tbd.yml')
        with open(path, 'r') as f:
            self.data = yamllib.load(f)

    @property
    def regions(self):
        return self.data.get('stacks', {}).keys()

    @property
    def stacks(self):
        if not getattr(self, '_stacks', None):
            self._stacks = []
            for region in self.regions:
                stackdata = self.data.get('stacks', {}).get(region, {})
                for name, info in stackdata.items():
                    self._stacks.append(Stack(region, name, info))
        return self._stacks

    def get_stack(self, name):
        try:
            return filter(lambda s: s.name == name, self.stacks)[0]
        except IndexError:
            return None

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
        compiled = jinjaenv.get_template(self.template).render()
        serialized = yamllib.load(compiled)
        return yamllib.dump(serialized)

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


@main.command(name='print')
@click.argument('stack')
def print_template(stack):
    stack = Config().get_stack(stack)
    print(stack.read_template_as_string())


if __name__ == '__main__':
    main()
