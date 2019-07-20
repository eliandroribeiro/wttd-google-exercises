#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
from urllib.request import urlopen
from time import time

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""


def read_urls(filename):
    """Returns a list of the puzzle urls from the given log file,
    extracting the hostname from the filename itself.
    Screens out duplicate urls and returns the urls sorted into
    increasing order."""

    # Lê o conteúdo do arquivo de log.
    with open(filename, 'r') as arquivo:
        conteudo = arquivo.read()

    # Define o hostname a partir do nome do arquivo.
    hostname = filename.split('_')[-1]

    # A classe set garante que haverá apenas uma única instância de cada URL.
    urls_unicas = set()

    # Localiza o caminho do arquivo de imagem do puzzle dentro do conteúdo do arquivo de registro.
    pattern = re.compile(r'(?:GET )(/[\w\d\./-]+/puzzle/[\w\d\./-]+) ')

    # Monta as URLs para cada imagem encontrada.
    for match in pattern.finditer(conteudo):
        url = f'https://{hostname}{match[1]}'
        urls_unicas.add(url)

    # Ordena sempre pelo último código de 4 letras na URL.
    # https://developers.google.com/edu/python/exercises/log-puzzle#part-c---image-slice-descrambling
    urls = sorted(urls_unicas, key=lambda u: u[-8:-4])
    return urls


def download_images(img_urls, dest_dir):
    """Given the urls already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory
    with an img tag to show each local image file.
    Creates the directory if necessary.
    """

    # Cria o diretório destino definido pelo usuário, se não houver.
    os.makedirs(dest_dir, exist_ok=True)

    # Cria o HTML que reúne os fragmentos da imagem.
    with open(f'{dest_dir}/index.html', 'wt') as html:
        html.write(
'''<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Logpuzzle</title>
</head>
<body style="font-size: 0;">
''')
        html.flush()

        # Adiciona ao HTML cada um dos fragmentos da imagem.
        for i, url in enumerate(img_urls):
            nome_img = f'img{i}.jpg'
            html.write(f'    <img src="{nome_img}" alt="Fragmento {i}">\n')
            html.flush()

            caminho_jpg = f'{dest_dir}/{nome_img}'

            try:
                if not os.path.exists(caminho_jpg): # Apenas para facilitar os testes
                    inicio = time()

                    # Baixa e grava no diretório o fragmento da imagem.
                    with urlopen(url, timeout=1.5) as resp:
                        bytes_img = resp.read()
                    with open(caminho_jpg, 'wb') as jpg:
                        jpg.write(bytes_img)

                    fim = time() - inicio
                    print(f'Download de {url} para {caminho_jpg} em {round(fim, 1)} segundos')
            except IOError as e:
                print(e)

        html.write(
'''</body>
</html>
''')


def main():
    args = sys.argv[1:]

    if not args:
        print('usage: [--todir dir] logfile ')
        sys.exit(1)

    todir = ''
    if args[0] == '--todir':
        todir = args[1]
        del args[0:2]

    img_urls = read_urls(args[0])

    if todir:
        download_images(img_urls, todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main()
