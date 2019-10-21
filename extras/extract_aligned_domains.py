#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
#
# Copyright (C) 2018 Satria A. Kautsar
# Wageningen University & Research
# Bioinformatics Group
"""
This script:
1. Read all hmmscanned BGC jsons in a folder
2. Write multifasta files of aligned sequences per domain
"""

import sys
import os
from glob import glob
from sys import argv
import json


def main():
    """
    arguments: extract_aligned_domains.py <json_folder> <output_folder>
    """
    json_folder = argv[1]
    output_folder = argv[2]

    if os.path.isfile(output_folder):
        print("Error: {} is a file.".format(output_folder))
        sys.exit(1)

    if os.path.isfile(json_folder):
        print("Error: {} is a file.".format(json_folder))
        sys.exit(1)

    json_files = []
    if os.path.isfile(json_folder):
        json_files = [json_folder]
    else:
        json_files = glob(os.path.join(json_folder,"**/*.json"), recursive=True)

    kdoms = {}
    for i, json_file in enumerate(json_files):
        json_object = {}
        with open(json_file, "r") as json_text:
            try:                
                json_object = json.loads(json_text.read())
            except:
                print("Error: failed to load json file {}".format(json_file))
                continue
        print("({}) Scanning {}".format(i, json_object["filename"]))
        scan_and_write(json_object, output_folder)


def scan_and_write(json_object, output_folder):
    for c, cluster in enumerate(json_object["clusters"]):
        for g, gene in enumerate(cluster["genes"]):
            if "pfams" in gene:
                for p, pfam in enumerate(gene["pfams"]):
                    with open(os.path.join(output_folder, "{}.fa".format(pfam["name"])), "a") as mf:
                        clasname = "hybrid"
                        if len(json_object["clusters"][c]["class"]) == 1:
                            clasname = json_object["clusters"][c]["class"][0]
                        mf.write(">{}|{}|{}|{}|{}|{}\n{}\n".format(json_object["folder"], json_object["filename"],c, g, p, clasname, pfam["sequence"]))


if __name__ == "__main__":
    main()