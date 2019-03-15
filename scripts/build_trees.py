#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Given a folder of multifasta files, run FastTreeMP and save alignment
trees into the output folder

usage: build_trees.py <fasta_folder> <output_folder> <use_normal>
---
- fasta_folder: folder containing input multifasta files
- output_folder: resulting tree files will be stored here
- use_normal: if 1, use regular single threaded FastTree version

=> required: FastTreeMP (http://www.microbesonline.org/fasttree/#OpenMP)
or FastTree, if use_normal == 1
"""

from sys import argv
from os import path
import glob
import subprocess


def main():
    fasta_folder = argv[1]
    output_folder = argv[2]
    use_normal = len(argv) > 3 and argv[3] == "1"

    fasta_files = glob.glob(path.join(fasta_folder, "*.fasta"))
    commands = []
    for i, fasta_path in enumerate(fasta_files):
        output_path = "{}.tree".format(path.join(output_folder, path.splitext(path.basename(fasta_path))[0]))
        if use_normal:
            commands.append(["fasttree {} > {}".format(fasta_path, output_path)])
        else:
            commands.append(["fasttreemp -fastest -noml {} > {}".format(fasta_path, output_path)])
    run_commands(commands)


def run_commands(commands):
    """ run commands from shell """
    for i, command in enumerate(commands):
        for com in command:
            print("{}/{}: {}".format(i, len(commands), com))
            if subprocess.check_call(com, shell=True) == 0:
                continue


if __name__ == "__main__":
    main()