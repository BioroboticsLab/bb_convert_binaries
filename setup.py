try: # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements

from setuptools import setup


install_reqs = parse_requirements('requirements.txt', session=False)
reqs = [str(ir.req) for ir in install_reqs]
dep_links = [str(req_line.url) for req_line in install_reqs]

setup(
    name='bb_convert_binaries',
    version='0.0.0.dev1',
    description='This package is used to convert the bb_binary data.',
    long_description='',
    url='https://github.com/BioroboticsLab/bb_convert_binaries',
    install_requires=reqs,
    dependency_links=dep_links,
    author='gitmirgut',
    author_email="gitmirgut@users.noreply.github.com",
    packages=['bb_convert_binaries'],
    package_data={'bb_convert_binaries': ['bb_binary_schemas/*.capnp']},
    license='Apache License 2.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.5'
    ],
)
