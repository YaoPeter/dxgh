#!/usr/bin/python
import sys
import csv
from scipy import stats

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: " + sys.argv[0] + " <csv_file_path>")
        sys.exit(1)

    with open(sys.argv[1], "rb") as csv_file:
        reader = csv.DictReader(csv_file)
        dataset = map(lambda x: {"d": int(x["depression"]), "g": int(x["gene"]), "s": int(x["stressful life events"])},
                      reader)
        for g in range(2):
            gene_dataset = filter(lambda x: x["g"] == g, dataset)
            for s in range(100):
                subset = filter(lambda x: x["s"] >= s, gene_dataset)
                if (len(subset) < 10):  # finished when too few samples left
                    break
                depression = map(lambda x: x["d"], subset)
                stressful = map(lambda x: x["s"], subset)
                try:
                    cor, pval = stats.pearsonr(depression, stressful)
                except Exception, e:
                    print e
                    continue
                print("when gene=%d and stressful events>=%d: cor=%7.4f, pval_0=%7.5f, #=%d"
                      % (g, s, cor, pval, len(depression)))
