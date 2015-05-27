from setuptools import setup, find_packages
import os

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

tests_require = [
    # please also add all test requirements to tox.ini.
    'zope.app.testing',
    'zope.app.zcmlfiles',
    'zope.component',
    ]

long_description = (
    read('README.rst')
    + '\n\n'
    + read('src', 'z3c', 'testsetup', 'README.txt')
    + '\n\n'
    + read('src', 'z3c', 'testsetup', 'HOWTO_UPGRADE.txt')
    + '\n\n'
    + read('CHANGES.rst')
    + '\n\n'
    + 'Download\n'
    + '********\n'
    )

setup(
    name='z3c.testsetup',
    version='0.8.4',
    author='Zope Foundation and Contributors',
    author_email='zope-dev@zope.org',
    url = 'http://pypi.python.org/pypi/z3c.testsetup',
    description='Easier test setup for Zope 3 projects and '
                'other Python packages.',
    long_description=long_description,
    license='ZPL 2.1',
    keywords="zope3 zope tests unittest doctest testsetup",
    classifiers=['Development Status :: 3 - Alpha',
                 'Environment :: Web Environment',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: Zope Public License',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.6',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.3',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: Implementation :: CPython',
                 'Programming Language :: Python :: Implementation :: PyPy',
                 'Operating System :: OS Independent',
                 'Framework :: Zope3',
                 ],

    packages=find_packages('src'),
    package_dir = {'': 'src'},
    namespace_packages = ['z3c'],
    include_package_data = True,
    zip_safe=False,
    install_requires=['setuptools',
                      'zope.testing',
                      'martian',
                      'six',
                      ],
    tests_require = tests_require,
    extras_require = dict(test=tests_require),
)
