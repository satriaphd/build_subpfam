#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Given a folder of multifasta files, run FastTreeMP and save alignment
trees into the output folder

usage: build_trees.py <fasta_folder> <output_folder> <threads>
---
- fasta_folder: folder containing input multifasta files
- output_folder: resulting tree files will be stored here
- threads: if > 1, use parallel FastTree version (FastTreeMP)

=> required: FastTreeMP (http://www.microbesonline.org/fasttree/#OpenMP)
or FastTree, if threads == 1
"""

from sys import argv
from os import path
import glob
import subprocess


def main():
    fasta_folder = argv[1]
    output_folder = argv[2]
    num_threads = int(argv[3])

    fasta_files = glob.glob(path.join(fasta_folder, "*.fa"))
    for i, fasta_path in enumerate(fasta_files):
        print("building tree for {}...".format(fasta_path))
        build_tree(fasta_path, output_folder, num_threads)


def build_tree(fasta_path, output_folder, num_threads):
    output_path = "{}.newick".format(path.join(output_folder, path.splitext(path.basename(fasta_path))[0]))
    if path.exists(output_path):
        raise Exception("Error: {} exists!".format(output_path))
    num_threads = 1 # todo check if num_threads > 1 and FastTreeMP is installed. for now, default to FastTree
    if num_threads > 1:
        command = (["OMP_NUM_THREADS={} && FastTreeMP -quiet -fastest -noml {} > {}".format(num_threads, fasta_path, output_path)])
    else:
        command = (["FastTree -quiet -fastest -noml {} > {}".format(fasta_path, output_path)])
    subprocess.check_output(command, shell=True)
    return output_path


if __name__ == "__main__":
    main()