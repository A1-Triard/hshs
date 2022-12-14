from collections import namedtuple
from itertools import chain, product, combinations, count
import os, sys, shutil
from datetime import datetime
from time import mktime
from os import path, chdir, utime, remove, mkdir
from sys import stdout, stderr
import yaml
import subprocess
from subprocess import PIPE
from shutil import copyfile, move, rmtree, copytree
import re

def assembly_plugin(path, year, month, day, hour, minute, second, keep=False):
    subprocess.run(['espa', '-p', 'ru', '-v'] + (['-k'] if keep else []) + [path + '.yaml'], stdout=stdout, stderr=stderr, check=True)
    date = datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)
    t = mktime(date.timetuple())
    utime(path, (t, t))

def write_records_count(esp_path):
    with open(esp_path, 'r', encoding='utf-8') as f:
        esp = yaml.load(f, Loader=yaml.FullLoader)
    esp[0]['TES3'][0]['HEDR']['records'] = len(esp) - 1
    with open(esp_path, 'w', encoding='utf-8') as f:
        yaml.dump(esp, f, allow_unicode=True)

def check_espa_version():
  espa = subprocess.run(['espa', '-V'], stdout=PIPE, check=True, universal_newlines=True)
  if not espa.stdout.startswith('0.11.'):
    print('wrong espa version {}'.format(espa.stdout))
    sys.exit(1)

def prepare_text(path, d):
    with open(path.upper(), 'r', encoding='utf-8') as utf8:
        with open(d + path + '.txt', 'w', encoding='cp1251') as cp1251:
            cp1251.write(utf8.read())

def prepare_content(path, d, year, month, day, hour, minute, second):
  copyfile(path + '.yaml', d + path + '.yaml')
  write_records_count(d + path + '.yaml')
  assembly_plugin(d + path, year, month, day, hour, minute, second)

def make_archive(name, dir):
    chdir(dir)
    if path.exists('../' + name + '.7z'):
        remove('../' + name + '.7z')
    subprocess.run(['7za', 'a', '../' + name + '.7z', '.'], stdout=stdout, stderr=stderr, check=True)
    chdir('..')

def represent_none(self, _):
    return self.represent_scalar('tag:yaml.org,2002:null', '~')

def main():
    cd = path.dirname(path.realpath(__file__))
    chdir(cd)
    check_espa_version()
    yaml.add_representer(type(None), represent_none)
    if path.exists('ar'):
        rmtree('ar')
    mkdir('ar')
    mkdir('ar/Data Files')
    prepare_text('Readme', 'ar/')
    prepare_content('HideSugarHideSkooma.esp', 'ar/Data Files/', 2017, 1, 10, 18, 53, 0)
    prepare_content('HideSugarHideSkooma+Tweaks.esp', 'ar/Data Files/', 2017, 1, 10, 18, 53, 0)
    prepare_content('HideSugarHideSkooma+Tweaks+MCPfiltering.esp', 'ar/Data Files/', 2017, 1, 10, 18, 53, 0)
    make_archive('HideSugarHideSkooma', 'ar')
    rmtree('ar')

if __name__ == "__main__":
    main()
