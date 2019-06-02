#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re
import os

"""Baby Names exercise

Define the extract_names() function below and change main()
to call it.

For writing regex, it's nice to include a copy of the target
text for inspiration.

Here's what the html looks like in the baby.html files:
...
<h3 align="center">Popularity in 1990</h3>
....
<tr align="right"><td>1</td><td>Michael</td><td>Jessica</td>
<tr align="right"><td>2</td><td>Christopher</td><td>Ashley</td>
<tr align="right"><td>3</td><td>Matthew</td><td>Brittany</td>
...

Suggested milestones for incremental development:
OK -Extract the year and print it
OK -Extract the names and rank numbers and just print them
   -Get the names data into a dict and print it
OK -Build the [year, 'name rank', ... ] list and print it
OK -Fix main() to use the extract_names list
"""


def extract_names(filename):
    """
    Given a file name for baby.html, returns a list starting with the year string
    followed by the name-rank strings in alphabetical order.
    ['2006', 'Aaliyah 91', Aaron 57', 'Abagail 895', ' ...]
    """

    with open(filename, 'r') as arquivo:
        conteudo = arquivo.read()

    ano = extrai_ano(conteudo)
    nomes = extrai_nomes_ranqueados_ordenados(conteudo)

    return [ano] + nomes


def extrai_ano(conteudo):
    pattern = re.compile(r'>Popularity in (\d{4})</')
    match = pattern.search(conteudo)
    ano = match[1]
    return ano


def extrai_nomes_ranqueados_ordenados(conteudo):
    pattern = re.compile(r'^<tr align="right"><td>(\d+)</td><td>(\w+)</td><td>(\w+)</td>$', re.MULTILINE)
    matches = pattern.finditer(conteudo)
    nomes_ranqueados = []

    for match in matches:
        posicao = match[1]
        nome_masculino = match[2]
        nome_feminino = match[3]

        nomes_ranqueados.append(f'{nome_masculino} {posicao}')
        nomes_ranqueados.append(f'{nome_feminino} {posicao}')

    nomes_ranqueados.sort()
    return nomes_ranqueados


def main():
    # This command-line parsing code is provided.
    # Make a list of command line arguments, omitting the [0] element
    # which is the script itself.
    args = sys.argv[1:]

    if not args:
        print('usage: [--summaryfile] file [file ...]')
        sys.exit(1)

    # Notice the summary flag and remove it from args if it is present.
    summary = False
    if args[0] == '--summaryfile':
        summary = True
        del args[0]

    # Trunca o arquivo, se for escrever nele.
    diretorio_script = os.path.dirname(os.path.abspath(__file__))
    arquivo_sumario = os.path.join(diretorio_script, 'summary.txt')
    if summary:
        with open(arquivo_sumario, 'w') as txt:
            pass

    # For each filename, get the names, then either print the text output
    # or write it to a summary file
    for html in args:
        nomes = extract_names(html)

        if summary:
            # Escreve uma linha para cada ano
            with open(arquivo_sumario, 'a') as txt:
                txt.write(str(nomes))
                txt.write('\n')
        else:
            print(nomes)


if __name__ == '__main__':
    main()
