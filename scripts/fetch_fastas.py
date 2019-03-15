#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Download rp15 stockholm files from Pfam database and convert
them to multifasta files

usage: fetch_fastas.py <domlist_txt> <pfamdb> <output_folder>
---
- domlist_txt: a text file listing the names (not accession)
               of pfam domains rp15 fasta files to download
- pfamdb: path to the Pfam-A.hmm database
- output_folder: resulting fasta files will be stored here

=> required: convbioseq.py (https://pypi.org/project/bioscripts.convert/) 
"""

from sys import argv
from os import path
import subprocess


def main():
    domlist_path = argv[1]
    pfamdb_path = argv[2]
    output_folder = argv[3]

    domlist = []
    with open(domlist_path, "r") as dl:
        for line in dl.readlines():
            domlist.append(line.rstrip().split("\t")[0])

    commands = collect_commands(domlist, pfamdb_path, output_folder)
    run_commands(commands)


def collect_commands(domlist, pfamdb_path, output_folder):
    """ given pfam name list and a pfam-A.hmm file, return commands
    to download rp15 stockholm files and convert it to multifasta files """
    commands = []
    with open(pfamdb_path, "r") as bf:
        name = ""
        for line in bf.readlines():
            if line.startswith("NAME"):
                name = line.rstrip().split(" ")[-1]
            if line.startswith("ACC"):
                acc = line.rstrip().split(" ")[-1].split(".")[0]
                if name in domlist:
                    fpath = path.join(output_folder, name)
                    commands.append([
                        "wget http://pfam.xfam.org/family/{}/alignment/rp15/gzipped -O {}.gz".format(acc, fpath),
                        "gunzip {}.gz".format(fpath),
                        "python2 convbioseq.py -i stockholm fasta {}".format(fpath),
                        "rm {}".format(fpath)
                        ])
    return commands


def run_commands(commands):
    """ run commands from shell """
    for i, command in enumerate(commands):
        for com in command:
            print("{}/{}: {}".format(i, len(commands), com))
            if subprocess.check_call(com, shell=True) == 0:
                continue


if __name__ == "__main__":
    main()