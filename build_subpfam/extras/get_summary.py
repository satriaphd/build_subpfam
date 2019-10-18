import os
import json
from sys import argv
from glob import glob

res_folder = argv[1]

pres_k1_files = glob(os.path.join(res_folder,"**/*.k1.*-top100.txt"), recursive=True)
#pres_k2_files = glob(os.path.join(res_folder,"**/*.k2.*-top100.txt"), recursive=True)
count_k1_files = glob(os.path.join(res_folder,"**/*.k1.*-top100-count.txt"), recursive=True)
#count_k2_files = glob(os.path.join(res_folder,"**/*.k2.*-top100-count.txt"), recursive=True)

pres_k1_top5s = {}
for f in pres_k1_files:
    with open(f, "r") as fr:
        i = 0
        for line in fr.readlines():
            if i > 4:
                break
            dom = line.split("\t")[0]
            if dom not in pres_k1_top5s:
                pres_k1_top5s[dom] = 0
            pres_k1_top5s[dom] += 1
            i += 1
with open("pres_k1_top5s.txt", "w") as fw:
    for key in sorted(pres_k1_top5s, key=pres_k1_top5s.get, reverse=True):
        fw.write("{}\t{}\n".format(key, pres_k1_top5s[key]))

pres_k1_min2in1to10 = {}
for f in pres_k1_files:
    with open(f, "r") as fr:
        i = 0
        for line in fr.readlines():
            if i > 9:
                break
            dom = line.split("\t")[0]
            if dom in pres_k1_top5s:
                i += 1
                continue
            if dom not in pres_k1_min2in1to10:
                pres_k1_min2in1to10[dom] = 0
            pres_k1_min2in1to10[dom] += 1
            i += 1
with open("pres_k1_min2in1to10.txt", "w") as fw:
    for key in sorted(pres_k1_min2in1to10, key=pres_k1_min2in1to10.get, reverse=True):
        if pres_k1_min2in1to10[key] < 2:
            break
        fw.write("{}\t{}\n".format(key, pres_k1_min2in1to10[key]))

#count_k1_top10s = {}
#for f in count_k1_files:
#    with open(f, "r") as fr:
#        i = 0
#        for line in fr.readlines():
#            if i > 4:
#                break
#            dom = line.split("\t")[0]
#            if dom not in count_k1_top10s:
#                count_k1_top10s[dom] = 0
#            count_k1_top10s[dom] += 1
#            i += 1
#with open("count_k1_top10s.txt", "w") as fw:
#    for key in sorted(count_k1_top10s, key=count_k1_top10s.get, reverse=True):
#        fw.write("{}\t{}\n".format(key, count_k1_top10s[key]))