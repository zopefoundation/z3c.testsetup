from setuptools import setup, find_packages
import os

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = (
    read('README.txt')
    + '\n\n'
    + read('CHANGES.txt')
    + '\n\n'
    )

setup(
    name='z3c.testsetup',
    version='0.1',
    author='Uli Fouquet',
    author_email='uli@gnufix.de',
    url='',
    download_url='',
    description='Easier test setup for Grok and Zope 3 components.',
    long_description=long_description,
    license='ZPL',
    classifiers=['Development Status :: 3 - Alpha',
                 'Environment :: Web Environment',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: Zope Public License',
                 'Programming Language :: Python',
                 'Framework :: Zope3',
                 ],

    packages=find_packages('src'),
    package_dir = {'': 'src'},
    namespace_packages = ['z3c'],
    include_package_data = True,
    zip_safe=False,
    install_requires=['setuptools',
                      'zope.component',
                      'zope.testing',
                      'zope.app.testing',
                      'martian',
                      ],
)
