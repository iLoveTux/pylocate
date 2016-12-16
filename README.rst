PyLocate
========

A simple command line tool to help you find files even within
zip archives.

Installation
------------

You can install pylocate with the following command::

    pip install pylocate

or for the bleeding edge (although they will usually be the same):

    pip install git+https://github.com/ilovetux/pylocate.git

Who is this for?
----------------

PyLocate is for anyone who needs to find files on their filesystem
by name. It is especially useful if you need to search within zip
files.

The functionality is loosely based on the well-known linux command
locate, but it does not use a db for caching which can be either
a good thing or a bad thing depending on your particular use case.
This results in slightly slower performance, but also does not require
you to run ``sudo updatedb`` before issuing the ``pylocate`` command.

This is also Python friendly, as well as the command line tool which
is the feature pylocate was designed for, there is also a Python
memory-efficient generator ``pylocate.locate`` which powers the CLI
so has all the advantages but does not need to be ``shelled out``. This
is useful if you are writing a program which might use many different
data files and would like the ability to search through a local directory.

Features
--------

PyLocate can search through zip files, just add the ``-z, --examine-zips``
flag, and the zip file will be treated just like a directory.

PyLocate can accept many locations to look through, just keep adding
``-d, --directory`` arguments to add locations to look through.

Match on multiple patterns, if you would like to search for all
``.py`` files as well as all ``.md`` files, just add them like so
``pylocate -p *.py -p *.md``

Optionally only match on all patterns, suppose you want to find all
``*.py`` files which have locate in the name you can do so like this
``pylocate -p *.py -p *locate*``

PyLocate operates on ``glob`` patterns so just pass in what the filename
should look like and it should work.

PyLocate can also use regular expressions to search for files, simply
specify the ``-e, --regex`` flag and your patterns.

PyLocate also provides a memory-efficient python generator for use
within your own programs.

How it works
------------

The operation is simple, we simply recurse through the provided directories
using ``os.walk`` then we look at the filenames in each directory. We use
Python's ``fnmatch.fnmatch`` for the filename matching by default, unless
the regex flag is provided in which case we compile the regular expression(s)
and use the regular expression objects ``search()`` method to perform the
match. When a match is found, we use ``print`` to display the filename.

If ``-z, --examine-zips`` is specified, we use Python's
``zipfile.ZipFile.namelist()`` to simply grab the names of the files within 
the zip file.

All of this functionality is provided by one Python generator, so it is easy
to use within your own programs. If you use it this way there is a 1:1
correspondence between the command line options and the parameters to the
function. The functionality is the same except that results are ``yield``ed
instead of ``print``ed.

Contributing
------------

I welcome all types of contributions even simple complaints. Please go to the
``issue tracker <https://github.com/ilovetux/pylocate/issues>``_ to open a bug
report, feature request or complaint. If you would like to submit a pull-request
go right ahead, chances are that I will thank you and include it right there on
the spot, but I might cherry-pick or ask for some improvements such as a test case.

Get the code
------------

You can get a copy of the code with the following command::

    git clone https://github.com/ilovetux/pylocate

Run the tests
-------------

You can run the tests with the following command::

    python setup.py nosetests

Getting help
------------

Please feel free to open an ``issue <https://github.com/ilovetux/pylocate/issues>``_
with any questions or comments you might have, I will try my best to answer
the same day.