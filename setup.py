from setuptools import setup

#http://docs.python.org/2/distutils/setupscript.html

setup(
    name='quant-finance',
    version='0.0.1',

    author='dev',
    author_email='dev@agutong.com',
    url='http://git.agutong.com/dev/quant-finance',

    license='LICENSE',
    description='quant finance',
    long_description=open('README.md').read(),

    packages=[
      'quant_finance',
    ],

    package_data = {
        #'quant_finance': ['config/*.yml'],
    },

    data_files=[
        #('/etc/init.d', ['bin/init-quant-finance'])
    ],

    scripts=[
    ],

    install_requires=[
        #"Django >= 1.1.1",
    ],

    dependency_links=[
        #zip/tar urls
    ]
)
