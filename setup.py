import sys
from setuptools import setup

tests_require = ["nose>=1.0"]
if sys.version_info < (3,0):
    tests_require = ["nose>=1.0", "mock"]

setup(
    name="pylocate",
    version="0.1.0",
    author="iLoveTux",
    author_email="me@ilovetux.com",
    description="Simple locate script which also looks into zip archives",
    license="GPLv3",
    keywords="locate files zip",
    url="http://github.com/ilovetux/pylocate",
    packages=['pylocate'],
    install_requires=[],
    entry_points={
        "console_scripts": [
            "pylocate=pylocate:main",
        ]
    },
    test_suite="nose.collector",
    tests_require=tests_require,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
