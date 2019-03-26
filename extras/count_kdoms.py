#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
#
# Copyright (C) 2018 Satria A. Kautsar
# Wageningen University & Research
# Bioinformatics Group
"""
This script:
1. Read all hmmscanned BGC jsons in a folder
2. Write a list of frequently occuring k-doms (+ pattern and - pattern), given k

this only supports domain and not subdomain level
"""

import sys
import os
from glob import glob
from sys import argv
import json


def main():
    """
    arguments: count_kdoms.py <k> <json_folder> <output_path>
    """
    k = int(argv[1])
    json_folder = argv[2]
    output_path = argv[3]

    if os.path.isfile(json_folder):
        print("Error: {} is a file.".format(json_folder))
        sys.exit(1)

    json_files = []
    if os.path.isfile(json_folder):
        json_files = [json_folder]
    else:
        json_files = glob(os.path.join(json_folder,"**/*.json"), recursive=True)

    kdoms = {}
    classes = {}
    for json_file in json_files:
        json_object = {}
        with open(json_file, "r") as json_text:
            try:                
                json_object = json.loads(json_text.read())
            except:
                print("Error: failed to load json file {}".format(json_file))
                continue
        filename_base = ".".join(json_object["filename"].split(".")[:-1]).split("/")[-1]
        kdoms[filename_base] = get_kdoms(json_object, k)
        json_file_base = json_file.split("/")[-1]
        db_type = "unknown"
        if "folder" in json_object:
            db_type = json_object["folder"]
        classes[filename_base] = get_class_base(get_class(json_object), db_type)

    # append k-dom features
    kdoms_presence = {}
    kdoms_classes_presence = {
    }
    kdoms_count = {}
    kdoms_classes_count = {
    }
    for filename_base in kdoms:
        appended_kdoms = []
        classess = classes[filename_base]
        for class2 in classess:
            if class2 not in kdoms_classes_count:
                kdoms_classes_count[class2] = {}
            if class2 not in kdoms_classes_presence:
                kdoms_classes_presence[class2] = {}
        for kdom in kdoms[filename_base]:
            if k > 1:
                minus_key = " - ".join(kdom)
                if minus_key not in kdoms_count:
                    kdoms_count[minus_key] = 0    
                kdoms_count[minus_key] += 1
                if minus_key not in kdoms_presence:
                    kdoms_presence[minus_key] = 0            
                for class2 in classess:
                    if minus_key not in kdoms_classes_count[class2]:
                        kdoms_classes_count[class2][minus_key] = 0    
                    kdoms_classes_count[class2][minus_key] += 1
                    if minus_key not in kdoms_classes_presence[class2]:
                        kdoms_classes_presence[class2][minus_key] = 0
                if minus_key not in appended_kdoms:
                    kdoms_presence[minus_key] += 1
                    for class2 in classess:
                        kdoms_classes_presence[class2][minus_key] += 1
                    appended_kdoms.append(minus_key)
                plus_key = " + ".join(sorted(kdom, key=lambda x: len(x), reverse=True))
                if plus_key not in kdoms_count:
                    kdoms_count[plus_key] = 0    
                kdoms_count[plus_key] += 1
                if plus_key not in kdoms_presence:
                    kdoms_presence[plus_key] = 0
                for class2 in classess:
                    if plus_key not in kdoms_classes_count[class2]:
                        kdoms_classes_count[class2][plus_key] = 0    
                    kdoms_classes_count[class2][plus_key] += 1
                    if plus_key not in kdoms_classes_presence[class2]:
                        kdoms_classes_presence[class2][plus_key] = 0
                if plus_key not in appended_kdoms:
                    kdoms_presence[plus_key] += 1
                    for class2 in classess:
                        kdoms_classes_presence[class2][plus_key] += 1
                    appended_kdoms.append(plus_key)
            else:
                key = kdom[0]
                if key not in kdoms_count:
                    kdoms_count[key] = 0    
                kdoms_count[key] += 1
                if key not in kdoms_presence:
                    kdoms_presence[key] = 0                     
                for class2 in classess:
                    if key not in kdoms_classes_count[class2]:
                        kdoms_classes_count[class2][key] = 0    
                    kdoms_classes_count[class2][key] += 1
                    if key not in kdoms_classes_presence[class2]:
                        kdoms_classes_presence[class2][key] = 0
                if key not in appended_kdoms:
                    kdoms_presence[key] += 1
                    for class2 in classess:
                        kdoms_classes_presence[class2][key] += 1
                    appended_kdoms.append(key)

    # write distribution of BGCs and classes per database
    with open("{}.classes-distribution.txt".format(output_path), "w") as outfile:
        dbfreqs = {}
        for filename in classes:
            cs_filename = classes[filename]
            dbn = cs_filename[0].split(":")[0]
            if dbn not in dbfreqs:
                dbfreqs[dbn] = {}
            clas = "hybrid"
            if len(cs_filename) == 1:
                clas = cs_filename[0].split(":")[-1]
            if clas not in dbfreqs[dbn]:
                dbfreqs[dbn][clas] = 0
            dbfreqs[dbn][clas] += 1
        outfile.write("db_name\tclass\tcount\n")
        for dbn in dbfreqs:
            for clas in sorted(dbfreqs[dbn]):
                outfile.write("{}\t{}\t{}\n".format(dbn, clas, dbfreqs[dbn][clas]))

    # write top-100 k-dom presence
    with open("{}.k{}-top100.txt".format(output_path, k), "w") as outfile:
        i = 0
        for key in sorted(kdoms_presence, key=kdoms_presence.get, reverse=True):
            if k < 2 or len(key.split(" + ")) > 1:
                if kdoms_presence[key] < 1:#i >= 300:
                    break
                outfile.write("{}\t{}\n".format(key, kdoms_presence[key]))
                i += 1

    # write top-100 k-dom presence for each class
    for class2 in kdoms_classes_presence:
        with open("{}.k{}.{}-top100.txt".format(output_path, k, class2), "w") as outfile:
            i = 0
            for key in sorted(kdoms_classes_presence[class2], key=kdoms_classes_presence[class2].get, reverse=True):
                if k < 2 or len(key.split(" + ")) > 1:
                    if kdoms_classes_presence[class2][key] < 5:#if i >= 300:
                        break
                    outfile.write("{}\t{}\n".format(key, kdoms_classes_presence[class2][key]))
                    i += 1

    # write top-100 k-dom count
    with open("{}.k{}-top100-count.txt".format(output_path, k), "w") as outfile:
        i = 0
        for key in sorted(kdoms_count, key=kdoms_count.get, reverse=True):
            if k < 2 or len(key.split(" + ")) > 1:
                if kdoms_count[key] < 1:#i >= 300:
                    break
                outfile.write("{}\t{}\n".format(key, kdoms_count[key]))
                i += 1

    # write top-100 k-dom count for each class
    for class2 in kdoms_classes_count:
        with open("{}.k{}.{}-top100-count.txt".format(output_path, k, class2), "w") as outfile:
            i = 0
            for key in sorted(kdoms_classes_count[class2], key=kdoms_classes_count[class2].get, reverse=True):
                if k < 2 or len(key.split(" + ")) > 1:
                    if i >= 300:
                        break
                    outfile.write("{}\t{}\n".format(key, kdoms_classes_count[class2][key]))
                    i += 1

    



def get_kdoms(json_object, k):
    """
    Scan cluster for k-doms
    return : list of k-doms (with hmm_list indices)
    """
    kdoms = []

    # collect "dom-sequence" per record
    dom_seq = []
    for cluster in json_object["clusters"]:
        for gene in cluster["genes"]:
            if "pfams" in gene:
                for pfam in gene["pfams"]:
                    dom_seq.append(pfam["name"])

    # scan k-doms
    i = 0
    while ((i + k) < len(dom_seq)):
        kdom = [dom_seq[ds] for ds in range(i, i+k)]
        kdoms.append(kdom)
        i += 1

    return kdoms


def get_class(json_object):
    classes = ""
    for cluster in json_object["clusters"]:
        if len(classes) > 0:
            classes += "+"
        classes += "-".join(cluster["class"])
    return classes


def get_class_base(class_name, db_type):
    return ["{}:{}".format(db_type, cn) for cn in class_name.split("-")] # use classes as it is

if __name__ == "__main__":
    main()