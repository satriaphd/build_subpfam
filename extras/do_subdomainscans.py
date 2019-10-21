from sys import argv
import os

aligned_hits_folder = argv[1]
domain_list_txt = argv[2]
subdomain_folder = argv[3]
output_folder = argv[4]

domains = []
with open(domain_list_txt, "r") as dl:
    for line in dl.readlines():
        domains.append(line.rstrip().split("\t")[0])

import subprocess
for i, domain in enumerate(domains):
    domtable_path = os.path.join(output_folder, "{}.domtable".format(domain))
    hmm_path = os.path.join(subdomain_folder, "{}-subdomains.hmm".format(domain))
    fasta_path = os.path.join(aligned_hits_folder, "{}.fa".format(domain))
    command = "hmmscan -T 1 --domT 1 --incT 1 --incdomT 1 --domtblout {} {} {}".format(domtable_path, hmm_path, fasta_path)
    print("{}/{}: {}".format(i + 1, len(domains) + 1, command))
    try:
        subprocess.check_output(command, shell=True)
    except:
        continue