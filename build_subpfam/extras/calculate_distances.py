import numpy as np
import time
        
features = []
with open("./tables/merged_dataset.tsv", "r") as d:
    i = 0
    lines = d.readlines()
    for i, line in enumerate(lines):
        if i > 0:
            cols = line.rstrip().split("\t")
            print("{}/{}: {}             ".format(i, len(lines), cols[0]), end="\r")
            f_dom = [min(int(val), 1) for val in cols[3:1791]]
            f_subdom = [float(val) for val in cols[1791:8648]]
            features.append((f_dom, f_subdom))

def calc_jacdist(i, j):
    x = features[i][0]
    y = features[j][0]
    x = np.asarray(x, np.bool) # Not necessary, if you keep your data
    y = np.asarray(y, np.bool) # in a boolean array already!
    return 1.00 - (np.double(np.bitwise_and(x, y).sum()) / np.double(np.bitwise_or(x, y).sum()))

def calc_wjacdist(i, j):
    x = features[i][0]
    y = features[j][0]
    return 1.00 - np.sum(np.minimum(x, y))/np.sum(np.maximum(x, y))

print("")

dist_dom = [[] for i in range(0, len(features))]
dist_subdom = [[] for i in range(0, len(features))]
for i in range(0, len(features)):
    print("Calc distance: {}/{}             ".format(i, len(features)), end="\r")
    for j in range(0, i + 1):
        #start = time.time()
        dist_dom[i].append(calc_jacdist(i, j))
        dist_subdom[i].append(calc_wjacdist(i, j))
        #print(time.time() - start)

with open("./tables/merged_dataset.dist_domain.txt", "w") as oo:
    print("Writing output: domain features")
    for dist in dist_dom:
        oo.write("{}\n".format("\t".join(["{:.3f}".format(val) for val in dist])))

with open("./tables/merged_dataset.dist_subdomain.txt", "w") as oo:
    print("Writing output: subdomain features")
    for dist in dist_subdom:
        oo.write("{}\n".format("\t".join(["{:.3f}".format(val) for val in dist])))

