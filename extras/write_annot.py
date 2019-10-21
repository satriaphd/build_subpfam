from sys import argv
import os
import random

domain_list_txt = argv[1]
clades_folder = argv[2]
output_folder = argv[3]

domains = []
with open(domain_list_txt, "r") as dl:
    for line in dl.readlines():
        domains.append(line.rstrip().split("\t")[0])

col = {}
for i, domain in enumerate(domains):
    clade_file = os.path.join(clades_folder, "{}.txt".format(domain))
    output_file = os.path.join(output_folder, "{}.annot.txt".format(domain))
    with open(output_file, "w") as a:
        print("writing {}".format(output_file))
        a.write("TREE_COLORS\nSEPARATOR SPACE\nDATA\n")
        with open(clade_file, "r") as c:
            for line in c.readlines():
                line = line.rstrip()
                line_cols = line.split("\t")
                acc = line_cols[0]
                fam = line_cols[1]
                if fam not in col:
                    r = lambda: random.randint(0,255)
                    col[fam] = 'rgb({},{},{})'.format(r(),r(),r())
                a.write("{} label_background {}\n".format(acc, col[fam]))