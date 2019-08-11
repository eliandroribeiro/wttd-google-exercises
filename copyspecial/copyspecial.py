#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

# Problem description:
# https://developers.google.com/edu/python/exercises/copy-special


import sys
import re
import os
import shutil
import subprocess
import logging
from errno import EEXIST

"""Copy Special exercise

The copyspecial.py program takes one or more directories as its arguments.
We'll say that a "special" file is one where the name contains the pattern __w__ somewhere,
where the w is one or more word chars.
The provided main() includes code to parse the command line arguments, but the rest is up to you.
Write functions to implement the features below and modify main() to call your functions.
"""


logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s %(asctime)s - %(message)s')
logger = logging.getLogger()


def get_special_paths(dirs):
    '''Gather a list of the absolute paths of the special files in all the directories.'''
    logger.info(f'get_special_paths({dirs})')

    pattern = re.compile(r'^.*__\w+__.*$')
    especiais = []
    unicos = set()

    try:
        for d in dirs:
            if not os.path.isdir(d):
                logger.warning(f'Argumento {d} ignorado. Não é um diretório.')
                continue

            logger.debug(f'\\  {d}')
            arqs = os.listdir(d)

            for arq in arqs:
                caminho = os.path.abspath(os.path.join(d, arq))

                # We'll assume that names are not repeated across the directories
                # (optional: check that assumption and error out if it's violated).
                if arq not in unicos:
                    unicos.add(arq)
                else:
                    raise FileExistsError(EEXIST, os.strerror(EEXIST), arq, None, caminho)

                if os.path.isfile(caminho) and pattern.match(arq):
                    logger.debug(f' |- {arq}')
                    especiais.append(caminho)
    except FileExistsError as e:
        print(f'Processo interrompido. Nome de arquivo duplicado: "{arq}".\n'
              f'Sugestão: renomeie o arquivo "{e.filename2}".')
        sys.exit(e.errno)
    except OSError as e:
        print(e)
        print('Continuando...')

    return especiais


def copy_to(paths, dir):
    '''If the "--todir dir" option is present at the start of the command line,
    do not print anything and instead copy the files to the given directory,
    creating it if necessary.'''
    logger.info(f'copy_to({paths}, {dir})')

    # Use the python module "shutil" for file copying.

    # If the child process exits with an error code, exit with an error code and print the command's output.
    # Test this by trying to write a zip file to a directory that does not exist.


def zip_to(paths, zippath):
    '''If the "--tozip zipfile" option is present at the start of the command line,
    run this command: "zip -j zipfile <list all the files>".
    This will create a zipfile containing the files.'''
    logger.info(f'zip_to({paths}, {zippath})')

    # Just for fun/reassurance, also print the command line you are going to do first.


def main():
    # This basic command line argument parsing code is provided.
    # Add code to call your functions below.

    # Make a list of command line arguments, omitting the [0] element
    # which is the script itself.
    args = sys.argv[1:]
    if not args:
        print("usage: [--todir dir][--tozip zipfile] dir [dir ...]")
        sys.exit(1)

    # todir and tozip are either set from command line
    # or left as the empty string.
    # The args array is left just containing the dirs.
    todir = ''
    if args[0] == '--todir':
        todir = args[1]
        del args[0:2]

    tozip = ''
    if args[0] == '--tozip':
        tozip = args[1]
        del args[0:2]

    if len(args) == 0:
        print("error: must specify one or more dirs")
        sys.exit(1)

    paths = get_special_paths(args)

    # In the simplest case, just print that list. Print one absolute path per line.
    if not todir and not tozip:
        print('\n'.join(paths))
        sys.exit(0)

    if todir:
        copy_to(paths, todir)

    if tozip:
        zip_to(paths, tozip)


if __name__ == "__main__":
    main()
