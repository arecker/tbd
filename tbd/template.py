import functools
import importlib
import os
import sys

import jinja2
import yaml as yamllib
import json as jsonlib

_REGISTERED = {}
_REGISTERED_FILTERS = {}


def register_function(func):
    functools.wraps(func)
    _REGISTERED[func.__name__] = func
    return func


def register_filter(func):
    functools.wraps(func)
    _REGISTERED_FILTERS[func.__name__] = func
    return func


def register_constant(key, value):
    _REGISTERED[key] = value


def prettify_json(content):
    data = jsonlib.loads(content)
    return jsonlib.dumps(data, indent=2)


def prettify_yaml(content):
    data = yamllib.load(content)
    return yamllib.dump(data, default_flow_style=False)


def prettify(ext, content):
    if ext in ['.yml', '.yaml']:
        return prettify_yaml(content)
    if ext in ['.js', '.json']:
        return prettify_json(content)


def render(path, template_dir, helpers_path=None, helpers_import='helpers'):
    sys.dont_write_bytecode = True
    sys.path.append(helpers_path or template_dir)
    importlib.import_module(helpers_import)
    loader = jinja2.FileSystemLoader(template_dir)
    environment = jinja2.Environment(loader=loader)
    environment.globals.update(_REGISTERED)
    environment.filters.update(_REGISTERED_FILTERS)
    content = environment.get_template(path).render()
    _, ext = os.path.splitext(path)
    return prettify(ext, content)


@register_filter
def yaml(data):
    return yamllib.dump(data, default_flow_style=True)


@register_filter
def json(data):
    return jsonlib.dumps(data)


@register_function
def ref(refname):
    return {'Ref': refname}


@register_function
def tags(**kwargs):
    return [{'Key': k, 'Value': v} for k, v in kwargs.items()]
