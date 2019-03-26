from Bio import SeqIO
from Bio import SearchIO
from sys import argv
import os

domtables_folder = argv[1]
domain_list_txt = argv[2]
subdomain_models_folder = argv[3]
output_folder = argv[4]
classes_txt = argv[5]

domains = []
with open(domain_list_txt, "r") as dl:
    for line in dl.readlines():
        domains.append(line.rstrip().split("\t")[0])

# hack to fix class assignment
classes_all = {}
with open(classes_txt, "r") as cf:
    for line in cf.readlines():
        cols = line.rstrip().split("\t")
        classes_all[cols[0]] = cols[1]

for i, domain in enumerate(domains):
    output_file = os.path.join(output_folder, "{}-subdomainhits.tsv".format(domain))
    if os.path.isfile(output_file):
        print("{}/{}: output file exists: {}! skipping...".format(i + 1, len(domains), output_file))
    else:
        features = {}
        classes = {}
        dbs = {}
        clades = []
        domtable_file = os.path.join(domtables_folder, "{}.domtable".format(domain))
        model_file = os.path.join(subdomain_models_folder, "{}-subdomains.hmm".format(domain))
        print("{}/{}: Parsing domtable {}".format(i + 1, len(domains), domtable_file))
        with open(model_file, "r") as mf:
            for line in mf.readlines():
                if line.startswith("NAME"):
                    clades.append(line.rstrip().split(" ")[-1])
        for runresult in SearchIO.parse(domtable_file, 'hmmscan3-domtab'):
            id_cols = runresult.id.split("|")
            bgc_id = id_cols[1]
            db_id = id_cols[0]
            #class_id = id_cols[5]
            class_id = classes_all[bgc_id]
            scores = {}
            best_score = -1
            for hsp in sorted(runresult.hsps, key=lambda hsp: -1 * hsp.bitscore):
                if best_score < 0:
                    best_score = hsp.bitscore
                if hsp.hit_id not in scores:
                    scores[hsp.hit_id] = round(hsp.bitscore / best_score, 3)
            hit_feature = []
            for clade in clades:
                if clade in scores:
                    hit_feature.append(scores[clade])
                else:
                    hit_feature.append(0)
            classes[bgc_id] = class_id
            dbs[bgc_id] = db_id
            if bgc_id not in features:
                features[bgc_id] = [0 for c in range(0, len(clades))]
            for c, v in enumerate(features[bgc_id]):
                if v < hit_feature[c]:
                    features[bgc_id][c] = hit_feature[c]
        with open(output_file, "w") as of:
            of.write("bgc_id\tdb\tclass\t{}\n".format("\t".join([clade for clade in clades])))
            for bgc_id in features:
                of.write("{}\t{}\t{}\t{}\n".format(bgc_id, dbs[bgc_id], classes[bgc_id], "\t".join([str(val) for val in features[bgc_id]])))