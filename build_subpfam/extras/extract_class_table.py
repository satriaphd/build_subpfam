import sys
import os
from glob import glob
from sys import argv
import json

json_folder = argv[1]
output_file = argv[2]

json_files = []
if os.path.isfile(json_folder):
    json_files = [json_folder]
else:
    json_files = glob(os.path.join(json_folder,"**/*.json"), recursive=True)

with open(output_file, "w") as mf:
    for i, json_file in enumerate(json_files):
        json_object = {}
        with open(json_file, "r") as json_text:
            try:                
                json_object = json.loads(json_text.read())
                for c, cluster in enumerate(json_object["clusters"]):
                    clasname = "hybrid"
                    if len(json_object["clusters"][c]["class"]) == 1:
                        clasname = json_object["clusters"][c]["class"][0]
                    mf.write("{}\t{}\n".format(json_object["filename"], clasname))
                    print("{}/{} {}".format(i, len(json_files), json_file))
            except:
                print("Error: failed to load json file {}".format(json_file))
                continue