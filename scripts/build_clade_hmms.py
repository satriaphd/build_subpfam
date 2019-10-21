#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Build clade HMMs from the given (trimmed) multifasta files

usage: build_clade_hmms.py <fasta_folder> <clade_txt_folder> <output_folder>
---
- fasta_folder: folder containing input multifasta files
- clade_txt_folder: path to clade assignment text files
- output_folder: resulting HMMs will be stored here
"""


from sys import argv
from os import path
from tempfile import TemporaryDirectory
import glob
import subprocess


def main():
    fasta_folder = argv[1]
    clade_txt_folder = argv[2]
    output_folder = argv[3]

    fasta_files = glob.glob(path.join(fasta_folder, "*.fa"))
    for i, fasta_path in enumerate(fasta_files):
        clade_txt_path = "{}.clades.txt".format(path.join(clade_txt_folder, path.splitext(path.basename(fasta_path))[0]))
        output_path = "{}.clades.hmm".format(path.join(output_folder, path.splitext(path.basename(fasta_path))[0]))
        print("Building clade HMM: {} ({}/{})".format(output_path, i+1, len(fasta_files)))
        clades = get_clades(clade_txt_path)
        build_hmm(fasta_path, clades, output_path)


def build_hmm(fasta_path, clades, output_hmm_path):
    """ build merged subpfam hmms """
    sequences = get_sequences(fasta_path)
    pfam_name = path.splitext(path.basename(fasta_path))[0]
    assert not path.exists(output_hmm_path)

    with TemporaryDirectory() as temp_dir:
        for cl in clades:
            hmm_name = "{}_c{}".format(pfam_name, cl)
            with open(path.join(temp_dir, "{}.fa".format(hmm_name)), "w") as fa:
                for fid in clades[cl]:
                    fa.write(">{}\n{}\n".format(fid, sequences[fid]))
            command = "hmmbuild -n {} {} {}".format(hmm_name, path.join(temp_dir, "{}.hmm".format(hmm_name)), path.join(temp_dir, "{}.fa".format(hmm_name)))
            if subprocess.check_call(command, shell=True) == 0:
                continue
        with open(output_hmm_path, "w") as hm:
            for cl in clades:
                hmm_name = "{}_c{}".format(pfam_name, cl)
                with open(path.join(temp_dir, "{}.hmm".format(hmm_name)), "r") as sm:
                    for line in sm.readlines():
                        hm.write(line)


def get_sequences(fasta_path):
    """ fetch fasta sequences into a dictionary """
    sequences = {}
    with open(fasta_path, "r") as fa:
        cur_id = ""
        for line in fa.readlines():
            if line.startswith(">"):
                cur_id = line.rstrip()[1:]
                sequences[cur_id] = ""
            else:
                if len(cur_id) > 0:
                    sequences[cur_id] += line.rstrip()
    return sequences


def get_clades(clade_txt_path):
    """ fetch clade list into a dictionary """
    clades = {}
    i = 0
    with open(clade_txt_path, "r") as ct:
        for line in ct.readlines():
            cols = line.rstrip().split("\t")
            fid = cols[0]
            cl = cols[1]
            if cl not in clades:
                clades[cl] = []
            clades[cl].append(fid)
            i += 1
    return clades


if __name__ == "__main__":
    main()