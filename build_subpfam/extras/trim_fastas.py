#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Trim rp15 raw alignment multifastas to prepare them for
tree building

usage: trim_fastas.py <fasta_folder> <output_folder>
---
- fasta_folder: folder containing input multifasta files
- output_folder: resulting trimmed fasta files will be stored here
"""

from sys import argv
from os import path
import glob


def main():
    fasta_folder = argv[1]
    output_folder = argv[2]

    fasta_files = glob.glob(path.join(fasta_folder, "*.fasta"))
    for i, fasta_path in enumerate(fasta_files):
        output_path = path.join(output_folder, path.basename(fasta_path))
        print("Trimming {} ({}/{})".format(fasta_path, i+1, len(fasta_files)))
        trim_fasta_file(fasta_path, output_path)


def trim_fasta_file(fasta_path, output_path):
    """ given a multifasta file, do trimming and save the resulting multifasta """
    with open(fasta_path, "r") as sf:
        sorted_accs = []
        idx = 0
        accs = []
        seq_matrix = []
        len_nongaps = []
        for line in sf.readlines():
            if line.startswith(">"):
                accs.append(line.rstrip()[1:])
                seq_matrix.append([])
                len_nongaps.append(0)
                sorted_accs.append(idx)
                idx += 1
            else:
                for c in line.rstrip():
                    seq_matrix[-1].append(c)
                    if c != "-":
                        len_nongaps[-1] += 1
        sorted_accs = sorted(sorted_accs, key=lambda i: -1 * len_nongaps[i])
        included_accs = sorted_accs[int(len(sorted_accs)*0.1):int(len(sorted_accs)*0.9)]
        print("ori:{}, filtered:{}".format(len(accs), len(included_accs)))
        included_cols = []
        for c in range(0, len(seq_matrix[0])):
            for i in included_accs:
                if seq_matrix[i][c] != "-":
                    included_cols.append(c)
                    break
        print("ori cols:{}, filtered cols:{}".format(len(seq_matrix[0]), len(included_cols)))
        with open(output_path, "w") as wf:                                
            for i in included_accs:
                wf.write(">{}\n".format(accs[i]))
                for c in included_cols:
                    wf.write(seq_matrix[i][c])
                wf.write("\n")


if __name__ == "__main__":
    main()