#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Given tree newick files, parse and automatically split each tree
into clades of similar size.

usage: extract_clades.py <trees_folder> <output_folder> <midroot_folder>
---
- trees_folder: folder containing input newick files
- output_folder: resulting clade text files will be stored here
- midroot_folder: if given, will save preprocessed trees used to call the
              clades here

=> required: ete3 (http://etetoolkit.org/download/)
"""

from sys import argv
from os import path
import glob
from ete3 import PhyloTree


def main():
    trees_folder = argv[1]
    output_folder = argv[2]
    midroot_folder = None
    if len(argv) > 3:
        midroot_folder = argv[3]

    tree_files = glob.glob(path.join(trees_folder, "*.newick"))
    commands = []
    for i, tree_path in enumerate(tree_files):
        output_path = "{}.clades.txt".format(path.join(output_folder, path.splitext(path.basename(tree_path))[0]))
        assert not path.exists(output_path)
        midroot_path = None
        if midroot_folder is not None:
            midroot_path = "{}.newick".format(path.join(midroot_folder, path.splitext(path.basename(tree_path))[0]))
            assert not path.exists(midroot_path)
        clades = extract_clades(tree_path, midroot_path)
        with open(output_path, "w") as th:
            for c, clade in enumerate(clades):
                for name in clade:
                    th.write("{}\t{}\n".format(name, c + 1))


def extract_clades(newick_file, processed_newick_out = None):
    """ the outer logic for tree splitting """
    # preprocess tree
    print("Pre-processing tree ({})".format(newick_file))
    tree = PhyloTree(newick_file)
    R = tree.get_midpoint_outgroup()
    tree.set_outgroup(R)
    tree.ladderize()
    tree.convert_to_ultrametric()
    if (processed_newick_out is not None):
        tree.write(format=1, outfile=processed_newick_out)
    # calculate clades
    print("Calling clades ({})".format(newick_file))
    def get_branch_length(node):
        for l in node:
            return l.get_distance(node)
    len_tree = len(tree)
    dist_tree = get_branch_length(tree)
    def condition_discard(node, tree):
        return (len(node) < 3)
    def condition_ok(node, tree):
        return len(node) < max(10, len_tree / 50)
    branches = get_pruned_branch(tree, tree, condition_discard, condition_ok, [])
    clades = {}
    for i, branch in enumerate(sorted(branches, key=lambda nodes: -1 * len(nodes))):
        clades[str(i + 1)] = [node.name for node in branch]
    return clades


def get_pruned_branch(node, tree, condition_discard, condition_ok, results):
    """ inner function, called recursively to call clades according to specific rules """
    if condition_discard(node, tree):
        pass
    elif condition_ok(node, tree):
        results.append(node)
    else:
        for childbranch in node.children:
            results = get_pruned_branch(childbranch, tree, condition_discard, condition_ok, results)
    return results


if __name__ == "__main__":
    main()