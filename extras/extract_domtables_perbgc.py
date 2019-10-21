from sys import argv
import os
import sys

domtables_folder = argv[1]
domain_list_txt = argv[2]
output_folder = argv[3]

domains = []
with open(domain_list_txt, "r") as dl:
    for line in dl.readlines():
        domains.append(line.rstrip().split("\t")[0])

for i, domain in enumerate(domains):
    domtable_file = os.path.join(domtables_folder, "{}.domtable".format(domain))
    with open(domtable_file, "r") as dt_domain:
        print("parsing domtable ({}/{}) {}".format(i + 1, len(domains), domtable_file), end="\r")
        lines = dt_domain.readlines()
        if lines[-1].rstrip() != "# [ok]":
            print("Error: domtable {} is not complete".format(domtable_file))
            sys.exit(1)
        else:
            for l, line in enumerate(lines):
                print("parsing domtable ({}/{}) {} ({}/{})".format(i + 1, len(domains), domtable_file, l, len(lines)), end="\r")
                if not line.startswith("#"):
                    cols = line.rstrip().split()
                    if len(cols) != 23:
                        print("Error: domtable {} is incorrectly formatted at line {}".format(domtable_file, l))
                        sys.exit(1)
                    else:
                        accs = cols[3].split("|")
                        if len(accs) != 6:
                            print("Error: domtable {} is incorrectly formatted at line {}".format(domtable_file, l))
                            sys.exit(1)
                        else:
                            with open(os.path.join(output_folder, "{}|{}.domtable".format(accs[0], accs[1])), "a") as bgct:
                                bgct.write("{}".format(line))