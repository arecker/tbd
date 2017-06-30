import sys
import functools
import importlib

import jinja2
from yaml import dump as yaml_dump
from json import dumps as json_dump


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


def render(path, template_dir, helpers_path=None, helpers_import='helpers'):
    sys.dont_write_bytecode = True
    sys.path.append(helpers_path or template_dir)
    importlib.import_module(helpers_import)
    loader = jinja2.FileSystemLoader(template_dir)
    environment = jinja2.Environment(loader=loader)
    environment.globals.update(_REGISTERED)
    environment.filters.update(_REGISTERED_FILTERS)
    return environment.get_template(path).render()


@register_filter
def yaml(data):
    return yaml_dump(data, default_flow_style=True)


@register_filter
def json(data):
    return json_dump(data)


@register_function
def ref(refname):
    return {'Ref': refname}


@register_function
def tags(**kwargs):
    return [{'Key': k, 'Value': v} for k, v in kwargs.items()]
