from setuptools import setup

setup(
    name='tbd',
    version='0.1',
    packages=['tbd'],
    test_suite='nose.collector',
    install_requires=[
        'boto3',
        'click',
        'jinja2',
        'pyyaml',
    ],
    entry_points='''
        [console_scripts]
        tbd=tbd:main
    ''',
)
